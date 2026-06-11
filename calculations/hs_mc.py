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
    """
    results = []
    
    # Eksekverer alle flytberegninger for Households og Settlements
    _add_mixed_household_waste_mc(results, preloaded_data, current_params, dataset_noise)
    _add_municipal_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    _add_nh3_human_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_luc_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_overland_flow_urban_mc(results, preloaded_data, current_params, dataset_noise)
    
    return results


def _apply_dataset_noise(base_value, dataset_key, dataset_noise, caller_func):
    """
    Hjelpefunksjon for å legge støy på en avlest fil-verdi basert på dataset_noise-strukturen.
    """
    if not dataset_noise or dataset_key not in dataset_noise:
        if dataset_noise and not hasattr(caller_func, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            setattr(caller_func, f"warned_{dataset_key}", True)
        return base_value

    noise_info = dataset_noise[dataset_key]
    noise_val = noise_info['value']
    
    if noise_info['type'] == 'perc':
        return base_value * noise_val
    else:
        if noise_val >= 0:
            return base_value + (noise_val * noise_info['upp_bound'])
        else:
            return base_value + (noise_val * noise_info['low_bound'])


# =========================================================================
# 1. HUSHOLDNINGSAVFALL
# =========================================================================
def _add_mixed_household_waste_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-PR.SO-Household waste-Nmix'
    collected_years = set()
    
    # Henter DataFrames lastet inn av data_loader.py (Vil krasje hvis nøklene mangler)
    df_05282 = preloaded_data['ssb_waste_05282']
    df_10514 = preloaded_data['ssb_waste_10514']
    
    # Kaller funksjonen med de korrekte posisjonelle argumentene
    household_waste = find_household_waste(df_05282, df_10514, current_params, dataset_noise)

    for year, value in household_waste.items():
        year = int(year)
        collected_years.add(year)
        
        # Setter til 0.0 kun hvis verdien blir negativ av støy
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
    
    N_amount = float(current_params.get("per_capita_WW_N_load_kg"))
    df_pop = preloaded_data.get('hs_pop_size_06913')
    if df_pop is None: return

    for row_idx in range(36, 78):
        if row_idx >= len(df_pop): break
        row_data = df_pop.iloc[row_idx]
        
        try:
            year_val = row_data.iloc[0]
            pop_val = row_data.iloc[1]
            
            if pd.notna(year_val) and pd.notna(pop_val):
                year = int(year_val)
                collected_years.add(year)
                
                perturbed_pop = _apply_dataset_noise(float(pop_val), dataset_key, dataset_noise, _add_municipal_wastewater_mc)
                value = perturbed_pop * N_amount * 1e-6
                if value < 0: value = 0.0
                
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': value,
                    'comment': 'ok (MC-støy lagt på)', 'data_sources': 'SSB table 06913'
                })
        except (ValueError, TypeError, KeyError): continue
            
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
    if data is None or smoking is None: return

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
    
    for _, row in merged.iterrows():
        try:
            year = int(row['Year'])
            collected_years.add(year)
            
            tot_p = _apply_dataset_noise(float(row['Total']), '07459', dataset_noise, _add_nh3_human_emissions_mc)
            age0_p = _apply_dataset_noise(float(row['Age0']), '07459', dataset_noise, _add_nh3_human_emissions_mc)
            age13_p = _apply_dataset_noise(float(row['Age1-3']), '07459', dataset_noise, _add_nh3_human_emissions_mc)
            
            smoke_modifier = _apply_dataset_noise(1.0, '05307', dataset_noise, _add_nh3_human_emissions_mc)
            total_smoked = ((float(row['Daily']) * cig_daily + float(row['Occ']) * cig_occ) / 100.0) * tot_p * smoke_modifier
            
            emissions_tN = (c_total * tot_p + c_age0 * age0_p + c_age1_3 * age13_p + c_smoke * total_smoked)
            value = emissions_tN / 1000.0
            if value < 0: value = 0.0
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': value,
                'comment': 'ok (MC-støy lagt på)', 'data_sources': 'SSB table 07459 & 05307'
            })
        except (ValueError, TypeError, KeyError): continue
            
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_luc_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-AT.AT-LUC emissions-N2O'
    collected_years = set()
    dataset_key = 'UNFCCC_emissions'
    
    conv = float(current_params.get("N2O_to_N_factor"))
    df_n2o = preloaded_data.get('hs_unfccc_n2o_raw')
    if df_n2o is None: return

    for row_idx in range(5, 38):
        if row_idx >= len(df_n2o): break
        row_data = df_n2o.iloc[row_idx]
        try:
            year = int(row_data.iloc[0])
            collected_years.add(year)
            raw_val = float(row_data.iloc[1])
            
            value = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_luc_N2O_emissions_mc)
            value = value * conv
            if value < 0: value = 0.0
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': value,
                'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
            })
        except (ValueError, TypeError, KeyError): continue
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_overland_flow_urban_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-HY.SW-Overland flow-Nmix'
    collected_years = set()
    dataset_key = 'TEOTIL'
    ret = float(current_params.get("HS_urban_retention_fraction"))
    
    # 1. Hent historisk data
    df_kyst = preloaded_data.get('hy_kyst_tilforsel')
    
    # 2. Hent TEOTIL3-data uten å utløse "ambiguous truth value"-feilen
    df_t3 = preloaded_data.get('hy_teotil3_by_source')
    if df_t3 is None:
        df_t3 = preloaded_data.get('hy_teotil3_to_coast')

    # 5a. Historisk periode (hvis tilgjengelig)
    if df_kyst is not None:
        for _, row in df_kyst.iterrows():
            try:
                year_val = row.iloc[0]
                raw_val = row.iloc[4]
                if pd.notna(year_val) and pd.notna(raw_val):
                    year = int(year_val)
                    if 1990 <= year <= 2026:
                        collected_years.add(year)
                        val_p = _apply_dataset_noise(float(raw_val), dataset_key, dataset_noise, _add_overland_flow_urban_mc)
                        val_p = _apply_dataset_noise(val_p, 'trend interpolation', dataset_noise, _add_overland_flow_urban_mc)
                        value = (val_p / 1000.0) * (1.0 - ret)
                        results.append({
                            'flow_name': flow_code, 'year': year, 'value': max(0.0, value),
                            'comment': 'ok', 'data_sources': 'Miljødirektoratet'
                        })
            except (ValueError, TypeError, IndexError): continue

    # 5b. Nyere periode (TEOTIL3)
    if df_t3 is not None:
        for _, row in df_t3.iterrows():
            try:
                year_val = row.iloc[0]
                raw_val = row.iloc[9]  # Dobbeltsjekk at kolonne-indeks 9 stemmer for verdiene i filen din!
                if pd.notna(year_val) and pd.notna(raw_val):
                    year = int(year_val)
                    
                    # Hvis året finnes fra historisk data, overskriver vi det med nyere data
                    if year in collected_years:
                        results[:] = [x for x in results if not (x['flow_name'] == flow_code and x['year'] == year)]
                    
                    collected_years.add(year)
                    val_p = _apply_dataset_noise(float(raw_val), dataset_key, dataset_noise, _add_overland_flow_urban_mc)
                    value = (val_p / 1000.0) * (1.0 - ret)
                    
                    results.append({
                        'flow_name': flow_code, 'year': year, 'value': max(0.0, value),
                        'comment': 'ok (TEOTIL3)', 'data_sources': 'TEOTIL3'
                    })
            except (ValueError, TypeError, IndexError): continue
            
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)