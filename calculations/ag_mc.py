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
    Henter ferdiginnlastet workbook fra RAM, gjør lineær interpolasjon for 
    datagapet i 2017-2019, og påfører sentralt trukket datasetstøy.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'AG.SM-MP.FP-Food crop products-Nmix'
    collected_years = set()
    data_sources = 'Eurostat Gross nutrient balance'
    comment = 'ok (MC-støy lagt på)'

    # 1. Hent ferdiglastet workbook fra RAM – krasj hvis den mangler
    workbook = preloaded_data.get('ag_gnb_workbook')
    if workbook is None:
        raise ValueError(f"[KRITISK] 'ag_gnb_workbook' mangler i preloaded_data for {flow_code}!")

    # 2. Slå opp ferdig generert støy – krasj hvis nøklene mangler
    dataset_key = 'Gross nutrient balance'
    if not dataset_noise or dataset_key not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{dataset_key}' mangler i dataset_noise for {flow_code}!")
        
    noise_val = dataset_noise[dataset_key]['value']
    noise_type = dataset_noise[dataset_key]['type']

    key_interp = 'trend interpolation'
    if key_interp not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_interp}' mangler i dataset_noise for {flow_code}!")
    noise_interp_val = dataset_noise[key_interp]['value']
    noise_interp_type = dataset_noise[key_interp]['type']

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

    # 3. Hent ut u-støyede basistall for interpolasjons-ankere
    value_2016 = year_values.get(2016)
    value_2020 = year_values.get(2020)

    # 4. Skriv resultater for rapporterte år og påfør asymmetrisk støy
    for year, total_value in year_values.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        # Påfør støyen matematisk korrekt basert på støytype
        if noise_type == 'perc':
            value = total_value * noise_val
        else:
            bound = dataset_noise[dataset_key]['upp_bound'] if noise_val >= 0 else dataset_noise[dataset_key]['low_bound']
            value = total_value + (noise_val * bound)
        if value < 0: 
            value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources,
        })

    # 5. Interpolering for datagapet 2017-2019 (krasj hardt hvis ankere mangler)
    if value_2016 is None or value_2020 is None:
        raise ValueError(
            f"[KRITISK] Kunne ikke interpolere 2017-2019 for {flow_code} "
            f"fordi basistall for enten 2016 ({value_2016}) eller 2020 ({value_2020}) mangler i GNB workbook!"
        )

    for year in range(2017, 2020):
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            
            # Lineær interpolasjon på de rene basistallene (vekt 1/4 per år fra 2016)
            base_interp_val = value_2016 + (value_2020 - value_2016) / 4.0 * (year - 2016)
            
            # Påfør først den generelle GNB-støyen
            if noise_type == 'perc':
                val_with_gnb = base_interp_val * noise_val
            else:
                bound_gnb = dataset_noise[dataset_key]['upp_bound'] if noise_val >= 0 else dataset_noise[dataset_key]['low_bound']
                val_with_gnb = base_interp_val + (noise_val * bound_gnb)

            # Påfør deretter trend/interpolasjonsstøy harmonisert
            if noise_interp_type == 'perc':
                value = val_with_gnb * noise_interp_val
            else:
                bound_interp = dataset_noise[key_interp]['upp_bound'] if noise_interp_val >= 0 else dataset_noise[key_interp]['low_bound']
                value = val_with_gnb + (noise_interp_val * bound_interp)

            if value < 0: 
                value = 0.0

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value),
                'comment': 'interpolated (MC-støy lagt på)',
                'data_sources': 'interpolated (Eurostat GNB gap)'
            })

    # 6. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_industrial_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Crop products for industrial use.
    Henter pre-loadet tabell-struktur fra RAM og sender til felles hjelpefunksjon.
    Krasjer umiddelbart ved manglende rådata eller støy-konfigurasjon.
    """
    flow_code = 'AG.SM-MP.OP-Crop products for industrial use-Nmix'
    collected_years = set()
    data_sources = 'Eurostat Gross nutrient balance, Nutrient removal by harvest of industrial crops'
    comment = 'ok (MC-støy lagt på)'

    # 1. Hent den ferdige DataFramen direkte fra RAM - krasj hvis den mangler
    df_gnb_sheet30 = preloaded_data.get('gnb_sheet30_raw')
    if df_gnb_sheet30 is None:
        raise ValueError(f"[KRITISK] 'gnb_sheet30_raw' mangler i preloaded_data for {flow_code}!")

    # 2. Hent støyjusterte verdier fra hjelpefunksjonen
    # MERK: Sørg for at find_industrial_crop_products() kaster KeyError hvis støy mangler!
    year_values = find_industrial_crop_products(df_gnb_sheet30, dataset_noise)

    # 3. Bygg resultat-strukturen for denne simuleringsrunden
    for year, value in year_values.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        # Siden vi kjører ren MC uten fallback/skjult interpolering, 
        # bruker vi en ren og konsistent kommentar.
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources
        })

    # 4. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_fodder_crops_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Fodder crops.
    Henter tre ferdiginnlastede DataFrames fra RAM og påfører sentralt trukket
    parameterstøy (N_content) og datasettstøy.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'AG.SM-AG.MM-Fodder crops-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'

    # 1. Globale parametere (Allerede perturbert sentralt)
    fodder_prot = float(current_params.get("fodder_protein_frac"))
    Jones = float(current_params.get("Jones_factor"))
    N_content = fodder_prot / Jones

    # 2. Hent og valider datasettstøy for SSB-kildene – krasj hvis nøkler mangler
    key_13648 = '13648'
    if not dataset_noise or key_13648 not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_13648}' mangler i dataset_noise for {flow_code}!")
    noise_13648_val = dataset_noise[key_13648]['value']
    noise_13648_type = dataset_noise[key_13648]['type']

    key_05772 = '05772'
    if not dataset_noise or key_05772 not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_05772}' mangler i dataset_noise for {flow_code}!")
    noise_05772_val = dataset_noise[key_05772]['value']
    noise_05772_type = dataset_noise[key_05772]['type']

    # 3. Hent og valider at alle rådata-filer eksisterer i RAM
    df_13648 = preloaded_data.get('ssb_13648_raw')
    df_05772 = preloaded_data.get('ssb_05772_raw')
    df_old = preloaded_data.get('grovfor_old_raw')

    if df_13648 is None:
        raise ValueError(f"[KRITISK] 'ssb_13648_raw' mangler i preloaded_data for {flow_code}!")
    if df_05772 is None:
        raise ValueError(f"[KRITISK] 'ssb_05772_raw' mangler i preloaded_data for {flow_code}!")
    if df_old is None:
        raise ValueError(f"[KRITISK] 'grovfor_old_raw' mangler i preloaded_data for {flow_code}!")

    # =========================================================================
    # DEL A: SSB table 13648
    # =========================================================================
    data_sources_A = 'SSB table 13648'
    for col_idx in range(1, 5):
        year_val = df_13648.iloc[3, col_idx]
        val5 = df_13648.iloc[4, col_idx]  # Eng til slått
        val6 = df_13648.iloc[5, col_idx]  # Grøntfôr- og silovekstar
        
        if pd.notna(year_val) and pd.notna(val5) and pd.notna(val6):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            
            base_value = (float(val5) + float(val6)) * N_content
            
            if noise_13648_type == 'perc':
                value = base_value * noise_13648_val
            else:
                bound = dataset_noise[key_13648]['upp_bound'] if noise_13648_val >= 0 else dataset_noise[key_13648]['low_bound']
                value = base_value + (noise_13648_val * bound)
            
            if value < 0: value = 0.0
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(value),
                'comment': comment, 'data_sources': data_sources_A
            })

    # =========================================================================
    # DEL B: SSB table 05772
    # =========================================================================
    data_sources_B = 'SSB table 05772'
    for col_idx in range(1, 22):
        year_val = df_05772.iloc[2, col_idx]
        val4 = df_05772.iloc[3, col_idx]  # Grøntfôr- og silovekstar
        val5 = df_05772.iloc[4, col_idx]  # Høy
        
        if pd.notna(year_val) and pd.notna(val4) and pd.notna(val5):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            
            base_value = (float(val4) + float(val5)) * N_content
            
            if noise_05772_type == 'perc':
                value = base_value * noise_05772_val
            else:
                bound = dataset_noise[key_05772]['upp_bound'] if noise_05772_val >= 0 else dataset_noise[key_05772]['low_bound']
                value = base_value + (noise_05772_val * bound)
            
            if value < 0: value = 0.0
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(value),
                'comment': comment, 'data_sources': data_sources_B
            })

    # =========================================================================
    # DEL C: Før 2000 (SSB Jordbruksstatistikk)
    # =========================================================================
    data_sources_C = 'SSB Jordbruksstatistikk'
    for r_idx in range(2, 18):
        year_val = df_old.iloc[r_idx, 0]
        val2 = df_old.iloc[r_idx, 1]  # Grøntfôr- og silovekstar
        val3 = df_old.iloc[r_idx, 2]  # Høy
        
        if pd.notna(year_val) and pd.notna(val2) and pd.notna(val3):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            
            base_value = (float(val2) + float(val3)) * N_content
            
            # Bruker samme støykonfigurasjon for historisk data som for 05772
            if noise_05772_type == 'perc':
                value = base_value * noise_05772_val
            else:
                bound = dataset_noise[key_05772]['upp_bound'] if noise_05772_val >= 0 else dataset_noise[key_05772]['low_bound']
                value = base_value + (noise_05772_val * bound)
            
            if value < 0: value = 0.0
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(value),
                'comment': comment, 'data_sources': data_sources_C
            })

    # 4. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    

def _add_NH3_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: NH3 emissions from soil management.
    Henter rådata fra RAM og beregner utslipp med påført datasetstøy via felles hjelpefunksjon.
    Krasjer umiddelbart hvis data mangler.
    """
    flow_code = 'AG.SM-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    # 1. Hent og valider globale parametere
    conv = float(current_params.get("NH3_to_N_factor"))
    
    # 2. Hent rådata fra RAM – krasj hardt hvis de mangler
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    if raw_lines is None:
        raise ValueError(f"[KRITISK] 'ag_crltap_raw_lines' mangler i preloaded_data for {flow_code}!")

    # 3. Kall hjelpefunksjonen som beregner summer og påfører støy
    # MERK: Sørg for at load_crltap_emissions_to_N kaster KeyError hvis 'CRLTAP' mangler i dataset_noise!
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=AG_SM_CRLTAP_SECTORS,
        pollutant='NH3',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    # 4. Bygg resultatstrukturen
    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })

    # 5. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_NOx_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: NOx emissions from soil management.
    Henter rådata fra RAM og beregner utslipp med påført datasetstøy via felles hjelpefunksjon.
    Krasjer umiddelbart hvis data mangler.
    """
    flow_code = 'AG.SM-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    # 1. Hent og valider globale parametere
    conv = float(current_params.get("NOx_to_N_factor"))
    
    # 2. Hent rådata fra RAM – krasj hardt hvis de mangler
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    if raw_lines is None:
        raise ValueError(f"[KRITISK] 'ag_crltap_raw_lines' mangler i preloaded_data for {flow_code}!")

    # 3. Kall hjelpefunksjonen som beregner summer og påfører støy
    # MERK: Sørg for at load_crltap_emissions_to_N kaster KeyError hvis 'CRLTAP' mangler i dataset_noise!
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=AG_SM_CRLTAP_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    # 4. Bygg resultatstrukturen
    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })

    # 5. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_N2O_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: N2O emissions from soil management.
    Henter rådata fra RAM og påfører sentralt trukket datasetstøy.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'AG.SM-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'UNFCCC CRT'

    # 1. Hent og valider globale parametere
    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    
    # 2. Slå opp ferdig generert støy – krasj hvis nøkkelen mangler
    key_n2o = 'UNFCCC_emissions'
    if not dataset_noise or key_n2o not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_n2o}' mangler i dataset_noise for {flow_code}!")
    
    noise_val = dataset_noise[key_n2o]['value']
    noise_type = dataset_noise[key_n2o]['type']

    # 3. Hent ferdiglastet DataFrame fra RAM – krasj hardt hvis den mangler
    df_unfccc = preloaded_data.get('unfccc_ark1_raw')
    if df_unfccc is None:
        raise ValueError(f"[KRITISK] 'unfccc_ark1_raw' mangler i preloaded_data for {flow_code}!")

    # 4. Gå gjennom radene og beregn verdier med støy
    for r_idx in range(4, 37):
        year_val = df_unfccc.iloc[r_idx, 0]
        ton_val = df_unfccc.iloc[r_idx, 2]

        if pd.notna(year_val) and pd.notna(ton_val):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)

            base_value = float(ton_val) * conv_N2O

            # Påfør støyen matematisk korrekt basert på støytype
            if noise_type == 'perc':
                value = base_value * noise_val
            else:
                # Absolutt støy bruker grensene trukket fra den asymmetriske distribusjonen
                bound = dataset_noise[key_n2o]['upp_bound'] if noise_val >= 0 else dataset_noise[key_n2o]['low_bound']
                value = base_value + (noise_val * bound)

            if value < 0: 
                value = 0.0

            results.append({
                'flow_name': flow_code, 
                'year': year, 
                'value': float(value),
                'comment': comment, 
                'data_sources': data_sources
            })

    # 5. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_leaching_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Leaching from soil management.
    Henter pre-loadet CSV-data fra RAM og påfører sentralt trukket datasetstøy.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'AG.SM-HY.SW-Leaching-Nmix'
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    comment = 'ok (MC-støy lagt på)'

    # 1. Slå opp ferdig generert støy – krasj hvis nøkkelen mangler
    key_leach = 'UNFCCC_emissions'
    if not dataset_noise or key_leach not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_leach}' mangler i dataset_noise for {flow_code}!")
        
    noise_val = dataset_noise[key_leach]['value']
    noise_type = dataset_noise[key_leach]['type']

    # 2. Hent ferdiglastet DataFrame fra RAM – krasj hardt hvis den mangler
    df_leaching = preloaded_data.get('ag_leaching_csv')
    if df_leaching is None:
        raise ValueError(f"[KRITISK] 'ag_leaching_csv' mangler i preloaded_data for {flow_code}!")

    # 3. Kjapp iterasjon over array-verdier i stedet for .iterrows()
    years = df_leaching['year'].values
    values_sm = df_leaching['Nr_SM'].values

    for i in range(len(years)):
        year = int(years[i])
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        base_value = float(values_sm[i])

        # Påfør asymmetrisk støy matematisk korrekt ut fra støytype
        if noise_type == 'perc':
            value = base_value * noise_val
        else:
            # Absolutt støy bruker grensene trukket fra den asymmetriske distribusjonen
            bound = dataset_noise[key_leach]['upp_bound'] if noise_val >= 0 else dataset_noise[key_leach]['low_bound']
            value = base_value + (noise_val * bound)

        if value < 0: 
            value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources,
        })

    # 4. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_leaching_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Leaching from manure management.
    Henter pre-loadet CSV-data fra RAM og påfører sentralt trukket datasetstøy.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'AG.MM-HY.SW-Leaching-Nmix'
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    comment = 'ok (MC-støy lagt på)'

    # 1. Slå opp ferdig generert støy – krasj hvis nøkkelen mangler
    key_leach = 'UNFCCC_emissions'
    if not dataset_noise or key_leach not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_leach}' mangler i dataset_noise for {flow_code}!")
        
    noise_val = dataset_noise[key_leach]['value']
    noise_type = dataset_noise[key_leach]['type']

    # 2. Hent ferdiglastet DataFrame fra RAM – krasj hardt hvis den mangler
    df_leaching = preloaded_data.get('ag_leaching_csv')
    if df_leaching is None:
        raise ValueError(f"[KRITISK] 'ag_leaching_csv' mangler i preloaded_data for {flow_code}!")

    # 3. Kjapp iterasjon over array-verdier i stedet for .iterrows()
    years = df_leaching['year'].values
    values_mm = df_leaching['Nr_MM'].values

    for i in range(len(years)):
        year = int(years[i])
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        base_value = float(values_mm[i])

        # Påfør asymmetrisk støy matematisk korrekt ut fra støytype
        if noise_type == 'perc':
            value = base_value * noise_val
        else:
            # Absolutt støy bruker grensene trukket fra den asymmetriske distribusjonen
            bound = dataset_noise[key_leach]['upp_bound'] if noise_val >= 0 else dataset_noise[key_leach]['low_bound']
            value = base_value + (noise_val * bound)

        if value < 0: 
            value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources,
        })

    # 4. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Animal products flow.
    Bruker ferdigfiltrerte FAOSTAT-data fra RAM. Mapper inn unikt støybelagte 
    N-faktorer direkte fra de flate parameterne i current_params (f.eks. 'prod_Milk').
    
    Krasjer umiddelbart dersom data, parametere eller støy-konfigurasjon mangler.
    """
    flow_code = 'AG.MM-MP.FP-Animal products-Nmix'
    collected_years = set()
    data_sources = 'FAOSTAT Crops and livestock products'
    comment = 'ok (MC-støy lagt på unikt per produkt)'

    # 1. Hent den ferdig slankede tabellen fra RAM - krasj hardt hvis den mangler
    df_fao = preloaded_data.get('fao_animal_production_clean')
    if df_fao is None:
        raise ValueError(f"[KRITISK] 'fao_animal_production_clean' mangler i preloaded_data for {flow_code}!")

    # 2. Hent datasettstøy for FAOSTAT – krasj hvis nøkkelen mangler
    key_fao = 'Crops and livestock products'
    if not dataset_noise or key_fao not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_fao}' mangler i dataset_noise for {flow_code}!")
        
    noise_val = dataset_noise[key_fao]['value']
    noise_type = dataset_noise[key_fao]['type']
    
    # 3. Slå opp den flate, perturberte N-prosenten (Krasjer hardt ved manglende data)
    def get_perturbed_product_frac(item_name):
        param_key = f"prod_{str(item_name).strip()}"
        val = current_params.get(param_key)
        
        if val is None:
            raise KeyError(
                f"[KRITISK FEIL] Produktet '{item_name}' ble funnet i FAOSTAT-dataene, "
                f"men parameteren '{param_key}' mangler i N_parameters.xlsx!"
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
            
            # Påfør asymmetrisk datasettstøy basert på støytype
            if noise_type == 'perc':
                value = base_value * noise_val
            else:
                bound = dataset_noise[key_fao]['upp_bound'] if noise_val >= 0 else dataset_noise[key_fao]['low_bound']
                value = base_value + (noise_val * bound)

            if value < 0: 
                value = 0.0

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value),
                'comment': comment,
                'data_sources': data_sources
            })

    # 7. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)

    
def _add_non_edible_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Non-edible animal products flow.
    Henter tre rådatakilder fra RAM og beregner via felles hjelpefunksjon.
    Krasjer umiddelbart hvis data mangler, og bruker utelukkende det globale EXPECTED_YEARS.
    """
    flow_code = 'AG.MM-MP.OP-Non-edible animal products-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på parametere og kildedata)'

    # 1. Hent og valider at alle rådata-filer eksisterer i RAM – krasj hardt hvis ikke
    df_hides_clean = preloaded_data.get('fao_hides_clean')
    df_wool = preloaded_data.get('wool_production')
    df_sheep = preloaded_data.get('ssb_sheep_numbers')
    
    if df_hides_clean is None:
        raise ValueError(f"[KRITISK] 'fao_hides_clean' mangler i preloaded_data for {flow_code}!")
    if df_wool is None:
        raise ValueError(f"[KRITISK] 'wool_production' mangler i preloaded_data for {flow_code}!")
    if df_sheep is None:
        raise ValueError(f"[KRITISK] 'ssb_sheep_numbers' mangler i preloaded_data for {flow_code}!")

    # 2. Kjør beregningen via hjelpefunksjonen
    # MERK: Sørg for at find_non_edible_animal_products() kaster feil hvis støy eller parametere mangler!
    year_values = find_non_edible_animal_products(
        df_hides_clean, df_wool, df_sheep, current_params, dataset_noise
    )

    # 3. Bygg resultatstrukturen dynamisk basert på det globale EXPECTED_YEARS
    for year in EXPECTED_YEARS:
        if year in year_values:
            collected_years.add(year)
            value = float(year_values[year])
            
            if value < 0: 
                value = 0.0

            # Beholder kilde-logikken din intakt, men knyttet til EXPECTED_YEARS-loopen
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

    # 4. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_manure_application_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Manure application flow.
    Henter data fra ferdiglastet Eurostat GNB Sheet 12, gjør lineær interpolasjon
    for 2017-2019, og påfører asymmetrisk datasettstøy basert på usikkerhetstype.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'AG.MM-AG.SM-Manure application-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    
    # 1. Hent rådata-matrisen fra RAM – krasj hardt hvis den mangler
    df_sheet12 = preloaded_data.get('gnb_sheet12_raw')
    if df_sheet12 is None:
        raise ValueError(f"[KRITISK] 'gnb_sheet12_raw' mangler i preloaded_data for {flow_code}!")

    # 2. Hent ut asymmetrisk datasettstøy – krasj hvis nøkler mangler
    key_gnb = 'Gross nutrient balance'
    if not dataset_noise or key_gnb not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_gnb}' mangler i dataset_noise for {flow_code}!")
    noise_gnb_val = dataset_noise[key_gnb]['value']
    noise_gnb_type = dataset_noise[key_gnb]['type']

    key_interp = 'trend interpolation'
    if key_interp not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_interp}' mangler i dataset_noise for {flow_code}!")
    noise_interp_val = dataset_noise[key_interp]['value']
    noise_interp_type = dataset_noise[key_interp]['type']

    # 3. Rekonstruer tabelloppslag (Sheet 12)
    year_row_idx = 8
    value_row_idx = 10
    first_col_idx = 1
    unit_factor = 1.0e-3

    years_row = df_sheet12.iloc[year_row_idx].values
    values_row = df_sheet12.iloc[value_row_idx].values

    year_values = {}
    for col_idx in range(first_col_idx, len(years_row)):
        yr = years_row[col_idx]
        val = values_row[col_idx]
        
        try:
            yr = int(float(yr))
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
        
        # Lagre de u-støyede basistallene som referansepunkter for interpolasjon
        if year == 2016:
            value_2016 = base_value
        elif year == 2020:
            value_2020 = base_value

        # Påfør asymmetrisk datasettstøy for rapporterte data
        if noise_gnb_type == 'perc':
            value = base_value * noise_gnb_val
        else:
            bound = dataset_noise[key_gnb]['upp_bound'] if noise_gnb_val >= 0 else dataset_noise[key_gnb]['low_bound']
            value = base_value + (noise_gnb_val * bound)

        if value < 0: 
            value = 0.0

        reported_entries.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': 'Eurostat Gross nutrient balance, Manure input'
        })

    results.extend(reported_entries)

    # 5. Interpolering for 2017-2019 (krasj hardt hvis referansepunkter mangler)
    if value_2016 is None or value_2020 is None:
        raise ValueError(
            f"[KRITISK] Kunne ikke interpolere 2017-2019 for {flow_code} "
            f"fordi basistall for enten 2016 ({value_2016}) eller 2020 ({value_2020}) mangler i rådata!"
        )

    for year in range(2017, 2020):
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            
            # Lineær interpolasjon på basistallene
            base_interp_val = value_2016 + (value_2020 - value_2016) / 4.0 * (year - 2016)
            
            # Påfør først GNB-støy
            if noise_gnb_type == 'perc':
                val_with_gnb = base_interp_val * noise_gnb_val
            else:
                bound_gnb = dataset_noise[key_gnb]['upp_bound'] if noise_gnb_val >= 0 else dataset_noise[key_gnb]['low_bound']
                val_with_gnb = base_interp_val + (noise_gnb_val * bound_gnb)

            # Påfør deretter trend/interpolasjonsstøy harmonisert
            if noise_interp_type == 'perc':
                value = val_with_gnb * noise_interp_val
            else:
                bound_interp = dataset_noise[key_interp]['upp_bound'] if noise_interp_val >= 0 else dataset_noise[key_interp]['low_bound']
                value = val_with_gnb + (noise_interp_val * bound_interp)

            if value < 0: 
                value = 0.0

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value),
                'comment': 'interpolated (MC-støy lagt på)',
                'data_sources': 'interpolated'
            })

    # 6. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_NH3_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: NH3 emissions from manure management.
    Henter rådata fra RAM og beregner utslipp for gjødselhåndtering via felles hjelpefunksjon.
    Krasjer umiddelbart hvis data mangler.
    """
    flow_code = 'AG.MM-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    # 1. Hent og valider globale parametere
    conv = float(current_params.get("NH3_to_N_factor"))
    
    # 2. Hent rådata fra RAM – krasj hardt hvis de mangler
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    if raw_lines is None:
        raise ValueError(f"[KRITISK] 'ag_crltap_raw_lines' mangler i preloaded_data for {flow_code}!")

    # 3. Kall hjelpefunksjonen som beregner summer for AG_MM-sektorene og påfører støy
    # MERK: Sørg for at load_crltap_emissions_to_N kaster KeyError hvis 'CRLTAP' mangler i dataset_noise!
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=AG_MM_CRLTAP_SECTORS,
        pollutant='NH3',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    # 4. Bygg resultatstrukturen
    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })

    # 5. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)

def _add_NOx_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: NOx emissions from manure management.
    Henter rådata fra RAM og beregner utslipp for gjødselhåndtering via felles hjelpefunksjon.
    Krasjer umiddelbart hvis data mangler.
    """
    flow_code = 'AG.MM-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    # 1. Hent og valider globale parametere
    conv = float(current_params.get("NOx_to_N_factor"))
    
    # 2. Hent rådata fra RAM – krasj hardt hvis de mangler
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    if raw_lines is None:
        raise ValueError(f"[KRITISK] 'ag_crltap_raw_lines' mangler i preloaded_data for {flow_code}!")

    # 3. Kall hjelpefunksjonen som beregner summer for AG_MM-sektorene og påfører støy
    # MERK: Sørg for at load_crltap_emissions_to_N kaster KeyError hvis 'CRLTAP' mangler i dataset_noise!
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=AG_MM_CRLTAP_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    # 4. Bygg resultatstrukturen
    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })

    # 5. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)

def _add_N2O_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: N2O emissions from manure management.
    Henter rådata fra RAM og påfører sentralt trukket datasetstøy.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'AG.MM-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'UNFCCC CRT'

    # 1. Hent og valider globale parametere
    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    
    # 2. Slå opp ferdig generert støy – krasj hvis nøkkelen mangler
    key_n2o = 'UNFCCC_emissions'
    if not dataset_noise or key_n2o not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_n2o}' mangler i dataset_noise for {flow_code}!")
    
    noise_val = dataset_noise[key_n2o]['value']
    noise_type = dataset_noise[key_n2o]['type']

    # 3. Hent ferdiglastet DataFrame fra RAM – krasj hardt hvis den mangler
    df_unfccc = preloaded_data.get('unfccc_ark1_raw')
    if df_unfccc is None:
        raise ValueError(f"[KRITISK] 'unfccc_ark1_raw' mangler i preloaded_data for {flow_code}!")

    # 4. Gå gjennom radene og beregn verdier med støy
    for r_idx in range(4, 38):
        year_val = df_unfccc.iloc[r_idx, 0]
        ton_val = df_unfccc.iloc[r_idx, 1]  # Kolonne 1 inneholder verdien for Manure Management

        if pd.notna(year_val) and pd.notna(ton_val):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)

            base_value = float(ton_val) * conv_N2O

            # Påfør støyen matematisk korrekt basert på støytype
            if noise_type == 'perc':
                value = base_value * noise_val
            else:
                bound = dataset_noise[key_n2o]['upp_bound'] if noise_val >= 0 else dataset_noise[key_n2o]['low_bound']
                value = base_value + (noise_val * bound)

            if value < 0: 
                value = 0.0

            results.append({
                'flow_name': flow_code, 
                'year': year, 
                'value': float(value),
                'comment': comment, 
                'data_sources': data_sources
            })

    # 5. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_live_animal_export_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Eksport av levende dyr (AG.MM-RW.RW-Live animal export-Nmix).
    Slår opp ferdig perturberte vekter ('weight_HORSES' osv.) fra parametergeneratoren.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'AG.MM-RW.RW-Live animal export-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy ferdig beregnet sentralt)'
    data_sources = 'FAOSTAT Crops and livestock products'
    
    # 1. Hent ferdiglastet eksport-DataFrame fra RAM – krasj hardt hvis den mangler
    final_data = preloaded_data.get('fao_live_animals_export')
    if final_data is None:
        raise ValueError(f"[KRITISK] 'fao_live_animals_export' mangler i preloaded_data for {flow_code}!")

    # 2. Hent globale perturberte parametere
    prot_frac = float(current_params.get("live_animal_protein_frac"))
    prot_to_N = float(current_params.get("Jones_factor"))

    # 3. Hent asymmetrisk kildestøy for FAOSTAT – krasj hvis nøkkelen mangler
    key_fao = 'Crops and livestock products'
    if not dataset_noise or key_fao not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_fao}' mangler i dataset_noise for {flow_code}!")
        
    noise_fao_val = dataset_noise[key_fao]['value']
    noise_fao_type = dataset_noise[key_fao]['type']

    df_round = final_data.copy()
    
    # Påfør asymmetrisk støy på kildedataene basert på støytype
    if noise_fao_type == 'perc':
        df_round['perturbed_value'] = df_round['Value'] * noise_fao_val
    else:
        # Absolutt støy (bruker asymmetriske grenser trukket sentralt)
        bound = dataset_noise[key_fao]['upp_bound'] if noise_fao_val >= 0 else dataset_noise[key_fao]['low_bound']
        df_round['perturbed_value'] = df_round['Value'] + (noise_fao_val * bound)

    # 4. Hjelpefunksjon for å hente de ferdig perturberte enkeltvektene per dyretype
    def get_perturbed_weight(item_name):
        clean_item = str(item_name).strip()
        param_key = f"weight_{clean_item}"
        
        # Sjekk om denne dyretypen i det hele tatt er definert i modellen din
        defined_weights = getattr(current_params, 'animal_weights', {})
        
        # Hvis dyretypen ikke finnes i Excel-arket 'animal_weights', ignorerer vi den
        if clean_item not in defined_weights:
            return 0.0
            
        # Hvis den SKAL være der, henter vi den. Krasjer hardt hvis parameteren mangler.
        return float(current_params.get(param_key))
    
    # 5. Beregn N-mengde per rad
    df_round['perturbed_weight'] = df_round['Item'].apply(get_perturbed_weight)
    df_round['N_amount'] = (df_round['perturbed_weight'] * df_round['perturbed_value'] * prot_frac * 1e-6 / prot_to_N)

    # 6. Aggreger per år til en kjapp ordbok
    total_N_per_year = df_round.groupby('Year')['N_amount'].sum().to_dict()
    
    # 7. Fyll ut for de forventede årstallene
    for year in sorted(EXPECTED_YEARS):
        if year in total_N_per_year:
            collected_years.add(year)
            val = total_N_per_year[year]
            if val < 0: 
                val = 0.0
            
            results.append({
                'flow_name': flow_code, 
                'year': year, 
                'value': float(val),
                'comment': comment, 
                'data_sources': data_sources
            })
            
    # 8. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_N2_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Dinitrogen-utslipp fra jordforvaltning (AG.SM-AT.AT-Emissions-N2).
    Bruker ferdig perturbert verdi for denitrifikasjon direkte fra current_params.
    Krasjer umiddelbart hvis parameteren mangler.
    """
    flow_code = 'AG.SM-AT.AT-Emissions-N2'
    collected_years = set()
    comment = 'ok (MC-støy lagt på global parameter)'
    data_sources = 'Schäppi2025Ann + NIBIO'
    
    # 1. Hent den ferdig perturberte parameterverdien – krasj hardt hvis den mangler
    val_param = current_params.get("denitrification_AG_N2")
    if val_param is None:
        raise KeyError(
            f"[KRITISK] Parameteren 'denitrification_AG_N2' mangler i current_params for {flow_code}! "
            f"Sjekk N_parameters.xlsx eller parametergeneratoren."
        )
        
    value = float(val_param)
    if value < 0: 
        value = 0.0

    # 2. Fyll ut verdien konstant for alle forventede årstall
    for year in sorted(EXPECTED_YEARS):
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,  
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 3. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)