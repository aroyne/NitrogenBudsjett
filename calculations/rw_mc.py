#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    process_generic_trade_flow
)
from calculations.shared_flow_calculations import find_aquaculture_production

def execute_calculations_rw(preloaded_data, current_params, dataset_noise, current_trade_factors):
    results = []
    
    _add_fuel_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_transport_fuel_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_solid_waste_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_food_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_other_goods_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_ammonia_import(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    
    _add_animal_feed_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_aquaculture_feed_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_live_animal_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_mineral_fertilizer_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_rw_outflow_oxn_mc(results, preloaded_data, current_params, dataset_noise)
    _add_rw_outflow_rdn_mc(results, preloaded_data, current_params, dataset_noise)
    
    return results


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


def _add_animal_feed_import_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'RW.RW-AG.MM-Animal feed import-Nmix'
    collected_years = set()
    
    df_raavarer = preloaded_data.get('feed_raavarer_import')
    df_totalkalkyle = preloaded_data.get('feed_totalkalkyle')
    
    N_content_carb = float(current_params.get("feed_carb_N_frac"))
    N_content_prot = float(current_params.get("feed_prot_N_frac"))
    
    param_key_dom_frac = "feed_historical_dom_frac"
    global_dom_frac_fallback = float(current_params.get(param_key_dom_frac))
    
    key_kraft = 'Kraftforstatistikk'
    noise_kraft = dataset_noise[key_kraft]
    key_total = 'Totalkalkylen'
    noise_total = dataset_noise[key_total]

    # --- Nyere år (Landbruksdirektoratet) ---
    N_cont_sum = 0
    valid_count = 0
    
    for idx, row in df_raavarer.iterrows():
        val_at_year = str(row['year']).strip()
        if val_at_year.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        year = int(float(val_at_year))
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            
            base_carb = float(row['value_carb'])
            base_prot = float(row['value_prot'])
            
            value_carb = base_carb * noise_kraft
            value_prot = base_prot * noise_kraft
                
            imported_feed_N = (value_carb * N_content_carb + value_prot * N_content_prot) / 1000
            imported_feed_N = max(0.0, imported_feed_N)
                
            results.append({
                'flow_name': flow_code, 'year': year, 'value': imported_feed_N,
                'comment': 'ok (MC-støy lagt på)',
                'data_sources': 'Landbruksdirektoratets kraftfôrstatistikk'
            })
            
            if (base_carb + base_prot) > 0:
                N_cont_sum += ((base_carb * N_content_carb + base_prot * N_content_prot) / (base_carb + base_prot))
                valid_count += 1

    N_cont_before_2000 = N_cont_sum / valid_count

    # --- Eldre år (NIBIO Totalkalkylen) ---
    for idx, row in df_totalkalkyle.iterrows():
        val_at_year = str(row['year']).strip()
        if val_at_year.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        year = int(float(val_at_year))
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            
            base_feed_tonn = float(row['value'])                
            feed_tonn = base_feed_tonn * noise_total
            
            # Sjekker om dom_frac mangler i Excel-filen
            if 'dom_frac' not in row or pd.isna(row['dom_frac']):
                if year >= 1995:
                    dom_frac = global_dom_frac_fallback
                    comment = f'interpolated (Mangler dom_frac i kilde, satt til perturbert parameter {param_key_dom_frac})'
                else:
                    raise ValueError(f"År {year} mangler 'dom_frac' i kilde og faller utenfor gyldig tidsintervall for parameter-fallback.")
            else:
                dom_frac = float(row['dom_frac'])
                comment = 'ok (MC-støy lagt på)' if year < 1995 else 'interpolated (MC-støy lagt på)'
            
            value_kt_N = feed_tonn * 1e-3 * N_cont_before_2000 * (1 - dom_frac)
            value_kt_N = max(0.0, value_kt_N)
                
            results.append({
                'flow_name': flow_code, 'year': year, 'value': value_kt_N,
                'comment': comment, 'data_sources': 'NIBIO Totalkalkylen'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    

def _add_aquaculture_feed_import_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'RW.RW-HY.AC-Aquaculture feed import-Nmix'
    collected_years = set()
    
    df_modern = preloaded_data.get('aqua_modern')
    df_old = preloaded_data.get('aqua_old')

    aquaculture_production = find_aquaculture_production(df_modern, df_old, current_params, dataset_noise)

    import_fraction = float(current_params.get("aquafeed_import_fraction"))
    prot_ret = float(current_params.get("aquafeed_N_retention"))
    feed_waste = float(current_params.get("aquafeed_waste_fraction"))

    for year, fish_harvested_N in aquaculture_production.items():
        if year not in EXPECTED_YEARS: 
            continue
        collected_years.add(year)
        
        eaten_feed_N = fish_harvested_N / prot_ret
        total_feed_N = eaten_feed_N / (1 - feed_waste)
        imported_feed_N = total_feed_N * import_fraction
        imported_feed_N = max(0.0, imported_feed_N)
            
        results.append({
            'flow_name': flow_code, 'year': year, 'value': float(imported_feed_N),
            'comment': 'ok (MC-støy beregnet via felles produksjonsmatrise)', 'data_sources': 'Fiskeridirektoratet'
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_live_animal_import_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'RW.RW-AG.MM-Live animal import-Nmix'
    collected_years = set()
    
    final_data = preloaded_data.get('fao_live_animals')

    prot_frac = float(current_params.get("live_animal_protein_frac"))
    prot_to_N = float(current_params.get("Jones_factor"))

    key_fao = 'Crops and livestock products'
    noise_fao = dataset_noise[key_fao]

    df_round = final_data.copy()
    df_round['perturbed_value'] = df_round['Value'] * noise_fao

    def get_perturbed_weight(item_name):
        param_key = f"weight_{str(item_name).strip()}"
        try:
            return float(current_params.get(param_key))
        except KeyError:
            # Godtatt fallback for sjeldne dyrearter som ikke er definert i N_parameters
            return 0.0

    df_round['perturbed_weight'] = df_round['Item'].apply(get_perturbed_weight)
    df_round['N_amount'] = (df_round['perturbed_weight'] * df_round['perturbed_value'] * prot_frac * 1e-6 / prot_to_N)

    total_N_per_year = df_round.groupby('Year')['N_amount'].sum().to_dict()
    
    for year in sorted(EXPECTED_YEARS):
        if year in total_N_per_year:
            collected_years.add(year)
            val = max(0.0, total_N_per_year[year])
            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(val),
                'comment': 'ok (MC-støy ferdig beregnet sentralt, uvesentlige arter satt til 0.0)', 'data_sources': 'FAOSTAT'
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_mineral_fertilizer_import_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'RW.RW-AG.SM-Mineral fertilizer import-Nmix'
    collected_years = set()
    
    final_data = preloaded_data.get('fao_mineral_fertilizer')
    key_fert = 'Fertilizer by nutrient'
    noise_fert = dataset_noise[key_fert]
    
    final_data.columns = [col.strip() for col in final_data.columns]
    import_data = final_data[final_data['Element'].str.strip() == 'Import quantity']
    total_fert_per_year = import_data.groupby('Year')['Value'].sum().to_dict()
    
    for year in sorted(EXPECTED_YEARS):
        if year in total_fert_per_year:
            collected_years.add(year)
            base_value = float(total_fert_per_year[year])            
            perturbed_value = base_value * noise_fert
            
            # Konverterer fra tonn (t) til kilotonn (ktN)
            value_kt = max(0.0, perturbed_value / 1000.0)
                
            results.append({
                'flow_name': flow_code, 'year': year, 'value': value_kt,
                'comment': 'ok (MC-støy ferdig beregnet sentralt)', 'data_sources': 'FAOSTAT'
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_rw_outflow_oxn_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'RW.RW-AT.AT-Atmospheric inflow-OXN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på kildens usikkerhetstype)'
    
    df_rw = preloaded_data.get('atm_in_out')

    for r in range(5, 45):
        # if r >= len(df_rw): 
        #     break
            
        val_at_year = str(df_rw.iloc[r, 0]).strip()
            
        year = int(float(val_at_year))
        collected_years.add(year)
        
        status_val = str(df_rw.iloc[r, 5]).strip()
        dataset_key = 'trend interpolation' if status_val == 'interpolated' else 'Source-receptor'
        data_sources = 'interpolated' if status_val == 'interpolated' else 'EMEP SR tables'
            
        base_value = float(df_rw.iloc[r, 1]) / 10  # 100 tN -> ktN
        
        if not dataset_noise or dataset_key not in dataset_noise:
            raise KeyError(f"[KRITISK] Atmosfærisk støy-nøkkel '{dataset_key}' mangler i dataset_noise for {flow_code}!")
            
        noise_val = dataset_noise[dataset_key]
        value = base_value * noise_val
            
        value = max(0.0, value)
            
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': comment, 'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_rw_outflow_rdn_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'RW.RW-AT.AT-Atmospheric inflow-RDN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på kildens usikkerhetstype)'
    
    df_rw = preloaded_data.get('atm_in_out')
    
    for r in range(5, 45): 
        # if r >= len(df_rw): 
        #     break
            
        val_at_year = str(df_rw.iloc[r, 0]).strip()
        if val_at_year.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        year = int(float(val_at_year))
        collected_years.add(year)
        
        status_val = str(df_rw.iloc[r, 5]).strip()
        dataset_key = 'trend interpolation' if status_val == 'interpolated' else 'Source-receptor'
        data_sources = 'interpolated' if status_val == 'interpolated' else 'EMEP SR tables'
            
        base_value = float(df_rw.iloc[r, 3]) / 10  # 100 tN -> ktN
        
        noise_val = dataset_noise[dataset_key]
        value = base_value * noise_val
            
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': comment, 'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)