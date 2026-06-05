#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:34:21 2025

@author: anja
"""
import pandas as pd
import openpyxl

from calculations.n_params import NParameters
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    combine_uncertainties_percent,
    get_uncertainty,
)
from calculations.shared_flow_calculations import (
    find_ammonia_import
)

expected_years = EXPECTED_YEARS

def execute_calculations_mc(preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogenflyt for atmosfæren uten fil-I/O i løkka.
    Returnerer rå-ordbøker for denne spesifikke iterasjonen.
    """
    results = []
    
    # Hent ut den forhåndsinnleste rå-DataFramen fra datalasteren vår
    df_atm = preloaded_data.get('atm_in_out')
    
    # Hvis vi ikke har lastet data, avbryter vi kontrollert
    if df_atm is None:
        print("[ADVARSEL] Data for 'atm_in_out' mangler i preloaded_data.")
        return results

    # 1. Kjør atmosfærisk utstrømning
    _add_atmospheric_outflow_oxn_mc(results, df_atm, current_params, dataset_noise)
    _add_atmospheric_outflow_rdn_mc(results, df_atm, current_params, dataset_noise)
    
    # 2. Hent ferdigberegnet ammoniakkimport fra fellesfunksjonen.
    prepared_trade_all = preloaded_data.get('trade_data')
    trade_params = preloaded_data.get('trade_params')
    
    if prepared_trade_all is not None and trade_params is not None:
        
        is_nh3 = prepared_trade_all['type'] == 'NH3'
        is_import = prepared_trade_all['impeks'] == 1
        
        df_ammonia_prepared = prepared_trade_all[is_nh3 & is_import].copy()
        df_ammonia_prepared['type'] = df_ammonia_prepared['impeks']
        
        ammonia_import_dict = find_ammonia_import(df_ammonia_prepared, current_params, trade_params)
        
        # Kjør beregningen for ammoniakksyntese (gjødselfiksering)
        _add_OP_N2_fixation_mc(results, preloaded_data, current_params, ammonia_import_dict, dataset_noise)
        
    else:
        print("[ADVARSEL] Mangler handelsdata i preloaded_data. Hopper over ammoniakk-strømmer.")    
    
    # 3. Biologiske N2-fikseringer (parameter-baserte)
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
        print(f"[ADVARSEL] Deponeringsdata mangler i preloaded_data for {flow_code}")
        return

    key_dep = 'Deposition'
    key_interp = 'trend interpolation'
    
    has_noise_dep = dataset_noise and key_dep in dataset_noise
    has_noise_interp = dataset_noise and key_interp in dataset_noise

    if dataset_noise and not hasattr(_deposition_flow_mc, "alarms_checked"):
        setattr(_deposition_flow_mc, "alarms_checked", True)
        if not has_noise_dep:
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{key_dep}' i dataset_uncertainties!")
        if not has_noise_interp:
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{key_interp}' i dataset_uncertainties!")

    mask_base = (data["pollutant"] == poll) & (data["class4"] == class4)
    df_subset = data[mask_base]
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
    
    for year in sorted(EXPECTED_YEARS):
        # Faglig kommentar som skal overleve aggregeringen til internasjonal rapportering
        comment = f"Atmospheric deposition of {poll} to land class '{class4}' calculated from NILU gridded models."
        
        if year < 2017:
            period = period_for_year(year)
            tonn_val = period_map.get(period)
            if tonn_val is None:
                raise ValueError(f"Ingen deponeringsdata funnet for {flow_code}, klasse={class4}, periode={period}")
                
            base_value = float(tonn_val) / 1000
            data_sources = 'NILU and geodata.no'
            
            if has_noise_dep:
                noise_info = dataset_noise[key_dep]
                noise_val = noise_info['value']
                if noise_info['type'] == 'perc':
                    value = base_value * noise_val
                else:
                    if noise_val >= 0:
                        value = base_value + (noise_val * noise_info['upp_bound'])
                    else:
                        value = base_value + (noise_val * noise_info['low_bound'])
            else:
                value = base_value
                
            if year == 2016:
                value_2016 = value
                
        elif year < 2022:
            if poll == 'NOx':
                value = value_2016 * 61440 / 68166
            else:
                value = value_2016 * 61175 / 73494
            value_last = value
            data_sources = 'NILU and geodata.no'
            
        else:
            base_value = value_last
            data_sources = 'extrapolated'
            comment += " (Extrapolated flat after 2021)."
            
            if has_noise_interp:
                noise_info = dataset_noise[key_interp]
                noise_val = noise_info['value']
                if noise_info['type'] == 'perc':
                    value = base_value * noise_val
                else:
                    if noise_val >= 0:
                        value = base_value + (noise_val * noise_info['upp_bound'])
                    else:
                        value = base_value + (noise_val * noise_info['low_bound'])
            else:
                value = base_value

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
    
    df_faostat = preloaded_data.get('faostat_fertilizer')
    if df_faostat is None:
        print(f"[ADVARSEL] Mangler faostat_fertilizer i preloaded_data.")
        return

    has_noise = dataset_noise and dataset_key in dataset_noise

    if dataset_noise and not has_noise and not hasattr(_add_OP_N2_fixation_mc, f"warned_{dataset_key}"):
        print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
        setattr(_add_OP_N2_fixation_mc, f"warned_{dataset_key}", True)

    for _, row in df_faostat.iterrows():
        year = int(row['Year'])
        if year in ammonia_import_dict:
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            
            base_faostat = float(row['Value']) / 1000 
            
            if has_noise:
                noise_info = dataset_noise[dataset_key]
                noise_val = noise_info['value']
                unc_type = noise_info['type']
                
                if unc_type == 'perc':
                    perturbed_faostat = base_faostat * noise_val
                else:
                    if noise_val >= 0:
                        perturbed_faostat = base_faostat + (noise_val * noise_info['upp_bound'])
                    else:
                        perturbed_faostat = base_faostat + (noise_val * noise_info['low_bound'])
            else:
                perturbed_faostat = base_faostat
            
            if perturbed_faostat < 0:
                perturbed_faostat = 0.0

            # Massebalanse: Gjødselproduksjon minus importert råstoff
            value = perturbed_faostat - ammonia_import_dict[year]
            
            comment = "Calculated via mass balance from FAOSTAT domestic fertilizer consumption and SSB ammonia trade statistics."
            
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
    comment = 'Agricultural biological nitrogen fixation (BNF) estimated from clover seed sales and fixed active pasture areas.'
    data_sources = 'Bleken & Bakken (1997) / NIBIO Totalkalkylen'
    
    value = float(current_params.get("AG_biological_fixation_N2", 0.0))
    
    # MERK: Sjekk at 'uncertainty'-nøkkelen er fjernet helt herfra
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })


def _add_FO_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-FS.FO-N2 fixation-N2'
    comment = 'Forest biological nitrogen fixation parameterized using fixed biome-specific fixation coefficients applied to national forest inventory areas.'
    data_sources = 'Moldan (2025) and SSB'
    
    value = float(current_params.get("FO_biological_fixation_N2", 18.0))
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })


def _add_OL_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-FS.OL-N2 fixation-N2'
    comment = 'Biological nitrogen fixation on unmanaged other lands calculated via biome area and reference wetland/alpine fixation limits.'
    data_sources = 'CORINE land cover inventory and Reddy & DeLaune (2008)'
    
    value = float(current_params.get("OL_biological_fixation_N2", 0.0))
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })


def _add_SW_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-HY.SW-N2 fixation-N2'
    comment = 'Surface water biological nitrogen fixation derived from oligotrophic lake surface area measurements and minimum cyanobacteria fixation parameters.'
    data_sources = 'NIBIO and Reddy & DeLaune (2008)'
    
    value = float(current_params.get("SW_biological_fixation_N2", 2.0))
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
        
def _add_atmospheric_outflow_oxn_mc(results, df_atm, current_params, dataset_noise):
    flow_code = 'AT.AT-RW.RW-Atmospheric outflow-OXN'
    collected_years = set()
    
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
            comment = 'Oxidized nitrogen atmospheric outflow escaping the national boundary (Extrapolated/interpolated trend).'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            comment = 'Oxidized nitrogen atmospheric outflow escaping the national boundary calculated via EMEP source-receptor budget matrices.'
            
        base_value = float(df_atm.iloc[r, 2]) / 10  
        
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        if dataset_noise and not has_noise and not hasattr(_add_atmospheric_outflow_oxn_mc, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            setattr(_add_atmospheric_outflow_oxn_mc, f"warned_{dataset_key}", True)
            
        if has_noise:
            noise_info = dataset_noise[dataset_key]
            noise_val = noise_info['value']
            unc_type = noise_info['type']
            
            if unc_type == 'perc':
                value = base_value * noise_val
            else:
                if noise_val >= 0:
                    value = base_value + (noise_val * noise_info['upp_bound'])
                else:
                    value = base_value + (noise_val * noise_info['low_bound'])
        else:
            value = base_value
            
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
            comment = 'Reduced nitrogen atmospheric outflow escaping the national boundary (Extrapolated/interpolated trend).'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            comment = 'Reduced nitrogen atmospheric outflow escaping the national boundary calculated via EMEP source-receptor budget matrices.'
            
        base_value = float(df_atm.iloc[r, 4]) / 10  
        
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        if dataset_noise and not has_noise and not hasattr(_add_atmospheric_outflow_rdn_mc, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            setattr(_add_atmospheric_outflow_rdn_mc, f"warned_{dataset_key}", True)
            
        if has_noise:
            noise_info = dataset_noise[dataset_key]
            noise_val = noise_info['value']
            unc_type = noise_info['type']
            
            if unc_type == 'perc':
                value = base_value * noise_val
            else:
                if noise_val >= 0:
                    value = base_value + (noise_val * noise_info['upp_bound'])
                else:
                    value = base_value + (noise_val * noise_info['low_bound'])
        else:
            value = base_value
            
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