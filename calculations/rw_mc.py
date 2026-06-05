#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modifisert MC-VERSJON: Beregner nitrogenflyt for rest-of-world (RW).
Sikret full konsistens med sentral distribusjonstrekking i generate_mc_parameters_fast.
"""
import pandas as pd
import numpy as np

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    process_generic_trade_flow
)
from calculations.shared_flow_calculations import find_aquaculture_production

def execute_calculations_rw(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    Hovedfunksjon for RW-poolen. Kjører alle underberegninger.
    Alle distribusjoner trekkes sentralt før denne kjøres.
    """
    results = []
    
    # 1. Handelsdata (Bruker din generiske handelsmodul som håndterer trade_factors korrekt)
    _add_fuel_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_transport_fuel_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_solid_waste_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_food_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_other_goods_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_ammonia_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    
    # 2. Spesialstrømmer (Bruker ferdig generert dataset_noise og parameterstøy)
    _add_animal_feed_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_aquaculture_feed_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_live_animal_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_mineral_fertilizer_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_rw_outflow_oxn_mc(results, preloaded_data, current_params, dataset_noise)
    _add_rw_outflow_rdn_mc(results, preloaded_data, current_params, dataset_noise)
    
    return results


# =============================================================================
# HANDELSTRØMMER (Generert via felles arkitektur)
# =============================================================================

def _add_fuel_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    process_generic_trade_flow(
        results=results, preloaded_data=preloaded_data, current_params=current_params,
        current_trade_factors=current_trade_factors, flow_code='RW.RW-EF.EC-Fuel import-Nmix',
        target_types='fuel', is_import=True, dataset_noise = dataset_noise
    )        

def _add_transport_fuel_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    process_generic_trade_flow(
        results=results, preloaded_data=preloaded_data, current_params=current_params,
        current_trade_factors=current_trade_factors, flow_code='RW.RW-EF.EC-Transport fuel import-Nmix',
        target_types='transport_fuel', is_import=True, dataset_noise = dataset_noise
    )        

def _add_solid_waste_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    process_generic_trade_flow(
        results=results, preloaded_data=preloaded_data, current_params=current_params,
        current_trade_factors=current_trade_factors, flow_code='RW.RW-PR.SO-Solid waste import-Nmix',
        target_types=['kommunalt_avfall','annet_avfall','slam','farlig_avfall','tekstilavfall','plastavfall','papiravfall'],
        is_import=True, dataset_noise = dataset_noise
    )
    
def _add_food_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    process_generic_trade_flow(
        results=results, preloaded_data=preloaded_data, current_params=current_params,
        current_trade_factors=current_trade_factors, flow_code='RW.RW-MP.FP-Food import-Nmix',
        target_types=['korn/planter', 'kjøtt/fisk/meieri/egg', 'mat'],
        is_import=True, dataset_noise = dataset_noise
    )
    
def _add_other_goods_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    process_generic_trade_flow(
        results=results, preloaded_data=preloaded_data, current_params=current_params,
        current_trade_factors=current_trade_factors, flow_code='RW.RW-MP.OP-Other goods import -Nmix',
        target_types=['organisk materiale','blomster','frø','kjemikalier','såpe','industrielt protein',
                      'plastprodukter','gummi','skinn','lærprodukter','tre','silke','ull',
                      'bomull','nylon','tekstil','møller','plast','leker','plastavfall','tekstil_brukt'],
        is_import=True, dataset_noise = dataset_noise
    )
    
def _add_ammonia_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    process_generic_trade_flow(
        results=results, preloaded_data=preloaded_data, current_params=current_params,
        current_trade_factors=current_trade_factors, flow_code='RW.RW-MP.OP-Ammonia import -Nmix',
        target_types='NH3', is_import=True, dataset_noise = dataset_noise
    )        


# =============================================================================
# SPESIALBEREGNINGER MED DATASETT- OG PARAMETERSTØY
# =============================================================================

def _add_animal_feed_import_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Kraftfôrimport. Ingen distribusjoner trekkes her.
    Sikret robust fallback hvis Excel-ark inneholder uventet 'abs'-støy.
    """
    flow_code = 'RW.RW-AG.MM-Animal feed import-Nmix'
    collected_years = set()
    
    df_raavarer = preloaded_data.get('feed_raavarer')
    df_totalkalkyle = preloaded_data.get('feed_totalkalkyle')
    
    if df_raavarer is None or df_totalkalkyle is None:
        print(f"[ADVARSEL] Mangler fôrdata i preloaded_data for {flow_code}.")
        return

    # Globale parametere (Allerede perturbert sentralt)
    N_content_carb = float(current_params.get("feed_carb_N_frac", 0.015))
    N_content_prot = float(current_params.get("feed_prot_N_frac", 0.070))
    
    # Datasetstøy: Kraftfôrstatistikk
    key_kraft = 'Kraftforstatistikk'
    has_noise_kraft = dataset_noise and key_kraft in dataset_noise
    noise_kraft = dataset_noise[key_kraft]['value'] if has_noise_kraft else 1.0
    type_kraft = dataset_noise[key_kraft]['type'] if has_noise_kraft else 'perc'
    
    # Datasetstøy: Totalkalkylen
    key_total = 'Totalkalkylen'
    has_noise_total = dataset_noise and key_total in dataset_noise
    noise_total = dataset_noise[key_total]['value'] if has_noise_total else 1.0
    type_total = dataset_noise[key_total]['type'] if has_noise_total else 'perc'

    # --- Nyere år (Landbruksdirektoratet) ---
    N_cont_sum = 0
    valid_count = 0
    
    for _, row in df_raavarer.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        
        base_carb = float(row['value_carb'])
        base_prot = float(row['value_prot'])
        
        # Robust støy-påføring (Støtter både perc og abs for mengdedata)
        if has_noise_kraft and type_kraft == 'perc':
            value_carb = base_carb * noise_kraft
            value_prot = base_prot * noise_kraft
        elif has_noise_kraft and type_kraft == 'abs':
            # Absolutt støy fordeles proporsjonalt eller legges flatt (her flatt pr fraksjon som sikkerhet)
            bound = dataset_noise[key_kraft]['upp_bound'] if noise_kraft >= 0 else dataset_noise[key_kraft]['low_bound']
            value_carb = base_carb + (noise_kraft * bound / 2)
            value_prot = base_prot + (noise_kraft * bound / 2)
        else:
            value_carb = base_carb
            value_prot = base_prot
            
        imported_feed_N = (value_carb * N_content_carb + value_prot * N_content_prot) / 1000
        if imported_feed_N < 0: imported_feed_N = 0.0
            
        results.append({
            'flow_name': flow_code, 'year': year, 'value': imported_feed_N,
            'comment': 'ok (MC-støy lagt på)',
            'data_sources': 'Landbruksdirektoratets kraftfôrstatistikk'
        })
        
        if (base_carb + base_prot) > 0:
            N_cont_sum += ((base_carb * N_content_carb + base_prot * N_content_prot) / (base_carb + base_prot))
            valid_count += 1

    N_cont_before_2000 = (N_cont_sum / valid_count) if valid_count > 0 else 0.025

    # --- Eldre år (NIBIO Totalkalkylen) ---
    for _, row in df_totalkalkyle.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        
        base_feed_tonn = float(row['value'])
        
        if has_noise_total and type_total == 'perc':
            feed_tonn = base_feed_tonn * noise_total
        elif has_noise_total and type_total == 'abs':
            bound = dataset_noise[key_total]['upp_bound'] if noise_total >= 0 else dataset_noise[key_total]['low_bound']
            feed_tonn = base_feed_tonn + (noise_total * bound)
        else:
            feed_tonn = base_feed_tonn
            
        dom_frac = float(row['dom_frac']) if year < 1995 else 0.694
        comment = 'ok (MC-støy lagt på)' if year < 1995 else 'interpolated (MC-støy lagt på)'
        
        value_kt_N = feed_tonn * 1e-3 * N_cont_before_2000 * (1 - dom_frac)
        if value_kt_N < 0: value_kt_N = 0.0
            
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value_kt_N,
            'comment': comment, 'data_sources': 'NIBIO Totalkalkylen'
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_aquaculture_feed_import_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Havbruksfôr. Alt av støy er ferdig beregnet i find_aquaculture_production
    og i parameter-overrides. Ingen trekninger her.
    """
    flow_code = 'RW.RW-HY.AC-Aquaculture feed import-Nmix'
    collected_years = set()
    
    df_modern = preloaded_data.get('aqua_modern')
    df_old = preloaded_data.get('aqua_old')
    if df_modern is None or df_old is None: return

    # find_aquaculture_production bruker ferdigstøysatte parametere internt!
    aquaculture_production = find_aquaculture_production(df_modern, df_old, current_params, dataset_noise)

    import_fraction = float(current_params.get("aquafeed_import_fraction", 0.80))
    prot_ret = float(current_params.get("aquafeed_N_retention", 0.35))
    feed_waste = float(current_params.get("aquafeed_waste_fraction", 0.05))

    for year, fish_harvested_N in aquaculture_production.items():
        if year not in EXPECTED_YEARS: continue
        collected_years.add(year)
        
        eaten_feed_N = (fish_harvested_N / prot_ret) if prot_ret > 0 else 0.0
        total_feed_N = (eaten_feed_N / (1 - feed_waste)) if feed_waste < 1 else 0.0
        imported_feed_N = total_feed_N * import_fraction
        
        if imported_feed_N < 0: imported_feed_N = 0.0
            
        results.append({
            'flow_name': flow_code, 'year': year, 'value': float(imported_feed_N),
            'comment': 'ok (MC-støy beregnet via felles produksjonsmatrise)', 'data_sources': 'Fiskeridirektoratet'
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_live_animal_import_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Levende dyr. Slår opp ferdig perturberte vekter ('weight_HORSES' osv) 
    fra parametergeneratoren. Ingen trekking eller .join() her.
    """
    flow_code = 'RW.RW-AG.MM-Live animal import-Nmix'
    collected_years = set()
    
    final_data = preloaded_data.get('fao_live_animals')
    if final_data is None: return

    prot_frac = float(current_params.get("live_animal_protein_frac", 0.15))
    prot_to_N = float(current_params.get("Jones_factor", 6.25))

    key_fao = 'Crops and livestock products'
    has_noise_fao = dataset_noise and key_fao in dataset_noise
    noise_fao = dataset_noise[key_fao]['value'] if has_noise_fao else 1.0

    df_round = final_data.copy()
    if has_noise_fao and dataset_noise[key_fao]['type'] == 'perc':
        df_round['perturbed_value'] = df_round['Value'] * noise_fao
    else:
        df_round['perturbed_value'] = df_round['Value']

    # Henter de ferdig perturberte enkeltvektene fra ordboken
    def get_perturbed_weight(item_name):
        return float(current_params.get(f"weight_{str(item_name).strip()}", 100.0))

    df_round['perturbed_weight'] = df_round['Item'].apply(get_perturbed_weight)
    df_round['N_amount'] = (df_round['perturbed_weight'] * df_round['perturbed_value'] * prot_frac * 1e-6 / prot_to_N)

    total_N_per_year = df_round.groupby('Year')['N_amount'].sum().to_dict()
    
    for year in sorted(EXPECTED_YEARS):
        if year in total_N_per_year:
            collected_years.add(year)
            val = total_N_per_year[year]
            if val < 0: val = 0.0
            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(val),
                'comment': 'ok (MC-støy ferdig beregnet sentralt)', 'data_sources': 'FAOSTAT'
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_mineral_fertilizer_import_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Mineralgjødsel. Vektorisert og henter ferdig støy fra RAM.
    """
    flow_code = 'RW.RW-AG.SM-Mineral fertilizer import-Nmix'
    collected_years = set()
    
    final_data = preloaded_data.get('fao_mineral_fertilizer')
    if final_data is None: return

    key_fert = 'Fertilizer by nutrient'
    has_noise_fert = dataset_noise and key_fert in dataset_noise
    noise_fert = dataset_noise[key_fert]['value'] if has_noise_fert else 1.0
    
    total_fert_per_year = final_data.groupby('Year')['Value'].sum().to_dict()
    
    for year in sorted(EXPECTED_YEARS):
        if year in total_fert_per_year:
            collected_years.add(year)
            base_value = float(total_fert_per_year[year])
            
            if has_noise_fert and dataset_noise[key_fert]['type'] == 'perc':
                perturbed_value = base_value * noise_fert
            else:
                perturbed_value = base_value
            
            value_kt = perturbed_value / 1000.0
            if value_kt < 0: value_kt = 0.0
                
            results.append({
                'flow_name': flow_code, 'year': year, 'value': value_kt,
                'comment': 'ok (MC-støy ferdig beregnet sentralt)', 'data_sources': 'FAOSTAT'
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


# =============================================================================
# ATMOSFÆRISKE STRØMMER (Sikret konsistent signatur mot preloaded_data og fortegn)
# =============================================================================

def _add_rw_outflow_oxn_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Oksidert nitrogen-innsig.
    Henter df_rw direkte fra preloaded_data for konsistent arkitektur.
    """
    flow_code = 'RW.RW-AT.AT-Atmospheric inflow-OXN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på kildens usikkerhetstype)'
    
    df_rw = preloaded_data.get('atm_in_out')
    if df_rw is None: return

    for r in range(5, 45):
        if r >= len(df_rw): break
            
        year_val = df_rw.iloc[r, 0]
        if pd.isna(year_val): continue
            
        year = int(year_val)
        collected_years.add(year)
        
        status_val = str(df_rw.iloc[r, 5]).strip()
        dataset_key = 'trend interpolation' if status_val == 'interpolated' else 'Source-receptor'
        data_sources = 'interpolated' if status_val == 'interpolated' else 'EMEP SR tables'
            
        base_value = float(df_rw.iloc[r, 1]) / 10  # 100 tN -> ktN
        
        # Sjekk ferdigstilt støy
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        if has_noise:
            noise_info = dataset_noise[dataset_key]
            noise_val = noise_info['value']
            
            if noise_info['type'] == 'perc':
                value = base_value * noise_val
            else:
                # Matematisk korrekt asymmetrisk håndtering: 
                # Hvis noise_val er negativ, vil "+ (negativ * positiv_Excel_verdi)" korrekt trekke fra verdien.
                bound = noise_info['upp_bound'] if noise_val >= 0 else noise_info['low_bound']
                value = base_value + (noise_val * bound)
        else:
            value = base_value
            
        if value < 0: value = 0.0
            
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': comment, 'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_rw_outflow_rdn_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Redusert nitrogen-innsig.
    Henter df_rw direkte fra preloaded_data for konsistent arkitektur.
    """
    flow_code = 'RW.RW-AT.AT-Atmospheric inflow-RDN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på kildens usikkerhetstype)'
    
    df_rw = preloaded_data.get('atm_in_out')
    if df_rw is None: return
    
    for r in range(5, 45): 
        if r >= len(df_rw): break
            
        year_val = df_rw.iloc[r, 0]
        if pd.isna(year_val): continue
            
        year = int(year_val)
        collected_years.add(year)
        
        status_val = str(df_rw.iloc[r, 5]).strip()
        dataset_key = 'trend interpolation' if status_val == 'interpolated' else 'Source-receptor'
        data_sources = 'interpolated' if status_val == 'interpolated' else 'EMEP SR tables'
            
        base_value = float(df_rw.iloc[r, 3]) / 10  # 100 tN -> ktN
        
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        if has_noise:
            noise_info = dataset_noise[dataset_key]
            noise_val = noise_info['value']
            
            if noise_info['type'] == 'perc':
                value = base_value * noise_val
            else:
                bound = noise_info['upp_bound'] if noise_val >= 0 else noise_info['low_bound']
                value = base_value + (noise_val * bound)
        else:
            value = base_value
            
        if value < 0: value = 0.0
            
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': comment, 'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)