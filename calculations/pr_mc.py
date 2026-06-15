#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:50:01 2026

@author: anja
"""

import pandas as pd  # Ensure you have pandas installed
import openpyxl
from calculations.n_params import NParameters
from calculations.shared_flow_calculations import (
    get_waste_frac,
    find_export_for_recycling,
    find_export_for_reuse,
    find_household_waste,
    find_landfill_emissions_to_water,
    find_other_industry_waste,
    find_recycling,
    find_sewage_sludge_biogas,
    find_solid_waste_export)
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    combine_uncertainties_percent,
    get_uncertainty,
    read_trade_data,
    # find_trade_data
)

def execute_calculations_pr(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    Hovedfunksjon for RW-poolen. Kjører alle underberegninger.
    Alle distribusjoner trekkes sentralt før denne kjøres.
    """
    results = []

    _add_waste_to_energy_mc(results, preloaded_data, current_params, dataset_noise)
    _add_recycling_mc(results, preloaded_data, current_params, dataset_noise, current_trade_factors)
    _add_ag_biologically_treated_organic_waste_mc(results, preloaded_data, current_params, dataset_noise)
    _add_wastewater_from_landfills_mc(results, preloaded_data, current_params, dataset_noise)
    _add_hs_biologically_treated_organic_waste_mc(results, preloaded_data, current_params, dataset_noise)
    _add_biofuels_production_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    
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


def _calculate_scaled_waste_timeseries(tonnes_modern_dict, tonnes_10513_dict, target_year_modern, target_year_10513, noise_modern, noise_10513, noise_hist):
    """
    Universell skaleringsmotor for avfallsstrømmer i MC-loopen.
    Tar inn råmengder (tonn) og spytter ut en ferdig harmonisert tidsserie fra 1984 til 2025.
    """
    final_series = {}

    # 1. Moderne data (f.eks. 12818-perioden) med sin støy
    for year, val in tonnes_modern_dict.items():
        final_series[year] = val * noise_modern

    # Hent ut de uforstyrrede basisverdiene for å unngå tolkningsstøy i overgangene
    value_modern_basis = tonnes_modern_dict.get(target_year_modern, 0.0)
    tonnes_basis_10513 = tonnes_10513_dict.get(target_year_10513, 0.0)

    if tonnes_basis_10513 == 0:
        raise ZeroDivisionError(f"[KRITISK] Mengdebasis i tabell 10513 for år {target_year_10513} er 0 eller mangler!")

    # 2. Skaler 2012-2017 bakover basert på forholdet mellom tabellene
    for year in range(2012, 2018):
        if year not in tonnes_10513_dict:
            raise KeyError(f"[KRITISK] År {year} mangler i de innsamlede 10513-dataene.")
        
        tonnes_year = tonnes_10513_dict[year]
        # Formel: Moderne_Basis * (Mengde_År / Mengde_Basis_10513)
        val_scaled = value_modern_basis * (tonnes_year / tonnes_basis_10513)
        final_series[year] = val_scaled * noise_10513

    # 3. Ekstrapoler 2012-verdien bakover til 1984
    value_2012_clean = value_modern_basis * (tonnes_10513_dict.get(2012, 0.0) / tonnes_basis_10513)
    
    for year in range(1984, 2012):
        final_series[year] = value_2012_clean * noise_hist

    return final_series

def _add_waste_to_energy_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-EF.EC-Waste to energy-Nmix'
    collected_years = set()
    data_sources = 'SSB'
    
    # Hent N-fraksjoner via current_params - krasjer om nøkkel mangler
    paper_N   = float(current_params.waste_N_frac('paper'))
    plastic_N = float(current_params.waste_N_frac('plastic'))
    wood_N    = float(current_params.waste_N_frac('wood'))
    textile_N = float(current_params.waste_N_frac('textiles'))
    wet_N     = float(current_params.waste_N_frac('wet_organic'))
    sludge_N  = float(current_params.waste_N_frac('sludge'))
    other_N   = float(current_params.waste_N_frac('other_materials'))
    haz_N     = float(current_params.waste_N_frac('hazardous'))
    contam_N  = float(current_params.waste_N_frac('contaminated_masses'))
    mixed_N   = float(current_params.waste_N_frac('mixed_waste'))
    rubber_N  = float(current_params.waste_N_frac('rubber'))
    park_N    = float(current_params.waste_N_frac('park_garden'))

    # =========================================================================
    # 1. PERIODE 1995-2011: SSB Tabell 05281 (Nøkkel: ssb_waste_05281)
    # =========================================================================
    dataset_key_05281 = '05281'
    df_05281 = preloaded_data.get('ssb_waste_05281')
    if df_05281 is None:
        raise ValueError(f"[KRITISK] Data 'ssb_waste_05281' mangler i preloaded_data for {flow_code}!")

    for col in range(3, 20):  
        # Ingen try/except eller strip-fallbacks her; feiler om dataen er korrupt eller tom
        year = int(float(df_05281.iloc[2, col]))
        collected_years.add(year)
        
        raw_tonnage = 0.0
        raw_tonnage += float(df_05281.iloc[60, col]) * paper_N    
        raw_tonnage += float(df_05281.iloc[88, col]) * paper_N    
        raw_tonnage += float(df_05281.iloc[62, col]) * plastic_N  
        raw_tonnage += float(df_05281.iloc[90, col]) * plastic_N  
        raw_tonnage += float(df_05281.iloc[65, col]) * wood_N     
        raw_tonnage += float(df_05281.iloc[93, col]) * wood_N     
        raw_tonnage += float(df_05281.iloc[66, col]) * textile_N  
        raw_tonnage += float(df_05281.iloc[94, col]) * textile_N  
        raw_tonnage += float(df_05281.iloc[67, col]) * wet_N      
        raw_tonnage += float(df_05281.iloc[95, col]) * wet_N      
        raw_tonnage += float(df_05281.iloc[69, col]) * sludge_N   
        raw_tonnage += float(df_05281.iloc[97, col]) * sludge_N   
        raw_tonnage += float(df_05281.iloc[70, col]) * other_N    
        raw_tonnage += float(df_05281.iloc[98, col]) * other_N    
        raw_tonnage += float(df_05281.iloc[71, col]) * haz_N      
        raw_tonnage += float(df_05281.iloc[99, col]) * haz_N      
        raw_tonnage += float(df_05281.iloc[72, col]) * contam_N   
        raw_tonnage += float(df_05281.iloc[100, col]) * contam_N  

        value = _apply_dataset_noise(raw_tonnage, dataset_key_05281, dataset_noise, _add_waste_to_energy_mc)
        if value < 0: value = 0.0

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på 05281)', 'data_sources': data_sources
        })

    # =========================================================================
    # 2. PERIODE 2012-2023: SSB Tabell 10513 (Nøkkel: ssb_waste_10513)
    # =========================================================================
    dataset_key_10513 = '10513'
    df_10513 = preloaded_data.get('ssb_waste_10513')
    if df_10513 is None:
        raise ValueError(f"[KRITISK] Data 'ssb_waste_10513' mangler i preloaded_data for {flow_code}!")

    # Endret fra 110 til 101 for å hindre at .iloc går out-of-bounds på siste steget (som skal være 100)
    for col in range(1, 101, 9):  
        year = int(float(df_10513.iloc[3, col]))
        collected_years.add(year)
        
        raw_tonnage = 0.0
        raw_tonnage += float(df_10513.iloc[6, col+5]) * wet_N       
        raw_tonnage += float(df_10513.iloc[7, col+5]) * park_N      
        raw_tonnage += float(df_10513.iloc[8, col+5]) * wood_N       
        raw_tonnage += float(df_10513.iloc[9, col+5]) * sludge_N     
        raw_tonnage += float(df_10513.iloc[10, col+5]) * paper_N     
        raw_tonnage += float(df_10513.iloc[16, col+5]) * plastic_N   
        raw_tonnage += float(df_10513.iloc[17, col+5]) * rubber_N    
        raw_tonnage += float(df_10513.iloc[18, col+5]) * textile_N   
        raw_tonnage += float(df_10513.iloc[21, col+5]) * haz_N       
        raw_tonnage += float(df_10513.iloc[22, col+5]) * mixed_N     
        raw_tonnage += float(df_10513.iloc[23, col+5]) * other_N     
        raw_tonnage += float(df_10513.iloc[24, col+5]) * contam_N    

        value = _apply_dataset_noise(raw_tonnage, dataset_key_10513, dataset_noise, _add_waste_to_energy_mc)
        if value < 0: value = 0.0

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på 10513)', 'data_sources': data_sources
        })
        
    # =========================================================================
    # 3. PERIODE 1990-1994: Historisk ekstrapolering (Nøkkel: waste_historical_fractions)
    # =========================================================================
    dataset_key_hist = 'historical_waste'
    df_hist = preloaded_data.get('waste_historical_fractions')
    if df_hist is None:
        raise ValueError(f"[KRITISK] Data 'waste_historical_fractions' mangler i preloaded_data for {flow_code}!")

    # Henter dataene direkte slik funksjonene leverer dem i MC-miljøet
    household_waste = find_household_waste(preloaded_data, current_params, dataset_noise)
    industry_waste, _ = find_other_industry_waste(
        preloaded_data['ssb_05282'], 
        preloaded_data['ssb_10514'], 
        preloaded_data['ssb_hist_industry_waste'], 
        current_params, 
        dataset_noise
    )

    inc_frac_1985 = float(df_hist.iloc[1, 1]) / 100  
    inc_frac_1992 = float(df_hist.iloc[2, 1]) / 100  
    change_per_year = (inc_frac_1992 - inc_frac_1985) / 7
    
    r_iloc = 2  
    for year in range(1990, 1995):
        collected_years.add(year)
        
        # Hent basis-nitrogenverdiene
        waste = household_waste[year] + industry_waste[year]
        
        if year < 1992:
            inc_frac = inc_frac_1985 + change_per_year * (year - 1985)
            comment_str = 'extrapolated (MC-støy lagt på basisdata)'
        else:
            inc_frac = float(df_hist.iloc[r_iloc, 1]) / 100
            comment_str = 'ok (MC-støy lagt på basisdata)'
            r_iloc += 1
            
        # Nøyaktig opprinnelig formel
        raw_val = waste * inc_frac
        
        value = _apply_dataset_noise(raw_val, dataset_key_hist, dataset_noise, _add_waste_to_energy_mc)

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': comment_str, 'data_sources': data_sources
        })
        
    # Sjekk om tidsserien har hull eller mangler år. Krasj hvis den ikke er komplett.
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_recycling_mc(results, preloaded_data, current_params, dataset_noise, current_trade_factors):
    flow_code = 'PR.SO-MP.OP-Recycling-Nmix'
    collected_years = set()
    data_sources = 'SSB'

    year_values = find_recycling(
        preloaded_data=preloaded_data,
        current_params=current_params,
        dataset_noise=dataset_noise,
        prepared_trade_recycling=preloaded_data.get('trade_recycling'),
        prepared_trade_reuse=preloaded_data.get('trade_reuse'),
        trade_params=current_trade_factors
    )

    for year, value in year_values.items():
        collected_years.add(year)
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': 'ok (MC-støy integrert i datagrunnlag)',
            'data_sources': data_sources
        })

    # Beholder rapporteringen av manglende år her også
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
def _add_ag_biologically_treated_organic_waste_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-AG.SM-Biologically treated organic waste-Nmix'
    collected_years = set()
    
    # =========================================================================
    # STRIKT STØYHENTING (Ingen fallbacks)
    # =========================================================================
    try:
        noise_biogass = float(dataset_noise['Biogass_Norge']['value'])
        noise_12818   = float(dataset_noise['12818']['value'])
        noise_10513   = float(dataset_noise['10513']['value'])
        noise_hist    = float(dataset_noise['historical_waste']['value'])
    except KeyError as e:
        raise KeyError(f"[KRITISK STOPP] Støy-ordboken mangler nødvendig MC-nøkkel for AG: {e}")

    # =========================================================================
    # DEL 1: 2021-2023 - DATA FRA BIOGASS NORGE (Danner basis for modern_dict)
    # =========================================================================
    df_biogass = preloaded_data.get('biogass_tall')
    if df_biogass is None:
        raise ValueError("[KRITISK] Data 'biogass_tall' mangler i preloaded_data!")
        
    value_2021 = 0.0
    tonnes_modern_dict = {}
    
    for col_idx in range(2, 6):
        try:
            year = int(float(str(df_biogass.iloc[6, col_idx]).strip()))
            val_ktN = float(df_biogass.iloc[31, col_idx]) / 1000.0
            
            if year == 2021:
                value_2021 = val_ktN
                
            # For 2021-2023 bruker vi Biogass Norge-data direkte som "modern" input
            if 2021 <= year <= 2023:
                tonnes_modern_dict[year] = val_ktN
        except (ValueError, TypeError, IndexError):
            continue

    # =========================================================================
    # DEL 2: 2018-2020 - SKALERING MED SSB TABELL 12818 Inn i modern_dict
    # =========================================================================
    df_12818 = preloaded_data.get('ssb_waste_12818')
    if df_12818 is None:
        raise ValueError("[KRITISK] Data 'ssb_waste_12818' mangler i preloaded_data!")

    tonnes_2021_basis = float(df_12818.iloc[5, 4])
    if tonnes_2021_basis == 0:
        raise ZeroDivisionError("[KRITISK] Skaleringsfaktor for 2021 i tabell 12818 er 0!")

    for col_idx in range(1, 4):
        try:
            year = int(float(str(df_12818.iloc[3, col_idx]).strip()))
            tonnes_year = float(df_12818.iloc[5, col_idx])
            
            # Beregn skalert verdi for 2018-2020 basert på 2021-forholdet
            val_scaled = tonnes_year * (value_2021 / tonnes_2021_basis)
            tonnes_modern_dict[year] = val_scaled
        except (ValueError, TypeError, IndexError):
            continue

    # =========================================================================
    # DEL 3: 2012-2017 - SAMLE RÅMENGDER FRA TABELL 10513
    # =========================================================================
    df_10513 = preloaded_data.get('ssb_waste_10513')
    if df_10513 is None:
        raise ValueError("[KRITISK] Data 'ssb_waste_10513' mangler i preloaded_data!")

    tonnes_10513_dict = {}
    
    for col in range(1, df_10513.shape[1], 9):
        cell_year = str(df_10513.iloc[3, col]).strip()
        if cell_year.replace('.0', '').isdigit():
            year = int(float(cell_year))
            
            try:
                # For AG.SM skalerer vi basert på den *totale råavfallsmengden* (tonn) i tabell 10513
                total_tonnes = (
                    float(df_10513.iloc[6, col + 2]) +  # Våtorganisk
                    float(df_10513.iloc[7, col + 2]) +  # Park- og hage
                    float(df_10513.iloc[8, col + 2]) +  # Treavfall
                    float(df_10513.iloc[9, col + 2])    # Slam
                )
                tonnes_10513_dict[year] = total_tonnes
            except (ValueError, TypeError, IndexError):
                continue

    # Strikt sjekk på at basisåret eksisterer i de innsamlede dataene
    if 2018 not in tonnes_10513_dict:
        raise KeyError("[KRITISK] Basisår 2018 mangler i tabell 10513-dataene for AG-skalering!")

    # =========================================================================
    # DEL 4: KJØR BEREGNING VIA DEN FELLES MOTOREN
    # =========================================================================
    # Merk at for AG sender vi inn 'noise_biogass' som modern støy siden 2021-2023-dataene styrer nivået
    final_values = _calculate_scaled_waste_timeseries(
        tonnes_modern_dict = tonnes_modern_dict,
        tonnes_10513_dict  = tonnes_10513_dict,
        target_year_modern = 2018,
        target_year_10513  = 2018,
        noise_modern       = noise_biogass, 
        noise_10513        = noise_10513,
        noise_hist         = noise_hist
    )

    # Overstyr årene 2018-2020 til å bruke sin spesifikke tabellstøy (noise_12818) i stedet for noise_biogass
    for year in range(2018, 2021):
        if year in tonnes_modern_dict:
            final_values[year] = tonnes_modern_dict[year] * noise_12818

    # Nullut år før 1990 slik notatene dine spesifiserte ("extrapolate back to 1990")
    for year in range(1984, 1990):
        final_values[year] = 0.0

    # =========================================================================
    # GENERER REKORDS TIL RESULTS
    # =========================================================================
    for year in sorted(final_values.keys()):
        collected_years.add(year)
        val = final_values[year]
        if val < 0: val = 0.0
        
        if year < 1990:
            comment_str = 'Ingen aktivitet før 1990'
            source_str  = 'Ingen data'
        elif year < 2012:
            comment_str = 'Ekstrapolert trend fra 2012'
            source_str  = 'extrapolated'
        else:
            comment_str = 'ok (Felles skaleringsmotor)'
            source_str  = 'Biogass Norge / SSB (Tabell 12818 / 10513)'

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': comment_str,
            'data_sources': source_str
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_wastewater_from_landfills_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-PR.WW-Wastewater from landfills-Nmix'
    collected_years = set()
    
    # =========================================================================
    # STRIKT STØYHENTING
    # =========================================================================
    try:
        noise_mildir = float(dataset_noise['norskeutslipp']['value'])
    except KeyError as e:
        raise KeyError(f"[KRITISK STOPP] Støy-ordboken mangler nødvendig MC-nøkkel: {e}")

    # Hent arkene fra preloaded_data
    uts_raw = preloaded_data.get('deponi_utslipp')
    tilk_raw = preloaded_data.get('deponi_tilkobling')
    
    if uts_raw is None or tilk_raw is None:
        raise ValueError("[KRITISK] Data for deponi_utslipp eller deponi_tilkobling mangler!")

    # 1. Bygg oppslags-sett for tilkoblingsstatus basert på posisjonsindeks (.iloc)
    tilk_ja = set()
    tilk_nei = set()
    
    for idx, row in tilk_raw.iterrows():
        # Hopp over header-raden hvis den dukker opp som første datalinje
        if idx == 0 and ("anlegg" in str(row.iloc[0]).lower() or "tilkoblet" in str(row.iloc[1]).lower()):
            continue
            
        name_clean = str(row.iloc[0]).strip().lower() # Kolonne 0: anleggsnavn
        status = str(row.iloc[1]).strip().lower()    # Kolonne 1: status
        
        if 'ja' in status:
            tilk_ja.add(name_clean)
        elif 'nei' in status:
            tilk_nei.add(name_clean)

    # 2. Loop over utslipp ved hjelp av .iloc posisjoner
    real_years_data = {}
    
    for idx, row in uts_raw.iterrows():
        # Hopp over header-raden hvis den dukker opp som første datalinje
        if idx == 0 and "anlegg" in str(row.iloc[0]).lower():
            continue
            
        try:
            # Hent verdier basert på kolonneposisjon fra bildet ditt
            year_val = str(row.iloc[3]).strip() # Kolonne 3: År
            if not year_val.replace('.0', '').isdigit():
                continue
                
            year = int(float(year_val))
            
            if 2011 <= year <= 2025:
                anlegg_name = str(row.iloc[0]).strip().lower() # Kolonne 0: Anleggsnavn
                raw_value = float(row.iloc[4])                 # Kolonne 4: Årlig utslipp til vann
                
                # Definer vekt basert på om navnet finnes i ja/nei listene
                weight = 0.5 # Default ukjent
                
                # Sjekk om navnet matcher helt eller delvis
                if any(ja_name in anlegg_name or anlegg_name in ja_name for ja_name in tilk_ja):
                    weight = 1.0
                elif any(nei_name in anlegg_name or anlegg_name in nei_name for nei_name in tilk_nei):
                    weight = 0.0
                
                # Beregn N-mengde koblet til avløp
                n_leachate_tN = raw_value * weight
                
                if year not in real_years_data:
                    real_years_data[year] = 0.0
                    
                # Akkumuler i ktN (tN / 1000.0) og legg på rundens MC-støy
                real_years_data[year] += (n_leachate_tN / 1000.0) * noise_mildir
                
        except (ValueError, TypeError, IndexError):
            continue

    # =========================================================================
    # DEL 3: BEREGN HISTORISK TREND (1990-2010)
    # =========================================================================
    valid_years = [y for y in real_years_data.keys() if 2011 <= y <= 2025]
    
    if valid_years:
        mean_connected_kt = sum(real_years_data[y] for y in valid_years) / len(valid_years)
    else:
        raise ValueError("[KRITISK] Ingen gyldige utslippsdata for deponier i perioden 2011-2025!")

    # Bygg endelig tidsrekke-ordbok
    final_values = {}
    
    for year in range(1990, 2011):
        final_values[year] = mean_connected_kt

    for year in range(2011, 2026):
        final_values[year] = real_years_data.get(year, 0.0)

    for year in range(1984, 1990):
        final_values[year] = 0.0

    # =========================================================================
    # GENERER REKORDS TIL RESULTS
    # =========================================================================
    for year in sorted(final_values.keys()):
        collected_years.add(year)
        val = final_values[year]
        if val < 0: val = 0.0
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': 'ok (Robust posisjonsindeksert mapping og MC-støy)',
            'data_sources': 'Utslipp_deponi.xlsx (Mildir)' if year >= 2011 else 'extrapolated'
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_hs_biologically_treated_organic_waste_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-HS.HS-Biologically treated organic waste-Nmix'
    collected_years = set()
    
    # =========================================================================
    # STRIKT STØYHENTING (Ingen fallbacks)
    # =========================================================================
    try:
        noise_12818 = float(dataset_noise['12818']['value'])
        noise_10513 = float(dataset_noise['10513']['value'])
        noise_hist  = float(dataset_noise['historical_waste']['value'])
    except KeyError as e:
        raise KeyError(f"[KRISK STOPP] Støy-ordboken mangler nødvendig MC-nøkkel for HS: {e}")

    # N-fraksjoner og tapsfaktorer via parametersystemet
    compost_old_N = float(current_params.waste_N_frac('compost_old'))
    wet_N         = float(current_params.waste_N_frac('wet_organic'))
    park_N        = float(current_params.waste_N_frac('park_garden'))
    sludge_N      = float(current_params.waste_N_frac('sludge'))
    
    # Henter prosentsats for N-tap (f.eks. 0.25)
    compost_N_loss = float(current_params.waste_N_frac('compost_N_loss'))

    # =========================================================================
    # DEL 1: LES NYERE DATA FRA TABELL 12818
    # =========================================================================
    df_12818 = preloaded_data.get('ssb_waste_12818')
    if df_12818 is None:
        raise ValueError("[KRITISK] Data 'ssb_waste_12818' mangler i preloaded_data!")

    tonnes_modern_dict = {}
    # Kolonner 1 til 7 tilsvarer årene i tabellen (juster range om nødvendig basert på filendringer)
    for col_idx in range(1, 8):
        try:
            year = int(float(str(df_12818.iloc[3, col_idx]).strip())) # Rad 4 i excel
            
            # Hent ut verdiene fra rad 7 og rad 8 i Excel (indeks 6 og 7 i Python)
            val_row7 = float(df_12818.iloc[5, col_idx])
            val_row8 = float(df_12818.iloc[6, col_idx])
            
            # Multipliser tonn med Nitrogeninnhold for kompost med en gang
            tonnes_modern_dict[year] = (val_row7 + val_row8) * compost_old_N
        except (ValueError, TypeError, IndexError):
            continue

    # =========================================================================
    # DEL 2: LES HISTORISKE DATA FRA TABELL 10513
    # =========================================================================
    df_10513 = preloaded_data.get('ssb_waste_10513')
    if df_10513 is None:
        raise ValueError("[KRITISK] Data 'ssb_waste_10513' mangler i preloaded_data!")

    tonnes_10513_dict = {}
    
    # Gå gjennom kolonnene i tabell 10513 (steg på 9 slik som før)
    for col in range(1, df_10513.shape[1], 9):
        cell_year = str(df_10513.iloc[3, col]).strip()
        if cell_year.replace('.0', '').isdigit():
            year = int(float(cell_year))
            
            try:
                # Beregn Nitrogenverdi ut ifra fraksjonene for våt, park og slam
                # Rad 7, 8 og 10 i Excel blir indeks 6, 7 og 9 i Python
                n_val = (
                    float(df_10513.iloc[6, col + 2]) * wet_N +
                    float(df_10513.iloc[7, col + 2]) * park_N +
                    float(df_10513.iloc[9, col + 2]) * sludge_N
                )
                
                # Inkluder prosesstapet (1 - N_loss) direkte på verdiene i denne tabellen
                tonnes_10513_dict[year] = n_val * (1.0 - compost_N_loss)
            except (ValueError, TypeError, IndexError):
                continue

    # =========================================================================
    # DEL 3: UTKØR BEREGNING VIA DEN FELLES MOTOREN
    # =========================================================================
    # Skaleringsmotoren tar basis i år 2018 for begge tabeller
    final_values = _calculate_scaled_waste_timeseries(
        tonnes_modern_dict = tonnes_modern_dict,
        tonnes_10513_dict  = tonnes_10513_dict,
        target_year_modern = 2018,
        target_year_10513  = 2018,
        noise_modern       = noise_12818,
        noise_10513        = noise_10513,
        noise_hist         = noise_hist
    )

    # =========================================================================
    # GENERER REKORDS TIL RESULTS
    # =========================================================================
    for year in sorted(final_values.keys()):
        collected_years.add(year)
        val = final_values[year]
        if val < 0: val = 0.0
        
        # Merk historiske rader før 1990 som 0 dersom prosjektrammen krever det, 
        # men koden din spesifiserte "extrapolate 2012 value back to 1984"
        if year < 1990:
            comment_str = 'Ekstrapolert trend før 1990'
            source_str  = 'extrapolated'
        elif year < 2012:
            comment_str = 'Ekstrapolert trend fra 2012'
            source_str  = 'extrapolated'
        else:
            comment_str = 'ok (Felles skaleringsmotor)'
            source_str  = 'SSB (Tabell 12818 / 10513)'

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': comment_str,
            'data_sources': source_str
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_biofuels_production_wastewater_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'PR.SO-PR.WW-Biofuels production wastewater-Nmix'
    collected_years = set()
    
    # =========================================================================
    # STRIKT STØYHENTING (Krasjer hvis nøkler mangler)
    # =========================================================================
    try:
        noise_biogass = float(dataset_noise['Biogass']['value'])
        noise_10513   = float(dataset_noise['10513']['value'])
        noise_12359   = float(dataset_noise['12359']['value'])
    except KeyError as e:
        raise KeyError(f"[KRITISK STOPP] Støy-ordboken mangler nødvendig MC-nøkkel for biofuels wastewater: {e}")

    # Hent fraksjoner dynamisk fra parameter-objektet via .waste_N_frac()
    paper_N    = float(current_params.waste_N_frac("paper"))
    plastic_N  = float(current_params.waste_N_frac("plastic"))
    wood_N     = float(current_params.waste_N_frac("wood"))
    textile_N  = float(current_params.waste_N_frac("textiles"))
    wet_N      = float(current_params.waste_N_frac("wet_organic"))
    sludge_N   = float(current_params.waste_N_frac("sludge"))
    other_N    = float(current_params.waste_N_frac("other_materials"))
    haz_N      = float(current_params.waste_N_frac("hazardous"))
    contam_N   = float(current_params.waste_N_frac("contaminated_masses"))
    mixed_N    = float(current_params.waste_N_frac("mixed_waste"))
    rubber_N   = float(current_params.waste_N_frac("rubber"))
    park_N     = float(current_params.waste_N_frac("park_garden"))
    
    # Globale parametere hentes med .get()
    manure_N    = float(current_params.get("manure_N_frac"))
    fish_N      = float(current_params.get("animal_waste_N_frac"))
    loss_factor = float(current_params.get("digestate_loss_fraction"))

    # =========================================================================
    # HENT OG BEHANDLE STRØM 1: HUSDYRGJØDSEL (Biogass.xlsx)
    # =========================================================================
    df_manure = preloaded_data.get('biogass_manure')
    if df_manure is None:
        raise ValueError("[KRITISK] Data 'biogass_manure' mangler i preloaded_data!")
        
    year_values_manure = {}
    for r in range(2, 14):
        try:
            year = int(float(str(df_manure.iloc[r, 3]).strip())) 
            val_raw = float(df_manure.iloc[r, 7])                
            year_values_manure[year] = (val_raw / 1000.0) * manure_N * noise_biogass
        except (ValueError, TypeError, IndexError):
            continue

    # =========================================================================
    # HENT OG BEHANDLE STRØM 2: FISKESLAM (Tabell 12359)
    # =========================================================================
    df_fish = preloaded_data.get('ssb_waste_12359')
    if df_fish is None:
        raise ValueError("[KRITISK] Data 'ssb_waste_12359' mangler i preloaded_data!")
        
    year_values_fish = {}
    for col in range(3, df_fish.shape[1]):
        try:
            year_val = str(df_fish.iloc[2, col]).strip() 
            if not year_val.replace('.0', '').isdigit():
                continue
            year = int(float(year_val))
            val_raw = float(df_fish.iloc[28, col])
            year_values_fish[year] = val_raw * fish_N * noise_12359
        except (ValueError, TypeError, IndexError):
            continue

    # =========================================================================
    # HENT OG BEHANDLE STRØM 3: AVFALLSREGNSKAP (Tabell 10513)
    # =========================================================================
    df_10513 = preloaded_data.get('ssb_waste_10513')
    if df_10513 is None:
        raise ValueError("[KRITISK] Data 'ssb_waste_10513' mangler i preloaded_data!")

    final_values = {}

    for col in range(1, 110, 9):
        if col >= df_10513.shape[1]:
            break
            
        cell_year = str(df_10513.iloc[3, col]).strip() 
        if cell_year.replace('.0', '').isdigit():
            year = int(float(cell_year))
            collected_years.add(year)
            
            try:
                v_10513 = 0.0
                v_10513 += float(df_10513.iloc[6, col + 2]) * wet_N       
                v_10513 += float(df_10513.iloc[7, col + 2]) * park_N      
                v_10513 += float(df_10513.iloc[8, col + 2]) * wood_N      
                v_10513 += float(df_10513.iloc[9, col + 2]) * sludge_N    
                v_10513 += float(df_10513.iloc[10, col + 2]) * paper_N    
                v_10513 += float(df_10513.iloc[16, col + 2]) * plastic_N  
                v_10513 += float(df_10513.iloc[17, col + 2]) * rubber_N   
                v_10513 += float(df_10513.iloc[18, col + 2]) * textile_N  
                v_10513 += float(df_10513.iloc[21, col + 2]) * haz_N      
                v_10513 += float(df_10513.iloc[22, col + 2]) * mixed_N    
                v_10513 += float(df_10513.iloc[23, col + 2]) * other_N    
                v_10513 += float(df_10513.iloc[24, col + 2]) * contam_N   
                
                value = v_10513 * noise_10513
                
                if year > 2012:
                    value += year_values_manure.get(year, 0.0)
                    
                if year > 2016:
                    value += year_values_fish.get(year, 0.0)
                
                final_values[year] = value * loss_factor
                
            except (ValueError, TypeError, IndexError):
                final_values[year] = 0.0

    # =========================================================================
    # DEL 4: HISTORISKE ÅR (1984-2011) - SETTES STRIKT TIL 0.0
    # =========================================================================
    for year in range(1984, 2012):
        collected_years.add(year)
        final_values[year] = 0.0

    # =========================================================================
    # GENERER REKORDS TIL RESULTS
    # =========================================================================
    for year in sorted(final_values.keys()):
        val = final_values[year]
        if val < 0: val = 0.0
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': 'ok (Sammensatt avfallsstrøm med MC-støy)' if year >= 2012 else 'Satt til 0 før 2012',
            'data_sources': 'SSB, Landbruksdirektoratet, Biogass Norge' if year >= 2012 else 'Ingen data før 2012'
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)