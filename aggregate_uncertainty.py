#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
What drives the uncertainty of balances, national totals, NUE indicators and
residual flows: which flows (analysis A) and which uncertainty sources
(analysis B).

Each quantity is analysed for its level (average 2022-2024) and its change
(average 2022-2024 minus average 1990-1992).

A, flows: from the raw Monte Carlo (MC_Raw_Simulations.csv.gz). The quantity
is linearised around the central run, Q ~ sum_i g_i F_i (g_i = +1/-1 for a
balance or sum, the partial derivative for a ratio), and the variance of the
quantity Y (level or change) is split exactly as

    Var(Y) = sum_i Cov(g_i F_i, Y) + Cov(remainder, Y)

so the shares add up to 1. Correlated flows (shared parameters and data sets,
flows derived from each other) share the variance between them; a negative
share means the flow dampens the uncertainty of Y. The remainder is the part
of Y that the linear sum over flows does not capture: non-linearity of a
ratio, and for a residual flow the terms of its mass balance that are not
flows themselves.

B, sources: from the elasticities of the first-order sensitivity analysis
(MC_uncertainty_elasticities.csv.gz, uncertainty_contributions.py). A one
standard deviation change in a source changes flow i in year y by
F_iy * e_iy * sigma_y, and Q by z_y = sum_i g_iy F_iy e_iy sigma_y. A source
drawn once for all years contributes (sum_y w_y z_y)^2 to Var(Y), a source
drawn per year sum_y (w_y z_y)^2, with w_y the weights of the years in Y.
Shares are taken over all sources; first-order, so indicative for residuals
close to zero and strongly skewed sources.

Run after main_mc.py --export-raw-mc --uncertainty-contributions (both files
must come from the same model version). Writes
output_files/MC_aggregate_summary.csv (central value and MC interval per
quantity) and output_files/MC_aggregate_contributions.csv (shares), for the
article (not shown in the report).
"""
import os

import numpy as np
import pandas as pd

import calculations_for_article as cfa

RAW_FILE = cfa.RAW_FILE
ELASTICITY_FILE = 'output_files/MC_uncertainty_elasticities.csv.gz'
SOURCES_FILE = 'output_files/MC_uncertainty_contributions.csv'
SUMMARY_FILE = 'output_files/MC_aggregate_summary.csv'
CONTRIBUTIONS_FILE = 'output_files/MC_aggregate_contributions.csv'

YEARS = list(cfa.ANALYSIS_YEARS)
START = (1990, 1992)
END = (2022, 2024)
GRADIENT_STEP = 1e-3  # kt N, added to one flow to get the partial derivative

# HY.AC is left out: its outflows are computed from its inflows, so its
# balance is zero in every iteration.
POOL_CODES = ['EF', 'EF.EC', 'EF.IC', 'EF.OE', 'EF.TR', 'MP', 'MP.FP', 'MP.OP', 'AG', 'AG.MM', 'AG.SM',
              'FS', 'FS.FO', 'FS.OL', 'PR', 'PR.SO', 'PR.WW', 'HS', 'AT', 'HY', 'HY.CW', 'HY.SW', 'RW']
BOUNDARY_SUBPOOLS = ('AT.AT', 'HY.CW', 'RW.RW')

CONSUMER_GOODS = 'MP.OP-HS.HS-Consumer goods-Nmix'
# The mass balance Consumer goods is the residual of (mp_mc.py,
# _add_consumer_goods_mc). The fertilizer-industry terms left out there are
# not flows and end up in the remainder.
CONSUMER_GOODS_IN = [
    'AG.SM-MP.OP-Crop products for industrial use-Nmix',
    'AG.MM-MP.OP-Non-edible animal products-Nmix',
    'PR.SO-MP.OP-Recycling-Nmix',
    'EF.EC-MP.OP-Fuel used as feedstock-Nmix',
    'FS.FO-MP.OP-Industrial round wood-Nmix',
    'RW.RW-MP.OP-Other goods import -Nmix',
]
CONSUMER_GOODS_OUT = [
    'MP.OP-PR.SO-Other industry waste-Nmix',
    'MP.OP-PR.WW-Other industry wastewater-Nmix',
    'MP.OP-HY.SW-Untreated wastewater-Nmix',
    'MP.OP-RW.RW-Other goods export-Nmix',
    'MP.OP-EF.IC-Industrial waste fuels-Nmix',
]


def _ends(f):
    parts = f.split('-')
    return parts[0], parts[1]


def _select(df, rule):
    return [f for f in cfa.flow_names(df) if rule(*_ends(f), f)]


def losses_to_air(species):
    return lambda df: cfa.sum_flows(df, _select(
        df, lambda s, t, f: t == 'AT.AT' and s != 'RW.RW' and f.endswith(f'-Emissions-{species}')), YEARS)


def inflows(code):
    """Everything that ends up in a subpool: all its inflows, including
    deposition and N2 fixation."""
    return lambda df: cfa.sum_flows(df, cfa._pool_flows(df, code, 'in'), YEARS)


def imports(include_atmosphere):
    return lambda df: cfa.sum_flows(df, _select(
        df, lambda s, t, f: s == 'RW.RW' and (include_atmosphere or t != 'AT.AT')), YEARS)


def exports(include_atmosphere):
    return lambda df: cfa.sum_flows(df, _select(
        df, lambda s, t, f: t == 'RW.RW' and (include_atmosphere or s != 'AT.AT')), YEARS)


def national_balance(df):
    """Inflows minus outflows across the boundary of the economy (AT.AT,
    HY.CW, RW.RW), as article_numbers.national_balance."""
    inside = lambda c: c in BOUNDARY_SUBPOOLS
    inflows = _select(df, lambda s, t, f: inside(s) and not inside(t))
    outflows = _select(df, lambda s, t, f: inside(t) and not inside(s))
    return cfa.sum_flows(df, inflows, YEARS) - cfa.sum_flows(df, outflows, YEARS)


def consumer_goods_components(df):
    return cfa.sum_flows(df, CONSUMER_GOODS_IN, YEARS) - cfa.sum_flows(df, CONSUMER_GOODS_OUT, YEARS)


def _quantity(qid, label, unit, fn, a_fn=None):
    """a_fn: the linear form used for analysis A when fn itself is a single
    flow (a residual), so that the flows it is built from get the shares."""
    return {'id': qid, 'label': label, 'unit': unit, 'fn': fn, 'a_fn': a_fn or fn}


QUANTITIES = (
    [_quantity('national_balance', 'Balance of the economy (towards AT.AT, HY.CW and RW.RW)', 'kt N/yr',
               national_balance),
     _quantity('losses_air_NH3', 'Emissions of NH3', 'kt N/yr', losses_to_air('NH3')),
     _quantity('losses_air_NOx', 'Emissions of NOx', 'kt N/yr', losses_to_air('NOx')),
     _quantity('losses_air_N2O', 'Emissions of N2O', 'kt N/yr', losses_to_air('N2O')),
     _quantity('inflow_HY.SW', 'All inflows to surface water (HY.SW)', 'kt N/yr', inflows('HY.SW')),
     _quantity('inflow_HY.CW', 'All inflows to coastal water (HY.CW)', 'kt N/yr', inflows('HY.CW')),
     _quantity('imports', 'Imports (excluding atmospheric inflow)', 'kt N/yr', imports(False)),
     _quantity('imports_incl_atm', 'Imports including atmospheric inflow', 'kt N/yr', imports(True)),
     _quantity('exports', 'Exports (excluding atmospheric outflow)', 'kt N/yr', exports(False)),
     _quantity('exports_incl_atm', 'Exports including atmospheric outflow', 'kt N/yr', exports(True)),
     _quantity('nue_q3', 'Food-system NUE, land-based', '%', cfa.q3_food_system_nue),
     _quantity('nue_q3_fish', 'Food-system NUE including fish', '%', cfa.q3_food_system_nue_incl_fish),
     _quantity('nue_q1a', 'Agriculture NUE (AG as a whole)', '%', cfa.q1a_ag_whole_nue),
     _quantity('nue_q2', 'Agriculture NUE corrected for feed import', '%',
               lambda df: cfa.q2_corrected_ag_whole_nue(df, YEARS)[1]),
     _quantity('nue_q1b', 'Manure management NUE (AG.MM)', '%', cfa.q1b_ag_mm_nue),
     _quantity('nue_q1c', 'Soil management NUE (AG.SM)', '%', cfa.q1c_ag_sm_nue),
     _quantity('consumer_goods', 'Consumer goods (residual of MP.OP)', 'kt N/yr',
               lambda df: cfa.flow_series(df, CONSUMER_GOODS, YEARS), consumer_goods_components)]
    + [_quantity(f'balance_{code}', f'Balance of {code}', 'kt N/yr',
                 lambda df, c=code: cfa.pool_balance(df, c, YEARS)) for code in POOL_CODES]
)

METRICS = {'level': {y: 1 / 3 for y in range(END[0], END[1] + 1)},
           'change': {**{y: -1 / 3 for y in range(START[0], START[1] + 1)},
                      **{y: 1 / 3 for y in range(END[0], END[1] + 1)}}}


def _weights(metric):
    return np.array([METRICS[metric].get(y, 0.0) for y in YEARS])


def _central_frame():
    df = cfa.load_stats()
    return df[df['year'].isin(YEARS)][['flow_name', 'year', 'central']].reset_index(drop=True)


def _evaluate(fn, df):
    out = fn(df).reindex(YEARS).to_numpy(dtype=float)
    cfa._FLOW_INDEX.clear()
    return out


def gradient(fn, central, flows):
    """Partial derivative of fn (per year) with respect to every flow, at the
    central values: flows x years."""
    base = _evaluate(fn, central)
    g = np.zeros((len(flows), len(YEARS)))
    for i, f in enumerate(flows):
        bumped = central.copy()
        bumped.loc[bumped['flow_name'] == f, 'central'] += GRADIENT_STEP
        g[i] = (_evaluate(fn, bumped) - base) / GRADIENT_STEP
    g[np.abs(g) < 1e-9] = 0.0
    return base, g


def _raw_array(flows):
    """Raw MC values as sims x flows x years (NaN, i.e. 'not done', as 0 as
    in cfa.sum_flows), sim_id 0 left out. Also the per-iteration frames for
    evaluating the quantities themselves."""
    sims = cfa.load_raw_simulations(YEARS, all_flows=True)
    arr = np.zeros((len(sims), len(flows), len(YEARS)))
    row = {f: i for i, f in enumerate(flows)}
    col = {y: j for j, y in enumerate(YEARS)}
    for k, sim in enumerate(sims):
        r = sim['flow_name'].map(row).to_numpy()
        c = sim['year'].map(col).to_numpy()
        arr[k, r, c] = np.nan_to_num(sim['central'].to_numpy(dtype=float))
    return arr, sims


def flow_contributions(g, raw, exact, w):
    """Analysis A: share of Var(Y) per flow and for the remainder, Y = sum_y
    w_y Q_y per iteration (exact: Q from the quantity function itself)."""
    y = exact @ w
    parts = np.einsum('fy,sfy,y->sf', g, raw, w)
    remainder = y - parts.sum(axis=1)
    var = np.var(y)
    yc = y - y.mean()
    share = ((parts - parts.mean(axis=0)) * yc[:, None]).mean(axis=0) / var
    rem_share = ((remainder - remainder.mean()) * yc).mean() / var
    return share, rem_share


def source_contributions(g, elast, w):
    """Analysis B: share of Var(Y) per source, and the first-order standard
    deviation of Y. elast: dict source_id -> (flows x years array of
    F * e * sigma, annual)."""
    variances = {}
    for sid, (dF, annual) in elast.items():
        z = (g * dF).sum(axis=0) * w
        variances[sid] = float((z ** 2).sum() if annual else z.sum() ** 2)
    total = sum(variances.values())
    return {k: v / total for k, v in variances.items() if v > 0}, np.sqrt(total)


def _elasticity_arrays(flows, central_array):
    el = pd.read_csv(ELASTICITY_FILE)
    row = {f: i for i, f in enumerate(flows)}
    col = {y: j for j, y in enumerate(YEARS)}
    el = el[el['year'].isin(YEARS) & el['flow_name'].isin(row)]
    out = {}
    for sid, g in el.groupby('source_id'):
        a = np.zeros((len(flows), len(YEARS)))
        r = g['flow_name'].map(row).to_numpy()
        c = g['year'].map(col).to_numpy()
        a[r, c] = central_array[r, c] * g['elasticity'].to_numpy() * g['rel_sd'].fillna(0.0).to_numpy()
        out[sid] = (a, bool(g['annual'].iloc[0]))
    return out


def compute():
    for path in (ELASTICITY_FILE, SOURCES_FILE):
        gap = os.path.getmtime(path) - os.path.getmtime(cfa.STATS_FILE)
        if gap < 0:
            raise RuntimeError(f"{path} is older than {cfa.STATS_FILE}; rerun the sensitivity analysis.")
    central = _central_frame()
    flows = sorted(central['flow_name'].unique())
    central_array = np.zeros((len(flows), len(YEARS)))
    row = {f: i for i, f in enumerate(flows)}
    central_array[central['flow_name'].map(row), central['year'].map({y: j for j, y in enumerate(YEARS)})] = \
        np.nan_to_num(central['central'].to_numpy(dtype=float))

    print("[AGGREGAT] Leser rå MC...")
    raw, sims = _raw_array(flows)
    print("[AGGREGAT] Leser elastisiteter...")
    elast = _elasticity_arrays(flows, central_array)
    names = pd.read_csv(SOURCES_FILE).drop_duplicates('source_id').set_index('source_id')

    summary, rows = [], []
    for q in QUANTITIES:
        print(f"[AGGREGAT]   {q['id']}")
        base, g = gradient(q['fn'], central, flows)
        _, g_a = gradient(q['a_fn'], central, flows) if q['a_fn'] is not q['fn'] else (base, g)
        exact = np.array([_evaluate(q['fn'], s) for s in sims])
        for metric in METRICS:
            w = _weights(metric)
            y = exact @ w
            b_share, b_sd = source_contributions(g, elast, w)
            summary.append({'quantity': q['id'], 'label': q['label'], 'unit': q['unit'],
                            'metric': metric, 'central': float(base @ w),
                            'p2_5': float(np.percentile(y, 2.5)), 'p97_5': float(np.percentile(y, 97.5)),
                            'mc_sd': float(np.std(y)), 'first_order_sd': b_sd})
            a_share, rem = flow_contributions(g_a, raw, exact, w)
            for i, s in enumerate(a_share):
                if g_a[i].any():
                    rows.append((q['id'], metric, 'flow', flows[i], flows[i], '', s))
            rows.append((q['id'], metric, 'flow', 'remainder', 'Remainder', '', rem))
            for sid, s in b_share.items():
                rows.append((q['id'], metric, 'source', sid, names.loc[sid, 'source'], names.loc[sid, 'type'], s))
    contributions = pd.DataFrame(rows, columns=['quantity', 'metric', 'analysis', 'item_id', 'item', 'type', 'share'])
    return pd.DataFrame(summary), contributions


def write(summary, contributions):
    summary.to_csv(SUMMARY_FILE, index=False)
    contributions.to_csv(CONTRIBUTIONS_FILE, index=False)
    print(f"[AGGREGAT] Skrevet {SUMMARY_FILE} og {CONTRIBUTIONS_FILE} ({len(contributions)} rader)")


if __name__ == '__main__':
    write(*compute())
