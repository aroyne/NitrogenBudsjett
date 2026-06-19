#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MC-VERSJON: Beregner nitrogenflyt for Households & Settlements (HS).
Rådata ligger i preloaded_data, mens støyfaktorer for hvert datasett sendes inn via dataset_noise.
Massebalanse-rammer er fjernet for optimalisert ytelse.
"""
import pandas as pd
import numpy as np

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    load_crltap_emissions_to_N
)
from calculations.shared_flow_calculations import find_household_waste


def execute_calculations_hs(preloaded_data, current_params, dataset_noise, current_trade_factors=None):
    """
    Hovedfunksjon for HS-poolen (MC). Mottar denne rundens støyordbok for datasett.
    Krasjer umiddelbart hvis kritiske inndata mangler.
    """
    results = []
    
    # Eksekverer alle flytberegninger for Households og Settlements
    _add_mixed_household_waste_mc(results, preloaded_data, current_params, dataset_noise)
    _add_municipal_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    _add_nh3_human_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_luc_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_overland_flow_urban_mc(results, preloaded_data, current_params, dataset_noise)
    
    return results


# =========================================================================
# 1. HUSHOLDNINGSAVFALL
# =========================================================================
def _add_mixed_household_waste_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-PR.SO-Household waste-Nmix'
    collected_years = set()
    
    # Henter DataFrames lastet inn av data_loader.py (Vil krasje hvis nøklene mangler)
    if 'ssb_05282' not in preloaded_data or 'ssb_10514' not in preloaded_data:
        raise ValueError(f"[KRITISK] Avfallsdata ('ssb_05282' eller 'ssb_10514') mangler i preloaded_data for {flow_code}!")
        
    # df_05282 = preloaded_data['ssb_05282']
    # df_10514 = preloaded_data['ssb_10514']
    
    # Kaller funksjonen med de korrekte posisjonelle argumentene
    household_waste = find_household_waste(preloaded_data, current_params, dataset_noise)

    for year, value in household_waste.items():
        year = int(year)
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        if value < 0: 
            value = 0.0
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (Beregnet fra SSB-tabeller med MC-støy)', 'data_sources': 'SSB'
        })
        
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)    
    

# =========================================================================
# 2. KOMMUNALT AVLØPSVANN
# =========================================================================
def _add_municipal_wastewater_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-PR.WW-Municipal wastewater-Nmix'
    collected_years = set()
    dataset_key = '06913'
    noise_val = dataset_noise[dataset_key]
    
    val_param = current_params.get("per_capita_WW_N_load_kg")
    if val_param is None:
        raise KeyError(f"[KRITISK] Parameter 'per_capita_WW_N_load_kg' mangler i current_params for {flow_code}!")
    N_amount = float(val_param)
    
    df_pop = preloaded_data.get('hs_pop_size_06913')
    if df_pop is None: 
        raise ValueError(f"[KRITISK] Data 'hs_pop_size_06913' mangler i preloaded_data for {flow_code}!")

    for row_idx in range(36, 78):
        if row_idx >= len(df_pop): 
            break
        row_data = df_pop.iloc[row_idx]
        
        year_val = row_data.iloc[0]
        pop_val = row_data.iloc[1]
        
        if pd.notna(year_val) and pd.notna(pop_val):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            
            perturbed_pop = float(pop_val)*noise_val
            value = perturbed_pop * N_amount * 1e-6
            if value < 0: 
                value = 0.0
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': value,
                'comment': 'ok (MC-støy lagt på)', 'data_sources': 'SSB table 06913'
            })
            
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


# =========================================================================
# 3. NH3-UTSLIPP FRA MENNESKEKROPPEN
# =========================================================================
def _add_nh3_human_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-AT.AT-Emissions-NH3'
    collected_years = set()
    
    c_total = float(current_params.get("NH3_emission_factor_total_pop"))
    c_age0 = float(current_params.get("NH3_emission_factor_age0"))
    c_age1_3 = float(current_params.get("NH3_emission_factor_age1_3"))
    c_smoke = float(current_params.get("NH3_emission_factor_cigarettes"))
    cig_daily = float(current_params.get("daily_smoker_cigs_per_year"))
    cig_occ = float(current_params.get("occasional_smoker_cigs_per_year"))

    data = preloaded_data.get('hs_pop_age_groups_07459')
    smoking = preloaded_data.get('hs_smoking_stats_05307')
    if data is None or smoking is None: 
        raise ValueError(f"[KRITISK] Befolkningsdata ('hs_pop_age_groups_07459') eller røykedata ('hs_smoking_stats_05307') mangler for {flow_code}!")

    df_pop = data.copy()
    df_pop.columns = ['Gender', 'AgeGroup', 'Year', 'Value']
    df_pop['Gender'] = df_pop['Gender'].fillna(method='ffill')
    df_pop['AgeGroup'] = df_pop['AgeGroup'].fillna(method='ffill')
    
    age_0 = df_pop[df_pop['AgeGroup'] == '0 år'].groupby('Year')['Value'].sum().reset_index()
    age_1_3 = df_pop[df_pop['AgeGroup'].isin(['1 år', '2 år', '3 år'])].groupby('Year')['Value'].sum().reset_index()
    total_pop = df_pop.groupby('Year')['Value'].sum().reset_index()
    
    population = age_0.merge(age_1_3, on='Year', suffixes=('_0', '_1_3')).merge(total_pop, on='Year')
    population.columns = ['Year', 'Age0', 'Age1-3', 'Total']
    
    df_smoke = smoking.copy()
    df_smoke.columns = ['A', 'B', 'Year', 'Daily', 'Occ']
    
    merged = population.merge(df_smoke[['Year', 'Daily', 'Occ']], on='Year', how='inner')
    
    noise_07459 = dataset_noise['07459'] # population
    noise_05307 = dataset_noise['05307'] # smoking
    
    for _, row in merged.iterrows():
        year = int(row['Year'])
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        tot_p = float(row['Total'])*noise_07459
        age0_p = float(row['Age0'])*noise_07459
        age13_p = float(row['Age1-3'])*noise_07459
        
        total_smoked = ((float(row['Daily']) * cig_daily + float(row['Occ']) * cig_occ) / 100.0) * tot_p * noise_05307
        
        emissions_tN = c_total * tot_p + c_age0 * age0_p + c_age1_3 * age13_p + c_smoke * total_smoked
        value = emissions_tN / 1000.0
        if value < 0: 
            value = 0.0
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'SSB table 07459 & 05307'
        })
            
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


# =========================================================================
# 4. LUC N2O-UTSLIPP
# =========================================================================
def _add_luc_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-AT.AT-LUC emissions-N2O'
    collected_years = set()
    dataset_key = 'UNFCCC_emissions'
    noise_val = dataset_noise[dataset_key]
    conv = float(current_params.get("N2O_to_N_factor"))
    df_n2o = preloaded_data.get('hs_unfccc_n2o_raw')
    if df_n2o is None: 
        raise ValueError(f"[KRITISK] Data 'hs_unfccc_n2o_raw' mangler i preloaded_data for {flow_code}!")

    for row_idx in range(5, 38):
        if row_idx >= len(df_n2o): 
            break
        row_data = df_n2o.iloc[row_idx]
        
        year = int(row_data.iloc[0])
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        raw_val = float(row_data.iloc[1])
        
        value = raw_val * noise_val
        value = value * conv
        if value < 0: 
            value = 0.0
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


# =========================================================================
# 5. OVERVANNSAVRENNING (URBAN)
# =========================================================================
# =========================================================================
# 5. OVERVANNSAVRENNING (URBAN)
# =========================================================================
def _add_overland_flow_urban_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-HY.SW-Overland flow-Nmix'
    collected_years = set()
    dataset_key = 'TEOTIL'
    ret = float(current_params.get("HS_urban_retention_fraction"))
    noise_data = dataset_noise[dataset_key]
    noise_interp = dataset_noise['trend interpolation']
    
    # 1. Hent historisk data og TEOTIL3
    df_kyst = preloaded_data.get('hy_kyst_tilforsel')
    df_t3 = preloaded_data.get('hy_teotil3_by_source')
    if df_t3 is None:
        df_t3 = preloaded_data.get('hy_teotil3_to_coast')
        
    if df_kyst is None and df_t3 is None:
        raise ValueError(f"[KRITISK] Begge datakilder ('hy_kyst_tilforsel' og TEOTIL3) mangler i preloaded_data for {flow_code}!")

    # 2. Historisk periode
    if df_kyst is not None:
        for idx, row in df_kyst.iterrows():
            val_at_col0 = str(row.iloc[0]).strip()
            
            # Hopp over rene tekst-headere hvis filen har blitt feillest
            if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
                continue
                
            try:
                year = int(float(val_at_col0))
                raw_val = row.iloc[4]
                
                if pd.notna(raw_val) and year in EXPECTED_YEARS:
                    collected_years.add(year)
                    val_p = float(raw_val)*noise_data*noise_interp
                    value = (val_p / 1000.0) * (1.0 - ret)
                    results.append({
                        'flow_name': flow_code, 'year': year, 'value': max(0.0, value),
                        'comment': 'ok', 'data_sources': 'Miljødirektoratet'
                    })
            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"[KRITISK DATAFEIL] Kunne ikke konvertere år/verdi i df_kyst (historisk) på rad {idx}.\n"
                    f"Verdi i kolonne 0: '{row.iloc[0]}' | Verdi i kolonne 4: '{row.iloc[4]}'\n"
                    f"Original feil: {e}"
                )

    # 3. Nyere periode (TEOTIL3) - overskriver eldre data dersom overlapp
    if df_t3 is not None:
        for idx, row in df_t3.iterrows():
            val_at_col0 = str(row.iloc[0]).strip()
            
            # Hopp over rene tekst-headere hvis filen har blitt feillest
            if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
                continue
                
            try:
                year = int(float(val_at_col0))
                raw_val = row.iloc[9]  # Kolonne-indeks 9 for verdiene
                
                if pd.notna(raw_val):
                    if year not in EXPECTED_YEARS:
                        continue
                    
                    # Slett duplikater fra historisk kilde dersom samme år finnes i TEOTIL3
                    if year in collected_years:
                        results[:] = [x for x in results if not (x['flow_name'] == flow_code and x['year'] == year)]
                    
                    collected_years.add(year)
                    val_p = float(raw_val)*noise_data
                    value = (val_p / 1000.0) * (1.0 - ret)
                    
                    results.append({
                        'flow_name': flow_code, 'year': year, 'value': max(0.0, value),
                        'comment': 'ok (TEOTIL3)', 'data_sources': 'TEOTIL3'
                    })
            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"[KRITISK DATAFEIL] Kunne ikke konvertere år/verdi i df_t3 (TEOTIL3) på rad {idx}.\n"
                    f"Verdi i kolonne 0: '{row.iloc[0]}' | Verdi i kolonne 9: '{row.iloc[9]}'\n"
                    f"Original feil: {e}"
                )
                
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)