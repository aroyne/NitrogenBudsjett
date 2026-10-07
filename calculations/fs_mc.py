#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Forests and semi-natural vegetation (FS) pool: forest (FS.FO) N2O/N2 emissions,
leaching, industrial round wood and fuel wood; other land (FS.OL) leaching and
grazing on utmark, and the NH3, NOx and N2O from manure deposited by grazing
animals on utmark. Other FS.OL emissions (N2, and NOx/N2O from the soils
themselves) are neglected, see forests_and_semi_natural_pool/subpool_other_land.md.
"""
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    add_flat_carryforward_year,
    load_crltap_emissions_to_N
)
from calculations.shared_flow_calculations import find_industrial_round_wood, find_teotil2_bias_corrected, utmark_grazing

def execute_calculations_fs(preloaded_data, current_params, dataset_noise):
    """
    Main function for the FS (forests and semi-natural vegetation) pool. Receives
    this round's noise dictionary for datasets.
    """
    results = []

    _add_fo_denitrification_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'FS.FO-AT.AT-Emissions-N2O', 'UNFCCC CRT')
    _add_fo_denitrification_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'FS.FO-AT.AT-Emissions-N2', 'UNFCCC CRT + Butterbach-Bahl et al. (2013)', n2_n2o_ratio_key='forest_N2_to_N2O_ratio')
    _add_land_leaching_mc(results, preloaded_data, current_params, dataset_noise, 'FS.FO-HY.SW-Leaching-Nmix', 'FO_leaching_bg_fraction', 10)
    _add_industrial_round_wood_mc(results, preloaded_data, current_params, dataset_noise)
    _add_fuel_wood_for_households_mc(results, preloaded_data, current_params, dataset_noise)
    _add_land_leaching_mc(results, preloaded_data, current_params, dataset_noise, 'FS.OL-HY.SW-Leaching-Nmix', 'OL_leaching_bg_fraction', 8)
    _add_ol_grazing_mc(results, preloaded_data, current_params, dataset_noise)
    _add_utmark_grazing_emissions_mc(results, preloaded_data, current_params, dataset_noise)

    return results


def _add_utmark_grazing_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    """
    NH3, NOx and N2O from manure deposited by grazing animals on utmark
    (AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix). The inventory
    reports these as part of the emissions from grazing animals on managed
    soils (NFR 3Da3, CRT 3.D); the utmark share is removed from the AG.SM
    flows in ag_mc.py and counted here. NH3 and NOx are the utmark share of
    3Da3 in the CLRTAP inventory, and N2O is calculated in utmark_grazing
    (shared_flow_calculations.py). Leaching from this manure is part of
    FS.OL-HY.SW-Leaching-Nmix (TEOTIL3 upland).
    """
    utmark = utmark_grazing(preloaded_data, current_params)
    # 'ag_crltap_raw_lines' <- webdabData1868031.txt (data_loader.py DATA_MAP):
    # CLRTAP inventory submissions
    raw_lines = preloaded_data['ag_crltap_raw_lines']

    for pollutant in ('NH3', 'NOx'):
        flow_code = f'FS.OL-AT.AT-Emissions-{pollutant}'
        collected_years = set()
        grazing = load_crltap_emissions_to_N(
            raw_lines=raw_lines, categories=['3Da3'], pollutant=pollutant,
            conv_to_N=float(current_params.get(f"{pollutant}_to_N_factor")),
            dataset_noise=dataset_noise, noise_key='CRLTAP'
        )
        for year, value in grazing.items():
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            results.append({
                'flow_name': flow_code, 'year': year,
                'value': float(value * utmark[year]['utmark_frac']),
                'comment': 'ok', 'data_sources': 'CRLTAP Inventory Submissions (3Da3), utmark share'
            })
        report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)

    flow_code = 'FS.OL-AT.AT-Emissions-N2O'
    collected_years = set()
    noise_val = dataset_noise['UNFCCC_N2O_agri_soils']
    for year in sorted(utmark):
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year,
            'value': float(utmark[year]['n2o'] * noise_val),
            'comment': 'ok', 'data_sources': 'UNFCCC CRT Table3.D, utmark share'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_fo_denitrification_emissions_mc(results, preloaded_data, current_params, dataset_noise, flow_code, data_sources, n2_n2o_ratio_key=None):
    """
    Shared implementation for FS.FO forest-soil denitrification emissions (N2O and
    N2, both reported by UNFCCC CRT Table 4 for forest land).
    preloaded_data['fs_unfccc_emissions_raw'] <- UNFCCC CRT Table4
    (data_loader.py's crt_n2o_hs_fs method, reading directly from the
    NOR-CRT-2026-... folder), column 3 = FS.FO N2O (kt).
    N2 is not reported directly - it is estimated as a fixed N2:N2O ratio applied
    to the same N2O series (n2_n2o_ratio_key='forest_N2_to_N2O_ratio', ratio 19.5
    per Schäppi et al. 2025); pass n2_n2o_ratio_key=None for the N2O flow itself.
    """
    collected_years = set()
    dataset_key = 'UNFCCC_N2O_lulucf'

    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    N2O_to_N = float(current_params.get("N2O_to_N_factor"))
    n2_n2o_ratio = float(current_params.get(n2_n2o_ratio_key)) if n2_n2o_ratio_key else 1.0

    for row in range(len(df_unfccc)):
        year = int(df_unfccc.iloc[row, 0])
        collected_years.add(year)

        raw_val = float(df_unfccc.iloc[row, 3])
        noise_val = dataset_noise[dataset_key]
        perturbed_raw = raw_val * noise_val

        value = perturbed_raw * N2O_to_N * n2_n2o_ratio

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
        
def _add_land_leaching_mc(results, preloaded_data, current_params, dataset_noise, flow_code, frac_key, teotil3_col):
    """
    Forest (FS.FO) or other land (FS.OL) leaching to surface water, selected by
    flow_code/frac_key/teotil3_col. Two data eras:
    - 1990-2012: TEOTIL2 natural diffuse loss (forest, mountain, lakes and
      agricultural background, not split by land type), bias-corrected to the
      TEOTIL3 wood + upland level, see find_teotil2_bias_corrected in
      shared_flow_calculations.py. Each land type's share of this is a fixed
      fraction (frac_key: FO_leaching_bg_fraction ~ 0.59,
      OL_leaching_bg_fraction ~ 0.41), matching wood's share of wood + upland
      in TEOTIL3 (0.56-0.60 over 2013-2023).
    - 2013-2023: preloaded_data['hy_teotil3_by_source'] <- data_files/
      teotil3_n_summary.xlsx, teotil3_col = 10 ('wood_totn_tonnes') for
      forest and 8 ('upland_totn_tonnes': mountain, heath and wetland) for
      other land.
    The two eras must not overlap: the TEOTIL2 series stops at the year before
    TEOTIL3 starts. A shared year in both loops would add two rows for that
    year within a single simulation, biasing its MC median/CI (see the
    groupby(['flow_name', 'year']) aggregation in utils_stat.py).
    """
    collected_years = set()
    data_sources = 'TEOTIL'
    dataset_key = 'TEOTIL'

    teotil2 = find_teotil2_bias_corrected(preloaded_data)
    df_teotil3 = preloaded_data.get('hy_teotil3_by_source')

    frac = float(current_params.get(frac_key))

    # 1990-2012 (TEOTIL2, bias-corrected)
    for year, raw_val in teotil2['forest_and_other_land'].items():
        year = int(year)
        collected_years.add(year)

        noise_val = dataset_noise[dataset_key]
        perturbed_raw = raw_val * noise_val

        value = perturbed_raw * frac

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': 'NIVA TEOTIL2, bias-corrected to TEOTIL3'
        })

    # 2013-2023 (TEOTIL3, row 0 is the header, rows 1-11 = years 2013-2023)
    for r in range(1, 12):
        year = int(df_teotil3.iloc[r, 0])
        collected_years.add(year)

        raw_val = float(df_teotil3.iloc[r, teotil3_col]) / 1000
        noise_val = dataset_noise[dataset_key]
        value = raw_val * noise_val

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': data_sources
        })

    # TEOTIL3 has not been updated for 2024; carry the 2023 value forward
    # with extra uncertainty rather than leave the flow silent for a year
    # the source will eventually cover.
    add_flat_carryforward_year(
        results, flow_code, collected_years, 2023, 2024, dataset_noise,
        data_sources='flat carry-forward from 2023 (TEOTIL3 not updated for 2024)'
    )

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_industrial_round_wood_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-MP.OP-Industrial round wood-Nmix'
    collected_years = set()

    # find_industrial_round_wood (shared_flow_calculations.py) reads
    # preloaded_data['faostat_forestry'] <- data_files/FAOSTAT_data_en_2-20-2026.csv
    # (Forestry production and trade)
    year_values = find_industrial_round_wood(preloaded_data, current_params, dataset_noise)
    
    for year, value in year_values.items():
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': 'FAOSTAT'
        })
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_fuel_wood_for_households_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-EF.OE-Fuel wood for households-Nmix'
    collected_years = set()
    data_sources = 'SSB'
    dataset_key = '09702'

    # 'fs_firewood_raw' <- data_files/09702_20251120-133716.xlsx: SSB table 09702,
    # firewood consumption in residences and holiday homes (1000 tonnes/year)
    df_ved = preloaded_data.get('fs_firewood_raw')
    # Fuel wood is mainly stem wood with bark, so the stem N content is used,
    # not the whole-tree value (which includes foliage and branches).
    N_content = float(current_params.get("household_fuelwood_N_frac"))

    # rows 3-37 = years 1990-2024
    for r in range(3, 38):
        year = int(df_ved.iloc[r, 0]) 
        collected_years.add(year)
        
        raw_val = float(df_ved.iloc[r, 1])
        noise_val = dataset_noise[dataset_key]
        perturbed_raw = raw_val * noise_val
        
        value = perturbed_raw * N_content 
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value, 
            'comment': 'ok', 'data_sources': data_sources
        })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


    
def _add_ol_grazing_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Feed taken up by livestock grazing on utmark. Hegrenes & Asheim (2006,
    Table 1.2, after Garmo & Skurdal 1998) estimate 303 mill. FEm taken up on
    utmark in 1996 by all grazing animals, 70% by sheep, 27% by cattle, 2% by
    goats and 1% by horses (fu_<animal>_1996). Dividing each group's share by
    the number of animals on utmark in 1996 gives FEm per animal, which is
    applied to every year's number of animals and converted to N via 150 g
    protein per FEm (protein_cont_grazing) and the Jones factor.

    Animal numbers are from SSB table 12660 (all animals with production
    subsidy for at least 8 weeks on utmark up to 2008 and 5 weeks from 2009;
    sheep include lambs; goats and horses are reported together), 1995-2025.
    For 1990-1994 sheep are extrapolated back from 1995 with the change in
    the number of winter-fed sheep (SSB table 03710); cattle, goats and
    horses are held at the 1995 level.

    Reindeer graze on utmark all year but are not covered by the estimate
    above; their uptake is set equal to their N excretion in the national
    inventory (CRT Table3.B(b), all deposited during grazing), since only a
    small part of the N is retained in the animals.
    """
    flow_code = 'FS.OL-AG.MM-Grazing-Nmix'
    collected_years = set()
    data_sources = 'SSB table 12660'
    noise_ssb = dataset_noise['12660']
    Jones = float(current_params.get("Jones_factor"))
    protein_cont = float(current_params.get("protein_cont_grazing")) * 1e-9  # g protein/FEm -> kt protein/FEm

    fem_1996 = {
        'sauer': float(current_params.get("fu_sheep_1996")) * 1e6,
        'storfe': float(current_params.get("fu_cattle_1996")) * 1e6,
        'geit_og_hest': (float(current_params.get("fu_goat_1996")) + float(current_params.get("fu_horse_1996"))) * 1e6,
    }

    # 'ssb_utmark_animals_12660' <- data_files/12660_husdyr_utmarksbeite.csv
    animals = preloaded_data['ssb_utmark_animals_12660']
    fem_per_animal = {group: fem_1996[group] / animals.loc[1996, group] for group in fem_1996}

    # Sheep in 1990-1994 follow the number of winter-fed sheep:
    # 'ssb_sheep_numbers' <- data_files/03710_20260128-152225.xlsx (SSB table
    # 03710). Cattle, goats and horses are held at the 1995 level, since no
    # national series for them on utmark exists before 1995 (the organised
    # grazing statistics grew in the early 1990s as more farmers joined
    # grazing associations, so they do not show the number of animals).
    df_sheep = preloaded_data['ssb_sheep_numbers'].dropna(subset=['År'])
    sheep_index = dict(zip(df_sheep['År'].astype(int), df_sheep['Husdyr (sau)'].astype(float)))

    # 'ag_prp_by_category_crt' <- UNFCCC CRT submission, Table3.B(b), N
    # deposited during grazing per animal category (kg N/yr)
    reindeer_kt = {year: cats['3.B.4.h.ii.'] * 1e-6
                   for year, cats in preloaded_data['ag_prp_by_category_crt'].items()}
    noise_crt = dataset_noise['UNFCCC_manure_applied']

    first_year = int(animals.index.min())
    for year in range(1990, 2026):
        if year >= first_year:
            n = {group: animals.loc[year, group] * noise_ssb for group in fem_1996}
            src = data_sources
        else:
            n = {group: animals.loc[first_year, group] * noise_ssb for group in fem_1996}
            n['sauer'] *= sheep_index[year] / sheep_index[first_year]
            src = 'SSB table 12660, 1995 level; sheep scaled with SSB table 03710'
        fem = sum(n[group] * fem_per_animal[group] for group in fem_1996)
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year,
            'value': fem * protein_cont / Jones + reindeer_kt.get(year, 0.0) * noise_crt,
            'comment': 'ok', 'data_sources': src
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)