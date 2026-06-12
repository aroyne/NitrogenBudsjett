#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modifisert MC-VERSJON: Beregner nitrogenflyt for Hydrosfæren (HY) og Akvakultur (AC).
Sikret full konsistens med sentral distribusjonstrekking og felles delte strømmer.
"""
import pandas as pd
import numpy as np

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years
)
from calculations.shared_flow_calculations import (
    find_aquaculture_production,
    find_treated_wastewater_discharge
)

def execute_calculations_hy(preloaded_data, current_params, dataset_noise):
    """
    Hovedfunksjon for HY-poolen. Kjører alle underberegninger.
    Alle distribusjoner og støyfaktorer trekkes sentralt før denne kjøres.
    """
    results = []
    
    # Et internt register for å spore tilførsler år for år (brukes til historisk retensjon)
    years_sorted = sorted(list(EXPECTED_YEARS))
    outflow_tracker = pd.DataFrame({'value': 0.0, 'entries': 0}, index=years_sorted)
    
    # 1. Sjekk kritiske fellesdata og hent delte strømmer (Shared flows)
    if 'aqua_modern' not in preloaded_data or 'aqua_old' not in preloaded_data:
        raise ValueError("[KRITISK] Akvakulturdata ('aqua_modern'/'aqua_old') mangler i preloaded_data!")
        
    aqua_production_dict = find_aquaculture_production(
        preloaded_data.get('aqua_modern'), 
        preloaded_data.get('aqua_old'), 
        current_params, 
        dataset_noise
    )
    
    # 2. Kjør spesialstrømmer for hydrosfære og akvakultur
    _add_inflow_to_coastal_waters(results, preloaded_data, current_params, dataset_noise, outflow_tracker)
    _add_wild_shellfish_and_macroalgae(results, preloaded_data, current_params, dataset_noise)
    _add_surface_water_emissions(results, preloaded_data, current_params, dataset_noise, outflow_tracker)
    _add_wild_fish_catch(results, preloaded_data, current_params, dataset_noise)
    _add_aquaculture_internal_flows(results, aqua_production_dict, current_params)
    
    return results


# =============================================================================
# UNDERFUNKSJONER FOR HYDROSFIÆRE- OG HAVBRUKSSTRØMMER
# =============================================================================

def _add_inflow_to_coastal_waters(results, preloaded_data, current_params, dataset_noise, outflow_tracker):
    """
    Beregner ferskvannstilførsel til kysten fra TEOTIL/Miljødirektoratet.
    Krasjer hardt dersom filer eller støyfaktorer mangler.
    """
    flow_code = 'HY.SW-HY.CW-Inflow to coastal waters-Nmix'
    collected_years = set()
    
    key_teotil = 'TEOTIL'
    if not dataset_noise or key_teotil not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_teotil}' mangler i dataset_noise for {flow_code}!")
    noise_teotil = dataset_noise[key_teotil]['value']
    
    if 'hy_ssb_05280_raw' not in preloaded_data or 'hy_utslipp_avlop_raw' not in preloaded_data:
        raise ValueError(f"[KRITISK] Avløpsdata mangler i preloaded_data for felles avløpsstrøm i {flow_code}!")
        
    ww_discharge_dict = find_treated_wastewater_discharge(
        df_05280=preloaded_data.get('hy_ssb_05280_raw'),
        df_utslipp=preloaded_data.get('hy_utslipp_avlop_raw'),
        current_params=current_params,
        dataset_noise=dataset_noise,
        expected_years=EXPECTED_YEARS
    )
    
    # --- Tidlige år (Miljødirektoratet-ark, 1990-2012-ish) ---
    df_kyst = preloaded_data.get('hy_kyst_tilforsel')
    if df_kyst is None:
        raise ValueError(f"[KRITISK] 'hy_kyst_tilforsel' mangler i preloaded_data for {flow_code}!")
        
    for i in range(len(df_kyst)):
        val_at_col0 = str(df_kyst.iloc[i, 0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        try:
            year = int(float(val_at_col0))
            if year in EXPECTED_YEARS:
                collected_years.add(year)
                val = (float(df_kyst.iloc[i, 3]) + float(df_kyst.iloc[i, 4]) + 
                       float(df_kyst.iloc[i, 5]) + float(df_kyst.iloc[i, 6])) / 1000.0
                val *= noise_teotil
                
                outflow_tracker.loc[year, 'entries'] = 1
                outflow_tracker.loc[year, 'value'] = val
                
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': val,
                    'comment': 'ok (Tidlig tidsserie, MC-støy lagt på)',
                    'data_sources': 'Miljødirektoratet / TEOTIL'
                })
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil ved prosessering av df_kyst på rad {i}: {e}")

    # --- Nyere år (TEOTIL3 matriser) ---
    df_t3_coast = preloaded_data.get('hy_teotil3_to_coast')
    df_t3_source = preloaded_data.get('hy_teotil3_by_source')
    
    if df_t3_coast is None or df_t3_source is None:
        raise ValueError(f"[KRITISK] En eller begge TEOTIL3-matriser mangler i preloaded_data for {flow_code}!")
        
    for r in range(len(df_t3_coast)):
        val_at_col0 = str(df_t3_coast.iloc[r, 0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        try:
            year = int(float(val_at_col0))
            if year in EXPECTED_YEARS:
                collected_years.add(year)
                val = (float(df_t3_coast.iloc[r, 1]) / 1000.0) - (float(df_t3_source.iloc[r, 3]) / 1000.0)
                val *= noise_teotil
                
                if year in ww_discharge_dict:
                    val -= ww_discharge_dict[year]
                
                val = max(0.0, val)
                outflow_tracker.loc[year, 'entries'] = 1
                outflow_tracker.loc[year, 'value'] = val
                
                existing_posts = [p for p in results if p['flow_name'] == flow_code and p['year'] == year]
                if existing_posts:
                    existing_posts[0]['value'] = val
                    existing_posts[0]['comment'] = 'ok (Overstyrt med nyere TEOTIL3, korrigert for avløp)'
                else:
                    results.append({
                        'flow_name': flow_code, 'year': year, 'value': val,
                        'comment': 'ok (TEOTIL3 matrise, korrigert for avløp)',
                        'data_sources': 'NIVA TEOTIL3'
                    })
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil ved prosessering av TEOTIL3-matriser på rad {r}: {e}")

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_wild_shellfish_and_macroalgae(results, preloaded_data, current_params, dataset_noise):
    """
    Beregner nitrogen ut med villfanget skalldyr og makroalger.
    """
    flow_code = 'HY.CW-MP.FP-Shellfish-Nmix'
    collected_years = set()
    
    fish_N_frac = float(current_params.get("fish_N_frac"))
    seaweed_N_frac = float(current_params.get("seaweed_N_frac"))
    
    key_fisk = 'Fiskeridirektoratet'
    if not dataset_noise or key_fisk not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_fisk}' mangler i dataset_noise for {flow_code}!")
    noise_fisk = dataset_noise[key_fisk]['value']

    # Moderne data
    df_art = preloaded_data.get('hy_art_raw')
    if df_art is None:
        raise ValueError(f"[KRITISK] 'hy_art_raw' mangler i preloaded_data for {flow_code}!")
        
    for col in range(2, df_art.shape[1]):
        val_at_cell = str(df_art.iloc[0, col]).strip()
        if val_at_cell.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        try:
            year = int(float(val_at_cell))
            if year in EXPECTED_YEARS:
                collected_years.add(year)
                val = 0.0
                shellfish_total_row = 35  
                algae_total_row = 41      
                
                if not pd.isna(df_art.iloc[shellfish_total_row, col]):
                    val += (float(df_art.iloc[shellfish_total_row, col]) / 1000.0) * fish_N_frac
                    
                if not pd.isna(df_art.iloc[algae_total_row, col]):
                    val += (float(df_art.iloc[algae_total_row, col]) / 1000.0) * seaweed_N_frac
                    
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': max(0.0, val * noise_fisk),
                    'comment': 'ok (MC-støy lagt på)', 'data_sources': 'Fiskeridirektoratet'
                })
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil i moderne fiskeridata, kolonne {col}: {e}")

    # Historiske data (før 1994)
    df_fiske_old = preloaded_data.get('hy_fiske_old_raw')
    if df_fiske_old is None:
        raise ValueError(f"[KRITISK] 'hy_fiske_old_raw' mangler i preloaded_data for {flow_code}!")
        
    for r in range(len(df_fiske_old)):
        val_at_col0 = str(df_fiske_old.iloc[r, 0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        try:
            year = int(float(val_at_col0))
            if year in EXPECTED_YEARS:
                collected_years.add(year)
                val = (float(df_fiske_old.iloc[r, 3]) * fish_N_frac) + (float(df_fiske_old.iloc[r, 4]) * seaweed_N_frac)
                
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': max(0.0, val * noise_fisk),
                    'comment': 'ok (Historiske data, MC-støy lagt på)', 'data_sources': 'Fiskeridirektoratet'
                })
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil i historisk fiskeridata på rad {r}: {e}")

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_surface_water_emissions(results, preloaded_data, current_params, dataset_noise, outflow_tracker):
    """
    Beregner ferskvannsretensjon og tilhørende atmosfæriske emisjoner av N2 og N2O.
    Bruker målt TEOTIL3-retensjon der det finnes, og faller tilbake på historisk kalsium 
    med EKSTRA usikkerhet for interpolering på de resterende årene.
    """
    flow_n2 = 'HY.SW-AT.AT-Emissions-N2'
    flow_n2o = 'HY.SW-AT.AT-Emissions-N2O'
    collected_years = set()
    
    fraction_N2O = float(current_params.get("surface_water_fraction_to_N2O"))
    ret_frac = float(current_params.get("surface_water_retention_fraction"))
    
    key_teotil = 'TEOTIL'
    key_interp = 'trend interpolation'
    
    # Sjekk at primærstøy eksisterer
    if not dataset_noise or key_teotil not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_teotil}' mangler i dataset_noise for retensjonsberegning!")
    noise_teotil = dataset_noise[key_teotil]['value']

    # 1. Modellering ut fra målt retensjon i TEOTIL3
    df_t3_ret = preloaded_data.get('hy_teotil3_retention')
    if df_t3_ret is None:
        raise ValueError(f"[KRITISK] 'hy_teotil3_retention' mangler i preloaded_data!")
        
    for r in range(len(df_t3_ret)):
        val_at_col0 = str(df_t3_ret.iloc[r, 0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        try:
            year = int(float(val_at_col0))
            if year in EXPECTED_YEARS:
                collected_years.add(year)
                base_ret_val = (float(df_t3_ret.iloc[r, 1]) / 1000.0) * noise_teotil
                
                results.append({'flow_name': flow_n2, 'year': year, 'value': max(0.0, base_ret_val * (1.0 - fraction_N2O)),
                                'comment': 'ok (TEOTIL3 retensjonsmatrise)', 'data_sources': 'NIVA TEOTIL3'})
                results.append({'flow_name': flow_n2o, 'year': year, 'value': max(0.0, base_ret_val * fraction_N2O),
                                'comment': 'ok (TEOTIL3 retensjonsmatrise)', 'data_sources': 'NIVA TEOTIL3'})
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Kunne ikke prosessere retensjonsmatrise på rad {r}: {e}")

    # 2. Historisk beregning basert på fast retensjonsbrøk + interpoleringsstøy for resterende år
    missing_years = EXPECTED_YEARS - collected_years
    if missing_years:
        if not dataset_noise or key_interp not in dataset_noise:
            raise KeyError(
                f"[KRITISK] Forhistoriske år krever interpolering, men støy-nøkkelen '{key_interp}' "
                f"mangler i dataset_noise for retensjonsberegning!"
            )
        noise_interp = dataset_noise[key_interp]['value']
        
        for year in sorted(missing_years):
            # Hvis vi ikke engang har outflow-data for dette året, må vi krasje
            if outflow_tracker.loc[year, 'entries'] != 1:
                raise ValueError(f"[KRITISK] Ingen inngående eller utgående ferskvannsdata funnet for året {year}. Kan ikke interpolere retensjon!")
                
            collected_years.add(year)
            
            # Baklengs kalkyle: Retensjon = Outflow * ret_frac / (1 - ret_frac)
            hist_ret_val = outflow_tracker.loc[year, 'value'] * ret_frac / (1.0 - ret_frac)
            
            # Legger på den ekstra usikkerheten for interpolering/modellering her
            hist_ret_val *= noise_interp
            
            results.append({'flow_name': flow_n2, 'year': year, 'value': max(0.0, hist_ret_val * (1.0 - fraction_N2O)),
                            'comment': 'modeled (Fast retensjonsbrøk + interpoleringsstøy)', 'data_sources': 'Beregningsmodell'})
            results.append({'flow_name': flow_n2o, 'year': year, 'value': max(0.0, hist_ret_val * fraction_N2O),
                            'comment': 'modeled (Fast retensjonsbrøk + interpoleringsstøy)', 'data_sources': 'Beregningsmodell'})

    # Sluttkontroll
    report_missing_years(flow_n2, EXPECTED_YEARS - collected_years, results)

def _add_wild_fish_catch(results, preloaded_data, current_params, dataset_noise):
    """
    Beregner marint uttak av nitrogen via tradisjonelt saltvannsfiske (villfangst).
    """
    flow_code = 'HY.CW-MP.FP-Fish (wild catch)-Nmix'
    collected_years = set()
    
    fish_N_frac = float(current_params.get("fish_N_frac"))
    key_fisk = 'Fiskeridirektoratet'
    if not dataset_noise or key_fisk not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_fisk}' mangler i dataset_noise for {flow_code}!")
    noise_fisk = dataset_noise[key_fisk]['value']

    df_art = preloaded_data.get('hy_art_raw')
    if df_art is None:
        raise ValueError(f"[KRITISK] 'hy_art_raw' mangler i preloaded_data for villfisk-beregning!")
        
    for col in range(2, df_art.shape[1]):
        val_at_cell = str(df_art.iloc[0, col]).strip()
        if val_at_cell.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        try:
            year = int(float(val_at_cell))
            if year in EXPECTED_YEARS:
                collected_years.add(year)
                val = 0.0
                for r_idx in [15, 20, 26, 38, 41]:
                    if not pd.isna(df_art.iloc[r_idx, col]):
                        val += float(df_art.iloc[r_idx, col])
                        
                val_kt_N = (val / 1000.0) * fish_N_frac * noise_fisk
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': max(0.0, val_kt_N),
                    'comment': 'ok (MC-støy lagt på)', 'data_sources': 'Fiskeridirektoratet'
                })
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil i moderne villfisk-kolonne {col}: {e}")

    df_fiske_old = preloaded_data.get('hy_fiske_old_raw')
    if df_fiske_old is None:
        raise ValueError(f"[KRITISK] 'hy_fiske_old_raw' mangler i preloaded_data for villfisk-beregning!")
        
    for r in range(len(df_fiske_old)):
        val_at_col0 = str(df_fiske_old.iloc[r, 0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        try:
            year = int(float(val_at_col0))
            if year in EXPECTED_YEARS:
                collected_years.add(year)
                val = (float(df_fiske_old.iloc[r, 1]) + float(df_fiske_old.iloc[r, 2])) * fish_N_frac * noise_fisk
                
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': max(0.0, val),
                    'comment': 'ok (Historiske data, MC-støy lagt på)', 'data_sources': 'Fiskeridirektoratet'
                })
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil i historisk villfisk-data på rad {r}: {e}")

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_aquaculture_internal_flows(results, aquaculture_production_dict, current_params):
    """
    Beregner akvakultur-interne og utgående strømmer ut fra den felles produksjonsmatrisen.
    """
    flow_harvest = 'HY.AC-MP.FP-Coastal fish and seafood-Nmix'
    flow_waste = 'HY.AC-HY.CW-Waste feed-Nmix'
    flow_excretia = 'HY.AC-HY.CW-Excretia-Nmix'
    
    collected_years = set()
    
    prot_ret = float(current_params.get("aquafeed_N_retention"))
    feed_waste = float(current_params.get("aquafeed_waste_fraction"))

    for year, fish_harvested_N in aquaculture_production_dict.items():
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            
            # 1. Slaktefisk ut av poolen
            results.append({
                'flow_name': flow_harvest, 'year': year, 'value': max(0.0, fish_harvested_N),
                'comment': 'ok (Beregnet fra felles shared flow produksjon)', 'data_sources': 'Fiskeridirektoratet'
            })
            
            # 2. Fôrspill og fekalier til kystvann
            total_feed_N = (fish_harvested_N / prot_ret) if prot_ret > 0 else 0.0
            waste_val = total_feed_N * feed_waste / (1.0 - feed_waste) if feed_waste < 1 else 0.0
            
            results.append({
                'flow_name': flow_waste, 'year': year, 'value': max(0.0, waste_val),
                'comment': 'ok (Beregnet ut fra retensjonsfaktorer)', 'data_sources': 'Mass balanse'
            })
            
            # 3. Metabolsk ekskresjon (oppløst N) til kystvann
            excretia_val = total_feed_N * (1.0 - prot_ret - feed_waste)
            results.append({
                'flow_name': flow_excretia, 'year': year, 'value': max(0.0, excretia_val),
                'comment': 'ok (Beregnet ut fra retensjonsfaktorer)', 'data_sources': 'Mass balanse'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_harvest, missing_years, results)