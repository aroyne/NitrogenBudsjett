#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:34:21 2025

@author: anja
"""
import pandas as pd  # Ensure you have pandas installed
import openpyxl

from calculations.n_params import NParameters
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    combine_uncertainties_percent,
    get_uncertainty,
    process_generic_trade_flow
)

expected_years = EXPECTED_YEARS

def execute_calculations_at(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    MC-VERSJON: Beregner nitrogenflyt for atmosfæren uten fil-I/O i løkka.
    Krasjer umiddelbart hvis kritiske inndata mangler.
    """
    results = []
    
    # 1. Hent og verifiser atmosfæriske rådata – krasj hardt hvis de mangler
    df_atm = preloaded_data.get('atm_in_out')
    if df_atm is None:
        raise ValueError("[KRITISK] Data for 'atm_in_out' mangler i preloaded_data under atmosfære-beregninger!")

    _add_atmospheric_outflow_oxn_mc(results, df_atm, current_params, dataset_noise)
    _add_atmospheric_outflow_rdn_mc(results, df_atm, current_params, dataset_noise)
    
    # 2. Hent handelsvolum – krasj hardt hvis det mangler
    df_vol = preloaded_data.get('compressed_trade_volume')
    if df_vol is None:
        raise ValueError("[KRITISK] 'compressed_trade_volume' mangler i preloaded_data. Kan ikke beregne ammoniakkimport!")

    # Genererer {år: verdi}-ordboken via fellesfunksjonen din
    ammonia_import_dict = process_generic_trade_flow(
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        target_types='NH3',  
        is_import=True      
    )    
            
    # Kjør fikseringsberegningen din
    _add_OP_N2_fixation_mc(results, preloaded_data, current_params, ammonia_import_dict, dataset_noise)    
    
    # 3. Biologiske N2-fikseringer (parameter-baserte - krasjer internt i parameter-get hvis de mangler)
    _add_AG_N2_fixation_mc(results, current_params)
    _add_FO_N2_fixation_mc(results, current_params)
    _add_OL_N2_fixation_mc(results, current_params)
    _add_SW_N2_fixation_mc(results, current_params)
    
    # 4. Deponeringsstrømmer (per arealklasse og komponent)
    _deposition_flow_mc(results, 'AT.AT-AG.SM-Deposition-OXN', 'jordbruk', 'NOx', preloaded_data, current_params, dataset_noise)    
    _deposition_flow_mc(results, 'AT.AT-AG.SM-Deposition-RDN', 'jordbruk', 'Nred', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-FS.FO-Deposition-OXN', 'skog', 'NOx', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-FS.FO-Deposition-RDN', 'skog', 'Nred', preloaded_data, current_params, dataset_noise)  
    _deposition_flow_mc(results, 'AT.AT-FS.OL-Deposition-OXN', 'annet', 'NOx', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-FS.OL-Deposition-RDN', 'annet', 'Nred', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-HS.HS-Deposition-OXN', 'bebyggelse', 'NOx', preloaded_data, current_params, dataset_noise) 
    _deposition_flow_mc(results, 'AT.AT-HS.HS-Deposition-RDN', 'bebyggelse', 'Nred', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-HY.SW-Deposition-OXN', 'overflatevann', 'NOx', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-HY.SW-Deposition-RDN', 'overflatevann', 'Nred', preloaded_data, current_params, dataset_noise)

    return results


def _deposition_flow_mc(results, flow_code, class4, poll, preloaded_data, current_params, dataset_noise):
    data = preloaded_data.get('deposition_data')
    if data is None:
        raise ValueError(f"[KRITISK] Deponeringsdata mangler i preloaded_data for {flow_code}!")

    # Definer de to unike dataset-nøklene som brukes i denne funksjonen
    key_dep = 'Deposition'
    key_interp = 'trend interpolation'
    
    # Sjekk støy-ordboken og krasj umiddelbart hvis nøklene mangler
    if not dataset_noise or key_dep not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_dep}' mangler i dataset_noise for {flow_code}!")
    if key_interp not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_interp}' mangler i dataset_noise for {flow_code}!")

    # Optimalisering: Filtrer på pollutant og arealklasse én gang utenfor års-løkka
    mask_base = (data["pollutant"] == poll) & (data["class4"] == class4)
    df_subset = data[mask_base]
    
    # Lag en lynrask oppslagstabell fra periode til verdi
    period_map = dict(zip(df_subset["period"], df_subset["N_tonn"]))
    
    def period_for_year(y):
        if y < 1988: return "1983-1987"
        elif y < 1992: return "1988-1992"
        elif y < 1997: return "1992-1996"
        elif y < 2002: return "1997-2001"
        elif y < 2007: return "2002-2006"
        elif y < 2012: return "2007-2011"
        else: return "2012-2016"

    value_2016 = None
    value_last = None
    
    # Løp igjennom alle år kronologisk (viktig for ekstrapoleringen)
    for year in sorted(EXPECTED_YEARS):
        comment = 'ok (MC-støy lagt på basert på uncertainty_type)'
        
        if year < 2017:
            period = period_for_year(year)
            tonn_val = period_map.get(period)
            if tonn_val is None:
                raise ValueError(f"Ingen deponeringsdata funnet for {flow_code}, klasse={class4}, periode={period}")
                
            base_value = float(tonn_val) / 1000
            data_sources = 'NILU and geodata.no'
            
            # --- STØYLOGIKK FOR 'Deposition' ---
            noise_info = dataset_noise[key_dep]
            noise_val = noise_info['value']
            if noise_info['type'] == 'perc':
                value = base_value * noise_val
            else:
                bound = noise_info['upp_bound'] if noise_val >= 0 else noise_info['low_bound']
                value = base_value + (noise_val * bound)
                
            if year == 2016:
                value_2016 = value
                
        elif year < 2022:
            # Skalering basert på 2016-verdien (beholder opprinnelig støy herfra)
            if value_2016 is None:
                raise ValueError(f"[KRITISK] Mangler 2016-verdi for å kunne skalere årene 2017-2021 i {flow_code}!")
            if poll == 'NOx':
                value = value_2016 * 61440 / 68166
            else:
                value = value_2016 * 61175 / 73494
            value_last = value
            data_sources = 'NILU and geodata.no'
            
        else:
            # Siste år ekstrapoleres flatt videre fra value_last
            if value_last is None:
                raise ValueError(f"[KRITISK] Mangler historisk verdi fra før 2022 for å kunne ekstrapolere i {flow_code}!")
            base_value = value_last
            data_sources = 'extrapolated'
            
            # --- STØYLOGIKK FOR 'trend interpolation' ---
            noise_info = dataset_noise[key_interp]
            noise_val = noise_info['value']
            if noise_info['type'] == 'perc':
                value = base_value * noise_val
            else:
                bound = noise_info['upp_bound'] if noise_val >= 0 else noise_info['low_bound']
                value = base_value + (noise_val * bound)

        # Fysisk sperre
        if value < 0:
            value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': comment,
            'data_sources': data_sources
        })
        
        
def _add_OP_N2_fixation_mc(results, preloaded_data, current_params, ammonia_import_dict, dataset_noise):
    flow_code = 'AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2'
    collected_years = set()
    
    dataset_key = 'Fertilizer by nutrient'
    data_sources = 'FAOSTAT Fertilizer by nutrient + SSB'
    
    # Hent ferdiglastet FAOSTAT-data – krasj hardt hvis de mangler
    df_faostat = preloaded_data.get('faostat_fertilizer')
    if df_faostat is None:
        raise ValueError(f"[KRITISK] Mangler 'faostat_fertilizer' i preloaded_data for {flow_code}!")

    # Sjekk støydata for dette datasettet i denne runden og krasj hvis de mangler
    if not dataset_noise or dataset_key not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{dataset_key}' mangler i dataset_noise for {flow_code}!")

    for _, row in df_faostat.iterrows():
        year = int(row['Year'])
        if year in ammonia_import_dict:  # Data finnes fra handelsstart (1988)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            
            # FAOSTAT-verdi gjøres om fra tonn til kt N
            base_faostat = float(row['Value']) / 1000 
            
            # --- STØYLOGIKK FOR 'Fertilizer by nutrient' ---
            noise_info = dataset_noise[dataset_key]
            noise_val = noise_info['value']
            unc_type = noise_info['type']
            
            if unc_type == 'perc':
                perturbed_faostat = base_faostat * noise_val
            else:
                bound = noise_info['upp_bound'] if noise_val >= 0 else noise_info['low_bound']
                perturbed_faostat = base_faostat + (noise_val * bound)
            
            if perturbed_faostat < 0:
                perturbed_faostat = 0.0

            # Formel: (FAOSTAT med støy) - (Ammoniakkimport med støy)
            value = perturbed_faostat - ammonia_import_dict[year]
            
            if value < 0:
                comment = 'ok (Negativ verdi pga. MC-støy i massebalanse)'
            elif value == 0:
                comment = 'ok (Nullverdi pga. MC-støy)'
            else:
                comment = 'ok (MC-støy lagt på)'
            
            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': value, 
                'comment': comment,
                'data_sources': data_sources
            })
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    

def _add_AG_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-AG.SM-Biological N2 fixation-N2'
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'Bleken & Bakken'
    
    val_param = current_params.get("AG_biological_fixation_N2")
    if val_param is None:
        raise KeyError(f"[KRITISK] Parameter 'AG_biological_fixation_N2' mangler i current_params for {flow_code}!")
        
    value = float(val_param)
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
        })


def _add_FO_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-FS.FO-N2 fixation-N2'
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'Moldan (2025) and SSB'
    
    val_param = current_params.get("FO_biological_fixation_N2")
    if val_param is None:
        raise KeyError(f"[KRITISK] Parameter 'FO_biological_fixation_N2' mangler i current_params for {flow_code}!")
        
    value = float(val_param)
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
        })


def _add_OL_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-FS.OL-N2 fixation-N2'
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CORINE land cover inventory and REddy & DeLaune (2008)'
    
    val_param = current_params.get("OL_biological_fixation_N2")
    if val_param is None:
        raise KeyError(f"[KRITISK] Parameter 'OL_biological_fixation_N2' mangler i current_params for {flow_code}!")
        
    value = float(val_param)
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
        })


def _add_SW_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-HY.SW-N2 fixation-N2'
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'NIBIO and Reddy & DeLaune (2008)'
    
    val_param = current_params.get("SW_biological_fixation_N2")
    if val_param is None:
        raise KeyError(f"[KRITISK] Parameter 'SW_biological_fixation_N2' mangler i current_params for {flow_code}!")
        
    value = float(val_param)
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
        })
        
        
def _add_atmospheric_outflow_oxn_mc(results, df_atm, current_params, dataset_noise):
    flow_code = 'AT.AT-RW.RW-Atmospheric outflow-OXN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på uncertainty_type)'
    
    for r in range(5, 45):
        if r >= len(df_atm):
            break
            
        year_val = df_atm.iloc[r, 0]
        if pd.isna(year_val):
            continue
            
        year = int(year_val)
        collected_years.add(year)
        
        status_val = str(df_atm.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            
        base_value = float(df_atm.iloc[r, 2]) / 10  
        
        # --- STØYLOGIKK: Krasj hardt hvis nøkkelen mangler ---
        if not dataset_noise or dataset_key not in dataset_noise:
            raise KeyError(f"[KRITISK] Støy-nøkkel '{dataset_key}' mangler i dataset_noise for {flow_code}!")
            
        noise_info = dataset_noise[dataset_key]
        noise_val = noise_info['value']
        unc_type = noise_info['type']
        
        if unc_type == 'perc':
            value = base_value * noise_val
        else:
            bound = noise_info['upp_bound'] if noise_val >= 0 else noise_info['low_bound']
            value = base_value + (noise_val * bound)
            
        if value < 0:
            value = 0.0
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_atmospheric_outflow_rdn_mc(results, df_atm, current_params, dataset_noise):
    flow_code = 'AT.AT-RW.RW-Atmospheric outflow-RDN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på uncertainty_type)'
    
    for r in range(5, 45): 
        if r >= len(df_atm):
            break
            
        year_val = df_atm.iloc[r, 0]
        if pd.isna(year_val):
            continue
            
        year = int(year_val)
        collected_years.add(year)
        
        status_val = str(df_atm.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            
        base_value = float(df_atm.iloc[r, 4]) / 10  
        
        # --- STØYLOGIKK: Krasj hardt hvis nøkkelen mangler ---
        if not dataset_noise or dataset_key not in dataset_noise:
            raise KeyError(f"[KRITISK] Støy-nøkkel '{dataset_key}' mangler i dataset_noise for {flow_code}!")
            
        noise_info = dataset_noise[dataset_key]
        noise_val = noise_info['value']
        unc_type = noise_info['type']
        
        if unc_type == 'perc':
            value = base_value * noise_val
        else:
            bound = noise_info['upp_bound'] if noise_val >= 0 else noise_info['low_bound']
            value = base_value + (noise_val * bound)
            
        if value < 0:
            value = 0.0
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


# Example usage
if __name__ == "__main__":
    # Testkall vil nå krasje kontrollert under testing hvis data ikke rutes inn riktig
    calculations = execute_calculations_at({}, {}, {}, {})