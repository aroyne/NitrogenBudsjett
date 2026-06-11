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
    Hjelpefunksjon for å legge støy på en avlest fil-verdi basert på dataset_noise-strukturen.
    Skiller strengt mellom prosentvis ('perc') og absoluttusikkerhet.
    """
    if not dataset_noise or dataset_key not in dataset_noise:
        if dataset_noise and not hasattr(caller_func, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            print(f"          Kjører deterministisk (støy = 0) for dette datasettet inntil Excel oppdateres.")
            setattr(caller_func, f"warned_{dataset_key}", True)
        return base_value

    noise_info = dataset_noise[dataset_key]
    noise_val = noise_info['value']
    
    if noise_info['type'] == 'perc':
        return base_value * noise_val
    else:
        if noise_val >= 0:
            return base_value + (noise_val * noise_info['upp_bound'])
        else:
            return base_value + (noise_val * noise_info['low_bound'])


def _add_fo_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-AT.AT-Emissions-N2O'
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    dataset_key = 'UNFCCC_emissions'
    
    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    if df_unfccc is None: return

    N2O_to_N = float(current_params.get("N2O_to_N_factor"))
    
    for row in range(5, 38):  
        try:
            year = int(df_unfccc.iloc[row, 0])
            collected_years.add(year)
            
            # 1. Hent råverdi og legg på datasett-støy
            raw_val = float(df_unfccc.iloc[row, 3])
            perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_fo_N2O_emissions_mc)
            
            # 2. Multipliser med parameteren til slutt
            value = perturbed_raw * N2O_to_N
            if value < 0: value = 0.0
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': value,
                'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
            })
        except (ValueError, TypeError, IndexError): continue
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_fo_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-AT.AT-Emissions-N2'
    collected_years = set()
    data_sources = 'UNFCCC CRT + Butterbach-Bahl et al. (2013)'
    dataset_key = 'UNFCCC_emissions'

    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    if df_unfccc is None: return

    N2O_to_N = float(current_params.get("N2O_to_N_factor"))
    ratio = float(current_params.get("forest_N2_to_N2O_ratio"))

    for row in range(5, 38):
        try:
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
        except (ValueError, TypeError, IndexError): continue

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
        
def _add_fo_leaching_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-HY.SW-Leaching-Nmix'
    collected_years = set()
    data_sources = 'TEOTIL'
    dataset_key = 'TEOTIL'
    
    df_kyst = preloaded_data.get('hy_kyst_tilforsel')
    df_teotil3 = preloaded_data.get('hy_teotil3_by_source')
    if df_kyst is None or df_teotil3 is None: return

    frac = float(current_params.get("FO_leaching_bg_fraction"))
    
    # Historiske år (Kysttilførsel)
    for r in range(1, 24):
        try:
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
        except (ValueError, TypeError, IndexError): continue
            
    # Nyere år (TEOTIL3)
    for r in range(1, 12):
        try:
            year = int(df_teotil3.iloc[r, 0]) 
            collected_years.add(year)
            
            raw_val = float(df_teotil3.iloc[r, 10]) / 1000 
            value = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_fo_leaching_mc)
            if value < 0: value = 0.0

            results.append({
                'flow_name': flow_code, 'year': year, 'value': value, 
                'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
            })
        except (ValueError, TypeError, IndexError): continue
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_industrial_round_wood_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.FO-MP.OP-Industrial round wood-Nmix'
    collected_years = set()   
    
    # Henter data fra delt MC-funksjon som baserer seg på allerede støysatte current_params
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
    if df_ved is None: return

    N_content = float(current_params.get("firewood_N_frac"))
    
    for r in range(3, 38):  
        try:
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
        except (ValueError, TypeError, IndexError): continue
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_ol_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.OL-AT.AT-Emissions-N2O'
    collected_years = set()
    data_sources = 'UNFCCC CRT'
    dataset_key = 'UNFCCC_emissions'

    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    if df_unfccc is None: return

    N2O_to_N = float(current_params.get("N2O_to_N_factor"))

    for row in range(5, 38):
        try:
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
        except (ValueError, TypeError, IndexError): continue

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_ol_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'FS.OL-AT.AT-Emissions-N2'
    collected_years = set()
    data_sources = 'UNFCCC CRT + Butterbach-Bahl et al. (2013)'
    dataset_key = 'UNFCCC_emissions'

    df_unfccc = preloaded_data.get('fs_unfccc_emissions_raw')
    if df_unfccc is None: return

    ratio = float(current_params.get("forest_N2_to_N2O_ratio"))
    N2O_to_N = float(current_params.get("N2O_to_N_factor"))

    for row in range(5, 38):
        try:
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
        except (ValueError, TypeError, IndexError): continue

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
        return

    frac = float(current_params.get("OL_leaching_bg_fraction"))
    
    # 1. Bygg en trygg ordbok fra df_kyst ved å bruke de faktiske kolonnenavnene
    # Kolonne 'Unnamed: 0' inneholder årstallet, og 'Bebygd' er kilden som skal brukes
    kyst_dict = {}
    for _, row in df_kyst.iterrows():
        try:
            year_val = int(row['Unnamed: 0'])
            # Henter 'Bebygd' (tilsvarer din gamle indeks 4)
            kyst_dict[year_val] = float(row['Bakgrunn'])
        except (ValueError, TypeError, KeyError):
            continue

    # 2. Bygg ordbok fra df_teotil3 (Antar kolonne 0 er år, og kolonne 10 er verdien)
    teotil_dict = {}
    for _, row in df_teotil3.iterrows():
        try:
            # Hvis df_teotil3 også har kolonnenavn, kan du bytte ut iloc her senere
            year_val = int(row.iloc[0])
            teotil_dict[year_val] = float(row.iloc[10])
        except (ValueError, TypeError, IndexError):
            continue
            
    # 3. Gå systematisk gjennom alle forventede år i modellen
    for year in EXPECTED_YEARS:
        value = 0.0
        
        # Prioriter TEOTIL3 hvis data finnes der (typisk nyere år)
        if year in teotil_dict:
            raw_val = teotil_dict[year] / 1000
            perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_ol_leaching_mc)
            value = perturbed_raw
            
        # Fallback til kyst-data for historiske år (typisk før 2012)
        elif year in kyst_dict:
            raw_val = kyst_dict[year] / 1000
            perturbed_raw = _apply_dataset_noise(raw_val, dataset_key, dataset_noise, _add_ol_leaching_mc)
            value = perturbed_raw * frac  # Bakgrunnsfraksjon legges på her

        else:
            # Året finnes ikke i noen av kildene, hopp over så report_missing fanger det opp
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
    
    fu_sheep_1996 = float(current_params.get("fu_sheep_1996"))*1e6 # mill FEm -> FEm
    fu_cattle_1996 = float(current_params.get("fu_cattle_1996"))*1e6 # mill FEm -> FEm
    fu_goat_1996 = float(current_params.get("fu_goat_1996")) *1e6 # mill FEm -> FEm   

    protein_cont = float(current_params.get("protein_cont_grazing"))*1e-9 # g/FEm -> kt/FEm

    sau, lam, storfe, geit = {}, {}, {}, {}

    def extract_sau_lam(df, cols, row_idx):
        for col in cols:
            try:
                year = int(df.iloc[0, col])
                # Legger datasett-støy direkte på dyretallene lest ut fra råfilene
                r_sau = float(df.iloc[row_idx, col-3])
                r_lam = float(df.iloc[row_idx, col-2])
                
                sau[year] = _apply_dataset_noise(r_sau, dataset_key, dataset_noise, _add_ol_grazing_mc)
                lam[year] = _apply_dataset_noise(r_lam, dataset_key, dataset_noise, _add_ol_grazing_mc)
            except (ValueError, TypeError, IndexError): continue

    if 'obb_Sau1990-99_raw' in preloaded_data:
        extract_sau_lam(preloaded_data['obb_Sau1990-99_raw'], range(6, 100, 10), 21)
    if 'obb_Sau2000-09_raw' in preloaded_data:
        extract_sau_lam(preloaded_data['obb_Sau2000-09_raw'], range(6, 100, 10), 22)
    if 'obb_Sau2010-19_raw' in preloaded_data:
        extract_sau_lam(preloaded_data['obb_Sau2010-19_raw'], range(6, 100, 10), 22)
    if 'obb_Sau2020-29_raw' in preloaded_data:
        extract_sau_lam(preloaded_data['obb_Sau2020-29_raw'], range(6, 60, 10), 13)

    df_sg_old = preloaded_data.get('obb_Storfe og geit1993-2019_raw')
    if df_sg_old is not None:
        for col in range(4, 59, 6):
            try:
                year = int(df_sg_old.iloc[0, col])
                r_st = float(df_sg_old.iloc[23, col-2])
                r_gt = float(df_sg_old.iloc[23, col-1])
                storfe[year] = _apply_dataset_noise(r_st, dataset_key, dataset_noise, _add_ol_grazing_mc)
                geit[year] = _apply_dataset_noise(r_gt, dataset_key, dataset_noise, _add_ol_grazing_mc)
            except (ValueError, TypeError, IndexError): continue
        for col in range(66, 200, 8):
            try:
                year = int(df_sg_old.iloc[0, col])
                r_st = float(df_sg_old.iloc[23, col-2])
                r_gt = float(df_sg_old.iloc[23, col-1])
                storfe[year] = _apply_dataset_noise(r_st, dataset_key, dataset_noise, _add_ol_grazing_mc)
                geit[year] = _apply_dataset_noise(r_gt, dataset_key, dataset_noise, _add_ol_grazing_mc)
            except (ValueError, TypeError, IndexError): continue

    df_sg_new = preloaded_data.get('obb_Storfe og geit2020-29_raw')
    if df_sg_new is not None:
        for col in range(6, 49, 8):
            try:
                year = int(df_sg_new.iloc[0, col])
                r_st = float(df_sg_new.iloc[13, col-2])
                r_gt = float(df_sg_new.iloc[13, col-1])
                storfe[year] = _apply_dataset_noise(r_st, dataset_key, dataset_noise, _add_ol_grazing_mc)
                geit[year] = _apply_dataset_noise(r_gt, dataset_key, dataset_noise, _add_ol_grazing_mc)
            except (ValueError, TypeError, IndexError): continue

    # Lineær ekstrapolering bakover for de manglende årene (1990-1992)
    for animal_dict in [storfe, geit]:
        if animal_dict:
            years = np.array(list(animal_dict.keys()), dtype=float)
            y = np.array(list(animal_dict.values()), dtype=float)    
            a, b = np.polyfit(years, y, 1)    
            for y_back in [1990, 1991, 1992]:
                animal_dict[y_back] = a * y_back + b

    if 1996 in sau and 1996 in lam and 1996 in storfe and 1996 in geit:
        fu_sheep = fu_sheep_1996 / sau[1996]
        fu_lamb = fu_sheep_1996 / lam[1996]
        fu_cattle = fu_cattle_1996 / storfe[1996]
        fu_goat = fu_goat_1996 / geit[1996]
    else:
        return

    for year in range(1990, 2026):
        if year in sau and year in lam and year in storfe and year in geit:
            collected_years.add(year)
            value = (sau[year]*fu_sheep + lam[year]*fu_lamb + storfe[year]*fu_cattle + geit[year]*fu_goat) * protein_cont / Jones
            if value < 0: value = 0.0
            
            results.append({
                'flow_name': flow_code, 'year': year, 'value': value, 
                'comment': 'ok (MC-støy lagt på)', 'data_sources': data_sources
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)