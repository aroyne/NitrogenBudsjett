#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MC-VERSJON: Beregner nitrogenflyt for skog og utmark (FS).
Rådata ligger i preloaded_data, mens støyfaktorer for hvert datasett sendes inn via dataset_noise.
"""
import pandas as pd
import numpy as np

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years
)
from calculations.shared_flow_calculations import find_industrial_round_wood

def execute_calculations_fs(preloaded_data, current_params, dataset_noise):
    """
    Hovedfunksjon for FS-poolen (MC). Mottar denne rundens støyordbok for datasett.
    """
    results = []
    
    _add_fo_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_fo_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_fo_leaching_mc(results, preloaded_data, current_params, dataset_noise)
    _add_industrial_round_wood_mc(results, preloaded_data, current_params, dataset_noise)  # Går via shared parameter-MC
    _add_fuel_wood_for_households_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ol_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ol_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ol_leaching_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ol_grazing_mc(results, preloaded_data, current_params, dataset_noise)

    return results


def _apply_dataset_noise(base_value, dataset_key, dataset_noise, caller_func):
    """
    Legger støy på verdi. Krasjer hardt dersom støy-nøkkel mangler.
    """
    if not dataset_noise or dataset_key not in dataset_noise:
        raise KeyError(
            f"[KRITISK FEIL] Støy-nøkkel '{dataset_key}' mangler i dataset_noise under kallet fra {caller_func.__name__}!"
        )

    noise_info = dataset_noise[dataset_key]
    noise_val = noise_info['value']
    
    if noise_info['type'] == 'perc':
        return base_value * noise_val
    else:
        bound = noise_info['upp_bound'] if noise_val >= 0 else noise_info['low_bound']
        return base_value + (noise_val * bound)


def _add_fo_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-AT.AT-Emissions-N2O'
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    dataset_key = 'UNFCCC_emissions'
    
    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    if df_unfccc is None:
        raise ValueError(f"[KRITISK] Data 'fs_unfccc_emissions_raw' mangler i preloaded_data for {flow_code}!")

    N2O_to_N = float(current_params.get("N2O_to_N_factor"))
    
    for row in range(4, 38):  
        year = int(df_unfccc.iloc[row, 0])
        collected_years.add(year)
        
        raw_val = float(df_unfccc.iloc[row, 3])
        perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_fo_N2O_emissions_mc)
        
        value = perturbed_raw * N2O_to_N
        if value < 0: value = 0.0
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
        })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_fo_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-AT.AT-Emissions-N2'
    collected_years = set()
    data_sources = 'UNFCCC CRT + Butterbach-Bahl et al. (2013)'
    dataset_key = 'UNFCCC_emissions'

    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    if df_unfccc is None:
        raise ValueError(f"[KRITISK] Data 'fs_unfccc_emissions_raw' mangler i preloaded_data for {flow_code}!")

    N2O_to_N = float(current_params.get("N2O_to_N_factor"))
    ratio = float(current_params.get("forest_N2_to_N2O_ratio"))

    for row in range(4, 38):
        year = int(df_unfccc.iloc[row, 0])
        collected_years.add(year)
        
        raw_val = float(df_unfccc.iloc[row, 3])
        perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_fo_N2_emissions_mc)
        
        value = perturbed_raw * N2O_to_N * ratio
        if value < 0: value = 0.0
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
        
def _add_fo_leaching_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-HY.SW-Leaching-Nmix'
    collected_years = set()
    data_sources = 'TEOTIL'
    dataset_key = 'TEOTIL'
    
    df_kyst = preloaded_data.get('hy_kyst_tilforsel')
    df_teotil3 = preloaded_data.get('hy_teotil3_by_source')
    if df_kyst is None or df_teotil3 is None:
        raise ValueError(f"[KRITISK] Koblingsdata ('hy_kyst_tilforsel' eller 'hy_teotil3_by_source') mangler for {flow_code}!")

    frac = float(current_params.get("FO_leaching_bg_fraction"))
    
    # Historiske år (Kysttilførsel)
    for r in range(0, 24):
        year = int(df_kyst.iloc[r, 0]) 
        collected_years.add(year)
        
        raw_val = float(df_kyst.iloc[r, 3]) / 1000
        perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_fo_leaching_mc)
        
        value = perturbed_raw * frac
        if value < 0: value = 0.0

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value, 
            'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
        })
            
    # Nyere år (TEOTIL3)
    for r in range(1, 12):
        year = int(df_teotil3.iloc[r, 0]) 
        collected_years.add(year)
        
        raw_val = float(df_teotil3.iloc[r, 10]) / 1000 
        value = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_fo_leaching_mc)
        if value < 0: value = 0.0

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value, 
            'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
        })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_industrial_round_wood_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-MP.OP-Industrial round wood-Nmix'
    collected_years = set()   
    
    year_values, _ = find_industrial_round_wood(preloaded_data, current_params, dataset_noise)
    
    for year, value in year_values.items():
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på via parametere)', 'data_sources': 'FAOSTAT'
        })
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_fuel_wood_for_households_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-EF.OE-Fuel wood for households-Nmix'
    collected_years = set()
    data_sources = 'SSB'
    dataset_key = '09702'
    
    df_ved = preloaded_data.get('fs_firewood_raw')
    if df_ved is None:
        raise ValueError(f"[KRITISK] Data 'fs_firewood_raw' mangler i preloaded_data for {flow_code}!")

    N_content = float(current_params.get("firewood_N_frac"))
    
    for r in range(3, 38):  
        year = int(df_ved.iloc[r, 0]) 
        collected_years.add(year)
        
        raw_val = float(df_ved.iloc[r, 1])
        perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_fuel_wood_for_households_mc)
        
        value = perturbed_raw * N_content 
        if value < 0: value = 0.0
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value, 
            'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
        })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_ol_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.OL-AT.AT-Emissions-N2O'
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    dataset_key = 'UNFCCC_emissions'

    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    if df_unfccc is None:
        raise ValueError(f"[KRITISK] Data 'fs_unfccc_emissions_raw' mangler i preloaded_data for {flow_code}!")

    N2O_to_N = float(current_params.get("N2O_to_N_factor"))

    for row in range(5, 38):
        year = int(df_unfccc.iloc[row, 0])
        collected_years.add(year)
        
        raw_val = float(df_unfccc.iloc[row, 7])
        perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_ol_N2O_emissions_mc)
        
        value = perturbed_raw * N2O_to_N
        if value < 0: value = 0.0
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_ol_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.OL-AT.AT-Emissions-N2'
    collected_years = set()
    data_sources = 'UNFCCC CRT + Butterbach-Bahl et al. (2013)'
    dataset_key = 'UNFCCC_emissions'

    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    if df_unfccc is None:
        raise ValueError(f"[KRITISK] Data 'fs_unfccc_emissions_raw' mangler i preloaded_data for {flow_code}!")

    ratio = float(current_params.get("forest_N2_to_N2O_ratio"))
    N2O_to_N = float(current_params.get("N2O_to_N_factor"))

    for row in range(5, 38):
        year = int(df_unfccc.iloc[row, 0])
        collected_years.add(year)
        
        raw_val = float(df_unfccc.iloc[row, 7])
        perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_ol_N2_emissions_mc)
        
        value = perturbed_raw * N2O_to_N * ratio
        if value < 0: value = 0.0
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)

    
def _add_ol_leaching_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.OL-HY.SW-Leaching-Nmix'
    collected_years = set()
    data_sources = 'TEOTIL'
    dataset_key = 'TEOTIL'
    
    df_kyst = preloaded_data.get('hy_kyst_tilforsel')
    df_teotil3 = preloaded_data.get('hy_teotil3_by_source')
    if df_kyst is None or df_teotil3 is None: 
        raise ValueError(f"[KRITISK] Koblingsdata mangler i preloaded_data for {flow_code}!")

    frac = float(current_params.get("OL_leaching_bg_fraction"))
    
    kyst_dict = {}
    for _, row in df_kyst.iterrows():
        if str(row['Unnamed: 0']).strip().lower() in ['year', 'år', 'årstall']:
            continue
        try:
            year_val = int(row['Unnamed: 0'])
            kyst_dict[year_val] = float(row['Bakgrunn'])
        except (ValueError, TypeError):
            continue

    teotil_dict = {}
    for idx, row in df_teotil3.iterrows():
        val_at_col0 = str(row.iloc[0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        try:
            year_val = int(float(val_at_col0))
            teotil_dict[year_val] = float(row.iloc[10])
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"[KRITISK DATAFEIL] Kunne ikke konvertere verdi til tall i df_teotil3 på rad {idx}.\n"
                f"Verdi i kolonne 0 (år): '{row.iloc[0]}' | Verdi i kolonne 10: '{row.iloc[10]}'\n"
                f"Original feil: {e}"
            )
            
    for year in EXPECTED_YEARS:
        value = None
        
        if year in teotil_dict:
            raw_val = teotil_dict[year] / 1000
            perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_ol_leaching_mc)
            value = perturbed_raw
            
        elif year in kyst_dict:
            raw_val = kyst_dict[year] / 1000
            perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_ol_leaching_mc)
            value = perturbed_raw * frac

        else:
            # Året finnes ikke i filene. Vi hopper over, slik at report_missing_years fanger det opp.
            continue

        if value < 0: 
            value = 0.0

        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value, 
            'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
        })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_ol_grazing_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.OL-AG.MM-Grazing-Nmix'
    collected_years = set()
    data_sources = 'NIBIO'
    dataset_key = 'beitestatistikk'
    
    Jones = float(current_params.get("Jones_factor"))
    
    fu_sheep_1996 = float(current_params.get("fu_sheep_1996")) * 1e6
    fu_cattle_1996 = float(current_params.get("fu_cattle_1996")) * 1e6
    fu_goat_1996 = float(current_params.get("fu_goat_1996")) * 1e6   

    protein_cont = float(current_params.get("protein_cont_grazing")) * 1e-9

    sau, lam, storfe, geit = {}, {}, {}, {}

    def extract_sau_lam(df, cols, row_idx):
        for col in cols:
            year = int(df.iloc[0, col])
            r_sau = float(df.iloc[row_idx, col-3])
            r_lam = float(df.iloc[row_idx, col-2])
            
            sau[year] = _apply_dataset_noise(r_sau, dataset_key, dataset_noise, _add_ol_grazing_mc)
            lam[year] = _apply_dataset_noise(r_lam, dataset_key, dataset_noise, _add_ol_grazing_mc)

    # Krasj hvis beite-datasett mangler i RAM
    required_sau_keys = ['obb_Sau1990-99_raw', 'obb_Sau2000-09_raw', 'obb_Sau2010-19_raw', 'obb_Sau2020-29_raw']
    for k in required_sau_keys:
        if k not in preloaded_data:
            raise ValueError(f"[KRITISK] Mangler fil-nøkkel '{k}' i preloaded_data for saueberegning!")
            
    extract_sau_lam(preloaded_data['obb_Sau1990-99_raw'], range(6, 100, 10), 21)
    extract_sau_lam(preloaded_data['obb_Sau2000-09_raw'], range(6, 100, 10), 22)
    extract_sau_lam(preloaded_data['obb_Sau2010-19_raw'], range(6, 100, 10), 22)
    extract_sau_lam(preloaded_data['obb_Sau2020-29_raw'], range(6, 60, 10), 13)

    df_sg_old = preloaded_data.get('obb_Storfe og geit1993-2019_raw')
    if df_sg_old is None:
        raise ValueError(f"[KRITISK] Mangler 'obb_Storfe og geit1993-2019_raw' for beiteberegning!")
        
    for col in range(4, 59, 6):
        year = int(df_sg_old.iloc[0, col])
        r_st = float(df_sg_old.iloc[23, col-2])
        r_gt = float(df_sg_old.iloc[23, col-1])
        storfe[year] = _apply_dataset_noise(r_st, dataset_key, dataset_noise, _add_ol_grazing_mc)
        geit[year] = _apply_dataset_noise(r_gt, dataset_key, dataset_noise, _add_ol_grazing_mc)
        
    for col in range(66, 200, 8):
        year = int(df_sg_old.iloc[0, col])
        r_st = float(df_sg_old.iloc[23, col-2])
        r_gt = float(df_sg_old.iloc[23, col-1])
        storfe[year] = _apply_dataset_noise(r_st, dataset_key, dataset_noise, _add_ol_grazing_mc)
        geit[year] = _apply_dataset_noise(r_gt, dataset_key, dataset_noise, _add_ol_grazing_mc)

    df_sg_new = preloaded_data.get('obb_Storfe og geit2020-29_raw')
    if df_sg_new is None:
        raise ValueError(f"[KRITISK] Mangler 'obb_Storfe og geit2020-29_raw' for beiteberegning!")
        
    for col in range(6, 49, 8):
        year = int(df_sg_new.iloc[0, col])
        r_st = float(df_sg_new.iloc[13, col-2])
        r_gt = float(df_sg_new.iloc[13, col-1])
        storfe[year] = _apply_dataset_noise(r_st, dataset_key, dataset_noise, _add_ol_grazing_mc)
        geit[year] = _apply_dataset_noise(r_gt, dataset_key, dataset_noise, _add_ol_grazing_mc)

    # Lineær ekstrapolering bakover for de manglende årene (1990-1992)
    for animal_dict in [storfe, geit]:
        years = np.array(list(animal_dict.keys()), dtype=float)
        y = np.array(list(animal_dict.values()), dtype=float)    
        a, b = np.polyfit(years, y, 1)    
        for y_back in [1990, 1991, 1992]:
            animal_dict[y_back] = a * y_back + b

    # Hvis referanseår 1996 ikke finnes, kastes det en feil
    if not (1996 in sau and 1996 in lam and 1996 in storfe and 1996 in geit):
        raise KeyError("[KRITISK FEIL] Referanseåret 1996 mangler i et eller flere beitedatasett. Kan ikke kalkulere fu_animal!")

    fu_sheep = fu_sheep_1996 / sau[1996]
    fu_lamb = fu_sheep_1996 / lam[1996]
    fu_cattle = fu_cattle_1996 / storfe[1996]
    fu_goat = fu_goat_1996 / geit[1996]

    for year in range(1990, 2026):
        if not (year in sau and year in lam and year in storfe and year in geit):
            raise KeyError(f"[KRITISK FEIL] Mangler komplette dyretall for årstallet {year}!")
            
        collected_years.add(year)
        value = (sau[year]*fu_sheep + lam[year]*fu_lamb + storfe[year]*fu_cattle + geit[year]*fu_goat) * protein_cont / Jones
        if value < 0: value = 0.0
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value, 
            'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)