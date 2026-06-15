#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:13:27 2026

@author: anja
"""
import pandas as pd
import numpy as np
import openpyxl

from calculations.n_params import NParameters
from calculations.utils import (
    EXPECTED_YEARS,
    combine_uncertainties_percent,
    get_uncertainty,
    find_trade_flow,
    find_trade_data,
    read_trade_data,
    read_year_value_row, 
    process_generic_trade_flow
)

params = NParameters("data_files/N_parameters.xlsx")
waste_fracs = params.get_table('waste_fractions').set_index('waste_category')
trade_data = read_trade_data('data_files/Tab_08801_1988_2024.csv')


def get_waste_frac(cat):
    row = waste_fracs.loc[cat]
    # N_frac is in kg N/kg, uncertainty is in %
    return float(row['N_frac']), float(row['uncertainty'])


import numpy as np
import pandas as pd

def find_ammonia_import(prepared_trade_data, current_params, trade_params):
    """Henter ammoniakkimport med kildestøy fra varehandelsstatistikk."""
    year_values = {}
    
    # Hent støy for utenrikshandel (f.eks. tabell 08801 eller tilsvarende fra listen din)
    noise_trade = float(current_params.get('08801', current_params.get('13136')))
    
    aggregated_data, _ = find_trade_flow(
        data_impeks=prepared_trade_data, 
        trade_params=trade_params, 
        dataset_unc=None, 
        wide=False
    )
    
    if not aggregated_data.empty:
        for index, row in aggregated_data.iterrows():
            year = int(row['year'])
            # Ganger inn støy for handelsstatistikk
            year_values[year] = float(row['N_amount']) * noise_trade
            
    return year_values


def find_aquaculture_production(df_aqua_modern, df_aqua_old, current_params, dataset_noise=None):
    """
    Henter akvakulturproduksjon fra Fiskeridirektoratet og konverterer til kt N.
    Påfører parameterstøy (fish_N_frac) og dataset-støy for Fiskeridirektoratet.
    """
    aquaculture_production = {}
    
    # 1. Hent den perturberte N-faktoren for fisk (parameterstøy)
    fish_N_frac = float(current_params.get('fish_N_frac'))
    
    # 2. Hent simulert aktivitetsstøy for Fiskeridirektoratet (dataset-støy)
    # Vi sjekker om den ligger i 'dataset_noise' først, med fallback til 'current_params'
    key_fisk = 'Fiskeridirektoratet'
    noise_aqua = 1.0
    
    if dataset_noise and key_fisk in dataset_noise:
        noise_info = dataset_noise[key_fisk]
        if noise_info['type'] == 'perc':
            noise_aqua = float(noise_info['value'])
        # Hvis det skulle være 'abs' støy, må det håndteres i løkka, 
        # men for aktivitetsdata fra Fiskeridirektoratet er det nesten alltid prosentvis (perc).
    else:
        # Fallback til din gamle logg dersom nøkkelen ble dyttet flatt inn i current_params
        noise_aqua = float(current_params.get('Fiskeridirekt', current_params.get('Fiskeridirektoratet')))

    # --- DEL 1: Moderne data (fra 1994 og utover) ---
    for col in df_aqua_modern.columns:
        try:
            year = int(col)
            col_data = pd.to_numeric(df_aqua_modern[col], errors='coerce').fillna(0)
            value_tonn = col_data.sum()
            
            # Formel: (Tonn / 1000 -> kt rundvekt) * N-fraksjon * aktivitetsstøy = kt N
            val_kt_N = (value_tonn / 1000) * fish_N_frac * noise_aqua
            
            if val_kt_N < 0:
                val_kt_N = 0.0
            aquaculture_production[year] = val_kt_N
            
        except ValueError:
            continue

    # --- DEL 2: Gamle data (før 1994) ---
    for _, row in df_aqua_old.iterrows():
        try:
            year = int(float(row.iloc[0]))
            value_base = float(row.iloc[1])
            
            # Formel: kt rundvekt * N-fraksjon * aktivitetsstøy = kt N
            val_kt_N = value_base * fish_N_frac * noise_aqua
            
            if val_kt_N < 0:
                val_kt_N = 0.0
            aquaculture_production[year] = val_kt_N
            
        except (ValueError, TypeError):
            continue

    return aquaculture_production


def find_export_for_recycling(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    """
    MC-VERSJON: Eksport til resirkulering (PR.SO-RW.RW-Export for recycling-Nmix).
    Gjenbruker den generiske handelsløsningen for materiale sendt til gjenvinning ut av landet.
    """
    year_values = process_generic_trade_flow(
        preloaded_data=preloaded_data, 
        current_params=current_params,
        current_trade_factors=current_trade_factors, 
        flow_code='PR.SO-RW.RW-Export for recycling-Nmix',
        target_types=['plastavfall', 'papiravfall', 'tekstilavfall'],
        is_import=False,  # Eksport
        dataset_noise=dataset_noise,
        results=results, 
    )
    
    return year_values


def find_export_for_reuse(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    """
    MC-VERSJON: Eksport til gjenbruk (PR.SO-RW.RW-Export for reuse-Nmix).
    Gjenbruker den generiske handelsløsningen for brukte produkter (f.eks. tekstiler) ut av landet.
    """
    year_values = process_generic_trade_flow(
        preloaded_data=preloaded_data, 
        current_params=current_params,
        current_trade_factors=current_trade_factors, 
        flow_code='PR.SO-RW.RW-Export for reuse-Nmix',
        target_types=['tekstil_brukt'],
        is_import=False,  # Eksport
        dataset_noise=dataset_noise,
        results=results, 
    )
    
    return year_values

def find_feedstock_fuel(preloaded_data, current_params, dataset_noise):
    """
    Beregner nitrogen i råstoff med kildestøy fra energibalansen (11561).
    Henter data fra preloaded_data i stedet for å lese filen for hver iterasjon.
    """
    year_values = {}
    
    # Hent støy for energibalansen (Tabell 11561) 
    noise_energy = float(dataset_noise['11561']['value'])
    
    # Hent parametere trygt fra current_params (støtter både dict og NParameters)
    GWh_to_TJ_factor = float(current_params.get('GWh_to_TJ_factor'))
    coal_NCV         = float(current_params.get('coal_feedstock_NCV'))
    oil_NCV          = float(current_params.get('oil_feedstock_NCV'))
    coal_N_frac      = float(current_params.get('coal_feedstock_N_frac'))
    oil_N_frac       = float(current_params.get('oil_feedstock_N_frac'))

    # Hent datarammen som ble preloaded i main_mc.py
    df_energy = preloaded_data.get('ssb_energy_balance_11561')
    
    if df_energy is None:
        print("  [ADVARSEL] ssb_energy_balance_11561 mangler i preloaded_data!")
        return year_values, 0.0

    # --- KULL OG KULLPRODUKTER ---
    # Justert range: Siden openpyxl (1-indeksert) brukte rad 39-73, 
    # tilsvarer dette indeks 38-72 i en rå data_only Pandas DataFrame.
    for row_idx in range(38, 73):
        try:
            if row_idx >= len(df_energy): 
                break
            row_data = df_energy.iloc[row_idx]
            year_val = row_data.iloc[2]   # Kolonne C
            value_val = row_data.iloc[3]  # Kolonne D
            
            if pd.notna(year_val) and pd.notna(value_val) and value_val != '-':
                year = int(year_val)
                value = float(value_val) / (GWh_to_TJ_factor * coal_NCV) * coal_N_frac
                year_values[year] = year_values.get(year, 0.0) + (value * noise_energy)
        except (ValueError, TypeError) as e:
            # Hvis år eller verdi ikke kan konverteres til tall (f.eks pga tekst på feil rad)
            print(f"  [Beregning-info] Hoppet over kull-rad {row_idx + 1} i Excel: Inneholder ikke gyldige talldata.")
            continue
        except Exception as e:
            print(f"  [Uventet feil] Kull-rad {row_idx}: {e}")
            continue

    # --- OLJE OG OLJEPRODUKTER ---
    # Justert range til 108-142 for å matche openpyxl 109-143
    for row_idx in range(108, 143):
        try:
            if row_idx >= len(df_energy): 
                break
            row_data = df_energy.iloc[row_idx]
            year_val = row_data.iloc[2]   # Kolonne C
            value_val = row_data.iloc[3]  # Kolonne D
            
            if pd.notna(year_val) and pd.notna(value_val) and value_val != '-':
                year = int(year_val)
                value = float(value_val) / (GWh_to_TJ_factor * oil_NCV) * oil_N_frac
                year_values[year] = year_values.get(year, 0.0) + (value * noise_energy)
        except (ValueError, TypeError):
            print(f"  [Beregning-info] Hoppet over olje-rad {row_idx + 1} i Excel: Inneholder ikke gyldige talldata.")
            continue
        except Exception as e:
            print(f"  [Uventet feil] Olje-rad {row_idx}: {e}")
            continue

    # Returnerer ALLTID en tuppel med to verdier, slik at utpakkingen (expected 2, got 0) aldri feiler
    return year_values, 0.0

def find_food_industry_waste(df_05282, df_10514, current_params, dataset_noise):
    """
    Beregner nitrogen i matindustriavfall basert på ferdiginnleste tabeller fra Pandas.
    Indeksene matcher nøyaktig openpyxl-strukturen (row/col skiftet med -1).
    """
    year_values = {}
    wet_org_N = float(current_params.get('wet_organic'))
    
    # Hent støy fra dataset_noise
    required_noise_keys = ['05282', '10514', 'trend interpolation']
    if not dataset_noise or any(k not in dataset_noise for k in required_noise_keys):
        missing = [k for k in required_noise_keys if not dataset_noise or k not in dataset_noise]
        raise KeyError(f"[KRITISK] Støy-nøkler mangler i dataset_noise for matindustriavfall: {missing}")
        
    noise_05282 = float(dataset_noise['05282']['value'])
    noise_10514 = float(dataset_noise['10514']['value'])
    noise_trend = float(dataset_noise['trend interpolation']['value'])
    
    value_2012_base = 0.0

    # --- DEL 1: Årene 2012-2023 (Tabell 10514) ---
    # I openpyxl: range(2, 115, 10). I Pandas endrer vi til kolonneindekser (col - 1)
    for col in range(2, 115, 10):  
        try:
            p_col = col - 1  # Konverter til Pandas 0-basert kolonneindeks
            year_val = df_10514.iloc[3, p_col]  # row 4 -> indeks 3
            if pd.isna(year_val):
                continue
            year = int(float(year_val))
            
            # row 7 -> indeks 6
            v_base = 0.0
            v_base += float(df_10514.iloc[6, p_col+1]) * wet_org_N
            v_base += float(df_10514.iloc[6, p_col+3]) * wet_org_N
            v_base += float(df_10514.iloc[6, p_col+8]) * wet_org_N
            
            if year == 2012:
                value_2012_base = v_base
                
            year_values[year] = {
                'value': max(0.0, v_base * noise_10514),
                'comment': 'ok (SSB Tabell 10514)',
                'data_sources': 'SSB'
            }
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil i ssb_10514 kolonne {col}: {e}")

    if value_2012_base == 0.0:
        raise ValueError("[KRITISK] Fant ikke basisverdi for år 2012 i Tabell 10514. Skalering umulig!")

    # --- DEL 2: Årene 1995-2011 (Tabell 05282) ---
    # Finner 2011-verdi for skalering (openpyxl col=162, row=14 -> Pandas col=161, row=13)
    try:
        p_col_2011 = 162 - 1
        value_2011_base = float(df_05282.iloc[13, p_col_2011+1]) * wet_org_N
        value_2011_base += float(df_05282.iloc[13, p_col_2011+3]) * wet_org_N
        value_2011_base += float(df_05282.iloc[13, p_col_2011+8]) * wet_org_N
    except Exception as e:
        raise ValueError(f"[KRITISK] Kunne ikke beregne 2011-skaleringsfaktor fra df_05282: {e}")

    if value_2011_base == 0.0:
        value_2011_base = 1.0

    mean_val_accumulator = 0.0
    mean_year_count = 0

    # I openpyxl: range(2, 170, 10)
    for col in range(2, 170, 10):  
        try:
            p_col = col - 1
            year_val = df_05282.iloc[3, p_col]  # row 4 -> indeks 3
            if pd.isna(year_val):
                continue
            year = int(float(year_val))
            
            # row 14 -> indeks 13
            v_base = 0.0
            v_base += float(df_05282.iloc[13, p_col+1]) * wet_org_N
            v_base += float(df_05282.iloc[13, p_col+3]) * wet_org_N
            v_base += float(df_05282.iloc[13, p_col+8]) * wet_org_N
            
            # Skaler verdien bakover i tid
            v_scaled = v_base * (value_2012_base / value_2011_base)
            
            if 1995 <= year < 2000:
                mean_val_accumulator += v_scaled
                mean_year_count += 1
                
            year_values[year] = {
                'value': max(0.0, v_scaled * noise_05282),
                'comment': 'ok (Skalert SSB Tabell 05282)',
                'data_sources': 'SSB'
            }
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil i ssb_05282 kolonne {col}: {e}")

    # --- DEL 3: Ekstrapolering for årene 1990-1994 ---
    final_mean = (mean_val_accumulator / mean_year_count) if mean_year_count > 0 else 0.0
    for year in range(1990, 1995):
        year_values[year] = {
            'value': max(0.0, final_mean * noise_05282 * noise_trend),
            'comment': 'extrapolated (added trend interpolation noise)',
            'data_sources': 'extrapolated'
        }
        
    return year_values


def find_household_waste(preloaded_data, current_params, dataset_noise):
    """
    Beregner nitrogenmengder i husholdningsavfall og tilhørende næringer (generert).
    Sikret mot IndexError uten bruk av lydløse fallbacks.
    """
    household_waste = {y: 0.0 for y in range(1990, 2024)}
    
    # Hent støyfaktorer for simuleringen
    noise_05282 = float(dataset_noise['05282']['value'])
    noise_10514 = float(dataset_noise['10514']['value'])
    noise_interp = float(dataset_noise['trend interpolation']['value'])

    # Hent N-fraksjoner via current_params
    paper_N   = float(current_params.waste_N_frac('paper'))
    plastic_N = float(current_params.waste_N_frac('plastic'))
    wood_N    = float(current_params.waste_N_frac('wood'))
    textile_N = float(current_params.waste_N_frac('textiles'))
    wet_N     = float(current_params.waste_N_frac('wet_organic'))
    other_N   = float(current_params.waste_N_frac('other_materials'))
    haz_N     = float(current_params.waste_N_frac('hazardous'))
    contam_N  = float(current_params.waste_N_frac('contaminated_masses'))
    park_N    = float(current_params.waste_N_frac('park_garden'))
    mixed_N   = float(current_params.waste_N_frac('mixed_waste'))

    # =========================================================================
    # TABELL 05281 / 05282 (1995-2011)
    # =========================================================================
    df_05282 = preloaded_data['ssb_waste_05281']
    value_1995 = 0.0
    width_05282 = df_05282.shape[1]

    col_to_year = {}
    for col_idx in range(3, width_05282):
        val = str(df_05282.iloc[2, col_idx]).strip()
        if val.replace('.0', '').isdigit():
            y = int(float(val))
            if 1995 <= y <= 2011:
                col_to_year[col_idx] = y

    for col_idx, year in col_to_year.items():
        val_year = 0.0
        
        # Papir (Excel rad 7 -> indeks 6)
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_05282: val_year += float(df_05282.iloc[6, col_idx + c]) * paper_N
        # Plast (Excel rad 9 -> indeks 8)
        for c in [5, 6, 9]:
            if col_idx + c < width_05282: val_year += float(df_05282.iloc[8, col_idx + c]) * plastic_N
        # Treavfall (Excel rad 12 -> indeks 11)
        for c in [5, 6, 9]:
            if col_idx + c < width_05282: val_year += float(df_05282.iloc[11, col_idx + c]) * wood_N
        # Tekstiler (Excel rad 13 -> indeks 12)
        for c in [5, 6, 9]:
            if col_idx + c < width_05282: val_year += float(df_05282.iloc[12, col_idx + c]) * textile_N
        # Våtorganisk (Excel rad 14 -> indeks 13)
        for c in [5, 6, 9]:
            if col_idx + c < width_05282: val_year += float(df_05282.iloc[13, col_idx + c]) * wet_N
        # Andre (Excel rad 17 -> indeks 16)
        for c in [5, 6, 9]:
            if col_idx + c < width_05282: val_year += float(df_05282.iloc[16, col_idx + c]) * other_N
        # Farlig (Excel rad 18 -> indeks 17)
        for c in [5, 6, 9]:
            if col_idx + c < width_05282: val_year += float(df_05282.iloc[17, col_idx + c]) * haz_N
        # Forurenset (Excel rad 19 -> indeks 18)
        for c in [5, 6, 9]:
            if col_idx + c < width_05282: val_year += float(df_05282.iloc[18, col_idx + c]) * contam_N

        household_waste[year] = val_year * noise_05282
        if year == 1995:
            value_1995 = household_waste[year]

    # =========================================================================
    # TABELL 10513 / 10514 (2012-2023)
    # =========================================================================
    df_10514 = preloaded_data['ssb_waste_10513']
    width_10514 = df_10514.shape[1]
    
    col_to_year_10514 = {}
    for col_idx in range(1, width_10514):
        val = str(df_10514.iloc[2, col_idx]).strip()
        if val.replace('.0', '').isdigit():
            y = int(float(val))
            if 2012 <= y <= 2023:
                col_to_year_10514[col_idx] = y

    for col_idx, year in col_to_year_10514.items():
        val_year = 0.0
        
        # Sjekker grensene for alle sub-kolonner (c) før iloc kalles
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[6, col_idx + c]) * wet_N
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[7, col_idx + c]) * park_N
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[8, col_idx + c]) * wood_N
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[10, col_idx + c]) * paper_N
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[16, col_idx + c]) * plastic_N
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[18, col_idx + c]) * textile_N
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[21, col_idx + c]) * haz_N
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[22, col_idx + c]) * mixed_N
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[23, col_idx + c]) * other_N
        for c in [4, 5, 6, 7, 9]:
            if col_idx + c < width_10514: val_year += float(df_10514.iloc[24, col_idx + c]) * contam_N

        household_waste[year] = val_year * noise_10514

    # =========================================================================
    # EKSTRAPOLERING 1990-1994
    # =========================================================================
    inhabitants_1990 = 4233116
    inhabitants_1995 = 4348410
    waste_kg_person_1990 = 200
    waste_kg_person_1995 = 289
    
    waste_kt_1990 = waste_kg_person_1990 * inhabitants_1990 * 1e-6
    waste_kt_1995 = waste_kg_person_1995 * inhabitants_1995 * 1e-6
    
    N_frac = value_1995 / waste_kt_1995
    value_1990 = waste_kt_1990 * N_frac
    change_per_year = (value_1995 - value_1990) / 5.0
    
    for idx, year in enumerate(range(1990, 1995)):
        household_waste[year] = (value_1990 + change_per_year * idx) * noise_interp

    return household_waste


def find_other_industry_waste(df_05282, df_10514, df_hist_waste, current_params, dataset_noise):
    """
    MC-OPTIMALISERT: Beregner nitrogen i øvrig industriavfall ved hjelp av NumPy.
    Ingen tause try-excepts. Krasjer hardt ved string/NaN-feil i SSB-tabellene.
    """
    industry_waste = {}
    industry_waste_unc = {}
    
    # 1. Hent nitrogen-fraksjoner fra parameter-objektet ditt
    paper_N     = float(current_params.waste_N_frac('paper'))
    plastic_N   = float(current_params.waste_N_frac('plastic'))
    wood_N      = float(current_params.waste_N_frac('wood'))
    textiles_N  = float(current_params.waste_N_frac('textiles'))
    wet_org_N   = float(current_params.waste_N_frac('wet_organic'))
    other_mat_N = float(current_params.waste_N_frac('other_materials'))
    hazardous_N = float(current_params.waste_N_frac('hazardous'))
    mixed_N     = float(current_params.waste_N_frac('mixed_waste'))
    
    # 2. Hent støyfaktorer og metadata-usikkerheter strikt uten fallbacks
    try:
        noise_05282 = float(dataset_noise['05282']['value'] if '05282' in dataset_noise else dataset_noise['ssb_waste_05282']['value'])
        noise_10514 = float(dataset_noise['10514']['value'] if '10514' in dataset_noise else dataset_noise['ssb_waste_10514']['value'])
        noise_trend = float(dataset_noise['trend interpolation']['value'] if 'trend interpolation' in dataset_noise else dataset_noise['trend_interpolation']['value'])
        
        u_05282  = dataset_noise['05282']['low_bound'] if '05282' in dataset_noise else dataset_noise['ssb_waste_05282']['low_bound']
        u_10514  = dataset_noise['10514']['low_bound'] if '10514' in dataset_noise else dataset_noise['ssb_waste_10514']['low_bound']
        u_trend  = dataset_noise['trend interpolation']['low_bound'] if 'trend interpolation' in dataset_noise else dataset_noise['trend_interpolation']['low_bound']
    except KeyError as e:
        raise KeyError(f"[KRITISK] Mangler støy-/usikkerhetsnøkkel '{e.args[0]}' i dataset_noise for industriavfall!")

    # Konverter til NumPy for hastighet
    arr_05282 = df_05282.values
    arr_10514 = df_10514.values
    
    # Vi må lagre en RÅ base_value for 1995 (uten støy) til ekstrapoleringen
    base_value_1995 = 0.0

    # --- DEL 1: ÅRENE 1995-2011 (Tabell 05282) ---
    for col in range(1, 169, 10):
        try:
            year = int(arr_05282[3, col])
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK] Klarte ikke lese årstall fra tabell 05282 i kolonne {col}: {e}")
            
        value_base = 0.0
        try:
            # Papir (Rad 7 -> indeks 6)
            for c in [2, 3, 8]: value_base += float(arr_05282[6, col + c]) * paper_N
            # Plast (Rad 9 -> indeks 8)
            for c in [2, 3, 8]: value_base += float(arr_05282[8, col + c]) * plastic_N
            # Treavfall (Rad 12 -> indeks 11)
            for c in [2, 3, 8]: value_base += float(arr_05282[11, col + c]) * wood_N
            # Tekstiler (Rad 13 -> indeks 12)
            for c in [2, 3, 8]: value_base += float(arr_05282[12, col + c]) * textiles_N
            # Våtorganisk (Rad 14 -> indeks 13) - Bare fra bergverk (c=2)
            for c in [2]:       value_base += float(arr_05282[13, col + c]) * wet_org_N
            # Andre materialer (Rad 17 -> indeks 16)
            for c in [2, 3, 8]: value_base += float(arr_05282[16, col + c]) * other_mat_N
            # Farlig avfall (Rad 18 -> indeks 17)
            for c in [2, 3, 8]: value_base += float(arr_05282[17, col + c]) * hazardous_N
        except (ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Fant uventet tekst/NaN i tabell 05282 under kolonne {col} for år {year}: {e}")

        if year == 1995:
            base_value_1995 = value_base
            
        industry_waste[year] = value_base * noise_05282
        industry_waste_unc[year] = u_05282

    # --- DEL 2: ÅRENE 2012-2023 (Tabell 10514) ---
    for col in range(1, 114, 10):
        try:
            year = int(arr_10514[3, col])
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK] Klarte ikke lese årstall fra tabell 10514 i kolonne {col}: {e}")
            
        value_base = 0.0
        try:
            # Våtorganisk (Rad 7 -> indeks 6)
            for c in [2]:       value_base += float(arr_10514[6, col + c]) * wet_org_N
            # Treavfall (Rad 9 -> indeks 8)
            for c in [2, 3, 8]: value_base += float(arr_10514[8, col + c]) * wood_N
            # Papir (Rad 11 -> indeks 10)
            for c in [2, 3, 8]: value_base += float(arr_10514[10, col + c]) * paper_N
            # Plast (Rad 17 -> indeks 16)
            for c in [2, 3, 8]: value_base += float(arr_10514[16, col + c]) * plastic_N
            # Tekstiler (Rad 19 -> indeks 18)
            for c in [2, 3, 8]: value_base += float(arr_10514[18, col + c]) * textiles_N
            # Andre materialer (Rad 24 -> indeks 23)
            for c in [2, 3, 8]: value_base += float(arr_10514[23, col + c]) * other_mat_N
            # Farlig avfall (Rad 22 -> indeks 21)
            for c in [2, 3, 8]: value_base += float(arr_10514[21, col + c]) * hazardous_N
            # Blandet avfall (Rad 23 -> indeks 22)
            for c in [2, 3, 8]: value_base += float(arr_10514[22, col + c]) * mixed_N
        except (ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Fant uventet tekst/NaN i tabell 10514 under kolonne {col} for år {year}: {e}")

        industry_waste[year] = value_base * noise_10514
        industry_waste_unc[year] = u_10514

    # --- DEL 3: LINEÆR EKSTRAPOLERING TILBAKE TIL 1990 ---
    try:
        # ENDRET: Rad 0 er 'næringsavfall'-headeren. Vi bruker rad 1 og 2!
        waste_kt_1992 = float(df_hist_waste.iloc[1, 2])
        waste_kt_1995 = float(df_hist_waste.iloc[2, 2])
    except IndexError:
        raise IndexError("[KRITISK] df_hist_waste har ikke nok rader/kolonner for indeks [1,2] eller [2,2]!")
    except (ValueError, TypeError):
        raise ValueError("[KRITISK] Historiske avfallsdata (df_hist_waste) inneholder ugyldige verdier (ikke-tall)!")

    if waste_kt_1995 <= 0 or base_value_1995 <= 0:
        raise ValueError(f"[KRITISK] Kan ikke ekstrapolere industriavfall! Sjekk rådata for 1995 (base_1995={base_value_1995}, hist_1995={waste_kt_1995})")

    # Beregner basert på RÅDATA uten støy for å unngå dobbel støy-forvridning
    N_frac = base_value_1995 / waste_kt_1995
    base_value_1992 = waste_kt_1992 * N_frac
    change_per_year = (base_value_1995 - base_value_1992) / 3
    
    step = 0
    for year in range(1990, 1995):
        base_value_extrapolated = base_value_1992 + (change_per_year * step)
        step += 1
        # Påfører støy lineært KUN én gang på slutten
        industry_waste[year] = base_value_extrapolated * noise_05282 * noise_trend
        industry_waste_unc[year] = u_trend

    # ENDRET: Returnerer nå både verdi-ordboken og usikkerhets-ordboken
    return industry_waste, industry_waste_unc


def find_industrial_crop_products(df_gnb_sheet30, dataset_noise):
    """
    Henter ut industrielle avlinger basert på pre-loadet DataFrame.
    Påfører sentralt trukket datasett- og ekstrapoleringsstøy matematisk korrekt (perc vs abs).
    """
    year_values = {}
    
    # --- 1. Sjekk og klargjør støy for Gross nutrient balance ---
    key_gnb = 'Gross nutrient balance'
    has_noise_gnb = dataset_noise and key_gnb in dataset_noise
    noise_gnb_val = dataset_noise[key_gnb]['value'] if has_noise_gnb else 1.0
    noise_gnb_type = dataset_noise[key_gnb]['type'] if has_noise_gnb else 'perc'
    
    # --- 2. Sjekk og klargjør støy for trendinterpolering ---
    key_interp = 'trend interpolation'
    has_noise_interp = dataset_noise and key_interp in dataset_noise
    noise_interp_val = dataset_noise[key_interp]['value'] if has_noise_interp else 1.0
    noise_interp_type = dataset_noise[key_interp]['type'] if has_noise_interp else 'perc'
    
    # Hent radene direkte basert på posisjon (rad 9 og rad 11 i Excel)
    year_row = df_gnb_sheet30.iloc[8]
    value_row = df_gnb_sheet30.iloc[10]
    
    # --- 3. Les og påfør støy på ordinære år ---
    for col_idx in range(1, len(df_gnb_sheet30.columns)):
        year_val = year_row.iloc[col_idx]
        val_val = value_row.iloc[col_idx]
        
        if pd.notna(year_val) and pd.notna(val_val) and val_val != '-':
            try:
                year = int(year_val)
                base_value = float(val_val) * 1.0e-3  # kg -> kt
                
                if has_noise_gnb:
                    if noise_gnb_type == 'perc':
                        value = base_value * noise_gnb_val
                    else:
                        bound = dataset_noise[key_gnb]['upp_bound'] if noise_gnb_val >= 0 else dataset_noise[key_gnb]['low_bound']
                        value = base_value + (noise_gnb_val * bound)
                else:
                    value = base_value
                
                if value < 0:
                    value = 0.0
                    
                year_values[year] = value
            except ValueError:
                continue

    # --- 4. Ekstrapolering for hull i tidsserien (2017-2019) ---
    if year_values:
        mean_value = float(np.mean(list(year_values.values())))
        
        for year in range(2017, 2020):
            if has_noise_interp:
                if noise_interp_type == 'perc':
                    value_interp = mean_value * noise_interp_val
                else:
                    bound = dataset_noise[key_interp]['upp_bound'] if noise_interp_val >= 0 else dataset_noise[key_interp]['low_bound']
                    value_interp = mean_value + (noise_interp_val * bound)
            else:
                value_interp = mean_value
                
            if value_interp < 0:
                value_interp = 0.0
                
            year_values[year] = value_interp
            
    return year_values

def find_industrial_round_wood(preloaded_data, current_params, dataset_noise):
    """
    Beregner industrirundvirke ved å bruke pre-loadet FAOSTAT-data fra RAM,
    og ferdigstøysatte parametere/kildestøy fra NParameters-objektet.
    """
    year_values = {}
    
    # 1. Hent modellparametere og kildestøy fra current_params (NParameters)
    noise_faostat = dataset_noise['Forestry production and trade']['value']
    wood_density  = float(current_params.get('wood_density'))
    conifer_N     = float(current_params.get('conifer_N_frac'))
    nonconifer_N   = float(current_params.get('nonconifer_N_frac'))
    
    # 2. Hent rådata fra preloaded_data (eller fall tilbake til CSV hvis ikke preloaded)
    # Merk: Sjekk om 'fs_unfccc_emissions_raw' eller lignende i loggen din er denne filen. 
    # Hvis rammeverket laster den som 'faostat_forestry', bruker vi det, eller leser direkte:
    data = preloaded_data.get('faostat_forestry')
    if data is None:
        data = pd.read_csv('data_files/FAOSTAT_data_en_2-20-2026.csv')
    
    # 3. Filtrer og prosesser dataene på samme måte som før
    filtered_data = data[(data['Element'] == 'Production') & (data['Value'] != 0)].copy()
    
    items_conifer = ['Industrial roundwood, coniferous']
    items_nonconifer = ['Industrial roundwood, non-coniferous']
    
    final_data = filtered_data[filtered_data['Item'].isin(items_conifer + items_nonconifer)].copy()
    
    # Beregn tonn basert på iterasjonens wood_density
    final_data['tonnes'] = final_data['Value'] * wood_density
    
    # Legg på N-fraksjoner
    mask_conifer = final_data['Item'].isin(items_conifer)
    mask_nonconifer = final_data['Item'].isin(items_nonconifer)
    
    final_data['N_kg_per_kg'] = 0.0
    final_data.loc[mask_conifer, 'N_kg_per_kg'] = conifer_N
    final_data.loc[mask_nonconifer, 'N_kg_per_kg'] = nonconifer_N
    
    # Tonn * kg N/tonn / 1e3 -> kt N
    final_data['N_amount'] = final_data['tonnes'] * final_data['N_kg_per_kg'] / 1e3
    
    # Summer per år
    total_N_per_year = final_data.groupby('Year')['N_amount'].sum().to_dict()
    
    # 4. Fyll year_values og legg på kildestøyen (noise_faostat)
    for year in EXPECTED_YEARS:
        value = total_N_per_year.get(year, 0.0)
        if value > 0:
            # Ganger med kildestøyen (Forestry proc) som har blitt generert for denne iterasjonen
            year_values[year] = value * noise_faostat
            
    return year_values, None

def find_industrial_waste_fuels(df_bio_08205, df_bio_hist, current_params, dataset_noise):
    """
    MC-OPTIMALISERT: Beregner egentilvirket bioenergi med datasettstøy og ekstrapoleringsstøy.
    Ingen usikkerhetsberegning. Krasjer hardt og umiddelbart ved ugyldige datatyper eller manglende støyfaktorer.
    """
    year_values = {}
    
    # 1. Hent støyfaktorer strikt fra dataset_noise
    try:
        noise_08205 = float(dataset_noise['08205']['value'] if '08205' in dataset_noise else dataset_noise['ssb_waste_08205']['value'])
        noise_trend = float(dataset_noise['trend interpolation']['value'] if 'trend interpolation' in dataset_noise else dataset_noise['trend_interpolation']['value'])
    except KeyError as e:
        raise KeyError(f"[KRITISK] Mangler støy-nøkkel '{e.args[0]}' i dataset_noise for bioenergi!")

    # 2. Hent globale parametere som rene floats
    NCV              = float(current_params.get('firewood_NCV'))
    N_content        = float(current_params.get('firewood_N_frac'))
    GWh_to_TJ_factor = float(current_params.get('GWh_to_TJ_factor'))    
    
    # Konverter til rå NumPy-matriser for loop-hastighet
    arr_08205 = df_bio_08205.values
    arr_hist = df_bio_hist.values
    
    # Vi samler RÅ verdier (uten støy) for årene under 2008 for å beregne et rent historisk snitt
    raw_sum_pre_2008 = 0.0
    
    # --- DEL 1: SSB Tabell 08205 (Nyere data) ---
    # Excel Rad 3 -> NumPy indeks 2 (Årstall). Excel Rad 10 -> NumPy indeks 9 (Verdier)
    
    for col in range(3, 25):
        try:
            year_val = arr_08205[2, col]
            value_val = arr_08205[9, col]
        except IndexError:
            raise IndexError(f"[KRITISK] Tabell 08205 har ikke kolonne-indeks {col} på rad 2 eller 9!")
            
        if pd.isna(year_val) or pd.isna(value_val):
            raise ValueError(f"[KRITISK DATAFEIL] Fant NaN-verdi i tabell 08205 ved kolonne-indeks {col}!")
            
        try:
            year = int(year_val)
            # Konvertering: GWh til TJ, del på NCV til kt brensel, gang med N_content til ktN
            value_raw = float(value_val) / GWh_to_TJ_factor / NCV * N_content
        except (ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Klarte ikke konvertere verdier i tabell 08205 ved kolonne {col}: {e}")
            
        # Lagre støybelagt verdi i resultat-ordboken
        year_values[year] = value_raw * noise_08205
        
        # Akkumuler RÅ verdi til gjennomsnittet hvis året er før 2008
        if year < 2008:
            raw_sum_pre_2008 += value_raw

    # --- DEL 2: Historiske data 1998-2002 (df_bio_hist) ---
    # Excel Rad 2..6 blir NumPy radindeks 1..5. Kolonne 1->0, 2->1, 3->2
    for r in range(1, 6):
        try:
            year_val = arr_hist[r, 0]
            val_col2 = arr_hist[r, 1]
            val_col3 = arr_hist[r, 2]
        except IndexError:
            raise IndexError(f"[KRITISK] Historisk biotabell har ikke radindeks {r}!")
            
        if pd.isna(year_val) or pd.isna(val_col2) or pd.isna(val_col3):
            raise ValueError(f"[KRITISK DATAFEIL] Fant NaN-verdi i historisk biotabell på radindeks {r}!")
            
        try:
            year = int(year_val)
            value_raw = (float(val_col2) + float(val_col3)) / GWh_to_TJ_factor / NCV * N_content
        except (ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Klarte ikke konvertere verdier i historisk biotabell på rad {r}: {e}")
            
        year_values[year] = value_raw * noise_08205
        
        if year < 2008:
            raw_sum_pre_2008 += value_raw

    # --- DEL 3: Gjennomsnitt for årene 1990-1997 (Ekstrapolering) ---
    if raw_sum_pre_2008 <= 0:
        raise ValueError("[KRITISK] Grunnlag for ekstrapolering av bioenergi er 0 eller negativt! Sjekk rådata.")
        
    # Beregn reelt gjennomsnitt av rådata (10 år totalt: 5 år fra 08205 + 5 år fra hist)
    mean_value_raw = raw_sum_pre_2008 / 10.0
    
    for year in range(1990, 1998):
        # Påfør ekstrapoleringsstøy på det rå gjennomsnittet
        year_values[year] = mean_value_raw * noise_trend

    return year_values



def find_landfill_emissions_to_water(df_uts, df_tilk, current_params):
    """
    Beregner deponiutslipp til vann fordelt på tilkoblet og ikke-tilkoblet kommunalt avløp.
    Bruker kildestøy fra 'norskeutslipp' og trendstøy for interpolerte år (2009-2010).
    """
    # 1. Hent støyfaktorer fra denne MC-runden
    # NÅ OPPDATERT: Bruker 'norskeutslipp' som primærnøkkel!
    noise_deponi = float(current_params.get('norskeutslipp'))
    noise_trend  = float(current_params.get('trend interpolation'))
    
    # Usikkerhet i tilkobling: For "ukjent" trekker vi en tilfeldig vekt mellom 0 og 1 for denne runden
    ukjent_vekt_tilkoblet = float(np.random.uniform(0.0, 1.0))
    ukjent_vekt_ikke = 1.0 - ukjent_vekt_tilkoblet

    # 2. Gjør anleggsnavn likt skrevet (strip og lower)
    df_uts = df_uts.copy()
    df_tilk = df_tilk.copy()
    
    df_uts["Anleggsnavn_norm"] = df_uts["Anleggsnavn"].str.strip().str.lower()
    df_tilk["Anleggsnavn_norm"] = df_tilk["anleggsnavn"].str.strip().str.lower()  
    
    # Slå sammen på normalisert navn
    df = pd.merge(
        df_uts,
        df_tilk[["Anleggsnavn_norm", "tilkoblet kommunalt avløp?"]],
        on="Anleggsnavn_norm",
        how="left"
    )
    
    col = "tilkoblet kommunalt avløp?"
    df["status"] = df[col].map(
        lambda x: "tilkoblet" if str(x).strip().lower() == "ja"
        else ("ikke" if str(x).strip().lower() == "nei" else "ukjent")
    )
    
    # Legg på kildestøyen direkte på rå-nitrogenmengden
    df["N"] = pd.to_numeric(df["Årlig utslipp til vann"], errors='coerce').fillna(0) * 1e-3 * noise_deponi # t -> kt
    
    # Definer vekter (Ukjent svinger tilfeldig fra runde til runde)
    df["w_tilkoblet"] = df["status"].map({"tilkoblet": 1.0, "ikke": 0.0, "ukjent": ukjent_vekt_tilkoblet})
    df["w_ikke"]      = df["status"].map({"tilkoblet": 0.0, "ikke": 1.0, "ukjent": ukjent_vekt_ikke})
    
    # Utslipp fordelt på strømmer
    df["N_tilkoblet"] = df["N"] * df["w_tilkoblet"]
    df["N_ikke"]      = df["N"] * df["w_ikke"]
    
    # Grupper per år
    df["År"] = pd.to_numeric(df["År"], errors='coerce')
    per_year = df.groupby("År", as_index=False)[["N_tilkoblet", "N_ikke"]].sum()
    
    # Pakk om til ordbøker
    dict_tilkoblet = dict(zip(per_year["År"], per_year["N_tilkoblet"]))
    dict_ikke = dict(zip(per_year["År"], per_year["N_ikke"]))
    
    # 3. INTERPOLERING FOR 2009 OG 2010
    # Vi finner gjennomsnittet av naboårene (2007, 2008, 2011, 2012)
    nabo_år = [2007, 2008, 2011, 2012]
    
    snitt_tilkoblet = np.mean([dict_tilkoblet.get(y, 0) for y in nabo_år if y in dict_tilkoblet])
    snitt_ikke = np.mean([dict_ikke.get(y, 0) for y in nabo_år if y in dict_ikke])
    
    for m_år in [2009, 2010]:
        # Ekstrapolert: Ganger det støybelagte snittet med trendstøyen
        dict_tilkoblet[m_år] = snitt_tilkoblet * noise_trend
        dict_ikke[m_år] = snitt_ikke * noise_trend

    return dict_tilkoblet, dict_ikke        
    
    
def find_non_edible_animal_products(df_hides_clean, df_wool, df_sheep, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i ikke-spiselige animalske produkter (huder og ull) lynraskt.
    Bruker ferdigfiltrerte data fra RAM, flate rundenøkler og asymmetrisk kildestøy.
    """
    year_values = {}
    
    # 1. Hent ut den asymmetriske datasettstøyen fra denne MC-runden (hvis den finnes, ellers 1.0)
    noise_faostat = dataset_noise['Crops and livestock products']['value']

    noise_ssb = dataset_noise['03710']['value']

    noise_wool = dataset_noise['Landbruksdirektoratet_wool']['value']

    # Trendstøy (hvis definert i dataset_noise, ellers 1.0)
    noise_trend = dataset_noise['trend interpolation']['value']

    # 2. Hent støybelagte parametere fra current_params (krasjer hardt om de mangler)
    N_content_hides = current_params.get('prod_Raw hides and skins')
    wool_pr_sheep = current_params.get('wool_per_sheep')
    N_content_wool = current_params.get('wool_N_frac')
    
    if N_content_hides is None or wool_pr_sheep is None or N_content_wool is None:
        raise KeyError(
            f"[KRITISK FEIL] Mangler parametere for ikke-spiselige produkter i current_params! "
            f"(prod_Raw hides and skins: {N_content_hides}, wool_per_sheep: {wool_pr_sheep}, wool_N_frac: {N_content_wool})"
        )

    # 3. Beregn N-mengde for huder og legg på kildestøy
    df_hides = df_hides_clean.copy()
    df_hides['N_amount'] = df_hides['Value'] * float(N_content_hides) * 1e-5 * float(noise_faostat)
    total_N_per_year = df_hides.groupby('Year')['N_amount'].sum().to_dict()

    # 4. Løp gjennom årene og legg til ull
    for year in range(1990, 2024):
        value = total_N_per_year.get(year, 0.0)
        
        if year > 2004 and year != 2001:
            # Bruk rapporterte ulldata + kildestøy
            wool_row = df_wool[df_wool['år'] == year]
            if not wool_row.empty:
                value += float(wool_row['ull'].iloc[0]) * float(N_content_wool) * float(noise_wool)
                
        elif year != 2001:
            # Bruk ekstrapolerte ulldata basert på SSB-sauetall + ssb-kildestøy
            sheep_row = df_sheep[df_sheep['År'] == year]
            if not sheep_row.empty:
                value += float(sheep_row['Husdyr (sau)'].iloc[0]) * float(wool_pr_sheep) * float(N_content_wool) * 1e-6 * float(noise_ssb)
                
        else:
            # Interpolering for 2001 + ssb-støy * trendstøy
            sheep_prev = df_sheep[df_sheep['År'] == year-1]
            sheep_next = df_sheep[df_sheep['År'] == year+1]
            if not sheep_prev.empty and not sheep_next.empty:
                avg_sheep = 0.5 * (
                    float(sheep_prev['Husdyr (sau)'].iloc[0]) +
                    float(sheep_next['Husdyr (sau)'].iloc[0])
                )
                value += (avg_sheep * float(wool_pr_sheep) * float(N_content_wool) * 1e-6 * float(noise_ssb)) * float(noise_trend)
                
        year_values[year] = value
        
    return year_values

def find_other_goods_export(prepared_trade_data, current_params, trade_params):
    """
    ULTRA-OPTIMALISERT: Beregner nitrogen i eksport av andre handelsvarer.
    Forventer forhåndssummerte data. Ingen tunge Pandas groupby-operasjoner inni loopen!
    """
    year_values = {}
    noise_trade = float(current_params.get('08801', current_params.get('13136')))
    
    # 1. Hent N-faktorer
    n_factor_dict = trade_params['value'].to_dict()
    
    # 2. Map faktorer og beregn N_amount i en midlertidig serie (vektorisert)
    v_factors = prepared_trade_data['konv'].map(n_factor_dict).fillna(0.0)
    n_amounts = (prepared_trade_data['amount'] * v_factors / 1e6 * noise_trade).values
    years = prepared_trade_data['year'].values
    
    # 3. Aggreger til ordbok med rå Python-loop (mye raskere enn Pandas groupby på små matriser)
    for idx in range(len(years)):
        yr = int(years[idx])
        year_values[yr] = year_values.get(yr, 0.0) + n_amounts[idx]
        
    return year_values



    
def find_other_industry_wastewater(prepared_wastewater_dict, current_params):
    """
    MC-OPTIMALISERT: Beregner nitrogen i avløpsvann fra øvrig industri.
    Mottar en ferdigpreparert ordbok med basetall og legger på rundens støyfaktor.
    """
    year_values = {}
    
    # Hent rundens støyfaktor for 'norskeutslipp' (hvis tom, bruk 1.0 som fallback)
    noise_norskeutslipp = float(current_params.get('norskeutslipp'))
    
    # Legg støy på de ferdige tallene for hvert år
    for year, base_value in prepared_wastewater_dict.items():
        year_values[year] = base_value * noise_norskeutslipp
        
    return year_values


def find_op_untreated_wastewater(prepared_untreated_dict, current_params):
    """
    MC-OPTIMALISERT: Beregner nitrogen i ubehandlet avløpsvann (OP).
    Mottar en ferdigpreparert ordbok og multipliserer med rundens 'norskeutslipp'-støy.
    """
    year_values = {}
    
    # Hent rundens støyfaktor for 'norskeutslipp'
    noise_norskeutslipp = float(current_params.get('norskeutslipp', 1.0))
    
    # Legg støy på de ferdigberegnede tallene
    for year, base_value in prepared_untreated_dict.items():
        year_values[year] = base_value * noise_norskeutslipp
        
    return year_values


def find_recycling(preloaded_data, current_params, current_trade_factors, dataset_noise, 
                   prepared_trade_recycling, prepared_trade_reuse, trade_params):
    """
    KORRIGERT VERSJON: Beregner nitrogen ved bruk av rå posisjons-indekser (iloc)
    siden Pandas har lastet inn kolonnenavnene som rene heltall [0, 1, 2...].
    """
    year_values = {y: 0.0 for y in range(1990, 2024)}
    
    # Hent tabellstøy
    noise_05281 = float(dataset_noise.get('05281', {}).get('value', 1.0))
    noise_10513 = float(dataset_noise.get('10513', {}).get('value', 1.0))
    noise_old = float(dataset_noise.get('historical_waste', {}).get('value', noise_05281))

    # N-fraksjoner
    paper_N   = float(current_params.waste_N_frac('paper'))
    plastic_N = float(current_params.waste_N_frac('plastic'))
    wood_N    = float(current_params.waste_N_frac('wood'))
    textile_N = float(current_params.waste_N_frac('textiles'))
    other_N   = float(current_params.waste_N_frac('other_materials'))
    haz_N     = float(current_params.waste_N_frac('hazardous'))
    mixed_N   = float(current_params.waste_N_frac('mixed_waste'))
    rubber_N  = float(current_params.waste_N_frac('rubber'))
    contam_N  = float(current_params.waste_N_frac('contaminated_masses'))

    # =========================================================================
    # 1. PARSING AV TABELL 05281 (1995-2011) - Posisjonsbasert (iloc)
    # =========================================================================
    df_05281 = preloaded_data.get('ssb_waste_05281')
    value_1995 = 0.0
    
    # Rad 2 inneholder årstallene bortover (kolonne 3 er 1995, 4 er 1996 osv)
    col_to_year_05281 = {}
    for col_idx in range(3,20):
        val = str(df_05281.iloc[2, col_idx]).strip()
        col_to_year_05281[col_idx] = int(val)

    # Loop gjennom alle rader for materialgjenvinning (excel-rad 18-31)
    for idx in range(17, 30):
        row_text = str(df_05281.iloc[idx, 2]).strip()
        n_frac = 0.0
        if 'Papir' in row_text: n_frac = paper_N
        elif 'Plast' in row_text: n_frac = plastic_N
        elif 'Treavfall' in row_text: n_frac = wood_N
        elif 'Tekstiler' in row_text: n_frac = textile_N
        elif 'Andre materialer' in row_text: n_frac = other_N
        elif 'Farlig avfall' in row_text: n_frac = haz_N
        elif 'Forurensede masser' in row_text: n_frac = contam_N

        if n_frac > 0:
            for col_idx, year in col_to_year_05281.items():
                val_kt = float(df_05281.iloc[idx, col_idx])
                year_values[year] += val_kt * n_frac * noise_05281

    value_1995 = year_values.get(1995, 0.0)

    # =========================================================================
    # 2. PARSING AV TABELL 10513 (2012-2023)
    # =========================================================================
    df_10513 = preloaded_data.get('ssb_waste_10513')
    if df_10513 is None:
        raise ValueError("[KRITISK] Data 'ssb_waste_10513' mangler i preloaded_data!")
        
    col_to_year_10513 = {}
    for col in range(1, df_10513.shape[1], 9):  
        cell_year = str(df_10513.iloc[3, col]).strip()
        if cell_year.replace('.0', '').isdigit():
            current_year = int(float(cell_year))
            target_col = col + 1  # Kolonneindeksen for materialgjenvinning
            if target_col < df_10513.shape[1]:
                col_to_year_10513[target_col] = current_year

    for idx in range(5, 25):
        row_text = str(df_10513.iloc[idx, 0]).strip()
        n_frac = 0.0
        
        if 'Papir' in row_text: n_frac = paper_N
        elif 'Plast' in row_text: n_frac = plastic_N
        elif 'Treavfall' in row_text: n_frac = wood_N
        elif 'Gummi' in row_text: n_frac = rubber_N
        elif 'Tekstiler' in row_text: n_frac = textile_N
        elif 'Farlig avfall' in row_text: n_frac = haz_N
        elif 'Blandet avfall' in row_text: n_frac = mixed_N
        elif 'Andre materialer' in row_text: n_frac = other_N
        elif 'Lett forurensede masser' in row_text.lower(): n_frac = contam_N

        if n_frac > 0:
            for col_idx, year in col_to_year_10513.items():
                val_kt = float(df_10513.iloc[idx, col_idx])
                year_values[year] += val_kt * n_frac * noise_10513
                
    # =========================================================================
    # 3. HISTORISK MODELLERING (1990-1994)
    # =========================================================================
    # Henter generert husholdningsavfall
    household_waste = find_household_waste(preloaded_data, current_params, dataset_noise)
    
    # Henter dataframene som find_other_industry_waste krever direkte fra preloaded_data
    df_05282_ind = preloaded_data['ssb_05282']
    df_10514_ind = preloaded_data['ssb_10514']
    df_hist_ind  = preloaded_data['ssb_hist_industry_waste']
    
    # Kaller funksjonen kirurgisk med alle 5 korrekte argumenter og henter ut kun waste-dicten [0]
    industry_waste = find_other_industry_waste(
        df_05282_ind, 
        df_10514_ind, 
        df_hist_ind, 
        current_params, 
        dataset_noise
    )[0]

    workbook = openpyxl.load_workbook('data_files/kommunalt_avfall_1985_1995.xlsx')
    sheet = workbook['forbrenning og gjenvinning']
    
    rec_frac_1985 = float(sheet.cell(row=2, column=2).value) / 100
    rec_frac_1992 = float(sheet.cell(row=3, column=2).value) / 100
    
    change_per_year = (rec_frac_1992 - rec_frac_1985) / 7
    rec_frac_1995 = rec_frac_1985 + change_per_year * (1995 - 1985)
    
    N_frac = value_1995 / ((household_waste[1995] + industry_waste[1995]) * rec_frac_1995)
    
    r = 3
    for year in range(1990, 1995):
        waste = household_waste[year] + industry_waste[year]
        
        if year < 1992:
            rec_frac = rec_frac_1985 + change_per_year * (year - 1985)
        else:
            rec_frac = float(sheet.cell(row=r, column=2).value) / 100
            r += 1
            
        value = waste * N_frac * rec_frac * noise_old
        year_values[year] = value        
        
    # =========================================================================
    # 4. FRATREKK AV HANDELSEKSPORT
    # =========================================================================
    export_resirk = find_export_for_recycling([], preloaded_data, current_params, current_trade_factors, dataset_noise)
    for year, val in export_resirk.items():
        if year in year_values: year_values[year] -= val

    export_reuse = find_export_for_reuse([], preloaded_data, current_params, current_trade_factors, dataset_noise)
    for year, val in export_reuse.items():
        if year in year_values: year_values[year] -= val

    # Nullstill negative
    for year in year_values:
        if year_values[year] < 0:
            year_values[year] = 0.0

    return year_values


def find_sewage_sludge_biogas(prepared_biogas_data, current_params):
    """
    MC-OPTIMALISERT: Beregner nitrogen i avløpsslam til biogass.
    Bruker ferdigpreparerte vektorer og rundens støyfaktorer.
    """
    year_values = {}
    
    # 1. Hent rundens unike støyfaktorer fra current_params
    sludge_N = float(current_params.get('sludge'))
    u_12359  = float(current_params.get('12359'))
    
    # 2. Beregn N_amount (vektorisert multiplikasjon: mengde * N-innhold * datasettstøy)
    n_amounts = prepared_biogas_data['amounts'] * sludge_N * u_12359
    years = prepared_biogas_data['years']
    
    # 3. Pakk inn i ordboken
    for idx, year in enumerate(years):
        year_values[year] = float(n_amounts[idx])
        
    return year_values


def find_solid_waste_export(prepared_waste_data, current_params, trade_params):
    """
    MC-OPTIMALISERT: Beregner nitrogen i eksport av fast avfall.
    Forventer forhåndssummerte mengder per år og konv-ID. Ingen groupby inni loopen!
    """
    year_values = {}
    
    # Hent rundens generelle støyfaktor for handelsdata
    noise_trade = float(current_params.get('08801', current_params.get('13136')))
    
    # 1. Hent rundens spesifikke N-faktorer for handelsvarene
    n_factor_dict = trade_params['value'].to_dict()
    
    # 2. Map faktorer og beregn N_amount (mengde * faktor / 1e6 * støy)
    v_factors = prepared_waste_data['konv'].map(n_factor_dict).fillna(0.0)
    n_amounts = (prepared_waste_data['amount'] * v_factors / 1e6 * noise_trade).values
    years = prepared_waste_data['year'].values
    
    # 3. Aggreger til ordbok
    for idx in range(len(years)):
        yr = int(years[idx])
        if 1988 <= yr <= 2024:
            year_values[yr] = year_values.get(yr, 0.0) + n_amounts[idx]
            
    return year_values


def find_treated_wastewater_discharge(df_05280, df_utslipp, current_params, dataset_noise=None, expected_years=None):
    """
    Henter renset avløpsvann fra SSB-data, ekstrapolerer bakover til 1990,
    og påfører simulert datasettstøy for tabell 05280.
    
    Returnerer:
        dict: En ordbok med {år: verdi_kt_N}
    """
    ww_discharge = {}
    
    # 1. Hent aktivitetsstøy for avløp (SSB tabell 05280)
    key_ssb = '05280'
    noise_ww = 1.0
    
    if dataset_noise and key_ssb in dataset_noise:
        noise_info = dataset_noise[key_ssb]
        if noise_info['type'] == 'perc':
            noise_ww = float(noise_info['value'])
    else:
        noise_ww = float(current_params.get('05280'))

    # For ekstrapolering bakover til 1990 trenger vi å holde styr på 1997-verdien
    value_1997 = 0.0

    # --- DEL 1: Nyere data (SSB 05280) ---
    # År ligger i radindeks 2 (Excel rad 3), verdier i radindeks 3 (Excel rad 4)
    # Kolonne 3 til 25 (Excel kolonne D til Z)
    if df_05280 is not None and df_05280.shape[0] > 3:
        years_row = df_05280.iloc[2]
        values_row = df_05280.iloc[3]
        
        for col_idx in range(3, min(26, df_05280.shape[1])):
            try:
                year = int(years_row.iloc[col_idx])
                val_t = float(values_row.iloc[col_idx])
                val_kt_N = (val_t / 1000.0) * noise_ww
                ww_discharge[year] = max(0.0, val_kt_N)
            except (ValueError, TypeError):
                continue

    # --- DEL 2: Historiske data 1997-2001 (utslipp_avløp.xlsx) ---
    # Radindeks 1 til 5 (Excel rad 2 til 6)
    if df_utslipp is not None:
        for r_idx in range(1, min(6, len(df_utslipp))):
            try:
                year = int(df_utslipp.iloc[r_idx, 0])
                val_kt_N = float(df_utslipp.iloc[r_idx, 1]) * noise_ww
                ww_discharge[year] = max(0.0, val_kt_N)
                
                if year == 1997:
                    value_1997 = val_kt_N
            except (ValueError, TypeError):
                continue

    # --- DEL 3: Ekstrapolering 1990-1996 ---
    # Bruker 1997-verdien som flat linje bakover hvis den ble funnet
    if value_1997 > 0.0:
        for year in range(1990, 1997):
            ww_discharge[year] = value_1997
            
    return ww_discharge

