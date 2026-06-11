#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modifisert MC-VERSJON: Beregner nitrogenflyt for landbruk (AG).
Sikret full konsistens med sentral distribusjonstrekking i generate_mc_parameters_fast.
"""
import pandas as pd
import numpy as np
from calculations.utils import (
    EXPECTED_YEARS,
    read_year_value_row,
    fill_missing_with_mean,
    report_missing_years,
    load_crltap_emissions_to_N,
)
from calculations.shared_flow_calculations import (
    find_industrial_crop_products,
    find_non_edible_animal_products
    )

AG_SM_CRLTAP_SECTORS = [
    '3Da1','3Da2a','3Da2b','3Da2c','3Da3','3Da4',
    '3Db','3Dc','3De','3Df','4B1','4B2','4C1','4C2',
]

AG_MM_CRLTAP_SECTORS = [
    '3B1a','3B1b','3B2','3B3',
    '3B4a','3B4d','3B4e','3B4f',
    '3B4gi','3B4gii','3B4giii','3B4giv','3B4h',
]


def execute_calculations_ag(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    Hovedfunksjon for AG-poolen. Kjører alle underberegninger.
    Alle distribusjoner trekkes sentralt i main_mc før denne kjøres.
    """
    results = []
    
    # 1. Spesialstrømmer (Henter ferdig generert dataset_noise og parameterstøy)
    _add_food_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_industrial_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_fodder_crops_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_NH3_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise)
    _add_NOx_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise)
    _add_N2O_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise)
    _add_leaching_soil_management_mc(results, preloaded_data, current_params, dataset_noise)
    _add_leaching_manure_management_mc(results, preloaded_data, current_params, dataset_noise)
    _add_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_non_edible_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_manure_application_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_NH3_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise)
    _add_NOx_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise)
    _add_N2O_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise)
    _add_live_animal_export_mc(results, preloaded_data, current_params, dataset_noise)
    _add_N2_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise)
    
    # [Neste strømmer legges til fortløpende her...]
    
    return results


# =============================================================================
# SPESIALBEREGNINGER MED DATASETT- OG PARAMETERSTØY
# =============================================================================

def _add_food_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Food crop products.
    Henter ferdiginnlastet workbook fra RAM og påfører sentralt trukket datasetstøy.
    """
    flow_code = 'AG.SM-MP.FP-Food crop products-Nmix'
    collected_years = set()
    data_sources = 'Eurostat Gross nutrient balance'
    comment = 'ok (MC-støy lagt på basert på kildens usikkerhetstype)'

    # 1. Hent ferdiglastet workbook fra RAM (lagt inn via din oppdaterte data_loader)
    workbook = preloaded_data.get('ag_gnb_workbook')
    if workbook is None:
        print(f"[ADVARSEL] Mangler ag_gnb_workbook i preloaded_data for {flow_code}.")
        return

    # 2. Slå opp ferdig generert støy for dette datasettet fra dataset_noise
    dataset_key = 'Gross nutrient balance'
    has_noise = dataset_noise and dataset_key in dataset_noise
    
    noise_val = dataset_noise[dataset_key]['value'] if has_noise else 1.0
    noise_type = dataset_noise[dataset_key]['type'] if has_noise else 'perc'

    # --- Sheet 26: total crops ---
    sheet_26 = workbook['Sheet 26']  # nutrient removal by harvest of crops
    year_values = read_year_value_row(
        sheet_26,
        year_values=None,
        year_row=9,
        value_row=11,
        first_col=2,
        unit_factor=1.0e-3,
        op='+',
    )

    # --- Sheet 30: industrial crops (subtract) ---
    sheet_30 = workbook['Sheet 30']  # nutrient removal by harvest of industrial crops
    year_values = read_year_value_row(
        sheet_30,
        year_values=year_values,
        year_row=9,
        value_row=11,
        first_col=2,
        unit_factor=-1.0e-3,  # minus/trekk fra industrial crops
        op='+',
    )

    # 3. Skriv resultater og påfør asymmetrisk støy pr. år
    for year, total_value in year_values.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        # Påfør støyen matematisk korrekt ut fra om den er prosent eller absolutt
        if has_noise:
            if noise_type == 'perc':
                value = total_value * noise_val
            else:
                # Absolutt støy bruker grensene trukket fra den asymmetriske distribusjonen
                bound = dataset_noise[dataset_key]['upp_bound'] if noise_val >= 0 else dataset_noise[dataset_key]['low_bound']
                value = total_value + (noise_val * bound)
        else:
            value = total_value

        if value < 0: 
            value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources,
        })

    # 4. Fyll manglende år med gjennomsnitt basert på de *støy-påførte* verdiene
    # (eller basert på originale verdier og påfør støy etterpå, her gjør vi det på de ferdige verdiene)
    actual_values = [r['value'] for r in results if r['flow_name'] == flow_code]
    mean_value = np.mean(actual_values) if actual_values else 0.0
    
    # Siden fill_missing_with_mean forventer den originale ordboken, men vi allerede har støy-justert i results,
    # lager vi en midlertidig støyjustert dict for å fore den funksjonen
    perturbed_year_values = {r['year']: r['value'] for r in results if r['flow_name'] == flow_code}
    
    fill_missing_with_mean(
        flow_code, perturbed_year_values, collected_years, results,
        mean=mean_value,
        comment='interpolated (MC-støy lagt på)',
        data_sources='interpolated',
    )
    
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_industrial_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Crop products for industrial use.
    Henter pre-loadet tabell-struktur fra RAM og sender til felles hjelpefunksjon.
    """
    flow_code = 'AG.SM-MP.OP-Crop products for industrial use-Nmix'
    collected_years = set()
    data_sources = 'Eurostat Gross nutrient balance, Nutrient removal by harvest of industrial crops'

    # 1. Hent den ferdige DataFramen direkte fra RAM
    df_gnb_sheet30 = preloaded_data.get('gnb_sheet30_raw')
    if df_gnb_sheet30 is None:
        print(f"[ADVARSEL] Mangler gnb_sheet30_raw i preloaded_data for {flow_code}.")
        return

    # 2. Hent ferdig støyjusterte verdier fra den delte hjelpefunksjonen
    year_values = find_industrial_crop_products(df_gnb_sheet30, dataset_noise)

    # 3. Bygg resultat-strukturen for denne simuleringsrunden
    for year, value in year_values.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        comment = 'interpolated (MC-støy lagt på)' if year in range(2017, 2020) else 'ok (MC-støy lagt på)'
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
def _add_fodder_crops_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Fodder crops.
    Henter tre ferdiginnlastede DataFrames fra RAM og påfører sentralt trukket
    parameterstøy (N_content) og datasettstøy (asymmetrisk perc vs abs).
    """
    flow_code = 'AG.SM-AG.MM-Fodder crops-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på kildens usikkerhetstype)'

    # 1. Globale parametere (Allerede perturbert sentralt i generate_mc_parameters_fast)
    fodder_prot = float(current_params.get("fodder_protein_frac"))
    Jones = float(current_params.get("Jones_factor"))
    N_content = fodder_prot / Jones

    # 2. Hent og klargjør datasettstøy for de to SSB-kildene
    key_13648 = '13648'
    has_noise_13648 = dataset_noise and key_13648 in dataset_noise
    noise_13648_val = dataset_noise[key_13648]['value'] if has_noise_13648 else 1.0
    noise_13648_type = dataset_noise[key_13648]['type'] if has_noise_13648 else 'perc'

    key_05772 = '05772'
    has_noise_05772 = dataset_noise and key_05772 in dataset_noise
    noise_05772_val = dataset_noise[key_05772]['value'] if has_noise_05772 else 1.0
    noise_05772_type = dataset_noise[key_05772]['type'] if has_noise_05772 else 'perc'

    # =========================================================================
    # DEL A: SSB table 13648
    # =========================================================================
    df_13648 = preloaded_data.get('ssb_13648_raw')
    if df_13648 is not None:
        data_sources = 'SSB table 13648'
        # Excel: cell(row=4, column=col) -> df.iloc[3, col-1]
        for col_idx in range(1, 5):  # range(2, 6) i Excel blir indeks 1 til 4 i DataFrame
            year_val = df_13648.iloc[3, col_idx]
            val5 = df_13648.iloc[4, col_idx]  # Eng til slått
            val6 = df_13648.iloc[5, col_idx]  # Grøntfôr- og silovekstar
            
            if pd.notna(year_val) and pd.notna(val5) and pd.notna(val6):
                year = int(year_val)
                collected_years.add(year)
                
                base_value = (float(val5) + float(val6)) * N_content
                
                if has_noise_13648:
                    if noise_13648_type == 'perc':
                        value = base_value * noise_13648_val
                    else:
                        bound = dataset_noise[key_13648]['upp_bound'] if noise_13648_val >= 0 else dataset_noise[key_13648]['low_bound']
                        value = base_value + (noise_13648_val * bound)
                else:
                    value = base_value
                
                if value < 0: value = 0.0
                
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': float(value),
                    'comment': comment, 'data_sources': data_sources
                })

    # =========================================================================
    # DEL B: SSB table 05772
    # =========================================================================
    df_05772 = preloaded_data.get('ssb_05772_raw')
    if df_05772 is not None:
        data_sources = 'SSB table 05772'
        # Excel: cell(row=3, column=col) -> df.iloc[2, col-1]
        for col_idx in range(1, 22):  # range(2, 23) i Excel blir indeks 1 til 21
            year_val = df_05772.iloc[2, col_idx]
            val4 = df_05772.iloc[3, col_idx]  # Grøntfôr- og silovekstar
            val5 = df_05772.iloc[4, col_idx]  # Høy
            
            if pd.notna(year_val) and pd.notna(val4) and pd.notna(val5):
                year = int(year_val)
                collected_years.add(year)
                
                base_value = (float(val4) + float(val5)) * N_content
                
                if has_noise_05772:
                    if noise_05772_type == 'perc':
                        value = base_value * noise_05772_val
                    else:
                        bound = dataset_noise[key_05772]['upp_bound'] if noise_05772_val >= 0 else dataset_noise[key_05772]['low_bound']
                        value = base_value + (noise_05772_val * bound)
                else:
                    value = base_value
                
                if value < 0: value = 0.0
                
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': float(value),
                    'comment': comment, 'data_sources': data_sources
                })

    # =========================================================================
    # DEL C: Før 2000 (SSB Jordbruksstatistikk)
    # =========================================================================
    df_old = preloaded_data.get('grovfor_old_raw')
    if df_old is not None:
        data_sources = 'SSB Jordbruksstatistikk'
        # Excel: cell(row=r, column=1) -> df.iloc[r-1, 0]
        for r_idx in range(2, 18):  # range(3, 19) i Excel blir indeks 2 til 17
            year_val = df_old.iloc[r_idx, 0]
            val2 = df_old.iloc[r_idx, 1]  # Grøntfôr- og silovekstar
            val3 = df_old.iloc[r_idx, 2]  # Høy
            
            if pd.notna(year_val) and pd.notna(val2) and pd.notna(val3):
                year = int(year_val)
                collected_years.add(year)
                
                base_value = (float(val2) + float(val3)) * N_content
                
                if has_noise_05772:
                    if noise_05772_type == 'perc':
                        value = base_value * noise_05772_val
                    else:
                        bound = dataset_noise[key_05772]['upp_bound'] if noise_05772_val >= 0 else dataset_noise[key_05772]['low_bound']
                        value = base_value + (noise_05772_val * bound)
                else:
                    value = base_value
                
                if value < 0: value = 0.0
                
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': float(value),
                    'comment': comment, 'data_sources': data_sources
                })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_NH3_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    conv = float(current_params.get("NH3_to_N_factor"))
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    
    if raw_lines is None:
        print(f"[ADVARSEL] Mangler ag_crltap_raw_lines i preloaded_data for {flow_code}.")
        return

    # Kall den oppdaterte hjelpefunksjonen
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=AG_SM_CRLTAP_SECTORS,
        pollutant='NH3',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': float(value),
            'comment': comment, 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_NOx_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    conv = float(current_params.get("NOx_to_N_factor"))
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    
    if raw_lines is None:
        print(f"[ADVARSEL] Mangler ag_crltap_raw_lines i preloaded_data for {flow_code}.")
        return

    # Kall den oppdaterte hjelpefunksjonen
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=AG_SM_CRLTAP_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': float(value),
            'comment': comment, 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_N2O_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'UNFCCC CRT'

    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    
    key_n2o = 'UNFCCC_emissions'
    has_noise = dataset_noise and key_n2o in dataset_noise
    noise_val = dataset_noise[key_n2o]['value'] if has_noise else 1.0
    noise_type = dataset_noise[key_n2o]['type'] if has_noise else 'perc'

    df_unfccc = preloaded_data.get('unfccc_ark1_raw')
    if df_unfccc is None:
        print(f"[ADVARSEL] Mangler unfccc_ark1_raw i preloaded_data for {flow_code}.")
        return

    for r_idx in range(4, 37):
        year_val = df_unfccc.iloc[r_idx, 0]
        ton_val = df_unfccc.iloc[r_idx, 2]

        if pd.notna(year_val) and pd.notna(ton_val):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)

            base_value = float(ton_val) * conv_N2O

            if has_noise:
                if noise_type == 'perc':
                    value = base_value * noise_val
                else:
                    bound = dataset_noise[key_n2o]['upp_bound'] if noise_val >= 0 else dataset_noise[key_n2o]['low_bound']
                    value = base_value + (noise_val * bound)
            else:
                value = base_value

            if value < 0: value = 0.0

            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(value),
                'comment': comment, 'data_sources': data_sources
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_leaching_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-HY.SW-Leaching-Nmix'
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    comment = 'ok (MC-støy lagt på)'

    # 1. Hent asymmetrisk datasettstøy
    key_leach = 'UNFCCC_emissions'
    has_noise = dataset_noise and key_leach in dataset_noise
    noise_val = dataset_noise[key_leach]['value'] if has_noise else 1.0
    noise_type = dataset_noise[key_leach]['type'] if has_noise else 'perc'

    # 2. Hent ferdiglastet DataFrame fra RAM
    df_leaching = preloaded_data.get('ag_leaching_csv')
    if df_leaching is None:
        print(f"[ADVARSEL] Mangler ag_leaching_csv i preloaded_data for {flow_code}.")
        return

    # 3. Kjapp iterasjon over array-verdier i stedet for .iterrows()
    years = df_leaching['year'].values
    values_sm = df_leaching['Nr_SM'].values

    for i in range(len(years)):
        year = int(years[i])
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        base_value = float(values_sm[i])

        # Påfør asymmetrisk støy robust
        if has_noise:
            if noise_type == 'perc':
                value = base_value * noise_val
            else:
                bound = dataset_noise[key_leach]['upp_bound'] if noise_val >= 0 else dataset_noise[key_leach]['low_bound']
                value = base_value + (noise_val * bound)
        else:
            value = base_value

        if value < 0: value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources,
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_leaching_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.MM-HY.SW-Leaching-Nmix'
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    comment = 'ok (MC-støy lagt på)'

    # 1. Hent asymmetrisk datasettstøy
    key_leach = 'UNFCCC_emissions'
    has_noise = dataset_noise and key_leach in dataset_noise
    noise_val = dataset_noise[key_leach]['value'] if has_noise else 1.0
    noise_type = dataset_noise[key_leach]['type'] if has_noise else 'perc'

    # 2. Hent ferdiglastet DataFrame fra RAM
    df_leaching = preloaded_data.get('ag_leaching_csv')
    if df_leaching is None:
        print(f"[ADVARSEL] Mangler ag_leaching_csv i preloaded_data for {flow_code}.")
        return

    # 3. Kjapp iterasjon over array-verdier i stedet for .iterrows()
    years = df_leaching['year'].values
    values_mm = df_leaching['Nr_MM'].values

    for i in range(len(years)):
        year = int(years[i])
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        base_value = float(values_mm[i])

        # Påfør asymmetrisk støy robust
        if has_noise:
            if noise_type == 'perc':
                value = base_value * noise_val
            else:
                bound = dataset_noise[key_leach]['upp_bound'] if noise_val >= 0 else dataset_noise[key_leach]['low_bound']
                value = base_value + (noise_val * bound)
        else:
            value = base_value

        if value < 0: value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources,
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Animal products flow.
    Bruker ferdigfiltrerte FAOSTAT-data fra RAM. Mapper inn unikt støybelagte 
    N-faktorer direkte fra de flate parameterne i current_params (f.eks. 'prod_Milk').
    
    Krasjer med KeyError dersom et produkt mangler i parametergrunnlaget.
    """
    flow_code = 'AG.MM-MP.FP-Animal products-Nmix'
    collected_years = set()
    data_sources = 'FAOSTAT Crops and livestock products'
    comment = 'ok (MC-støy lagt på unikt per produkt)'

    # 1. Hent den ferdig slankenede tabellen fra RAM
    df_fao = preloaded_data.get('fao_animal_production_clean')
    if df_fao is None:
        print(f"[ADVARSEL] Mangler fao_animal_production_clean i preloaded_data for {flow_code}.")
        return

    # 2. Hent datasettstøy for FAOSTAT (Crops and livestock products)
    key_fao = 'Crops and livestock products'
    has_noise = dataset_noise and key_fao in dataset_noise
    noise_val = dataset_noise[key_fao]['value'] if has_noise else 1.0
    noise_type = dataset_noise[key_fao]['type'] if has_noise else 'perc'
    
    # 3. Slå opp den flate, perturberte N-prosenten (Krasjer hardt ved manglende data)
    def get_perturbed_product_frac(item_name):
        param_key = f"prod_{str(item_name).strip()}"
        
        # Siden current_params er et NParameters-objekt, må vi bruke .get()
        # Vi setter default=None for å fange opp om den faktisk mangler.
        val = current_params.get(param_key)
        
        if val is None:
            raise KeyError(
                f"[KRITISK FEIL] Produktet '{item_name}' ble funnet i FAOSTAT-dataene, "
                f"men parameteren '{param_key}' mangler i N_parameters.xlsx (eller ble ikke generert i main_mc.py)!"
            )
            
        return float(val)
    # 4. Beregn N-mengder vektorisert med .apply()
    working_df = df_fao.copy()
    working_df['N_content_percent'] = working_df['Item'].apply(get_perturbed_product_frac)
    
    # Verdi (tonn produkt) * N_content_percent / 1e5 = kt N
    working_df['N_amount_kt'] = working_df['Value'] * working_df['N_content_percent'] / 1.0e5

    # 5. Aggreger per år
    total_N_per_year = working_df.groupby('Year')['N_amount_kt'].sum().to_dict()

    # 6. Bygg resultatstrukturen for de forventede årene
    for year in EXPECTED_YEARS:
        if year in total_N_per_year:
            collected_years.add(year)
            base_value = float(total_N_per_year[year])
            
            # Påfør asymmetrisk datasettstøy
            if has_noise:
                if noise_type == 'perc':
                    value = base_value * noise_val
                else:
                    bound = dataset_noise[key_fao]['upp_bound'] if noise_val >= 0 else dataset_noise[key_fao]['low_bound']
                    value = base_value + (noise_val * bound)
            else:
                value = base_value

            if value < 0: value = 0.0

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value),
                'comment': comment,
                'data_sources': data_sources
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
def _add_non_edible_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Non-edible animal products flow.
    """
    flow_code = 'AG.MM-MP.OP-Non-edible animal products-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på parametere og kildedata)'

    # Hent ferdiglastede dataframes fra RAM
    df_hides_clean = preloaded_data.get('fao_hides_clean')
    df_wool = preloaded_data.get('wool_production')
    df_sheep = preloaded_data.get('ssb_sheep_numbers')
    
    if df_hides_clean is None or df_wool is None or df_sheep is None:
        print(f"[ADVARSEL] Mangler preloaded datagrunnlag for {flow_code}. Hopper over flommen.")
        return

    # Kjør beregningen
    year_values = find_non_edible_animal_products(
        df_hides_clean, df_wool, df_sheep, current_params, dataset_noise
    )

    # Legg til i resultatlisten (antar at EXPECTED_YEARS er definert globalt, f.eks. range(1990, 2024))
    for year in range(1990, 2024):
        if year in year_values:
            collected_years.add(year)
            value = float(year_values[year])
            
            if value < 0: value = 0.0

            if year > 2004 and year != 2001:
                data_sources = 'FAOSTAT Crops and livestock products + Landbruksdirektoratet'
            elif year != 2001:
                data_sources = 'FAOSTAT Crops and livestock products + Landbruksdirektoratet + SSB, extrapolated'
            else:
                data_sources = 'FAOSTAT Crops and livestock products'

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': value,
                'comment': comment,
                'data_sources': data_sources
            })

    # Hvis du har en definert mengde forventede år (f.eks. EXPECTED_YEARS = set(range(1990, 2024)))
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_manure_application_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Manure application flow (AG.MM-AG.SM-Manure application-Nmix).
    Henter data fra ferdiglastet Eurostat GNB Sheet 12, gjør lineær interpolasjon
    for 2017-2019, og påfører asymmetrisk datasettstøy.
    """
    flow_code = 'AG.MM-AG.SM-Manure application-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på datasett)'
    
    # 1. Hent rådata-matrisen fra RAM
    df_sheet12 = preloaded_data.get('gnb_sheet12_raw')
    if df_sheet12 is None:
        print(f"[ADVARSEL] Mangler 'gnb_sheet12_raw' i preloaded_data. Hopper over {flow_code}.")
        return

    # 2. Hent ut den asymmetriske datasettstøyen fra denne iterasjonen
    has_gnb = dataset_noise and 'Gross nutrient balance' in dataset_noise
    noise_gnb = dataset_noise['Gross nutrient balance']['value'] if has_gnb else 1.0

    has_interp = dataset_noise and 'trend interpolation' in dataset_noise
    noise_interp = dataset_noise['trend interpolation']['value'] if has_interp else 1.0

    # 3. Rekonstruer read_year_value_row logikken for en ren DataFrame
    # Original: year_row=9 (indeks 8), value_row=11 (indeks 10), first_col=2 (indeks 1)
    # Enhetsfaktor: 1.0e-3 (konverterer fra tonn til kilotonn)
    year_row_idx = 8
    value_row_idx = 10
    first_col_idx = 1
    unit_factor = 1.0e-3

    # Hent radene ut fra DataFramen
    years_row = df_sheet12.iloc[year_row_idx].values
    values_row = df_sheet12.iloc[value_row_idx].values

    year_values = {}
    # Loop over kolonnene fra first_col_idx til enden
    for col_idx in range(first_col_idx, len(years_row)):
        yr = years_row[col_idx]
        val = values_row[col_idx]
        
        # Sjekk at året er et gyldig tall/årstall
        try:
            yr = int(float(yr))
            # Sjekk om verdien er numerisk og ikke tom (None/NaN)
            if pd.notna(val) and val != '':
                year_values[yr] = float(val) * unit_factor
        except (ValueError, TypeError):
            continue

    # 4. Behandle dataene og legg til i resultatene
    value_2016 = None
    value_2020 = None
    reported_entries = []

    for year, base_value in year_values.items():
        if year not in EXPECTED_YEARS:
            continue
            
        collected_years.add(year)
        
        # Lagre referansepunkter for interpolasjonen
        if year == 2016:
            value_2016 = base_value
        elif year == 2020:
            value_2020 = base_value

        # Påfør datasettstøy for rapporterte data
        value = base_value * float(noise_gnb)
        if value < 0: value = 0.0

        reported_entries.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': 'Eurostat Gross nutrient balance, Manure input'
        })

    # Legg til de rapporterte årene i resultatlisten
    results.extend(reported_entries)

    # 5. Interpolering for 2017-2019 (hvis vi har 2016 og 2020 tilgjengelig)
    if value_2016 is not None and value_2020 is not None:
        for year in range(2017, 2020):
            if year in EXPECTED_YEARS:
                collected_years.add(year)
                
                # Lineær interpolasjon på de u-støyede basistallene
                base_interp_val = value_2016 + (value_2020 - value_2016) / 4.0 * (year - 2016)
                
                # Påfør både GNB-støy og trend/interpolasjonsstøy harmonisert
                value = base_interp_val * float(noise_gnb) * float(noise_interp)
                if value < 0: value = 0.0

                results.append({
                    'flow_name': flow_code,
                    'year': year,
                    'value': float(value),
                    'comment': comment,
                    'data_sources': 'interpolated'
                })
    else:
        print(f"[ADVARSEL] Kunne ikke interpolere 2017-2019 for {flow_code} fordi data for 2016 eller 2020 mangler.")

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_NH3_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    """MC-VERSJON: AG.MM-AT.AT-Emissions-NH3"""
    flow_code = 'AG.MM-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    conv = float(current_params.get("NH3_to_N_factor"))
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    
    if raw_lines is None:
        print(f"[ADVARSEL] Mangler ag_crltap_raw_lines i preloaded_data for {flow_code}.")
        return

    # Kall hjelpefunksjonen med AG_MM_CRLTAP_SECTORS i stedet for AG_SM
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=AG_MM_CRLTAP_SECTORS,
        pollutant='NH3',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': float(value),
            'comment': comment, 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_NOx_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    """MC-VERSJON: AG.MM-AT.AT-Emissions-NOx"""
    flow_code = 'AG.MM-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    conv = float(current_params.get("NOx_to_N_factor"))
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    
    if raw_lines is None:
        print(f"[ADVARSEL] Mangler ag_crltap_raw_lines i preloaded_data for {flow_code}.")
        return

    # Kall hjelpefunksjonen med AG_MM_CRLTAP_SECTORS i stedet for AG_SM
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=AG_MM_CRLTAP_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': float(value),
            'comment': comment, 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_N2O_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    """MC-VERSJON: AG.MM-AT.AT-Emissions-N2O"""
    flow_code = 'AG.MM-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'UNFCCC CRT'

    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    
    key_n2o = 'UNFCCC_emissions'
    has_noise = dataset_noise and key_n2o in dataset_noise
    noise_val = dataset_noise[key_n2o]['value'] if has_noise else 1.0
    noise_type = dataset_noise[key_n2o]['type'] if has_noise else 'perc'

    df_unfccc = preloaded_data.get('unfccc_ark1_raw')
    if df_unfccc is None:
        print(f"[ADVARSEL] Mangler unfccc_ark1_raw i preloaded_data for {flow_code}.")
        return

    for r_idx in range(4, 37):
        year_val = df_unfccc.iloc[r_idx, 0]
        ton_val = df_unfccc.iloc[r_idx, 1]  # ENDRET FRA 2 TIL 1: Rad 1 inneholder verdien for Manure Management

        if pd.notna(year_val) and pd.notna(ton_val):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)

            base_value = float(ton_val) * conv_N2O

            if has_noise:
                if noise_type == 'perc':
                    value = base_value * noise_val
                else:
                    bound = dataset_noise[key_n2o]['upp_bound'] if noise_val >= 0 else dataset_noise[key_n2o]['low_bound']
                    value = base_value + (noise_val * bound)
            else:
                value = base_value

            if value < 0: value = 0.0

            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(value),
                'comment': comment, 'data_sources': data_sources
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_live_animal_export_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Eksport av levende dyr (AG.MM-RW.RW-Live animal export-Nmix).
    Slår opp ferdig perturberte vekter ('weight_HORSES' osv.) fra parametergeneratoren.
    Ingen tunge fil-I/O eller .join()-operasjoner her.
    """
    flow_code = 'AG.MM-RW.RW-Live animal export-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy ferdig beregnet sentralt)'
    data_sources = 'FAOSTAT Crops and livestock products'
    
    # Hent ferdiglastet eksport-DataFrame fra RAM
    final_data = preloaded_data.get('fao_live_animals_export')
    if final_data is None:
        print(f"[ADVARSEL] Mangler fao_live_animals_export i preloaded_data for {flow_code}.")
        return

    # Hent globale perturberte parametere
    prot_frac = float(current_params.get("live_animal_protein_frac"))
    prot_to_N = float(current_params.get("Jones_factor"))

    # Hent asymmetrisk kildestøy
    key_fao = 'Crops and livestock products'
    has_noise_fao = dataset_noise and key_fao in dataset_noise
    noise_fao = dataset_noise[key_fao]['value'] if has_noise_fao else 1.0

    df_round = final_data.copy()
    if has_noise_fao and dataset_noise[key_fao]['type'] == 'perc':
        df_round['perturbed_value'] = df_round['Value'] * noise_fao
    else:
        df_round['perturbed_value'] = df_round['Value']

    # Hjelpefunksjon for å hente de ferdig perturberte enkeltvektene per dyretype
    def get_perturbed_weight(item_name):
        clean_item = str(item_name).strip()
        param_key = f"weight_{clean_item}"
        
        # Hent den rå ordboken fra objektet for å se om denne dyretypen i det hele tatt er definert i modellen din
        defined_weights = getattr(current_params, 'animal_weights', {})
        
        # Hvis dyretypen ikke finnes i Excel-arket 'animal_weights', ignorerer vi den ved å returnere 0.0
        if clean_item not in defined_weights:
            return 0.0
            
        # Hvis den derimot SKAL være der, bruker vi det vanlige oppslaget.
        # Siden vi har fjernet fallbacks i get(), vil dette krasje hardt og riktig 
        # dersom parameteren ble borte under Monte Carlo-genereringen.
        return float(current_params.get(param_key))
    
    # Beregn N-mengde per rad
    df_round['perturbed_weight'] = df_round['Item'].apply(get_perturbed_weight)
    df_round['N_amount'] = (df_round['perturbed_weight'] * df_round['perturbed_value'] * prot_frac * 1e-6 / prot_to_N)

    # Aggreger per år til en kjapp ordbok
    total_N_per_year = df_round.groupby('Year')['N_amount'].sum().to_dict()
    
    # Fyll ut for de forventede årstallene
    for year in sorted(EXPECTED_YEARS):
        if year in total_N_per_year:
            collected_years.add(year)
            val = total_N_per_year[year]
            if val < 0: val = 0.0
            
            results.append({
                'flow_name': flow_code, 
                'year': year, 
                'value': float(val),
                'comment': comment, 
                'data_sources': data_sources
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_N2_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Dinitrogen-utslipp fra jordforvaltning (AG.SM-AT.AT-Emissions-N2).
    Bruker ferdig perturbert verdi for denitrifikasjon direkte fra current_params.
    """
    flow_code = 'AG.SM-AT.AT-Emissions-N2'
    collected_years = set()
    comment = 'ok (MC-støy lagt på global parameter)'
    data_sources = 'Schäppi2025Ann + NIBIO'
    
    # Hent den ferdig perturberte parameterverdien fra denne MC-runden
    # Fallback settes til f.eks. 16.0 ktN/år basert på kildekommentaren din
    value = float(current_params.get("denitrification_AG_N2"))
    
    if value < 0: 
        value = 0.0

    # Fyll ut verdien konstant for alle forventede årstall
    for year in sorted(EXPECTED_YEARS):
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,  
            'comment': comment,
            'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)