#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:50:01 2026

@author: anja
"""

import pandas as pd  
from calculations.shared_flow_calculations import (
    find_export_for_recycling,
    find_export_for_reuse,
    find_household_waste,
    find_other_industry_waste,
    find_recycling)
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    load_crltap_emissions_to_N,
    process_generic_trade_flow,
)

PR_SO_CRLTAP_SECTORS = [
    '1A1a', '5A', '5B1', '5B2', '5C1a', '5C1bi', 
    '5C1bii', '5C1biii', '5C1biv', '5C1bv', '5C1bvi', '5E'
]
PR_WW_CRLTAP_SECTORS = ['5D1', '5D2', '5D3']

def execute_calculations_pr(preloaded_data, current_params, dataset_noise, current_trade_factors):
    results = []

    _add_waste_to_energy_mc(results, preloaded_data, current_params, dataset_noise)
    _add_recycling_mc(results, preloaded_data, current_params, dataset_noise, current_trade_factors)
    _add_ag_biologically_treated_organic_waste_mc(results, preloaded_data, current_params, dataset_noise)
    _add_wastewater_from_landfills_mc(results, preloaded_data, current_params, dataset_noise)
    _add_hs_biologically_treated_organic_waste_mc(results, preloaded_data, current_params, dataset_noise)
    # _add_biofuels_production_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    _add_so_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_so_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_so_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_so_leaching_mc(results, preloaded_data, current_params, dataset_noise)
    _add_export_for_recycling_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_export_for_reuse_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_solid_waste_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_ag_sewage_sludge_fertilizer_mc(results, preloaded_data, current_params, dataset_noise)
    _add_hs_sewage_sludge_fertilizer_mc(results, preloaded_data, current_params, dataset_noise)
    _add_sewage_sludge_landfill_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ww_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ww_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_treated_ww_discharge_mc(results, preloaded_data, current_params, dataset_noise)
    
    
    return results


def _add_waste_to_energy_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-EF.EC-Waste to energy-Nmix'
    collected_years = set()
    data_sources = 'SSB'
    
    paper_N   = float(current_params.waste_N_frac('paper'))
    plastic_N = float(current_params.waste_N_frac('plastic'))
    wood_N    = float(current_params.waste_N_frac('wood'))
    textile_N = float(current_params.waste_N_frac('textiles'))
    wet_N     = float(current_params.waste_N_frac('wet_organic'))
    sludge_N  = float(current_params.waste_N_frac('sludge'))
    other_N   = float(current_params.waste_N_frac('other_materials'))
    haz_N     = float(current_params.waste_N_frac('hazardous'))
    contam_N  = float(current_params.waste_N_frac('contaminated_masses'))
    mixed_N   = float(current_params.waste_N_frac('mixed_waste'))
    rubber_N  = float(current_params.waste_N_frac('rubber'))
    park_N    = float(current_params.waste_N_frac('park_garden'))

    # =========================================================================
    # 1. PERIODE 1995-2011: SSB Tabell 05281 (Nøkkel: ssb_waste_05281)
    # =========================================================================
    dataset_key_05281 = '05281'
    df_05281 = preloaded_data.get('ssb_waste_05281')
    noise_05281 = dataset_noise[dataset_key_05281]

    for col in range(3, 20):  
        year = int(float(df_05281.iloc[2, col]))
        collected_years.add(year)
        
        raw_tonnage = 0.0
        raw_tonnage += float(df_05281.iloc[60, col]) * paper_N    
        raw_tonnage += float(df_05281.iloc[88, col]) * paper_N    
        raw_tonnage += float(df_05281.iloc[62, col]) * plastic_N  
        raw_tonnage += float(df_05281.iloc[90, col]) * plastic_N  
        raw_tonnage += float(df_05281.iloc[65, col]) * wood_N     
        raw_tonnage += float(df_05281.iloc[93, col]) * wood_N     
        raw_tonnage += float(df_05281.iloc[66, col]) * textile_N  
        raw_tonnage += float(df_05281.iloc[94, col]) * textile_N  
        raw_tonnage += float(df_05281.iloc[67, col]) * wet_N      
        raw_tonnage += float(df_05281.iloc[95, col]) * wet_N      
        raw_tonnage += float(df_05281.iloc[69, col]) * sludge_N   
        raw_tonnage += float(df_05281.iloc[97, col]) * sludge_N   
        raw_tonnage += float(df_05281.iloc[70, col]) * other_N    
        raw_tonnage += float(df_05281.iloc[98, col]) * other_N    
        raw_tonnage += float(df_05281.iloc[71, col]) * haz_N      
        raw_tonnage += float(df_05281.iloc[99, col]) * haz_N      
        raw_tonnage += float(df_05281.iloc[72, col]) * contam_N   
        raw_tonnage += float(df_05281.iloc[100, col]) * contam_N  

        value = raw_tonnage*noise_05281

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': data_sources
        })

    # =========================================================================
    # 2. PERIODE 2012-2023: SSB Tabell 10513 (Nøkkel: ssb_waste_10513)
    # =========================================================================
    dataset_key_10513 = '10513'
    df_10513 = preloaded_data.get('ssb_waste_10513')
    noise_10513 = dataset_noise[dataset_key_10513]

    for col in range(1, 101, 9):  
        year = int(float(df_10513.iloc[3, col]))
        collected_years.add(year)
        
        raw_tonnage = 0.0
        raw_tonnage += float(df_10513.iloc[6, col+5]) * wet_N       
        raw_tonnage += float(df_10513.iloc[7, col+5]) * park_N      
        raw_tonnage += float(df_10513.iloc[8, col+5]) * wood_N       
        raw_tonnage += float(df_10513.iloc[9, col+5]) * sludge_N     
        raw_tonnage += float(df_10513.iloc[10, col+5]) * paper_N     
        raw_tonnage += float(df_10513.iloc[16, col+5]) * plastic_N   
        raw_tonnage += float(df_10513.iloc[17, col+5]) * rubber_N    
        raw_tonnage += float(df_10513.iloc[18, col+5]) * textile_N   
        raw_tonnage += float(df_10513.iloc[21, col+5]) * haz_N       
        raw_tonnage += float(df_10513.iloc[22, col+5]) * mixed_N     
        raw_tonnage += float(df_10513.iloc[23, col+5]) * other_N     
        raw_tonnage += float(df_10513.iloc[24, col+5]) * contam_N    

        value = raw_tonnage*noise_10513

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': data_sources
        })
        
    # =========================================================================
    # 3. PERIODE 1990-1994: Historisk ekstrapolering (Nøkkel: waste_historical_fractions)
    # =========================================================================
    dataset_key_hist = 'historical_waste'
    df_hist = preloaded_data.get('waste_historical_fractions')
    noise_hist = dataset_noise[dataset_key_hist]
    noise_trend = dataset_noise['trend interpolation']

    household_waste = find_household_waste(preloaded_data, current_params, dataset_noise)
    industry_waste = find_other_industry_waste(
        preloaded_data['ssb_05282'], 
        preloaded_data['ssb_10514'], 
        preloaded_data['ssb_hist_industry_waste'], 
        current_params, 
        dataset_noise
    )

    inc_frac_1985 = float(df_hist.iloc[1, 1]) / 100  
    inc_frac_1992 = float(df_hist.iloc[2, 1]) / 100  
    change_per_year = (inc_frac_1992 - inc_frac_1985) / 7
    
    r_iloc = 2  
    for year in range(1990, 1995):
        collected_years.add(year)
        
        waste = household_waste[year] + industry_waste[year]
        
        if year < 1992:
            inc_frac = inc_frac_1985 + change_per_year * (year - 1985)
            comment_str = 'extrapolated (MC-støy lagt på basisdata)'
        else:
            inc_frac = float(df_hist.iloc[r_iloc, 1]) / 100
            comment_str = 'ok'
            r_iloc += 1
            
        raw_val = waste * inc_frac        
        value = raw_val*noise_hist*noise_trend

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': comment_str, 'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_recycling_mc(results, preloaded_data, current_params, dataset_noise, current_trade_factors):
    flow_code = 'PR.SO-MP.OP-Recycling-Nmix'
    collected_years = set()
    data_sources = 'SSB'

    year_values = find_recycling(
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        dataset_noise=dataset_noise,
        prepared_trade_recycling=preloaded_data.get('trade_recycling'),
        prepared_trade_reuse=preloaded_data.get('trade_reuse'),
        trade_params=current_trade_factors
    )

    for year, value in year_values.items():
        collected_years.add(year)
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': 'ok',
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
def _add_ag_biologically_treated_organic_waste_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-AG.SM-Biologically treated organic waste-Nmix'
    collected_years = set()
    
    # 1) find the fraction of N in input waste (excluding sewage sludge) for biological treatment from SSB 10513 (2012-2024)
    # as well as the fraction of sewage sludge in input
    wet_N         = float(current_params.waste_N_frac('wet_organic'))
    park_N        = float(current_params.waste_N_frac('park_garden'))
    wood_N        = float(current_params.waste_N_frac('wood'))
    
    noise_trend = dataset_noise['trend interpolation']
    noise_10513 = dataset_noise['10513']
    noise_12818 = dataset_noise['12818']
    df_10513 = preloaded_data.get('ssb_waste_10513') # given in kt
    total_10513 = {}
    frac_N_10513 = {}
    frac_sludge_10513 = {}
    for col in range(1, df_10513.shape[1], 9):
        cell_year = str(df_10513.iloc[3, col]).strip()
        if cell_year.replace('.0', '').isdigit():
            year = int(float(cell_year))
        total = ( #levert til biogassproduksjon (+2) og kompost (+3))
            float(df_10513.iloc[6, col + 2]) + float(df_10513.iloc[6, col + 3]) +  # Våtorganisk
            float(df_10513.iloc[7, col + 2]) +  float(df_10513.iloc[7, col + 3]) + # Park- og hage
            float(df_10513.iloc[8, col + 2]) + float(df_10513.iloc[8, col + 2])  # Treavfall
        )
        frac_sludge_10513[year] = (float(df_10513.iloc[9, col + 2])+float(df_10513.iloc[9, col + 3]))/(total+float(df_10513.iloc[9, col + 2])+float(df_10513.iloc[9, col + 3]))
        total_10513[year] = total
        total_N = (
            float(df_10513.iloc[6, col + 2]) * wet_N +  # Våtorganisk
            float(df_10513.iloc[7, col + 2]) * park_N +  # Park- og hage
            float(df_10513.iloc[8, col + 2]) * wood_N   # Treavfall
        )
        frac_N_10513[year] = total_N/total

    # 2) find the amount of disposed waste allocated to agriculture from SSB 12818 (2018-2023)
    # removing sewage sludge fraction from previous step
    df_12818 = preloaded_data.get('ssb_waste_12818') # given in kt
    waste_ag = {}
    for col_idx in range(1, 7):
        year = int(float(str(df_12818.iloc[3, col_idx]).strip()))
        kt_ag = float(df_12818.iloc[5, col_idx])
        waste_ag[year] = kt_ag*(1-frac_sludge_10513[year])
    
    # 3) find the N content of that waste by using fraction N from 1)
    N_ag = {}
    for year in range(2018,2024):
        N_ag[year] = waste_ag[year]*frac_N_10513[year]

    # 3b) for 2012-2017, scale 2018 input amount and ag fraction using totals from 10513
    for year in range(2012,2018):
        N_ag[year] = N_ag[2018]/total_10513[2018]*total_10513[year]
        
    # 4) extrapolate constant 2012 value back to 1990
    for year in range(1990,2012):
        N_ag[year] = N_ag[2012]
                      
    for year in range(1990,2024):
        collected_years.add(year)
        val = N_ag[year]*noise_10513*noise_12818
        
        if year < 2012:
            val *= noise_trend
            comment_str = 'ok'
            source_str  = 'extrapolated'
        elif year < 2018:
            comment_str = 'ok'
            source_str  = 'extrapolated/SSB'
            
        else:
            comment_str = 'ok'
            source_str  = 'SSB'

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': comment_str,
            'data_sources': source_str
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_hs_biologically_treated_organic_waste_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-HS.HS-Biologically treated organic waste-Nmix'
    collected_years = set()
    
    # 1) find the fraction of N in input waste (excluding sewage sludge) for biological treatment from SSB 10513 (2012-2024)
    # as well as the fraction of sewage sludge in input
    wet_N         = float(current_params.waste_N_frac('wet_organic'))
    park_N        = float(current_params.waste_N_frac('park_garden'))
    wood_N        = float(current_params.waste_N_frac('wood'))
    
    noise_trend = dataset_noise['trend interpolation']
    noise_10513 = dataset_noise['10513']
    noise_12818 = dataset_noise['12818']
    df_10513 = preloaded_data.get('ssb_waste_10513') # given in kt
    total_10513 = {}
    frac_N_10513 = {}
    frac_sludge_10513 = {}
    for col in range(1, df_10513.shape[1], 9):
        cell_year = str(df_10513.iloc[3, col]).strip()
        if cell_year.replace('.0', '').isdigit():
            year = int(float(cell_year))
        total = ( #levert til biogassproduksjon (+2) og kompost (+3))
            float(df_10513.iloc[6, col + 2]) + float(df_10513.iloc[6, col + 3]) +  # Våtorganisk
            float(df_10513.iloc[7, col + 2]) +  float(df_10513.iloc[7, col + 3]) + # Park- og hage
            float(df_10513.iloc[8, col + 2]) + float(df_10513.iloc[8, col + 2])  # Treavfall
        )
        frac_sludge_10513[year] = (float(df_10513.iloc[9, col + 2])+float(df_10513.iloc[9, col + 3]))/(total+float(df_10513.iloc[9, col + 2])+float(df_10513.iloc[9, col + 3]))
        total_10513[year] = total
        total_N = (
            float(df_10513.iloc[6, col + 2]) * wet_N +  # Våtorganisk
            float(df_10513.iloc[7, col + 2]) * park_N +  # Park- og hage
            float(df_10513.iloc[8, col + 2]) * wood_N   # Treavfall
        )
        frac_N_10513[year] = total_N/total

    # 2) find the amount of disposed waste allocated to HS ("grøntareal" + "levert jordprodusent") from SSB 12818 (2018-2023)
    # removing sewage sludge fraction from previous step
    df_12818 = preloaded_data.get('ssb_waste_12818') # given in kt
    waste_hs = {}
    for col_idx in range(1, 7):
        year = int(float(str(df_12818.iloc[3, col_idx]).strip()))
        kt_hs = float(df_12818.iloc[6, col_idx]) + float(df_12818.iloc[7, col_idx])
        waste_hs[year] = kt_hs*(1-frac_sludge_10513[year])
    
    # 3) find the N content of that waste by using fraction N from 1)
    N_hs = {}
    for year in range(2018,2024):
        N_hs[year] = waste_hs[year]*frac_N_10513[year]

    # 3b) for 2012-2017, scale 2018 input amount and ag fraction using totals from 10513
    for year in range(2012,2018):
        N_hs[year] = N_hs[2018]/total_10513[2018]*total_10513[year]
        
    # 4) extrapolate constant 2012 value back to 1990
    for year in range(1990,2012):
        N_hs[year] = N_hs[2012]
                      
    for year in range(1990,2024):
        collected_years.add(year)
        val = N_hs[year]*noise_10513*noise_12818
        
        if year < 2012:
            val *= noise_trend
            comment_str = 'ok'
            source_str  = 'extrapolated'
        elif year < 2018:
            comment_str = 'ok'
            source_str  = 'extrapolated/SSB'
            
        else:
            comment_str = 'ok'
            source_str  = 'SSB'

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': comment_str,
            'data_sources': source_str
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_wastewater_from_landfills_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-PR.WW-Wastewater from landfills-Nmix'
    collected_years = set()
    
    noise_mildir = float(dataset_noise['norskeutslipp'])
    uts_raw = preloaded_data.get('deponi_utslipp')
    tilk_raw = preloaded_data.get('deponi_tilkobling')

    tilk_ja = set()
    tilk_nei = set()
    
    for idx, row in tilk_raw.iterrows():
        # Hopp over header-raden hvis den dukker opp som første datalinje
        if idx == 0 and ("anlegg" in str(row.iloc[0]).lower() or "tilkoblet" in str(row.iloc[1]).lower()):
            continue
            
        name_clean = str(row.iloc[0]).strip().lower() # Kolonne 0: anleggsnavn
        status = str(row.iloc[1]).strip().lower()    # Kolonne 1: status
        
        if 'ja' in status:
            tilk_ja.add(name_clean)
        elif 'nei' in status:
            tilk_nei.add(name_clean)

    real_years_data = {}
    
    for idx, row in uts_raw.iterrows():
        # Hopp over header-raden hvis den dukker opp som første datalinje
        if idx == 0 and "anlegg" in str(row.iloc[0]).lower():
            continue
            
        try:
            year_val = str(row.iloc[3]).strip() # Kolonne 3: År
            if not year_val.replace('.0', '').isdigit():
                continue
                
            year = int(float(year_val))
            
            if 2011 <= year <= 2025:
                anlegg_name = str(row.iloc[0]).strip().lower() # Kolonne 0: Anleggsnavn
                raw_value = float(row.iloc[4])                 # Kolonne 4: Årlig utslipp til vann
                
                # Sjekk om navnet matcher helt eller delvis
                if any(ja_name in anlegg_name or anlegg_name in ja_name for ja_name in tilk_ja):
                    weight = 1.0
                elif any(nei_name in anlegg_name or anlegg_name in nei_name for nei_name in tilk_nei):
                    weight = 0.0
                else: # ukjent
                    weight = 0.5
                    
                
                # Beregn N-mengde koblet til avløp
                n_leachate_tN = raw_value * weight
                
                if year not in real_years_data:
                    real_years_data[year] = 0.0
                    
                # Akkumuler i ktN (tN / 1000.0) og legg på rundens MC-støy
                real_years_data[year] += (n_leachate_tN / 1000.0) * noise_mildir
                
        except (ValueError, TypeError, IndexError):
            continue

    # ekstrapolere historisk (1990-2010)
    valid_years = [y for y in real_years_data.keys() if 2011 <= y <= 2025]
    mean_connected_kt = sum(real_years_data[y] for y in valid_years) / len(valid_years)

    final_values = {}
    
    for year in range(1990, 2011):
        final_values[year] = mean_connected_kt

    for year in range(2011, 2026):
        final_values[year] = real_years_data.get(year)

    for year in sorted(final_values.keys()):
        collected_years.add(year)
        val = final_values[year]
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': 'ok',
            'data_sources': 'Utslipp_deponi.xlsx (Mildir)' if year >= 2011 else 'extrapolated'
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_so_leaching_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-HY.SW-Leaching-Nmix'
    collected_years = set()
    comment = 'ok'
    noise_mildir = float(dataset_noise['norskeutslipp'])

    uts_raw = preloaded_data.get('deponi_utslipp')
    tilk_raw = preloaded_data.get('deponi_tilkobling')

    tilk_ja = set()
    tilk_nei = set()
    
    for idx, row in tilk_raw.iterrows():
        if idx == 0 and ("anlegg" in str(row.iloc[0]).lower() or "tilkoblet" in str(row.iloc[1]).lower()):
            continue
            
        name_clean = str(row.iloc[0]).strip().lower() # Kolonne 0: anleggsnavn
        status = str(row.iloc[1]).strip().lower()    # Kolonne 1: status
        
        if 'ja' in status:
            tilk_ja.add(name_clean)
        elif 'nei' in status:
            tilk_nei.add(name_clean)

    real_years_data = {}
    
    for idx, row in uts_raw.iterrows():
        if idx == 0 and "anlegg" in str(row.iloc[0]).lower():
            continue
            
        try:
            year_val = str(row.iloc[3]).strip() # Kolonne 3: År
            if not year_val.replace('.0', '').isdigit():
                continue
                
            year = int(float(year_val))
            
            if 2011 <= year <= 2025:
                anlegg_name = str(row.iloc[0]).strip().lower() # Kolonne 0: Anleggsnavn
                raw_value = float(row.iloc[4])                 # Kolonne 4: Årlig utslipp til vann
                
                if any(ja_name in anlegg_name or anlegg_name in ja_name for ja_name in tilk_ja):
                    weight = 0.0  # Tilkoblet -> Skal IKKE regnes som sigevann direkte til natur
                elif any(nei_name in anlegg_name or anlegg_name in nei_name for nei_name in tilk_nei):
                    weight = 1.0  # Ikke tilkoblet -> Går 100% til natur (sigevann)
                else:# ukjent
                    weight = 0.5
                
                n_leachate_tN = raw_value * weight
                
                if year not in real_years_data:
                    real_years_data[year] = 0.0
                    
                real_years_data[year] += (n_leachate_tN / 1000.0) * noise_mildir
                
        except (ValueError, TypeError, IndexError):
            continue

    valid_years = [y for y in real_years_data.keys() if 2011 <= y <= 2025]
    
    mean_unconnected_kt = sum(real_years_data[y] for y in valid_years) / len(valid_years)

    final_values = {}
    
    for year in range(1990, 2011):
        final_values[year] = mean_unconnected_kt

    for year in range(2011, 2026):
        final_values[year] = real_years_data.get(year, 0.0)

    for year in range(1984, 1990):
        final_values[year] = 0.0

    for year in sorted(final_values.keys()):
        collected_years.add(year)
        val = final_values[year]
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': comment,
            'data_sources': 'Utslipp_deponi.xlsx (Mildir)' if year >= 2011 else 'extrapolated'
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

# def _add_biofuels_production_wastewater_mc(results, preloaded_data, current_params, dataset_noise):
#     flow_code = 'PR.SO-PR.WW-Biofuels production wastewater-Nmix'
#     collected_years = set()
    
#     noise_biogass = float(dataset_noise['Biogass'])
#     noise_10513   = float(dataset_noise['10513'])
#     noise_12359   = float(dataset_noise['12359'])

#     paper_N    = float(current_params.waste_N_frac("paper"))
#     plastic_N  = float(current_params.waste_N_frac("plastic"))
#     wood_N     = float(current_params.waste_N_frac("wood"))
#     textile_N  = float(current_params.waste_N_frac("textiles"))
#     wet_N      = float(current_params.waste_N_frac("wet_organic"))
#     sludge_N   = float(current_params.waste_N_frac("sludge"))
#     other_N    = float(current_params.waste_N_frac("other_materials"))
#     haz_N      = float(current_params.waste_N_frac("hazardous"))
#     contam_N   = float(current_params.waste_N_frac("contaminated_masses"))
#     mixed_N    = float(current_params.waste_N_frac("mixed_waste"))
#     rubber_N   = float(current_params.waste_N_frac("rubber"))
#     park_N     = float(current_params.waste_N_frac("park_garden"))
    
#     manure_N    = float(current_params.get("manure_N_frac"))
#     fish_N      = float(current_params.get("animal_waste_N_frac"))
#     loss_factor = float(current_params.get("digestate_loss_fraction"))

#     df_manure = preloaded_data.get('biogass_manure')
        
#     year_values_manure = {}
#     for r in range(2, 14):
#         try:
#             year = int(float(str(df_manure.iloc[r, 3]).strip())) 
#             val_raw = float(df_manure.iloc[r, 7])                
#             year_values_manure[year] = (val_raw / 1000.0) * manure_N * noise_biogass
#         except (ValueError, TypeError, IndexError):
#             continue

#     df_fish = preloaded_data.get('ssb_waste_12359')
        
#     year_values_fish = {}
#     for col in range(3, df_fish.shape[1]):
#         try:
#             year_val = str(df_fish.iloc[2, col]).strip() 
#             if not year_val.replace('.0', '').isdigit():
#                 continue
#             year = int(float(year_val))
#             val_raw = float(df_fish.iloc[28, col])
#             year_values_fish[year] = val_raw * fish_N * noise_12359
#         except (ValueError, TypeError, IndexError):
#             continue

#     df_10513 = preloaded_data.get('ssb_waste_10513')

#     final_values = {}

#     for col in range(1, 110, 9):
#         if col >= df_10513.shape[1]:
#             break
            
#         cell_year = str(df_10513.iloc[3, col]).strip() 
#         if cell_year.replace('.0', '').isdigit():
#             year = int(float(cell_year))
#             collected_years.add(year)
            
#             try:
#                 v_10513 = 0.0
#                 v_10513 += float(df_10513.iloc[6, col + 2]) * wet_N       
#                 v_10513 += float(df_10513.iloc[7, col + 2]) * park_N      
#                 v_10513 += float(df_10513.iloc[8, col + 2]) * wood_N      
#                 v_10513 += float(df_10513.iloc[9, col + 2]) * sludge_N    
#                 v_10513 += float(df_10513.iloc[10, col + 2]) * paper_N    
#                 v_10513 += float(df_10513.iloc[16, col + 2]) * plastic_N  
#                 v_10513 += float(df_10513.iloc[17, col + 2]) * rubber_N   
#                 v_10513 += float(df_10513.iloc[18, col + 2]) * textile_N  
#                 v_10513 += float(df_10513.iloc[21, col + 2]) * haz_N      
#                 v_10513 += float(df_10513.iloc[22, col + 2]) * mixed_N    
#                 v_10513 += float(df_10513.iloc[23, col + 2]) * other_N    
#                 v_10513 += float(df_10513.iloc[24, col + 2]) * contam_N   
                
#                 value = v_10513 * noise_10513
                
#                 if year > 2012:
#                     value += year_values_manure.get(year, 0.0)
                    
#                 if year > 2016:
#                     value += year_values_fish.get(year, 0.0)
                
#                 final_values[year] = value * loss_factor
                
#             except (ValueError, TypeError, IndexError):
#                 final_values[year] = 0.0

#     for year in range(1984, 2012):
#         collected_years.add(year)
#         final_values[year] = 0.0

#     for year in sorted(final_values.keys()):
#         val = final_values[year]
        
#         results.append({
#             'flow_name': flow_code,
#             'year': year,
#             'value': val,
#             'comment': 'ok' if year >= 2012 else 'Satt til 0 før 2012',
#             'data_sources': 'SSB, Landbruksdirektoratet, Biogass Norge' if year >= 2012 else 'Ingen data før 2012'
#         })

#     missing_years = EXPECTED_YEARS - collected_years
#     report_missing_years(flow_code, missing_years, results)
    
def _add_so_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok'
    data_sources = 'CRLTAP Inventory Submissions'

    conv = float(current_params.get("NOx_to_N_factor"))    
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=PR_SO_CRLTAP_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        val_clean = float(value)
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': val_clean,
            'comment': comment, 
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_so_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok'
    data_sources = 'CRLTAP Inventory Submissions'

    conv = float(current_params.get("NH3_to_N_factor"))
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=PR_SO_CRLTAP_SECTORS,
        pollutant='NH3',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        val_clean = float(value)
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': val_clean,
            'comment': comment, 
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_so_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok'
    data_sources = 'UNFCCC CRT'

    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    key_n2o = 'UNFCCC_emissions'
    noise_val = dataset_noise[key_n2o]

    df_so_emissions = preloaded_data.get('n2o_so_raw')
    for index, row in df_so_emissions.iterrows():
        year_val = row['year']
        n2o_val = row['value']  # Kolonnenavnet i csv er 'value'
        
        if pd.isna(year_val) or pd.isna(n2o_val):
            continue
            
        year = int(year_val)
        if year not in EXPECTED_YEARS:
            continue
            
        collected_years.add(year)
        
        base_value = float(n2o_val) * conv_N2O
        value = base_value * noise_val
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_export_for_recycling_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    flow_code = 'PR.SO-RW.RW-Export for recycling-Nmix'
    data_sources = 'SSB'
    collected_years = set()
    
    year_values = find_export_for_recycling(
        results=None,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        dataset_noise=dataset_noise
    )

    for year, value in year_values.items():
        collected_years.add(year)
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': 'ok',
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_export_for_reuse_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    flow_code = 'PR.SO-RW.RW-Export for reuse-Nmix'
    data_sources = 'SSB'
    collected_years = set()
    
    year_values = find_export_for_reuse(
        results=None,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        dataset_noise=dataset_noise
    )
    
    for year, value in year_values.items():
        collected_years.add(year)
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': 'ok',
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)

    
def _add_ag_sewage_sludge_fertilizer_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.WW-AG.SM-Sewage sludge fertilizer-Nmix'
    dataset_key = '05279'
    noise_val = dataset_noise[dataset_key]
    collected_years = set()
    comment = 'ok'
    N_content = float(current_params.waste_N_frac('sludge'))
    df_modern = preloaded_data['sewage_sludge_modern']
    df_hist = preloaded_data['sewage_sludge_historical']
    
    # 2002-2024 
    data_sources = 'SSB tab 05279'
    for col_idx in range(2, len(df_modern.columns)):
        year_val = df_modern.iloc[2, col_idx]
        if year_val is None or pd.isna(year_val):
            continue
        year = int(year_val)
        
        raw_val = df_modern.iloc[4, col_idx]
        if raw_val is None or pd.isna(raw_val):
            continue
            
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        perturbed_tonnage = raw_tonnage*noise_val
        
        value = (perturbed_tonnage / 1000) * N_content 
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 1993-2001
    noise_val = dataset_noise['historical_waste']
    for r in range(1, 10):  
        year_val = df_hist.iloc[r, 0]
        if year_val is None or pd.isna(year_val): 
            continue
        year = int(year_val)  
        
        raw_val = df_hist.iloc[r, 1]
        if raw_val is None or pd.isna(raw_val): 
            continue
        
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        perturbed_tonnage = raw_tonnage*noise_val
        
        share = float(df_hist.iloc[r, 3]) / 100  
        value = perturbed_tonnage * share * N_content  
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
            
    #  1990-1992 (Ekstrapolering)
    values_93_95 = [res['value'] for res in results if res['flow_name'] == flow_code and res['year'] in [1993, 1994, 1995]]
    mean_val = sum(values_93_95) / 3 if values_93_95 else 0.0
    
    data_sources_ext = 'extrapolated'
    for year in range(1990, 1993):  
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': mean_val, 
            'comment': 'Ekstrapolert snitt (1993-1995) med MC-støy',
            'data_sources': data_sources_ext
        })    
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_hs_sewage_sludge_fertilizer_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.WW-HS.HS-Sewage sludge fertilizer-Nmix'
    dataset_key = '05279'
    collected_years = set()
    comment = 'ok'
    
    N_content = float(current_params.waste_N_frac('sludge'))
    
    df_modern = preloaded_data['sewage_sludge_modern']
    df_hist = preloaded_data['sewage_sludge_historical']
    noise_modern = dataset_noise[dataset_key]
    noise_hist = dataset_noise['historical_waste']
    
    # 1. 2002-2024
    data_sources = 'SSB table 05279'
    for col_idx in range(2, len(df_modern.columns)):
        year_val = df_modern.iloc[2, col_idx]
        if year_val is None or pd.isna(year_val):
            continue
        year = int(year_val)
            
        val_green = df_modern.iloc[5, col_idx] # Radindeks 5 (Grøntareal)
        val_soil = df_modern.iloc[6, col_idx]  # Radindeks 6 (Jordprodusent)
        
        if (val_green is None or pd.isna(val_green)) and (val_soil is None or pd.isna(val_soil)):
            continue
            
        collected_years.add(year)
        
        tonnage_green = float(val_green) if val_green is not None and not pd.isna(val_green) else 0.0
        tonnage_soil = float(val_soil) if val_soil is not None and not pd.isna(val_soil) else 0.0
        
        perturbed_green = tonnage_green*noise_modern
        perturbed_soil = tonnage_soil*noise_modern
        
        value = ((perturbed_green + perturbed_soil) / 1000) * N_content 
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 2. 1993-2001
    for r in range(1, 10):  
        year_val = df_hist.iloc[r, 0]
        if year_val is None or pd.isna(year_val): 
            continue
        year = int(year_val)  
        
        raw_val = df_hist.iloc[r, 1]
        if raw_val is None or pd.isna(raw_val): 
            continue
        
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        perturbed_tonnage = raw_tonnage*noise_hist
        
        share = float(df_hist.iloc[r, 2]) / 100  # Kolonne indeks 2 er 'grøntareal %'
        value = perturbed_tonnage * share * N_content  
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 3. 1990-1992
    values_93_95 = [res['value'] for res in results if res['flow_name'] == flow_code and res['year'] in [1993, 1994, 1995]]
    mean_val = sum(values_93_95) / 3 if values_93_95 else 0.0
    
    data_sources_ext = 'extrapolated'
    for year in range(1990, 1993):  
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': mean_val, 
            'comment': 'Ekstrapolert snitt (1993-1995) med MC-støy',
            'data_sources': data_sources_ext
        })    
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_ww_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.WW-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok'
    data_sources = 'UNFCCC CRT'

    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    key_n2o = 'UNFCCC_emissions'
    noise_val = dataset_noise[key_n2o]

    df_ww_emissions = preloaded_data.get('n2o_ww_raw')
    for index, row in df_ww_emissions.iterrows():
        year_val = row['year']
        n2o_val = row['value']  # Kolonnenavnet i csv er 'value'
        
        if pd.isna(year_val) or pd.isna(n2o_val):
            continue
            
        year = int(year_val)
        if year not in EXPECTED_YEARS:
            continue
            
        collected_years.add(year)
        
        base_value = float(n2o_val) * conv_N2O
        value = base_value * noise_val
 
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_solid_waste_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    flow_code = 'PR.SO-RW.RW-Solid waste export-Nmix'
    collected_years = set()
    comment = 'ok'
    data_sources = 'SSB tab 08801'

    trade_results = []
    process_generic_trade_flow(
        results=trade_results, 
        preloaded_data=preloaded_data, 
        current_params=current_params,
        current_trade_factors=current_trade_factors, 
        flow_code=flow_code,
        target_types=['kommunalt_avfall', 'farlig_avfall', 'annet_avfall'],
        is_import=False,  # Eksport (tilsvarer impeks = 2)
        dataset_noise=dataset_noise
    )

    trade_years_dict = {row['year']: row['value'] for row in trade_results}

    for year in sorted(EXPECTED_YEARS):
        # Vi forholder oss til tidslinjen fra opprinnelig funksjon (f.eks. fra 1988 og utover)
        if year < 1988:
            continue
            
        collected_years.add(year)

        if 1988 <= year <= 2001:
            value = 0.0
            current_comment = comment
        else:
            # Hent den beregnede MC-verdien fra handelsfunksjonen (default til 0.0 hvis år mangler)
            value = float(trade_years_dict.get(year, 0.0))
            current_comment = comment

        # Sikre mot eventuelle NaN-verdier eller negative avvik fra støyen
        if value < 0 or pd.isna(value):
            value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': current_comment,
            'data_sources': data_sources
        })

    # 4. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
def _add_sewage_sludge_landfill_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.WW-PR.SO-Sewage sludge landfill-Nmix'
    collected_years = set()
    comment = 'ok'
    
    N_content = float(current_params.waste_N_frac('sludge'))
    
    df_modern = preloaded_data['sewage_sludge_modern']
    df_hist = preloaded_data['sewage_sludge_historical']
    
    # 1. 2002-2024
    data_sources = 'SSB table 05279'
    noise_05279 = dataset_noise['05279']
    # Det opprinnelige skriptet stoppet på kolonne 26 i Excel (tilsvarer indeks 25 her)
    for col_idx in range(2, min(25, len(df_modern.columns))):
        year_val = df_modern.iloc[2, col_idx]
        if year_val is None or pd.isna(year_val):
            continue
        year = int(year_val)
            
        val_cover = df_modern.iloc[7, col_idx]     # Radindeks 7 (Dekkmasse avfallsfylling)
        val_landfill = df_modern.iloc[8, col_idx]  # Radindeks 8 (Slamdeponi)
        
        if (val_cover is None or pd.isna(val_cover)) and (val_landfill is None or pd.isna(val_landfill)):
            continue
            
        collected_years.add(year)
        
        tonnage_cover = float(val_cover) if val_cover is not None and not pd.isna(val_cover) else 0.0
        perturbed_cover = tonnage_cover*noise_05279
        value = (perturbed_cover / 1000) * N_content
        
        if val_landfill is not None and not isinstance(val_landfill, str) and not pd.isna(val_landfill):
            perturbed_landfill = val_landfill*noise_05279
            value += (perturbed_landfill / 1000) * N_content
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 2. 1993-2001
    noise_hist = dataset_noise['slamdisponering']
    for r in range(1, 10):  
        year_val = df_hist.iloc[r, 0]
        if year_val is None or pd.isna(year_val): 
            continue
        year = int(year_val)  
        
        raw_val = df_hist.iloc[r, 1]
        if raw_val is None or pd.isna(raw_val): 
            continue
        
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        perturbed_tonnage = raw_tonnage*noise_hist
        
        share = float(df_hist.iloc[r, 4]) / 100  # Kolonne indeks 4 er '% slamdeponi + avfallsfylling'
        value = perturbed_tonnage * share * N_content  
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 3. 1990-1992
    values_93_95 = [res['value'] for res in results if res['flow_name'] == flow_code and res['year'] in [1993, 1994, 1995]]
    mean_val = sum(values_93_95) / 3 if values_93_95 else 0.0
    
    data_sources_ext = 'extrapolated'
    for year in range(1990, 1993):  
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': mean_val, 
            'comment': 'Ekstrapolert snitt (1993-1995) med MC-støy',
            'data_sources': data_sources_ext
        })    
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_ww_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.WW-AT.AT-Emissions-N2'
    collected_years = set()
    comment = 'ok'
    data_sources = 'treatment plant reports (norskeutslipp.no / veas.nu)'
    dataset_key = 'nitrogenrensing_avlop'
    noise_val = dataset_noise[dataset_key]

    removal_default = float(current_params.get("avlop_removal_default_rate")) 
    N_released_df = preloaded_data.get('avlop_sewage_cleaning')
    df = N_released_df.copy()
    num_cols = [col for col in df.columns if col != 'år']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce') / 1000.0

    def _get_val(plant_column, target_year):
        row = df[df["år"] == target_year]
        val = row[plant_column].iloc[0]
        if pd.isna(val) or val is None:
            return 0.0
        return float(val)

    mean_Lillehammer = df["Lillehammer"].mean() 
    
    mask_veas = (df["år"] >= 2002) & (df["år"] <= 2003)
    mean_Veas = df.loc[mask_veas, "VEAS"].mean()
    
    mean_NordreFollo = df["Nordre Follo"].mean()
    
    mask_gard = (df["år"] >= 2002) & (df["år"] <= 2009)
    mean_Gardermoen = df.loc[mask_gard, "Gardermoen"].mean()
    
    mean_NRVA = df["NRVA"].mean()

    # Faktor-funksjon for renseeffekt: r / (1 - r)
    def _factor(r):
        return r / (1.0 - r)

    for year in EXPECTED_YEARS:
        collected_years.add(year)
        
        if year < 1995:
            value = 0.0
            
        elif year < 1997:  # Kun Lillehammer
            value = mean_Lillehammer * _factor(removal_default)
            
        elif year < 1998:  # + VEAS og Nordre Follo
            value = (mean_Lillehammer + mean_Veas + mean_NordreFollo) * _factor(removal_default)
            
        elif year < 2002:  # + Gardermoen
            value = (mean_Lillehammer + mean_Veas + mean_NordreFollo + mean_Gardermoen) * _factor(removal_default)
            
        elif year == 2002:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year + 1) * _factor(removal_default)  # Ekstrapolert fra neste år
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0  # Reverser ktN-deling for rensegrad-prosent
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            
        elif year == 2003:  # + NRVA
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += mean_NRVA * removal_default  # Beholder din originale formel for akkurat dette leddet
            
        elif year in [2004, 2005]:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += mean_NordreFollo * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year == 2006:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += mean_NordreFollo * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += mean_NRVA * _factor(removal_default)
            
        elif year in [2007, 2008]:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year in range(2009, 2012):
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year == 2012:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += mean_NordreFollo * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year in range(2013, 2016):
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year == 2016:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            value += _get_val("Bekkelaget", year) * _factor(removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year in [2017, 2018]:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            value += _get_val("Bekkelaget", year) * _factor(removal_default)
            
            rem_nrva = _get_val("rensegrad NRVA", year) * 1000.0
            value += _get_val("NRVA", year) * _factor(rem_nrva if rem_nrva > 0 else removal_default)
            
        elif year in [2019, 2020]:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            
            rem_nrva = _get_val("rensegrad NRVA", year) * 1000.0
            value += _get_val("NRVA", year) * _factor(rem_nrva if rem_nrva > 0 else removal_default)
            
        elif year == 2021:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year < 2025:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            
            rem_nrva = _get_val("rensegrad NRVA", year) * 1000.0
            value += _get_val("NRVA", year) * _factor(rem_nrva if rem_nrva > 0 else removal_default)
            
        else:  # 2025 og fremover (inkluderer Hokksund)
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            
            rem_nrva = _get_val("rensegrad NRVA", year) * 1000.0
            value += _get_val("NRVA", year) * _factor(rem_nrva if rem_nrva > 0 else removal_default)
            value += _get_val("Hokksund", year) * _factor(removal_default)

        value *= noise_val

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),  
            'comment': comment,
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_treated_ww_discharge_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.WW-HY.CW-Treated wastewater discharge-Nmix'
    dataset_key = '05280'
    collected_years = set()
    comment = 'ok'
    
    df_modern = preloaded_data['hy_ssb_05280_raw']
    df_hist = preloaded_data['avlop_utslipp_historical']
    
    # 1. Nyere data: 2002 til 2024 
    noise_val = dataset_noise[dataset_key]
    data_sources = 'SSB table 05280'
    max_col = min(26, df_modern.shape[1])
    
    for col_idx in range(3, max_col):
        year_val = df_modern.iloc[2, col_idx]
        raw_val = df_modern.iloc[3, col_idx]
        
        if pd.isna(year_val) or pd.isna(raw_val):
            continue
            
        year = int(float(str(year_val).strip()))
        raw_tonnage = float(raw_val)
            
        collected_years.add(year)
        perturbed_tonnage = raw_tonnage*noise_val
        value = perturbed_tonnage / 1000.0
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 2. Historiske data: 1997 til 2001 
    noise_val = dataset_noise['utslipp_avløp']
    value_1997 = None
    for r in range(1, 6):
        year_val = df_hist.iloc[r, 0]
        if year_val is None or pd.isna(year_val):
            continue
        year = int(year_val)
        
        raw_val = df_hist.iloc[r, 1]
        if raw_val is None or pd.isna(raw_val):
            continue
            
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        
        perturbed_tonnage = raw_tonnage*noise_val
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': perturbed_tonnage, 
            'comment': comment,
            'data_sources': data_sources
        })
        
        if year == 1997:
            value_1997 = perturbed_tonnage

    # 3. Ekstrapolering bakover: 1990 til 1996 (Konstant basert på perturbert 1997-verdi)
    data_sources_ext = 'extrapolated'
    for year in range(1990, 1997):  
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value_1997, 
            'comment': 'Ekstrapolert verdi basert på 1997 med MC-støy',
            'data_sources': data_sources_ext
        })    
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)