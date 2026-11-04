#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Forests and semi-natural vegetation (FS) pool: forest (FS.FO) N2O/N2 emissions,
leaching, industrial round wood and fuel wood; other land (FS.OL) leaching and
grazing on utmark, and the NH3, NOx and N2O from manure deposited by grazing
animals on utmark. Other FS.OL emissions (N2, and NOx/N2O from the soils
themselves) are neglected, see forests_and_semi_natural_pool/subpool_other_land.md.
"""
import pandas as pd

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    add_flat_carryforward_year,
    load_crltap_emissions_to_N
)
from calculations.shared_flow_calculations import find_industrial_round_wood, find_teotil2_bias_corrected, utmark_grazing, utmark_grazing_uptake

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
    _add_fuel_wood_for_heat_plants_mc(results, preloaded_data, current_params, dataset_noise)
    _add_land_leaching_mc(results, preloaded_data, current_params, dataset_noise, 'FS.OL-HY.SW-Leaching-Nmix', 'OL_leaching_bg_fraction', 8)
    _add_ol_grazing_mc(results, preloaded_data, current_params, dataset_noise)
    _add_game_meat_mc(results, preloaded_data, current_params, dataset_noise)
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
    utmark = utmark_grazing(preloaded_data, current_params, dataset_noise)
    # 'ag_crltap_raw_lines' <- webdabData1868031.txt (data_loader.py DATA_MAP):
    # CLRTAP inventory submissions
    raw_lines = preloaded_data['ag_crltap_raw_lines']

    for pollutant in ('NH3', 'NOx'):
        flow_code = f'FS.OL-AT.AT-Emissions-{pollutant}'
        collected_years = set()
        grazing = load_crltap_emissions_to_N(
            raw_lines=raw_lines, categories=['3Da3'], pollutant=pollutant,
            conv_to_N=float(current_params.get(f"{pollutant}_to_N_factor")),
            dataset_noise=dataset_noise
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
    for year in sorted(utmark):
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year,
            'value': float(utmark[year]['n2o'] * dataset_noise.factor('UNFCCC_N2O_agri_soils', year)),
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
        perturbed_raw = raw_val * dataset_noise.factor(dataset_key, year)

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
    dataset_key = 'TEOTIL:natural'

    teotil2 = find_teotil2_bias_corrected(preloaded_data, dataset_noise)
    df_teotil3 = preloaded_data.get('hy_teotil3_by_source')

    frac = float(current_params.get(frac_key))

    # 1990-2012 (TEOTIL2, bias-corrected)
    for year, raw_val in teotil2['forest_and_other_land'].items():
        year = int(year)
        collected_years.add(year)

        perturbed_raw = raw_val * dataset_noise.factor(dataset_key, year)

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
        value = raw_val * dataset_noise.factor(dataset_key, year)

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': data_sources
        })

    # TEOTIL3 has not been updated for 2024; carry the 2023 value forward
    # with extra uncertainty rather than leave the flow silent for a year
    # the source will eventually cover.
    add_flat_carryforward_year(
        results, flow_code, collected_years, 2023, 2024, dataset_noise,
        data_sources='TEOTIL3 not updated for 2024'
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
    data_sources = 'SSB; UNFCCC CRT'
    dataset_key = '09702'

    # 'fs_firewood_raw' <- data_files/09702_20251120-133716.xlsx: SSB table 09702,
    # firewood consumption in residences and holiday homes (1000 tonnes/year)
    df_ved = preloaded_data.get('fs_firewood_raw')
    # Fuel wood is mainly stem wood with bark, so the stem N content is used,
    # not the whole-tree value (which includes foliage and branches).
    N_content = float(current_params.get("household_fuelwood_N_frac"))

    # Wood pellets and chips burned in commercial/institutional buildings and
    # in agriculture, forestry and fishing are added here, as Schäppi et al.
    # (2025, chapter 4.4.4) suggest one flow to EF.OE when households dominate.
    # 'fuel_wood_other_sectors' <- NOR-CRT-2026 submission folder (data_loader.py
    # DATA_MAP): Table1.A(a)s4, 1.A.4.a and 1.A.4.c Biomass, consumption in TJ
    df_other = preloaded_data['fuel_wood_other_sectors']
    NCV = float(current_params.get('firewood_NCV'))
    N_other = float(current_params.get('heat_plant_wood_N_frac'))
    other_sectors = {}
    for year, tj in zip(df_other.year, df_other.TJ):
        other_sectors[int(year)] = other_sectors.get(int(year), 0.0) + tj / NCV * N_other * dataset_noise.factor('UNFCCC_fuel', int(year))

    # rows 3-37 = years 1990-2024
    for r in range(3, 38):
        year = int(df_ved.iloc[r, 0]) 
        collected_years.add(year)
        
        raw_val = float(df_ved.iloc[r, 1])
        perturbed_raw = raw_val * dataset_noise.factor(dataset_key, year)
        
        value = perturbed_raw * N_content + other_sectors[year]
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value, 
            'comment': 'ok', 'data_sources': data_sources
        })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_fuel_wood_for_heat_plants_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Wood fuel burned in heat and power plants (CRT 1.A.1.a biomass). The fuel
    is energy wood, bark, branches and tops and wood chips. Energy wood
    ("rundvirke til flis", SSB table 14641) and bark are not part of the
    industrial roundwood under bark in FS.FO-MP.OP, so the flow is counted
    in full from the forest.
    """
    flow_code = 'FS.FO-EF.EC-Fuel wood for co-fired power plants-Nmix'
    collected_years = set()

    # 'fuel_wood_heat_plants' <- NOR-CRT-2026 submission folder (data_loader.py
    # DATA_MAP): Table1.A(a)s1, 1.A.1.a Biomass, consumption in TJ
    df = preloaded_data['fuel_wood_heat_plants']
    NCV = float(current_params.get('firewood_NCV'))
    N_content = float(current_params.get('heat_plant_wood_N_frac'))

    for year, tj in zip(df.year, df.TJ):
        year = int(year)
        collected_years.add(year)
        value = tj / NCV * N_content * dataset_noise.factor('UNFCCC_fuel', year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': 'UNFCCC CRT'
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)



def _add_game_meat_mc(results, preloaded_data, current_params, dataset_noise):
    """
    N in meat from big game shot in ordinary hunting, eaten in households.
    Moose, red deer and roe deer are counted from forest (FS.FO), wild
    reindeer from other land (FS.OL). Small game is left out (a few hundred
    tonnes of meat per year, well below 0.01 kt N).

    'ssb_hunting' <- jaktstatistikk_storvilt.csv (data_loader.py DATA_MAP,
    downloaded by data_files/ssb_jaktstatistikk.py): SSB calculated total
    carcass weight of moose and red deer (tables 10817, 10818, from the
    1998-1999 season) and wild reindeer (10820, from 1986-1987), and the
    number of moose, red deer and roe deer shot (06036, 06037, 03947). Each
    season is assigned to the year it starts.

    Before 1998 moose and red deer are the number shot times the average
    carcass weight per animal shot in 1998-2002. Roe deer are the number shot
    times roe_deer_carcass_weight; the 2016 season, which is missing in
    table 03947, is interpolated, and the 2023 and 2024 seasons, which are
    not yet in the table, are held at the 2022 level.
    """
    df = preloaded_data['ssb_hunting']
    n_frac = float(current_params.get('game_meat_N_frac'))
    roe_weight_t = float(current_params.get('roe_deer_carcass_weight')) / 1000.0
    key = 'SSB_jaktstatistikk'

    first_carcass = int(df['elg_slaktevekt_t'].first_valid_index())
    calib = list(range(first_carcass, first_carcass + 5))
    weight_per_animal = {sp: df.loc[calib, f'{sp}_slaktevekt_t'].sum() / df.loc[calib, f'{sp}_felt'].sum()
                         for sp in ('elg', 'hjort')}
    last_roe = int(df['radyr_felt'].last_valid_index())

    forest, other = {}, {}
    for year in sorted(EXPECTED_YEARS):
        if year not in df.index:
            continue
        sources = []
        tonnes = 0.0
        for sp in ('elg', 'hjort'):
            if year >= first_carcass:
                tonnes += df.loc[year, f'{sp}_slaktevekt_t']
            else:
                fill = dataset_noise.fill('extrapolation', f'game meat {sp} <{first_carcass}', year, calib)
                tonnes += df.loc[year, f'{sp}_felt'] * weight_per_animal[sp] * fill
                sources.append(f'Filled (number shot times carcass weight per animal, from {calib[0]}-{calib[-1]})')
        if pd.notna(df.loc[year, 'radyr_felt']):
            tonnes += df.loc[year, 'radyr_felt'] * roe_weight_t
        elif year < last_roe:
            # A season missing inside the series (2016): linear interpolation
            # between the neighbouring seasons.
            roe = df['radyr_felt'].dropna()
            before = max(y for y in roe.index if y < year)
            after = min(y for y in roe.index if y > year)
            n_roe = roe[before] + (roe[after] - roe[before]) * (year - before) / (after - before)
            fill = dataset_noise.fill('interpolation', f'game meat roe deer {before}-{after}', year, [before, after])
            tonnes += n_roe * roe_weight_t * fill
            sources.append(f'Filled (roe deer interpolated between {before} and {after})')
        else:
            fill = dataset_noise.fill('carry', f'game meat roe deer {last_roe}+', year, [last_roe])
            tonnes += df.loc[last_roe, 'radyr_felt'] * roe_weight_t * fill
            sources.append(f'Filled (roe deer held at {last_roe})')
        factor = dataset_noise.factor(key, year)
        src = '; '.join(sorted(set(sources)) + ['SSB hunting statistics'])
        forest[year] = (tonnes * 1e-3 * n_frac * factor, src)
        if pd.notna(df.loc[year, 'villrein_slaktevekt_t']):
            other[year] = (df.loc[year, 'villrein_slaktevekt_t'] * 1e-3 * n_frac * factor, 'SSB hunting statistics')

    for flow_code, values in (('FS.FO-HS.HS-Game meat-Nmix', forest), ('FS.OL-HS.HS-Game meat-Nmix', other)):
        for year, (value, src) in values.items():
            results.append({'flow_name': flow_code, 'year': year, 'value': float(value),
                            'comment': 'ok', 'data_sources': src})
        report_missing_years(flow_code, EXPECTED_YEARS - set(values), results)


def _add_ol_grazing_mc(results, preloaded_data, current_params, dataset_noise):
    """Feed taken up by livestock grazing on utmark; see utmark_grazing_uptake
    in shared_flow_calculations.py."""
    flow_code = 'FS.OL-AG.MM-Grazing-Nmix'
    collected_years = set()
    for year, (value, src) in utmark_grazing_uptake(preloaded_data, current_params, dataset_noise).items():
        collected_years.add(year)
        results.append({'flow_name': flow_code, 'year': year, 'value': value,
                        'comment': 'ok', 'data_sources': src})

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)