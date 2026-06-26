#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    load_crltap_emissions_to_N,
    process_generic_trade_flow
)
from calculations.shared_flow_calculations import find_feedstock_fuel

# Sector-konstanter bevares for CRLTAP-funksjonene
CRLTAP_EC_SECTORS = ['1A1a', '1A1b', '1A1c', '1B1a', '1B1b', '1B1c', '1B2ai', '1B2aiv', '1B2av', '1B2b', '1B2', '1B2d']
CRLTAP_IC_SECTORS = ['1A2a', '1A2b', '1A2c', '1A2d', '1A2e', '1A2f', '1A2gvii', '1A2gviii']
CRLTAP_TR_SECTORS = ['1A3a(i)', '1A3aii(i)', '1A3bi', '1A3bii', '1A3biii', '1A3biv', '1A3bv', '1A3bvi', '1A3bvii', '1A3c', '1A3di(ii)', '1A3dii', '1A3ei', '1A3eii']
CRLTAP_OE_SECTORS = ['1A4a1', '1A4aii', '1A4bi', '1A4bii', '1A4ci', '1A4cii', '1A4ciii', '1A5a', '1A5b']


def execute_calculations_ef(preloaded_data, current_params, dataset_noise, current_trade_factors):
    results = []
    
    _add_fuel_for_industry_mc(results, preloaded_data, dataset_noise)
    _add_fuel_for_transport_mc(results, preloaded_data, dataset_noise)
    _add_fuel_for_heating_mc(results, preloaded_data, dataset_noise)
    _add_fuel_used_as_feedstock_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ec_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ec_N2O_emissions_mc(results, preloaded_data, dataset_noise)
    _add_fuel_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_ic_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ic_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_ic_N2O_emissions_mc(results, preloaded_data, dataset_noise)
    _add_tr_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_tr_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_tr_N2O_emissions_mc(results, preloaded_data, dataset_noise)
    _add_export_of_transport_fuels_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_oe_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_oe_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_oe_N2O_emissions_mc(results, preloaded_data, dataset_noise)

    return results


def _add_fuel_for_industry_mc(results, preloaded_data, dataset_noise):
    flow_code = 'EF.EC-EF.IC-Fuel for industry-Nmix'
    collected_years = set()
    dataset_key = 'UNFCCC_fuel'
    
    df = preloaded_data.get('fuel_for_industry')

    for _, row in df.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        raw_val = float(row['value'])
        noise_val = dataset_noise[dataset_key]
        value = raw_val * noise_val

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_fuel_for_transport_mc(results, preloaded_data, dataset_noise):
    flow_code = 'EF.EC-EF.TR-Fuel for transport-Nmix'
    collected_years = set()
    dataset_key = 'UNFCCC_fuel'
    
    df = preloaded_data.get('fuel_for_transport')

    for _, row in df.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        raw_val = float(row['value'])
        noise_val = dataset_noise[dataset_key]
        value = raw_val * noise_val
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_fuel_for_heating_mc(results, preloaded_data, dataset_noise):
    flow_code = 'EF.EC-EF.OE-Fuel for heating-Nmix'
    collected_years = set()
    dataset_key = 'UNFCCC_fuel'
    
    df = preloaded_data.get('fuel_for_heating')

    for _, row in df.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        raw_val = float(row['value'])
        noise_val = dataset_noise[dataset_key]
        value = raw_val * noise_val
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_fuel_used_as_feedstock_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'EF.EC-MP.OP-Fuel used as feedstock-Nmix'
    collected_years = set()
    
    year_values = find_feedstock_fuel(preloaded_data, current_params, dataset_noise)
    
    for year, value in year_values.items():
        year = int(year)
        collected_years.add(year)
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på via parametere)', 'data_sources': 'SSB table 11561'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_ec_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'EF.EC-AT.AT-Emissions-NOx'
    collected_years = set()
    dataset_key = 'CRLTAP'
    
    conv = float(current_params.get("NOx_to_N_factor"))
    crltap_data = preloaded_data.get('ag_crltap_raw_lines')        
    sums = load_crltap_emissions_to_N(
        crltap_data, 
        CRLTAP_EC_SECTORS, 
        'NOx', 
        conv, 
        dataset_noise
    )
    noise_val = dataset_noise[dataset_key]
    
    for year, val in sums.items():
        year = int(year)
        collected_years.add(year)
        value = float(val) * noise_val
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'CRLTAP Inventory Submissions'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_ec_N2O_emissions_mc(results, preloaded_data, dataset_noise):
    flow_code = 'EF.EC-AT.AT-Emissions-N2O'
    collected_years = set()
    dataset_key = 'UNFCCC_emissions'
    
    df = preloaded_data.get('n2o_ec_data')
    noise_val = dataset_noise[dataset_key]

    for _, row in df.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        raw_val = float(row['value_EC'])        
        value = raw_val * noise_val
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_fuel_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    flow_code = 'EF.EC-RW.RW-Fuel export-Nmix'
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code=flow_code,
        target_types='fuel',
        is_import=False,
        dataset_noise=dataset_noise
    )
    

def _add_ic_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'EF.IC-AT.AT-Emissions-NH3'
    collected_years = set()    
    conv = float(current_params.get("NH3_to_N_factor"))
    crltap_data = preloaded_data.get('ag_crltap_raw_lines')        
    sums = load_crltap_emissions_to_N(
        crltap_data, 
        CRLTAP_IC_SECTORS, 
        'NH3', 
        conv, 
        dataset_noise
    )
    
    for year, value in sums.items():
        year = int(year)
        collected_years.add(year)
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'CRLTAP Inventory Submissions'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_ic_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'EF.IC-AT.AT-Emissions-NOx'
    collected_years = set()
    
    conv = float(current_params.get("NOx_to_N_factor"))
    crltap_data = preloaded_data.get('ag_crltap_raw_lines')
        
    sums = load_crltap_emissions_to_N(
        crltap_data, 
        CRLTAP_IC_SECTORS, 
        'NOx', 
        conv, 
        dataset_noise
    )
    
    for year, value in sums.items():
        year = int(year)
        collected_years.add(year)
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'CRLTAP Inventory Submissions'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_ic_N2O_emissions_mc(results, preloaded_data, dataset_noise):
    flow_code = 'EF.IC-AT.AT-Emissions-N2O'
    collected_years = set()
    dataset_key = 'UNFCCC_emissions'
    
    df = preloaded_data.get('n2o_ec_data')
    noise_val = dataset_noise[dataset_key]
    for _, row in df.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        raw_val = float(row['value_IC'])
        value = raw_val * noise_val
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_tr_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'EF.TR-AT.AT-Emissions-NH3'
    collected_years = set()
    
    conv = float(current_params.get("NH3_to_N_factor"))
    crltap_data = preloaded_data.get('ag_crltap_raw_lines')
        
    sums = load_crltap_emissions_to_N(
        crltap_data, 
        CRLTAP_TR_SECTORS, 
        'NH3', 
        conv, 
        dataset_noise
    )
    
    for year, value in sums.items():
        year = int(year)
        collected_years.add(year)
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'CRLTAP Inventory Submissions'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_tr_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'EF.TR-AT.AT-Emissions-NOx'
    collected_years = set()
    
    conv = float(current_params.get("NOx_to_N_factor"))
    crltap_data = preloaded_data.get('ag_crltap_raw_lines')
        
    sums = load_crltap_emissions_to_N(
        crltap_data, 
        CRLTAP_TR_SECTORS, 
        'NOx', 
        conv, 
        dataset_noise
    )
    
    for year, value in sums.items():
        year = int(year)
        collected_years.add(year)
        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'CRLTAP Inventory Submissions'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_tr_N2O_emissions_mc(results, preloaded_data, dataset_noise):
    flow_code = 'EF.TR-AT.AT-Emissions-N2O'
    collected_years = set()
    dataset_key = 'UNFCCC_emissions'
    
    df = preloaded_data.get('n2o_ec_data')    
    noise_val = dataset_noise[dataset_key]

    for _, row in df.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        raw_val = float(row['value_TR'])
        value = raw_val*noise_val
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_export_of_transport_fuels_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    flow_code = 'EF.EC-RW.RW-Export of transport fuels-Nmix'
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code=flow_code,
        target_types='transport_fuel',
        is_import=False,
        dataset_noise=dataset_noise
    )
    

def _add_oe_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'EF.OE-AT.AT-Emissions-NH3'
    collected_years = set()
    
    conv = float(current_params.get("NH3_to_N_factor"))
    crltap_data = preloaded_data.get('ag_crltap_raw_lines')
    sums = load_crltap_emissions_to_N(
        crltap_data, 
        CRLTAP_OE_SECTORS, 
        'NH3', 
        conv, 
        dataset_noise
    )
    
    for year, value in sums.items():
        year = int(year)
        collected_years.add(year)        
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'CRLTAP Inventory Submissions'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_oe_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'EF.OE-AT.AT-Emissions-NOx'
    collected_years = set()
    
    conv = float(current_params.get("NOx_to_N_factor"))
    crltap_data = preloaded_data.get('ag_crltap_raw_lines')
    sums = load_crltap_emissions_to_N(
        crltap_data, 
        CRLTAP_OE_SECTORS, 
        'NOx', 
        conv, 
        dataset_noise
    )
    
    for year, value in sums.items():
        year = int(year)
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'CRLTAP Inventory Submissions'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_oe_N2O_emissions_mc(results, preloaded_data, dataset_noise):
    flow_code = 'EF.OE-AT.AT-Emissions-N2O'
    collected_years = set()
    dataset_key = 'UNFCCC_emissions'
    
    df = preloaded_data.get('n2o_ec_data')
    noise_val = dataset_noise[dataset_key]
    for _, row in df.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        raw_val = float(row['value_OE'])
        value = raw_val * noise_val
        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok (MC-støy lagt på)', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)