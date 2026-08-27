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
    report_missing_years
)
from calculations.shared_flow_calculations import (
    find_aquaculture_production,
    find_treated_wastewater_discharge
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
    _add_aquaculture_internal_flows(results, aqua_production_dict, current_params)
    
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

    # Earlier years (1990-2012): Miljødirektoratet's coastal N-loading compilation.
    # 'hy_kyst_tilforsel' <- Tilførsel av nitrogen til kystområdene fordelt på
    # kilder.xlsx (data_loader.py DATA_MAP): N loading to Norwegian coastal
    # areas by source, 1990-2023
    df_kyst = preloaded_data.get('hy_kyst_tilforsel')

    for i in range(len(df_kyst)):
        val_at_col0 = str(df_kyst.iloc[i, 0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue

        year = int(float(val_at_col0))
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            # Columns 3-6: Bakgrunn (background), Bebygd (built-up/urban),
            # Industri, Jordbruk (agriculture). Akvakultur (col 1) and Avløp
            # (col 2) are deliberately excluded - they're covered by the
            # dedicated aquaculture and wastewater flows.
            val = (float(df_kyst.iloc[i, 3]) + float(df_kyst.iloc[i, 4]) +
                   float(df_kyst.iloc[i, 5]) + float(df_kyst.iloc[i, 6])) / 1000.0
            val *= noise_teotil

            outflow_tracker.loc[year, 'entries'] = 1
            outflow_tracker.loc[year, 'value'] = val

            results.append({
                'flow_name': flow_code, 'year': year, 'value': val,
                'comment': 'ok',
                'data_sources': 'Miljødirektoratet / TEOTIL'
            })

    # Later years (2013 onward): TEOTIL3 model matrices, superseding the
    # Miljødirektoratet figures above for overlapping years.
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

            existing_posts = [p for p in results if p['flow_name'] == flow_code and p['year'] == year]
            if existing_posts:
                existing_posts[0]['value'] = val
                existing_posts[0]['comment'] = 'ok'
            else:
                results.append({
                    'flow_name': flow_code, 'year': year, 'value': val,
                    'comment': 'ok',
                    'data_sources': 'NIVA TEOTIL3'
                })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_wild_shellfish_and_macroalgae(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'HY.CW-MP.FP-Shellfish-Nmix'
    collected_years = set()
    
    fish_N_frac = float(current_params.get("fish_N_frac"))
    seaweed_N_frac = float(current_params.get("seaweed_N_frac"))
    
    key_fisk = 'Fiskeridirektoratet'
    noise_fisk = dataset_noise[key_fisk]
    noise_interp = dataset_noise['trend interpolation']

    # 'hy_art_raw' <- art.xlsx (data_loader.py DATA_MAP): Fiskeridirektoratet
    # catch statistics by species ("Fangst fordelt på art"), 2000-2024
    df_art = preloaded_data.get('hy_art_raw')
    # 'hy_fiske_old_raw' <- fiske_1990_2000.xlsx (data_loader.py DATA_MAP):
    # historical wild catch compilation (pelagic fish, bottom fish,
    # crustaceans, seaweed), 1990-2000, used to extend the modern
    # Fiskeridirektoratet series backward
    df_fiske_old = preloaded_data.get('hy_fiske_old_raw')

    shellfish_total_row = 35  # 'Delsum' subtotal for shellfish/crustacean species
    algae_total_row = 41      # 'Delsum' subtotal for macroalgae; NaN before 2011

    # Anchor points to bridge the 2001-2010 gap in hy_art_raw's macroalgae
    # data: the last historical seaweed figure (2000) and the first modern
    # one (2011).
    year_to_col = {}
    for col in range(2, df_art.shape[1]):
        val_at_cell = str(df_art.iloc[0, col]).strip()
        if val_at_cell.lower() not in ['year', 'år', 'årstall', 'nan', '']:
            year_to_col[int(float(val_at_cell))] = col
    seaweed_2011_kt = float(df_art.iloc[algae_total_row, year_to_col[2011]]) / 1000.0

    seaweed_2000_kt = None
    for r in range(1, 12):
        if int(float(str(df_fiske_old.iloc[r, 0]).strip())) == 2000:
            seaweed_2000_kt = float(df_fiske_old.iloc[r, 4])
            break

    for col in range(2, df_art.shape[1]):
        val_at_cell = str(df_art.iloc[0, col]).strip()
        if val_at_cell.lower() in ['year', 'år', 'årstall', 'nan', '']:
            continue

        year = int(float(val_at_cell))
        # Year 2000 is left to hy_fiske_old_raw below: this sheet's macroalgae
        # subtotal (row 41) is NaN before 2011, so using it for 2000 would
        # silently drop the seaweed component that the historical source has.
        if year in EXPECTED_YEARS and year > 2000:
            collected_years.add(year)
            val = 0.0
            data_source = 'Fiskeridirektoratet'

            if not pd.isna(df_art.iloc[shellfish_total_row, col]):
                val += (float(df_art.iloc[shellfish_total_row, col]) / 1000.0) * fish_N_frac

            algae_cell = df_art.iloc[algae_total_row, col]
            if not pd.isna(algae_cell):
                val += (float(algae_cell) / 1000.0) * seaweed_N_frac
            elif 2001 <= year <= 2010:
                # No macroalgae figure in this sheet before 2011; linearly
                # interpolate between the 2000 (historical) and 2011 (modern)
                # anchors, with interpolation noise on top of the regular
                # dataset noise applied below.
                frac = (year - 2000) / (2011 - 2000)
                interp_seaweed_kt = seaweed_2000_kt + frac * (seaweed_2011_kt - seaweed_2000_kt)
                val += interp_seaweed_kt * seaweed_N_frac * noise_interp
                data_source = 'interpolated (Fiskeridirektoratet macroalgae gap)'

            results.append({
                'flow_name': flow_code, 'year': year, 'value': val * noise_fisk,
                'comment': 'ok', 'data_sources': data_source
            })

    # Historical data (1990-2000): the only source with a seaweed component
    # covering years before 2011.
    for r in range(1, 12):
        val_at_col0 = str(df_fiske_old.iloc[r, 0]).strip()
        if val_at_col0.lower() in ['year', 'år', 'årstall', 'nan', '', 'none']:
            continue

        year = int(float(val_at_col0))
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
      - 1990-2012 back-calculates retention from coastal outflow (populated by
        _add_inflow_to_coastal_waters, which must run first) using a typical
        retention fraction: Retention = Outflow * ret_frac / (1 - ret_frac),
        derived from Outflow = Inflow * (1 - ret_frac).
      - Years before 1990 are ignored (no outflow data to back-calculate from).
    """
    flow_n2 = 'HY.SW-AT.AT-Emissions-N2'
    flow_n2o = 'HY.SW-AT.AT-Emissions-N2O'
    collected_years = set()

    fraction_N2O = float(current_params.get("surface_water_fraction_to_N2O"))
    ret_frac = float(current_params.get("surface_water_retention_fraction"))

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
    noise_interp = dataset_noise[key_interp]

    missing_years = {y for y in EXPECTED_YEARS if y >= 1990} - collected_years

    for year in sorted(missing_years):
        if year in outflow_tracker.index and outflow_tracker.loc[year, 'entries'] == 1:
            collected_years.add(year)

            hist_ret_val = outflow_tracker.loc[year, 'value'] * ret_frac / (1.0 - ret_frac)
            hist_ret_val *= noise_interp

            results.append({'flow_name': flow_n2, 'year': year, 'value': hist_ret_val * (1.0 - fraction_N2O),
                            'comment': 'ok', 'data_sources': 'Calculation model'})
            results.append({'flow_name': flow_n2o, 'year': year, 'value': hist_ret_val * fraction_N2O,
                            'comment': 'ok', 'data_sources': 'Calculation model'})

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

def _add_aquaculture_internal_flows(results, aquaculture_production_dict, current_params):
    flow_harvest = 'HY.AC-MP.FP-Coastal fish and seafood-Nmix'
    flow_waste = 'HY.AC-HY.CW-Waste feed-Nmix'
    flow_excretia = 'HY.AC-HY.CW-Excretia-Nmix'
    
    collected_years = set()
    
    prot_ret = float(current_params.get("aquafeed_N_retention"))
    feed_waste = float(current_params.get("aquafeed_waste_fraction"))

    for year, fish_harvested_N in aquaculture_production_dict.items():
        if year in EXPECTED_YEARS:
            collected_years.add(year)

            # 1. Harvested fish leaving the pool.
            results.append({
                'flow_name': flow_harvest, 'year': year, 'value': fish_harvested_N,
                'comment': 'ok', 'data_sources': 'Fiskeridirektoratet'
            })

            # 2. Feed waste and faeces to coastal water: back-calculate total
            # feed N from the harvested N via the retention fraction, then
            # split off the fraction lost as uneaten feed.
            total_feed_N = (fish_harvested_N / prot_ret) if prot_ret > 0 else 0.0
            waste_val = total_feed_N * feed_waste

            results.append({
                'flow_name': flow_waste, 'year': year, 'value': waste_val,
                'comment': 'ok', 'data_sources': 'Mass balance'
            })

            # 3. Metabolic (dissolved) excretion to coastal water: whatever's
            # left of total feed N once retained and wasted N are removed.
            excretia_val = total_feed_N * (1.0 - prot_ret - feed_waste)
            results.append({
                'flow_name': flow_excretia, 'year': year, 'value': excretia_val,
                'comment': 'ok', 'data_sources': 'Mass balance'
            })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_harvest, missing_years, results)