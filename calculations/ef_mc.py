#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Energy and Fuels (EF) pool: N in fuel combusted by each EF subsector (EC/IC/TR/OE),
their NH3/NOx/N2O combustion emissions to the atmosphere, fuel used as feedstock
(not combusted), and fuel/transport-fuel export.

EF subsectors follow the CRLTAP/IPCC 1A energy-sector categories:
- EC = "Energy Combustion" (energy industries, IPCC 1A1 + fugitive 1B)
- IC = "Industrial Combustion" (manufacturing industries and construction, 1A2)
- TR = Transport (1A3)
- OE = "Other Energy" (other sectors, 1A4-1A5: commercial/residential/agriculture)
"""
from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    load_crltap_emissions_to_N,
    process_generic_trade_flow
)
from calculations.shared_flow_calculations import find_feedstock_fuel

# CRLTAP category codes per EF subsector, used to select which rows of the
# CRLTAP inventory (webdabData1863365.txt, loaded as 'ag_crltap_raw_lines') to
# sum for each subsector's NH3/NOx emissions.
CRLTAP_EC_SECTORS = ['1A1a', '1A1b', '1A1c', '1B1a', '1B1b', '1B1c', '1B2ai', '1B2aiv', '1B2av', '1B2b', '1B2c', '1B2d']
CRLTAP_IC_SECTORS = ['1A2a', '1A2b', '1A2c', '1A2d', '1A2e', '1A2f', '1A2gvii', '1A2gviii']
CRLTAP_TR_SECTORS = ['1A3ai(i)', '1A3aii(i)', '1A3bi', '1A3bii', '1A3biii', '1A3biv', '1A3bv', '1A3bvi', '1A3bvii', '1A3c', '1A3di(ii)', '1A3dii', '1A3ei', '1A3eii']
CRLTAP_OE_SECTORS = ['1A4ai', '1A4aii', '1A4bi', '1A4bii', '1A4ci', '1A4cii', '1A4ciii', '1A5a', '1A5b']


def execute_calculations_ef(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    Main function for the EF (energy and fuels) pool. Runs all sub-calculations:
    N in combusted fuel per subsector, fuel used as feedstock, fuel/transport-fuel
    export, and NH3/NOx/N2O combustion emissions per subsector.
    """
    results = []

    _add_fuel_for_ec_subsector_mc(results, preloaded_data, dataset_noise, 'EF.EC-EF.IC-Fuel for industry-Nmix', 'fuel_for_industry')
    _add_fuel_for_ec_subsector_mc(results, preloaded_data, dataset_noise, 'EF.EC-EF.TR-Fuel for transport-Nmix', 'fuel_for_transport')
    _add_fuel_for_ec_subsector_mc(results, preloaded_data, dataset_noise, 'EF.EC-EF.OE-Fuel for heating-Nmix', 'fuel_for_heating')
    _add_fuel_used_as_feedstock_mc(results, preloaded_data, current_params, dataset_noise)

    # EC has no NH3 variant: no NH3 combustion emissions are modeled for energy
    # industries (see energy_and_fuels_pool/flow_EF_EC_AT_AT_Emissions_*.md - only
    # NOx and N2O flows exist for EC). This is intentional, not a missing function.
    _add_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'EF.EC-AT.AT-Emissions-NOx', CRLTAP_EC_SECTORS, 'NOx')
    _add_n2o_emissions_mc(results, preloaded_data, dataset_noise, 'EF.EC-AT.AT-Emissions-N2O', 'value_EC')
    _add_fuel_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)

    _add_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'EF.IC-AT.AT-Emissions-NH3', CRLTAP_IC_SECTORS, 'NH3')
    _add_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'EF.IC-AT.AT-Emissions-NOx', CRLTAP_IC_SECTORS, 'NOx')
    _add_n2o_emissions_mc(results, preloaded_data, dataset_noise, 'EF.IC-AT.AT-Emissions-N2O', 'value_IC')

    _add_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'EF.TR-AT.AT-Emissions-NH3', CRLTAP_TR_SECTORS, 'NH3')
    _add_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'EF.TR-AT.AT-Emissions-NOx', CRLTAP_TR_SECTORS, 'NOx')
    _add_n2o_emissions_mc(results, preloaded_data, dataset_noise, 'EF.TR-AT.AT-Emissions-N2O', 'value_TR', dataset_key='UNFCCC_N2O_transport')
    _add_export_of_transport_fuels_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)

    _add_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'EF.OE-AT.AT-Emissions-NH3', CRLTAP_OE_SECTORS, 'NH3')
    _add_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, 'EF.OE-AT.AT-Emissions-NOx', CRLTAP_OE_SECTORS, 'NOx')
    _add_n2o_emissions_mc(results, preloaded_data, dataset_noise, 'EF.OE-AT.AT-Emissions-N2O', 'value_OE')

    return results


def _add_fuel_for_ec_subsector_mc(results, preloaded_data, dataset_noise, flow_code, preload_key):
    """
    Shared implementation for N in fuel combusted by an EF.EC subsector (industry,
    transport, heating). preload_key selects the source compilation:
    'fuel_for_industry' <- data_files/N_fuel_for_industry.csv
    'fuel_for_transport' <- data_files/N_fuel_for_transport.csv
    'fuel_for_heating' <- data_files/N_fuel_for_heating.csv
    All three are compiled from UNFCCC CRT (Common Reporting Tables) fuel
    consumption in TJ, converted to N via IPCC (2006) NCVs and Schäppi (2025)
    Annexes Table 15 N contents (see DATA_SOURCES.txt).
    """
    collected_years = set()
    dataset_key = 'UNFCCC_fuel'

    df = preloaded_data.get(preload_key)

    for _, row in df.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        raw_val = float(row['value'])
        noise_val = dataset_noise[dataset_key]
        value = raw_val * noise_val

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_fuel_used_as_feedstock_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'EF.EC-MP.OP-Fuel used as feedstock-Nmix'
    collected_years = set()

    # find_feedstock_fuel (shared_flow_calculations.py) reads
    # preloaded_data['ssb_energy_balance_11561'] <- data_files/11561_20251113-154607.xlsx
    year_values = find_feedstock_fuel(preloaded_data, current_params, dataset_noise)

    for year, value in year_values.items():
        year = int(year)
        collected_years.add(year)

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': 'SSB table 11561'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_crltap_emissions_mc(results, preloaded_data, current_params, dataset_noise, flow_code, sectors, pollutant):
    """
    Shared implementation for CRLTAP-derived NH3/NOx combustion emissions of an EF
    subsector. `sectors` is one of the CRLTAP_{EC,IC,TR,OE}_SECTORS lists above;
    `pollutant` is 'NH3' or 'NOx'. Reads preloaded_data['ag_crltap_raw_lines'] <-
    data_files/webdabData1863365.txt (CRLTAP Inventory Submissions).
    """
    collected_years = set()

    conv = float(current_params.get(f"{pollutant}_to_N_factor"))
    crltap_data = preloaded_data.get('ag_crltap_raw_lines')
    sums = load_crltap_emissions_to_N(
        crltap_data,
        sectors,
        pollutant,
        conv,
        dataset_noise
    )

    for year, value in sums.items():
        year = int(year)
        collected_years.add(year)

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': 'CRLTAP Inventory Submissions'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_n2o_emissions_mc(results, preloaded_data, dataset_noise, flow_code, value_col, dataset_key='UNFCCC_N2O_energy'):
    """
    Shared implementation for combustion N2O emissions of an EF subsector. All four
    subsectors are split columns of the same compilation:
    preloaded_data['n2o_ec_data'] <- data_files/N2O_EC.csv (N2O emissions from
    combustion, split by EC/IC/TR/OE, UNFCCC CRT). value_col is 'value_EC',
    'value_IC', 'value_TR' or 'value_OE'. dataset_key defaults to the stationary-
    combustion uncertainty (Norway NID Annexes 2025, Annex 2: N2O EF for 1A1/1A2/1A4/1A5
    and 1B2C = "Fac3"); the EF.TR caller overrides this with 'UNFCCC_N2O_transport'
    since Annex 2 gives transport its own, much smaller uncertainty (25-65%, not Fac3).
    """
    collected_years = set()

    df = preloaded_data.get('n2o_ec_data')
    noise_val = dataset_noise[dataset_key]

    for _, row in df.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        raw_val = float(row[value_col])
        value = raw_val * noise_val

        results.append({
            'flow_name': flow_code, 'year': year, 'value': value,
            'comment': 'ok', 'data_sources': 'UNFCCC CRT'
        })
    report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)


def _add_fuel_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    flow_code = 'EF.EC-RW.RW-Fuel export-Nmix'
    # process_generic_trade_flow reads preloaded_data['compressed_trade_volume'],
    # built in data_loader.py from data_files/Tab_08801_1988_2024.csv (SSB table
    # 08801, full Norwegian import/export statistics by HS commodity code).
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


def _add_export_of_transport_fuels_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    flow_code = 'EF.TR-RW.RW-Export of transport fuels-Nmix'
    # process_generic_trade_flow reads preloaded_data['compressed_trade_volume'],
    # built in data_loader.py from data_files/Tab_08801_1988_2024.csv (SSB table
    # 08801, full Norwegian import/export statistics by HS commodity code).
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