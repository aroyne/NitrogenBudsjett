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
    """
    results = []
    
    # Hent ut den forhåndsinnleste rå-DataFramen fra datalasteren vår
    df_atm = preloaded_data.get('atm_in_out')
    
    # Hvis vi ikke har lastet data (f.eks. i en kjapp test), avbryter vi kontrollert
    if df_atm is None:
        print("[ADVARSEL] Data for 'atm_in_out' mangler i preloaded_data.")
        return results

    # 1. Kjør den første omskrevne funksjonen (vi definerer den under)
    _add_atmospheric_outflow_oxn_mc(results, df_atm, current_params, dataset_noise)
    _add_atmospheric_outflow_rdn_mc(results, df_atm, current_params, dataset_noise)
    
    # 2. Hent ferdigberegnet ammoniakkimport fra din egne fellesfunksjon.
    df_vol = preloaded_data.get('compressed_trade_volume')
    
    if df_vol is not None:
        # Genererer {år: verdi}-ordboken via fellesfunksjonen din
        ammonia_import_dict = process_generic_trade_flow(
            preloaded_data=preloaded_data,
            current_params=current_params,
            current_trade_factors=current_trade_factors,
            target_types='NH3',  
            is_import=True       
        )    
                
        # 7. Kjør fikseringsberegningen din som vanlig
        _add_OP_N2_fixation_mc(results, preloaded_data, current_params, ammonia_import_dict, dataset_noise)        
    else:
        print("[ADVARSEL] Mangler 'compressed_trade_volume' i preloaded_data. Hopper over ammoniakk-strømmer.")    
    
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

    # Definer de to unike dataset-nøklene som brukes i denne funksjonen
    key_dep = 'Deposition'
    key_interp = 'trend interpolation'
    
    # Sjekk om støydata finnes i denne rundens støy-ordbok
    has_noise_dep = dataset_noise and key_dep in dataset_noise
    has_noise_interp = dataset_noise and key_interp in dataset_noise

    # --- ALARM/VARSEL: Sjekk om nøklene mangler i Excel (Kjøres kun én gang per nøkkel) ---
    if dataset_noise and not hasattr(_deposition_flow_mc, "alarms_checked"):
        setattr(_deposition_flow_mc, "alarms_checked", True)
        if not has_noise_dep:
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{key_dep}' i dataset_uncertainties!")
        if not has_noise_interp:
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{key_interp}' i dataset_uncertainties!")
        if not has_noise_dep or not has_noise_interp:
            print(f"          Mangler blir kjørt deterministisk (støy = 0) inntil Excel oppdateres.")

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
                
            # Konverter tonn -> kt 
            base_value = float(tonn_val) / 1000
            data_sources = 'NILU and geodata.no'
            
            # --- STØYLOGIKK FOR 'Deposition' ---
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
            # Skalering basert på 2016-verdien (beholder opprinnelig støy herfra)
            if poll == 'NOx':
                value = value_2016 * 61440 / 68166
            else:
                value = value_2016 * 61175 / 73494
            value_last = value
            data_sources = 'NILU and geodata.no'
            
        else:
            # Siste år ekstrapoleres flatt videre fra value_last
            base_value = value_last
            data_sources = 'extrapolated'
            
            # --- STØYLOGIKK FOR 'trend interpolation' ---
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

        # Fysisk sperre: Deponering kan ikke bli negativ
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
    comment = 'ok (MC-støy lagt på basert på uncertainty_type)'
    
    dataset_key = 'Fertilizer by nutrient'
    data_sources = 'FAOSTAT Fertilizer by nutrient + SSB'
    
    # Hent ferdiglastet FAOSTAT-data
    df_faostat = preloaded_data.get('faostat_fertilizer')
    if df_faostat is None:
        print(f"[ADVARSEL] Mangler faostat_fertilizer i preloaded_data.")
        return

    # Sjekk om det finnes støydata for dette datasettet i denne runden
    has_noise = dataset_noise and dataset_key in dataset_noise

    # Én-gangs alarmbeskjed per kjøring dersom datasettet mangler usikkerhetsdefinisjon i Excel
    if dataset_noise and not has_noise and not hasattr(_add_OP_N2_fixation_mc, f"warned_{dataset_key}"):
        print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
        print(f"          Kjører deterministisk (støy = 0) for dette datasettet inntil Excel oppdateres.")
        setattr(_add_OP_N2_fixation_mc, f"warned_{dataset_key}", True)

    for _, row in df_faostat.iterrows():
        year = int(row['Year'])
        if year in ammonia_import_dict:  # Data finnes fra handelsstart (1988)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            
            # FAOSTAT-verdi gjøres om fra tonn til kt N
            base_faostat = float(row['Value']) / 1000 
            
            # --- STØYLOGIKK: Skiller strengt mellom 'perc' og 'abs' ---
            if has_noise:
                noise_info = dataset_noise[dataset_key]
                noise_val = noise_info['value']
                unc_type = noise_info['type']
                
                if unc_type == 'perc':
                    # Prosentvis usikkerhet: noise_val svinger rundt 1.0 (f.eks. 0.95 eller 1.03)
                    perturbed_faostat = base_faostat * noise_val
                else:
                    # Absolutt usikkerhet: noise_val svinger mellom -1.0 og +1.0.
                    # Skalerer avviket med riktig grense avhengig av fortegn.
                    if noise_val >= 0:
                        perturbed_faostat = base_faostat + (noise_val * noise_info['upp_bound'])
                    else:
                        perturbed_faostat = base_faostat + (noise_val * noise_info['low_bound'])
            else:
                # Fallback hvis deterministisk (i==0) eller ved manglende Excel-rad
                perturbed_faostat = base_faostat
            
            # Fysisk sperre: En gjødselmengde kan logisk sett ikke bli negativ av støy
            if perturbed_faostat < 0:
                perturbed_faostat = 0.0

            # Formel: (FAOSTAT med støy) - (Ammoniakkimport med støy)
            value = perturbed_faostat - ammonia_import_dict[year]
            
            # Dynamisk kommentar for sporbarhet
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
    
    # Henter rundens ferdigstøysatte verdi direkte fra parameter-ordboka
    value = float(current_params.get("AG_biological_fixation_N2", 0.0))
    uncertainty = 50.0  # Beholdes statisk som metadata i ordboka
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })


def _add_FO_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-FS.FO-N2 fixation-N2'
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'Moldan (2025) and SSB'
    
    # Fallback til 18.0 kt N hvis parameteren mot formodning skulle mangle
    value = float(current_params.get("FO_biological_fixation_N2", 18.0))
    uncertainty = 50.0
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })


def _add_OL_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-FS.OL-N2 fixation-N2'
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CORINE land cover inventory and REddy & DeLaune (2008)'
    
    value = float(current_params.get("OL_biological_fixation_N2", 0.0))
    uncertainty = 50.0
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })


def _add_SW_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-HY.SW-N2 fixation-N2'
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'NIBIO and Reddy & DeLaune (2008)'
    
    # Fallback til 2.0 kt N
    value = float(current_params.get("SW_biological_fixation_N2", 2.0))
    uncertainty = 50.0
    
    for year in EXPECTED_YEARS:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
        
        
def _add_atmospheric_outflow_oxn_mc(results, df_atm, current_params, dataset_noise):
    flow_code = 'AT.AT-RW.RW-Atmospheric outflow-OXN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på uncertainty_type)'
    
    # Vi looper over de samme radene (Excel 6-46 blir Pandas index 5-45)
    for r in range(5, 45):
        if r >= len(df_atm):
            break
            
        year_val = df_atm.iloc[r, 0]  # Kolonne 1 (A) -> Indeks 0
        if pd.isna(year_val):
            continue
            
        year = int(year_val)
        collected_years.add(year)
        
        # Sjekk status i Kolonne 6 (F) -> Indeks 5 for å velge riktig datasett-nøkkel
        status_val = str(df_atm.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            
        # Hent basisverdi fra Kolonne 3 (C) for OXN og gjør om fra 100 tN til ktN  
        base_value = float(df_atm.iloc[r, 2]) / 10  
        
        # --- STØYLOGIKK: Sjekk om nøkkelen finnes i denne rundens støy-ordbok ---
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        # Én-gangs alarmbeskjed per kjøring dersom datasettet mangler i Excel
        if dataset_noise and not has_noise and not hasattr(_add_atmospheric_outflow_oxn_mc, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            print(f"          Kjører deterministisk (støy = 0) for denne strømmen inntil Excel oppdateres.")
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
            
        # Fysisk sperre: Atmosfærisk utstrømning kan ikke bli negativ
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
    
    # Excel rad 6 til 46 blir i Pandas index 5 til 45:
    for r in range(5, 45): 
        if r >= len(df_atm):
            break
            
        year_val = df_atm.iloc[r, 0]  # Kolonne A (1) -> Indeks 0
        if pd.isna(year_val):
            continue
            
        year = int(year_val)
        collected_years.add(year)
        
        # Sjekk status i Kolonne 6 (F) -> Indeks 5 for å velge riktig datasett-nøkkel
        status_val = str(df_atm.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            
        # Hent basisverdi fra Kolonne E (5) -> Indeks 4 og gjør om fra 100 tN til ktN  
        base_value = float(df_atm.iloc[r, 4]) / 10  
        
        # --- STØYLOGIKK ---
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        if dataset_noise and not has_noise and not hasattr(_add_atmospheric_outflow_rdn_mc, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            print(f"          Kjører deterministisk (støy = 0) for denne strømmen inntil Excel oppdateres.")
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


# Example usage
if __name__ == "__main__":
    calculations = execute_calculations_mc()
    for calc in calculations:
        print(calc)

