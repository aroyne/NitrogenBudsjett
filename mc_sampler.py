#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Draws every Monte Carlo input for a whole run up front, from a single master
seed, and serves the values for one iteration at a time.

All perturbed inputs in N_parameters.xlsx are collected into one table of
items (group = sheet name, id, base value, bounds, distribution). For each
item an (nsim,) array of values is drawn in one go:

- row 0 is the deterministic baseline (the base value, and 1.0 for dataset
  noise factors),
- rows 1..nsim-1 are random draws.

Every item gets its own random-number stream, derived from the master seed
and the item's (group, id). Adding, removing or changing one item therefore
leaves the draws of every other item unchanged, and the same seed always
reproduces the same run.

A parameter is drawn once per iteration and shared by every flow and year
that uses it, so correlations between flows (shared N contents, mass-balance
residuals) and between years are kept within each iteration.
"""
import zlib

import numpy as np
import pandas as pd

DEFAULT_SEED = 20261018

# (group/sheet, id column, value column, key prefix used in current_params)
STANDARD_SHEETS = [
    ('global_parameters', 'parameter_id', 'value', ''),
    ('waste_fractions', 'waste_category', 'N_frac', ''),
    ('animal_weights', 'item_name', 'avg_weight_kg', 'weight_'),
]


def item_rng(seed, group, item_id):
    """Random-number stream for one item, fixed by the master seed and (group, id)."""
    key = zlib.crc32(f"{group}:{item_id}".encode('utf-8'))
    return np.random.default_rng(np.random.SeedSequence(seed, spawn_key=(key,)))


def draw_values(rng, n, val, low_b, upp_b, unc_type, dist_type):
    """
    Draws n values for an item described by bounds and a distribution type.

    A blank (NaN) low_b/upp_b, or low_b == upp_b == 0, means the item is not
    perturbed and val is returned for every draw.

    For unc_type == 'perc', low_b/upp_b are +/- percentages of val. For 'abs'
    they are literal bounds on the drawn value, not offsets from val. For PERT
    the bounds are the minimum and maximum; for normal and lognormal
    distributions they are a 95% interval. The lognormal distribution has its
    median at val and the upper bound at its 97.5th percentile, as for IPCC
    uncertainty factors ("Fac2", "Fac3").

    Negative draws are set to 0 when val >= 0.
    """
    if pd.isna(low_b) or pd.isna(upp_b) or (low_b == 0 and upp_b == 0):
        return np.full(n, val)

    low_b = float(low_b)
    upp_b = float(upp_b)
    unc_type = str(unc_type).lower().strip()
    dist_type = str(dist_type).lower().strip()

    if unc_type == 'perc':
        abs_min = val * (1 - low_b / 100.0)
        abs_max = val * (1 + upp_b / 100.0)
    elif unc_type == 'abs':
        abs_min = low_b
        abs_max = upp_b
    else:
        raise ValueError(f"Ukjent uncertainty_type '{unc_type}'")

    if 'pert' in dist_type:
        range_val = abs_max - abs_min
        if range_val == 0:
            return np.full(n, val)
        alpha = 1 + 4 * (val - abs_min) / range_val
        beta = 1 + 4 * (abs_max - val) / range_val
        draws = abs_min + rng.beta(alpha, beta, n) * range_val
    elif 'log' in dist_type:
        if val <= 0:
            return np.full(n, val)
        sigma_log = np.log(abs_max / val) / 1.96
        draws = rng.lognormal(np.log(val), sigma_log, n)
    elif dist_type in ('norm', 'normal'):
        std_dev = (abs_max - abs_min) / 2.0 / 1.96
        draws = rng.normal(val, std_dev, n)
    else:
        raise ValueError(f"Ukjent distribution_type '{dist_type}'")

    if val >= 0:
        draws = np.where(draws < 0, 0.0, draws)
    return draws


def _draw_relative_percent(rng, n, val, u_percent, dist_type):
    """
    Draws n values as val times a factor around 1, where u_percent is the
    standard deviation (normal) or the half-width (uniform) of that factor in
    percent. Used for animal_products and protein_food_items. Negative draws
    are set to 0.
    """
    u_val = float(u_percent) / 100.0
    if u_val <= 0:
        return np.full(n, val)
    if dist_type == 'unif':
        draws = val * rng.uniform(1.0 - u_val, 1.0 + u_val, n)
    else:
        draws = val * rng.normal(1.0, u_val, n)
    return np.where(draws < 0, 0.0, draws)


def _check_unique(group, ids):
    dup = ids[ids.duplicated()]
    if len(dup):
        raise ValueError(f"Duplikat-id i '{group}': {sorted(dup.unique())}")


class MCSampler:
    """
    Holds the drawn values for all MC inputs of one run.

    self.draws maps group -> {key: (nsim,) array}. Groups: the sheet names in
    STANDARD_SHEETS, 'dataset_uncertainties', 'trade_parameters',
    'animal_products' and 'protein_food_items'.
    """

    def __init__(self, base_params, trade_params, nsim, seed=DEFAULT_SEED):
        self.nsim = nsim
        self.seed = seed
        self.draws = {}
        n_random = nsim - 1

        def add(group, key, baseline, random_draws):
            self.draws.setdefault(group, {})[key] = np.concatenate(([baseline], random_draws))

        for group, id_col, val_col, prefix in STANDARD_SHEETS:
            df = base_params.get_table(group)
            ids = df[id_col].astype(str).str.strip()
            _check_unique(group, ids)
            for item_id, (_, row) in zip(ids, df.iterrows()):
                val = float(row[val_col])
                rnd = draw_values(item_rng(seed, group, item_id), n_random, val,
                                     row['lower_bound'], row['upper_bound'],
                                     row['uncertainty_type'], row['distribution_type'])
                add(group, prefix + item_id, val, rnd)

        # Dataset noise: multiplicative factors around 1.0.
        group = 'dataset_uncertainties'
        df = base_params.get_table(group)
        ids = df['dataset_name'].astype(str).str.strip()
        _check_unique(group, ids)
        for item_id, (_, row) in zip(ids, df.iterrows()):
            rnd = draw_values(item_rng(seed, group, item_id), n_random, 1.0,
                                 row['lower_bound'], row['upper_bound'],
                                 row['uncertainty_type'], row['distribution_type'])
            add(group, item_id, 1.0, rnd)

        # Trade N fractions (NParameters.get_trade_params, indexed by param_id).
        group = 'trade_parameters'
        ids = trade_params.index.astype(str).str.strip().to_series(index=trade_params.index)
        _check_unique(group, ids)
        for item_id, (_, row) in zip(ids, trade_params.iterrows()):
            val = float(row['value'])
            rnd = draw_values(item_rng(seed, group, item_id), n_random, val,
                                 row['lower_bound'], row['upper_bound'],
                                 row['uncertainty_type'], row['distribution_type'])
            add(group, item_id, val, rnd)

        # animal_products: upper_bound is the relative uncertainty in percent.
        group = 'animal_products'
        df = base_params.get_table(group)
        ids = df['item'].astype(str).str.strip()
        _check_unique(group, ids)
        for item_id, (_, row) in zip(ids, df.iterrows()):
            val = float(row['N_content_percent'])
            dist = str(row['distribution_type']).strip().lower()
            rnd = _draw_relative_percent(item_rng(seed, group, item_id), n_random, val,
                                         row['upper_bound'], dist)
            add(group, f"prod_{item_id}", val, rnd)

        # protein_food_items: 'uncertainty' is a normal standard deviation in percent.
        group = 'protein_food_items'
        df = base_params.get_table(group)
        ids = df['food_group'].astype(str).str.strip()
        _check_unique(group, ids)
        for item_id, (_, row) in zip(ids, df.iterrows()):
            val = float(row['protein_content'])
            rnd = _draw_relative_percent(item_rng(seed, group, item_id), n_random, val,
                                         row['uncertainty'], 'norm')
            add(group, f"food_protein_{item_id}", val, rnd)

    def iteration(self, i):
        """
        Returns (param_overrides, dataset_noise, trade_factors) for iteration i.
        param_overrides goes to NParameters.override_global_params.
        """
        param_overrides = {}
        for group in [g for g, *_ in STANDARD_SHEETS] + ['animal_products', 'protein_food_items']:
            for key, arr in self.draws[group].items():
                param_overrides[key] = float(arr[i])
        dataset_noise = {k: float(a[i]) for k, a in self.draws['dataset_uncertainties'].items()}
        trade_factors = {k: float(a[i]) for k, a in self.draws['trade_parameters'].items()}
        return param_overrides, dataset_noise, trade_factors

    def to_long(self):
        """All drawn values in long format: sim_id, group, id, value."""
        frames = []
        sim_ids = np.arange(self.nsim)
        for group, items in self.draws.items():
            for key, arr in items.items():
                frames.append(pd.DataFrame({'sim_id': sim_ids, 'group': group,
                                            'id': key, 'value': arr}))
        return pd.concat(frames, ignore_index=True)
