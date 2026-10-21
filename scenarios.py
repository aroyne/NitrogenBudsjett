#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Named scenarios for two method choices in agriculture, for the article: how
much they change the agricultural NUE indicators and balances compared with
the Monte Carlo interval of the main run.

Each scenario is one run with central values (iteration 0), compared with
the same run for the main choices.

- G1, Fodder crops step adjusted: Fodder crops from 2021 scaled so that the
  change from 2020 to 2021 equals the change in Eurostat's gross nutrient
  balance (calculations_for_article.fodder_crops_level_adjusted).
- G2, no dry-matter conversion of eng til slått before 2021: the figures
  used as SSB reports them (hay weight, energy basis before 1995).
- U1, fixed utmark share: 47 % of the manure deposited by grazing animals
  lands on utmark in every year, instead of the share estimated from the SSB
  survey of grazing weeks and the cattle on utmark.

Writes output_files/scenario_results.csv and the note
claude_tekst/2026-10-21_scenarioer.md. The Monte Carlo interval of the main
run comes from output_files/MC_aggregate_summary.csv
(aggregate_uncertainty.py).
"""
import pandas as pd

import calculations_for_article as cfa
import aggregate_uncertainty as au

RESULTS_FILE = 'output_files/scenario_results.csv'
NOTE_FILE = 'claude_tekst/2026-10-21_scenarioer.md'

# Utmark share of grazing manure used before the survey-based estimate: the
# former parameter innmark_prp_fraction = 0.53 (apportioning national PRP by
# animal category with typical grazing practice per species).
FIXED_UTMARK_SHARE = 0.47

QUANTITIES = ['nue_q1a', 'nue_q2', 'nue_q1b', 'nue_q1c', 'nue_q3',
              'balance_AG', 'balance_AG.MM', 'balance_AG.SM', 'balance_FS.OL']

SCENARIOS = {
    'G1': 'Fodder crops step in 2021 adjusted to Eurostat GNB',
    'G2': 'No dry-matter conversion of eng til slått before 2021',
    'U1': f'Fixed utmark share of grazing manure ({FIXED_UTMARK_SHARE:.0%})',
}


def _fixed_utmark(original):
    """utmark_grazing with the utmark share fixed. Manure, leaching and N2O
    are all proportional to the share, so each year is rescaled."""
    def wrapped(preloaded_data, current_params, dataset_noise):
        result = original(preloaded_data, current_params, dataset_noise)
        for year, r in result.items():
            k = FIXED_UTMARK_SHARE / r['utmark_frac']
            result[year] = {'utmark_frac': FIXED_UTMARK_SHARE, 'manure': r['manure'] * k,
                            'leaching': r['leaching'] * k, 'n2o': r['n2o'] * k}
        return result
    return wrapped


def _run(preloaded_data, base_params, sampler, pools, overrides=None, fixed_utmark=False):
    from main_mc import run_once, setup_iteration
    import calculations.ag_mc as ag_mc
    import calculations.fs_mc as fs_mc
    params, noise, trade = setup_iteration(base_params, sampler, 0)
    originals = {}
    if overrides:
        originals = {k: params.get(k) for k in overrides}
        params.override_global_params(overrides)
    patched = (ag_mc.utmark_grazing, fs_mc.utmark_grazing)
    if fixed_utmark:
        ag_mc.utmark_grazing = fs_mc.utmark_grazing = _fixed_utmark(patched[0])
    try:
        records = run_once(preloaded_data, params, noise, trade, pools)
    finally:
        ag_mc.utmark_grazing, fs_mc.utmark_grazing = patched
        if originals:
            params.override_global_params(originals)
    df = pd.DataFrame(records)
    df = df[df['year'].isin(au.YEARS)].rename(columns={'value': 'central'})
    df['central'] = pd.to_numeric(df['central'], errors='coerce')
    return df[['flow_name', 'year', 'central']].reset_index(drop=True)


def _metrics(df):
    """Level and change (as in aggregate_uncertainty.py) of each quantity."""
    fns = {q['id']: q['fn'] for q in au.QUANTITIES}
    out = {}
    for qid in QUANTITIES:
        values = au._evaluate(fns[qid], df)
        for metric in au.METRICS:
            out[(qid, metric)] = float(values @ au._weights(metric))
    return out


def compute():
    from main_mc import POOL_ORDER
    from data_loader import load_all_data
    from calculations.n_params import NParameters
    from mc_sampler import MCSampler, DEFAULT_SEED

    pools = list(POOL_ORDER)
    preloaded_data = load_all_data(pools)
    base_params = NParameters("parameters/N_parameters.xlsx")
    preloaded_data.setdefault('trade_params', base_params.get_trade_params())
    sampler = MCSampler(base_params, preloaded_data['trade_params'], 1, seed=DEFAULT_SEED)

    base = _run(preloaded_data, base_params, sampler, pools)
    runs = {
        'base': base,
        'G1': cfa.fodder_crops_level_adjusted(base),
        'G2': _run(preloaded_data, base_params, sampler, pools,
                   overrides={'hay_DM_frac': 1.0, 'hay_energy_to_DM_basis_frac': 1.0}),
        'U1': _run(preloaded_data, base_params, sampler, pools, fixed_utmark=True),
    }
    metrics = {name: _metrics(df) for name, df in runs.items()}

    mc = pd.read_csv(au.SUMMARY_FILE).set_index(['quantity', 'metric'])
    labels = {q['id']: (q['label'], q['unit']) for q in au.QUANTITIES}
    rows = []
    for (qid, metric), value in metrics['base'].items():
        row = {'quantity': qid, 'label': labels[qid][0], 'unit': labels[qid][1], 'metric': metric,
               'base': value, 'mc_central': mc.loc[(qid, metric), 'central'],
               'p2_5': mc.loc[(qid, metric), 'p2_5'], 'p97_5': mc.loc[(qid, metric), 'p97_5']}
        for name in SCENARIOS:
            row[name] = metrics[name][(qid, metric)]
        rows.append(row)
    return pd.DataFrame(rows)


def _fmt(x):
    return f"{x:.1f}".replace('-', '−')


def write(results):
    results.to_csv(RESULTS_FILE, index=False)
    lines = ["# Scenarioer for metodevalg i jordbruket (steg 5 C)", "",
             "Generert av `scenarios.py`. Bare til artikkelen. Hvert scenario er én kjøring med sentrale verdier; "
             "MC-intervallet er 2,5–97,5-persentilene for hovedvalget (`aggregate_uncertainty.py`). "
             "Nivå = snitt 2022–2024, endring = snitt 2022–2024 minus snitt 1990–1992 (NUE i prosentpoeng). "
             "Utenfor = scenarioverdien ligger utenfor MC-intervallet.", ""]
    lines += [f"- **{k}:** {v}" for k, v in SCENARIOS.items()]
    lines.append("")
    for metric, head in [('level', 'Nivå 2022–2024'), ('change', 'Endring fra 1990–1992')]:
        lines += [f"## {head}", "",
                  "| Størrelse | Hovedvalg | MC-intervall | " + " | ".join(SCENARIOS) + " |",
                  "|---|---|---|" + "---|" * len(SCENARIOS)]
        for r in results[results['metric'] == metric].itertuples():
            cells = []
            for name in SCENARIOS:
                v = getattr(r, name)
                outside = ' (utenfor)' if not r.p2_5 <= v <= r.p97_5 else ''
                cells.append(f"{_fmt(v)}{outside}")
            lines.append(f"| {r.label} ({r.unit}) | {_fmt(r.base)} | {_fmt(r.p2_5)} til {_fmt(r.p97_5)} | "
                         + " | ".join(cells) + " |")
        lines.append("")
    with open(NOTE_FILE, 'w') as f:
        f.write("\n".join(lines))
    print(f"[SCENARIO] Skrevet {RESULTS_FILE} og {NOTE_FILE}")


if __name__ == '__main__':
    write(compute())
