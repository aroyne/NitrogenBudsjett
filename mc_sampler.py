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

Bounds are read as a 95% interval (2.5th and 97.5th percentiles), as in the
NNB guidance (Schaeppi et al. 2025, Annex A.7) and IPCC (2006). Two
distribution follows how the bounds are given: normal for symmetric bounds
up to +/-40 % (truncated at zero), lognormal for bounds that are symmetric in
log space (uncertainty factors), and triangular (minimum >= 0) for wider
symmetric bounds, asymmetric bounds and quantities with a hard bound at 0 or
1. A triangular row can be marked 'minmax' in the 'bounds' column, for
ranges taken from the literature as minimum and maximum.
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

# Number of normal draws below zero that were redrawn (see draw_values).
TRUNCATED_NORMAL_DRAWS = [0]


def item_rng(seed, group, item_id):
    """Random-number stream for one item, fixed by the master seed and (group, id)."""
    key = zlib.crc32(f"{group}:{item_id}".encode('utf-8'))
    return np.random.default_rng(np.random.SeedSequence(seed, spawn_key=(key,)))


def _triangular_quantiles(t):
    """2.5th and 97.5th percentiles of a triangular distribution on [0, 1] with its mode at t."""
    def q(p):
        return np.sqrt(p * t) if p < t else 1 - np.sqrt((1 - p) * (1 - t))
    return q(0.025), q(0.975)


def _bisect(f, a, b, n=60):
    """Root of f on [a, b], with f(a) > 0 > f(b)."""
    for _ in range(n):
        m = (a + b) / 2
        if f(m) > 0:
            a = m
        else:
            b = m
    return (a + b) / 2


def triangular_minmax_from_95(mode, lo, hi):
    """
    Minimum and maximum of the triangular distribution with the given mode
    whose 2.5th and 97.5th percentiles are lo and hi.

    On [0, 1] with mode t the percentiles are (q_lo(t), q_hi(t)). Requiring
    (lo - mode) / (hi - mode) = (q_lo - t) / (q_hi - t) fixes t; the range
    then follows from (hi - lo) / (q_hi - q_lo).
    """
    if not lo <= mode <= hi or lo == hi:
        raise ValueError(f"Triangulær: modus {mode} må ligge innenfor [{lo}, {hi}]")
    if hi == mode:
        a, b = triangular_minmax_from_95(-mode, -hi, -lo)
        return -b, -a
    r = (lo - mode) / (hi - mode)
    # t_max: where q_hi(t) = t; the root for t lies in (0, t_max).
    t_max = _bisect(lambda t: _triangular_quantiles(t)[1] - t, 0.0, 1.0)

    def h(t):
        q_lo, q_hi = _triangular_quantiles(t)
        return (q_lo - t) - r * (q_hi - t)

    t = _bisect(h, 0.0, t_max)
    q_lo, q_hi = _triangular_quantiles(t)
    width = (hi - lo) / (q_hi - q_lo)
    a = lo - q_lo * width
    return a, a + width


def draw_values(rng, n, val, low_b, upp_b, unc_type, dist_type, bounds='95'):
    """
    Draws n values for an item described by bounds and a distribution type.

    A blank (NaN) low_b/upp_b, or low_b == upp_b == 0, means the item is not
    perturbed and val is returned for every draw.

    For unc_type == 'perc', low_b/upp_b are -/+ percentages of val. For 'abs'
    they are literal bounds on the drawn value, not offsets from val.

    Normal (symmetric bounds up to +/-40 %): mean val, bounds at +/-1.96
    standard deviations, truncated at zero. Lognormal (bounds symmetric in
    log space, such as the inventories' uncertainty factors, and skewed
    parameters): median at val and the upper bound at the 97.5th percentile,
    as for IPCC uncertainty factors ("Fac2", "Fac3"). Triangular (wider
    symmetric bounds, asymmetric bounds, and quantities with a hard bound at
    0 or 1): mode at val; with bounds == '95' the bounds are the
    2.5th and 97.5th percentiles and the minimum and maximum are solved from
    them (triangular_minmax_from_95); with bounds == 'minmax' they are the
    minimum and maximum.

    Raises if a distribution could give values below zero for val >= 0.
    """
    if pd.isna(low_b) or pd.isna(upp_b) or (low_b == 0 and upp_b == 0):
        return np.full(n, val)

    low_b = float(low_b)
    upp_b = float(upp_b)
    unc_type = str(unc_type).lower().strip()
    dist_type = str(dist_type).lower().strip()
    bounds = '95' if pd.isna(bounds) or str(bounds).strip() == '' else str(bounds).strip().lower()
    if bounds not in ('95', 'minmax'):
        raise ValueError(f"Ukjent bounds '{bounds}' (bruk tom, '95' eller 'minmax')")

    if unc_type == 'perc':
        lo = val * (1 - low_b / 100.0)
        hi = val * (1 + upp_b / 100.0)
    elif unc_type == 'abs':
        lo = low_b
        hi = upp_b
    else:
        raise ValueError(f"Ukjent uncertainty_type '{unc_type}'")

    if dist_type == 'triangular':
        if hi == lo:
            return np.full(n, val)
        if bounds == 'minmax':
            a, b = lo, hi
            if not a <= val <= b:
                raise ValueError(f"Triangulær: modus {val} må ligge innenfor [{a}, {b}]")
        else:
            a, b = triangular_minmax_from_95(val, lo, hi)
        if val >= 0 and a < 0:
            raise ValueError(
                f"Triangulær med 95 %-grenser [{lo:.4g}, {hi:.4g}] rundt {val:.4g} gir minimum {a:.4g} < 0; "
                f"bruk 'minmax' i kolonnen bounds")
        if a == val == b:
            return np.full(n, val)
        return rng.triangular(a, val, b, n)

    if bounds == 'minmax':
        raise ValueError("'minmax' kan bare brukes med triangulær fordeling")
    if dist_type == 'normal':
        # Normal is used for symmetric bounds up to +/-40 %, where a draw
        # below zero has a probability of about 5e-7. Such draws are redrawn
        # (a normal truncated at zero) and counted in TRUNCATED_NORMAL_DRAWS.
        sd = (hi - lo) / 2.0 / 1.96
        draws = rng.normal(val, sd, n)
        if val >= 0:
            neg = draws < 0
            while neg.any():
                TRUNCATED_NORMAL_DRAWS[0] += int(neg.sum())
                draws[neg] = rng.normal(val, sd, int(neg.sum()))
                neg = draws < 0
        return draws
    if dist_type == 'log-normal':
        if val <= 0:
            return np.full(n, val)
        sigma_log = np.log(hi / val) / 1.96
        return rng.lognormal(np.log(val), sigma_log, n)
    raise ValueError(f"Fordelingen '{dist_type}' er ikke tillatt (bruk normal, log-normal eller triangular)")


def _check_unique(group, ids):
    dup = ids[ids.duplicated()]
    if len(dup):
        raise ValueError(f"Duplikat-id i '{group}': {sorted(dup.unique())}")


def _draw_row(seed, group, item_id, n, val, row):
    try:
        return draw_values(item_rng(seed, group, item_id), n, val,
                           row['lower_bound'], row['upper_bound'],
                           row['uncertainty_type'], row['distribution_type'], row['bounds'])
    except ValueError as e:
        raise ValueError(f"{group} / {item_id}: {e}") from e


class DatasetNoise:
    """
    Uncertainty factors for the data sets in one MC iteration.
    factor(key, year) is the multiplicative factor for data set `key` in
    `year`. Each data set has one factor per iteration, the same for all
    years; the calculations ask for it per year so that a year-to-year part
    can be added here without changing them.
    """

    def __init__(self, factors):
        self._factors = dict(factors)

    def factor(self, key, year):
        return self._factors[key]


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
                add(group, prefix + item_id, val, _draw_row(seed, group, item_id, n_random, val, row))

        # Dataset noise: multiplicative factors around 1.0.
        group = 'dataset_uncertainties'
        df = base_params.get_table(group)
        ids = df['dataset_name'].astype(str).str.strip()
        _check_unique(group, ids)
        for item_id, (_, row) in zip(ids, df.iterrows()):
            add(group, item_id, 1.0, _draw_row(seed, group, item_id, n_random, 1.0, row))

        # Trade N fractions (NParameters.get_trade_params, indexed by param_id).
        group = 'trade_parameters'
        ids = pd.Series(trade_params.index.astype(str).str.strip())
        _check_unique(group, ids)
        for item_id, (_, row) in zip(ids, trade_params.iterrows()):
            val = float(row['value'])
            add(group, item_id, val, _draw_row(seed, group, item_id, n_random, val, row))

        # animal_products: lower_bound/upper_bound are -/+ percent (95% interval).
        group = 'animal_products'
        df = base_params.get_table(group)
        ids = df['item'].astype(str).str.strip()
        _check_unique(group, ids)
        for item_id, (_, row) in zip(ids, df.iterrows()):
            val = float(row['N_content_percent'])
            add(group, f"prod_{item_id}", val,
                _draw_row(seed, group, item_id, n_random, val, row))

        # protein_food_items: 'uncertainty' is +/- percent (95% interval), lognormal.
        group = 'protein_food_items'
        df = base_params.get_table(group)
        ids = df['food_group'].astype(str).str.strip()
        _check_unique(group, ids)
        for item_id, (_, row) in zip(ids, df.iterrows()):
            val = float(row['protein_content'])
            u = row['uncertainty']
            rnd = draw_values(item_rng(seed, group, item_id), n_random, val, u, u, 'perc', 'log-normal')
            add(group, f"food_protein_{item_id}", val, rnd)

    def iteration(self, i):
        """
        Returns (param_overrides, dataset_noise, trade_factors) for iteration
        i; dataset_noise is a DatasetNoise.
        param_overrides goes to NParameters.override_global_params.
        """
        param_overrides = {}
        for group in [g for g, *_ in STANDARD_SHEETS] + ['animal_products', 'protein_food_items']:
            for key, arr in self.draws[group].items():
                param_overrides[key] = float(arr[i])
        dataset_noise = DatasetNoise({k: float(a[i]) for k, a in self.draws['dataset_uncertainties'].items()})
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
