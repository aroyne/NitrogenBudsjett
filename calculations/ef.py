#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 15:26:53 2025

@author: anja
"""

import pandas as pd

from calculations.n_params import NParameters
from calculations.shared_flow_calculations import (
    find_feedstock_fuel
    )
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    combine_uncertainties_percent,
    get_uncertainty,
    load_crltap_emissions_to_N,
    read_trade_data,
    find_trade_data
)

expected_years = EXPECTED_YEARS
trade_data = read_trade_data('data_files/Tab_08801_1988_2024.csv')


# CRLTAP sectors used in this pool (see Schäppi2025Ann / EMEP CRF codes)

CRLTAP_EC_SECTORS = [
    '1A1a', '1A1b', '1A1c',
    '1B1a', '1B1b', '1B1c',
    '1B2ai', '1B2aiv', '1B2av',
    '1B2b', '1B2', '1B2d',
]

CRLTAP_IC_SECTORS = [
    '1A2a', '1A2b', '1A2c', '1A2d',
    '1A2e', '1A2f', '1A2gvii', '1A2gviii',
]

CRLTAP_TR_SECTORS = [
    '1A3a(i)', '1A3aii(i)',
    '1A3bi', '1A3bii', '1A3biii', '1A3biv',
    '1A3bv', '1A3bvi', '1A3bvii',
    '1A3c',
    '1A3di(ii)', '1A3dii',
    '1A3ei', '1A3eii',
]

CRLTAP_OE_SECTORS = [
    '1A4a1', '1A4aii',
    '1A4bi', '1A4bii',
    '1A4ci', '1A4cii', '1A4ciii',
    '1A5a', '1A5b',
]

def execute_calculations():
    results = []
    params = NParameters("data_files/N_parameters.xlsx")
    dataset_unc = params.get_table('dataset_uncertainties').set_index('dataset_name')
    
    # initializing values for mass balance
    years = sorted(expected_years)
    EC_out = pd.DataFrame({
        'year': years,
        'value': 0.0,               # float zeros; use 0 if you want ints
        'entries': 0    # need to count the right number of entries that year if comment to be 'ok'
    })
    EC_out.set_index('year', inplace=True)
    IC_in = pd.DataFrame({
        'year': years,
        'value': 0.0,               # float zeros; use 0 if you want ints
        'entries': 0    # need to count the right number of entries that year if comment to be 'ok'
    })
    IC_in.set_index('year', inplace=True)
    IC_out = pd.DataFrame({
        'year': years,
        'value': 0.0,               # float zeros; use 0 if you want ints
        'entries': 0    # need to count the right number of entries that year if comment to be 'ok'
    })
    IC_out.set_index('year', inplace=True)
    
    _add_fuel_for_industry(results, IC_in, dataset_unc)
    _add_fuel_for_transport(results, dataset_unc)
    _add_fuel_for_heating(results, dataset_unc)
    _add_fuel_used_as_feedstock(results, params, EC_out, dataset_unc)
    _add_ec_NOx_emissions(results, params, dataset_unc)
    _add_ec_N2O_emissions(results, dataset_unc)
    _add_fuel_export(results, EC_out, dataset_unc, trade_data)
    _add_ic_NH3_emissions(results, params, IC_out, dataset_unc)
    _add_ic_NOx_emissions(results, params, IC_out, dataset_unc)
    _add_ic_N2O_emissions(results, IC_out, dataset_unc)
    # _add_ic_N2_emissions(results, IC_in, IC_out)
    _add_tr_NH3_emissions(results, params, dataset_unc)
    _add_tr_NOx_emissions(results, params, dataset_unc)
    _add_tr_N2O_emissions(results, dataset_unc)
    _add_export_of_transport_fuels(results, dataset_unc)
    _add_oe_NH3_emissions(results, params, dataset_unc)
    _add_oe_NOx_emissions(results, params, dataset_unc)
    _add_oe_N2O_emissions(results, dataset_unc)

    

    return results  # list of flow records

def _add_fuel_for_industry(results, IC_in, dataset_unc):
    flow_code = 'EF.EC-EF.IC-Fuel for industry-Nmix'
    collected_years = set()
    # UNFCCC, common reporting Norway https://unfccc.int/documents/644485
    # Table 1
    data_sources = 'UNFCCC CRT'
    comment = 'ok'
    data = pd.read_csv('data_files/N_fuel_for_industry.csv')
    data = data[['year', 'value']]
    u_dataset_fuel = get_uncertainty(dataset_unc, 'UNFCCC_fuel')
    for index, row in data.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        value = row['value']
        IC_in.loc[year,'value'] += value
        IC_in.loc[year,'entries'] += 1
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': u_dataset_fuel
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)
        
def _add_fuel_for_transport(results, dataset_unc):
    flow_code = 'EF.EC-EF.TR-Fuel for transport-Nmix'
    collected_years = set()
    # UNFCCC, common reporting Norway https://unfccc.int/documents/644485
    # Table 1
    data_sources = 'UNFCCC CRT'
    comment = 'ok'
    data = pd.read_csv('data_files/N_fuel_for_transport.csv')
    data = data[['year', 'value']]
    u_dataset_fuel = get_uncertainty(dataset_unc, 'UNFCCC_fuel')
    for index, row in data.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        value = row['value']
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': u_dataset_fuel
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)

def _add_fuel_for_heating(results, dataset_unc):
    flow_code = 'EF.EC-EF.OE-Fuel for heating-Nmix'
    collected_years = set()
    # UNFCCC, common reporting Norway https://unfccc.int/documents/644485
    # Table 1
    data_sources = 'UNFCCC CRT'
    comment = 'ok'
    data = pd.read_csv('data_files/N_fuel_for_heating.csv')
    data = data[['year', 'value']]
    u_dataset_fuel = get_uncertainty(dataset_unc, 'UNFCCC_fuel')
    for index, row in data.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        value = row['value']
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': u_dataset_fuel
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_fuel_used_as_feedstock(results, params, EC_out, dataset_unc):
    flow_code = 'EF.EC-MP.OP-Fuel used as feedstock-Nmix' 
    collected_years = set()
    # use data from SSB
    data_sources = 'SSB table 11561'
    comment = 'ok'
    year_values, uncertainty = find_feedstock_fuel(params, dataset_unc)
    for year, value in year_values.items():
        year = int(year)
        collected_years.add(year)
        EC_out.loc[year,'value'] += value
        EC_out.loc[year,'entries'] += 1
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value,
            'comment': comment,
            'data_sources': data_sources,        
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)
    
# def _add_ec_NH3_emissions(results, params, dataset_unc):
#     flow_code = 'EF.EC-AT.AT-Emissions-NH3'
#     collected_years = set()
#     comment = 'ok'
#     # use data from CRLTAP
#     data_sources = 'CRLTAP Inventory Submissions'
#     u_dataset_crltap = get_uncertainty(dataset_unc, 'CRLTAP')
#     conv, u_conv = params.get_global_param_with_uncertainty("NH3_to_N_factor")    
#     uncertainty = combine_uncertainties_percent(u_dataset_crltap, u_conv)
#     sums = load_crltap_emissions_to_N(
#         filename='data_files/webdabData1863365.txt',
#         categories=CRLTAP_EC_SECTORS,
#         pollutant='NH3',
#         conv_to_N=conv,
#     )   
#     for year, val in sums.items():
#         collected_years.add(int(year))
#         results.append({
#             'flow_name': flow_code,
#             'year': int(year),
#             'value': float(val),
#             'comment': comment,
#             'data_sources': data_sources,
#             'uncertainty': uncertainty
#         })
#     missing_years = expected_years - collected_years
#     report_missing_years(flow_code, missing_years, results)
    
def _add_ec_NOx_emissions(results, params, dataset_unc):
    flow_code = 'EF.EC-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok'
    # use data from CRLTAP
    u_dataset_crltap = get_uncertainty(dataset_unc, 'CRLTAP')
    conv, u_conv = params.get_global_param_with_uncertainty("NOx_to_N_factor")
    uncertainty = combine_uncertainties_percent(u_dataset_crltap, u_conv)
    data_sources = 'CRLTAP Inventory Submissions'
    sums = load_crltap_emissions_to_N(
        filename='data_files/webdabData1863365.txt',
        categories=CRLTAP_EC_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
    )    
    for year, val in sums.items():
        collected_years.add(int(year))
        results.append({
            'flow_name': flow_code,
            'year': int(year),
            'value': float(val),
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)
    
def _add_ec_N2O_emissions(results, dataset_unc):
    flow_code = 'EF.EC-AT.AT-Emissions-N2O'
    collected_years = set()
    # UNFCCC, common reporting Norway https://unfccc.int/documents/644485
    # Table 1
    data_sources = 'UNFCCC CRT'
    comment = 'ok'
    uncertainty = get_uncertainty(dataset_unc, 'UNFCCC_emissions')
    data = pd.read_csv('data_files/N2O_EC.csv')
    data = data[['year', 'value_EC']]
    for index, row in data.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        value = row['value_EC']
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)

        
def _add_fuel_export(results, EC_out, dataset_unc, trade_data):
    flow_code = 'EF.EC-RW.RW-Fuel export-Nmix'
    collected_years = set()
    comment = 'ok'
    uncertainty = get_uncertainty(dataset_unc, '08801')
    data_sources = 'SSB tab 08801'
    # using trade data from SSB
    u_08801 = float(dataset_unc.loc['08801', 'uncertainty'])
    uncertainty = u_08801
    comment = 'ok'
    data_sources = 'SSB tab 08801'
    # HS-koder for energivarer starter på 27. 
    # Importing N-contents for HS codes
    hs_N_content = pd.read_excel('data_files/N_content_fuels.xlsx')
    # only the ones not labeled T under "transport?"
    hs_N_content = hs_N_content[hs_N_content['transport?'].isna()]
    hs_N_content['N-content'] *= 1e-2 # from weight % to frac
    impeks = 2 # 1 for import, 2 for export
    aggregated_data = find_trade_data(trade_data, hs_N_content, impeks)
    for year in expected_years:
        if aggregated_data['year'].isin([year]).any():
            collected_years.add(year)
            n_amount_row = aggregated_data[aggregated_data['year'] == year]
            value = n_amount_row['N_amount'].values[0]
            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': value, 
                'comment': comment,
                'data_sources': data_sources,
                'uncertainty': uncertainty
            })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)

    
def _add_ic_NH3_emissions(results, params, IC_out, dataset_unc):
    flow_code = 'EF.IC-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok'
    data_sources = 'CRLTAP Inventory Submissions'
    # use data from CRLTAP
    u_dataset_crltap = get_uncertainty(dataset_unc, 'CRLTAP')
    conv, u_conv = params.get_global_param_with_uncertainty("NH3_to_N_factor")
    uncertainty = combine_uncertainties_percent(u_dataset_crltap, u_conv)
    sums = load_crltap_emissions_to_N(
        filename='data_files/webdabData1863365.txt',
        categories=CRLTAP_IC_SECTORS,
        pollutant='NH3',
        conv_to_N=conv,
    )    
    for year, val in sums.items():
        collected_years.add(int(year))
        IC_out.loc[year,'value'] += val
        IC_out.loc[year,'entries'] += 1
        results.append({
            'flow_name': flow_code,
            'year': int(year),
            'value': float(val),
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)

def _add_ic_NOx_emissions(results, params, IC_out, dataset_unc):
    flow_code = 'EF.IC-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok'
    # use data from CRLTAP
    u_dataset_crltap = get_uncertainty(dataset_unc, 'CRLTAP')
    conv, u_conv = params.get_global_param_with_uncertainty("NOx_to_N_factor")
    uncertainty = combine_uncertainties_percent(u_dataset_crltap, u_conv)
    data_sources = 'CRLTAP Inventory Submissions'
    sums = load_crltap_emissions_to_N(
        filename='data_files/webdabData1863365.txt',
        categories=CRLTAP_IC_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
    )    
    for year, val in sums.items():
        collected_years.add(int(year))
        IC_out.loc[year,'value'] += val
        IC_out.loc[year,'entries'] += 1
        results.append({
            'flow_name': flow_code,
            'year': int(year),
            'value': float(val),
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_ic_N2O_emissions(results, IC_out, dataset_unc):
    flow_code = 'EF.IC-AT.AT-Emissions-N2O'
    collected_years = set()
    # UNFCCC, common reporting Norway https://unfccc.int/documents/644485
    # Table 1
    data_sources = 'UNFCCC CRT'
    uncertainty = get_uncertainty(dataset_unc, 'UNFCCC_emissions')
    comment = 'ok'
    data = pd.read_csv('data_files/N2O_EC.csv')
    data = data[['year', 'value_IC']]
    for index, row in data.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        value = row['value_IC']
        IC_out.loc[year,'value'] += value
        IC_out.loc[year,'entries'] += 1
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)


# def _add_ic_N2_emissions(results, IC_in, IC_out):
#     flow_code = 'EF.IC-AT.AT-Emissions-N2'
#     # include flows from MP, AG, FS and PR
#     collected_years = set()
#     comment = 'ok'
#     data_sources = 'mass balance'
#     uncertainty = 30
#     for year in expected_years:
#         collected_years.add(year)
#         if IC_in.loc[year,'entries'] == 1 and IC_out.loc[year,'entries'] == 3:
#             final_value = IC_in.loc[year,'value'] - IC_out.loc[year,'value']
#             comment = 'ok'
#             data_sources = 'mass balance'
#         else:
#             final_value = 0
#             comment = 'not done'
#             data_sources = 'entries missing for mass balance'            
#         results.append({
#             'flow_name': flow_code,
#             'year': year,
#             'value': final_value,  
#             'comment': comment,
#             'data_sources': data_sources,
#             'uncertainty': uncertainty
#         })
#     missing_years = expected_years - collected_years
#     report_missing_years(flow_code, missing_years, results)


def _add_tr_NH3_emissions(results, params, dataset_unc):
    flow_code = 'EF.TR-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok'
    # use data from CRLTAP
    data_sources = 'CRLTAP Inventory Submissions'
    u_dataset_crltap = get_uncertainty(dataset_unc, 'CRLTAP')
    conv, u_conv = params.get_global_param_with_uncertainty("NH3_to_N_factor")
    uncertainty = combine_uncertainties_percent(u_dataset_crltap, u_conv)
    sums = load_crltap_emissions_to_N(
        filename='data_files/webdabData1863365.txt',
        categories=CRLTAP_TR_SECTORS,
        pollutant='NH3',
        conv_to_N=conv,
    )    
    for year, val in sums.items():
        collected_years.add(int(year))
        results.append({
            'flow_name': flow_code,
            'year': int(year),
            'value': float(val),
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_tr_NOx_emissions(results, params, dataset_unc):
    flow_code = 'EF.TR-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok'
    # use data from CRLTAP
    data_sources = 'CRLTAP Inventory Submissions'
    u_dataset_crltap = get_uncertainty(dataset_unc, 'CRLTAP')
    conv, u_conv = params.get_global_param_with_uncertainty("NOx_to_N_factor")
    uncertainty = combine_uncertainties_percent(u_dataset_crltap, u_conv)
    sums = load_crltap_emissions_to_N(
        filename='data_files/webdabData1863365.txt',
        categories=CRLTAP_TR_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
    )    
    for year, val in sums.items():
        collected_years.add(int(year))
        results.append({
            'flow_name': flow_code,
            'year': int(year),
            'value': float(val),
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)

    
def _add_tr_N2O_emissions(results, dataset_unc):
    flow_code = 'EF.TR-AT.AT-Emissions-N2O'
    collected_years = set()
    # UNFCCC, common reporting Norway https://unfccc.int/documents/644485
    # Table 1
    data_sources = 'UNFCCC CRT'
    uncertainty = get_uncertainty(dataset_unc, 'UNFCCC_emissions')
    comment = 'ok'
    data = pd.read_csv('data_files/N2O_EC.csv')
    data = data[['year', 'value_TR']]
    for index, row in data.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        value = row['value_TR']
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_export_of_transport_fuels(results, dataset_unc):
    flow_code = 'EF.TR-RW.RW-Export of transport fuels-Nmix'
    collected_years = set()
    comment = 'ok'
    uncertainty = get_uncertainty(dataset_unc, '08801')
    data_sources = 'SSB tab 08801'
    # Transport fuel exports only (transport_flag='T'), N in kt per year
    # HS-koder for energivarer starter på 27. 
    # Importing N-contents for HS codes
    hs_N_content = pd.read_excel('data_files/N_content_fuels.xlsx')
    # only the ones not labeled T under "transport?"
    hs_N_content = hs_N_content[hs_N_content['transport?'] == 'T']
    hs_N_content['N-content'] *= 1e-2 # from weight % to frac
    impeks = 2 # 1 for import, 2 for export
    aggregated_data = find_trade_data(trade_data, hs_N_content, impeks)
    for year in expected_years:
        if aggregated_data['year'].isin([year]).any():
            collected_years.add(year)
            n_amount_row = aggregated_data[aggregated_data['year'] == year]
            value = n_amount_row['N_amount'].values[0]
            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': value, 
                'comment': comment,
                'data_sources': data_sources,
                'uncertainty': uncertainty
            })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_oe_NH3_emissions(results, params, dataset_unc):
    flow_code = 'EF.OE-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok'
    # use data from CRLTAP
    data_sources = 'CRLTAP Inventory Submissions'
    u_dataset_crltap = get_uncertainty(dataset_unc, 'CRLTAP')
    conv, u_conv = params.get_global_param_with_uncertainty("NH3_to_N_factor")
    uncertainty = combine_uncertainties_percent(u_dataset_crltap, u_conv)
    sums = load_crltap_emissions_to_N(
        filename='data_files/webdabData1863365.txt',
        categories=CRLTAP_OE_SECTORS,
        pollutant='NH3',
        conv_to_N=conv,
    )    
    for year, val in sums.items():
        collected_years.add(int(year))
        results.append({
            'flow_name': flow_code,
            'year': int(year),
            'value': float(val),
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_oe_NOx_emissions(results, params, dataset_unc):
    flow_code = 'EF.OE-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok'
    # use data from CRLTAP
    data_sources = 'CRLTAP Inventory Submissions'
    u_dataset_crltap = get_uncertainty(dataset_unc, 'CRLTAP')
    conv, u_conv = params.get_global_param_with_uncertainty("NOx_to_N_factor")
    uncertainty = combine_uncertainties_percent(u_dataset_crltap, u_conv)
    sums = load_crltap_emissions_to_N(
        filename='data_files/webdabData1863365.txt',
        categories=CRLTAP_OE_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
    )    
    for year, val in sums.items():
        collected_years.add(int(year))
        results.append({
            'flow_name': flow_code,
            'year': int(year),
            'value': float(val),
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)

    
def _add_oe_N2O_emissions(results, dataset_unc):
    flow_code = 'EF.OE-AT.AT-Emissions-N2O'
    collected_years = set()
    # UNFCCC, common reporting Norway https://unfccc.int/documents/644485
    # Table 1
    data_sources = 'UNFCCC CRT'
    uncertainty = get_uncertainty(dataset_unc, 'UNFCCC_emissions')
    comment = 'ok'
    data = pd.read_csv('data_files/N2O_EC.csv')
    data = data[['year', 'value_OE']]
    for index, row in data.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        value = row['value_OE']
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources,
            'uncertainty': uncertainty
        })
    missing_years = expected_years - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    




if __name__ == "__main__":
    calculations = execute_calculations()
    for calc in calculations:
        print(calc)
