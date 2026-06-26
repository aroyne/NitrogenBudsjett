#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
)
from calculations.shared_flow_calculations import find_household_waste

def execute_calculations_hs(preloaded_data, current_params, dataset_noise, current_trade_factors=None):
    results = []
    
    _add_mixed_household_waste_mc(results, preloaded_data, current_params, dataset_noise)
    _add_municipal_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    _add_nh3_human_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_luc_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_overland_flow_urban_mc(results, preloaded_data, current_params, dataset_noise)
    
    return results


def _add_mixed_household_waste_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-PR.SO-Household waste-Nmix'
    collected_years = set()
    
    household_waste = find_household_waste(preloaded_data, current_params, dataset_noise)

    for year, value in household_waste.items():
        year = int(year)
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (Beregnet fra SSB-tabeller med MC-støy)', 'data_sources': 'SSB'
        })
        
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)    
    

def _add_municipal_wastewater_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-PR.WW-Municipal wastewater-Nmix'
    collected_years = set()
    dataset_key = '06913'
    noise_val = dataset_noise[dataset_key]
    
    val_param = current_params.get("per_capita_WW_N_load_kg")
    N_amount = float(val_param)
    df_pop = preloaded_data.get('hs_pop_size_06913')

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
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'SSB table 07459 & 05307'
        })
            
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_luc_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HS.HS-AT.AT-LUC emissions-N2O'
    collected_years = set()
    dataset_key = 'UNFCCC_emissions'
    noise_val = dataset_noise[dataset_key]
    conv = float(current_params.get("N2O_to_N_factor"))
    df_n2o = preloaded_data.get('hs_unfccc_n2o_raw')

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
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


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

    # 2. Historisk periode
    if df_kyst is not None:
        for idx, row in df_kyst.iterrows():
            val_at_col0 = str(row.iloc[0]).strip()
            
            # Hopp over rene tekst-headere hvis filen har blitt feillest
            if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
                continue
                
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

    # 3. Nyere periode (TEOTIL3) - overskriver eldre data dersom overlapp
    if df_t3 is not None:
        for idx, row in df_t3.iterrows():
            val_at_col0 = str(row.iloc[0]).strip()
            
            # Hopp over rene tekst-headere hvis filen har blitt feillest
            if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
                continue
                
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
                
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)