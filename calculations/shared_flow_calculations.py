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
    # find_trade_flow,
    read_trade_data,
    process_generic_trade_flow
)

params = NParameters("data_files/N_parameters.xlsx")
waste_fracs = params.get_table('waste_fractions').set_index('waste_category')
trade_data = read_trade_data('data_files/Tab_08801_1988_2024.csv')


def find_aquaculture_production(df_aqua_modern, df_aqua_old, current_params, dataset_noise=None):
    aquaculture_production = {}
    
    fish_N_frac = float(current_params.get('fish_N_frac'))
    key_fisk = 'Fiskeridirektoratet'
    noise_aqua = dataset_noise[key_fisk]

    # --- DEL 1: Moderne data (fra 1994 og utover) ---
    for col in df_aqua_modern.columns:
        try:
            year = int(col)
            col_data = pd.to_numeric(df_aqua_modern[col], errors='coerce').fillna(0)
            value_tonn = col_data.sum()
            
            # Formel: (Tonn / 1000 -> kt rundvekt) * N-fraksjon * aktivitetsstøy = kt N
            val_kt_N = (value_tonn / 1000) * fish_N_frac * noise_aqua
            
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
            
            aquaculture_production[year] = val_kt_N
            
        except (ValueError, TypeError):
            continue

    return aquaculture_production


def find_export_for_recycling(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
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
    year_values = {}
    
    noise_energy = float(dataset_noise['11561'])
    
    GWh_to_TJ_factor = float(current_params.get('GWh_to_TJ_factor'))
    coal_NCV         = float(current_params.get('coal_feedstock_NCV'))
    oil_NCV          = float(current_params.get('oil_feedstock_NCV'))
    coal_N_frac      = float(current_params.get('coal_feedstock_N_frac'))
    oil_N_frac       = float(current_params.get('oil_feedstock_N_frac'))

    df_energy = preloaded_data.get('ssb_energy_balance_11561')
    
    # --- KULL OG KULLPRODUKTER ---
    for row_idx in range(38, 73):
        if row_idx >= len(df_energy): 
            break
        row_data = df_energy.iloc[row_idx]
        year_val = row_data.iloc[2]   # Kolonne C
        value_val = row_data.iloc[3]  # Kolonne D
        
        if pd.notna(year_val) and pd.notna(value_val) and value_val != '-':
            year = int(year_val)
            value = float(value_val) / (GWh_to_TJ_factor * coal_NCV) * coal_N_frac
            year_values[year] = year_values.get(year, 0.0) + (value * noise_energy)

    # --- OLJE OG OLJEPRODUKTER ---
    for row_idx in range(108, 143):
        if row_idx >= len(df_energy): 
            break
        row_data = df_energy.iloc[row_idx]
        year_val = row_data.iloc[2]   # Kolonne C
        value_val = row_data.iloc[3]  # Kolonne D
        
        if pd.notna(year_val) and pd.notna(value_val) and value_val != '-':
            year = int(year_val)
            value = float(value_val) / (GWh_to_TJ_factor * oil_NCV) * oil_N_frac
            year_values[year] = year_values.get(year, 0.0) + (value * noise_energy)

    return year_values

def find_food_industry_waste(df_05282, df_10514, current_params, dataset_noise):
    year_values = {}
    wet_org_N = float(current_params.get('wet_organic'))
    
    noise_05282 = float(dataset_noise['05282'])
    noise_10514 = float(dataset_noise['10514'])
    noise_trend = float(dataset_noise['trend interpolation'])
    
    value_2012_base = 0.0

    # --- DEL 1: Årene 2012-2023 (Tabell 10514) ---
    for col in range(2, 115, 10):  
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

    if value_2012_base == 0.0:
        raise ValueError("[KRITISK] Fant ikke basisverdi for år 2012 i Tabell 10514. Skalering umulig!")

    # --- DEL 2: Årene 1995-2011 (Tabell 05282) ---
    p_col_2011 = 162 - 1
    value_2011_base = float(df_05282.iloc[13, p_col_2011+1]) * wet_org_N
    value_2011_base += float(df_05282.iloc[13, p_col_2011+3]) * wet_org_N
    value_2011_base += float(df_05282.iloc[13, p_col_2011+8]) * wet_org_N

    if value_2011_base == 0.0:
        value_2011_base = 1.0

    mean_val_accumulator = 0.0
    mean_year_count = 0

    # I openpyxl: range(2, 170, 10)
    for col in range(2, 170, 10):  
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
    household_waste = {y: 0.0 for y in range(1990, 2024)}
    
    noise_05282 = float(dataset_noise['05282'])
    noise_10514 = float(dataset_noise['10514'])
    noise_interp = float(dataset_noise['trend interpolation'])

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
    df_05282 = preloaded_data['ssb_05282']
    value_1995 = 0.0
    width_05282 = df_05282.shape[1]

    col_to_year = {}
    for col_idx in range(1, width_05282):
        val = str(df_05282.iloc[3, col_idx]).strip()
        if val.replace('.0', '').isdigit():
            y = int(float(val))
            if 1995 <= y <= 2011:
                col_to_year[col_idx] = y

    for col_idx, year in col_to_year.items():
        val_year = 0.0
        
        # Papir (Excel rad 7 -> indeks 6)
        for c in [5, 6, 9]:
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
    df_10514 = preloaded_data['ssb_10514']
    width_10514 = df_10514.shape[1]
    
    col_to_year_10514 = {}
    for col_idx in range(1, width_10514):
        val = str(df_10514.iloc[3, col_idx]).strip()
        if val.replace('.0', '').isdigit():
            y = int(float(val))
            if 2012 <= y <= 2023:
                col_to_year_10514[col_idx] = y

    for col_idx, year in col_to_year_10514.items():
        val_year = 0.0
        
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
    
    paper_N     = float(current_params.waste_N_frac('paper'))
    plastic_N   = float(current_params.waste_N_frac('plastic'))
    wood_N      = float(current_params.waste_N_frac('wood'))
    textiles_N  = float(current_params.waste_N_frac('textiles'))
    wet_org_N   = float(current_params.waste_N_frac('wet_organic'))
    other_mat_N = float(current_params.waste_N_frac('other_materials'))
    hazardous_N = float(current_params.waste_N_frac('hazardous'))
    mixed_N     = float(current_params.waste_N_frac('mixed_waste'))
    
    noise_05282 = float(dataset_noise['05282'])
    noise_10514 = float(dataset_noise['10514'])
    noise_trend = float(dataset_noise['trend interpolation'])        

    arr_05282 = df_05282.values
    arr_10514 = df_10514.values
    
    base_value_1995 = 0.0

    # --- DEL 1: ÅRENE 1995-2011 (Tabell 05282) ---
    for col in range(1, 169, 10):
        year = int(arr_05282[3, col])
            
        value_base = 0.0
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

        if year == 1995:
            base_value_1995 = value_base
            
        industry_waste[year] = value_base * noise_05282

    # --- DEL 2: ÅRENE 2012-2023 (Tabell 10514) ---
    for col in range(1, 114, 10):
        year = int(arr_10514[3, col])
            
        value_base = 0.0
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

        industry_waste[year] = value_base * noise_10514

    # --- DEL 3: LINEÆR EKSTRAPOLERING TILBAKE TIL 1990 ---
    waste_kt_1992 = float(df_hist_waste.iloc[1, 2])
    waste_kt_1995 = float(df_hist_waste.iloc[2, 2])


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

    return industry_waste


def find_industrial_crop_products(df_gnb_sheet30, dataset_noise):
    year_values = {}
    
    key_gnb = 'Gross nutrient balance'
    noise_gnb_val = dataset_noise[key_gnb]
    
    key_interp = 'trend interpolation'
    noise_interp_val = dataset_noise[key_interp]
    
    year_row = df_gnb_sheet30.iloc[8]
    value_row = df_gnb_sheet30.iloc[10]
    
    for col_idx in range(1, len(df_gnb_sheet30.columns)):
        year_val = year_row.iloc[col_idx]
        val_val = value_row.iloc[col_idx]
        
        if pd.notna(year_val) and pd.notna(val_val) and val_val != '-':
            try:
                year = int(year_val)
                base_value = float(val_val) * 1.0e-3  # kg -> kt
                value = base_value * noise_gnb_val
                
                year_values[year] = value
            except ValueError:
                continue

    # --- 4. Ekstrapolering for hull i tidsserien (2017-2019) ---
    if year_values:
        mean_value = float(np.mean(list(year_values.values())))
        
        for year in range(2017, 2020):
            value_interp = mean_value * noise_interp_val
                
            year_values[year] = value_interp
            
    return year_values

def find_industrial_round_wood(preloaded_data, current_params, dataset_noise):
    year_values = {}
    
    noise_faostat = dataset_noise['Forestry production and trade']
    wood_density  = float(current_params.get('wood_density'))
    conifer_N     = float(current_params.get('conifer_N_frac'))
    nonconifer_N   = float(current_params.get('nonconifer_N_frac'))
    
    data = preloaded_data.get('faostat_forestry')
    
    filtered_data = data[(data['Element'] == 'Production') & (data['Value'] != 0)].copy()
    
    items_conifer = ['Industrial roundwood, coniferous']
    items_nonconifer = ['Industrial roundwood, non-coniferous']
    
    final_data = filtered_data[filtered_data['Item'].isin(items_conifer + items_nonconifer)].copy()
    
    final_data['tonnes'] = final_data['Value'] * wood_density
    
    mask_conifer = final_data['Item'].isin(items_conifer)
    mask_nonconifer = final_data['Item'].isin(items_nonconifer)
    
    final_data['N_kg_per_kg'] = 0.0
    final_data.loc[mask_conifer, 'N_kg_per_kg'] = conifer_N
    final_data.loc[mask_nonconifer, 'N_kg_per_kg'] = nonconifer_N
    
    # Tonn * kg N/tonn / 1e3 -> kt N
    final_data['N_amount'] = final_data['tonnes'] * final_data['N_kg_per_kg'] / 1e3
    
    total_N_per_year = final_data.groupby('Year')['N_amount'].sum().to_dict()
    
    # 4. Fyll year_values og legg på kildestøyen (noise_faostat)
    for year in EXPECTED_YEARS:
        value = total_N_per_year.get(year, 0.0)
        if value > 0:
            # Ganger med kildestøyen (Forestry proc) som har blitt generert for denne iterasjonen
            year_values[year] = value * noise_faostat
            
    return year_values

def find_industrial_waste_fuels(df_bio_08205, df_bio_hist, current_params, dataset_noise):
    year_values = {}
    
    noise_08205 = float(dataset_noise['08205'])
    noise_trend = float(dataset_noise['trend interpolation'])

    NCV              = float(current_params.get('firewood_NCV'))
    N_content        = float(current_params.get('firewood_N_frac'))
    GWh_to_TJ_factor = float(current_params.get('GWh_to_TJ_factor'))    
    
    arr_08205 = df_bio_08205.values
    arr_hist = df_bio_hist.values
    
    raw_sum_pre_2008 = 0.0
    
    # --- DEL 1: SSB Tabell 08205 (Nyere data) ---
    
    for col in range(3, 25):
        year_val = arr_08205[2, col]
        value_val = arr_08205[9, col]
            
        year = int(year_val)
        # Konvertering: GWh til TJ, del på NCV til kt brensel, gang med N_content til ktN
        value_raw = float(value_val) / GWh_to_TJ_factor / NCV * N_content
            
        year_values[year] = value_raw * noise_08205
                # Akkumuler RÅ verdi til gjennomsnittet hvis året er før 2008
        if year < 2008:
            raw_sum_pre_2008 += value_raw

    # --- DEL 2: Historiske data 1998-2002 (df_bio_hist) ---
    for r in range(1, 6):
        year_val = arr_hist[r, 0]
        val_col2 = arr_hist[r, 1]
        val_col3 = arr_hist[r, 2]
            
        year = int(year_val)
        value_raw = (float(val_col2) + float(val_col3)) / GWh_to_TJ_factor / NCV * N_content
            
        year_values[year] = value_raw * noise_08205
        
        if year < 2008:
            raw_sum_pre_2008 += value_raw

    # --- DEL 3: Gjennomsnitt for årene 1990-1997 (Ekstrapolering) ---
    mean_value_raw = raw_sum_pre_2008 / 10.0
    
    for year in range(1990, 1998):
        # Påfør ekstrapoleringsstøy på det rå gjennomsnittet
        year_values[year] = mean_value_raw * noise_trend

    return year_values


def find_non_edible_animal_products(df_hides_clean, df_wool, df_sheep, current_params, dataset_noise):
    year_values = {}
    
    noise_faostat = dataset_noise['Crops and livestock products']
    noise_ssb = dataset_noise['03710']
    noise_wool = dataset_noise['Landbruksdirektoratet_wool']
    noise_trend = dataset_noise['trend interpolation']

    N_content_hides = current_params.get('prod_Raw hides and skins')
    wool_pr_sheep = current_params.get('wool_per_sheep')
    N_content_wool = current_params.get('wool_N_frac')
    
    df_hides = df_hides_clean.copy()
    df_hides['N_amount'] = df_hides['Value'] * float(N_content_hides) * 1e-5 * float(noise_faostat)
    total_N_per_year = df_hides.groupby('Year')['N_amount'].sum().to_dict()

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

    
def find_other_industry_wastewater(prepared_wastewater_dict, current_params):
    year_values = {}
    
    noise_norskeutslipp = float(current_params.get('norskeutslipp'))
    
    for year, base_value in prepared_wastewater_dict.items():
        year_values[year] = base_value * noise_norskeutslipp
        
    return year_values


def find_recycling(preloaded_data, current_params, current_trade_factors, dataset_noise, 
                    prepared_trade_recycling, prepared_trade_reuse, trade_params):
    year_values = {y: 0.0 for y in range(1990, 2024)}
    
    noise_05281 = float(dataset_noise['05281'])
    noise_10513 = float(dataset_noise['10513'])
    noise_old = float(dataset_noise['historical_waste'])

    paper_N   = float(current_params.waste_N_frac('paper'))
    plastic_N = float(current_params.waste_N_frac('plastic'))
    wood_N    = float(current_params.waste_N_frac('wood'))
    textile_N = float(current_params.waste_N_frac('textiles'))
    other_N   = float(current_params.waste_N_frac('other_materials'))
    haz_N     = float(current_params.waste_N_frac('hazardous'))
    mixed_N   = float(current_params.waste_N_frac('mixed_waste'))
    rubber_N  = float(current_params.waste_N_frac('rubber'))
    contam_N  = float(current_params.waste_N_frac('contaminated_masses'))

    df_05281 = preloaded_data.get('ssb_waste_05281')
    value_1995 = 0.0
    
    col_to_year_05281 = {}
    for col_idx in range(3,20):
        val = str(df_05281.iloc[2, col_idx]).strip()
        col_to_year_05281[col_idx] = int(val)

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

    df_10513 = preloaded_data.get('ssb_waste_10513')
        
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
                
    household_waste = find_household_waste(preloaded_data, current_params, dataset_noise)
    
    df_05282_ind = preloaded_data['ssb_05282']
    df_10514_ind = preloaded_data['ssb_10514']
    df_hist_ind  = preloaded_data['ssb_hist_industry_waste']
    
    industry_waste = find_other_industry_waste(
        df_05282_ind, 
        df_10514_ind, 
        df_hist_ind, 
        current_params, 
        dataset_noise
    )

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
        
    export_resirk = find_export_for_recycling([], preloaded_data, current_params, current_trade_factors, dataset_noise)
    for year, val in export_resirk.items():
        if year in year_values: year_values[year] -= val

    export_reuse = find_export_for_reuse([], preloaded_data, current_params, current_trade_factors, dataset_noise)
    for year, val in export_reuse.items():
        if year in year_values: year_values[year] -= val

    return year_values


def find_treated_wastewater_discharge(df_05280, df_utslipp, current_params, dataset_noise=None, expected_years=None):
    ww_discharge = {}
    
    key_ssb = '05280'
    noise_ww = dataset_noise[key_ssb]

    value_1997 = 0.0

    # --- DEL 1: Nyere data (SSB 05280) ---
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

