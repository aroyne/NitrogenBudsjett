#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Forests and semi-natural vegetation (FS) pool: forest (FS.FO) N2O/N2 emissions,
leaching, industrial round wood and fuel wood; other land (FS.OL) leaching and
organised grazing. FS.OL has no atmospheric emissions flows here - NOx, N2 and
N2O are deliberately neglected as negligible/unreported, see
forests_and_semi_natural_pool/subpool_other_land.md for the reasoning and sources.
"""
import numpy as np

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years
)
from calculations.shared_flow_calculations import find_industrial_round_wood

def execute_calculations_fs(preloaded_data, current_params, dataset_noise):
    """
    Main function for the FS (forests and semi-natural vegetation) pool. Receives
    this round's noise dictionary for datasets.
    """
    results = []

    _add_fo_denitrification_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'FS.FO-AT.AT-Emissions-N2O', 'UNFCCC CRT')
    _add_fo_denitrification_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'FS.FO-AT.AT-Emissions-N2', 'UNFCCC CRT + Butterbach-Bahl et al. (2013)', n2_n2o_ratio_key='forest_N2_to_N2O_ratio')
    _add_land_leaching_mc(results, preloaded_data, current_params, dataset_noise, 'FS.FO-HY.SW-Leaching-Nmix', 'FO_leaching_bg_fraction')
    _add_industrial_round_wood_mc(results, preloaded_data, current_params, dataset_noise)
    _add_fuel_wood_for_households_mc(results, preloaded_data, current_params, dataset_noise)
    _add_land_leaching_mc(results, preloaded_data, current_params, dataset_noise, 'FS.OL-HY.SW-Leaching-Nmix', 'OL_leaching_bg_fraction')
    _add_ol_grazing_mc(results, preloaded_data, current_params, dataset_noise)

    return results


def _add_fo_denitrification_emissions_mc(results, preloaded_data, current_params, dataset_noise, flow_code, data_sources, n2_n2o_ratio_key=None):
    """
    Shared implementation for FS.FO forest-soil denitrification emissions (N2O and
    N2, both reported by UNFCCC CRT Table 4 for forest land).
    preloaded_data['fs_unfccc_emissions_raw'] <- data_files/N2O_NOx_HS_FS.xlsx,
    column 3 = FS.FO N2O (kt), rows 5-38 = years 2023 down to 1990.
    N2 is not reported directly - it is estimated as a fixed N2:N2O ratio applied
    to the same N2O series (n2_n2o_ratio_key='forest_N2_to_N2O_ratio', ratio 19.5
    per Schäppi et al. 2025); pass n2_n2o_ratio_key=None for the N2O flow itself.
    """
    collected_years = set()
    dataset_key = 'UNFCCC_N2O_lulucf'

    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    N2O_to_N = float(current_params.get("N2O_to_N_factor"))
    n2_n2o_ratio = float(current_params.get(n2_n2o_ratio_key)) if n2_n2o_ratio_key else 1.0

    for row in range(5, 39):
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
    
        
def _add_land_leaching_mc(results, preloaded_data, current_params, dataset_noise, flow_code, frac_key):
    """
    Forest (FS.FO) or other land (FS.OL) leaching to surface water, selected by
    flow_code/frac_key. Two data eras, per Sample et al. (2024):
    - 1990-2012: preloaded_data['hy_kyst_tilforsel'] <- data_files/Tilførsel av
      nitrogen til kystområdene fordelt på kilder.xlsx (Miljødirektoratet's older
      "Kysttilførsel" compilation), column 3 = 'Bakgrunn' (diffuse background N
      loading, not split by land type). Each land type's share of this is
      estimated as a fixed fraction (frac_key: FO_leaching_bg_fraction ~ 0.59,
      OL_leaching_bg_fraction ~ 0.42), calibrated by comparing to the newer
      TEOTIL3 split over the overlapping 2013-2023 period.
    - 2013-2023: preloaded_data['hy_teotil3_by_source'] <- data_files/
      teotil3_n_summary.xlsx, column 10 = 'wood_totn_tonnes'. TEOTIL3 does not
      split forest from other land, so this same column is the source for both
      flows - FS.FO and FS.OL leaching are identical for 2013-2023 by
      construction, not by coincidence.
    The two eras must not overlap at 2013: Kysttilførsel stops at 2012 so TEOTIL3
    is the sole source for 2013 onward. A shared year in both loops would add two
    rows for that year within a single simulation, biasing its MC median/CI (see
    the groupby(['flow_name', 'year']) aggregation in utils_stat.py).
    """
    collected_years = set()
    data_sources = 'TEOTIL'
    dataset_key = 'TEOTIL'

    df_kyst = preloaded_data.get('hy_kyst_tilforsel')
    df_teotil3 = preloaded_data.get('hy_teotil3_by_source')

    frac = float(current_params.get(frac_key))

    # 1990-2012 (Kysttilførsel, rows 0-22)
    for r in range(0, 23):
        year = int(df_kyst.iloc[r, 0])
        collected_years.add(year)

        raw_val = float(df_kyst.iloc[r, 3]) / 1000
        noise_val = dataset_noise[dataset_key]
        perturbed_raw = raw_val * noise_val

        value = perturbed_raw * frac

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': data_sources
        })

    # 2013-2023 (TEOTIL3, row 0 is the header, rows 1-11 = years 2013-2023)
    for r in range(1, 12):
        year = int(df_teotil3.iloc[r, 0])
        collected_years.add(year)

        raw_val = float(df_teotil3.iloc[r, 10]) / 1000
        noise_val = dataset_noise[dataset_key]
        value = raw_val * noise_val

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': data_sources
        })

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
    N_content = float(current_params.get("firewood_N_frac"))

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
    Organised grazing (NIBIO beitestatistikk) combined with estimated fodder
    intake per animal group from Table 1.2 in Hegrenes & Asheim (2006).
    Feed units (FEm) per animal are calibrated once, using 1996 national FEm
    totals (fu_<animal>_1996, from Hegrenes & Asheim) divided by the 1996
    released-animal counts read from the OBB grazing statistics below. That
    per-animal FEm rate is then applied to every year's animal counts to get
    total feed units grazed, converted to N via an average protein content of
    150 g per FEm (protein_cont_grazing) and the Jones factor.
    """
    flow_code = 'FS.OL-AG.MM-Grazing-Nmix'
    collected_years = set()
    data_sources = 'NIBIO'
    dataset_key = 'beitestatistikk'
    noise_val = dataset_noise[dataset_key]
    Jones = float(current_params.get("Jones_factor"))
    
    fu_sheep_1996 = float(current_params.get("fu_sheep_1996")) * 1e6
    fu_cattle_1996 = float(current_params.get("fu_cattle_1996")) * 1e6
    fu_goat_1996 = float(current_params.get("fu_goat_1996")) * 1e6   

    protein_cont = float(current_params.get("protein_cont_grazing")) * 1e-9

    sau, lam, storfe, geit = {}, {}, {}, {}

    # preloaded_data['obb_<sheet>_raw'] <- data_files/OBB_Fylke_1970-2025.xlsx
    # (Landbruksdirektoratet, Organisert beitebruk), one sheet per animal group
    # and decade. Column layout differs by decade, hence the varying row_idx and
    # column strides below; row_idx selects the national-total row (summed
    # across counties) for released ("sleppt") sheep/lamb counts that year.
    def extract_sau_lam(df, cols, row_idx):
        for col in cols:
            year = int(df.iloc[0, col])
            r_sau = float(df.iloc[row_idx, col-3])
            r_lam = float(df.iloc[row_idx, col-2])
            sau[year] = r_sau * noise_val
            lam[year] = r_lam * noise_val

    extract_sau_lam(preloaded_data['obb_Sau1990-99_raw'], range(6, 100, 10), 21)
    extract_sau_lam(preloaded_data['obb_Sau2000-09_raw'], range(6, 100, 10), 22)
    extract_sau_lam(preloaded_data['obb_Sau2010-19_raw'], range(6, 100, 10), 22)
    extract_sau_lam(preloaded_data['obb_Sau2020-29_raw'], range(6, 60, 10), 13)

    # Cattle (storfe) and goat (geit) counts come from separate sheets in the
    # same workbook, again with the national-total row selected per decade.
    df_sg_old = preloaded_data.get('obb_Storfe og geit1993-2019_raw')

    for col in range(4, 59, 6):
        year = int(df_sg_old.iloc[0, col])
        r_st = float(df_sg_old.iloc[23, col-2])
        r_gt = float(df_sg_old.iloc[23, col-1])
        storfe[year] = r_st * noise_val
        geit[year] = r_gt * noise_val
        
    for col in range(66, 200, 8):
        year = int(df_sg_old.iloc[0, col])
        r_st = float(df_sg_old.iloc[23, col-2])
        r_gt = float(df_sg_old.iloc[23, col-1])
        storfe[year] = r_st * noise_val
        geit[year] = r_gt * noise_val

    df_sg_new = preloaded_data.get('obb_Storfe og geit2020-29_raw')
        
    for col in range(6, 49, 8):
        year = int(df_sg_new.iloc[0, col])
        r_st = float(df_sg_new.iloc[13, col-2])
        r_gt = float(df_sg_new.iloc[13, col-1])
        storfe[year] = r_st * noise_val
        geit[year] = r_gt * noise_val

    # Linear backward extrapolation for the missing years (1990-1992)
    for animal_dict in [storfe, geit]:
        years = np.array(list(animal_dict.keys()), dtype=float)
        y = np.array(list(animal_dict.values()), dtype=float)    
        a, b = np.polyfit(years, y, 1)    
        for y_back in [1990, 1991, 1992]:
            animal_dict[y_back] = a * y_back + b

    # Ewes are released to outfield pasture together with their lambs, and a
    # lamb's feed unit is assumed equal in size to an adult sheep's, so both are
    # calibrated from the same fu_sheep_1996 reference total against their
    # respective 1996 counts and later summed as equivalent grazing animals.
    fu_sheep = fu_sheep_1996 / sau[1996]
    fu_lamb = fu_sheep_1996 / lam[1996]
    fu_cattle = fu_cattle_1996 / storfe[1996]
    fu_goat = fu_goat_1996 / geit[1996]

    for year in range(1990, 2026):            
        collected_years.add(year)
        value = (sau[year]*fu_sheep + lam[year]*fu_lamb + storfe[year]*fu_cattle + geit[year]*fu_goat) * protein_cont / Jones
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value, 
            'comment': 'ok', 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)