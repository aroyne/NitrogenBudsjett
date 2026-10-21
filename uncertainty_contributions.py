#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Which uncertainty sources drive the uncertainty of each flow, and how much.

A first-order sensitivity analysis around the central (deterministic) run:

1. A traced run records every input the model reads that has an uncertainty
   in the Monte Carlo: dataset factors (with their parts, e.g. one facility),
   CLRTAP inventory groups, parameters, N contents of waste and traded goods,
   and fill draws for filled years (with the distance to the nearest known
   year).
2. Each source is raised by 10 % on its own, and the relative change in every
   flow and year gives the elasticity e.
3. The source's relative standard deviation sigma comes from the sampler's
   own draws (the same distribution and width the Monte Carlo uses); for fill
   draws it is ln(1 + u(d))/1.96 with u(d) from the sheet fill_uncertainties.
4. The contribution to the variance is (e * sigma)^2; its share is taken per
   flow and year, and averaged over the years of a period.

The sources are drawn independently in the Monte Carlo, so the contributions
add up to first order. Non-linear effects are not included: residuals close
to zero (and cut at zero), strongly skewed sources and products of uncertain
factors. For those the shares are indicative.

Writes output_files/MC_uncertainty_contributions.csv, read by
report_generator.py for the "Uncertainty" section of each flow page, and the
elasticities per flow, year and source to
output_files/MC_uncertainty_elasticities.csv.gz, read by
aggregate_uncertainty.py for balances, national totals and NUE.
"""
import re

import numpy as np
import pandas as pd

from mc_sampler import MCSampler, DatasetNoise, STANDARD_SHEETS

STEP = 1.10
PERIODS = {'1990-1994': (1990, 1994), '2020-2024': (2020, 2024)}
NSIM_WIDTH = 4001
OUTPUT_FILE = 'output_files/MC_uncertainty_contributions.csv'
ELASTICITY_FILE = 'output_files/MC_uncertainty_elasticities.csv.gz'

TYPE_WORDS = {
    'R': 'Registered data',
    'R/M1': 'Registered data',
    'S': 'Survey or self-reported data',
    'M1': 'Inventory with published uncertainty',
    'M2': 'Modelled statistics',
    'A': 'Assumption',
}
FILL_WORDS = {
    'interpolation': 'Gap filling: interpolation',
    'carry': 'Gap filling: held constant or averaged',
    'extrapolation': 'Gap filling: extrapolation',
}


def _rel_sd(arr):
    return float(np.std(arr[1:]) / arr[0]) if arr[0] else float('nan')


def _width(row, is_ratio=True):
    """Uncertainty column text for a sheet row (95 % bounds, distribution)."""
    lo, hi = row['lower_bound'], row['upper_bound']
    dist = str(row['distribution_type']).replace('log-normal', 'lognormal')
    if str(row['uncertainty_type']).strip() == 'abs':
        text = f"{lo:g}–{hi:g}"
    elif lo == hi:
        text = f"±{hi:g} %"
    else:
        text = f"−{lo:g}/+{hi:g} %"
    if str(row.get('bounds', '')).strip() == 'minmax':
        text += ' (min–max)'
    return f"{text}, {dist}"


def _name(row, fallback):
    name = row.get('display_name') if hasattr(row, 'get') else None
    return str(name).strip() if isinstance(name, str) and name.strip() else fallback


def _sources(bp, sampler, wide, seen):
    """List of (source_id, display name, type, uncertainty text, sigma or None,
    bump) for every traced input with an uncertainty."""
    out = []
    ds = bp.get_table('dataset_uncertainties').set_index('dataset_name')
    for key, sub in sorted(seen['dataset'], key=str):
        if key.startswith('CRLTAP:'):
            continue
        row = ds.loc[key]
        type_code = str(row['uncertainty_source']).split(':')[0].split('(')[0].strip()
        type_code = type_code.replace('Type ', '').split(',')[0].strip()
        typ = 'Splice between data sources' if key.startswith('splice:') else TYPE_WORDS.get(type_code, type_code)
        width = _width(row) + (', drawn per year' if str(row['annual_draw']).strip() == 'yes' else '')
        name = _name(row, key) + (f" ({sub})" if sub is not None else '')
        out.append((f"dataset|{key}|{sub}", name, typ, width,
                    _rel_sd(wide.draws['dataset_uncertainties'][key]), ('dataset', key, sub)))

    cr = bp.get_table('crltap_uncertainties')
    groups = sorted({sampler.crltap_keys[k] for k, _ in seen['dataset'] if k.startswith('CRLTAP:')})
    for g in groups:
        grp, pol = g.split(':')
        row = cr[(cr['noise_group'].astype(str) == grp) & (cr['pollutant'] == pol)].iloc[0]
        out.append((f"crltap|{g}", _name(row, f"{pol} emissions, NFR {grp}"),
                    TYPE_WORDS['M1'], _width(row), _rel_sd(wide.draws['crltap_uncertainties'][g]), ('crltap', g)))

    for (kind, fid), years in sorted(seen['fill'].items()):
        label = re.sub(r'^[A-Z]{2}\.[A-Z]{2}-[A-Z]{2}\.[A-Z]{2}-[^:]*:', '', fid)
        out.append((f"fill|{fid}", f"{FILL_WORDS[kind].split(': ')[1].capitalize()} ({label})",
                    FILL_WORDS[kind], None, None, ('fill', kind, fid)))

    tables = {g: bp.get_table(g).set_index(idc) for g, idc, _, _ in STANDARD_SHEETS}
    prefix_of = {g: prefix for g, _, _, prefix in STANDARD_SHEETS}
    extra = {'animal_products': ('prod_', 'item', 'N content of animal product'),
             'protein_food_items': ('food_protein_', 'food_group', 'Protein content of food group')}
    for pid in sorted(seen['param']):
        group = next((g for g in tables if pid in wide.draws[g]), None)
        if group is None:
            for g, (prefix, _, text) in extra.items():
                if pid in wide.draws[g]:
                    sigma = _rel_sd(wide.draws[g][pid])
                    if sigma and sigma > 1e-9:
                        out.append((f"param|{pid}", f"{text}: {pid[len(prefix):].replace('_', ' ')}",
                                    'Parameter', f"±{sigma * 196:.0f} %", sigma, ('param', pid)))
            continue  # otherwise a fixed constant, not drawn in the Monte Carlo
        sigma = _rel_sd(wide.draws[group][pid])
        if not sigma or np.isnan(sigma) or sigma < 1e-9:
            continue
        row = tables[group].loc[pid[len(prefix_of[group]):]]
        if group == 'waste_fractions':
            name, typ = _name(row, f"N content of waste: {pid.replace('_', ' ')}"), 'N content of waste'
        else:
            name, typ = _name(row, str(row.get('description', pid))), 'Parameter'
        out.append((f"param|{pid}", name, typ, _width(row), sigma, ('param', pid)))

    trade = bp.get_trade_params()
    for tid, arr in wide.draws['trade_parameters'].items():
        sigma = _rel_sd(arr)
        if not sigma or np.isnan(sigma) or sigma < 1e-9:
            continue
        row = trade.loc[tid]
        out.append((f"trade|{tid}", _name(row, f"N content of traded goods: {tid.replace('_', ' ')}"),
                    'N content of traded goods', _width(row), sigma, ('trade', tid)))
    return out


def compute(run_once, preloaded_data, base_params, pools, seed):
    """
    Runs the sensitivity analysis and returns (summary, elasticities).
    summary has one row per flow, period and source: share of the variance,
    elasticity, uncertainty text and the other flows the source affects.
    elasticities has one row per flow, year and source, with the source's
    relative standard deviation and whether it is drawn independently per
    year. base_params must hold the central values (iteration 0) when this
    is called.
    """
    trade_params = preloaded_data['trade_params']
    wide = MCSampler(base_params, trade_params, NSIM_WIDTH, seed=seed)
    sampler = MCSampler(base_params, trade_params, 1, seed=seed)
    overrides, base_noise, base_trade = sampler.iteration(0)
    base_params.override_global_params(overrides)
    fill_params = sampler._fill_params

    seen = {'dataset': set(), 'fill': {}, 'param': set()}
    orig_factor, orig_fill = DatasetNoise.factor, DatasetNoise.fill
    cls = type(base_params)
    orig_get, orig_waste = cls.get, cls.waste_N_frac

    def tr_factor(self, key, year, sub=None):
        seen['dataset'].add((key, sub))
        return orig_factor(self, key, year, sub)

    def tr_fill(self, kind, fill_id, year, anchors):
        seen['fill'].setdefault((kind, fill_id), {})[year] = min(abs(year - a) for a in anchors)
        return orig_fill(self, kind, fill_id, year, anchors)

    def tr_get(self, pid):
        seen['param'].add(pid)
        return orig_get(self, pid)

    def tr_waste(self, cat):
        seen['param'].add(cat)
        return orig_waste(self, cat)

    DatasetNoise.factor, DatasetNoise.fill = tr_factor, tr_fill
    cls.get, cls.waste_N_frac = tr_get, tr_waste
    try:
        base_df = pd.DataFrame(run_once(preloaded_data, base_params, base_noise, base_trade, pools))
    finally:
        DatasetNoise.factor, DatasetNoise.fill = orig_factor, orig_fill
        cls.get, cls.waste_N_frac = orig_get, orig_waste

    def totals(df):
        return pd.to_numeric(df['value'], errors='coerce').groupby([df['flow_name'], df['year']]).sum()

    base = totals(base_df)
    base_nonzero = base.where(base.abs() > 1e-6)

    class Bumped(DatasetNoise):
        """Central dataset noise with one source raised by STEP."""

        def __init__(self, target):
            super().__init__(base_noise._factors, sampler, 0)
            self.target = target

        def factor(self, key, year, sub=None):
            f = DatasetNoise.factor(self, key, year, sub)
            t = self.target
            hit = ((t[0] == 'dataset' and key == t[1] and sub == t[2])
                   or (t[0] == 'crltap' and sampler.crltap_keys.get(key) == t[1]))
            return f * STEP if hit else f

        def fill(self, kind, fill_id, year, anchors):
            f = DatasetNoise.fill(self, kind, fill_id, year, anchors)
            return f * STEP if self.target[0] == 'fill' and fill_id == self.target[2] else f

    def run(target):
        noise, trade = base_noise, base_trade
        if target[0] in ('dataset', 'crltap', 'fill'):
            noise = Bumped(target)
        elif target[0] == 'trade':
            trade = dict(base_trade)
            trade[target[1]] *= STEP
        else:
            original = base_params.get(target[1]) if target[1] not in base_params.waste_fractions \
                else base_params.waste_N_frac(target[1])
            base_params.override_global_params({target[1]: original * STEP})
        try:
            return totals(pd.DataFrame(run_once(preloaded_data, base_params, noise, trade, pools))).reindex(base.index)
        finally:
            if target[0] == 'param':
                base_params.override_global_params({target[1]: original})

    def fill_sigma(kind, d):
        p = fill_params[kind]
        u = float(p['u0_pct']) + float(p['k_pct_per_year']) * d
        if pd.notna(p['cap_pct']):
            u = min(u, float(p['cap_pct']))
        return np.log(1 + u / 100) / 1.96, u

    sources = _sources(base_params, sampler, wide, seen)
    print(f"[USIKKERHET] {len(sources)} kilder, én modellkjøring per kilde...")
    rows = []
    for i, (sid, name, typ, width, sigma, target) in enumerate(sources):
        annual = target[0] == 'dataset' and target[1] in sampler.annual_keys
        e = (run(target) / base_nonzero - 1.0) / (STEP - 1.0)
        e = e[e.abs() > 1e-4].dropna()
        for (flow, year), ev in e.items():
            u = np.nan
            if target[0] == 'fill':
                d = seen['fill'][(target[1], target[2])].get(year)
                s, u = fill_sigma(target[1], d) if d is not None else (np.nan, np.nan)
            else:
                s = sigma
            rows.append((flow, year, sid, name, typ, width, ev, s, u, annual))
        if i % 100 == 0:
            print(f"[USIKKERHET]   {i}/{len(sources)}")
    res = pd.DataFrame(rows, columns=['flow_name', 'year', 'source_id', 'source', 'type', 'uncertainty',
                                      'elasticity', 'rel_sd', 'fill_u', 'annual'])

    # A fill draw can also move years where it is not applied directly
    # (moving averages, residuals built from filled years of other flows);
    # those rows get the draw's mean width over the years where it applies.
    res['rel_sd'] = res['rel_sd'].fillna(res.groupby('source_id')['rel_sd'].transform('mean'))
    res['var'] = (res['elasticity'] * res['rel_sd']) ** 2
    res['share'] = res['var'] / res.groupby(['flow_name', 'year'])['var'].transform('sum')
    affected = res.groupby('source_id')['flow_name'].agg(lambda s: sorted(set(s)))

    out = []
    for period, (a, b) in PERIODS.items():
        sub = res[res['year'].between(a, b)]
        n_years = sub.groupby('flow_name')['year'].nunique()
        agg = (sub.groupby(['flow_name', 'source_id'])
                  .agg(source=('source', 'first'), type=('type', 'first'), uncertainty=('uncertainty', 'first'),
                       elasticity=('elasticity', 'mean'), share=('share', 'sum'),
                       fill_u_min=('fill_u', 'min'), fill_u_max=('fill_u', 'max'))
                  .reset_index())
        agg['share'] = agg['share'] / agg['flow_name'].map(n_years)
        agg['period'] = period
        out.append(agg)
    summary = pd.concat(out, ignore_index=True)
    is_fill = summary['source_id'].str.startswith('fill|')
    summary.loc[is_fill, 'uncertainty'] = summary[is_fill].apply(
        lambda r: (f"±{r.fill_u_min:.0f}–{r.fill_u_max:.0f} %, lognormal, grows with distance to known year"
                   if pd.notna(r.fill_u_min) else 'grows with distance to known year'), axis=1)
    summary['other_flows'] = [';'.join(f for f in affected[sid] if f != flow)
                              for flow, sid in zip(summary['flow_name'], summary['source_id'])]
    elasticities = res[['flow_name', 'year', 'source_id', 'elasticity', 'rel_sd', 'annual']]
    return summary.drop(columns=['fill_u_min', 'fill_u_max']), elasticities


def write(summary, elasticities, path=OUTPUT_FILE, elasticity_path=ELASTICITY_FILE):
    summary.to_csv(path, index=False)
    print(f"[USIKKERHET] Skrevet {path} ({len(summary)} rader)")
    elasticities.to_csv(elasticity_path, index=False, compression='gzip')
    print(f"[USIKKERHET] Skrevet {elasticity_path} ({len(elasticities)} rader)")
