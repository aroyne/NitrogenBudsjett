#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from calculations.n_params import NParameters


# --------- helpers ---------

def load_population():
    pop = pd.read_excel(
        'data_files/06913_20251113-124117.xlsx',
        skiprows=2,
        skipfooter=42
    ).set_index('Unnamed: 0')
    return pop  # index: year (int), col: 'Befolkning 1. januar'


def map_broad_group(code: str) -> str:
    """
    Map SSB food code (old and new) to a broad food group.
    Works for both 06376 and 10249 index codes.
    """
    # Normalise: we use first 2–5 characters depending on pattern
    # For old codes: '00', '01', '02', ..., '11'
    # For new codes: '0111', '0112', '0113', '0121', '0122', '02', ...
    if code.startswith('00'):
        return 'Brød og korn'
    if code.startswith('0111'):
        return 'Brød og korn'
    if code.startswith('0112'):
        return 'Kjøtt'
    if code.startswith('01') and not code.startswith('0111') and not code.startswith('0112') and not code.startswith('0113'):
        # old '01 Kjøtt og kjøttvarer'
        return 'Kjøtt'
    if code.startswith('0113') or code.startswith('02'):
        # '0113 Fisk', old '02 Fisk og fiskevarer'
        return 'Fisk'
    if code.startswith('0114') or code.startswith('03'):
        return 'Melk, ost og egg'
    if code.startswith('0115') or code.startswith('04'):
        return 'Oljer og fett'
    if code.startswith('0116') or code.startswith('05'):
        return 'Frukt og grønt'
    if code.startswith('0117') or code.startswith('06'):
        # put poteter into same broad group as grønnsaker
        return 'Frukt og grønt'
    if code.startswith('0118') or code.startswith('07'):
        return 'Sukker/sjokolade'
    if code.startswith('0119') or code.startswith('09'):
        return 'Andre matvarer'
    if code.startswith('0121') or code.startswith('08'):
        return 'Kaffe/te/kakao'
    if code.startswith('0122') or code.startswith('11'):
        # alkoholfrie drikker including brus/juice
        return 'Sukkerholdige drikkevarer'
    if code.startswith('02') or code.startswith('021'):
        # alkoholdrikker
        return 'Alkohol'
    return None  # unmapped


# --------- load old (06376) data 1984–1998 ---------

def load_old_mengde_and_N(Jones):
    # Mengde per person per år, by group and interval
    mengde_old = pd.read_excel(
        'data_files/06376_20260129-155937.xlsx',
        sheet_name='06376',
        index_col=0,
        skipfooter=18,
        header=3
    ).iloc[:, 0::2]

    mengde_old = mengde_old.astype(str).applymap(
        lambda s: s.replace(',', '.') if pd.notna(s) else s
    )
    mengde_old = mengde_old.apply(lambda col: pd.to_numeric(col, errors='coerce'))
    mengde_old = mengde_old.dropna(how='all')

    # protein fractions (old table)
    protein_old = pd.read_excel(
        'data_files/protein_innhold_mat_SSB_gammel.xlsx',
        sheet_name='Ark1',
        index_col=0,
        header=None
    ).iloc[:, 0]
    protein_old = pd.to_numeric(
        protein_old.astype(str).str.replace(',', '.'),
        errors='coerce'
    ) / 100.0  # % → fraction

    protein_old = protein_old.reindex(mengde_old.index)

    # protein per group per person per year (kg/pers/year) for each interval
    protein_per_group_old = mengde_old.mul(protein_old, axis=0)

    # N per group per person per year (kg N/pers/year) for each interval
    N_per_group_per_pers_old = protein_per_group_old / Jones

    return mengde_old, N_per_group_per_pers_old


def expand_intervals_to_years(mengde_int, N_int, population, years):
    """
    Expand interval-based mengde_int (kg/pers/yr) and N_int (kgN/pers/yr)
    from 06376 to yearly values 1984–1998 using the same rules you used
    for totals, then convert N to kt/year.
    Both mengde_int and N_int are per broad group after aggregation.
    """

    # Required interval columns:
    # '1983-1985', '1989-1991', '1996-1998'
    # (we don’t use 1986-1988 or 1992-1994 explicitly in the rules)
    try:
        N_8385 = N_int['1983-1985']
        N_8991 = N_int['1989-1991']
        N_9698 = N_int['1996-1998']

        M_8385 = mengde_int['1983-1985']
        M_8991 = mengde_int['1989-1991']
        M_9698 = mengde_int['1996-1998']
    except KeyError:
        # Helpful debug if column labels differ from what we expect
        print("Available interval columns in N_int:", list(N_int.columns))
        print("Available interval in mengde_int:", list(mengde_int.columns))
        raise

    broad_groups = mengde_int.index

    # yearly per-person values (kg/pers/year or kgN/pers/year)
    mengde_yearly = pd.DataFrame(index=broad_groups, columns=years, dtype=float)
    N_yearly = pd.DataFrame(index=broad_groups, columns=years, dtype=float)

    for year in years:
        if year < 1986:
            # 1984–1985: use 1983–1985
            mengde_yearly[year] = M_8385
            N_yearly[year] = N_8385
        elif year < 1989:
            # 1986–1988: average 1983–1985 and 1989–1991
            mengde_yearly[year] = (M_8385 + M_8991) / 2.0
            N_yearly[year] = (N_8385 + N_8991) / 2.0
        elif year < 1992:
            # 1989–1991
            mengde_yearly[year] = M_8991
            N_yearly[year] = N_8991
        elif year < 1996:
            # 1992–1995: average 1989–1991 and 1996–1998
            mengde_yearly[year] = (M_8991 + M_9698) / 2.0
            N_yearly[year] = (N_8991 + N_9698) / 2.0
        else:
            # 1996–1998: use 1996–1998
            mengde_yearly[year] = M_9698
            N_yearly[year] = N_9698

    # multiply N by population (kgN/yr) and convert to kt
    N_total_kg = N_yearly.copy()
    for year in years:
        pop = population.loc[year, 'Befolkning 1. januar']
        N_total_kg[year] *= pop

    N_total_kt = N_total_kg / 1e3  # kg → kt

    return mengde_yearly, N_total_kt


# --------- load new (10249) data 1999–2012 ---------

def load_new_mengde_and_N(Jones, population):
    # 1999–2012: kg/person/year
    mengde = pd.read_excel(
        'data_files/10249_20260129-155747.xlsx',
        sheet_name='10249',
        index_col=0,
        skipfooter=17,
        header=2
    ).iloc[:, 0::2]

    mengde = mengde.astype(str).applymap(
        lambda s: s.replace(',', '.') if pd.notna(s) else s
    )
    mengde = mengde.apply(lambda col: pd.to_numeric(col, errors='coerce'))
    mengde = mengde.dropna(how='all')
    mengde = mengde[~mengde.index.isna()]
    mengde.columns = mengde.columns.astype(int)

    # protein (new table)
    protein = pd.read_excel(
        'data_files/protein_innhold_mat_SSB.xlsx',
        sheet_name='Ark1',
        index_col=0,
        header=None
    ).iloc[:, 0]
    protein = pd.to_numeric(
        protein.astype(str).str.replace(',', '.'),
        errors='coerce'
    ) / 100.0

    protein = protein.reindex(mengde.index)

    protein_per_group = mengde.mul(protein, axis=0)
    N_per_group_per_pers = protein_per_group / Jones  # kg N/pers/yr

    # aggregate to broad groups
    codes = mengde.index.to_series().str.split().str[0]
    broad = codes.apply(map_broad_group)

    mengde_broad = mengde.copy()
    mengde_broad['broad_group'] = broad
    mengde_broad = mengde_broad.dropna(subset=['broad_group'])
    meng_broad = mengde_broad.groupby('broad_group').sum()

    N_broad = N_per_group_per_pers.copy()
    N_broad['broad_group'] = broad
    N_broad = N_broad.dropna(subset=['broad_group'])
    N_broad = N_broad.groupby('broad_group').sum()

    # multiply N by population and convert to kt
    N_total_kg = N_broad.copy()
    for year in N_total_kg.columns:
        pop = population.loc[int(year), 'Befolkning 1. januar']
        N_total_kg[year] *= pop

    N_total_kt = N_total_kg / 1e3  # kg → kt

    return mengde_broad, N_total_kt


# --------- main ---------

def main():
    params = NParameters("data_files/N_parameters.xlsx")
    Jones = params.get("Jones_factor")

    population = load_population()

    # ---- OLD part: 1984–1998 ----
    mengde_old_raw, N_old_raw = load_old_mengde_and_N(Jones)

    # aggregate old to broad groups by interval
    codes_old = mengde_old_raw.index.to_series().str.split().str[0]
    broad_old = codes_old.apply(map_broad_group)

    mengde_old_broad_int = mengde_old_raw.copy()
    mengde_old_broad_int['broad_group'] = broad_old
    mengde_old_broad_int = mengde_old_broad_int.dropna(subset=['broad_group'])
    mengde_old_broad_int = mengde_old_broad_int.groupby('broad_group').sum()

    N_old_broad_int = N_old_raw.copy()
    N_old_broad_int['broad_group'] = broad_old
    N_old_broad = N_old_broad_int.dropna(subset=['broad_group'])
    N_old_broad_int = N_old_broad_int.groupby('broad_group').sum()

    years_old = list(range(1984, 1999))
    mengde_old_yearly, N_old_total_kt = expand_intervals_to_years(
        mengde_old_broad_int,
        N_old_broad_int,
        population,
        years_old
    )

    # ---- NEW part: 1999–2012 ----
    mengde_new_broad, N_new_total_kt = load_new_mengde_and_N(Jones, population)

    # ---- Combine 1984–2012 ----

    # 1) Keep only year-like columns (all digits) from each DF
    def keep_year_columns(df):
        year_cols = [c for c in df.columns if str(c).isdigit()]
        df_years = df[year_cols].copy()
        df_years.columns = [int(c) for c in df_years.columns]
        return df_years

    mengde_old_yearly = keep_year_columns(mengde_old_yearly)
    N_old_total_kt = keep_year_columns(N_old_total_kt)

    mengde_new_broad = keep_year_columns(mengde_new_broad)
    N_new_total_kt = keep_year_columns(N_new_total_kt)

    # 2) Concatenate and sort by year
    mengde_all = pd.concat([mengde_old_yearly, mengde_new_broad], axis=1)
    mengde_all = mengde_all.loc[:, sorted(mengde_all.columns)]

    N_all_kt = pd.concat([N_old_total_kt, N_new_total_kt], axis=1)
    N_all_kt = N_all_kt.loc[:, sorted(N_all_kt.columns)]

    # ---- Plot 1: cumulative food amount (kg/pers/yr) ----

    mengde_all_T = mengde_all.T  # index: years, columns: broad groups

    plt.figure(figsize=(12, 7))
    mengde_all_T.plot.area(ax=plt.gca())
    plt.xlabel('Year')
    plt.ylabel('Food amount (kg/person/year)')
    plt.title('Food amount per broad category (kg/person/year), 1984–2012')
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='small')
    plt.tight_layout()
    plt.savefig("food_amount_broad_categories_1984_2012.png", dpi=300)
    plt.show()

    # ---- Plot 2: cumulative N (ktN/yr) ----

    N_all_T = N_all_kt.T  # index: years, columns: broad groups

    plt.figure(figsize=(12, 7))
    N_all_T.plot.area(ax=plt.gca())
    plt.xlabel('Year')
    plt.ylabel('N in food (kt N/year)')
    plt.title('N in food per broad category (kt N/year), 1984–2012')
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='small')
    plt.tight_layout()
    plt.savefig("food_N_broad_categories_1984_2012.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
