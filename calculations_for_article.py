#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
All calculations on the model output that the article needs, collected in
one place: nitrogen use efficiency (NUE) at several system boundaries, AG
mass balances, per-hectare and per-capita figures, each with trend
statistics. Reads output_files/MC_Reporting_Statistics.xlsx and
output_files/MC_Raw_Simulations.csv.gz (both produced by main_mc.py).
The methods and current results are documented in
claude_tekst/2026-09-25_calculations_for_article_metodenotat.md.

Run directly to print a full report to stdout:

    python3 calculations_for_article.py

Re-run whenever the underlying model output changes (i.e. after any
main_mc.py run that regenerates MC_Reporting_Statistics.xlsx) to refresh the
numbers used in the article.

Each series is reported twice over:
- from the run's median values (MC_Reporting_Statistics.xlsx), with a
  Mann-Kendall p-value and a Theil-Sen slope with its 95 % confidence
  interval. These describe how well the trend is determined given the
  year-to-year scatter of the median series only.
- from every individual MC iteration (MC_Raw_Simulations.csv.gz), recomputing
  the same series and Theil-Sen trend within each simulation and reporting
  the 2.5-97.5 percentile range. This carries the model's own parameter and
  data uncertainty into the trend. Much of that uncertainty is systematic
  (the same perturbed parameter applies to every year of a simulation), so
  it is strongly correlated between years - a trend interval built from
  per-year +/-1 sigma values would overstate it, which is why the trend is
  computed per iteration instead. Since the true error structure lies
  between fully correlated and fully independent between years, the trend
  is also recomputed with years drawn independently from different
  iterations, and the two intervals are reported together as bounds.

MC_Raw_Simulations.csv.gz is only written when main_mc.py is run with
--export-raw-mc, so run it as `main_mc.py --pool all --nsim 1000
--export-raw-mc` before this script.
"""

import functools
import itertools
import os
from math import erf, sqrt

import numpy as np
import pandas as pd

STATS_FILE = 'output_files/MC_Reporting_Statistics.xlsx'
RAW_FILE = 'output_files/MC_Raw_Simulations.csv.gz'
Z_95 = 1.959964  # two-sided 95 % standard normal quantile
MC_RESAMPLE_SEED = 20260925  # fixed seed so variant (ii) resampling is reproducible
ANALYSIS_YEARS = range(1990, 2025)  # the only years with complete flow coverage for all pools


# =============================================================================
# Trend statistics: Mann-Kendall significance test + Theil-Sen slope estimator
# =============================================================================
# Implemented from scratch (no scipy/pymannkendall available in this
# environment). Standard WMO/IPCC-style non-parametric trend methodology:
# Mann-Kendall for significance (robust to non-normal residuals and outliers),
# Theil-Sen for the slope (median of all pairwise slopes, robust to outliers).

def _mann_kendall_variance(values):
    """Variance of the Mann-Kendall S statistic, with the standard tie
    correction."""
    n = len(values)
    _, counts = np.unique(values, return_counts=True)
    tie_term = np.sum(counts * (counts - 1) * (2 * counts + 5))
    return (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0


def mann_kendall(values):
    """Returns (S, Z, p_value) for the two-sided Mann-Kendall trend test."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    S = sum(np.sign(values[j] - values[i]) for i, j in itertools.combinations(range(n), 2))
    var_S = _mann_kendall_variance(values)

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


def theil_sen_ci(years, values, z=Z_95):
    """Non-parametric confidence interval for the Theil-Sen slope (Hollander
    & Wolfe 1973, as given in Gilbert 1987, section 16.5): with N ordered
    pairwise slopes and C = z * sqrt(Var(S)) from the Mann-Kendall
    variance, the bounds are the M1-th and (M2+1)-th slopes,
    M1 = (N - C) / 2 and M2 = (N + C) / 2."""
    years = np.asarray(years, dtype=float)
    values = np.asarray(values, dtype=float)
    n = len(values)
    slopes = np.sort([
        (values[j] - values[i]) / (years[j] - years[i])
        for i, j in itertools.combinations(range(n), 2)
        if years[j] != years[i]
    ])
    c = z * sqrt(_mann_kendall_variance(values))
    m1 = int(round((len(slopes) - c) / 2))
    m2 = int(round((len(slopes) + c) / 2))
    return slopes[m1 - 1], slopes[m2]


def trend_report(years, values, start_year, end_year):
    """Runs Mann-Kendall + Theil-Sen on a (years, values) series and returns a
    dict with the fitted start/end values, percent change between them (via
    the Theil-Sen fit, not the raw endpoints), and the Mann-Kendall p-value."""
    S, Z, p_value = mann_kendall(values)
    slope, intercept = theil_sen(years, values)
    fit_start = intercept + slope * start_year
    fit_end = intercept + slope * end_year
    pct_change = 100 * (fit_end - fit_start) / abs(fit_start) if fit_start != 0 else float('nan')
    # The slope's confidence bounds are expressed as percent change over the
    # same fitted start value, so they are directly comparable to pct_change.
    slope_lo, slope_hi = theil_sen_ci(years, values)
    span = end_year - start_year
    return {
        'sen_slope_per_year': slope,
        'sen_slope_lo': slope_lo,
        'sen_slope_hi': slope_hi,
        'pct_change_lo': 100 * slope_lo * span / abs(fit_start),
        'pct_change_hi': 100 * slope_hi * span / abs(fit_start),
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


@functools.lru_cache(maxsize=None)
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


# Inputs and outputs of Q1c, one row each, for the decomposition table.
AG_SM_NUE_COMPONENTS = [
    ('Mineral fertilizer', 'in', FERTILIZER_SM),
    ('Manure application', 'in', MANURE_APPLICATION),
    ('Deposition', 'in', DEPOSITION_SM),
    ('Biological N2 fixation', 'in', BNF_SM),
    ('Fodder crops', 'out', FODDER_CROPS),
    ('Food crop products', 'out', FOOD_CROP_PRODUCTS),
    ('Crop products for industrial use', 'out', INDUSTRIAL_CROP_PRODUCTS),
]


def ag_sm_nue_decomposition(df, years=ANALYSIS_YEARS):
    """Start/end period averages and 1990-2024 trend (median series) for each
    input and output of Q1c, plus the input and output totals, to show which
    flows drive the AG.SM NUE trend."""
    years = list(years)
    rows = []
    groups = [(name, side, flows) for name, side, flows in AG_SM_NUE_COMPONENTS]
    for side in ('in', 'out'):
        groups.append((f"Total {side}puts", side, [f for _, sd, fl in AG_SM_NUE_COMPONENTS if sd == side for f in fl]))
    for name, side, flows in groups:
        s = sum_flows(df, flows, years)
        rows.append({'component': name, 'side': side,
                     'avg_start': s.loc[years[0]:years[0] + 2].mean(),
                     'avg_end': s.loc[years[-1] - 2:years[-1]].mean(),
                     **trend_report(years, s.values, years[0], years[-1])})
    return pd.DataFrame(rows)


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


def ag_losses_total(df, years=ANALYSIS_YEARS):
    """All N losses from agriculture (kt N/yr): NH3, N2O, NOx and N2
    (denitrification) to the atmosphere plus leaching to water, from both
    AG.MM and AG.SM."""
    return sum_flows(df, AG_ATMOSPHERIC_LOSSES + AG_LEACHING, years)


def fodder_loss_to_close_mm(df, years=ANALYSIS_YEARS):
    """Share of Fodder crops (%) that would have to be lost between field and
    feed trough for the AG.MM balance to be zero. A loss L removes L x Fodder
    crops from MM's input and SM's output at the same time, so the AG total
    balance is unchanged; it only moves surplus from MM to SM. Fodder crops
    includes innmark grazing, where silage losses do not apply, so the share
    of harvested fodder alone would be higher."""
    return 100 * ag_mm_balance(df, years) / sum_flows(df, FODDER_CROPS, years)


def fodder_loss_to_close_sm(df, years=ANALYSIS_YEARS):
    """Share of Fodder crops (%) that would have to be lost for the AG.SM
    balance to be zero (see fodder_loss_to_close_mm)."""
    return -100 * ag_sm_balance(df, years) / sum_flows(df, FODDER_CROPS, years)


# =============================================================================
# Per-hectare and per-capita normalisations
# =============================================================================

# NIBIO's agricultural area figure, the same one used to derive
# denitrification_AG_N2 in N_parameters.xlsx (14 kg N/ha German default x
# this area). A single recent-vintage value, not a historical time series -
# this project does not currently load a yearly agricultural-area dataset, so
# it is treated as constant across all years. Revisit if a proper time series
# becomes available, since Norway's agricultural area has drifted over 1990-2024.
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


@functools.lru_cache(maxsize=None)
def _population():
    """SSB table 06913, population on 1 January (loaded once per run)."""
    from data_loader import load_all_data
    preloaded = load_all_data({'mp'})
    return preloaded['ssb_06913']['Befolkning 1. januar']


def nox_emissions_per_capita(df, years=ANALYSIS_YEARS):
    """Total national NOx emissions (summed across every pool that reports an
    '-AT.AT-Emissions-NOx' flow), in grams of N per person per year. This is
    the nitrogen-equivalent mass tracked throughout the model, not the
    conventional kg-NOx (or NO2-equivalent) per capita figure used in
    emissions-reporting contexts - divide by NOx_to_N_factor to convert to a
    NOx-mass basis if a directly comparable figure is needed."""
    total_nox_kt = sum_flows(df, NOX_FLOWS_ALL_POOLS, years)
    return total_nox_kt * 1.0e9 / _population().reindex(years)  # kt N -> g N, / population


# =============================================================================
# Energy and fuels (EF) pool balance, ammonia import and fertilizer export
# =============================================================================

# Every flow crossing the EF pool boundary. The internal EF.EC -> EF.IC/EF.OE/
# EF.TR fuel transfers are left out, as in the pool balance plots
# (utils_stat.process_and_export_mc_results), since they cancel within EF.
EF_IN_FULL = [
    'FS.FO-EF.OE-Fuel wood for households-Nmix',
    'MP.OP-EF.IC-Industrial waste fuels-Nmix',
    'PR.SO-EF.EC-Waste to energy-Nmix',
    'RW.RW-EF.EC-Fuel import-Nmix',
    'RW.RW-EF.TR-Import of transport fuel-Nmix',
]
EF_OUT_FULL = [
    'EF.EC-AT.AT-Emissions-N2O', 'EF.EC-AT.AT-Emissions-NOx',
    'EF.IC-AT.AT-Emissions-N2O', 'EF.IC-AT.AT-Emissions-NH3', 'EF.IC-AT.AT-Emissions-NOx',
    'EF.OE-AT.AT-Emissions-N2O', 'EF.OE-AT.AT-Emissions-NH3', 'EF.OE-AT.AT-Emissions-NOx',
    'EF.TR-AT.AT-Emissions-N2O', 'EF.TR-AT.AT-Emissions-NH3', 'EF.TR-AT.AT-Emissions-NOx',
    'EF.EC-MP.OP-Fuel used as feedstock-Nmix',
    'EF.EC-RW.RW-Fuel export-Nmix',
    'EF.TR-RW.RW-Export of transport fuels-Nmix',
]
# The ammonia import flow name has a space before '-Nmix', exactly as defined
# in rw_mc.py.
AMMONIA_IMPORT = ['RW.RW-MP.OP-Ammonia import -Nmix']
FERTILIZER_EXPORT = ['MP.OP-RW.RW-Mineral fertilizer export-Nmix']


def ef_balance(df, years=ANALYSIS_YEARS):
    """Overall EF pool balance (kt N/yr): all inflows minus all outflows
    across the pool boundary."""
    return sum_flows(df, EF_IN_FULL, years) - sum_flows(df, EF_OUT_FULL, years)


def ammonia_import(df, years=ANALYSIS_YEARS):
    """Ammonia import (kt N/yr)."""
    return sum_flows(df, AMMONIA_IMPORT, years)


def fertilizer_export(df, years=ANALYSIS_YEARS):
    """Mineral fertilizer export (kt N/yr)."""
    return sum_flows(df, FERTILIZER_EXPORT, years)


# Every flow crossing the MP.FP (food processing) subpool boundary. There are
# no MP.FP <-> MP.OP transfers in the model.
MP_FP_IN_FULL = [
    'AG.MM-MP.FP-Animal products-Nmix',
    'AG.SM-MP.FP-Food crop products-Nmix',
    'HY.AC-MP.FP-Coastal fish and seafood-Nmix',
    'HY.CW-MP.FP-Fish (wild catch)-Nmix',
    'HY.CW-MP.FP-Shellfish-Nmix',
    'RW.RW-MP.FP-Food import-Nmix',
]
MP_FP_OUT_FULL = [
    'MP.FP-AG.MM-Farm animal feed-Nmix',
    'MP.FP-AG.SM-Seeds and planting material -Nmix',
    'MP.FP-HS.HS-Food products-Nmix',
    'MP.FP-HY.AC-Feed to coastal aquaculture-Nmix',
    'MP.FP-HY.SW-Untreated wastewater-Nmix',
    'MP.FP-PR.SO-Food industry waste-Nmix',
    'MP.FP-PR.WW-Food industry wastewater-Nmix',
    'MP.FP-RW.RW-Feed export-Nmix',
    'MP.FP-RW.RW-Food export-Nmix',
]


def mp_fp_balance(df, years=ANALYSIS_YEARS):
    """MP.FP subpool balance (kt N/yr): all inflows minus all outflows
    across the subpool boundary."""
    return sum_flows(df, MP_FP_IN_FULL, years) - sum_flows(df, MP_FP_OUT_FULL, years)


# Every flow crossing the PR.SO (solid waste) and PR.WW (wastewater) subpool
# boundaries. The PR.SO <-> PR.WW transfers (landfill leachate, sewage sludge
# to landfill) cross the subpool boundaries but cancel in the PR pool total.
# Landfilled N has no outflow of its own: it stays in PR.SO and shows up as
# a positive PR.SO balance.
PR_SO_IN_FULL = [
    'HS.HS-PR.SO-Household waste-Nmix',
    'MP.FP-PR.SO-Food industry waste-Nmix',
    'MP.OP-PR.SO-Other industry waste-Nmix',
    'PR.WW-PR.SO-Sewage sludge landfill-Nmix',
    'RW.RW-PR.SO-Solid waste import-Nmix',
]
PR_SO_OUT_FULL = [
    'PR.SO-AG.SM-Biologically treated organic waste-Nmix',
    'PR.SO-AT.AT-Emissions-N2O', 'PR.SO-AT.AT-Emissions-NH3', 'PR.SO-AT.AT-Emissions-NOx',
    'PR.SO-EF.EC-Waste to energy-Nmix',
    'PR.SO-HS.HS-Biologically treated organic waste-Nmix',
    'PR.SO-HY.SW-Leaching-Nmix',
    'PR.SO-MP.OP-Recycling-Nmix',
    'PR.SO-PR.WW-Wastewater from landfills-Nmix',
    'PR.SO-RW.RW-Export for recycling-Nmix',
    'PR.SO-RW.RW-Export for reuse-Nmix',
    'PR.SO-RW.RW-Solid waste export-Nmix',
]
PR_WW_IN_FULL = [
    'HS.HS-PR.WW-Municipal wastewater-Nmix',
    'MP.FP-PR.WW-Food industry wastewater-Nmix',
    'MP.OP-PR.WW-Other industry wastewater-Nmix',
    'PR.SO-PR.WW-Wastewater from landfills-Nmix',
]
PR_WW_OUT_FULL = [
    'PR.WW-AG.SM-Sewage sludge fertilizer-Nmix',
    'PR.WW-AT.AT-Emissions-N2',
    'PR.WW-AT.AT-Emissions-N2O',
    'PR.WW-HS.HS-Sewage sludge fertilizer-Nmix',
    'PR.WW-HY.CW-Treated wastewater discharge-Nmix',
    'PR.WW-PR.SO-Sewage sludge landfill-Nmix',
]
PR_INTERNAL = ['PR.SO-PR.WW-Wastewater from landfills-Nmix', 'PR.WW-PR.SO-Sewage sludge landfill-Nmix']
WASTE_TO_ENERGY = ['PR.SO-EF.EC-Waste to energy-Nmix']
RECYCLING_ALL = ['PR.SO-MP.OP-Recycling-Nmix', 'PR.SO-RW.RW-Export for recycling-Nmix',
                 'PR.SO-RW.RW-Export for reuse-Nmix']
WW_N2_REMOVAL = ['PR.WW-AT.AT-Emissions-N2']
WW_DISCHARGE = ['PR.WW-HY.CW-Treated wastewater discharge-Nmix']


def pr_so_balance(df, years=ANALYSIS_YEARS):
    """PR.SO balance (kt N/yr): inflows minus outflows. Mostly N going to
    landfill, which has no outflow of its own."""
    return sum_flows(df, PR_SO_IN_FULL, years) - sum_flows(df, PR_SO_OUT_FULL, years)


def pr_ww_balance(df, years=ANALYSIS_YEARS):
    """PR.WW balance (kt N/yr): inflows minus outflows."""
    return sum_flows(df, PR_WW_IN_FULL, years) - sum_flows(df, PR_WW_OUT_FULL, years)


def pr_balance(df, years=ANALYSIS_YEARS):
    """PR pool balance (kt N/yr), PR.SO + PR.WW; the internal transfers cancel."""
    return pr_so_balance(df, years) + pr_ww_balance(df, years)


def pr_inputs(df, years=ANALYSIS_YEARS):
    """All inflows to the PR pool from outside it (kt N/yr)."""
    return sum_flows(df, [f for f in PR_SO_IN_FULL + PR_WW_IN_FULL if f not in PR_INTERNAL], years)


def pr_outputs(df, years=ANALYSIS_YEARS):
    """All outflows from the PR pool to outside it (kt N/yr)."""
    return sum_flows(df, [f for f in PR_SO_OUT_FULL + PR_WW_OUT_FULL if f not in PR_INTERNAL], years)


def pr_so_inputs(df, years=ANALYSIS_YEARS):
    """All inflows to PR.SO (kt N/yr)."""
    return sum_flows(df, PR_SO_IN_FULL, years)


def waste_to_energy(df, years=ANALYSIS_YEARS):
    """Solid waste incinerated for energy (kt N/yr)."""
    return sum_flows(df, WASTE_TO_ENERGY, years)


def recycling_all(df, years=ANALYSIS_YEARS):
    """Recycling in Norway plus export for recycling and reuse (kt N/yr)."""
    return sum_flows(df, RECYCLING_ALL, years)


def pr_so_balance_share(df, years=ANALYSIS_YEARS):
    """PR.SO balance (mostly landfill) as a share of PR.SO inflows (%)."""
    return 100 * pr_so_balance(df, years) / pr_so_inputs(df, years)


def waste_to_energy_share(df, years=ANALYSIS_YEARS):
    """Waste to energy as a share of PR.SO inflows (%)."""
    return 100 * waste_to_energy(df, years) / pr_so_inputs(df, years)


def ww_n2_removal_share(df, years=ANALYSIS_YEARS):
    """N removed as N2 in wastewater treatment, as a share of N leaving
    treatment either as N2 or as treated discharge to coastal water (%)."""
    n2 = sum_flows(df, WW_N2_REMOVAL, years)
    return 100 * n2 / (n2 + sum_flows(df, WW_DISCHARGE, years))


# Every flow crossing the HS.HS pool boundary (HS has one subpool).
HS_IN_FULL = [
    'AT.AT-HS.HS-Deposition-OXN', 'AT.AT-HS.HS-Deposition-RDN',
    'MP.FP-HS.HS-Food products-Nmix',
    'MP.OP-HS.HS-Consumer goods-Nmix',
    'MP.OP-HS.HS-Mineral fertilizer-Nmix',
    'PR.SO-HS.HS-Biologically treated organic waste-Nmix',
    'PR.WW-HS.HS-Sewage sludge fertilizer-Nmix',
]
HS_OUT_FULL = [
    'HS.HS-AT.AT-Emissions-NH3',
    'HS.HS-AT.AT-LUC emissions-N2O',
    'HS.HS-HY.SW-Overland flow-Nmix',
    'HS.HS-PR.SO-Household waste-Nmix',
    'HS.HS-PR.WW-Municipal wastewater-Nmix',
]
HOUSEHOLD_WASTE = ['HS.HS-PR.SO-Household waste-Nmix']
MUNICIPAL_WASTEWATER = ['HS.HS-PR.WW-Municipal wastewater-Nmix']


def hs_balance(df, years=ANALYSIS_YEARS):
    """HS pool balance (kt N/yr): inflows minus outflows."""
    return sum_flows(df, HS_IN_FULL, years) - sum_flows(df, HS_OUT_FULL, years)


def hs_inputs(df, years=ANALYSIS_YEARS):
    """All inflows to HS (kt N/yr)."""
    return sum_flows(df, HS_IN_FULL, years)


def hs_outputs(df, years=ANALYSIS_YEARS):
    """All outflows from HS (kt N/yr)."""
    return sum_flows(df, HS_OUT_FULL, years)


def hs_food_and_consumer_goods_share(df, years=ANALYSIS_YEARS):
    """Food products + consumer goods as a share of HS inflows (%)."""
    return 100 * sum_flows(df, FOOD_PRODUCTS_CONSUMED + CONSUMER_GOODS, years) / hs_inputs(df, years)


def hs_waste_and_wastewater_share(df, years=ANALYSIS_YEARS):
    """Household waste + municipal wastewater as a share of HS outflows (%)."""
    return 100 * sum_flows(df, HOUSEHOLD_WASTE + MUNICIPAL_WASTEWATER, years) / hs_outputs(df, years)


def household_waste(df, years=ANALYSIS_YEARS):
    """Household and settlement waste (kt N/yr)."""
    return sum_flows(df, HOUSEHOLD_WASTE, years)


# Household waste (HS.HS-PR.SO) split by source sector. Rows and column
# offsets mirror shared_flow_calculations.find_household_waste exactly and
# must be kept in sync with it. Table 05282 (1995-2011) covers construction,
# services and households; table 10514 (2012-) also includes the energy and
# water/sewage/waste-management sectors. 1990-1994 is extrapolated from
# waste per person in find_household_waste and has no sector split.
HOUSEHOLD_WASTE_SECTORS = {
    'ssb_05282': {'first_year': 1995, 'last_year': 2011,
                  'sectors': {'Construction': 5, 'Services': 6, 'Households': 9},
                  'rows': {6: 'paper', 8: 'plastic', 11: 'wood', 12: 'textiles', 13: 'wet_organic',
                           16: 'other_materials', 17: 'hazardous', 18: 'contaminated_masses'}},
    'ssb_10514': {'first_year': 2012, 'last_year': 2024,
                  'sectors': {'Energy supply': 4, 'Water, sewage, waste': 5, 'Construction': 6,
                              'Services': 7, 'Households': 9},
                  'rows': {6: 'wet_organic', 7: 'park_garden', 8: 'wood', 10: 'paper', 16: 'plastic',
                           18: 'textiles', 21: 'hazardous', 22: 'mixed_waste', 23: 'other_materials',
                           24: 'contaminated_masses'}},
}


@functools.lru_cache(maxsize=None)
def _waste_tables():
    """SSB tables 05282 and 10514 (loaded once per run)."""
    from data_loader import load_all_data
    preloaded = load_all_data({'hs'})
    return preloaded['ssb_05282'], preloaded['ssb_10514']


def household_waste_by_sector(waste_N):
    """Household waste N (kt N/yr) per source sector and year, for a dict of
    N fractions per waste category (kg N/kg). Dataset noise is left out: it
    multiplies every sector equally and cancels in the shares."""
    tables = dict(zip(['ssb_05282', 'ssb_10514'], _waste_tables()))
    out = {}
    for key, spec in HOUSEHOLD_WASTE_SECTORS.items():
        d = tables[key]
        for col in range(1, d.shape[1]):
            label = str(d.iloc[3, col]).strip()
            if not label.replace('.0', '').isdigit():
                continue
            year = int(float(label))
            if not spec['first_year'] <= year <= spec['last_year']:
                continue
            out[year] = {sector: sum(float(d.iloc[row, col + offset]) * waste_N[cat]
                                     for row, cat in spec['rows'].items()) / 1000.0  # tonnes -> kt
                         for sector, offset in spec['sectors'].items()}
    return pd.DataFrame(out).T.sort_index().fillna(0.0)


def household_waste_sector_shares(n_draws=1000, seed=MC_RESAMPLE_SEED, years=(1995, 2011, 2012, 2023, 2024)):
    """Sector shares (%) of household waste N in the given years: the value
    with median N fractions, and the 2.5/50/97.5 percentiles over n_draws
    draws of the waste N fractions (waste_fractions sheet, same
    perturbation as main_mc.generate_mc_parameters_fast)."""
    from main_mc import _draw_perturbed_value
    wf = pd.read_excel('parameters/N_parameters.xlsx', sheet_name='waste_fractions')
    wf = wf.set_index('waste_category')
    base = household_waste_by_sector(wf['N_frac'].to_dict())
    base_share = 100 * base.div(base.sum(axis=1), axis=0).loc[list(years)]
    np.random.seed(seed)
    draws = []
    for _ in range(n_draws):
        waste_N = {cat: _draw_perturbed_value(r.N_frac, r.lower_bound, r.upper_bound, r.uncertainty_type, r.distribution_type)
                   for cat, r in wf.iterrows()}
        t = household_waste_by_sector(waste_N).loc[list(years)]
        draws.append(100 * t.div(t.sum(axis=1), axis=0))
    stacked = pd.concat(draws, keys=range(n_draws))
    q = stacked.groupby(level=1).quantile([0.025, 0.5, 0.975]).unstack()
    return base_share, q


# =============================================================================
# Consumer goods, food flows and per-capita values
# =============================================================================

# Consumer goods is the MP.OP residual (six inflows minus five outflows, with
# fertilizer-production intermediates removed from both trade terms), see
# mp_mc._add_consumer_goods_mc.
CONSUMER_GOODS = ['MP.OP-HS.HS-Consumer goods-Nmix']
FOOD_IMPORT = ['RW.RW-MP.FP-Food import-Nmix']


def consumer_goods(df, years=ANALYSIS_YEARS):
    """Consumer goods delivered to households (kt N/yr)."""
    return sum_flows(df, CONSUMER_GOODS, years)


def consumer_goods_per_capita(df, years=ANALYSIS_YEARS):
    """Consumer goods per person (kg N/person/yr), population on 1 January
    from SSB table 06913."""
    return consumer_goods(df, years) * 1.0e6 / _population().reindex(years)  # kt N -> kg N, / population


def food_import(df, years=ANALYSIS_YEARS):
    """Food import (kt N/yr)."""
    return sum_flows(df, FOOD_IMPORT, years)


def food_products_consumed(df, years=ANALYSIS_YEARS):
    """Food products to households (kt N/yr). mp_mc._add_food_products_mc
    builds this from SSB per-person intake/consumption surveys (tables 06376,
    10249, 13695) times population, plus pet food, so it follows population
    by construction and cannot reflect changes in food waste."""
    return sum_flows(df, FOOD_PRODUCTS_CONSUMED, years)


def food_products_per_capita(df, years=ANALYSIS_YEARS):
    """Food products to households per person (kg N/person/yr)."""
    return food_products_consumed(df, years) * 1.0e6 / _population().reindex(years)  # kt N -> kg N, / population


def food_export(df, years=ANALYSIS_YEARS):
    """Total food export including fish (kt N/yr)."""
    return sum_flows(df, FOOD_EXPORT_TOTAL, years)


# =============================================================================
# Per-iteration MC uncertainty
# =============================================================================

MC_FLOWS = sorted(set(
    FERTILIZER_SM + DEPOSITION_SM + BNF_SM + MANURE_APPLICATION + GRAZING_UTMARK + FODDER_CROPS
    + FARM_ANIMAL_FEED + FEED_IMPORT + FOOD_CROP_PRODUCTS + INDUSTRIAL_CROP_PRODUCTS + ANIMAL_PRODUCTS
    + NON_EDIBLE_ANIMAL_PRODUCTS + FOOD_PRODUCTS_CONSUMED + FOOD_EXPORT_TOTAL + WILD_CATCH + AQUACULTURE_FEED
    + MM_IN_FULL + MM_OUT_FULL + SM_IN_FULL + SM_OUT_FULL + AG_LEACHING + AG_ATMOSPHERIC_LOSSES
    + NOX_FLOWS_ALL_POOLS + EF_IN_FULL + EF_OUT_FULL + AMMONIA_IMPORT + FERTILIZER_EXPORT + CONSUMER_GOODS + FOOD_IMPORT
    + MP_FP_IN_FULL + MP_FP_OUT_FULL + HS_IN_FULL + HS_OUT_FULL + PR_SO_IN_FULL + PR_SO_OUT_FULL + PR_WW_IN_FULL + PR_WW_OUT_FULL
))


def load_raw_simulations(years=ANALYSIS_YEARS):
    """One small DataFrame per MC iteration, holding that iteration's value
    for every flow used here. The value goes in a 'median' column so every
    question function (which reads flow values via flow_series) runs
    unchanged on a single iteration.

    main_mc.py writes the raw file just before the statistics file in the
    same run, so a raw file much older than the statistics file comes from
    an earlier run and would silently mix two model versions."""
    age_gap = os.path.getmtime(STATS_FILE) - os.path.getmtime(RAW_FILE)
    if not 0 <= age_gap < 600:
        raise RuntimeError(
            f"{RAW_FILE} is not from the same main_mc.py run as {STATS_FILE} "
            f"(modified {age_gap / 3600:.1f} h apart). Rerun main_mc.py with --export-raw-mc."
        )
    raw = pd.read_csv(RAW_FILE, usecols=['flow_name', 'year', 'value', 'sim_id'])
    raw = raw[raw['flow_name'].isin(MC_FLOWS) & raw['year'].isin(list(years))]
    duplicated = raw.duplicated(['sim_id', 'flow_name', 'year']).sum()
    if duplicated:
        raise ValueError(f"{duplicated} duplicated (sim_id, flow_name, year) rows in {RAW_FILE}")
    raw = raw.rename(columns={'value': 'median'})
    return [g for _, g in raw.groupby('sim_id')]


def mc_series_matrix(series_fn, sims, years=ANALYSIS_YEARS):
    """One row per MC iteration, one column per year: the series recomputed
    from that iteration's own flow values."""
    return np.array([series_fn(sim_df).reindex(list(years)).values for sim_df in sims])


def _trend_percentiles(matrix, years):
    """Theil-Sen trend and period averages for every row of matrix (one time
    series per row). Returns the 2.5/50/97.5 percentiles of the start- and
    end-period averages, the slope and the percent change, plus the share of
    rows whose slope has the same sign as the median slope."""
    years = list(years)
    rows = []
    for values in matrix:
        slope, intercept = theil_sen(years, values)
        fit_start = intercept + slope * years[0]
        fit_end = intercept + slope * years[-1]
        rows.append({
            'avg_start': values[:3].mean(),
            'avg_end': values[-3:].mean(),
            'slope': slope,
            'pct_change': 100 * (fit_end - fit_start) / abs(fit_start),
        })
    res = pd.DataFrame(rows)
    q = res.quantile([0.025, 0.5, 0.975])
    same_sign = (np.sign(res['slope']) == np.sign(q.loc[0.5, 'slope'])).mean()
    return q, same_sign, len(res)


def mc_trend_interval(matrix, years=ANALYSIS_YEARS):
    """Variant (i), errors fully correlated in time: each MC iteration is one
    consistent time series, since every perturbed parameter and dataset noise
    factor applies to all years of that iteration."""
    return _trend_percentiles(matrix, years)


def mc_trend_interval_independent_years(matrix, years=ANALYSIS_YEARS, n_resamples=None, seed=MC_RESAMPLE_SEED):
    """Variant (ii), errors independent between years: each synthetic time
    series takes every year from a randomly drawn MC iteration, so a value
    for one year is combined with values for other years from other
    iterations. All flows within a year still come from the same iteration
    (the whole iteration's state that year is one data point). This is valid
    because every series here is computed year by year - its value for year
    t depends only on flows in year t.

    Together with variant (i) this brackets the trend uncertainty: the true
    error structure lies between fully correlated (systematic errors, e.g. a
    wrong N content applies to every year) and fully independent (random
    year-to-year errors, e.g. reporting errors in annual statistics)."""
    n_sims, n_years = matrix.shape
    rng = np.random.default_rng(seed)
    picks = rng.integers(0, n_sims, size=(n_resamples or n_sims, n_years))
    resampled = matrix[picks, np.arange(n_years)]
    return _trend_percentiles(resampled, years)


# =============================================================================
# Series reported for the article
# =============================================================================

# (key, label, series function of one DataFrame, MC interval available?)
# A series built partly from data outside the MC (FAOSTAT item-level
# production for the poultry/pork share) is reported without an MC interval.
# Q3's non-fish food export uses median trade N-factors (see
# food_export_excluding_fish), so its MC interval leaves out that small
# term's own uncertainty.
SERIES = [
    ('q1a', "Q1a: AG whole NUE (%), external flows only", q1a_ag_whole_nue, True),
    ('q1b', "Q1b: AG.MM alone NUE (%)", q1b_ag_mm_nue, True),
    ('q1c', "Q1c: AG.SM alone NUE (%)", q1c_ag_sm_nue, True),
    ('q2_naive', "Q2: naive AG-whole NUE (%) (= Q1a, repeated for comparison)", lambda d: q2_corrected_ag_whole_nue(d)[0], True),
    ('q2_corrected', "Q2: corrected AG-whole NUE (%) (imported feed at domestic-equivalent N-cost)", lambda d: q2_corrected_ag_whole_nue(d)[1], True),
    ('q2_poultry_pork_share', "Q2 (context): poultry+turkey+pork share of Animal products N (%)", lambda d: poultry_pork_share_of_animal_products(), False),
    ('q3', "Q3: food-system NUE (%), land-based, excl. aquaculture", q3_food_system_nue, True),
    ('q3_incl_fish', "Q3 (comparison): food-system NUE (%), incl. wild catch and aquaculture", q3_food_system_nue_incl_fish, True),
    ('balance_mm', "AG.MM full mass balance (kt N/yr, in - out)", ag_mm_balance, True),
    ('balance_sm', "AG.SM full mass balance (kt N/yr, in - out)", ag_sm_balance, True),
    ('balance_ag', "AG total mass balance (kt N/yr, MM + SM)", ag_total_balance, True),
    ('ag_losses', "AG total N losses (kt N/yr, NH3 + N2O + NOx + N2 + leaching)", ag_losses_total, True),
    ('fodder_loss_mm', "Fodder crops loss needed to close the AG.MM balance (% of Fodder crops)", fodder_loss_to_close_mm, True),
    ('fodder_loss_sm', "Fodder crops loss needed to close the AG.SM balance (% of Fodder crops)", fodder_loss_to_close_sm, True),
    ('leaching_per_ha', f"AG leaching per hectare (kg N/ha/yr, area={AGRICULTURAL_AREA_HA:,} ha)", lambda d: ag_per_hectare(d)['leaching_kgN_ha'], True),
    ('atmospheric_per_ha', f"AG atmospheric losses per hectare (kg N/ha/yr, area={AGRICULTURAL_AREA_HA:,} ha)", lambda d: ag_per_hectare(d)['atmospheric_kgN_ha'], True),
    ('input_per_ha', f"AG soil N input per hectare (kg N/ha/yr, area={AGRICULTURAL_AREA_HA:,} ha)", lambda d: ag_per_hectare(d)['input_kgN_ha'], True),
    ('nox_per_capita', "National NOx emissions per capita (g N/person/yr)", nox_emissions_per_capita, True),
    ('balance_ef', "EF overall mass balance (kt N/yr, in - out)", ef_balance, True),
    ('ammonia_import', "Ammonia import (kt N/yr)", ammonia_import, True),
    ('fertilizer_export', "Mineral fertilizer export (kt N/yr)", fertilizer_export, True),
    ('balance_mp_fp', "MP.FP subpool mass balance (kt N/yr, in - out)", mp_fp_balance, True),
    ('hs_inputs', "HS pool inputs (kt N/yr)", hs_inputs, True),
    ('hs_outputs', "HS pool outputs (kt N/yr)", hs_outputs, True),
    ('balance_hs', "HS pool mass balance (kt N/yr, in - out)", hs_balance, True),
    ('hs_food_cg_share', "Food products + consumer goods, share of HS inputs (%)", hs_food_and_consumer_goods_share, True),
    ('hs_waste_ww_share', "Household waste + municipal wastewater, share of HS outputs (%)", hs_waste_and_wastewater_share, True),
    ('household_waste', "Household and settlement waste (kt N/yr)", household_waste, True),
    ('pr_inputs', "PR pool inputs (kt N/yr)", pr_inputs, True),
    ('pr_outputs', "PR pool outputs (kt N/yr)", pr_outputs, True),
    ('balance_pr', "PR pool mass balance (kt N/yr, in - out)", pr_balance, True),
    ('balance_pr_so', "PR.SO subpool mass balance (kt N/yr, in - out; mostly landfill)", pr_so_balance, True),
    ('balance_pr_ww', "PR.WW subpool mass balance (kt N/yr, in - out)", pr_ww_balance, True),
    ('pr_so_balance_share', "PR.SO balance as share of PR.SO inputs (%)", pr_so_balance_share, True),
    ('waste_to_energy', "Waste to energy (kt N/yr)", waste_to_energy, True),
    ('waste_to_energy_share', "Waste to energy as share of PR.SO inputs (%)", waste_to_energy_share, True),
    ('recycling_all', "Recycling incl. export for recycling and reuse (kt N/yr)", recycling_all, True),
    ('ww_n2_removal_share', "N removed as N2 in wastewater treatment, share of N2 + treated discharge (%)", ww_n2_removal_share, True),
    ('consumer_goods', "Consumer goods to households (kt N/yr)", consumer_goods, True),
    ('consumer_goods_per_capita', "Consumer goods per capita (kg N/person/yr)", consumer_goods_per_capita, True),
    ('food_import', "Food import (kt N/yr)", food_import, True),
    ('food_products', "Food products to households (kt N/yr)", food_products_consumed, True),
    ('food_products_per_capita', "Food products to households per capita (kg N/person/yr)", food_products_per_capita, True),
    ('food_export', "Food export incl. fish (kt N/yr)", food_export, True),
]


def summarize_series(key, label, series_fn, mc, df, sims, years=ANALYSIS_YEARS):
    """All reported statistics for one series: the median series itself,
    its start/end period averages, the trend statistics from trend_report,
    and (if mc) the per-year MC percentiles and the MC percentiles under
    both error structures: variant (i)
    from mc_trend_interval and variant (ii) from
    mc_trend_interval_independent_years."""
    years = list(years)
    series = series_fn(df)
    result = {
        'key': key,
        'label': label,
        'series': series,
        'avg_start': series.loc[years[0]:years[0] + 2].mean(),
        'avg_end': series.loc[years[-1] - 2:years[-1]].mean(),
        'trend': trend_report(years, series.values, years[0], years[-1]),
        'mc': None,
        'mc_independent_years': None,
    }
    if mc:
        matrix = mc_series_matrix(series_fn, sims, years)
        q, same_sign, n_sims = mc_trend_interval(matrix, years)
        # Per-year 2.5 / 50 / 97.5 percentiles across iterations.
        year_q = np.nanpercentile(matrix, [2.5, 50, 97.5], axis=0)
        result['mc'] = {'quantiles': q, 'same_sign': same_sign, 'n_sims': n_sims,
                        'year_values': {y: tuple(year_q[:, i]) for i, y in enumerate(years)},
                        'matrix': matrix}
        q, same_sign, n_resamples = mc_trend_interval_independent_years(matrix, years)
        result['mc_independent_years'] = {'quantiles': q, 'same_sign': same_sign, 'n_resamples': n_resamples}
    return result


# Sub-periods for series whose 1990-2024 trend hides distinct phases. The
# boundaries are read off the median series: Consumer goods steps up in
# 1993-1995 and again around 2005; food export rises to 2000, is flat to
# 2006, rises to 2010 and is flat after; food products to households are
# flat until 2005.
SEGMENTS = {
    'consumer_goods': [(1990, 1995), (1995, 2004), (2005, 2024)],
    'consumer_goods_per_capita': [(1990, 1995), (1995, 2024), (2005, 2024)],
    'food_import': [(1990, 2010), (2010, 2024)],
    'food_products': [(1990, 2005), (2005, 2024)],
    'food_products_per_capita': [(1990, 2005), (2005, 2024)],
    'food_export': [(1990, 2000), (2000, 2006), (2006, 2010), (2010, 2024)],
}


# Period averages other than the standard 1990-1992 / 2022-2024 ones.
PERIOD_MEANS = {
    'ag_losses': [(1990, 1991)],
    'ww_n2_removal_share': [(2023, 2023)],
}


def period_mean_interval(result, start_year, end_year, years=ANALYSIS_YEARS, seed=MC_RESAMPLE_SEED):
    """Mean of the median series over start_year-end_year, with the
    2.5/50/97.5 percentiles of the same mean across MC iterations under
    variant (i) (each iteration's own years) and variant (ii) (each year
    drawn from a random iteration, as in mc_trend_interval_independent_years)."""
    years = list(years)
    cols = [years.index(y) for y in range(start_year, end_year + 1)]
    matrix = result['mc']['matrix'][:, cols]
    rng = np.random.default_rng(seed)
    picks = rng.integers(0, matrix.shape[0], size=matrix.shape)
    resampled = matrix[picks, np.arange(matrix.shape[1])]
    return {
        'median_series': result['series'].loc[start_year:end_year].mean(),
        'mc_i': tuple(np.percentile(matrix.mean(axis=1), [2.5, 50, 97.5])),
        'mc_ii': tuple(np.percentile(resampled.mean(axis=1), [2.5, 50, 97.5])),
    }


# Ratios between two single years, per MC iteration.
YEAR_RATIOS = {
    'household_waste': [(1990, 2017), (1995, 2017)],
}


def year_ratio_interval(result, start_year, end_year, years=ANALYSIS_YEARS):
    """end_year / start_year for the median series, and the 2.5/50/97.5
    percentiles of the same ratio across MC iterations (variant (i); each
    iteration's own two years)."""
    years = list(years)
    m = result['mc']['matrix']
    ratio = m[:, years.index(end_year)] / m[:, years.index(start_year)]
    return {
        'median_series': result['series'].loc[end_year] / result['series'].loc[start_year],
        'mc_i': tuple(np.percentile(ratio, [2.5, 50, 97.5])),
    }


def year_ratios(results, ratios=YEAR_RATIOS):
    """year_ratio_interval for every entry in YEAR_RATIOS."""
    by_key = {r['key']: r for r in results}
    return {(key, a, b): year_ratio_interval(by_key[key], a, b) for key, spans in ratios.items() for a, b in spans}


def period_means(results, periods=PERIOD_MEANS):
    """period_mean_interval for every entry in PERIOD_MEANS, keyed by
    (series key, start year, end year)."""
    by_key = {r['key']: r for r in results}
    return {(key, a, b): period_mean_interval(by_key[key], a, b)
            for key, spans in periods.items() for a, b in spans}


def segment_trends(results, segments=SEGMENTS):
    """trend_report on each sub-period of the median series, keyed by
    (series key, start year, end year)."""
    by_key = {r['key']: r['series'] for r in results}
    return {
        (key, a, b): trend_report(list(range(a, b + 1)), by_key[key].loc[a:b].values, a, b)
        for key, periods in segments.items() for a, b in periods
    }


def compute_all():
    """Summaries for every series in SERIES, in order."""
    df = load_stats()
    sims = load_raw_simulations()
    return [summarize_series(key, label, fn, mc, df, sims) for key, label, fn, mc in SERIES], len(sims)


# =============================================================================
# Report
# =============================================================================

def print_summary(result, years=ANALYSIS_YEARS):
    years = list(years)
    trend = result['trend']
    print(f"\n{result['label']}")
    print(f"  {years[0]}-{years[0]+2} avg: {result['avg_start']:.2f}   {years[-1]-2}-{years[-1]} avg: {result['avg_end']:.2f}")
    print(f"  Theil-Sen: {trend['sen_slope_per_year']:.4f}/yr "
          f"[95% CI {trend['sen_slope_lo']:.4f} to {trend['sen_slope_hi']:.4f}]  "
          f"(fit {years[0]}: {trend['fit_start']:.2f} -> fit {years[-1]}: {trend['fit_end']:.2f}, "
          f"{trend['pct_change']:+.1f}% [95% CI {trend['pct_change_lo']:+.1f} to {trend['pct_change_hi']:+.1f}%])")
    print(f"  Mann-Kendall: Z={trend['mk_Z']:.3f}  p={trend['mk_p']:.5f}")
    if result['mc'] is None:
        print("  MC interval: not available (series uses data outside the MC)")
        return
    q = result['mc']['quantiles']
    print(f"  MC ({result['mc']['n_sims']} iterations, 2.5-97.5 %): "
          f"{years[0]}-{years[0]+2} avg {q.loc[0.025, 'avg_start']:.2f} to {q.loc[0.975, 'avg_start']:.2f}   "
          f"{years[-1]-2}-{years[-1]} avg {q.loc[0.025, 'avg_end']:.2f} to {q.loc[0.975, 'avg_end']:.2f}")
    print(f"  MC trend (i), errors correlated in time: {q.loc[0.5, 'slope']:.4f}/yr [{q.loc[0.025, 'slope']:.4f} to {q.loc[0.975, 'slope']:.4f}], "
          f"{q.loc[0.5, 'pct_change']:+.1f}% [{q.loc[0.025, 'pct_change']:+.1f} to {q.loc[0.975, 'pct_change']:+.1f}%], "
          f"same sign as median trend in {100 * result['mc']['same_sign']:.1f}% of iterations")
    q = result['mc_independent_years']['quantiles']
    print(f"  MC trend (ii), errors independent between years: {q.loc[0.5, 'slope']:.4f}/yr [{q.loc[0.025, 'slope']:.4f} to {q.loc[0.975, 'slope']:.4f}], "
          f"{q.loc[0.5, 'pct_change']:+.1f}% [{q.loc[0.025, 'pct_change']:+.1f} to {q.loc[0.975, 'pct_change']:+.1f}%], "
          f"same sign as median trend in {100 * result['mc_independent_years']['same_sign']:.1f}% of resamples")


def main():
    results, n_sims = compute_all()
    years = list(ANALYSIS_YEARS)

    print("=" * 78)
    print("Calculations for the article: NUE, AG mass balances, per-hectare and per-capita figures")
    print(f"Source: {STATS_FILE} + {RAW_FILE} ({n_sims} iterations)   Years: {years[0]}-{years[-1]}")
    print("=" * 78)
    for result in results:
        print_summary(result)
    print("\nOther period averages")
    for (key, a, b), m in period_means(results).items():
        print(f"  {key} {a}-{b}: {m['median_series']:.2f}  MC (i) {m['mc_i'][1]:.2f} [{m['mc_i'][0]:.2f}, {m['mc_i'][2]:.2f}]"
              f"  MC (ii) {m['mc_ii'][1]:.2f} [{m['mc_ii'][0]:.2f}, {m['mc_ii'][2]:.2f}]")
    print("\nSub-period trends (median series)")
    for (key, a, b), trend in segment_trends(results).items():
        print(f"  {key} {a}-{b}: {trend['pct_change']:+.1f}% "
              f"[95% CI {trend['pct_change_lo']:+.1f} to {trend['pct_change_hi']:+.1f}]  MK p={trend['mk_p']:.4f}")
    print("\n" + "=" * 78)


if __name__ == '__main__':
    main()
