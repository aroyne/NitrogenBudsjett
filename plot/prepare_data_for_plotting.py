#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 08:09:50 2026

@author: anja
"""

import pandas as pd
import numpy as np
import re


# Les sheet, strip kolonnenavn og dropp første data-rad (umiddelbart etter header)
def read_sheet(file_path="Report.xlsx", sheet_name="2a. Database N flows", header_row=0, drop_first_data_row=True):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
    df.columns = [str(c).strip() for c in df.columns]
    if drop_first_data_row:
        # drop the first data row (row after header)
        if len(df) >= 1:
            df = df.iloc[1:].reset_index(drop=True)
    return df

# Normaliser value (robust, kort parser), species og year
def parse_number_simple(s):
    """Enkel, robust parser for tallstrenger:
    - fjerner spaces/apostrof, håndterer parentes som negativt tall
    - hvis både '.' og ',' finnes: bruker siste separator som desimal
    - hvis kun ',' finnes: bytter ',' -> '.'
    - ellers beholder '.' som desimal
    """
    if pd.isna(s):
        return np.nan
    t = str(s).strip()
    # fjern normal og usynlige mellomrom + apostrof
    t = re.sub(r"[\s\u00A0\u202f']", "", t)
    # parenteser -> negativt
    if re.match(r'^\(.*\)$', t):
        t = "-" + t[1:-1]
    # behold kun relevante tegn (siffer, minus, komma, punktum)
    t = re.sub(r'[^\d\-\.,]', '', t)
    if t == '' or t in ['-', ',', '.']:
        return np.nan

    # avgjør desimalsep hvis både '.' og ',' finnes
    if ',' in t and '.' in t:
        if t.rfind(',') > t.rfind('.'):
            # komma sist -> komma er desimal
            t = t.replace('.', '').replace(',', '.')
        else:
            # punktum sist -> punktum er desimal
            t = t.replace(',', '')
    elif ',' in t:
        t = t.replace(',', '.')
    # hvis bare punktum eller ingen separator: behold som er

    try:
        return float(t)
    except:
        return np.nan

def normalize_value_series_minimal(series):
    return series.apply(parse_number_simple)

def read_definitions(file_path="Report.xlsx", sheet_name="5.a Definitions"):
    # Les pool (B=COLUMN 2, C=3) og subpool (E=5, F=6, G=7), header=1
    pools_df = pd.read_excel(file_path, sheet_name=sheet_name, header=1, usecols="B,C", dtype=object)
    pools_df.columns = ['pool_abbr', 'pool_desc']
    pools_df = pools_df.applymap(lambda x: None if pd.isna(x) else str(x).strip())
    
    subpools_df = pd.read_excel(file_path, sheet_name=sheet_name, header=1, usecols="E,F,G", dtype=object)
    subpools_df.columns = ['subpool_abbr', 'subpool_desc', 'part_of_pool']
    subpools_df = subpools_df.applymap(lambda x: None if pd.isna(x) else str(x).strip())
    
    # Bygg mappings
    # pool_map = {r['pool_abbr']: r['pool_desc'] for _, r in pools_df.iterrows() if r['pool_abbr']}
    code2desc = {}

    for _, r in subpools_df.iterrows():
        if r['subpool_abbr'] and r['part_of_pool']:
            code2desc[f"{r['part_of_pool']}.{r['subpool_abbr']}"] = r['subpool_desc']

    return code2desc


if __name__ == "__main__":
    df = read_sheet()
