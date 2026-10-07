#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hydrosphere (HY) pool: N flows between surface water, coastal water and
aquaculture - coastal inflow, wild catch and shellfish/macroalgae harvest,
freshwater retention/denitrification, and aquaculture's internal N budget
(harvest, feed waste, excretion).
"""
import pandas as pd

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    add_flat_carryforward_year
)
from calculations.shared_flow_calculations import (
    find_aquaculture_production,
    find_recovered_lost_fish_N,
    find_treated_wastewater_discharge,
    find_teotil2_bias_corrected,
    get_aquafeed_budget,
    teotil3_table
)

def execute_calculations_hy(preloaded_data, current_params, dataset_noise):
    results = []
    
    years_sorted = sorted(list(EXPECTED_YEARS))
    outflow_tracker = pd.DataFrame({'value': 0.0, 'entries': 0}, index=years_sorted)
            
    # 'aqua_modern'/'aqua_old' <- A.06.002_20251111-140559.xlsx (1994 onward)
    # and akvakultur_1984_1994.xlsx (data_loader.py DATA_MAP, 'excel_aquaculture'
    # method): Fiskeridirektoratet aquaculture sales of salmon/trout by county,
    # species and year, extended backward with a historical compilation
    aqua_production_dict = find_aquaculture_production(
        preloaded_data.get('aqua_modern'),
        preloaded_data.get('aqua_old'),
        current_params,
        dataset_noise
    )
    _add_inflow_to_coastal_waters(results, preloaded_data, current_params, dataset_noise, outflow_tracker)
    _add_wild_shellfish_and_macroalgae(results, preloaded_data, current_params, dataset_noise)
    _add_surface_water_emissions(results, preloaded_data, current_params, dataset_noise, outflow_tracker)
    _add_wild_fish_catch(results, preloaded_data, current_params, dataset_noise)
    # 'aqua_losses' <- A.05.021a_20260924-142624.xlsx (data_loader.py DATA_MAP):
    # Fiskeridirektoratet losses of farmed salmon/trout by cause, 1000 fish
    lost_fish_N_dict = find_recovered_lost_fish_N(
        preloaded_data['aqua_losses'], aqua_production_dict, current_params, dataset_noise
    )
    _add_aquaculture_internal_flows(results, aqua_production_dict, lost_fish_N_dict, current_params, dataset_noise)
    
    return results


def _add_inflow_to_coastal_waters(results, preloaded_data, current_params, dataset_noise, outflow_tracker):
    """
    N reaching coastal waters (CW) via surface water (SW) from diffuse sources
    only - aquaculture and treated wastewater are excluded here because they
    have their own dedicated flows elsewhere.
    """
    flow_code = 'HY.SW-HY.CW-Inflow to coastal waters-Nmix'
    collected_years = set()

    key_teotil = 'TEOTIL'
    noise_teotil = dataset_noise[key_teotil]

    ww_discharge_dict = find_treated_wastewater_discharge(
        df_05280=preloaded_data.get('hy_ssb_05280_raw'),
        df_utslipp=preloaded_data.get('hy_utslipp_avlop_raw'),
        dataset_noise=dataset_noise
    )

    # 1990-2012: TEOTIL2 background, agriculture, urban and industry reaching
    # the coast, bias-corrected to TEOTIL3 (see find_teotil2_bias_corrected).
    # Aquaculture and wastewater are not included - they have their own flows.
    teotil2 = find_teotil2_bias_corrected(preloaded_data)
    for year, raw_val in teotil2['diffuse_to_coast'].items():
        year = int(year)
        collected_years.add(year)
        val = raw_val * noise_teotil

        outflow_tracker.loc[year, 'entries'] = 1
        outflow_tracker.loc[year, 'value'] = val

        results.append({
            'flow_name': flow_code, 'year': year, 'value': val,
            'comment': 'ok',
            'data_sources': 'NIVA TEOTIL2, bias-corrected to TEOTIL3'
        })

    # 2013 onward: TEOTIL3 model matrices.
    # 'hy_teotil3_to_coast'/'hy_teotil3_by_source' <- teotil3_n_summary.xlsx
    # (data_loader.py DATA_MAP): relevant N flows extracted from the TEOTIL
    # model, 2013 onward
    df_t3_coast = preloaded_data.get('hy_teotil3_to_coast')
    df_t3_source = preloaded_data.get('hy_teotil3_by_source')

    for r in range(len(df_t3_coast)):
        val_at_col0 = str(df_t3_coast.iloc[r, 0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue

        year = int(float(val_at_col0))
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            # Total N to coast minus the aquaculture-specific column (col 3),
            # then minus treated wastewater discharge below - both have their
            # own dedicated flows and must not be double-counted here.
            val = (float(df_t3_coast.iloc[r, 1]) / 1000.0) - (float(df_t3_source.iloc[r, 3]) / 1000.0)
            val *= noise_teotil

            if year in ww_discharge_dict:
                val -= ww_discharge_dict[year]

            # Unlike the other clamps in this file, this one is not proven
            # unreachable by construction: it's a residual of independently
            # sourced series (TEOTIL3 total, aquaculture, wastewater), so a
            # data mismatch could in principle drive it negative. Kept as an
            # intentional domain floor (a negative N flow has no physical
            # meaning) rather than removed.
            val = max(0.0, val)
            outflow_tracker.loc[year, 'entries'] = 1
            outflow_tracker.loc[year, 'value'] = val

            results.append({
                'flow_name': flow_code, 'year': year, 'value': val,
                'comment': 'ok',
                'data_sources': 'NIVA TEOTIL3'
            })

    # TEOTIL3 has not been updated for 2024; carry the 2023 value forward
    # with extra uncertainty rather than leave the flow silent for a year
    # the source will eventually cover.
    add_flat_carryforward_year(
        results, flow_code, collected_years, 2023, 2024, dataset_noise,
        data_sources='flat carry-forward from 2023 (TEOTIL3 not updated for 2024)'
    )

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_wild_shellfish_and_macroalgae(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HY.CW-MP.FP-Shellfish-Nmix'
    collected_years = set()
    
    fish_N_frac = float(current_params.get("fish_N_frac"))
    seaweed_N_frac = float(current_params.get("seaweed_N_frac"))
    
    key_fisk = 'Fiskeridirektoratet'
    noise_fisk = dataset_noise[key_fisk]

    # 'hy_art_raw' <- art.xlsx (data_loader.py DATA_MAP): Fiskeridirektoratet
    # catch statistics by species ("Fangst fordelt på art"), 2000-2024
    df_art = preloaded_data.get('hy_art_raw')
    # 'hy_fiske_old_raw' <- fiske_1990_2000.xlsx (data_loader.py DATA_MAP):
    # historical wild catch compilation (pelagic fish, bottom fish,
    # crustaceans, seaweed), 1990-2000, used to extend the modern
    # Fiskeridirektoratet series backward
    df_fiske_old = preloaded_data.get('hy_fiske_old_raw')

    shellfish_total_row = 35  # 'Delsum' subtotal for shellfish/crustacean species
    # Macroalgae rows: 'Brunalger' (kelp, all years) and 'Andre makroalger'
    # (from 2018). The 'Delsum' row for macroalgae is empty before 2011, so
    # the two rows are read directly. Quantities are wet weight.
    algae_rows = [39, 40]

    for col in range(2, df_art.shape[1]):
        val_at_cell = str(df_art.iloc[0, col]).strip()
        if val_at_cell.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue

        year = int(float(val_at_cell))
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            shellfish_kt = float(df_art.iloc[shellfish_total_row, col]) / 1000.0
            algae_kt = sum(float(df_art.iloc[r, col]) for r in algae_rows
                           if not pd.isna(df_art.iloc[r, col])) / 1000.0
            val = shellfish_kt * fish_N_frac + algae_kt * seaweed_N_frac

            results.append({
                'flow_name': flow_code, 'year': year, 'value': val * noise_fisk,
                'comment': 'ok', 'data_sources': 'Fiskeridirektoratet'
            })

    # Historical data (1990-1999): hy_art_raw covers 2000 onward, so this
    # loop stops at 1999.
    for r in range(1, 11):
        year = int(float(str(df_fiske_old.iloc[r, 0]).strip()))
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            # Column 3: crustaceans (1000 tons); column 4: seaweed (1000 tons)
            val = (float(df_fiske_old.iloc[r, 3]) * fish_N_frac) + (float(df_fiske_old.iloc[r, 4]) * seaweed_N_frac)

            results.append({
                'flow_name': flow_code, 'year': year, 'value': val * noise_fisk,
                'comment': 'ok', 'data_sources': 'Fiskeridirektoratet'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_surface_water_emissions(results, preloaded_data, current_params, dataset_noise, outflow_tracker):
    """
    Freshwater N retention and the associated atmospheric N2/N2O emissions.
      - 2013+ uses TEOTIL3's retention matrix directly.
      - 1990-2012 back-calculates retention from the diffuse coastal outflow
        (populated by _add_inflow_to_coastal_waters, which must run first) as
        Retention = Outflow * R, where R is TEOTIL3's mean ratio of retention
        to the diffuse inputs to the coast (total to coast minus aquaculture
        and wastewater) over the TEOTIL3 years. Retention is set relative to
        the diffuse part only, since aquaculture and most wastewater are
        discharged directly to the sea and do not pass lakes and rivers.
      - Years before 1990 are ignored (no outflow data to back-calculate from).
    """
    flow_n2 = 'HY.SW-AT.AT-Emissions-N2'
    flow_n2o = 'HY.SW-AT.AT-Emissions-N2O'
    collected_years = set()

    fraction_N2O = float(current_params.get("surface_water_fraction_to_N2O"))

    key_teotil = 'TEOTIL'
    key_interp = 'trend interpolation'

    noise_teotil = dataset_noise[key_teotil]

    # 2013 onward: read retention directly from the TEOTIL3 matrix.
    # 'hy_teotil3_retention' <- teotil3_n_summary.xlsx (data_loader.py
    # DATA_MAP): relevant N flows extracted from the TEOTIL model, 2013 onward
    df_t3_ret = preloaded_data.get('hy_teotil3_retention')

    for r in range(len(df_t3_ret)):
        val_at_col0 = str(df_t3_ret.iloc[r, 0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '', 'none']:
            continue

        year = int(float(val_at_col0))
        if year in EXPECTED_YEARS and year >= 2013:
            collected_years.add(year)
            base_ret_val = (float(df_t3_ret.iloc[r, 1]) / 1000.0) * noise_teotil

            results.append({'flow_name': flow_n2, 'year': year, 'value': base_ret_val * (1.0 - fraction_N2O),
                            'comment': 'ok', 'data_sources': 'NIVA TEOTIL3'})
            results.append({'flow_name': flow_n2o, 'year': year, 'value': base_ret_val * fraction_N2O,
                            'comment': 'ok', 'data_sources': 'NIVA TEOTIL3'})

    # 1990-2012: back-calculate retention from outflow_tracker (see docstring).
    # 'hy_teotil3_to_coast'/'hy_teotil3_by_source' <- teotil3_n_summary.xlsx
    t3_ret = teotil3_table(df_t3_ret)['totn_retained_tonnes']
    t3_src = teotil3_table(preloaded_data['hy_teotil3_by_source'])
    t3_coast = teotil3_table(preloaded_data['hy_teotil3_to_coast'])['totn_to-coast_tonnes']
    t3_diffuse_to_coast = (t3_coast - t3_src['aquaculture_totn_tonnes']
                           - t3_src['large-wastewater_totn_tonnes'] - t3_src['spredt_totn_tonnes'])
    ret_ratio = t3_ret.mean() / t3_diffuse_to_coast.loc[t3_ret.index].mean()
    noise_interp = dataset_noise[key_interp]

    missing_years = {y for y in EXPECTED_YEARS if y >= 1990} - collected_years

    for year in sorted(missing_years):
        if year in outflow_tracker.index and outflow_tracker.loc[year, 'entries'] == 1:
            collected_years.add(year)

            hist_ret_val = outflow_tracker.loc[year, 'value'] * ret_ratio
            hist_ret_val *= noise_interp

            results.append({'flow_name': flow_n2, 'year': year, 'value': hist_ret_val * (1.0 - fraction_N2O),
                            'comment': 'ok', 'data_sources': 'Calculation model'})
            results.append({'flow_name': flow_n2o, 'year': year, 'value': hist_ret_val * fraction_N2O,
                            'comment': 'ok', 'data_sources': 'Calculation model'})

    # TEOTIL3 has not been updated for 2024; carry the 2023 value forward
    # with extra uncertainty rather than leave the flow silent for a year
    # the source will eventually cover. collected_years is shared by both
    # flows (they're always added together above), so each call gets its
    # own copy - otherwise the first call marking 2024 "collected" would
    # make the second call's no-op guard skip flow_n2o entirely.
    cy_n2, cy_n2o = set(collected_years), set(collected_years)
    add_flat_carryforward_year(
        results, flow_n2, cy_n2, 2023, 2024, dataset_noise,
        data_sources='flat carry-forward from 2023 (TEOTIL3 not updated for 2024)'
    )
    add_flat_carryforward_year(
        results, flow_n2o, cy_n2o, 2023, 2024, dataset_noise,
        data_sources='flat carry-forward from 2023 (TEOTIL3 not updated for 2024)'
    )
    collected_years |= cy_n2 | cy_n2o

    # Missing-year bookkeeping (years 1990 onward only) - both flows need this,
    # not just flow_n2, or flow_n2o silently ends up with fewer rows.
    expected_from_1990 = {y for y in EXPECTED_YEARS if y >= 1990}
    report_missing_years(flow_n2, expected_from_1990 - collected_years, results)
    report_missing_years(flow_n2o, expected_from_1990 - collected_years, results)
    
    
def _add_wild_fish_catch(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HY.CW-MP.FP-Fish (wild catch)-Nmix'
    collected_years = set()
    
    fish_N_frac = float(current_params.get("fish_N_frac"))
    key_fisk = 'Fiskeridirektoratet'
    noise_fisk = dataset_noise[key_fisk]

    # 'hy_art_raw' <- art.xlsx (data_loader.py DATA_MAP): Fiskeridirektoratet
    # catch statistics by species ("Fangst fordelt på art"), 2000-2024
    df_art = preloaded_data.get('hy_art_raw')

    for col in range(2, df_art.shape[1]):
        val_at_cell = str(df_art.iloc[0, col]).strip()
        if val_at_cell.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue

        year = int(float(val_at_cell))
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            val = 0.0
            # 'Delsum' subtotal rows for pelagic fish, cod-family fish, other
            # bottom/deep-water fish, and skates/sharks - i.e. all "true fish"
            # categories, excluding shellfish and seaweed (see the shellfish
            # and macroalgae flow above).
            for r_idx in [15, 20, 26, 38]:
                if not pd.isna(df_art.iloc[r_idx, col]):
                    val += float(df_art.iloc[r_idx, col])

            val_kt_N = (val / 1000.0) * fish_N_frac * noise_fisk
            results.append({
                'flow_name': flow_code, 'year': year, 'value': val_kt_N,
                'comment': 'ok', 'data_sources': 'Fiskeridirektoratet'
            })

    # Historical data (1990-1999): hy_art_raw already has complete data for
    # year 2000 onward, so this loop stops one year short to avoid double-
    # counting 2000.
    # 'hy_fiske_old_raw' <- fiske_1990_2000.xlsx (data_loader.py DATA_MAP):
    # historical wild catch compilation (pelagic fish, bottom fish,
    # crustaceans, seaweed), 1990-2000, used to extend the modern
    # Fiskeridirektoratet series backward
    df_fiske_old = preloaded_data.get('hy_fiske_old_raw')

    for r in range(1, 11):
        val_at_col0 = str(df_fiske_old.iloc[r, 0]).strip()
        year = int(float(val_at_col0))

        if year in EXPECTED_YEARS:
            collected_years.add(year)
            # Column 1: pelagic fish (1000 tons); column 2: bottom fish (1000 tons)
            val = (float(df_fiske_old.iloc[r, 1]) + float(df_fiske_old.iloc[r, 2])) * fish_N_frac * noise_fisk

            results.append({
                'flow_name': flow_code, 'year': year, 'value': val,
                'comment': 'ok', 'data_sources': 'Fiskeridirektoratet'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)

def _add_aquaculture_internal_flows(results, aquaculture_production_dict, lost_fish_N_dict, current_params, dataset_noise):
    flow_harvest = 'HY.AC-MP.FP-Coastal fish and seafood-Nmix'
    flow_waste = 'HY.AC-HY.CW-Waste feed-Nmix'
    flow_excretia = 'HY.AC-HY.CW-Excretia-Nmix'

    collected_years = set()

    for year, fish_harvested_N in aquaculture_production_dict.items():
        if year in EXPECTED_YEARS:
            collected_years.add(year)

            # 1. Fish leaving the pool: sold fish plus dead and discarded fish
            # taken out of the sea (see find_recovered_lost_fish_N).
            lost_fish_N = lost_fish_N_dict[year]
            results.append({
                'flow_name': flow_harvest, 'year': year, 'value': fish_harvested_N + lost_fish_N,
                'comment': 'ok', 'data_sources': 'Fiskeridirektoratet'
            })

            # 2. Feed waste and faeces to coastal water: get_aquafeed_budget
            # splits harvested N into the same underlying feed budget used by
            # MP.FP-HY.AC-Feed to coastal aquaculture-Nmix and RW.RW-HY.AC-
            # Aquaculture feed import-Nmix (see its docstring), so all three
            # flows stay mass-balance consistent. The budget is built from
            # sold fish only, since the apparent retention it uses (Aas et al.
            # 2022) is a whole-system figure that already counts lost fish as
            # unretained feed N.
            _, _, waste_val, excretia_val = get_aquafeed_budget(fish_harvested_N, year, current_params, dataset_noise)
            # Lost fish ate feed that stayed in their bodies rather than being
            # excreted, so their N is taken out of excretion.
            excretia_val -= lost_fish_N

            results.append({
                'flow_name': flow_waste, 'year': year, 'value': waste_val,
                'comment': 'ok', 'data_sources': 'Mass balance'
            })

            # 3. Metabolic (dissolved) excretion to coastal water: the eaten
            # feed N that wasn't retained as fish biomass.
            results.append({
                'flow_name': flow_excretia, 'year': year, 'value': excretia_val,
                'comment': 'ok', 'data_sources': 'Mass balance'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_harvest, missing_years, results)