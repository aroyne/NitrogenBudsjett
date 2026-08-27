#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General-purpose helpers shared across the calculations/ modules: filling in
missing years, reading year/value pairs out of fixed-layout Excel sheets,
converting CRLTAP emissions inventory data to N, and processing generic
foreign trade flows.
"""

import numpy as np
import pandas as pd


start_year = 1984
end_year = 2025
EXPECTED_YEARS = set(range(start_year, end_year + 1))



def report_missing_years(flow_code, missing_years, results,
                          comment='not done', data_sources='no data',
                          default_value=np.nan):
    """
    Append zero flows for missing_years to results.

    Parameters
    ----------
    flow_code : str
    missing_years : iterable of int
    results : list of dict  (modified in-place)
    comment : str
    data_sources : str
    default_value : float
    """
    for year in missing_years:
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': default_value,
            'comment': comment,
            'data_sources': data_sources,
        })


def read_year_value_row(sheet,
                        year_values=None,
                        year_row=9,
                        value_row=11,
                        first_col=2,
                        unit_factor=1.0,
                        op='+'):
    """
    Read year/value pairs from one row of an Excel sheet and accumulate
    them into a dict.

    Parameters
    ----------
    sheet : openpyxl worksheet
    year_values : dict or None
        If None, a new dict is created. If dict, updated in place.
        Keys: int year, values: float.
    year_row : int
        Row index containing the years.
    value_row : int
        Row index containing the values corresponding to the years.
    first_col : int
        First column index to read (default 2 = column B).
    unit_factor : float
        Multiplier applied to each numeric value (e.g. 1e-3 to convert t → kt).
    op : str
        How to combine with existing values:
        '+' (default) → add to existing;
        'replace' → overwrite existing.

    Returns
    -------
    dict
        The updated dict mapping year → value.
    """
    if year_values is None:
        year_values = {}

    for col in range(first_col, sheet.max_column + 1):
        year = sheet.cell(row=year_row, column=col).value
        value = sheet.cell(row=value_row, column=col).value
        if year is None or value in (None, ':'):
            continue

        year = int(year)
        val = float(value) * unit_factor

        if op == '+':
            year_values[year] = year_values.get(year, 0.0) + val
        elif op == 'replace':
            year_values[year] = val
        else:
            raise ValueError("op must be '+' or 'replace'")

    return year_values


def load_crltap_emissions_to_N(raw_lines, categories, pollutant, conv_to_N, dataset_noise, noise_key='CRLTAP', skiprows=4, sep=';'):
    """
    Sums CRLTAP Inventory Submissions emissions (webdabData*.txt, format
    ISO2;YEAR;SECTOR;POLLUTANT;UNIT;NUMBER) over the given NFR sector codes
    and pollutant, and converts the result to N. Used across ag_mc.py,
    ef_mc.py, mp_mc.py and pr_mc.py for CRLTAP-derived NH3/NOx flows.
    """
    noise_val = dataset_noise[noise_key]
    valid_lines = raw_lines[skiprows:] if len(raw_lines) > skiprows else []
    yearly_raw_sums = {}

    for line in valid_lines:
        if not line.strip():
            continue

        parts = line.split(sep)
        if len(parts) < 6:
            continue

        try:
            cat_val = parts[2].strip()
            poll_val = parts[3].strip()

            if cat_val in categories and poll_val == pollutant:
                year = int(parts[1].strip())

                # CRLTAP reports non-numeric flags (IE/NA/NE/NO) for sector/
                # pollutant/year combinations with no estimate; '-' means zero,
                # the other flags mean the row has no usable number at all and
                # is skipped (caught by the except clause below) rather than
                # counted as zero.
                val_str = parts[5].strip()
                raw_val = float(val_str) if (val_str and val_str != '-') else 0.0

                yearly_raw_sums[year] = yearly_raw_sums.get(year, 0.0) + raw_val
        except (ValueError, IndexError):
            continue

    final_sums = {}
    for year, raw_sum in yearly_raw_sums.items():
        base_value = raw_sum * conv_to_N
        final_sums[year] = base_value * noise_val

    return final_sums

def read_trade_data(trade_file):
    """Reads SSB table 08801 raw foreign trade statistics (year, direction,
    HS code, country, value/amount columns) into a fixed-column DataFrame."""
    trade_data = pd.read_csv(trade_file, sep=';', header=None)
    trade_columns = ['year', 'impeks', 'HS_code', 'country', 'value_code', 'amount', 'value_2', 'value_3']
    trade_data.columns = trade_columns
    return trade_data

def process_generic_trade_flow(preloaded_data, current_params, current_trade_factors,
                                target_types, is_import=True, dataset_noise=None, flow_code=None, results=None, data_sources='SSB tab 08801'):
    """
    Computes N in an import or export flow from the pre-merged trade volume
    table (preloaded_data['compressed_trade_volume'], built in data_loader.py
    from SSB table 08801 joined against the trade_mapping sheet), filtered to
    the given HS-code-derived 'type' categories and trade direction. Shared
    by most of the RW.RW-facing import/export flows across ag_mc.py, ef_mc.py,
    mp_mc.py, pr_mc.py and rw_mc.py.
    """
    df_vol = preloaded_data.get('compressed_trade_volume')
    if df_vol is None:
        # data_loader.py's own load of 'compressed_trade_volume' is wrapped in
        # a broad try/except that can leave this key unset on failure - see
        # CLAUDE.md's utils.py notes for the plan to revisit this together
        # with data_loader.py's own review.
        if flow_code:
            print(f"[ADVARSEL] Mangler handelsdata for {flow_code}.")
        return {}

    dataset_key = '08801'
    noise_val = dataset_noise[dataset_key]

    if isinstance(target_types, (str, int, float)):
        types_to_match = {str(target_types).lower().strip()}
    else:
        types_to_match = {str(t).lower().strip() for t in target_types}

    # impeks: 1 = import, 2 = export
    impeks_target = ['1', '1.0'] if is_import else ['2', '2.0']
    is_correct_type = df_vol['type'].astype(str).str.lower().str.strip().isin(types_to_match)
    is_correct_direction = df_vol['impeks'].astype(str).str.strip().isin(impeks_target)

    df_filtered = df_vol[is_correct_type & is_correct_direction].copy()

    flow_dict = {}

    if not df_filtered.empty:
        # fillna(0.0): every 'konv' code currently present in
        # compressed_trade_volume has a matching entry in current_trade_factors
        # (verified against real data), so this only guards against a future
        # trade_mapping addition that outpaces trade_params rather than a
        # known gap today.
        v_factors = df_filtered['konv'].astype(str).str.strip().map(current_trade_factors).fillna(0.0)
        df_filtered['perturbed_amount'] = df_filtered['amount'] * noise_val
        df_filtered['N_amount'] = df_filtered['perturbed_amount'] * v_factors / 1e6
        df_filtered.loc[df_filtered['N_amount'] < 0, 'N_amount'] = 0.0
        for yr_raw, amt in zip(df_filtered['year'].values, df_filtered['N_amount'].values):
            yr = int(float(yr_raw))
            flow_dict[yr] = flow_dict.get(yr, 0.0) + amt

    if results is not None and flow_code is not None:
        collected_years = set()
        for year in EXPECTED_YEARS:
            if year in flow_dict:
                collected_years.add(year)
                results.append({
                    'flow_name': flow_code,
                    'year': year,
                    'value': float(flow_dict[year]), 
                    'comment': 'ok',
                    'data_sources': data_sources
                })
        report_missing_years(flow_code, EXPECTED_YEARS - collected_years, results)

    return flow_dict