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
    find_export_for_recycling,
    find_export_for_reuse,
    find_household_waste,
    find_other_industry_waste,
    find_recycling)
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    load_crltap_emissions_to_N,
    process_generic_trade_flow,
)

PR_SO_CRLTAP_SECTORS = [
    '1A1a', '5A', '5B1', '5B2', '5C1a', '5C1bi', 
    '5C1bii', '5C1biii', '5C1biv', '5C1bv', '5C1bvi', '5E'
]
PR_WW_CRLTAP_SECTORS = ['5D1', '5D2', '5D3']

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
    _add_so_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_so_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_so_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_so_leaching_mc(results, preloaded_data, current_params, dataset_noise)
    _add_export_for_recycling_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_export_for_reuse_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_solid_waste_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_ag_sewage_sludge_fertilizer_mc(results, preloaded_data, current_params, dataset_noise)
    _add_hs_sewage_sludge_fertilizer_mc(results, preloaded_data, current_params, dataset_noise)
    _add_sewage_sludge_landfill_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ww_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ww_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_treated_ww_discharge_mc(results, preloaded_data, current_params, dataset_noise)
    
    
    return results


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
    noise_05281 = dataset_noise[dataset_key_05281]
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

        value = raw_tonnage*noise_05281
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
    noise_10513 = dataset_noise[dataset_key_10513]
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

        value = raw_tonnage*noise_10513
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
    noise_hist = dataset_noise[dataset_key_hist]
    noise_trend = dataset_noise['trend interpolation']
    if df_hist is None:
        raise ValueError(f"[KRITISK] Data 'waste_historical_fractions' mangler i preloaded_data for {flow_code}!")

    # Henter dataene direkte slik funksjonene leverer dem i MC-miljøet
    household_waste = find_household_waste(preloaded_data, current_params, dataset_noise)
    industry_waste = find_other_industry_waste(
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
        
        value = raw_val*noise_hist*noise_trend

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
        current_trade_factors=current_trade_factors,
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
        noise_biogass = float(dataset_noise['Biogass_Norge'])
        noise_12818   = float(dataset_noise['12818'])
        noise_10513   = float(dataset_noise['10513'])
        noise_hist    = float(dataset_noise['historical_waste'])
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
    noise_10513 = dataset_noise['10513']
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
            raw_val = tonnes_modern_dict[year]
            # Funksjonen håndterer nå automatisk om '12818' er oppgitt som 'perc' eller 'low_bound'/'upp_bound'
            final_values[year] = raw_val*noise_12818
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
        noise_mildir = float(dataset_noise['norskeutslipp'])
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
    noise_12818 = dataset_noise['12818']
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
    noise_10513 = dataset_noise['10513']
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
    # 1. Kjør motoren flatt uten støy (støyfaktorer settes til 1.0)
    clean_values = _calculate_scaled_waste_timeseries(
        tonnes_modern_dict = tonnes_modern_dict,
        tonnes_10513_dict  = tonnes_10513_dict,
        target_year_modern = 2018,
        target_year_10513  = 2018,
        noise_modern       = 1.0,
        noise_10513        = 1.0,
        noise_hist         = 1.0
    )
    
    noise_hist = dataset_noise['historical_waste']
    noise_trend = dataset_noise['trend interpolation']
    # 2. Påfør riktig type distribusjonsstøy basert på tidsperiode
    for year in sorted(clean_values.keys()):
        collected_years.add(year)
        raw_val = clean_values[year]
        
        # Bestem støy-nøkkel basert på årsepoken dataene opprinnelig kom fra
        if year >= 2012:
            if year >= 2018:
                val = raw_val*noise_12818
            else:
                val = raw_val*noise_10513
        else:
            val = raw_val * noise_hist
        
        # B) EKSTRA STØY FOR EKSTRAPOLERTE ÅR (Før 2012)
        # Siden de historiske dataene er basert på en fremskrevet trend, påfører vi 
        # 'trend interpolation'-støy på toppen av den vanlige basestøyen.
        if year < 2012:
            val *= noise_trend
        
        if val < 0: 
            val = 0.0
            
        # Bestem kommentar og kilde (likt som før)...
        if year < 2012:
            comment_str = 'Ekstrapolert trend fra 2012'
            source_str  = 'extrapolated'
        else:
            comment_str = 'ok (MC-støy påført sentralt)'
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
        noise_biogass = float(dataset_noise['Biogass'])
        noise_10513   = float(dataset_noise['10513'])
        noise_12359   = float(dataset_noise['12359'])
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
    
def _add_so_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: NOx-utslipp til atmosfære fra avfallsbehandling (PR.SO-AT.AT-Emissions-NOx).
    Gjenbruker load_crltap_emissions_to_N med spesifikke avfallssektorer (CRLTAP).
    """
    flow_code = 'PR.SO-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    # 1. Hent og valider global konverteringsfaktor (.get)
    conv = float(current_params.get("NOx_to_N_factor"))
    
    # 2. Hent rådata fra RAM – krasj hardt hvis de mangler
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    if raw_lines is None:
        raise ValueError(f"[KRITISK] 'ag_crltap_raw_lines' mangler i preloaded_data for {flow_code}!")

    # 3. Kall felles hjelpefunksjon med avfallssektorene
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=PR_SO_CRLTAP_SECTORS,
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
        
        # Vask eventuelle negative verdier til 0.0, og håndter NaN
        val_clean = float(value)
        if val_clean < 0 or pd.isna(val_clean): 
            val_clean = 0.0
            
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': val_clean,
            'comment': comment, 
            'data_sources': data_sources
        })

    # 5. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_so_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: NH3-utslipp til atmosfære fra avfallsbehandling (PR.SO-AT.AT-Emissions-NH3).
    Gjenbruker load_crltap_emissions_to_N med spesifikke avfallssektorer (CRLTAP).
    """
    flow_code = 'PR.SO-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    # 1. Hent og valider global konverteringsfaktor (.get)
    conv = float(current_params.get("NH3_to_N_factor"))
    
    # 2. Hent rådata fra RAM
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    if raw_lines is None:
        raise ValueError(f"[KRITISK] 'ag_crltap_raw_lines' mangler i preloaded_data for {flow_code}!")

    # 3. Kall felles hjelpefunksjon med avfallssektorene
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=PR_SO_CRLTAP_SECTORS,
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
        
        # Vask eventuelle negative verdier til 0.0, og håndter NaN
        val_clean = float(value)
        if val_clean < 0 or pd.isna(val_clean): 
            val_clean = 0.0
            
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': val_clean,
            'comment': comment, 
            'data_sources': data_sources
        })

    # 5. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_so_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: N2O-utslipp til atmosfære fra avfallsbehandling (PR.SO-AT.AT-Emissions-N2O).
    Henter ferdiginnlastet CSV-data (N2O_SO.csv) fra RAM og påfører sentralt trukket datasettstøy.
    """
    flow_code = 'PR.SO-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'UNFCCC CRT'

    # 1. Hent og valider globale parametere
    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    
    # 2. Slå opp ferdig generert støy – krasj hvis nøkkelen mangler
    key_n2o = 'UNFCCC_emissions'
    if not dataset_noise or key_n2o not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_n2o}' mangler i dataset_noise for {flow_code}!")
    
    noise_val = dataset_noise[key_n2o]

    # 3. Hent ferdiglastet DataFrame fra RAM
    df_so_emissions = preloaded_data.get('n2o_so_raw')
    if df_so_emissions is None:
        raise ValueError(f"[KRITISK] 'n2o_so_raw' mangler i preloaded_data for {flow_code}!")

    # 4. Gå gjennom radene i den ferdiginnlastede CSV-filen
    for index, row in df_so_emissions.iterrows():
        try:
            year_val = row['year']
            n2o_val = row['value']  # Kolonnenavnet i csv er 'value'
            
            if pd.isna(year_val) or pd.isna(n2o_val):
                continue
                
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
                
            collected_years.add(year)
            
            # Basisverdi konvertert til reell N-vekt
            base_value = float(n2o_val) * conv_N2O

            # Påfør støyen matematisk korrekt basert på støytype
            value = base_value * noise_val

            # Sikre at fysiske utslipp aldri blir negative
            if value < 0: 
                value = 0.0

            results.append({
                'flow_name': flow_code, 
                'year': year, 
                'value': float(value),
                'comment': comment, 
                'data_sources': data_sources
            })
            
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Kunne ikke prosessere rad {index} i n2o_so_raw for {flow_code}: {e}")

    # 5. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_so_leaching_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Sigevann (leaching) fra deponi til overflatevann (PR.SO-HY.SW-Leaching-Nmix).
    Beregner deponiutslipp som IKKE er tilkoblet kommunalt avløp (invertert vekt).
    Ekstrapolerer historisk snitt for årene 1990-2010 basert på posisjonsindeksert mapping fra RAM.
    """
    flow_code = 'PR.SO-HY.SW-Leaching-Nmix'
    collected_years = set()
    comment = 'ok (Robust posisjonsindeksert mapping og MC-støy)'
    
    # =========================================================================
    # STRIKT STØYHENTING
    # =========================================================================
    try:
        noise_mildir = float(dataset_noise['norskeutslipp'])
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
            # Hent verdier basert på kolonneposisjon
            year_val = str(row.iloc[3]).strip() # Kolonne 3: År
            if not year_val.replace('.0', '').isdigit():
                continue
                
            year = int(float(year_val))
            
            # Opprinnelig funksjon sjekker 2011 <= year <= 2025, og ekskluderer 2009/2010 via range
            if 2011 <= year <= 2025:
                anlegg_name = str(row.iloc[0]).strip().lower() # Kolonne 0: Anleggsnavn
                raw_value = float(row.iloc[4])                 # Kolonne 4: Årlig utslipp til vann
                
                # INVERTERT VEKT: Vi skal ha tak i de som IKKE er tilkoblet avløp
                weight = 0.5 # Default ukjent
                
                # Sjekk om navnet matcher helt eller delvis
                if any(ja_name in anlegg_name or anlegg_name in ja_name for ja_name in tilk_ja):
                    weight = 0.0  # Tilkoblet -> Skal IKKE regnes som sigevann direkte til natur
                elif any(nei_name in anlegg_name or anlegg_name in nei_name for nei_name in tilk_nei):
                    weight = 1.0  # Ikke tilkoblet -> Går 100% til natur (sigevann)
                
                # Beregn N-mengde som siver ut i naturen
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
        mean_unconnected_kt = sum(real_years_data[y] for y in valid_years) / len(valid_years)
    else:
        raise ValueError("[KRITISK] Ingen gyldige utslippsdata for deponier i perioden 2011-2025!")

    # Bygg endelig tidsrekke-ordbok
    final_values = {}
    
    for year in range(1990, 2011):
        final_values[year] = mean_unconnected_kt

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
        if val < 0 or pd.isna(val): 
            val = 0.0
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': comment,
            'data_sources': 'Utslipp_deponi.xlsx (Mildir)' if year >= 2011 else 'extrapolated'
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_export_for_recycling_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    """
    MC-VERSJON: Legger til eksport for resirkulering i resultatlisten.
    Her sender vi inn resultatlisten direkte til find-funksjonen for full automatisering.
    """
    flow_code = 'PR.SO-RW.RW-Export for recycling-Nmix'
    data_sources = 'SSB'
    collected_years = set()
    
    # Vi lar find-funksjonen populere resultatlisten (results) direkte via den generiske motoren.
    # Dette håndterer årstall, støy, kommentarer og fyller manglende år med NaN automatisk.
    year_values = find_export_for_recycling(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        dataset_noise=dataset_noise
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


def _add_export_for_reuse_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    """
    MC-VERSJON: Legger til eksport for gjenbruk i resultatlisten.
    """
    flow_code = 'PR.SO-RW.RW-Export for reuse-Nmix'
    data_sources = 'SSB'
    collected_years = set()
    
    # Samme her: Vi videresender resultatlisten slik at kjernefunksjonen gjør hele jobben.
    year_values = find_export_for_reuse(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        dataset_noise=dataset_noise
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

    
def _add_ww_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: N2O-utslipp til atmosfære fra avløpshåndtering (PR.WW-AT.AT-Emissions-N2O).
    Henter ferdiginnlastet CSV-data (N2O_SO.csv) fra RAM og påfører sentralt trukket datasettstøy.
    """
    flow_code = 'PR.WW-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'UNFCCC CRT'

    # 1. Hent og valider globale parametere
    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    
    # 2. Slå opp ferdig generert støy – krasj hvis nøkkelen mangler
    key_n2o = 'UNFCCC_emissions'
    if not dataset_noise or key_n2o not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_n2o}' mangler i dataset_noise for {flow_code}!")
    
    noise_val = dataset_noise[key_n2o]

    # 3. Hent ferdiglastet DataFrame fra RAM (bruker samme csv-grunnlag som SO)
    df_ww_emissions = preloaded_data.get('n2o_ww_raw')
    if df_ww_emissions is None:
        raise ValueError(f"[KRITISK] 'n2o_ww_raw' mangler i preloaded_data for {flow_code}!")

    # 4. Gå gjennom radene i den ferdiginnlastede CSV-filen
    for index, row in df_ww_emissions.iterrows():
        try:
            year_val = row['year']
            n2o_val = row['value']  # Kolonnenavnet i csv er 'value'
            
            if pd.isna(year_val) or pd.isna(n2o_val):
                continue
                
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
                
            collected_years.add(year)
            
            # Basisverdi konvertert til reell N-vekt
            base_value = float(n2o_val) * conv_N2O

            # Påfør støyen matematisk korrekt basert på støytype
            value = base_value * noise_val
 
            # Sikre at fysiske utslipp aldri blir negative
            if value < 0: 
                value = 0.0

            results.append({
                'flow_name': flow_code, 
                'year': year, 
                'value': float(value),
                'comment': comment, 
                'data_sources': data_sources
            })
            
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Kunne ikke prosessere rad {index} i n2o_so_raw for {flow_code}: {e}")

    # 5. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_solid_waste_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    """
    MC-VERSJON: Eksport av fast avfall (PR.SO-RW.RW-Solid waste export-Nmix).
    Gjenbruker den generiske handelsløsningen for MC med spesifikke avfallskategorier,
    og nullstiller årene før 2002 i tråd med opprinnelig historisk datagrunnlag.
    """
    flow_code = 'PR.SO-RW.RW-Solid waste export-Nmix'
    collected_years = set()
    comment = 'ok (Generisk handelsløsning med MC-støy)'
    data_sources = 'SSB tab 08801'

    # 1. Kjør den generiske handelsløsningen for å hente og beregne verdiene med støy
    # target_types tilsvarer types_to_keep fra den gamle find_solid_waste_export
    trade_results = []
    process_generic_trade_flow(
        results=trade_results, 
        preloaded_data=preloaded_data, 
        current_params=current_params,
        current_trade_factors=current_trade_factors, 
        flow_code=flow_code,
        target_types=['kommunalt_avfall', 'farlig_avfall', 'annet_avfall'],
        is_import=False,  # Eksport (tilsvarer impeks = 2)
        dataset_noise=dataset_noise
    )

    # 2. Konverter handelsresultatene til en oppslagsordbok per år
    trade_years_dict = {row['year']: row['value'] for row in trade_results}

    # 3. Bygg den endelige tidsrekken og håndter de historiske null-årene (1988-2001)
    for year in sorted(EXPECTED_YEARS):
        # Vi forholder oss til tidslinjen fra opprinnelig funksjon (f.eks. fra 1988 og utover)
        if year < 1988:
            continue
            
        collected_years.add(year)

        if 1988 <= year <= 2001:
            value = 0.0
            current_comment = comment
        else:
            # Hent den beregnede MC-verdien fra handelsfunksjonen (default til 0.0 hvis år mangler)
            value = float(trade_years_dict.get(year, 0.0))
            current_comment = comment

        # Sikre mot eventuelle NaN-verdier eller negative avvik fra støyen
        if value < 0 or pd.isna(value):
            value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': current_comment,
            'data_sources': data_sources
        })

    # 4. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
def _add_ag_sewage_sludge_fertilizer_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Avløpsslam til jordbruk (PR.WW-AG.SM-Sewage sludge fertilizer-Nmix).
    Synkronisert med faktiske Pandas-indekser fra SSB tab 05279.
    """
    flow_code = 'PR.WW-AG.SM-Sewage sludge fertilizer-Nmix'
    dataset_key = '05279'
    noise_val = dataset_noise[dataset_key]
    collected_years = set()
    comment = 'ok (MC-støy påført aktivitetsnivå og slam-N)'
    
    # Strikt parameterhenting (krasjer hvis mangler)
    N_content = float(current_params.waste_N_frac('sludge'))
    
    df_modern = preloaded_data['sewage_sludge_modern']
    df_hist = preloaded_data['sewage_sludge_historical']
    
    # 1. 2002-2024 (Nyere SSB-data via DataFrame)
    data_sources = 'SSB tab 05279'
    
    # Årene ligger i radindeks 2, fra kolonne 2 og utover
    for col_idx in range(2, len(df_modern.columns)):
        year_val = df_modern.iloc[2, col_idx]
        if year_val is None or pd.isna(year_val):
            continue
        year = int(year_val)
        
        # Jordbruksareal ligger i radindeks 4
        raw_val = df_modern.iloc[4, col_idx]
        if raw_val is None or pd.isna(raw_val):
            continue
            
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        perturbed_tonnage = raw_tonnage*noise_val
        
        # Verdi i tonn tørrstoff -> deles på 1000 for å få kilotonn
        value = (perturbed_tonnage / 1000) * N_content 
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 2. 1993-2001 (Historisk SSB-data via DataFrame)
    noise_val = dataset_noise['historical_waste']
    # Starter på radindeks 1 til og med 9
    for r in range(1, 10):  
        year_val = df_hist.iloc[r, 0]
        if year_val is None or pd.isna(year_val): 
            continue
        year = int(year_val)  
        
        raw_val = df_hist.iloc[r, 1]
        if raw_val is None or pd.isna(raw_val): 
            continue
        
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        perturbed_tonnage = raw_tonnage*noise_val
        
        # Historisk tabell er allerede i 1000 tonn, share er i %, så vi deler share på 100
        share = float(df_hist.iloc[r, 3]) / 100  # Kolonne indeks 3 er '% jordbruk'
        value = perturbed_tonnage * share * N_content  
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
            
    # 3. 1990-1992 (Ekstrapolering)
    # Henter de genererte verdiene for 1993, 1994, 1995 fra results for å beregne snittet
    values_93_95 = [res['value'] for res in results if res['flow_name'] == flow_code and res['year'] in [1993, 1994, 1995]]
    mean_val = sum(values_93_95) / 3 if values_93_95 else 0.0
    
    data_sources_ext = 'extrapolated'
    for year in range(1990, 1993):  
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': mean_val, 
            'comment': 'Ekstrapolert snitt (1993-1995) med MC-støy',
            'data_sources': data_sources_ext
        })    
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_hs_sewage_sludge_fertilizer_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Slam til grøntarealer og jordprodusenter (PR.WW-HS.HS-Sewage sludge fertilizer-Nmix).
    """
    flow_code = 'PR.WW-HS.HS-Sewage sludge fertilizer-Nmix'
    dataset_key = '05279'
    collected_years = set()
    comment = 'ok (MC-støy påført aktivitetsnivå og slam-N)'
    
    N_content = float(current_params.waste_N_frac('sludge'))
    
    df_modern = preloaded_data['sewage_sludge_modern']
    df_hist = preloaded_data['sewage_sludge_historical']
    noise_modern = dataset_noise[dataset_key]
    noise_hist = dataset_noise['historical_waste']
    
    # 1. 2002-2024
    data_sources = 'SSB table 05279'
    for col_idx in range(2, len(df_modern.columns)):
        year_val = df_modern.iloc[2, col_idx]
        if year_val is None or pd.isna(year_val):
            continue
        year = int(year_val)
            
        val_green = df_modern.iloc[5, col_idx] # Radindeks 5 (Grøntareal)
        val_soil = df_modern.iloc[6, col_idx]  # Radindeks 6 (Jordprodusent)
        
        if (val_green is None or pd.isna(val_green)) and (val_soil is None or pd.isna(val_soil)):
            continue
            
        collected_years.add(year)
        
        tonnage_green = float(val_green) if val_green is not None and not pd.isna(val_green) else 0.0
        tonnage_soil = float(val_soil) if val_soil is not None and not pd.isna(val_soil) else 0.0
        
        perturbed_green = tonnage_green*noise_modern
        perturbed_soil = tonnage_soil*noise_modern
        
        value = ((perturbed_green + perturbed_soil) / 1000) * N_content 
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 2. 1993-2001
    for r in range(1, 10):  
        year_val = df_hist.iloc[r, 0]
        if year_val is None or pd.isna(year_val): 
            continue
        year = int(year_val)  
        
        raw_val = df_hist.iloc[r, 1]
        if raw_val is None or pd.isna(raw_val): 
            continue
        
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        perturbed_tonnage = raw_tonnage*noise_hist
        
        share = float(df_hist.iloc[r, 2]) / 100  # Kolonne indeks 2 er 'grøntareal %'
        value = perturbed_tonnage * share * N_content  
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 3. 1990-1992
    values_93_95 = [res['value'] for res in results if res['flow_name'] == flow_code and res['year'] in [1993, 1994, 1995]]
    mean_val = sum(values_93_95) / 3 if values_93_95 else 0.0
    
    data_sources_ext = 'extrapolated'
    for year in range(1990, 1993):  
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': mean_val, 
            'comment': 'Ekstrapolert snitt (1993-1995) med MC-støy',
            'data_sources': data_sources_ext
        })    
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_sewage_sludge_landfill_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Slam til deponi og dekkmasse (PR.WW-PR.SO-Sewage sludge landfill-Nmix).
    """
    flow_code = 'PR.WW-PR.SO-Sewage sludge landfill-Nmix'
    dataset_key = '05279'
    collected_years = set()
    comment = 'ok (MC-støy påført aktivitetsnivå og slam-N)'
    
    N_content = float(current_params.waste_N_frac('sludge'))
    
    df_modern = preloaded_data['sewage_sludge_modern']
    df_hist = preloaded_data['sewage_sludge_historical']
    
    # 1. 2002-2024
    data_sources = 'SSB table 05279'
    noise_05279 = dataset_noise['05279']
    # Det opprinnelige skriptet stoppet på kolonne 26 i Excel (tilsvarer indeks 25 her)
    for col_idx in range(2, min(25, len(df_modern.columns))):
        year_val = df_modern.iloc[2, col_idx]
        if year_val is None or pd.isna(year_val):
            continue
        year = int(year_val)
            
        val_cover = df_modern.iloc[7, col_idx]     # Radindeks 7 (Dekkmasse avfallsfylling)
        val_landfill = df_modern.iloc[8, col_idx]  # Radindeks 8 (Slamdeponi)
        
        if (val_cover is None or pd.isna(val_cover)) and (val_landfill is None or pd.isna(val_landfill)):
            continue
            
        collected_years.add(year)
        
        tonnage_cover = float(val_cover) if val_cover is not None and not pd.isna(val_cover) else 0.0
        perturbed_cover = tonnage_cover*noise_05279
        value = (perturbed_cover / 1000) * N_content
        
        if val_landfill is not None and not isinstance(val_landfill, str) and not pd.isna(val_landfill):
            perturbed_landfill = val_landfill*noise_05279
            value += (perturbed_landfill / 1000) * N_content
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 2. 1993-2001
    noise_hist = dataset_noise['slamdisponering']
    for r in range(1, 10):  
        year_val = df_hist.iloc[r, 0]
        if year_val is None or pd.isna(year_val): 
            continue
        year = int(year_val)  
        
        raw_val = df_hist.iloc[r, 1]
        if raw_val is None or pd.isna(raw_val): 
            continue
        
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        perturbed_tonnage = raw_tonnage*noise_hist
        
        share = float(df_hist.iloc[r, 4]) / 100  # Kolonne indeks 4 er '% slamdeponi + avfallsfylling'
        value = perturbed_tonnage * share * N_content  
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 3. 1990-1992
    values_93_95 = [res['value'] for res in results if res['flow_name'] == flow_code and res['year'] in [1993, 1994, 1995]]
    mean_val = sum(values_93_95) / 3 if values_93_95 else 0.0
    
    data_sources_ext = 'extrapolated'
    for year in range(1990, 1993):  
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': mean_val, 
            'comment': 'Ekstrapolert snitt (1993-1995) med MC-støy',
            'data_sources': data_sources_ext
        })    
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_ww_N2_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: N2-utslipp til atmosfære fra denitrifikasjon i renseanlegg (PR.WW-AT.AT-Emissions-N2).
    """
    flow_code = 'PR.WW-AT.AT-Emissions-N2'
    collected_years = set()
    comment = 'ok (MC-støy påført renseanlegg og rensegrader)'
    data_sources = 'treatment plant reports (norskeutslipp.no / veas.nu)'
    dataset_key = 'nitrogenrensing_avlop'
    noise_val = dataset_noise[dataset_key]

    # 1. Hent standard rensegrad (krasjer strikt hvis parameteren mangler i MC)
    removal_default = float(current_params.get("avlop_removal_default_rate")) # f.eks. 0.7
    
    # 2. Hent eller last arket (støtter både preloaded data og direkte disk-fallback)
    N_released_df = preloaded_data.get('avlop_sewage_cleaning')
    if N_released_df is None:
        # Midlertidig fallback hvis den ikke er lagt til i data_loader.py ennå
        N_released_df = pd.read_excel("data_files/nitrogenrensing_avløp.xlsx", sheet_name="Ark1", nrows=31)

    # Klon tabellen så vi ikke muterer originalen i RAM mellom MC-iterasjonene
    df = N_released_df.copy()
    
    # Konverter alle numeriske kolonner unntatt 'år' fra tN til ktN
    num_cols = [col for col in df.columns if col != 'år']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce') / 1000.0

    # Hjelpefunksjon for å hente celler, legge på støy, og sikre mot NaN
    def _get_val(plant_column, target_year):
        row = df[df["år"] == target_year]
        if row.empty:
            raise ValueError(f"[KRITISK] Fant ikke data for år {target_year} i kolonne '{plant_column}'!")
        val = row[plant_column].iloc[0]
        if pd.isna(val) or val is None:
            return 0.0
        return float(val*noise_val)

    # Beregn historiske snitt basert på de støyiniserte kolonnene
    # (Vi gjør dette dynamisk per MC-iterasjon basert på tabellen med støy)
    mean_Lillehammer = df["Lillehammer"].mean() 
    
    mask_veas = (df["år"] >= 2002) & (df["år"] <= 2003)
    mean_Veas = df.loc[mask_veas, "VEAS"].mean()
    
    mean_NordreFollo = df["Nordre Follo"].mean()
    
    mask_gard = (df["år"] >= 2002) & (df["år"] <= 2009)
    mean_Gardermoen = df.loc[mask_gard, "Gardermoen"].mean()
    
    mean_NRVA = df["NRVA"].mean()

    # Faktor-funksjon for renseeffekt: r / (1 - r)
    def _factor(r):
        return r / (1.0 - r) if r < 1.0 else 0.0

    # 3. Hovedløkke over alle simuleringsår
    for year in EXPECTED_YEARS:
        collected_years.add(year)
        
        if year < 1995:
            value = 0.0
            
        elif year < 1997:  # Kun Lillehammer
            value = mean_Lillehammer * _factor(removal_default)
            
        elif year < 1998:  # + VEAS og Nordre Follo
            value = (mean_Lillehammer + mean_Veas + mean_NordreFollo) * _factor(removal_default)
            
        elif year < 2002:  # + Gardermoen
            value = (mean_Lillehammer + mean_Veas + mean_NordreFollo + mean_Gardermoen) * _factor(removal_default)
            
        elif year == 2002:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year + 1) * _factor(removal_default)  # Ekstrapolert fra neste år
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0  # Reverser ktN-deling for rensegrad-prosent
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            
        elif year == 2003:  # + NRVA
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += mean_NRVA * removal_default  # Beholder din originale formel for akkurat dette leddet
            
        elif year in [2004, 2005]:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += mean_NordreFollo * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year == 2006:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += mean_NordreFollo * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += mean_NRVA * _factor(removal_default)
            
        elif year in [2007, 2008]:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year in range(2009, 2012):
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year == 2012:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += mean_NordreFollo * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year in range(2013, 2016):
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year == 2016:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            value += _get_val("Bekkelaget", year) * _factor(removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year in [2017, 2018]:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            value += _get_val("Bekkelaget", year) * _factor(removal_default)
            
            rem_nrva = _get_val("rensegrad NRVA", year) * 1000.0
            value += _get_val("NRVA", year) * _factor(rem_nrva if rem_nrva > 0 else removal_default)
            
        elif year in [2019, 2020]:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            
            rem_nrva = _get_val("rensegrad NRVA", year) * 1000.0
            value += _get_val("NRVA", year) * _factor(rem_nrva if rem_nrva > 0 else removal_default)
            
        elif year == 2021:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            value += _get_val("NRVA", year) * _factor(removal_default)
            
        elif year < 2025:
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            
            rem_nrva = _get_val("rensegrad NRVA", year) * 1000.0
            value += _get_val("NRVA", year) * _factor(rem_nrva if rem_nrva > 0 else removal_default)
            
        else:  # 2025 og fremover (inkluderer Hokksund)
            value = _get_val("Lillehammer", year) * _factor(removal_default)
            value += _get_val("VEAS", year) * _factor(removal_default)
            value += _get_val("Nordre Follo", year) * _factor(removal_default)
            value += _get_val("Gardermoen", year) * _factor(removal_default)
            
            rem_bekk = _get_val("rensegrad Bekkelaget", year) * 1000.0
            value += _get_val("Bekkelaget", year) * _factor(rem_bekk if rem_bekk > 0 else removal_default)
            
            rem_nrva = _get_val("rensegrad NRVA", year) * 1000.0
            value += _get_val("NRVA", year) * _factor(rem_nrva if rem_nrva > 0 else removal_default)
            value += _get_val("Hokksund", year) * _factor(removal_default)

        # Vask mot negative verdier og NaN
        if value < 0 or pd.isna(value):
            value = 0.0

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(value),  
            'comment': comment,
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_treated_ww_discharge_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Renset avløpsvann ut i kystvann (PR.WW-HY.CW-Treated wastewater discharge-Nmix).
    STRIKT: Kaster feil hvis parametere/støy mangler. Håndterer NaN/None dataceller trygt.
    """
    flow_code = 'PR.WW-HY.CW-Treated wastewater discharge-Nmix'
    dataset_key = '05280'
    collected_years = set()
    comment = 'ok (MC-støy påført aktivitetsnivå)'
    
    df_modern = preloaded_data['hy_ssb_05280_raw']
    df_hist = preloaded_data['avlop_utslipp_historical']
    
    # 1. Nyere data: 2002 til 2024 (År i rad 2, Verdier i rad 3, fra kolonne 3 og utover)
    noise_val = dataset_noise[dataset_key]
    data_sources = 'SSB table 05280'
    max_col = min(26, df_modern.shape[1])
    
    for col_idx in range(3, max_col):
        year_val = df_modern.iloc[2, col_idx]
        raw_val = df_modern.iloc[3, col_idx]
        
        if pd.isna(year_val) or pd.isna(raw_val):
            continue
            
        try:
            year = int(float(str(year_val).strip()))
            raw_tonnage = float(raw_val)
        except (ValueError, TypeError):
            # Krasjer hardt eller varsler hvis dataen er korrupt fremfor å late som ingenting
            raise ValueError(f"[KRITISK FEIL] Klarte ikke å konvertere data i kolonne {col_idx}. År: {year_val}, Verdi: {raw_val}")
            
        collected_years.add(year)
        perturbed_tonnage = raw_tonnage*noise_val
        
        # Siden SSB-tabellen oppgir verdien direkte i tonn (f.eks. 15654.8), 
        # må vi dele på 1000 for å konvertere til ktN (kilotonn) som modellen din krever:
        value = perturbed_tonnage / 1000.0
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    # 2. Historiske data: 1997 til 2001 (Excel rad 2 til 7 -> radindeks 1 til 6)
    noise_val = dataset_noise['utslipp_avløp']
    value_1997 = None
    for r in range(1, 6):
        year_val = df_hist.iloc[r, 0]
        if year_val is None or pd.isna(year_val):
            continue
        year = int(year_val)
        
        raw_val = df_hist.iloc[r, 1]
        if raw_val is None or pd.isna(raw_val):
            continue
            
        collected_years.add(year)
        raw_tonnage = float(raw_val)
        
        # Siden den historiske tidsrekken bygger på tabell 05280s historikk, brukes samme støy-nøkkel
        perturbed_tonnage = raw_tonnage*noise_val
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': perturbed_tonnage, 
            'comment': comment,
            'data_sources': data_sources
        })
        
        if year == 1997:
            value_1997 = perturbed_tonnage

    # En kjapp, strikt validering på at vi faktisk fant verdien for 1997 (ingen tause feil/fallbacks)
    if value_1997 is None:
        raise ValueError(f"[KRITISK] Fant ikke historisk verdi for år 1997 i dataene til {flow_code}!")

    # 3. Ekstrapolering bakover: 1990 til 1996 (Konstant basert på perturbert 1997-verdi)
    data_sources_ext = 'extrapolated'
    for year in range(1990, 1997):  
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value_1997, 
            'comment': 'Ekstrapolert verdi basert på 1997 med MC-støy',
            'data_sources': data_sources_ext
        })    
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)