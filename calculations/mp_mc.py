#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
MC-VERSJON: Beregner nitrogenflyt for Market & Processing (MP).
Rådata ligger i preloaded_data, mens støyfaktorer for hvert datasett sendes inn via dataset_noise.
"""
import pandas as pd
import numpy as np

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years
)
from calculations.shared_flow_calculations import (
    find_aquaculture_production,
    find_feedstock_fuel,
    find_food_industry_waste,
    find_industrial_round_wood,
    find_industrial_waste_fuels,
    find_other_goods_export,
    find_other_goods_import,
    find_other_industry_waste,
    find_other_industry_wastewater,
    find_op_untreated_wastewater,
    find_recycling,
    find_industrial_crop_products,
    find_non_edible_animal_products
    )


def execute_calculations_mp(preloaded_data, current_params, dataset_noise, current_trade_factors=None):
    """
    Hovedfunksjon for MP-poolen (MC). Mottar denne rundens parameter- og støyordbøker.
    Krasjer umiddelbart hvis kritiske inndata mangler.
    """
    results = []
    
    # Kaller den første delberegningen for såkorn og plantemateriale
    _add_seeds_and_planting_material_mc(results, preloaded_data, current_params, dataset_noise)
    _add_farm_animal_feed_mc(results, preloaded_data, current_params, dataset_noise)
    _add_food_industry_waste_mc(results, preloaded_data, current_params, dataset_noise)
    _add_food_industry_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    
    
    return results


def _add_seeds_and_planting_material_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Beregner nitrogenmengde i innkjøpt såkorn og plantemateriale (MP -> AG).
    Data hentes fra NIBIO Totalkalkylen (NibioStatistics-5.xlsx).
    """
    flow_code = 'MP.FP-AG.SM-Seeds and planting material -Nmix'
    collected_years = set()
    data_sources = 'NIBIO Totalkalkylen'
    comment = 'ok (MC-støy lagt på)'
    
    # 1. Hent parametere for protein- og nitrogenfraksjoner fra current_params
    seed_cereal_prot  = float(current_params.get("seed_cereal_protein_frac"))
    seed_cereal_fac   = float(current_params.get("seed_cereal_protein_to_N"))
    seed_oil_prot     = float(current_params.get("seed_oilseed_protein_frac"))
    seed_pea_prot     = float(current_params.get("seed_pea_protein_frac"))
    seed_grass_prot   = float(current_params.get("seed_grass_protein_frac"))
    seed_rootveg_prot = float(current_params.get("seed_rootveg_protein_frac"))
    Jones             = float(current_params.get("Jones_factor"))
    
    # Beregn N-fraksjoner (protein_frac / protein_to_N_factor)
    seed_cereal_N  = seed_cereal_prot / seed_cereal_fac
    seed_oil_N     = seed_oil_prot / Jones
    seed_pea_N     = seed_pea_prot / Jones
    seed_grass_N   = seed_grass_prot / Jones
    seed_rootveg_N = seed_rootveg_prot / Jones
    
    # 2. Hent støyfaktor for Totalkalkylen
    key_dataset = 'Totalkalkylen'
    if not dataset_noise or key_dataset not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_dataset}' mangler i dataset_noise for {flow_code}!")
    noise_totalkalkylen = dataset_noise[key_dataset]['value']
    
    # Ordbok for å akkumulere verdiene per år på tvers av alle fanene
    year_values = {}
    
    # Definer fanene vi skal hente fra preloaded_data og tilhørende N-fraksjon
    sheets_to_process = [
        ('mp_sau_saakorn_raw', seed_cereal_N),       # 'Sum innkjøpt såkorn'
        ('mp_oljefroe_raw', seed_oil_N),             # 'Oljefrø til modning'
        ('mp_erter_raw', seed_pea_N),                # 'Erter'
        ('mp_engfroe_raw', seed_grass_N),            # 'Sum engfrø'
        ('mp_rotvekst_groennsak_raw', seed_rootveg_N) # 'Sum rotvekst- og grønnsakfrø'
    ]
    
    for preload_key, n_fraction in sheets_to_process:
        df_sheet = preloaded_data.get(preload_key)
        if df_sheet is None:
            raise ValueError(f"[KRITISK] '{preload_key}' mangler i preloaded_data for {flow_code}!")
            
        # Vi går gjennom radene dynamisk i stedet for fast range(27,69) for økt robusthet.
        # Men vi sjekker kolonne 0 for gyldige årstall.
        for r in range(len(df_sheet)):
            val_col0 = str(df_sheet.iloc[r, 0]).strip()
            
            # Hopp over overskrifter eller tomme celler i årskolonnen
            if val_col0.lower() in ['year', 'år', 'årstall', 'nan', '', 'none']:
                continue
                
            try:
                year = int(float(val_col0))
                if year in EXPECTED_YEARS:
                    # Hent mengde i tonn (kolonne 1 / B)
                    raw_val = df_sheet.iloc[r, 1]
                    if pd.isna(raw_val) or str(raw_val).strip().lower() in ['none', 'nan', '']:
                        tonn_verdi = 0.0
                    else:
                        tonn_verdi = float(raw_val)
                    
                    # Konverterer: tonn -> kt (* 1e-3), deretter * N-fraksjon
                    value_kt_N = tonn_verdi * 1e-3 * n_fraction
                    year_values[year] = year_values.get(year, 0.0) + value_kt_N
                    
            except (ValueError, TypeError):
                # Hvis vi treffer tekst eller fotnoter i bunnen av arket, hopper vi bare over raden
                continue

    # 3. Pakk ut de akkumulerte verdiene, legg på MC-støy og lagre i results
    for year, total_val in year_values.items():
        collected_years.add(year)
        
        # Legg på denne rundens unike Monte Carlo-støy for Totalkalkylen
        final_val = total_val * noise_totalkalkylen
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': max(0.0, final_val),
            'comment': comment,
            'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_farm_animal_feed_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Beregner innenlandsk nitrogenflyt i kraftfôr til husdyr (MP -> AG).
    """
    flow_code = 'MP.FP-AG.MM-Farm animal feed-Nmix'
    collected_years = set()
    
    # 1. Hent parametere
    N_content_carb = float(current_params.get("feed_carb_N_frac"))
    N_content_prot = float(current_params.get("feed_prot_N_frac"))
    
    if not dataset_noise or 'Kraftforstatistikk' not in dataset_noise or 'Totalkalkylen' not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkler mangler i dataset_noise for {flow_code}!")
        
    noise_kraftfor = dataset_noise['Kraftforstatistikk']['value']
    noise_totalkalkylen = dataset_noise['Totalkalkylen']['value']
    noise_trend_interpolation = dataset_noise['trend interpolation']['value']
    
    final_yearly_values = {}
    
    # 2. DEL 1: Landbruksdirektoratets kraftfôrstatistikk (2004->)
    df_raw = preloaded_data.get('feed_raavarer_norsk')
    if df_raw is None:
        raise ValueError(f"[KRITISK] 'feed_raavarer_norsk' mangler i preloaded_data!")
        
    N_cont_accumulator = 0.0
    valid_count = 0
    
    for r in range(len(df_raw)):
        try:
            year_val = df_raw.iloc[r, 0]
            if pd.isna(year_val):
                continue
                
            year = int(float(year_val))
            val_carb = float(df_raw.iloc[r, 1])
            val_prot = float(df_raw.iloc[r, 2])
            
            value_kt_N = (val_carb * N_content_carb + val_prot * N_content_prot) / 1000.0
            value_kt_N_noisy = value_kt_N * noise_kraftfor
            
            if year in EXPECTED_YEARS:
                final_yearly_values[year] = {
                    'value': max(0.0, value_kt_N_noisy),
                    'comment': 'ok',
                    'data_sources': 'Kraftfôrstatistikk'
                }
            
            total_tonn = val_carb + val_prot
            if total_tonn > 0:
                N_cont_accumulator += value_kt_N / total_tonn
                valid_count += 1
            
        except Exception as e:
            raise ValueError(f"[KRITISK] Feil på rad {r} i feed_raavarer: {e}")

    N_cont_before_2000 = (N_cont_accumulator / valid_count) * 1e3

    # 3. DEL 2: Totalkalkylen (1985-1999)
    df_tk = preloaded_data.get('feed_totalkalkyle')
    if df_tk is None:
        raise ValueError(f"[KRITISK] 'feed_totalkalkyle' mangler i preloaded_data!")

    for r in range(len(df_tk)):
        try:
            year_val = df_tk.iloc[r, 0]
            if pd.isna(year_val):
                continue
                
            year = int(float(year_val))
            value_tonn = float(df_tk.iloc[r, 1])
            
            if year < 1995:
                dom_frac = float(df_tk.iloc[r, 2])
            else:
                param_key_dom_frac = "feed_historical_dom_frac"
                dom_frac = float(current_params.get(param_key_dom_frac))
                
            value_kt_N_hist = value_tonn * 1e-3 * N_cont_before_2000 * dom_frac
            value_kt_N_hist_noisy = value_kt_N_hist * noise_totalkalkylen
            
            if year in EXPECTED_YEARS and year not in final_yearly_values:
                final_yearly_values[year] = {
                    'value': max(0.0, value_kt_N_hist_noisy),
                    'comment': 'ok',
                    'data_sources': 'Totalkalkylen'
                }
                
        except Exception as e:
            raise ValueError(f"[KRITISK] Feil på rad {r} i feed_totalkalkyle: {e}")

    # 4. DEL 3: Interpolering (2000-2003)
    val_1999 = final_yearly_values[1999]['value']
    val_2004 = final_yearly_values[2004]['value']
    slope = (val_2004 - val_1999) / 5.0
    
    for gap_year in [2000, 2001, 2002, 2003]:
        if gap_year in EXPECTED_YEARS:
            steps = gap_year - 1999
            interpolated_base = val_1999 + (slope * steps)
            final_interpolated_value = interpolated_base * noise_trend_interpolation
            
            final_yearly_values[gap_year] = {
                'value': max(0.0, final_interpolated_value),
                'comment': 'interpolated',
                'data_sources': 'Interpolert'
            }

    # 5. Pakk ut til resultatlisten
    for year in sorted(final_yearly_values.keys()):
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': final_yearly_values[year]['value'],
            'comment': final_yearly_values[year]['comment'], 'data_sources': final_yearly_values[year]['data_sources']
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_food_industry_waste_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Henter matindustriavfall fra fellesberegningen og legger det til i resultatene.
    """
    flow_code = 'MP.FP-PR.SO-Food industry waste-Nmix'
    collected_years = set()
    
    df_05282 = preloaded_data.get('ssb_05282')
    df_10514 = preloaded_data.get('ssb_10514')
    
    if df_05282 is None or df_10514 is None:
        raise ValueError(f"[KRITISK] Datatabeller ssb_05282/ssb_10514 mangler i preloaded_data for {flow_code}!")
        
    # Henter de ferdig beregnede og støybelagte verdiene
    calculated_years = find_food_industry_waste(df_05282, df_10514, current_params, dataset_noise)
    
    # Pakk ut til resultatlisten
    for year in sorted(calculated_years.keys()):
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': calculated_years[year]['value'],
                'comment': calculated_years[year]['comment'],
                'data_sources': calculated_years[year]['data_sources']
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_food_industry_wastewater_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i avløpsvann fra matindustrien (MP.FP-PR.WW-Food industry wastewater-Nmix).
    Bruker ferdiginnlastede data fra Miljødirektoratet og kategoriseringer.
    """
    flow_code = 'MP.FP-PR.WW-Food industry wastewater-Nmix'
    collected_years = set()
    
    # 1. Hent tabeller fra preloaded_data
    df_emissions_raw = preloaded_data.get('mildir_emissions')
    df_categories = preloaded_data.get('industry_categories')
    
    if df_emissions_raw is None or df_categories is None:
        raise ValueError(f"[KRITISK] Data ('mildir_emissions'/'industry_categories') mangler i preloaded_data for {flow_code}!")
        
    # 2. Hent støy fra dataset_noise
    key_støy = 'norskeutslipp'
    if not dataset_noise or key_støy not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_støy}' mangler i dataset_noise for {flow_code}!")
        
    noise_factor = float(dataset_noise[key_støy]['value'])
    støy_type = dataset_noise[key_støy]['type']  # 'perc' eller 'abs'

    # 3. Prosesser og filtrer data (Dette gjøres i RAM, lynraskt per iterasjon)
    emissions = df_emissions_raw[df_emissions_raw['Komponent'] == 'nitrogen, totalt']
    
    categories_keep = df_categories[
        (df_categories['kategori'] == 'FP') & 
        (df_categories['kommunalt nett?'].isin(['ja']))
    ]
    
    emissions_FP = emissions[emissions['AnleggNavn'].isin(categories_keep['Virksomhet'])]
    sum_by_year = emissions_FP.groupby(['År'])['Mengde'].sum().reset_index()
    
    # 4. Loop over de aggregerte årene og legg på MC-støy
    for index, row in sum_by_year.iterrows():
        try:
            year = int(row['År'])
            if year in EXPECTED_YEARS:
                collected_years.add(year)
                
                # Basisverdi (konverteres fra kg(?) til tonn/kt ved å dele på 1000)
                base_value = float(row['Mengde']) / 1000.0
                
                # Håndtering av støytype (prosentvis vs absolutt)
                if støy_type == 'perc':
                    value_noisy = base_value * noise_factor
                elif støy_type == 'abs':
                    bound = dataset_noise[key_støy]['upper_bound'] if noise_factor >= 0 else dataset_noise[key_støy]['lower_bound']
                    value_noisy = base_value + (noise_factor * bound)
                else:
                    raise ValueError(f"[KRITISK] Ukjent støytype '{støy_type}' for {flow_code}")
                if year == 2020:
                    print(f"[DEBUG] År: {year} | Base: {base_value:.4f} | Støyfaktor: {noise_factor:.4f} | Sluttverdi: {value_noisy:.4f}")
                results.append({
                    'flow_name': flow_code,
                    'year': year,
                    'value': max(0.0, value_noisy),
                    'comment': 'ok (MC-støy lagt på)',
                    'data_sources': 'Miljødirektoratet'
                })
        except (ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil ved prosessering av år på rad {index} for {flow_code}: {e}")

    # 5. Sluttkontroll på manglende år
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)