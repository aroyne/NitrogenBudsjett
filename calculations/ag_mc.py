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

# CRLTAP category codes for the two AG subsectors, used to select which rows of
# the CRLTAP inventory (webdabData1863365.txt, loaded as 'ag_crltap_raw_lines')
# to sum for each subsector's NH3/NOx emissions.
# SM = Soil Management: direct/indirect emissions from synthetic fertilizer and
# crop residue N applied to soil (CRLTAP 3D) plus agricultural residue burning
# (CRLTAP 4B/4C).
AG_SM_CRLTAP_SECTORS = [
    '3Da1','3Da2a','3Da2b','3Da2c','3Da3','3Da4',
    '3Db','3Dc','3De','3Df','4B1','4B2','4C1','4C2',
]

# MM = Manure Management: emissions from livestock manure during storage and
# handling, before it is applied to soil (CRLTAP 3B).
AG_MM_CRLTAP_SECTORS = [
    '3B1a','3B1b','3B2','3B3',
    '3B4a','3B4d','3B4e','3B4f',
    '3B4gi','3B4gii','3B4giii','3B4giv','3B4h',
]


def execute_calculations_ag(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    Main function for the AG (agriculture) pool. Runs all sub-calculations.
    All distributions are drawn centrally in main_mc before this runs.
    """
    results = []

    _add_food_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_industrial_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_fodder_crops_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.SM-AT.AT-Emissions-NH3', AG_SM_CRLTAP_SECTORS, 'NH3')
    _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.SM-AT.AT-Emissions-NOx', AG_SM_CRLTAP_SECTORS, 'NOx')
    _add_ag_n2o_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.SM-AT.AT-Emissions-N2O', 2, 'UNFCCC_N2O_agri_soils')
    _add_ag_leaching_mc(results, preloaded_data, dataset_noise, 'AG.SM-HY.SW-Leaching-Nmix', 'Nr_SM')
    _add_ag_leaching_mc(results, preloaded_data, dataset_noise, 'AG.MM-HY.SW-Leaching-Nmix', 'Nr_MM')
    _add_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_non_edible_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_manure_application_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.MM-AT.AT-Emissions-NH3', AG_MM_CRLTAP_SECTORS, 'NH3')
    _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.MM-AT.AT-Emissions-NOx', AG_MM_CRLTAP_SECTORS, 'NOx')
    _add_ag_n2o_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.MM-AT.AT-Emissions-N2O', 1, 'UNFCCC_N2O_agri_manure')
    _add_live_animal_export_mc(results, preloaded_data, current_params, dataset_noise)
    _add_N2_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise)

    return results


def _add_food_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-MP.FP-Food crop products-Nmix'
    collected_years = set()
    data_sources = 'Eurostat Gross nutrient balance'
    comment = 'ok'

    # 'ag_gnb_workbook' <- data_files/aei_pr_gnb__custom_18744910_spreadsheet.xlsx
    # (Eurostat Gross nutrient balance)
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
        unit_factor=-1.0e-3,  # subtract industrial crops
        op='+',
    )

    # Un-noised base values, used as anchors for interpolation
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

    # Interpolation for the 2017-2019 data gap
    for year in range(2017, 2020):
        if year in EXPECTED_YEARS:
            collected_years.add(year)

            # Linear interpolation on the un-noised base values (1/4 weight per year from 2016)
            base_interp_val = value_2016 + (value_2020 - value_2016) / 4.0 * (year - 2016)

            # Apply the general GNB dataset noise first...
            val_with_gnb = base_interp_val * noise_val

            # ...then a separate interpolation noise on top, since interpolated
            # years carry additional uncertainty beyond the source dataset's own.
            value = val_with_gnb * noise_interp_val

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value),
                'comment': 'ok',
                'data_sources': 'interpolated (Eurostat GNB gap)'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_industrial_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'AG.SM-MP.OP-Crop products for industrial use-Nmix'
    collected_years = set()
    data_sources = 'Eurostat Gross nutrient balance, Nutrient removal by harvest of industrial crops'
    comment = 'ok'

    # 'gnb_sheet30_raw' <- data_files/aei_pr_gnb__custom_18744910_spreadsheet.xlsx,
    # Sheet 30 (Eurostat Gross nutrient balance, nutrient removal by harvest of
    # industrial crops)
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
    comment = 'ok'

    fodder_prot = float(current_params.get("fodder_protein_frac"))
    Jones = float(current_params.get("Jones_factor"))
    N_content = fodder_prot / Jones

    key_13648 = '13648'
    noise_13648_val = dataset_noise[key_13648]
    key_05772 = '05772'
    noise_05772_val = dataset_noise[key_05772]

    # 'ssb_13648_raw' <- data_files/13648_20251117-154625.xlsx: SSB table 13648
    # (agricultural yield), covers 2021-2024
    # 'ssb_05772_raw' <- data_files/05772_20251210-142618.xlsx: SSB table 05772
    # (agricultural yield), covers 2000-2020
    # 'grovfor_old_raw' <- data_files/grovfor_før_2000.xlsx: historical hay/silage
    # yield compiled from Jordbruksstatistikk 2000 (SSB), covers 1984-1999
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

    # Pre-2000 (SSB Jordbruksstatistikk)
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

def _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, flow_code, sectors, pollutant):
    """
    Shared implementation for CRLTAP-derived NH3/NOx emissions of an AG subsector
    (soil management or manure management). `sectors` is AG_SM_CRLTAP_SECTORS or
    AG_MM_CRLTAP_SECTORS above; `pollutant` is 'NH3' or 'NOx'. Reads
    preloaded_data['ag_crltap_raw_lines'] <- data_files/webdabData1863365.txt
    (CRLTAP Inventory Submissions).
    """
    collected_years = set()
    comment = 'ok'
    data_sources = 'CRLTAP Inventory Submissions'

    conv = float(current_params.get(f"{pollutant}_to_N_factor"))
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')

    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=sectors,
        pollutant=pollutant,
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


def _add_ag_n2o_emissions_mc(results, preloaded_data, current_params, dataset_noise, flow_code, value_col, dataset_key):
    """
    Shared implementation for AG subsector N2O emissions. Both subsectors are
    columns of the same compilation: preloaded_data['unfccc_ark1_raw'] <-
    data_files/N2O_NOx_AG.xlsx (N2O and NOx emissions from agriculture, UNFCCC
    CRT Table 3), loaded without headers - column 1 = 'N2O, MM', column 2 =
    'N2O, SM'. Rows 4-37 = years 2023 down to 1990. dataset_key differs by caller
    since Norway NID Annexes 2025, Annex 2 gives manure management (IPCC 3B,
    'UNFCCC_N2O_agri_manure') and soil emissions (IPCC 3D, 'UNFCCC_N2O_agri_soils')
    different N2O uncertainty ("Fac2" vs "Fac3").
    """
    collected_years = set()
    comment = 'ok'
    data_sources = 'UNFCCC CRT'

    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    noise_val = dataset_noise[dataset_key]
    df_unfccc = preloaded_data.get('unfccc_ark1_raw')

    for r_idx in range(4, 38):
        year_val = df_unfccc.iloc[r_idx, 0]
        ton_val = df_unfccc.iloc[r_idx, value_col]

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


def _add_ag_leaching_mc(results, preloaded_data, dataset_noise, flow_code, value_col):
    """
    Shared implementation for AG subsector Nr leaching/runoff. Both subsectors
    are columns of the same compilation: preloaded_data['ag_leaching_csv'] <-
    data_files/Nr_AG--HY.csv (Nr runoff and leaching from soil/manure
    management, UNFCCC CRT Table 3). value_col is 'Nr_SM' or 'Nr_MM'.
    """
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    comment = 'ok'

    key_leach = 'UNFCCC_N_leaching'
    noise_val = dataset_noise[key_leach]

    df_leaching = preloaded_data.get('ag_leaching_csv')
    years = df_leaching['year'].values
    values = df_leaching[value_col].values

    for i in range(len(years)):
        year = int(years[i])
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)

        base_value = float(values[i])
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
    comment = 'ok'

    # 'fao_animal_production_clean' <- data_files/FAOSTAT_data_en_11-18-2025.csv
    # (Crop and livestock products: production quantity, animal products)
    df_fao = preloaded_data.get('fao_animal_production_clean')
    key_fao = 'Crops and livestock products'
    noise_val = dataset_noise[key_fao]

    def get_perturbed_product_frac(item_name):
        param_key = f"prod_{str(item_name).strip()}"
        return float(current_params.get(param_key))

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
    comment = 'ok'

    # 'fao_hides_clean' <- data_files/FAOSTAT_data_en_11-18-2025.csv (Crop and
    # livestock products, hides production quantity)
    # 'wool_production' <- data_files/ull.xlsx (wool delivered to slaughterhouses,
    # 2005-2024, compiled from Landbruksdirektoratet raw data)
    # 'ssb_sheep_numbers' <- data_files/03710_20260128-152225.xlsx (SSB table
    # 03710, winter-fed sheep count)
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

            # Wool/sheep data for 2001 is interpolated from 2000 and 2002 in
            # find_non_edible_animal_products (shared_flow_calculations.py) due
            # to a real gap in ssb_sheep_numbers for that year. This branching
            # must mirror the one there exactly to keep the reported source in
            # sync with how the value was actually computed.
            if year > 2004:
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
    comment = 'ok'
    
    # 'gnb_sheet12_raw' <- data_files/aei_pr_gnb__custom_18744910_spreadsheet.xlsx,
    # Sheet 12 (Eurostat Gross nutrient balance, manure N input)
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

        # Eurostat's GNB sheet alternates each value column with an empty flag
        # column (year cell is None there), and marks missing years with ':'
        # instead of a number - both cases are expected and skipped, not errors.
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
        
        # Store the un-noised base values as anchors for interpolation
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

    # Interpolation for the 2017-2019 data gap
    for year in range(2017, 2020):
        if year in EXPECTED_YEARS:
            collected_years.add(year)

            # Linear interpolation on the base values
            base_interp_val = value_2016 + (value_2020 - value_2016) / 4.0 * (year - 2016)
            val_with_gnb = base_interp_val * noise_gnb_val
            value = val_with_gnb * noise_interp_val

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value),
                'comment': 'ok',
                'data_sources': 'interpolated'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    
def _add_live_animal_export_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Weight-based N export from live animal exports (FAOSTAT). Only animal types
    explicitly weighted in N_parameters.xlsx's 'animal_weights' table contribute
    - FAOSTAT's live-animal export list includes types the model deliberately
    does not track a weight for (e.g. minor/non-livestock categories), and those
    rows are meant to contribute zero rather than requiring a weight for every
    FAOSTAT item.
    """
    flow_code = 'AG.MM-RW.RW-Live animal export-Nmix'
    collected_years = set()
    comment = 'ok'
    data_sources = 'FAOSTAT Crops and livestock products'

    # 'fao_live_animals_export' <- data_files/FAOSTAT_data_en_11-12-2025.csv
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

        try:
            return float(current_params.get(param_key))
        except KeyError:
            # FAOSTAT's live-animal export list includes types the model
            # deliberately does not track a weight for (see docstring above).
            return 0.0

    df_round['perturbed_weight'] = df_round['Item'].apply(get_perturbed_weight)
    df_round['N_amount'] = (df_round['perturbed_weight'] * df_round['perturbed_value'] * prot_frac * 1e-6 / prot_to_N)

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
    comment = 'ok'
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