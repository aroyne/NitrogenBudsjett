#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from calculations.utils import (
    EXPECTED_YEARS,
    read_year_value_row,
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
    
    return results


def _add_food_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-MP.FP-Food crop products-Nmix'
    collected_years = set()
    data_sources = 'Eurostat Gross nutrient balance'
    comment = 'ok (MC-støy lagt på)'

    workbook = preloaded_data.get('ag_gnb_workbook')
    dataset_key = 'Gross nutrient balance'
    noise_val = dataset_noise[dataset_key]
    key_interp = 'trend interpolation'
    noise_interp_val = dataset_noise[key_interp]

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

    # u-støyede basistall for interpolasjons-ankere
    value_2016 = year_values.get(2016)
    value_2020 = year_values.get(2020)

    for year, total_value in year_values.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        value = total_value * noise_val
        if value < 0: 
            value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources,
        })

    # Interpolering for datagapet 2017-2019 
    for year in range(2017, 2020):
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            
            # Lineær interpolasjon på de rene basistallene (vekt 1/4 per år fra 2016)
            base_interp_val = value_2016 + (value_2020 - value_2016) / 4.0 * (year - 2016)
            
            # Påfør først den generelle GNB-støyen
            val_with_gnb = base_interp_val * noise_val

            # Påfør deretter trend/interpolasjonsstøy harmonisert
            value = val_with_gnb * noise_interp_val

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value),
                'comment': 'interpolated (MC-støy lagt på)',
                'data_sources': 'interpolated (Eurostat GNB gap)'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_industrial_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-MP.OP-Crop products for industrial use-Nmix'
    collected_years = set()
    data_sources = 'Eurostat Gross nutrient balance, Nutrient removal by harvest of industrial crops'
    comment = 'ok (MC-støy lagt på)'

    df_gnb_sheet30 = preloaded_data.get('gnb_sheet30_raw')
    year_values = find_industrial_crop_products(df_gnb_sheet30, dataset_noise)

    for year, value in year_values.items():
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

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_fodder_crops_flow_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-AG.MM-Fodder crops-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'

    fodder_prot = float(current_params.get("fodder_protein_frac"))
    Jones = float(current_params.get("Jones_factor"))
    N_content = fodder_prot / Jones

    key_13648 = '13648'
    noise_13648_val = dataset_noise[key_13648]
    key_05772 = '05772'
    noise_05772_val = dataset_noise[key_05772]

    df_13648 = preloaded_data.get('ssb_13648_raw')
    df_05772 = preloaded_data.get('ssb_05772_raw')
    df_old = preloaded_data.get('grovfor_old_raw')

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
            
            value = base_value * noise_13648_val
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(value),
                'comment': comment, 'data_sources': data_sources_A
            })

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
            
            value = base_value * noise_05772_val
            
            if value < 0: value = 0.0
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(value),
                'comment': comment, 'data_sources': data_sources_B
            })

    # Før 2000 (SSB Jordbruksstatistikk)
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
            value = base_value * noise_05772_val
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(value),
                'comment': comment, 'data_sources': data_sources_C
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
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
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
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
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
    noise_val = dataset_noise[key_n2o]
    df_unfccc = preloaded_data.get('unfccc_ark1_raw')

    for r_idx in range(4, 37):
        year_val = df_unfccc.iloc[r_idx, 0]
        ton_val = df_unfccc.iloc[r_idx, 2]

        if pd.notna(year_val) and pd.notna(ton_val):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)

            base_value = float(ton_val) * conv_N2O
            value = base_value * noise_val

            results.append({
                'flow_name': flow_code, 
                'year': year, 
                'value': float(value),
                'comment': comment, 
                'data_sources': data_sources
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_leaching_soil_management_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-HY.SW-Leaching-Nmix'
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    comment = 'ok (MC-støy lagt på)'

    key_leach = 'UNFCCC_emissions'
    noise_val = dataset_noise[key_leach]

    df_leaching = preloaded_data.get('ag_leaching_csv')
    years = df_leaching['year'].values
    values_sm = df_leaching['Nr_SM'].values

    for i in range(len(years)):
        year = int(years[i])
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        base_value = float(values_sm[i])
        value = base_value * noise_val

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

    key_leach = 'UNFCCC_emissions'
    noise_val = dataset_noise[key_leach]

    df_leaching = preloaded_data.get('ag_leaching_csv')
    years = df_leaching['year'].values
    values_mm = df_leaching['Nr_MM'].values

    for i in range(len(years)):
        year = int(years[i])
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        
        base_value = float(values_mm[i])
        value = base_value * noise_val

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
    flow_code = 'AG.MM-MP.FP-Animal products-Nmix'
    collected_years = set()
    data_sources = 'FAOSTAT Crops and livestock products'
    comment = 'ok (MC-støy lagt på unikt per produkt)'

    df_fao = preloaded_data.get('fao_animal_production_clean')
    key_fao = 'Crops and livestock products'
    noise_val = dataset_noise[key_fao]
    
    def get_perturbed_product_frac(item_name):
        param_key = f"prod_{str(item_name).strip()}"
        val = current_params.get(param_key)
        
        if val is None:
            raise KeyError(
                f"[KRITISK FEIL] Produktet '{item_name}' ble funnet i FAOSTAT-dataene, "
                f"men parameteren '{param_key}' mangler i N_parameters.xlsx!"
            )
        return float(val)

    working_df = df_fao.copy()
    working_df['N_content_percent'] = working_df['Item'].apply(get_perturbed_product_frac)
    working_df['N_amount_kt'] = working_df['Value'] * working_df['N_content_percent'] / 1.0e5

    total_N_per_year = working_df.groupby('Year')['N_amount_kt'].sum().to_dict()

    for year in EXPECTED_YEARS:
        if year in total_N_per_year:
            collected_years.add(year)
            base_value = float(total_N_per_year[year])
            value = base_value * noise_val

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
    flow_code = 'AG.MM-MP.OP-Non-edible animal products-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på parametere og kildedata)'

    df_hides_clean = preloaded_data.get('fao_hides_clean')
    df_wool = preloaded_data.get('wool_production')
    df_sheep = preloaded_data.get('ssb_sheep_numbers')
    
    year_values = find_non_edible_animal_products(
        df_hides_clean, df_wool, df_sheep, current_params, dataset_noise
    )

    for year in EXPECTED_YEARS:
        if year in year_values:
            collected_years.add(year)
            value = float(year_values[year])
            
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

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_manure_application_flow_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.MM-AG.SM-Manure application-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    
    df_sheet12 = preloaded_data.get('gnb_sheet12_raw')
    key_gnb = 'Gross nutrient balance'
    noise_gnb_val = dataset_noise[key_gnb]
    key_interp = 'trend interpolation'
    noise_interp_val = dataset_noise[key_interp]

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

        value = base_value * noise_gnb_val

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

    # Interpolering for 2017-2019 
    for year in range(2017, 2020):
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            
            # Lineær interpolasjon på basistallene
            base_interp_val = value_2016 + (value_2020 - value_2016) / 4.0 * (year - 2016)
            val_with_gnb = base_interp_val * noise_gnb_val
            value = val_with_gnb * noise_interp_val

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value),
                'comment': 'interpolated (MC-støy lagt på)',
                'data_sources': 'interpolated'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_NH3_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.MM-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    conv = float(current_params.get("NH3_to_N_factor"))
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
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
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)

def _add_NOx_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.MM-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    conv = float(current_params.get("NOx_to_N_factor"))
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
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
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)

def _add_N2O_emissions_manure_management_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.MM-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'UNFCCC CRT'

    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    key_n2o = 'UNFCCC_emissions'
    noise_val = dataset_noise[key_n2o]
    df_unfccc = preloaded_data.get('unfccc_ark1_raw')

    for r_idx in range(4, 38):
        year_val = df_unfccc.iloc[r_idx, 0]
        ton_val = df_unfccc.iloc[r_idx, 1]  # Kolonne 1 inneholder verdien for Manure Management

        if pd.notna(year_val) and pd.notna(ton_val):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)

            base_value = float(ton_val) * conv_N2O
            value = base_value * noise_val

            results.append({
                'flow_name': flow_code, 
                'year': year, 
                'value': float(value),
                'comment': comment, 
                'data_sources': data_sources
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_live_animal_export_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.MM-RW.RW-Live animal export-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy ferdig beregnet sentralt)'
    data_sources = 'FAOSTAT Crops and livestock products'
    
    final_data = preloaded_data.get('fao_live_animals_export')
    prot_frac = float(current_params.get("live_animal_protein_frac"))
    prot_to_N = float(current_params.get("Jones_factor"))
    key_fao = 'Crops and livestock products'
    noise_fao_val = dataset_noise[key_fao]

    df_round = final_data.copy()
    df_round['perturbed_value'] = df_round['Value'] * noise_fao_val

    def get_perturbed_weight(item_name):
        clean_item = str(item_name).strip()
        param_key = f"weight_{clean_item}"
        
        # Sjekk om denne dyretypen i det hele tatt er definert i modellen din
        defined_weights = getattr(current_params, 'animal_weights', {})
        
        # Hvis dyretypen ikke finnes i Excel-arket 'animal_weights', ignorerer vi den
        if clean_item not in defined_weights:
            return 0.0
            
        return float(current_params.get(param_key))
    
    # Beregn N-mengde per rad
    df_round['perturbed_weight'] = df_round['Item'].apply(get_perturbed_weight)
    df_round['N_amount'] = (df_round['perturbed_weight'] * df_round['perturbed_value'] * prot_frac * 1e-6 / prot_to_N)

    # Aggreger per år til en kjapp ordbok
    total_N_per_year = df_round.groupby('Year')['N_amount'].sum().to_dict()
    
    for year in sorted(EXPECTED_YEARS):
        if year in total_N_per_year:
            collected_years.add(year)
            val = total_N_per_year[year]
            
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
    flow_code = 'AG.SM-AT.AT-Emissions-N2'
    collected_years = set()
    comment = 'ok (MC-støy lagt på global parameter)'
    data_sources = 'Schäppi2025Ann + NIBIO'
    
    val_param = current_params.get("denitrification_AG_N2")        
    value = float(val_param)
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