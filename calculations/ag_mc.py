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
    find_non_edible_animal_products,
    utmark_grazing
    )

# CRLTAP category codes for the two AG subsectors, used to select which rows of
# the CRLTAP inventory (webdabData1868031.txt, loaded as 'ag_crltap_raw_lines')
# to sum for each subsector's NH3/NOx emissions.
# SM = Soil Management: emissions from fertilizer, manure, sludge, grazing and
# crop residue N applied to soil (CRLTAP 3D, Schäppi et al. 2025 Table 30),
# plus field burning of agricultural residues (3F), which the text of the
# guidance names as an NH3 source although Table 30 does not list it. The
# LULUCF codes 4B1/4B2/4C1/4C2 in Table 30 are not reported in the CRLTAP
# inventory and give zero.
AG_SM_CRLTAP_SECTORS = [
    '3Da1','3Da2a','3Da2b','3Da2c','3Da3','3Da4',
    '3Db','3Dc','3De','3Df','3F','4B1','4B2','4C1','4C2',
]

# MM = Manure Management: emissions from livestock manure during housing and
# storage, before it is applied to soil (CRLTAP 3B, Table 29), plus 3I
# (other agriculture), which in Norway is NH3 from ammonia treatment of straw
# for feed.
AG_MM_CRLTAP_SECTORS = [
    '3B1a','3B1b','3B2','3B3',
    '3B4a','3B4d','3B4e','3B4f',
    '3B4gi','3B4gii','3B4giii','3B4giv','3B4h','3I',
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
    # Grazing manure on utmark (unmanaged land) and its losses; the
    # inventory counts all grazing manure as input to managed soils, so the
    # utmark losses are removed from the AG.SM flows (see utmark_grazing).
    utmark_losses = utmark_grazing(preloaded_data, current_params)
    _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.SM-AT.AT-Emissions-NH3', AG_SM_CRLTAP_SECTORS, 'NH3', utmark_losses)
    _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.SM-AT.AT-Emissions-NOx', AG_SM_CRLTAP_SECTORS, 'NOx', utmark_losses)
    _add_ag_n2o_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.SM-AT.AT-Emissions-N2O', 2, 'UNFCCC_N2O_agri_soils', utmark_losses)
    _add_ag_leaching_mc(results, preloaded_data, dataset_noise, 'AG.SM-HY.SW-Leaching-Nmix', 'Nr_SM', utmark_losses)
    _add_ag_leaching_mc(results, preloaded_data, dataset_noise, 'AG.MM-HY.SW-Leaching-Nmix', 'Nr_MM')
    _add_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_non_edible_animal_products_flow_mc(results, preloaded_data, current_params, dataset_noise)
    _add_manure_application_flow_mc(results, preloaded_data, current_params, dataset_noise, utmark_losses)
    _add_utmark_manure_flow_mc(results, current_params, dataset_noise, utmark_losses)
    _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.MM-AT.AT-Emissions-NH3', AG_MM_CRLTAP_SECTORS, 'NH3')
    _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.MM-AT.AT-Emissions-NOx', AG_MM_CRLTAP_SECTORS, 'NOx')
    _add_ag_n2o_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'AG.MM-AT.AT-Emissions-N2O', 1, 'UNFCCC_N2O_agri_manure')
    _add_live_animal_export_mc(results, preloaded_data, current_params, dataset_noise)
    _add_N2_emissions_soil_management_mc(results, preloaded_data, current_params, dataset_noise)

    return results


def _add_food_crop_products_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Nutrient removal by harvest of crops minus industrial crops, from
    Eurostat's Gross Nutrient Balance. Years missing in the balance (2017-2019
    and 2024) are filled from SSB's cereal harvest: cereals carry most of the
    N, so the cereal N is the SSB harvest times the N per tonne of harvest in
    the balance (interpolated between the nearest years with data, or taken
    from the last year), and the remaining crops are interpolated or held at
    the last year's value.
    """
    flow_code = 'AG.SM-MP.FP-Food crop products-Nmix'
    collected_years = set()
    data_sources = 'Eurostat Gross nutrient balance'
    comment = 'ok'

    # 'ag_gnb_workbook' <- data_files/aei_pr_gnb__custom_18744910_spreadsheet.xlsx
    # (Eurostat Gross nutrient balance)
    # 'ssb_cereal_harvest_07479' <- data_files/07479_kornavling.csv (SSB table
    # 07479, cereal harvest, 1000 t)
    workbook = preloaded_data.get('ag_gnb_workbook')
    cereal_harvest = preloaded_data['ssb_cereal_harvest_07479']['kornavling_1000t']
    noise_val = dataset_noise['Gross nutrient balance']
    noise_ssb = dataset_noise['07479']

    def read_sheet(name, factor):
        return read_year_value_row(workbook[name], year_values=None, year_row=9, value_row=11,
                                   first_col=2, unit_factor=factor, op='+')

    crops = read_sheet('Sheet 26', 1.0e-3)       # nutrient removal by harvest of crops
    industrial = read_sheet('Sheet 30', 1.0e-3)  # of which industrial crops (subtracted)
    cereals = read_sheet('Sheet 27', 1.0e-3)     # of which cereals
    food = {y: v - industrial.get(y, 0.0) for y, v in crops.items()}

    for year, value in food.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value * noise_val),
            'comment': comment,
            'data_sources': data_sources,
        })

    # Years without a balance figure, but with an SSB cereal harvest.
    gnb_years = sorted(y for y in food if y in cereals and y in cereal_harvest.index)
    n_per_harvest = {y: cereals[y] / cereal_harvest[y] for y in gnb_years}
    other_crops = {y: food[y] - cereals[y] for y in gnb_years}
    for year in sorted(EXPECTED_YEARS - set(food)):
        if year < gnb_years[0] or year not in cereal_harvest.index:
            continue
        before = max(y for y in gnb_years if y < year)
        after = [y for y in gnb_years if y > year]
        if after:
            w = (year - before) / (after[0] - before)
            n_per_t = n_per_harvest[before] + w * (n_per_harvest[after[0]] - n_per_harvest[before])
            other = other_crops[before] + w * (other_crops[after[0]] - other_crops[before])
        else:
            n_per_t, other = n_per_harvest[before], other_crops[before]
        value = (n_per_t * cereal_harvest[year] * noise_ssb + other) * noise_val
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': 'Eurostat GNB scaled by SSB cereal harvest (table 07479)',
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
    # find_industrial_crop_products already extrapolates 2024 (3-year average
    # of 2021-2023 - this flow is small and volatile with no clear trend, so
    # that's a more representative anchor than a flat carry-forward of 2023
    # alone) - done there rather than here so mp_mc.py's consumer-goods mass
    # balance, which calls the same function directly, sees the same value.
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
            'data_sources': data_sources if year != 2024 else '3-year average of 2021-2023 (Eurostat GNB not yet released for 2024)'
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_fodder_crops_flow_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Harvested (slått) forage from SSB yield statistics, plus grazing directly
    on agricultural land (innmark), which the harvest statistics do not
    cover. Innmark grazing is taken from Budsjettnemnda for jordbruket's
    Totalkalkylen "Eng, beite" series (\\citet{bfj_totalkalkylen_2025}),
    1000 FEm/year, calculated by BFJ as 200 FEm/daa on innmarksbeite plus
    18 FEm/daa aftermath grazing on eng til slått, both scaled by the
    actual-vs-normal-year harvest ratio (\\citet{landbruksdirektoratet_forressurser_2021}).
    Converted to N using the same 150 g protein/FEm assumption as the
    corresponding utmark-grazing flow (FS.OL-AG.MM-Grazing-Nmix in fs_mc.py),
    since both represent grazed grass rather than harvested crop mass and
    are not on the same physical basis as fodder_protein_frac below (which
    is calibrated per kg of harvested dry matter, not per feed unit).

    Harvested-forage and grazing values are summed into a single value per
    year before being reported, since two rows for the same (flow_name,
    year) would each be treated as a separate observation when results are
    aggregated across simulations, biasing that year's median/CI.
    """
    flow_code = 'AG.SM-AG.MM-Fodder crops-Nmix'
    collected_years = set()
    comment = 'ok'

    fodder_prot = float(current_params.get("fodder_protein_frac"))
    Jones = float(current_params.get("Jones_factor"))
    N_content = fodder_prot / Jones
    # SSB reports "Grønfôr- og silovekstar" as fresh/ensiled weight (farmers
    # report m3 silage, round bales or tonnes of fresh fodder), while
    # fodder_protein_frac is per kg dry matter. Green fodder is therefore
    # converted to dry matter before the N content applies.
    green_dm = float(current_params.get("green_fodder_DM_frac"))
    # SSB reports eng til slått as dry matter from 2021, as hay converted via
    # dry matter for 1995-2020, and as hay converted on an energy basis before
    # 1995. The energy-basis figures are scaled to the dry-matter basis so the
    # series is continuous across 1995.
    hay_energy_basis = float(current_params.get("hay_energy_to_DM_basis_frac"))
    # Before 2021 the eng til slått figures are hay weight, converted here to
    # dry matter to match fodder_protein_frac.
    hay_dm = float(current_params.get("hay_DM_frac"))

    key_13648 = '13648'
    noise_13648_val = dataset_noise[key_13648]
    key_05772 = '05772'
    noise_05772_val = dataset_noise[key_05772]

    # 'ssb_13648_raw' <- data_files/13648_20260916-101847.xlsx: SSB table 13648
    # (agricultural yield), covers 2021-2025. Laid out with years down rows
    # (from row 5) and crops across columns, unlike every other year-range
    # table in this file (which puts years across columns) - SSB changed this
    # table's orientation in the 2026-09-16 export.
    # 'ssb_05772_raw' <- data_files/05772_20251210-142618.xlsx: SSB table 05772
    # (agricultural yield), covers 2000-2020
    # 'grovfor_old_raw' <- data_files/grovfor_før_2000.xlsx: historical hay/silage
    # yield compiled from Jordbruksstatistikk 2000 (SSB), covers 1984-1999
    df_13648 = preloaded_data.get('ssb_13648_raw')
    df_05772 = preloaded_data.get('ssb_05772_raw')
    df_old = preloaded_data.get('grovfor_old_raw')

    year_entries = {}

    for row_idx in range(5, df_13648.shape[0]):
        year_val = df_13648.iloc[row_idx, 0]
        if pd.isna(year_val):
            continue
        try:
            year = int(year_val)
        except (TypeError, ValueError):
            # Row 0 stops being a year once the year block ends (footer text
            # such as "Tal for 2024 er framleis førebels...").
            continue
        if year not in EXPECTED_YEARS:
            continue
        val5 = df_13648.iloc[row_idx, 1]  # Eng til slått
        val6 = df_13648.iloc[row_idx, 2]  # Grøntfôr- og silovekstar

        if pd.notna(val5) and pd.notna(val6):
            base_value = (float(val5) + float(val6) * green_dm) * N_content
            year_entries[year] = {'value': base_value * noise_13648_val, 'data_sources': 'SSB table 13648'}

    for col_idx in range(1, 22):
        year_val = df_05772.iloc[2, col_idx]
        val4 = df_05772.iloc[3, col_idx]  # Grøntfôr- og silovekstar
        val5 = df_05772.iloc[4, col_idx]  # Høy

        if pd.notna(year_val) and pd.notna(val4) and pd.notna(val5):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            base_value = (float(val4) * green_dm + float(val5) * hay_dm) * N_content
            value = base_value * noise_05772_val
            if value < 0:
                value = 0.0
            year_entries[year] = {'value': value, 'data_sources': 'SSB table 05772'}

    # Pre-2000 (SSB Jordbruksstatistikk)
    for r_idx in range(2, 18):
        year_val = df_old.iloc[r_idx, 0]
        val2 = df_old.iloc[r_idx, 1]  # Høy
        val3 = df_old.iloc[r_idx, 2]  # Grønfôr og silovekstar

        if pd.notna(year_val) and pd.notna(val2) and pd.notna(val3):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            hay = float(val2)
            if year < 1995:
                hay *= hay_energy_basis
            base_value = (hay * hay_dm + float(val3) * green_dm) * N_content
            value = base_value * noise_05772_val
            year_entries[year] = {'value': value, 'data_sources': 'SSB Jordbruksstatistikk'}

    # Innmark grazing (Budsjettnemnda for jordbruket Totalkalkylen), added on
    # top of the harvested-forage value for each year rather than as its own
    # row - see this function's docstring for why.
    df_innmark = preloaded_data.get('ag_innmark_grazing_raw')
    noise_bfj_val = dataset_noise['BFJ_totalkalkylen_grazing']
    n_content_grazing = float(current_params.get("protein_cont_grazing")) / Jones / 1.0e9  # g protein/FEm -> kt N/FEm

    for row_idx in range(1, df_innmark.shape[0]):
        year_val = df_innmark.iloc[row_idx, 0]
        fem_1000 = df_innmark.iloc[row_idx, 3]

        if pd.isna(year_val) or pd.isna(fem_1000):
            continue
        year = int(year_val)
        if year not in EXPECTED_YEARS or year not in year_entries:
            continue

        grazing_value = float(fem_1000) * 1000 * n_content_grazing * noise_bfj_val  # 1000 FEm -> FEm -> kt N
        year_entries[year]['value'] += grazing_value
        year_entries[year]['data_sources'] += ' + BFJ Totalkalkylen, Eng-beite'

    for year, entry in year_entries.items():
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': float(entry['value']),
            'comment': comment, 'data_sources': entry['data_sources']
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)

def _add_ag_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, flow_code, sectors, pollutant, utmark_losses=None):
    """
    Shared implementation for CRLTAP-derived NH3/NOx emissions of an AG subsector
    (soil management or manure management). `sectors` is AG_SM_CRLTAP_SECTORS or
    AG_MM_CRLTAP_SECTORS above; `pollutant` is 'NH3' or 'NOx'. Reads
    preloaded_data['ag_crltap_raw_lines'] <- data_files/webdabData1868031.txt
    (CRLTAP Inventory Submissions). With utmark_losses (soil management only),
    the utmark share of emissions from grazing animals (3Da3) is left out.
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
    if utmark_losses is not None:
        grazing = load_crltap_emissions_to_N(
            raw_lines=raw_lines, categories=['3Da3'], pollutant=pollutant,
            conv_to_N=conv, dataset_noise=dataset_noise, noise_key='CRLTAP'
        )
        for year in sums:
            sums[year] -= grazing.get(year, 0.0) * utmark_losses[year]['utmark_frac']

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


def _add_ag_n2o_emissions_mc(results, preloaded_data, current_params, dataset_noise, flow_code, value_col, dataset_key, utmark_losses=None):
    """
    Shared implementation for AG subsector N2O emissions. Both subsectors are
    columns of the same series: preloaded_data['unfccc_ark1_raw'] <- UNFCCC
    CRT Table3 (data_loader.py's crt_n2o_ag method, reading directly from
    the NOR-CRT-2026-... folder), column 1 = "3.B. Manure management" N2O,
    column 2 = "3.D. Agricultural soils" N2O. dataset_key differs by caller
    since Norway NID Annexes 2025, Annex 2 gives manure management (IPCC 3B,
    'UNFCCC_N2O_agri_manure') and soil emissions (IPCC 3D, 'UNFCCC_N2O_agri_soils')
    different N2O uncertainty ("Fac2" vs "Fac3"). With utmark_losses (soil
    management only), N2O from grazing manure on utmark is left out.
    """
    collected_years = set()
    comment = 'ok'
    data_sources = 'UNFCCC CRT'

    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    noise_val = dataset_noise[dataset_key]
    df_unfccc = preloaded_data.get('unfccc_ark1_raw')

    for r_idx in range(len(df_unfccc)):
        year_val = df_unfccc.iloc[r_idx, 0]
        ton_val = df_unfccc.iloc[r_idx, value_col]

        if pd.notna(year_val) and pd.notna(ton_val):
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)

            base_value = float(ton_val) * conv_N2O
            if utmark_losses is not None:
                base_value -= utmark_losses[year]['n2o']
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


def _add_ag_leaching_mc(results, preloaded_data, dataset_noise, flow_code, value_col, utmark_losses=None):
    """
    Shared implementation for AG subsector Nr leaching/runoff. Both subsectors
    are columns of the same series: preloaded_data['ag_leaching_csv'] <-
    UNFCCC CRT Tables 3.D/3.B(b) (data_loader.py's crt_nr_ag method, reading
    directly from the NOR-CRT-2026-... folder). value_col is 'Nr_SM' or 'Nr_MM'.
    With utmark_losses (soil management only), leaching from grazing manure
    on utmark is left out.
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
        if utmark_losses is not None:
            base_value -= utmark_losses[year]['leaching']
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

    # 'fao_animal_production_clean' <- data_files/FAOSTAT_data_en_9-24-2026.csv
    # (Crop and livestock products: production quantity, restricted in
    # data_loader.py to individual livestock products, no aggregates)
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

    # 'fao_hides_clean' <- data_files/FAOSTAT_data_en_9-24-2026.csv (Crop and
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
    
def _add_manure_application_flow_mc(results, preloaded_data, current_params, dataset_noise, utmark_losses):
    """
    N in managed manure applied to agricultural soil: the IPCC 2006 FAM term
    (Eq. 11.4, Volume 4 Chapter 11) - managed manure N net of losses during
    animal housing and manure storage (tracked separately as AG.MM's own
    emissions flows) - plus the share of manure deposited directly by
    grazing animals (PRP) that lands on agricultural grazing land (innmark)
    rather than unmanaged land (utmark, which goes to FS.OL in
    _add_utmark_manure_flow_mc).

    EUROSTAT's Gross Nutrient Balance reports a substantially larger figure
    for this same quantity (roughly 40-65% higher across the time series):
    its own documentation states manure excretion coefficients are gross,
    with "no reductions... made for volatilisation from the moment of
    excretion till the application to the soil" (\\citet{eurostat_gnb_glossary_2025})
    - i.e. it measures total excretion rather than what actually reaches
    the field. EUROSTAT's Norwegian series also has a reporting-methodology
    discontinuity around 2017-2020 (Norway supplied EUROSTAT with
    pre-calculated results up to 2017; EUROSTAT has calculated results
    itself from raw activity data since 2020, per personal correspondence
    with EUROSTAT), producing an artificial ~23% step between 2016 and 2020
    that does not appear in the CRT-based series used here.

    'ag_manure_applied_crt'/'ag_manure_prp_crt' <- UNFCCC CRT submission,
    Table3.D, "Animal manure applied to soils" / "Urine and dung deposited
    by grazing animals" (data_loader.py DATA_MAP)
    """
    flow_code = 'AG.MM-AG.SM-Manure application-Nmix'
    collected_years = set()
    comment = 'ok'
    data_sources = 'UNFCCC CRT Table3.D'

    fam_values = preloaded_data.get('ag_manure_applied_crt')
    prp_values = preloaded_data.get('ag_manure_prp_crt')
    noise_val = dataset_noise['UNFCCC_manure_applied']

    for year in sorted(set(fam_values) & set(prp_values)):
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)

        innmark_frac = 1.0 - utmark_losses[year]['utmark_frac']
        base_value_t = fam_values[year] + prp_values[year] * innmark_frac
        value = (base_value_t * 1.0e-3) * noise_val  # t N -> kt N

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),
            'comment': comment,
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
def _add_utmark_manure_flow_mc(results, current_params, dataset_noise, utmark_losses):
    """
    Manure deposited by grazing animals on utmark (unmanaged land), the part
    of the inventory's PRP (CRT Table3.D) that is not applied to AG.SM; see
    utmark_grazing in shared_flow_calculations.py.
    """
    flow_code = 'AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix'
    collected_years = set()
    noise_val = dataset_noise['UNFCCC_manure_applied']

    for year in sorted(utmark_losses):
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(utmark_losses[year]['manure'] * noise_val),
            'comment': 'ok',
            'data_sources': 'UNFCCC CRT Table3.D and 3.B(b), SSB'
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

    # 'fao_live_animals_export' <- data_files/FAOSTAT_data_en_9-24-2026-3.csv
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
    """
    N2 from denitrification in agricultural soils: a default loss rate per ha
    (Schäppi et al. 2025) times the agricultural area in use each year.
    'ssb_agri_area_05982' <- data_files/05982_jordbruksareal_i_drift.csv: SSB
    table 05982, agricultural area in use (daa); the table has no values for
    1990-1998, which are interpolated linearly between 1989 and 1999.
    """
    flow_code = 'AG.SM-AT.AT-Emissions-N2'
    collected_years = set()
    comment = 'ok'
    data_sources = 'Schäppi2025Ann + SSB table 05982'

    rate_kg_per_ha = float(current_params.get("denitrification_AG_N2_per_ha"))
    area_daa = preloaded_data['ssb_agri_area_05982']['jordbruksareal_i_drift_daa']
    area_daa = area_daa.reindex(range(area_daa.index.min(), area_daa.index.max() + 1)).interpolate()

    for year in sorted(EXPECTED_YEARS):
        collected_years.add(year)
        area_ha = area_daa[year] / 10.0  # daa -> ha
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': rate_kg_per_ha * area_ha * 1.0e-6,  # kg N -> kt N
            'comment': comment,
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
