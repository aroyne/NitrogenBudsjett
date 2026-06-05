#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 09:37:11 2026

@author: anja
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 09:30:00 2026

@author: anja
"""
import pandas as pd
import numpy as np

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
)

def execute_calculations_rw(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    MC-VERSJON: Beregner nitrogenflyt for rest-of-world (RW) uten fil-I/O i løkka.
    """
    results = []
    
    # 1. Hent ut den forhåndsinnleste rå-DataFramen fra datalasteren for 'rw_in_out' eller tilsvarende
    # (Justert navnet her så det matcher din datalaster-konvensjon fra at_mc)
    df_rw = preloaded_data.get('atm_in_out')
    
    if df_rw is None:
        print("[ADVARSEL] Data for 'atm_in_out' mangler i preloaded_data.")
        return results

    # 2. Kjør de omskrevne funksjonene med støyhåndtering
    _add_fuel_import(results, preloaded_data, current_params, current_trade_factors)
    _add_rw_outflow_oxn_mc(results, df_rw, current_params, dataset_noise)
    _add_rw_outflow_rdn_mc(results, df_rw, current_params, dataset_noise)
    
    return results


def _add_fuel_import(results, preloaded_data, current_params, current_trade_factors):
    """
    Optimalisert MC-versjon for brenselimport (ikke-transport).
    Henter pre-komprimerte tonnasjer, påfører aktivitetsstøy (SSB 08801) 
    og unike, perturberte nitrogenfaktorer (fra trade_parameters) per varetype (konv).
    """
    flow_code = 'RW.RW-EF.EC-Fuel import-Nmix'
    collected_years = set()
    comment = 'ok'
    data_sources = 'SSB tab 08801'
    
    # Hent den komprimerte volum-matrisen fra RAM (bygget i data_loader)
    df_vol = preloaded_data.get('compressed_trade_volume')
    
    if df_vol is not None and current_trade_factors is not None:
        # Hent simulert aktivitetsstøy for utenrikshandel for denne runden
        noise_trade = float(current_params.get('08801', current_params.get('13136', 1.0)))
        
        # 1. OPPRETT SIKRE KOLONNER FOR MATCHING (Små bokstaver, fjern mellomrom, tving strenger)
        df_vol['type_clean'] = df_vol['type'].astype(str).str.lower().str.strip()
        df_vol['impeks_str'] = df_vol['impeks'].astype(str).str.strip()
        
        # 2. FILTRER: Sjekker både mot tallet 1 og strengen '1' for sikkerhets skyld
        is_fuel = df_vol['type_clean'] == 'fuel'
        is_import = df_vol['impeks_str'].isin(['1', '1.0'])
        
        df_fuel = df_vol[is_fuel & is_import].copy()
        
        # --- FEILSØKINGS-PRINT (Slå på hvis tabellen fortsatt blir tom) ---
        print(f"[DEBUG] Rader i df_vol: {len(df_vol)}, Rader etter fuel/import-filter: {len(df_fuel)}")
        if len(df_fuel) == 0:
            print("[DEBUG] Unike typer funnet i df_vol:", df_vol['type_clean'].unique())
            print("[DEBUG] Unike impeks funnet i df_vol:", df_vol['impeks_str'].unique())
        
        if not df_fuel.empty:
            # 3. Map inn de unike, perturberte N-faktorene basert på 'konv'-kolonnen
            # Sørg for at nøklene i current_trade_factors også sjekkes uten whitespace hvis nødvendig
            df_fuel['konv_clean'] = df_fuel['konv'].astype(str).str.strip()
            
            # # --- FEILSØKINGSBLOKK: SE PÅ ORDBOKEN ---
            # print("\n" + "="*60)
            # print("[DEBUG] Unike koder i rådata (konv_clean):")
            # print(list(df_fuel['konv_clean'].unique()))
            # print("-"*60)
            # print("[DEBUG] Tilgjengelige koder i current_trade_factors (Excel):")
            # print(list(current_trade_factors.keys()))
            # print("="*60 + "\n")
            
            # # Framprovoser en kontrollert stopp så vi rekker å lese terminalen
            # raise RuntimeError("Kontrollert stopp for å lese koder")
            
            # # --- NY PRINT FOR Å SE PÅ RADENE ---
            # print("\n" + "="*60)
            # print("[DEBUG] Slik ser radene ut FØR mapping av N-faktorer:")
            # # Vi viser et utvalg av kolonner for å ikke fylle hele skjermen
            # print(df_fuel[['year', 'impeks', 'type', 'konv_clean', 'amount']].head(10).to_string())
            # print("="*60)
            
            v_factors = df_fuel['konv_clean'].map(current_trade_factors).fillna(0.0)
            
            # 4. Vektorisert beregning (kg * aktivitetsstøy * parameterstøy / 1e9 = kt N)
            df_fuel['N_amount'] = df_fuel['amount'] * noise_trade * v_factors / 1e9
            
            # 5. Aggreger alle ulike brenseltyper (konv) per år
            years = df_fuel['year'].values
            n_amounts = df_fuel['N_amount'].values
            
            fuel_import_dict = {}
            for idx in range(len(years)):
                try:
                    # int(float(...)) håndterer trygt både "2020", 2020.0 og 2020
                    yr = int(float(years[idx]))
                    fuel_import_dict[yr] = fuel_import_dict.get(yr, 0.0) + n_amounts[idx]
                except (ValueError, TypeError):
                    continue # Hopper over eventuelle korrupte årstall-rader
        else:
            fuel_import_dict = {}
            
        # 6. Pakk resultatene inn i det rene formatet utan usikkerhets-kolonne
        for year in EXPECTED_YEARS:
            if year in fuel_import_dict:
                collected_years.add(year)
                results.append({
                    'flow_name': flow_code,
                    'year': year,
                    'value': fuel_import_dict[year], 
                    'comment': comment,
                    'data_sources': data_sources
                })
                
        # Håndter manglende år
        missing_years = EXPECTED_YEARS - collected_years
        report_missing_years(flow_code, missing_years, results)
        
    else:
        print(f"[ADVARSEL] Mangler handelsdata eller faktorer i _add_fuel_import for {flow_code}.")    
        

def _add_rw_outflow_oxn_mc(results, df_rw, current_params, dataset_noise):
    flow_code = 'RW.RW-AT.AT-Atmospheric inflow-OXN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på uncertainty_type)'
    
    # Antar samme rad-oppsett (Excel rad 6-46 blir Pandas indeks 5-45) som df_atm
    for r in range(5, 45):
        if r >= len(df_rw):
            break
            
        year_val = df_rw.iloc[r, 0]  # Kolonne 1 (A) -> Indeks 0
        if pd.isna(year_val):
            continue
            
        year = int(year_val)
        collected_years.add(year)
        
        # Sjekk status i Kolonne 6 (F) -> Indeks 5 for å velge riktig datasett-nøkkel
        status_val = str(df_rw.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            
        # Hent basisverdi fra Kolonne 2 (B) -> indeks 1 for OXN og gjør om fra 100 tN til ktN  
        base_value = float(df_rw.iloc[r, 1]) / 10  
        
        # --- STØYLOGIKK ---
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        if dataset_noise and not has_noise and not hasattr(_add_rw_outflow_oxn_mc, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            print(f"          Kjører deterministisk (støy = 0) for denne strømmen inntil Excel oppdateres.")
            setattr(_add_rw_outflow_oxn_mc, f"warned_{dataset_key}", True)
            
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


def _add_rw_outflow_rdn_mc(results, df_rw, current_params, dataset_noise):
    flow_code = 'RW.RW-AT.AT-Atmospheric inflow-RDN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på uncertainty_type)'
    
    for r in range(5, 45): 
        if r >= len(df_rw):
            break
            
        year_val = df_rw.iloc[r, 0]  # Kolonne A -> Indeks 0
        if pd.isna(year_val):
            continue
            
        year = int(year_val)
        collected_years.add(year)
        
        status_val = str(df_rw.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            
        # Hent basisverdi fra Kolonne D (4) -> Indeks 3 og gjør om fra 100 tN til ktN  
        base_value = float(df_rw.iloc[r, 3]) / 10  
        
        # --- STØYLOGIKK ---
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        if dataset_noise and not has_noise and not hasattr(_add_rw_outflow_rdn_mc, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            print(f"          Kjører deterministisk (støy = 0) for denne strømmen inntil Excel oppdateres.")
            setattr(_add_rw_outflow_rdn_mc, f"warned_{dataset_key}", True)
            
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