#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 08:14:54 2026

@author: anja
"""
# lag linjeplott for alle strømmer som har verdier (per år)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime


def plot_flows_time_series(
    df,
    flow_col='Flow Code',         # kolonnen som identifiserer strømmen (eller 'Flow Code' el.)
    year_col='Year',
    value_col='Value',
    unc_col='Uncertainty',        # relativ usikkerhet i prosent
    year_min=1984,
    year_max=2025,
    outdir='flow_time_plots',     # hvis gitt: lagrer fil per flow i denne mappen
    figsize=(8, 3.5),
    style='seaborn-whitegrid',
    dpi=150,
    skip_empty=True,              # hopp over flows uten noen verdier
    max_plots=None                # hvis ikke None: stopp etter denne mange plots (brukbart ved debugging)
):
    """
    Lag ett linjeplot per flow. Matplotlib vil ikke tegne linje over NaN, så gap oppstår
    der et år mangler - akkurat som ønsket.

    Usikkerhet:
    - 'Uncertainty' tolkes som relativ standardavvik i prosent (f.eks. 20 -> sigma = 0.2 * Value).
    - For hvert år og flow beregnes |Value| * Uncertainty/100 som standardavvik.
    - Hvis det finnes flere rader for samme år og flow, beholdes siste både for verdi og usikkerhet
      (konsistent med dagens håndtering av dubletter).
    - Error bars tegnes bare for år der det faktisk finnes en verdi (ikke NaN).
    """

    keep_cols = ['Flow', 'Year', 'Flow Code',
                 'Pool-Out', 'Pool-In', 'Subpool-Out', 'Subpool-In',
                 'Value', 'Species', 'Data sources', unc_col]
    if df.empty:
        df = pd.DataFrame(columns=keep_cols)
    else:
        # Ta bare kolonnene vi trenger (så langt det lar seg gjøre)
        cols_existing = [c for c in keep_cols if c in df.columns]
        df = df[cols_existing].reset_index(drop=True)

    # Typ/whitespace-rydding
    for c in ['Pool-Out', 'Pool-In', 'Subpool-Out', 'Subpool-In', 'Species']:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

    # drop NaN 
    df = df[df[value_col].notna()].copy()

    # sørg for at usikkerhetskolonnen finnes og er numerisk
    if unc_col not in df.columns:
        raise ValueError(f"Dataframe mangler kolonnen '{unc_col}' for usikkerhet i prosent.")
    df[unc_col] = pd.to_numeric(df[unc_col], errors='coerce')
    df = df[df[unc_col].notna()].copy()

    plt.style.use(style)
    years_full = list(range(year_min, year_max + 1))

    # For sikkerhet: kopier og sørg for riktig typer
    needed_cols = [flow_col, year_col, value_col, 'Data sources', unc_col]
    needed_cols = [c for c in needed_cols if c in df.columns]
    df2 = df[needed_cols].copy()
    df2[year_col] = df2[year_col].astype(int)

    # group by flow identifier
    flows = sorted(df2[flow_col].dropna().astype(str).unique())

    if outdir:
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)

    plotted = 0
    skipped_empty = []

    for flow in flows:
        if max_plots is not None and plotted >= max_plots:
            break

        sub = df2[df2[flow_col].astype(str) == flow].copy()
        if sub.empty:
            continue

        # --- Verdier per år ---
        s_val = sub.set_index(year_col)[value_col].sort_index()
        # ved dubletter: hold siste (samme logikk for usikkerhet under)
        s_val = s_val[~s_val.index.duplicated(keep='last')]

        # --- Usikkerhet per år (beregn sigma) ---
        # relativ usikkerhet i prosent -> sigma_abs = |Value| * Uncertainty (given as fraction)
        sigma_series = (sub.set_index(year_col)[value_col].abs() *
                        sub.set_index(year_col)[unc_col])
        sigma_series = sigma_series.sort_index()
        sigma_series = sigma_series[~sigma_series.index.duplicated(keep='last')]

        # reindex til full årsliste
        s_full = pd.Series(index=years_full, dtype=float)
        sigma_full = pd.Series(index=years_full, dtype=float)

        for y, v in s_val.items():
            yi = int(y)
            if year_min <= yi <= year_max:
                s_full.loc[yi] = v

        for y, sig in sigma_series.items():
            yi = int(y)
            if year_min <= yi <= year_max:
                sigma_full.loc[yi] = sig

        # ta hensyn til drop_zero_as_missing: hvis verdi er NaN, skal vi ikke ha sigma heller
        sigma_full[s_full.isna()] = np.nan

        # Data sources på full årsliste
        ds_sub = sub.set_index(year_col)['Data sources'].sort_index()
        ds_full = ds_sub.reindex(years_full)  # NaN for år uten data

        # hvis skip_empty og ingen verdier: hopp over
        if skip_empty and s_full.notna().sum() == 0:
            skipped_empty.append(flow)
            continue

        # masker for interpolert/ekstrapolert (case-insensitive)
        mask_interp_full = ds_full.str.contains(r'interpolated|extrapolated',
                                                case=False, na=False)

        # mask for år med faktisk verdi
        mask_has_value = s_full.notna()

        # kombinasjon: år der vi har verdi og det er merket interpolated/extrapolated
        mask_to_mark = mask_has_value & mask_interp_full

        # --- Plot ---
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

        # linje + punkter
        ax.plot(years_full, s_full.values, '-o',
                markersize=5, linewidth=1.25, label=str(flow),
                markerfacecolor='white')

        # error bars: kun der vi har ikke-NaN-verdier
        mask_err = s_full.notna() & sigma_full.notna()
        x_err = np.array(years_full)[mask_err.to_numpy()]
        y_err = s_full[mask_err].to_numpy()
        yerr = sigma_full[mask_err].to_numpy()

        if len(x_err) > 0:
            ax.errorbar(
                x_err,
                y_err,
                yerr=yerr,
                fmt='none',          # ingen ekstra markør; bruker de som allerede er plottet
                ecolor='gray',
                elinewidth=1,
                capsize=3,
                alpha=0.8,
                label='±1σ'
            )

        # overplot kryss for interpolated/extrapolated
        x_mark = np.array(years_full)[mask_to_mark.to_numpy()]
        y_mark = s_full[mask_to_mark].to_numpy()
        if len(x_mark) > 0:
            ax.plot(x_mark, y_mark, linestyle='None', marker='x', color='red',
                    markersize=7, markeredgewidth=1.5,
                    label='interpolated/extrapolated')

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # estetikk
        ax.set_xlabel('Year')
        ax.set_ylabel('kt N')
        ax.set_title(f"{flow}  ({int(s_full.notna().sum())} years with data) — {ts}")
        ax.set_xlim(year_min - 0.5, year_max + 0.5)
        ax.set_xticks(list(range(
            year_min,
            year_max + 1,
            max(1, (year_max - year_min) // 12)
        )))
        ax.set_ylim(bottom=0)
        ax.grid(True, alpha=0.3)

        # # enkel legend (unngå duplikate labels)
        # handles, labels = ax.get_legend_handles_labels()
        # unique = dict()
        # for h, l in zip(handles, labels):
        #     if l not in unique:
        #         unique[l] = h
        # ax.legend(unique.values(), unique.keys(), loc='best', fontsize='small')

        plt.tight_layout()

        # lagre eller vis
        if outdir:
            safe_name = str(flow).replace('/', '_').replace(' ', '_') \
                                 .replace('.', '_').replace(':', '_')
            fname = outdir / f"{safe_name}.png"
            fig.savefig(fname, dpi=dpi)
            plt.close(fig)
            print(f"Saved: {fname}")
        else:
            plt.show()

        plotted += 1

    print(f"Done; plotted {plotted} flows (out of {len(flows)} available).")
    if skipped_empty:
        print(f"Skipped (empty): {len(skipped_empty)} flows")

if __name__ == "__main__":
    # bare som placeholder – du må gi inn en ekte df ved bruk
    plot_flows_time_series(pd.DataFrame())
