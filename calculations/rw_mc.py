#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rest of world (RW) pool: imports into Norway (fuel, food, feed, live animals,
fertilizer, other goods) and atmospheric inflow (transboundary transport of
N into Norway).
"""
import pandas as pd

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    process_generic_trade_flow
)
from calculations.shared_flow_calculations import find_aquaculture_production, get_aquafeed_budget, get_aquafeed_import_fraction

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

    # 'atm_in_out' <- atm_in_out.xlsx (data_loader.py DATA_MAP): EMEP
    # source-receptor data for Norway
    df_atm = preloaded_data.get('atm_in_out')
    _add_atmospheric_inflow_mc(results, 'RW.RW-AT.AT-Atmospheric inflow-OXN', 1, df_atm, current_params, dataset_noise)
    _add_atmospheric_inflow_mc(results, 'RW.RW-AT.AT-Atmospheric inflow-RDN', 3, df_atm, current_params, dataset_noise)

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
        current_trade_factors=current_trade_factors, flow_code='RW.RW-EF.TR-Import of transport fuel-Nmix',
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
    
    # 'feed_raavarer_import' <- Årlig råvareforbruk.xlsx (data_loader.py
    # DATA_MAP, 'excel_feed_raavarer_import' method): Landbruksdirektoratets
    # kraftfôrstatistikk, imported raw materials for concentrate feed
    df_raavarer = preloaded_data.get('feed_raavarer_import')
    # 'feed_totalkalkyle' <- NibioStatistics-4.xlsx (data_loader.py DATA_MAP):
    # NIBIO Totalkalkylen, purchased concentrate feed (tonnes, price,
    # domestically produced fraction), 1985-1999
    df_totalkalkyle = preloaded_data.get('feed_totalkalkyle')

    N_content_carb = float(current_params.get("feed_carb_N_frac"))
    N_content_prot = float(current_params.get("feed_prot_N_frac"))
    
    param_key_dom_frac = "feed_historical_dom_frac"
    global_dom_frac_fallback = float(current_params.get(param_key_dom_frac))
    
    key_kraft = 'Kraftforstatistikk'
    noise_kraft = dataset_noise[key_kraft]
    key_total = 'Totalkalkylen'
    noise_total = dataset_noise[key_total]

    # Newer years (Landbruksdirektoratet), 2000 onward.
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

            results.append({
                'flow_name': flow_code, 'year': year, 'value': imported_feed_N,
                'comment': 'ok',
                'data_sources': 'Landbruksdirektoratets kraftfôrstatistikk'
            })

            if (base_carb + base_prot) > 0:
                N_cont_sum += ((base_carb * N_content_carb + base_prot * N_content_prot) / (base_carb + base_prot))
                valid_count += 1

    # Average N content per tonne of imported raw feed material across
    # 2000+, used below as a stand-in for the earlier Totalkalkylen-era
    # tonnage, which isn't broken down by carbohydrate/protein content.
    N_cont_before_2000 = N_cont_sum / valid_count

    # Older years (NIBIO Totalkalkylen), 1985-1999.
    for idx, row in df_totalkalkyle.iterrows():
        val_at_year = str(row['year']).strip()
        if val_at_year.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue
            
        year = int(float(val_at_year))
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            
            base_feed_tonn = float(row['value'])                
            feed_tonn = base_feed_tonn * noise_total
            
            # 'dom_frac' (domestically produced fraction) is reported directly
            # for 1985-1994; later years fall back to the cross-year average.
            if 'dom_frac' not in row or pd.isna(row['dom_frac']):
                dom_frac = global_dom_frac_fallback
            else:
                dom_frac = float(row['dom_frac'])

            value_kt_N = feed_tonn * 1e-3 * N_cont_before_2000 * (1 - dom_frac)

            results.append({
                'flow_name': flow_code, 'year': year, 'value': value_kt_N,
                'comment': 'ok', 'data_sources': 'NIBIO Totalkalkylen'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    

def _add_aquaculture_feed_import_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'RW.RW-HY.AC-Aquaculture feed import-Nmix'
    collected_years = set()
    
    # 'aqua_modern'/'aqua_old' <- A.06.002_20251111-140559.xlsx (1994 onward)
    # and akvakultur_1984_1994.xlsx (data_loader.py DATA_MAP, 'excel_aquaculture'
    # method): Fiskeridirektoratet aquaculture sales of salmon/trout by county,
    # species and year, extended backward with a historical compilation
    df_modern = preloaded_data.get('aqua_modern')
    df_old = preloaded_data.get('aqua_old')

    aquaculture_production = find_aquaculture_production(df_modern, df_old, current_params, dataset_noise)

    for year, fish_harvested_N in aquaculture_production.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)

        # get_aquafeed_budget splits harvested fish N into the same
        # underlying feed budget used by MP.FP-HY.AC-Feed to coastal
        # aquaculture-Nmix in mp_mc.py, which keeps only the domestic share
        # of this same total.
        total_feed_N, _, _, _ = get_aquafeed_budget(fish_harvested_N, year, current_params, dataset_noise)
        # get_aquafeed_import_fraction (see its docstring) replaces a flat
        # import share with one that varies by year.
        import_fraction = get_aquafeed_import_fraction(year, current_params, dataset_noise)
        imported_feed_N = total_feed_N * import_fraction

        results.append({
            'flow_name': flow_code, 'year': year, 'value': float(imported_feed_N),
            'comment': 'ok', 'data_sources': 'Fiskeridirektoratet'
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_live_animal_import_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'RW.RW-AG.MM-Live animal import-Nmix'
    collected_years = set()
    
    # 'fao_live_animals' <- FAOSTAT_data_en_11-12-2025.csv (data_loader.py
    # DATA_MAP, 'csv_live_animals' method): FAOSTAT crop and livestock
    # products, import quantity of live animals
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
            # Intentional: FAOSTAT includes animal types this model doesn't
            # assign a weight to (see the same fallback in ag_mc.py's
            # _add_live_animal_export_mc); their contribution is dropped
            # rather than the whole flow crashing.
            return 0.0

    df_round['perturbed_weight'] = df_round['Item'].apply(get_perturbed_weight)
    df_round['N_amount'] = (df_round['perturbed_weight'] * df_round['perturbed_value'] * prot_frac * 1e-6 / prot_to_N)

    total_N_per_year = df_round.groupby('Year')['N_amount'].sum().to_dict()

    for year in sorted(EXPECTED_YEARS):
        if year in total_N_per_year:
            collected_years.add(year)
            val = total_N_per_year[year]
            results.append({
                'flow_name': flow_code, 'year': year, 'value': float(val),
                'comment': 'ok', 'data_sources': 'FAOSTAT'
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_mineral_fertilizer_import_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'RW.RW-AG.SM-Mineral fertilizer import-Nmix'
    collected_years = set()
    
    # 'fao_mineral_fertilizer' <- FAOSTAT_data_en_11-12-2025-2.csv
    # (data_loader.py DATA_MAP): FAOSTAT fertilizer by nutrient, export
    # quantity (also used here for its import-quantity rows)
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

            value_kt = perturbed_value / 1000.0  # tonnes -> kt

            results.append({
                'flow_name': flow_code, 'year': year, 'value': value_kt,
                'comment': 'ok', 'data_sources': 'FAOSTAT'
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_atmospheric_inflow_mc(results, flow_code, value_col, df_rw, current_params, dataset_noise):
    """
    Shared implementation for atmospheric inflow (transboundary transport of N
    into Norway), for both OXN (value_col=1, 'NOx in' in atm_in_out.xlsx) and
    RDN (value_col=3, 'NH3 in'). Source rows are in units of 100 t N (see the
    file header), so dividing by 10 converts to kt N. Mirrors
    at_mc.py's _add_atmospheric_outflow_mc, which reads the 'out' columns of
    the same file for the reverse direction.
    """
    collected_years = set()
    comment = 'ok'

    for r in range(5, 45):
        year_val = df_rw.iloc[r, 0]
        if pd.isna(year_val):
            continue

        year = int(year_val)
        collected_years.add(year)

        status_val = str(df_rw.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'

        base_value = float(df_rw.iloc[r, value_col]) / 10
        noise_val = dataset_noise[dataset_key]
        value = base_value * noise_val

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': comment,
            'data_sources': data_sources
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)