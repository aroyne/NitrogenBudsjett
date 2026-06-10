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
    read_year_value_row
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
    noise_trade = float(current_params.get('08801', current_params.get('13136', 1.0)))
    
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
    fish_N_frac = float(current_params.get('fish_N_frac', 0.028))
    
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
        noise_aqua = float(current_params.get('Fiskeridirekt', current_params.get('Fiskeridirektoratet', 1.0)))

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


def find_export_for_recycling(prepared_trade_data, current_params, trade_params):
    """Henter eksport for resirkulering med varehandelsstøy."""
    year_values = {}
    noise_trade = float(current_params.get('08801', current_params.get('13136', 1.0)))
    
    aggregated_data, _ = find_trade_flow(
        data_impeks=prepared_trade_data, 
        trade_params=trade_params, 
        dataset_unc=None, 
        wide=False
    )
    
    if not aggregated_data.empty:
        for index, row in aggregated_data.iterrows():
            year = int(row['year'])
            year_values[year] = float(row['N_amount']) * noise_trade
            
    return year_values


def find_export_for_reuse(prepared_trade_data, current_params, trade_params):
    """Henter eksport for gjenbruk med varehandelsstøy."""
    year_values = {}
    noise_trade = float(current_params.get('08801', current_params.get('13136', 1.0)))
    
    aggregated_data, _ = find_trade_flow(
        data_impeks=prepared_trade_data, 
        trade_params=trade_params, 
        dataset_unc=None, 
        wide=False
    )
    
    if not aggregated_data.empty:
        for index, row in aggregated_data.iterrows():
            year = int(row['year'])
            year_values[year] = float(row['N_amount']) * noise_trade
            
    return year_values


def find_feedstock_fuel(df_energy, current_params):
    """Beregner nitrogen i råstoff med kildestøy fra energibalansen (11561)."""
    year_values = {}
    
    # Hent støy for energibalansen (Tabell 11561 står øverst i arket ditt)
    noise_energy = float(current_params.get('11561', 1.0))
    
    GWh_to_TJ_factor = float(current_params['GWh_to_TJ_factor'])
    coal_NCV         = float(current_params['coal_feedstock_NCV'])
    oil_NCV          = float(current_params['oil_feedstock_NCV'])
    coal_N_frac      = float(current_params['coal_feedstock_N_frac'])
    oil_N_frac       = float(current_params['oil_feedstock_N_frac'])

    # --- KULL ---
    for row_idx in range(38, 73):
        try:
            row_data = df_energy.iloc[row_idx]
            year_val = row_data.iloc[2]
            value_val = row_data.iloc[3]
            
            if pd.notna(year_val) and pd.notna(value_val) and value_val != '-':
                year = int(year_val)
                value = float(value_val) / (GWh_to_TJ_factor * coal_NCV) * coal_N_frac
                # Multipliser med kildestøy
                year_values[year] = year_values.get(year, 0.0) + (value * noise_energy)
        except Exception:
            continue

    # --- OLJE ---
    for row_idx in range(108, 143):
        try:
            row_data = df_energy.iloc[row_idx]
            year_val = row_data.iloc[2]
            value_val = row_data.iloc[3]
            
            if pd.notna(year_val) and pd.notna(value_val) and value_val != '-':
                year = int(year_val)
                value = float(value_val) / (GWh_to_TJ_factor * oil_NCV) * oil_N_frac
                # Multipliser med kildestøy
                year_values[year] = year_values.get(year, 0.0) + (value * noise_energy)
        except Exception:
            continue

    return year_values


def find_food_industry_waste(df_05282, df_10514, current_params):
    """
    NY/OPPDATERT: Beregner nitrogen i matindustriavfall basert på ferdiginnleste tabeller
    og gjeldende MC-parametersett (inkludert både kildestøy og ekstrapoleringsstøy).
    """
    year_values = {}
    wet_org_N = float(current_params['wet_organic'])
    
    noise_05282 = float(current_params.get('05282', 1.0))
    noise_10514 = float(current_params.get('10514', 1.0))
    noise_trend = float(current_params.get('trend interpolation', 1.0))
    
    value_2012 = 0.0
    value_2011 = 0.0
    mean_val = 0.0

    # --- DEL 1: Årene 2012-2023 (Tabell 10514) ---
    for col in range(1, 114, 10):  
        try:
            year = int(df_10514.iloc[3, col])
            value = 0.0
            # Summerer jordbruk(col+1), industri(col+3), annen næring(col+8) fra Rad 7 (indeks 6)
            value += float(df_10514.iloc[6, col+1]) * wet_org_N
            value += float(df_10514.iloc[6, col+3]) * wet_org_N
            value += float(df_10514.iloc[6, col+8]) * wet_org_N
            
            if year == 2012:
                value_2012 = value
                
            year_values[year] = value * noise_10514
        except Exception:
            continue

    # --- DEL 2: Årene 1995-2011 (Tabell 05282) ---
    # Først finn 2011-verdi for skalering (kolonne 162 i openpyxl -> indeks 161)
    try:
        v_2011 = float(df_05282.iloc[13, 161+1]) * wet_org_N
        v_2011 += float(df_05282.iloc[13, 161+3]) * wet_org_N
        v_2011 += float(df_05282.iloc[13, 161+8]) * wet_org_N
        value_2011 = v_2011
    except Exception:
        value_2011 = 1.0

    for col in range(1, 169, 10):  
        try:
            year = int(df_05282.iloc[3, col])
            value = 0.0
            # Rad 14 (indeks 13)
            value += float(df_05282.iloc[13, col+1]) * wet_org_N
            value += float(df_05282.iloc[13, col+3]) * wet_org_N
            value += float(df_05282.iloc[13, col+8]) * wet_org_N
            
            # Skalering i henhold til opprinnelig formel
            if value_2011 > 0:
                value *= (value_2012 / value_2011)
                
            if year < 2000:
                mean_val += value  
                
            year_values[year] = value * noise_05282
        except Exception:
            continue

    # --- DEL 3: Ekstrapolering for årene 1990-1994 (Gjennomsnitt) ---
    final_mean = (mean_val / 5.0) if mean_val > 0 else 0.0
    for year in range(1990, 1995):
        # Siden dette er ekstrapolert, legger vi på noise_trend!
        year_values[year] = final_mean * noise_05282 * noise_trend
        
    return year_values


def find_household_waste(df_05282, df_10514, current_params):
    """
    Beregner nitrogen i husholdningsavfall basert på SSB-tabeller.
    Gjenoppretter den nøyaktige originale interpoleringen for 1990-1994.
    """
    household_waste = {}
    
    # Hent nitrogen-fraksjonene fra denne rundens parametersett
    paper_N   = float(current_params['paper'])
    plastic_N = float(current_params['plastic'])
    wood_N    = float(current_params['wood'])
    textile_N = float(current_params['textiles'])
    wet_N     = float(current_params['wet_organic'])
    other_N   = float(current_params['other_materials'])
    haz_N     = float(current_params['hazardous'])
    contam_N  = float(current_params['contaminated_masses'])
    mixed_N   = float(current_params['mixed_waste'])
    park_N    = float(current_params['park_garden'])
    
    # Hent ut denne rundens MC-støyfaktorer
    noise_05282 = float(current_params.get('05282', 1.0))
    noise_10514 = float(current_params.get('10514', 1.0))
    noise_trend = float(current_params.get('trend interpolation', 1.0))
    
    value_1995 = 0.0

    # --- DEL 1: ÅRENE 1995-2011 (Tabell 05282) ---
    # range(2, 170, 10) i openpyxl -> range(1, 169, 10) i Pandas iloc (0-indeksert)
    for col in range(1, 169, 10):
        try:
            year = int(df_05282.iloc[3, col]) # rad 4 -> indeks 3
            value = 0.0
            
            # Vi summerer kolonnene nøyaktig slik du gjorde i den opprinnelige koden:
            # Papir (Rad 7 -> indeks 6)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_05282.iloc[6, col + c]) * paper_N
            # Plast (Rad 9 -> indeks 8)
            for c in [5, 6, 9]:
                value += float(df_05282.iloc[8, col + c]) * plastic_N
            # Treavfall (Rad 12 -> indeks 11)
            for c in [5, 6, 9]:
                value += float(df_05282.iloc[11, col + c]) * wood_N
            # Tekstiler (Rad 13 -> indeks 12)
            for c in [5, 6, 9]:
                value += float(df_05282.iloc[12, col + c]) * textile_N
            # Våtorganisk (Rad 14 -> indeks 13)
            for c in [5, 6, 9]:
                value += float(df_05282.iloc[13, col + c]) * wet_N
            # Andre materialer (Rad 17 -> indeks 16)
            for c in [5, 6, 9]:
                value += float(df_05282.iloc[16, col + c]) * other_N
            # Farlig avfall (Rad 18 -> indeks 17)
            for c in [5, 6, 9]:
                value += float(df_05282.iloc[17, col + c]) * haz_N
            # Forurensede masser (Rad 19 -> indeks 18)
            for c in [5, 6, 9]:
                value += float(df_05282.iloc[18, col + c]) * contam_N

            # Ta vare på RÅ-verdien for 1995 FØR datasettstøy legges på, 
            # slik at interpoleringen bakover baserer seg på riktig utgangspunkt.
            if year == 1995:
                value_1995 = value
                
            household_waste[year] = value * noise_05282
        except Exception:
            continue

    # --- DEL 2: ÅRENE 2012-2023 (Tabell 10514) ---
    # range(2, 115, 10) i openpyxl -> range(1, 114, 10) i Pandas iloc
    for col in range(1, 114, 10):
        try:
            year = int(df_10514.iloc[3, col]) # rad 4 -> indeks 3
            value = 0.0
            
            # Våtorganisk (Rad 7 -> indeks 6)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[6, col + c]) * wet_N
            # Park og hage (Rad 8 -> indeks 7)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[7, col + c]) * park_N
            # Treavfall (Rad 9 -> indeks 8)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[8, col + c]) * wood_N
            # Papir (Rad 11 -> indeks 10)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[10, col + c]) * paper_N
            # Plast (Rad 17 -> indeks 16)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[16, col + c]) * plastic_N
            # Tekstiler (Rad 19 -> indeks 18)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[18, col + c]) * textile_N
            # Andre materialer (Rad 24 -> indeks 23)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[23, col + c]) * other_N
            # Farlig avfall (Rad 22 -> indeks 21)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[21, col + c]) * haz_N
            # Blandet avfall (Rad 23 -> indeks 22)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[22, col + c]) * mixed_N
            # Forurensede masser (Rad 25 -> indeks 24)
            for c in [4, 5, 6, 7, 9]:
                value += float(df_10514.iloc[24, col + c]) * contam_N

            household_waste[year] = value * noise_10514
        except Exception:
            continue

    # --- DEL 3: REEL LINEÆR EKSTRAPOLERING TILBAKE TIL 1990 ---
    inhabitants_1990 = 4233116
    inhabitants_1995 = 4348410
    waste_kg_person_1990 = 200
    waste_kg_person_1995 = 289
    
    waste_kt_1990 = waste_kg_person_1990 * inhabitants_1990 * 1e-6
    waste_kt_1995 = waste_kg_person_1995 * inhabitants_1995 * 1e-6
    
    # Sjekk at vi faktisk fikk tak i 1995-verdien fra loopen over
    if waste_kt_1995 > 0 and value_1995 > 0:
        N_frac = value_1995 / waste_kt_1995
        value_1990 = waste_kt_1990 * N_frac
        change_per_year = (value_1995 - value_1990) / 5
        
        step = 0
        for year in range(1990, 1995):
            value = value_1990 + change_per_year * step
            step += 1
            # For ekstrapolerte år: Vi bruker kildestøyen for 05282 (siden 1995 kom derfra)
            # OG vi GANGER med trendstøyen (noise_trend) for å gi den ekstra usikkerhetsbredde!
            household_waste[year] = value * noise_05282 * noise_trend
            
    return household_waste


import numpy as np
import pandas as pd

import numpy as np
import pandas as pd

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

def find_industrial_round_wood(preloaded_data, current_params):
    """
    Beregner industrirundvirke ved å bruke pre-loadet FAOSTAT-data fra RAM,
    og ferdigstøysatte parametere/kildestøy fra NParameters-objektet.
    """
    year_values = {}
    
    # 1. Hent modellparametere og kildestøy fra current_params (NParameters)
    noise_faostat = float(current_params.get('Forestry proc', 1.0))
    wood_density  = float(current_params.get('wood_density', 0.0))
    conifer_N     = float(current_params.get('conifer_N_frac', 0.0))
    nonconifer_N   = float(current_params.get('nonconifer_N_frac', 0.0))
    
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

def find_industrial_waste_fuels(df_bio_08205, df_bio_hist, current_params):
    """Beregner egentilvirket bioenergi med datasettstøy og ekstrapoleringsstøy."""
    year_values = {}
    
    noise_08205 = float(current_params.get('08205', 1.0))
    noise_trend = float(current_params.get('trend interpolation', 1.0))
    
    # Parametere
    NCV              = float(current_params['firewood_NCV'])
    N_content        = float(current_params['firewood_N_frac'])
    GWh_to_TJ_factor = float(current_params['GWh_to_TJ_factor'])
    
    val = 0.0
    
    # --- DEL 1: SSB Tabell 08205 (Nyere data) ---
    year_row = df_bio_08205.iloc[2]
    value_row = df_bio_08205.iloc[9]
    
    for col in range(3, 25):
        try:
            year_val = year_row.iloc[col]
            value_val = value_row.iloc[col]
            
            if pd.notna(year_val) and pd.notna(value_val):
                year = int(year_val)
                value = float(value_val) / GWh_to_TJ_factor / NCV * N_content
                year_values[year] = value * noise_08205
                
                if year < 2008:
                    val += value * noise_08205
        except Exception:
            continue

    # --- DEL 2: Historiske data 1998-2002 ---
    for r in range(1, 6):
        try:
            year_val = df_bio_hist.iloc[r, 0]
            val_col2 = df_bio_hist.iloc[r, 1]
            val_col3 = df_bio_hist.iloc[r, 2]
            
            if pd.notna(year_val):
                year = int(year_val)
                value = (float(val_col2) + float(val_col3)) / GWh_to_TJ_factor / NCV * N_content
                year_values[year] = value * noise_08205
                
                if year < 2008:
                    val += value * noise_08205
        except Exception:
            continue

    # --- DEL 3: Gjennomsnitt for årene 1990-1997 (Ekstrapolering) ---
    mean_value = val / 10.0 if val > 0 else 0.0
    for year in range(1990, 1998):
        # EKSTRAPOLERT: Her ganger vi det støybelagte gjennomsnittet med noise_trend!
        year_values[year] = mean_value * noise_trend
        
    return year_values


def find_landfill_emissions_to_water(df_uts, df_tilk, current_params):
    """
    Beregner deponiutslipp til vann fordelt på tilkoblet og ikke-tilkoblet kommunalt avløp.
    Bruker kildestøy fra 'norskeutslipp' og trendstøy for interpolerte år (2009-2010).
    """
    # 1. Hent støyfaktorer fra denne MC-runden
    # NÅ OPPDATERT: Bruker 'norskeutslipp' som primærnøkkel!
    noise_deponi = float(current_params.get('norskeutslipp', 1.0))
    noise_trend  = float(current_params.get('trend interpolation', 1.0))
    
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
    has_fao = dataset_noise and 'Crops and livestock products' in dataset_noise
    noise_faostat = dataset_noise['Crops and livestock products']['value'] if has_fao else 1.0

    has_03710 = dataset_noise and '03710' in dataset_noise
    noise_ssb = dataset_noise['03710']['value'] if has_03710 else 1.0

    has_wool = dataset_noise and 'Landbruksdirektoratet_wool' in dataset_noise
    noise_wool = dataset_noise['Landbruksdirektoratet_wool']['value'] if has_wool else 1.0

    # Trendstøy (hvis definert i dataset_noise, ellers 1.0)
    noise_trend = 1.0
    if dataset_noise and 'trend interpolation' in dataset_noise:
        noise_trend = dataset_noise['trend interpolation']['value']

    # 2. Hent støybelagte parametere fra current_params (krasjer hardt om de mangler)
    N_content_hides = current_params.get('prod_Raw hides and skins', None)
    wool_pr_sheep = current_params.get('wool_per_sheep', None)
    N_content_wool = current_params.get('wool_N_frac', None)
    
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
    noise_trade = float(current_params.get('08801', current_params.get('13136', 1.0)))
    
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


def find_other_goods_import(prepared_trade_data, current_params, trade_params):
    """
    ULTRA-OPTIMALISERT: Beregner nitrogen i import av andre handelsvarer.
    Forventer forhåndssummerte data. Ingen tunge Pandas groupby-operasjoner inni loopen!
    """
    year_values = {}
    noise_trade = float(current_params.get('08801', current_params.get('13136', 1.0)))
    
    # 1. Hent N-faktorer
    n_factor_dict = trade_params['value'].to_dict()
    
    # 2. Map faktorer og beregn N_amount (vektorisert)
    v_factors = prepared_trade_data['konv'].map(n_factor_dict).fillna(0.0)
    n_amounts = (prepared_trade_data['amount'] * v_factors / 1e6 * noise_trade).values
    years = prepared_trade_data['year'].values
    
    # 3. Aggreger til ordbok
    for idx in range(len(years)):
        yr = int(years[idx])
        year_values[yr] = year_values.get(yr, 0.0) + n_amounts[idx]
        
    return year_values



def find_other_industry_waste(df_05282, df_10514, df_hist_waste, current_params):
    """
    MC-OPTIMALISERT: Beregner nitrogen i øvrig industriavfall basert på SSB-tabeller.
    Konverterer DataFrames til NumPy-matriser for ekstremt raske celleoppslag inni loopen.
    """
    industry_waste = {}
    
    # 1. Hent nitrogen-fraksjoner fra denne rundens parametersett
    paper_N     = float(current_params['paper'])
    plastic_N   = float(current_params['plastic'])
    wood_N      = float(current_params['wood'])
    textiles_N  = float(current_params['textiles'])
    wet_org_N   = float(current_params['wet_organic'])
    other_mat_N = float(current_params['other_materials'])
    hazardous_N = float(current_params['hazardous'])
    mixed_N     = float(current_params['mixed_waste'])
    
    # 2. Hent støyfaktorer for denne MC-runden
    noise_05282 = float(current_params.get('05282', 1.0))
    noise_10514 = float(current_params.get('10514', 1.0))
    noise_trend = float(current_params.get('trend interpolation', 1.0))
    
    # --- HASTIGHETS-BOOST: Konverter til NumPy-matriser ---
    arr_05282 = df_05282.values
    arr_10514 = df_10514.values
    
    value_1995 = 0.0

    # --- DEL 1: ÅRENE 1995-2011 (Tabell 05282) ---
    for col in range(1, 169, 10):
        try:
            year = int(arr_05282[3, col])  # Mye raskere enn .iloc
            value = 0.0
            
            # Papir (Rad 7 -> indeks 6)
            for c in [2, 3, 8]: value += float(arr_05282[6, col + c]) * paper_N
            # Plast (Rad 9 -> indeks 8)
            for c in [2, 3, 8]: value += float(arr_05282[8, col + c]) * plastic_N
            # Treavfall (Rad 12 -> indeks 11)
            for c in [2, 3, 8]: value += float(arr_05282[11, col + c]) * wood_N
            # Tekstiler (Rad 13 -> indeks 12)
            for c in [2, 3, 8]: value += float(arr_05282[12, col + c]) * textiles_N
            # Våtorganisk (Rad 14 -> indeks 13) - Bare fra bergverk (c=2)
            for c in [2]:      value += float(arr_05282[13, col + c]) * wet_org_N
            # Andre materialer (Rad 17 -> indeks 16)
            for c in [2, 3, 8]: value += float(arr_05282[16, col + c]) * other_mat_N
            # Farlig avfall (Rad 18 -> indeks 17)
            for c in [2, 3, 8]: value += float(arr_05282[17, col + c]) * hazardous_N

            if year == 1995:
                value_1995 = value
                
            industry_waste[year] = value * noise_05282
        except Exception:
            continue

    # --- DEL 2: ÅRENE 2012-2023 (Tabell 10514) ---
    for col in range(1, 114, 10):
        try:
            year = int(arr_10514[3, col])
            value = 0.0
            
            # Våtorganisk (Rad 7 -> indeks 6)
            for c in [2]:      value += float(arr_10514[6, col + c]) * wet_org_N
            # Treavfall (Rad 9 -> indeks 8)
            for c in [2, 3, 8]: value += float(arr_10514[8, col + c]) * wood_N
            # Papir (Rad 11 -> indeks 10)
            for c in [2, 3, 8]: value += float(arr_10514[10, col + c]) * paper_N
            # Plast (Rad 17 -> indeks 16)
            for c in [2, 3, 8]: value += float(arr_10514[16, col + c]) * plastic_N
            # Tekstiler (Rad 19 -> indeks 18)
            for c in [2, 3, 8]: value += float(arr_10514[18, col + c]) * textiles_N
            # Andre materialer (Rad 24 -> indeks 23)
            for c in [2, 3, 8]: value += float(arr_10514[23, col + c]) * other_mat_N
            # Farlig avfall (Rad 22 -> indeks 21)
            for c in [2, 3, 8]: value += float(arr_10514[21, col + c]) * hazardous_N
            # Blandet avfall (Rad 23 -> indeks 22)
            for c in [2, 3, 8]: value += float(arr_10514[22, col + c]) * mixed_N

            industry_waste[year] = value * noise_10514
        except Exception:
            continue

    # --- DEL 3: LINEÆR EKSTRAPOLERING TILBAKE TIL 1990 ---
    try:
        waste_kt_1992 = float(df_hist_waste.iloc[0, 2])
        waste_kt_1995 = float(df_hist_waste.iloc[1, 2])
        
        if value_1995 == 0.0:
            col_1995 = 1
            v_95 = 0.0
            for c in [2, 3, 8]: v_95 += float(arr_05282[6, col_1995 + c]) * paper_N
            for c in [2, 3, 8]: v_95 += float(arr_05282[8, col_1995 + c]) * plastic_N
            for c in [2, 3, 8]: v_95 += float(arr_05282[11, col_1995 + c]) * wood_N
            for c in [2, 3, 8]: v_95 += float(arr_05282[12, col_1995 + c]) * textiles_N
            for c in [2]:      v_95 += float(arr_05282[13, col_1995 + c]) * wet_org_N
            for c in [2, 3, 8]: v_95 += float(arr_05282[16, col_1995 + c]) * other_mat_N
            for c in [2, 3, 8]: v_95 += float(arr_05282[17, col_1995 + c]) * hazardous_N
            value_1995 = v_95

        if waste_kt_1995 > 0 and value_1995 > 0:
            N_frac = value_1995 / waste_kt_1995
            value_1992 = waste_kt_1992 * N_frac
            change_per_year = (value_1995 - value_1992) / 3
            
            idx = 0
            for year in range(1990, 1995):
                value = value_1992 + change_per_year * idx
                idx += 1
                industry_waste[year] = value * noise_05282 * noise_trend
    except Exception:
        pass

    return industry_waste

    
def find_other_industry_wastewater(prepared_wastewater_dict, current_params):
    """
    MC-OPTIMALISERT: Beregner nitrogen i avløpsvann fra øvrig industri.
    Mottar en ferdigpreparert ordbok med basetall og legger på rundens støyfaktor.
    """
    year_values = {}
    
    # Hent rundens støyfaktor for 'norskeutslipp' (hvis tom, bruk 1.0 som fallback)
    noise_norskeutslipp = float(current_params.get('norskeutslipp', 1.0))
    
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


def find_recycling(data_05281, data_10513, data_hist_rec, current_params, 
                   household_waste, industry_waste, export_resirk, export_reuse):
    """
    MC-OPTIMALISERT: Beregner nitrogen til materialgjenvinning.
    Bruker ferdigpreparerte vektorer og rundens støyfaktorer for ekstrem fart.
    """
    year_values = {}
    
    # 1. Hent rundens støyfaktorer (avfallsfraksjoner og datasettmultiplikatorer)
    paper_N   = float(current_params.get('paper', 0.0))
    plastic_N = float(current_params.get('plastic', 0.0))
    wood_N    = float(current_params.get('wood', 0.0))
    textile_N = float(current_params.get('textiles', 0.0))
    other_N   = float(current_params.get('other_materials', 0.0))
    haz_N     = float(current_params.get('hazardous', 0.0))
    contam_N  = float(current_params.get('contaminated_masses', 0.0))
    rubber_N  = float(current_params.get('rubber', 0.0))
    mixed_N   = float(current_params.get('mixed_waste', 0.0))
    
    u_05281 = float(current_params.get('05281', 1.0))
    u_10513 = float(current_params.get('10513', 1.0))

    # 2. Beregn perioden 1995-2011 (vektorisert via NumPy)
    vals_05281 = (
        data_05281['paper'] * paper_N +
        data_05281['plastic'] * plastic_N +
        data_05281['wood'] * wood_N +
        data_05281['textile'] * textile_N +
        data_05281['other'] * other_N +
        data_05281['haz'] * haz_N +
        data_05281['contam'] * contam_N
    ) * u_05281
    
    value_1995 = 0.0
    for idx, year in enumerate(data_05281['years']):
        year_values[year] = float(vals_05281[idx])
        if year == 1995:
            value_1995 = float(vals_05281[idx])

    # 3. Beregn perioden 2012-2023 (vektorisert via NumPy)
    vals_10513 = (
        data_10513['wood'] * wood_N +
        data_10513['paper'] * paper_N +
        data_10513['plastic'] * plastic_N +
        data_10513['rubber'] * rubber_N +
        data_10513['textile'] * textile_N +
        data_10513['haz'] * haz_N +
        data_10513['mixed'] * mixed_N +
        data_10513['other'] * other_N +
        data_10513['contam'] * contam_N
    ) * u_10513
    
    for idx, year in enumerate(data_10513['years']):
        year_values[year] = float(vals_10513[idx])

    # 4. Beregn den historiske perioden 1990-1994 basert på 1995-tallene
    rec_frac_1985 = data_hist_rec['rec_frac_1985']
    change_per_year = data_hist_rec['change_per_year']
    
    rec_frac_1995 = rec_frac_1985 + change_per_year * (1995 - 1985)
    
    # Unngå ZeroDivisionError hvis summen i 1995 er 0
    denom = (household_waste.get(1995, 0.0) + industry_waste.get(1995, 0.0)) * rec_frac_1995
    N_frac = value_1995 / denom if denom != 0 else 0.0
    
    # Loop over historiske år
    for idx, year in enumerate(range(1990, 1995)):
        waste = household_waste.get(year, 0.0) + industry_waste.get(year, 0.0)
        if year < 1992:
            rec_frac = rec_frac_1985 + change_per_year * (year - 1985)
        else:
            rec_frac = data_hist_rec['fractions_92_94'][year - 1992]
            
        year_values[year] = waste * N_frac * rec_frac

    # 5. Trekk fra eksport for resirkulering og gjenbruk (som allerede er beregnet i loopen)
    for year in year_values:
        if year in export_resirk:
            year_values[year] -= export_resirk[year]
        if year in export_reuse:
            year_values[year] -= export_reuse[year]
            
    return year_values


def find_sewage_sludge_biogas(prepared_biogas_data, current_params):
    """
    MC-OPTIMALISERT: Beregner nitrogen i avløpsslam til biogass.
    Bruker ferdigpreparerte vektorer og rundens støyfaktorer.
    """
    year_values = {}
    
    # 1. Hent rundens unike støyfaktorer fra current_params
    sludge_N = float(current_params.get('sludge', 0.0))
    u_12359  = float(current_params.get('12359', 1.0))
    
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
    noise_trade = float(current_params.get('08801', current_params.get('13136', 1.0)))
    
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
        noise_ww = float(current_params.get('05280', 1.0))

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

