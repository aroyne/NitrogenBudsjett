#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:50:01 2026

@author: anja
"""

import pandas as pd  # Ensure you have pandas installed
import openpyxl
from calculations.n_params import NParameters
from calculations.shared_flow_calculations import (
    get_waste_frac,
    find_export_for_recycling,
    find_export_for_reuse,
    find_household_waste,
    find_landfill_emissions_to_water,
    find_other_industry_waste,
    find_recycling,
    find_sewage_sludge_biogas,
    find_solid_waste_export)
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    combine_uncertainties_percent,
    get_uncertainty,
    read_trade_data,
    # find_trade_data
)

def execute_calculations_pr(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    Hovedfunksjon for RW-poolen. Kjører alle underberegninger.
    Alle distribusjoner trekkes sentralt før denne kjøres.
    """
    results = []

    _add_waste_to_energy_mc(results, preloaded_data, current_params, dataset_noise)
    _add_recycling_mc(results, preloaded_data, current_params, dataset_noise, current_trade_factors)
    
    return results


def _apply_dataset_noise(base_value, dataset_key, dataset_noise, caller_func):
    """
    Legger støy på verdi. Krasjer hardt dersom støy-nøkkel mangler.
    """
    if not dataset_noise or dataset_key not in dataset_noise:
        raise KeyError(
            f"[KRITISK FEIL] Støy-nøkkel '{dataset_key}' mangler i dataset_noise under kallet fra {caller_func.__name__}!"
        )

    noise_info = dataset_noise[dataset_key]
    noise_val = noise_info['value']
    
    if noise_info['type'] == 'perc':
        return base_value * noise_val
    else:
        bound = noise_info['upp_bound'] if noise_val >= 0 else noise_info['low_bound']
        return base_value + (noise_val * bound)


def _add_waste_to_energy_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-EF.EC-Waste to energy-Nmix'
    collected_years = set()
    data_sources = 'SSB'
    
    # Hent N-fraksjoner via current_params - krasjer om nøkkel mangler
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
    if df_05281 is None:
        raise ValueError(f"[KRITISK] Data 'ssb_waste_05281' mangler i preloaded_data for {flow_code}!")

    for col in range(3, 20):  
        # Ingen try/except eller strip-fallbacks her; feiler om dataen er korrupt eller tom
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

        value = _apply_dataset_noise(raw_tonnage, dataset_key_05281, dataset_noise, _add_waste_to_energy_mc)
        if value < 0: value = 0.0

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på 05281)', 'data_sources': data_sources
        })

    # =========================================================================
    # 2. PERIODE 2012-2023: SSB Tabell 10513 (Nøkkel: ssb_waste_10513)
    # =========================================================================
    dataset_key_10513 = '10513'
    df_10513 = preloaded_data.get('ssb_waste_10513')
    if df_10513 is None:
        raise ValueError(f"[KRITISK] Data 'ssb_waste_10513' mangler i preloaded_data for {flow_code}!")

    # Endret fra 110 til 101 for å hindre at .iloc går out-of-bounds på siste steget (som skal være 100)
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

        value = _apply_dataset_noise(raw_tonnage, dataset_key_10513, dataset_noise, _add_waste_to_energy_mc)
        if value < 0: value = 0.0

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på 10513)', 'data_sources': data_sources
        })
        
    # =========================================================================
    # 3. PERIODE 1990-1994: Historisk ekstrapolering (Nøkkel: waste_historical_fractions)
    # =========================================================================
    dataset_key_hist = 'historical_waste'
    df_hist = preloaded_data.get('waste_historical_fractions')
    if df_hist is None:
        raise ValueError(f"[KRITISK] Data 'waste_historical_fractions' mangler i preloaded_data for {flow_code}!")

    # Henter dataene direkte slik funksjonene leverer dem i MC-miljøet
    household_waste = find_household_waste(preloaded_data, current_params, dataset_noise)
    industry_waste, _ = find_other_industry_waste(
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
        
        # Hent basis-nitrogenverdiene
        waste = household_waste[year] + industry_waste[year]
        
        if year < 1992:
            inc_frac = inc_frac_1985 + change_per_year * (year - 1985)
            comment_str = 'extrapolated (MC-støy lagt på basisdata)'
        else:
            inc_frac = float(df_hist.iloc[r_iloc, 1]) / 100
            comment_str = 'ok (MC-støy lagt på basisdata)'
            r_iloc += 1
            
        # Nøyaktig opprinnelig formel
        raw_val = waste * inc_frac
        
        value = _apply_dataset_noise(raw_val, dataset_key_hist, dataset_noise, _add_waste_to_energy_mc)

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': comment_str, 'data_sources': data_sources
        })
        
    # Sjekk om tidsserien har hull eller mangler år. Krasj hvis den ikke er komplett.
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_recycling_mc(results, preloaded_data, current_params, dataset_noise, current_trade_factors):
    flow_code = 'PR.SO-MP.OP-Recycling-Nmix'
    collected_years = set()
    data_sources = 'SSB'

    year_values = find_recycling(
        preloaded_data=preloaded_data,
        current_params=current_params,
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
            'comment': 'ok (MC-støy integrert i datagrunnlag)',
            'data_sources': data_sources
        })

    # Beholder rapporteringen av manglende år her også
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
