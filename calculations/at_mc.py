#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atmosphere (AT) pool: biological/industrial N2 fixation, atmospheric deposition
to other pools, and atmospheric outflow (transboundary transport out of Norway).
"""
import pandas as pd
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    process_generic_trade_flow
)

def execute_calculations_at(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    Main function for the AT (atmosphere) pool. Runs all sub-calculations:
    biological/industrial N2 fixation, atmospheric deposition to other pools,
    and atmospheric outflow (transboundary transport out of Norway).
    """
    results = []

    # 'atm_in_out' <- data_files/atm_in_out.xlsx: EMEP source-receptor data for Norway
    # (https://www.emep.int/mscw/mscw_srdata.html, downloaded Nov 2025)
    df_atm = preloaded_data.get('atm_in_out')

    _add_atmospheric_outflow_mc(results, 'AT.AT-RW.RW-Atmospheric outflow-OXN', 2, df_atm, current_params, dataset_noise)
    _add_atmospheric_outflow_mc(results, 'AT.AT-RW.RW-Atmospheric outflow-RDN', 4, df_atm, current_params, dataset_noise)
    
    # process_generic_trade_flow reads preloaded_data['compressed_trade_volume'],
    # built in data_loader.py from data_files/Tab_08801_1988_2024.csv (SSB table
    # 08801, full Norwegian import/export statistics by HS commodity code).
    ammonia_import_dict = process_generic_trade_flow(
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        target_types='NH3',  
        is_import=True,
        dataset_noise=dataset_noise
    )    
    
    ammonia_export_dict = process_generic_trade_flow(
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        target_types='NH3',  
        is_import=False,
        dataset_noise=dataset_noise
    )  
            
    _add_OP_N2_fixation_mc(results, preloaded_data, current_params, ammonia_import_dict, ammonia_export_dict, dataset_noise)    
    
    _add_AG_N2_fixation_mc(results, current_params)
    _add_FO_N2_fixation_mc(results, current_params)
    _add_OL_N2_fixation_mc(results, current_params)
    _add_SW_N2_fixation_mc(results, current_params)
    
    _deposition_flow_mc(results, 'AT.AT-AG.SM-Deposition-OXN', 'jordbruk', 'NOx', preloaded_data, current_params, dataset_noise)    
    _deposition_flow_mc(results, 'AT.AT-AG.SM-Deposition-RDN', 'jordbruk', 'Nred', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-FS.FO-Deposition-OXN', 'skog', 'NOx', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-FS.FO-Deposition-RDN', 'skog', 'Nred', preloaded_data, current_params, dataset_noise)  
    _deposition_flow_mc(results, 'AT.AT-FS.OL-Deposition-OXN', 'annet', 'NOx', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-FS.OL-Deposition-RDN', 'annet', 'Nred', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-HS.HS-Deposition-OXN', 'bebyggelse', 'NOx', preloaded_data, current_params, dataset_noise) 
    _deposition_flow_mc(results, 'AT.AT-HS.HS-Deposition-RDN', 'bebyggelse', 'Nred', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-HY.SW-Deposition-OXN', 'overflatevann', 'NOx', preloaded_data, current_params, dataset_noise)
    _deposition_flow_mc(results, 'AT.AT-HY.SW-Deposition-RDN', 'overflatevann', 'Nred', preloaded_data, current_params, dataset_noise)

    return results


def _deposition_flow_mc(results, flow_code, class4, poll, preloaded_data, current_params, dataset_noise):
    # 'deposition_data' <- data_files/N_per_class_period_distributed_unallocated_long.csv:
    # atmospheric N deposition (tonnes) by 5-year period, pollutant (NOx/Nred) and
    # class4 (receiving land-use class: jordbruk/skog/annet/bebyggelse/overflatevann).
    # Source: NILU gridded deposition data, Blake et al. (2023), distributed across
    # land classes using the NIBIO AR5 map (see atmosphere_pool/flow_AT_AT_*_Deposition_*.md).
    data = preloaded_data.get('deposition_data')
    key_dep = 'Deposition'
    key_interp = 'trend interpolation'

    mask_base = (data["pollutant"] == poll) & (data["class4"] == class4)
    df_subset = data[mask_base]
    period_map = dict(zip(df_subset["period"], df_subset["N_tonn"]))

    def period_for_year(y):
        # Period boundaries match the 5-year NILU/EMEP bins in the source data exactly.
        # The source also has an earlier "1978-1982" bin, never selected here since
        # EXPECTED_YEARS starts at 1984.
        if y < 1988: return "1983-1987"
        elif y < 1992: return "1988-1992"
        elif y < 1997: return "1992-1996"
        elif y < 2002: return "1997-2001"
        elif y < 2007: return "2002-2006"
        elif y < 2012: return "2007-2011"
        else: return "2012-2016"

    value_2016 = None
    value_last = None
    collected_years = set()

    for year in sorted(EXPECTED_YEARS):
        comment = 'ok'
        collected_years.add(year)

        if year < 2017:
            period = period_for_year(year)
            tonn_val = period_map.get(period)
                
            base_value = float(tonn_val) / 1000
            data_sources = 'NILU and geodata.no'
            
            noise_val = dataset_noise[key_dep]
            value = base_value * noise_val
                
            if year == 2016:
                value_2016 = value
                
        elif year < 2022:
            # No new NILU period map exists yet for 2017-2021, so we keep the 2016
            # per-class distribution and scale it by the national trend reported for
            # observed (kriging-method) deposition since 2015 in Blake et al. (2023,
            # Table 3): NOx -10%, Nred/NHx -17%, giving factors 61440/68166 and
            # 61175/73494. The kriging method is used here rather than the newer
            # NILU model-assimilation totals for 2017-2021 because NILU themselves
            # advise using the kriging method specifically for trend assessment
            # (personal correspondence, 2026): it is the only method applied
            # consistently across all periods, whereas the assimilation methodology
            # for the two most recent periods differs somewhat between them.
            if poll == 'NOx':
                value = value_2016 * 61440 / 68166
            else:
                value = value_2016 * 61175 / 73494
            value_last = value
            data_sources = 'NILU and geodata.no'
            
        else:
            # Last year is extrapolated flat forward from value_last
            base_value = value_last
            data_sources = 'extrapolated'
            
            noise_val = dataset_noise[key_interp]
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


def _add_OP_N2_fixation_mc(results, preloaded_data, current_params, ammonia_import_dict, ammonia_export_dict, dataset_noise):
    flow_code = 'AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2'
    collected_years = set()
    
    dataset_key = 'Fertilizer by nutrient'
    data_sources = 'FAOSTAT Fertilizer by nutrient + SSB'

    # 'faostat_fertilizer_production' <- data_files/FAOSTAT_data_en_11-25-2025.csv:
    # FAOSTAT Fertilizer by nutrient, domestic production (downloaded 25.11.2025)
    df_faostat = preloaded_data['faostat_fertilizer_production']

    for _, row in df_faostat.iterrows():
        year = int(row['Year'])
        if year in ammonia_import_dict:  # Data finnes fra handelsstart (1988)
            if year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            
            base_faostat = float(row['Value']) / 1000  # tN -> ktN
            
            noise_val = dataset_noise[dataset_key]
            perturbed_faostat = base_faostat * noise_val
            
            # Mass balance proxy for domestic industrial N2 fixation via ammonia
            # synthesis: FAOSTAT-reported domestic fertilizer N production, minus
            # imported ammonia N (not fixed domestically), plus exported ammonia N
            # (fixed domestically but leaving before being counted as production).
            # Known to be a noisy proxy - see atmosphere_pool/flow_AT_AT_MP_OP_
            # Ammonia_synthesis_N2_fixation_N2.md.
            # Export presence is sporadic (SSB tab 08801 has no NH3 export row in 1991,
            # 2003, 2006, 2007 - no shipments that year, not missing data), so a missing
            # year defaults to 0 rather than requiring the key like import does.
            value = perturbed_faostat - ammonia_import_dict[year] + ammonia_export_dict.get(year, 0.0)
            
            comment = 'ok'

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': value, 
                'comment': comment,
                'data_sources': data_sources
            })
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)    
    

def _add_AG_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-AG.SM-Biological N2 fixation-N2'
    comment = 'ok'
    data_sources = 'Bleken & Bakken'
    collected_years = set()

    val_param = current_params.get("AG_biological_fixation_N2")
    value = float(val_param)

    for year in EXPECTED_YEARS:
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': comment,
            'data_sources': data_sources,
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_FO_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-FS.FO-N2 fixation-N2'
    comment = 'ok'
    data_sources = 'Moldan (2025) and SSB'
    collected_years = set()

    fixation_rate = float(current_params.get("FO_biological_fixation_N2"))
    forested_area = float(current_params.get("forested_area"))

    value = fixation_rate*forested_area

    for year in EXPECTED_YEARS:
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': comment,
            'data_sources': data_sources,
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_OL_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-FS.OL-N2 fixation-N2'
    comment = 'ok'
    data_sources = 'CORINE land cover inventory and REddy & DeLaune (2008)'
    collected_years = set()

    fixation_marshes = float(current_params.get("N2_fixation_freshwater_marshes"))
    fixation_peat = float(current_params.get("N2_fixation_peat_bog"))
    fixation_wetl = float(current_params.get("N2_fixation_coastal_wetlands"))
    marshes_area = float(current_params.get("inland_marshes_area"))
    peat_area = float(current_params.get("peat_bog_area"))
    intertidal_area = float(current_params.get("intertidal_flats_area"))

    value = (fixation_marshes*marshes_area + fixation_peat*peat_area + fixation_wetl*intertidal_area)*1e-6 # kg -> kt

    for year in EXPECTED_YEARS:
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': comment,
            'data_sources': data_sources,
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_SW_N2_fixation_mc(results, current_params):
    flow_code = 'AT.AT-HY.SW-N2 fixation-N2'
    comment = 'ok'
    data_sources = 'NIBIO and Reddy & DeLaune (2008)'
    collected_years = set()

    fixation_SW = float(current_params.get("N2_fixation_SW"))
    area_SW = float(current_params.get("surface_water_area"))

    value = fixation_SW*area_SW*1e-3 # tN -> ktN

    for year in EXPECTED_YEARS:
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': comment,
            'data_sources': data_sources,
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
        
        
def _add_atmospheric_outflow_mc(results, flow_code, value_col, df_atm, current_params, dataset_noise):
    """
    Shared implementation for atmospheric outflow (transboundary transport of N
    out of Norway), for both OXN (value_col=2, 'NOx out' in atm_in_out.xlsx) and
    RDN (value_col=4, 'NH3 out'). Source rows are in units of 100 t N (see the
    file header), so dividing by 10 converts to kt N.
    """
    collected_years = set()
    comment = 'ok'

    for r in range(5, 45):
        if r >= len(df_atm):
            break

        year_val = df_atm.iloc[r, 0]
        if pd.isna(year_val):
            continue

        year = int(year_val)
        collected_years.add(year)

        status_val = str(df_atm.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'

        base_value = float(df_atm.iloc[r, value_col]) / 10
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


if __name__ == "__main__":
    # Test call: will crash in a controlled way if data isn't routed in correctly
    calculations = execute_calculations_at({}, {}, {}, {})