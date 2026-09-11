#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nitrogen use efficiency (NUE) and mass-balance trend calculations for the
article. Reads output_files/MC_Reporting_Statistics.xlsx (produced by
main_mc.py) and reports median-based NUE ratios and mass balances for a set
of questions defined and discussed while writing the article, each with a
Mann-Kendall significance test and a Theil-Sen slope estimate.

Run directly to print a full report to stdout:

    python3 nue_analysis.py

Re-run whenever the underlying model output changes (i.e. after any
main_mc.py run that regenerates MC_Reporting_Statistics.xlsx) to refresh the
numbers used in the article.

Only the run's median values are used (no re-sampling of the MC
distributions) - this mirrors how the numbers were derived and reported in
the article's supporting analysis.
"""

import itertools
from math import erf, sqrt

import numpy as np
import pandas as pd

STATS_FILE = 'output_files/MC_Reporting_Statistics.xlsx'
ANALYSIS_YEARS = range(1990, 2024)  # the only years with complete flow coverage for all pools


# =============================================================================
# Trend statistics: Mann-Kendall significance test + Theil-Sen slope estimator
# =============================================================================
# Implemented from scratch (no scipy/pymannkendall available in this
# environment). Standard WMO/IPCC-style non-parametric trend methodology:
# Mann-Kendall for significance (robust to non-normal residuals and outliers),
# Theil-Sen for the slope (median of all pairwise slopes, robust to outliers).

def mann_kendall(values):
    """Returns (S, Z, p_value) for the two-sided Mann-Kendall trend test."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    S = sum(np.sign(values[j] - values[i]) for i, j in itertools.combinations(range(n), 2))

    _, counts = np.unique(values, return_counts=True)
    tie_term = np.sum(counts * (counts - 1) * (2 * counts + 5))
    var_S = (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0

    if S > 0:
        Z = (S - 1) / sqrt(var_S)
    elif S < 0:
        Z = (S + 1) / sqrt(var_S)
    else:
        Z = 0.0
    p_value = 2 * (1 - 0.5 * (1 + erf(abs(Z) / sqrt(2))))
    return S, Z, p_value


def theil_sen(years, values):
    """Returns (slope, intercept) for the Theil-Sen estimator (median of all
    pairwise slopes between distinct years, plus the median-of-residuals
    intercept)."""
    years = np.asarray(years, dtype=float)
    values = np.asarray(values, dtype=float)
    n = len(values)
    slopes = [
        (values[j] - values[i]) / (years[j] - years[i])
        for i, j in itertools.combinations(range(n), 2)
        if years[j] != years[i]
    ]
    slope = np.median(slopes)
    intercept = np.median(values - slope * years)
    return slope, intercept


def trend_report(years, values, start_year, end_year):
    """Runs Mann-Kendall + Theil-Sen on a (years, values) series and returns a
    dict with the fitted start/end values, percent change between them (via
    the Theil-Sen fit, not the raw endpoints), and the Mann-Kendall p-value."""
    S, Z, p_value = mann_kendall(values)
    slope, intercept = theil_sen(years, values)
    fit_start = intercept + slope * start_year
    fit_end = intercept + slope * end_year
    pct_change = 100 * (fit_end - fit_start) / abs(fit_start) if fit_start != 0 else float('nan')
    return {
        'sen_slope_per_year': slope,
        'fit_start': fit_start,
        'fit_end': fit_end,
        'pct_change': pct_change,
        'mk_Z': Z,
        'mk_p': p_value,
    }


# =============================================================================
# Data loading
# =============================================================================

def load_stats():
    df = pd.read_excel(STATS_FILE)
    df.columns = [c.strip() for c in df.columns]
    return df


def flow_series(df, flow_name, years=ANALYSIS_YEARS):
    """Median value of one flow_name for each year in `years` (0.0 if a year
    is genuinely absent - only used for flows confirmed present in all
    ANALYSIS_YEARS; a silent 0.0 for a missing year would otherwise corrupt a
    sum without warning)."""
    sub = df[df['flow_name'] == flow_name].set_index('year')['median']
    missing = set(years) - set(sub.index)
    if missing:
        raise KeyError(f"'{flow_name}' is missing values for years: {sorted(missing)}")
    return sub.reindex(years)


def sum_flows(df, flow_names, years=ANALYSIS_YEARS):
    total = pd.Series(0.0, index=list(years))
    for name in flow_names:
        total = total.add(flow_series(df, name, years), fill_value=0.0)
    return total


# =============================================================================
# Flow-name groupings, one place per question so a data/flow-name change only
# needs to be updated here.
# =============================================================================

FERTILIZER_SM = [
    'MP.OP-AG.SM-Mineral fertilizer-Nmix',       # domestic
    'RW.RW-AG.SM-Mineral fertilizer import-Nmix',  # imported
]
DEPOSITION_SM = [
    'AT.AT-AG.SM-Deposition-OXN',
    'AT.AT-AG.SM-Deposition-RDN',
]
BNF_SM = ['AT.AT-AG.SM-Biological N2 fixation-N2']
MANURE_APPLICATION = ['AG.MM-AG.SM-Manure application-Nmix']
GRAZING_UTMARK = ['FS.OL-AG.MM-Grazing-Nmix']
FODDER_CROPS = ['AG.SM-AG.MM-Fodder crops-Nmix']  # includes innmark grazing, see ag_mc.py
FARM_ANIMAL_FEED = ['MP.FP-AG.MM-Farm animal feed-Nmix']
FEED_IMPORT = ['RW.RW-AG.MM-Animal feed import-Nmix']  # terrestrial livestock feed only, not aquafeed

FOOD_CROP_PRODUCTS = ['AG.SM-MP.FP-Food crop products-Nmix']
INDUSTRIAL_CROP_PRODUCTS = ['AG.SM-MP.OP-Crop products for industrial use-Nmix']
ANIMAL_PRODUCTS = ['AG.MM-MP.FP-Animal products-Nmix']
NON_EDIBLE_ANIMAL_PRODUCTS = ['AG.MM-MP.OP-Non-edible animal products-Nmix']

FOOD_PRODUCTS_CONSUMED = ['MP.FP-HS.HS-Food products-Nmix']  # national consumption, SSB-based
FOOD_EXPORT_TOTAL = ['MP.FP-RW.RW-Food export-Nmix']  # includes fish - see food_export_excluding_fish()

# Wild catch and aquaculture feed, used only by the fish/aquaculture-included
# variant of Q3 below - treated the same way BNF is treated elsewhere: a
# 'free' natural N source (wild catch) or an external feed cost (aquafeed)
# that must be counted as an input if the corresponding output (fish landed
# or farmed) is counted as food.
WILD_CATCH = [
    'HY.CW-MP.FP-Fish (wild catch)-Nmix',
    'HY.CW-MP.FP-Shellfish-Nmix',
]
AQUACULTURE_FEED = [
    'MP.FP-HY.AC-Feed to coastal aquaculture-Nmix',  # domestic
    'RW.RW-HY.AC-Aquaculture feed import-Nmix',       # imported
]

# 'kjøtt/fisk/meieri/egg' bundles fish together with meat/dairy/eggs at the
# trade_mapping type level, so excluding fish from Food export requires going
# one level deeper to the konv codes (MC_Reporting_Statistics.xlsx only has
# the already-summed flow, not this breakdown).
FOOD_EXPORT_TYPES = {'korn/planter', 'kjøtt/fisk/meieri/egg', 'mat'}
FISH_EXPORT_KONV = 'fish_fresh_frozen'


def food_export_excluding_fish(years=ANALYSIS_YEARS):
    """MP.FP-RW.RW-Food export-Nmix, with the fish_fresh_frozen konv category
    removed. Norway's fish exports (the vast majority of Food export by mass)
    are not matched by any fertilizer/manure/BNF/deposition input in Q3's
    denominator, since they come from the sea rather than AG.SM - including
    them in N_food would inflate food-system NUE without a matching
    input-side cost. Uses the trade_parameters median value (not
    MC-perturbed) for a single, reproducible point estimate, since this
    breakdown isn't carried in MC_Reporting_Statistics.xlsx."""
    from data_loader import load_all_data
    preloaded = load_all_data({'mp'})
    df_vol = preloaded['compressed_trade_volume']
    trade_params = pd.read_excel('parameters/N_parameters.xlsx', sheet_name='trade_parameters')
    factors = dict(zip(trade_params['param_id'], trade_params['value']))

    is_export = df_vol['impeks'].astype(str).str.strip().isin(['2', '2.0'])
    is_food = df_vol['type'].astype(str).str.lower().str.strip().isin(FOOD_EXPORT_TYPES)
    is_not_fish = df_vol['konv'] != FISH_EXPORT_KONV
    sub = df_vol[is_export & is_food & is_not_fish].copy()
    sub['N_amount'] = sub['amount'] * sub['konv'].map(factors).fillna(0.0) / 1e6

    yearly = sub.groupby('year')['N_amount'].sum()
    yearly.index = yearly.index.astype(int)
    return yearly.reindex(years, fill_value=0.0)

# Full mass-balance flow sets (all inflows/outflows, not just the
# efficiency-scoped subset above) - used for the AG.MM/AG.SM balance
# investigation, not for the NUE ratios themselves.
MM_IN_FULL = FODDER_CROPS + GRAZING_UTMARK + FARM_ANIMAL_FEED + FEED_IMPORT + [
    'RW.RW-AG.MM-Live animal import-Nmix',
]
MM_OUT_FULL = MANURE_APPLICATION + [
    'AG.MM-AT.AT-Emissions-N2O', 'AG.MM-AT.AT-Emissions-NH3', 'AG.MM-AT.AT-Emissions-NOx',
    'AG.MM-HY.SW-Leaching-Nmix',
] + ANIMAL_PRODUCTS + NON_EDIBLE_ANIMAL_PRODUCTS + ['AG.MM-RW.RW-Live animal export-Nmix']
SM_IN_FULL = MANURE_APPLICATION + BNF_SM + DEPOSITION_SM + [
    'MP.FP-AG.SM-Seeds and planting material -Nmix',
] + FERTILIZER_SM + [
    'PR.SO-AG.SM-Biologically treated organic waste-Nmix',
    'PR.WW-AG.SM-Sewage sludge fertilizer-Nmix',
]
SM_OUT_FULL = FODDER_CROPS + [
    'AG.SM-AT.AT-Emissions-N2', 'AG.SM-AT.AT-Emissions-N2O', 'AG.SM-AT.AT-Emissions-NH3',
    'AG.SM-AT.AT-Emissions-NOx', 'AG.SM-HY.SW-Leaching-Nmix',
] + FOOD_CROP_PRODUCTS + INDUSTRIAL_CROP_PRODUCTS


# =============================================================================
# Question 1: has agricultural N-efficiency changed since Bleken & Bakken (1997)?
# =============================================================================

def q1a_ag_whole_nue(df, years=ANALYSIS_YEARS):
    """AG as a whole, external flows only (AG.SM<->AG.MM internal transfers
    excluded to avoid double counting)."""
    inp = sum_flows(df, FERTILIZER_SM + DEPOSITION_SM + GRAZING_UTMARK + BNF_SM + FEED_IMPORT, years)
    out = sum_flows(df, FOOD_CROP_PRODUCTS + INDUSTRIAL_CROP_PRODUCTS + ANIMAL_PRODUCTS + NON_EDIBLE_ANIMAL_PRODUCTS, years)
    return 100 * out / inp


def q1b_ag_mm_nue(df, years=ANALYSIS_YEARS):
    """AG.MM alone. Feed counted in full as input since the subsystem is
    viewed in isolation here; manure deliberately excluded (it comes from the
    animals, not into them)."""
    inp = sum_flows(df, FODDER_CROPS + FARM_ANIMAL_FEED + FEED_IMPORT + GRAZING_UTMARK, years)
    out = sum_flows(df, ANIMAL_PRODUCTS + NON_EDIBLE_ANIMAL_PRODUCTS, years)
    return 100 * out / inp


def q1c_ag_sm_nue(df, years=ANALYSIS_YEARS):
    """AG.SM alone."""
    inp = sum_flows(df, MANURE_APPLICATION + FERTILIZER_SM + DEPOSITION_SM + BNF_SM, years)
    out = sum_flows(df, FODDER_CROPS + FOOD_CROP_PRODUCTS + INDUSTRIAL_CROP_PRODUCTS, years)
    return 100 * out / inp


# =============================================================================
# Question 2: how much does imported feed flatter the naive AG-whole NUE?
# =============================================================================

def q2_corrected_ag_whole_nue(df, years=ANALYSIS_YEARS):
    """Replaces the raw imported-feed tonnage with its 'domestic-equivalent
    cost': imported feed x AG.SM's own N-cost (1/NUE), i.e. what it would
    have cost in N terms to grow the same feed value domestically."""
    naive_nue = q1a_ag_whole_nue(df, years)

    sm_nue_frac = q1c_ag_sm_nue(df, years) / 100.0
    sm_n_cost = 1.0 / sm_nue_frac  # Bleken & Bakken style N-cost = input/output

    inp_excl_feed = sum_flows(df, FERTILIZER_SM + DEPOSITION_SM + GRAZING_UTMARK + BNF_SM, years)
    feed_import = flow_series(df, FEED_IMPORT[0], years)
    corrected_inp = inp_excl_feed + feed_import * sm_n_cost

    out = sum_flows(df, FOOD_CROP_PRODUCTS + INDUSTRIAL_CROP_PRODUCTS + ANIMAL_PRODUCTS + NON_EDIBLE_ANIMAL_PRODUCTS, years)
    corrected_nue = 100 * out / corrected_inp
    return naive_nue, corrected_nue


# Monogastric meat categories (chicken/duck/goose/turkey/pig): unlike
# ruminants, these species eat almost no home-grown roughage, so their share
# of animal-product N is a proxy for how much of AG.MM's output depends on
# concentrate feed (increasingly imported) rather than domestic grazing/
# fodder - directly relevant context for Q2's imported-feed correction.
POULTRY_TURKEY_PORK_ITEMS = [
    'Meat of chickens, fresh or chilled',
    'Meat of ducks, fresh or chilled',
    'Meat of geese, fresh or chilled',
    'Meat of turkeys, fresh or chilled',
    'Meat of pig with the bone, fresh or chilled',
]


def poultry_pork_share_of_animal_products(years=ANALYSIS_YEARS):
    """Poultry+turkey+pork's share (%) of AG.MM-MP.FP-Animal products-Nmix,
    recomputed from the same FAOSTAT item-level data and animal_products
    N-content table the flow itself is built from (item-level detail isn't
    kept in the aggregated MC_Reporting_Statistics.xlsx flow), using the
    table's median N_content_percent (not MC-perturbed) for a single,
    reproducible point estimate."""
    from data_loader import load_all_data
    preloaded = load_all_data({'ag'})
    df_fao = preloaded['fao_animal_production_clean']

    n_content = pd.read_excel('parameters/N_parameters.xlsx', sheet_name='animal_products')
    factors = dict(zip(n_content['item'], n_content['N_content_percent']))

    working = df_fao.copy()
    working['N_amount_kt'] = working['Value'] * working['Item'].map(factors) / 1.0e5
    working['is_poultry_pork'] = working['Item'].isin(POULTRY_TURKEY_PORK_ITEMS)

    total_by_year = working.groupby('Year')['N_amount_kt'].sum()
    subset_by_year = working[working['is_poultry_pork']].groupby('Year')['N_amount_kt'].sum()

    share = 100 * subset_by_year.reindex(total_by_year.index, fill_value=0.0) / total_by_year
    share.index = share.index.astype(int)
    return share.reindex(years)


# =============================================================================
# Question 3: food-system NUE (Hayashi/Erisman-style), land-based, aquaculture
# excluded. See claude_tekst/2026-09-10_NUE_metodikk_og_beregninger.md for the
# full discussion of why each term is scoped the way it is - in particular,
# N_import here is DELIBERATELY feed import only (not food import): food
# import substitutes for domestic production rather than feeding into it.
# =============================================================================

def q3_food_system_nue(df, years=ANALYSIS_YEARS):
    """N_food = domestic consumption + non-fish food export, i.e. all food
    the system produced whether it was eaten domestically or exported (fish
    export excluded - see food_export_excluding_fish())."""
    denom = sum_flows(df, FERTILIZER_SM + MANURE_APPLICATION + BNF_SM + DEPOSITION_SM + FEED_IMPORT, years)
    n_food = flow_series(df, FOOD_PRODUCTS_CONSUMED[0], years) + food_export_excluding_fish(years)
    return 100 * n_food / denom


def q3_food_system_nue_incl_fish(df, years=ANALYSIS_YEARS):
    """Same formula as q3_food_system_nue(), but with wild catch and
    aquaculture brought into the system boundary instead of excluded, for
    comparison: wild catch (no feed of its own) is added to the denominator
    alongside BNF/deposition as another 'free' natural N input, aquaculture
    feed (domestic + imported) is added as its N cost, and the numerator uses
    the full, un-filtered Food export (fish included) instead of
    food_export_excluding_fish()."""
    denom = sum_flows(
        df,
        FERTILIZER_SM + MANURE_APPLICATION + BNF_SM + DEPOSITION_SM + FEED_IMPORT
        + WILD_CATCH + AQUACULTURE_FEED,
        years,
    )
    n_food = flow_series(df, FOOD_PRODUCTS_CONSUMED[0], years) + flow_series(df, FOOD_EXPORT_TOTAL[0], years)
    return 100 * n_food / denom


# =============================================================================
# AG.MM / AG.SM full mass balance (all inflows minus all outflows, not just
# the efficiency-scoped subset above) - the basis for the 2026-09 asymmetry
# investigation (MM persistently positive, SM close to balanced/slightly
# negative).
# =============================================================================

def ag_mm_balance(df, years=ANALYSIS_YEARS):
    return sum_flows(df, MM_IN_FULL, years) - sum_flows(df, MM_OUT_FULL, years)


def ag_sm_balance(df, years=ANALYSIS_YEARS):
    return sum_flows(df, SM_IN_FULL, years) - sum_flows(df, SM_OUT_FULL, years)


def ag_total_balance(df, years=ANALYSIS_YEARS):
    """MM balance + SM balance; the AG.SM<->AG.MM internal flows (manure
    application, fodder crops) cancel out automatically since they appear
    once on each side."""
    return ag_mm_balance(df, years) + ag_sm_balance(df, years)


# =============================================================================
# Per-hectare and per-capita normalisations
# =============================================================================

# NIBIO's agricultural area figure, the same one used to derive
# denitrification_AG_N2 in N_parameters.xlsx (14 kg N/ha German default x
# this area). A single recent-vintage value, not a historical time series -
# this project does not currently load a yearly agricultural-area dataset, so
# it is treated as constant across all years. Revisit if a proper time series
# becomes available, since Norway's agricultural area has drifted over 1990-2023.
AGRICULTURAL_AREA_HA = 1_132_693

AG_LEACHING = ['AG.SM-HY.SW-Leaching-Nmix', 'AG.MM-HY.SW-Leaching-Nmix']
AG_ATMOSPHERIC_LOSSES = [
    'AG.SM-AT.AT-Emissions-N2', 'AG.SM-AT.AT-Emissions-N2O', 'AG.SM-AT.AT-Emissions-NH3', 'AG.SM-AT.AT-Emissions-NOx',
    'AG.MM-AT.AT-Emissions-N2O', 'AG.MM-AT.AT-Emissions-NH3', 'AG.MM-AT.AT-Emissions-NOx',
]


def ag_per_hectare(df, years=ANALYSIS_YEARS):
    """Leaching, atmospheric losses (NH3+N2O+NOx+N2) and total input reaching
    agricultural soil (fertiliser + manure + BNF + deposition + seeds +
    organic waste/sludge - i.e. SM_IN_FULL), all in kg N/ha/year."""
    kt_to_kg_per_ha = 1.0e6 / AGRICULTURAL_AREA_HA
    return pd.DataFrame({
        'leaching_kgN_ha': sum_flows(df, AG_LEACHING, years) * kt_to_kg_per_ha,
        'atmospheric_kgN_ha': sum_flows(df, AG_ATMOSPHERIC_LOSSES, years) * kt_to_kg_per_ha,
        'input_kgN_ha': sum_flows(df, SM_IN_FULL, years) * kt_to_kg_per_ha,
    })


NOX_FLOWS_ALL_POOLS = [
    'AG.MM-AT.AT-Emissions-NOx', 'AG.SM-AT.AT-Emissions-NOx',
    'EF.EC-AT.AT-Emissions-NOx', 'EF.IC-AT.AT-Emissions-NOx', 'EF.OE-AT.AT-Emissions-NOx', 'EF.TR-AT.AT-Emissions-NOx',
    'MP.OP-AT.AT-Emissions-NOx', 'PR.SO-AT.AT-Emissions-NOx',
]


def nox_emissions_per_capita(years=ANALYSIS_YEARS):
    """Total national NOx emissions (summed across every pool that reports an
    '-AT.AT-Emissions-NOx' flow), in grams of N per person per year. This is
    the nitrogen-equivalent mass tracked throughout the model, not the
    conventional kg-NOx (or NO2-equivalent) per capita figure used in
    emissions-reporting contexts - divide by NOx_to_N_factor to convert to a
    NOx-mass basis if a directly comparable figure is needed."""
    from data_loader import load_all_data
    preloaded = load_all_data({'mp'})
    pop = preloaded['ssb_06913']['Befolkning 1. januar']

    df = load_stats()
    total_nox_kt = sum_flows(df, NOX_FLOWS_ALL_POOLS, years)
    return total_nox_kt * 1.0e9 / pop.reindex(years)  # kt N -> g N, / population


# =============================================================================
# Report
# =============================================================================

def _print_series_summary(label, series, years=ANALYSIS_YEARS):
    years = list(years)
    trend = trend_report(years, series.values, years[0], years[-1])
    avg_start = series.loc[years[0]:years[0] + 2].mean()
    avg_end = series.loc[years[-1] - 2:years[-1]].mean()
    print(f"\n{label}")
    print(f"  {years[0]}-{years[0]+2} avg: {avg_start:.2f}   {years[-1]-2}-{years[-1]} avg: {avg_end:.2f}")
    print(f"  Theil-Sen: {trend['sen_slope_per_year']:.4f}/yr  "
          f"(fit {years[0]}: {trend['fit_start']:.2f} -> fit {years[-1]}: {trend['fit_end']:.2f}, "
          f"{trend['pct_change']:+.1f}%)")
    print(f"  Mann-Kendall: Z={trend['mk_Z']:.3f}  p={trend['mk_p']:.5f}")


def main():
    df = load_stats()
    years = list(ANALYSIS_YEARS)

    print("=" * 78)
    print("NUE and AG mass-balance report")
    print(f"Source: {STATS_FILE}   Years: {years[0]}-{years[-1]}")
    print("=" * 78)

    _print_series_summary("Q1a: AG whole NUE (%), external flows only", q1a_ag_whole_nue(df))
    _print_series_summary("Q1b: AG.MM alone NUE (%)", q1b_ag_mm_nue(df))
    _print_series_summary("Q1c: AG.SM alone NUE (%)", q1c_ag_sm_nue(df))

    naive_nue, corrected_nue = q2_corrected_ag_whole_nue(df)
    _print_series_summary("Q2: naive AG-whole NUE (%) (= Q1a, repeated for comparison)", naive_nue)
    _print_series_summary("Q2: corrected AG-whole NUE (%) (imported feed at domestic-equivalent N-cost)", corrected_nue)
    _print_series_summary("Q2 (context): poultry+turkey+pork share of Animal products N (%)", poultry_pork_share_of_animal_products())

    _print_series_summary("Q3: food-system NUE (%), land-based, excl. aquaculture", q3_food_system_nue(df))
    _print_series_summary("Q3 (comparison): food-system NUE (%), incl. wild catch and aquaculture", q3_food_system_nue_incl_fish(df))

    _print_series_summary("AG.MM full mass balance (kt N/yr, in - out)", ag_mm_balance(df))
    _print_series_summary("AG.SM full mass balance (kt N/yr, in - out)", ag_sm_balance(df))
    _print_series_summary("AG total mass balance (kt N/yr, MM + SM)", ag_total_balance(df))

    per_ha = ag_per_hectare(df)
    _print_series_summary(f"AG leaching per hectare (kg N/ha/yr, area={AGRICULTURAL_AREA_HA:,} ha)", per_ha['leaching_kgN_ha'])
    _print_series_summary(f"AG atmospheric losses per hectare (kg N/ha/yr, area={AGRICULTURAL_AREA_HA:,} ha)", per_ha['atmospheric_kgN_ha'])
    _print_series_summary(f"AG soil N input per hectare (kg N/ha/yr, area={AGRICULTURAL_AREA_HA:,} ha)", per_ha['input_kgN_ha'])

    _print_series_summary("National NOx emissions per capita (g N/person/yr)", nox_emissions_per_capita())

    print("\n" + "=" * 78)


if __name__ == '__main__':
    main()
