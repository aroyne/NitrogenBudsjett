import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def plot_subpool_balance(df, pool, subpool, output_dir=".", suffix=""):
    """
    Lager figur med N-balanse for en gitt subpool (pool.subpool),
    med alle strømmer stablet over/under null per år, en svart linje
    for totalbalansen, og usikkerhet på totalbalansen (± 1 sigma)
    vist som stiplede linjer og som et skyggebånd.

    Forutsetninger om usikkerhet:
    - Kolonnen 'Uncertainty' finnes i df og er relativ standardavvik i prosent
      (f.eks. 20 betyr sigma = 0.2 * Value).
    - Usikkerheter på ulike strømmer antas uavhengige.
    """

    # Kopi så vi ikke endrer original-df i kalleren
    df = df.copy()

    # Rydd typer
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna(subset=["Year", "Value"])

    # Sjekk at Uncertainty finnes
    if "Uncertainty" not in df.columns:
        raise ValueError("Dataframe mangler kolonnen 'Uncertainty' for usikkerhet i prosent.")

    df["Uncertainty"] = pd.to_numeric(df["Uncertainty"], errors="coerce")
    df = df.dropna(subset=["Uncertainty"])

    # Ignorer Flow Codes som er 0 i alle år
    nonzero_flag = df.groupby("Flow Code")["Value"].transform(lambda s: (s != 0).any())
    df = df[nonzero_flag].copy()

    # Velg rader som gjelder denne subpoolen (inn eller ut)
    mask_in  = (df["Pool-In"]  == pool) & (df["Subpool-In"]  == subpool)
    mask_out = (df["Pool-Out"] == pool) & (df["Subpool-Out"] == subpool)
    df_sp = df[mask_in | mask_out].copy()
    
    if df_sp.empty:
        print(f"Ingen data for subpool {pool}.{subpool}, hopper over.")
        return

    # Klassifiser inn/ut og lag FlowID
    def classify_row(row):
        if (row["Pool-In"] == pool) and (row["Subpool-In"] == subpool):
            return "in"
        else:
            return "out"

    df_sp["Direction"] = df_sp.apply(classify_row, axis=1)
    df_sp["FlowID"] = df_sp["Flow Code"].fillna(df_sp["Flow"])

    # Gi negativt fortegn til ut-strømmene (Value)
    df_sp.loc[df_sp["Direction"] == "out", "Value"] *= -1

    # Absolutt standardavvik for hver rad (uavhengig av fortegn på Value)
    df_sp["sigma_abs"] = (df_sp["Value"].abs() * df_sp["Uncertainty"] / 100.0)

    # Varians per rad
    df_sp["var"] = df_sp["sigma_abs"] ** 2

    # År × FlowID-matrise (sum per år, ikke kumulativ over tid) for Value
    flow_year = (df_sp
                 .groupby(["Year", "FlowID"])["Value"]
                 .sum()
                 .unstack("FlowID")
                 .fillna(0))
    flow_year = flow_year.sort_index()

    if flow_year.empty:
        print(f"Ingen ikke-null strømmer for subpool {pool}.{subpool}, hopper over.")
        return

    years = flow_year.index.values

    # Samme aggregering for varians
    var_flow_year = (df_sp
                     .groupby(["Year", "FlowID"])["var"]
                     .sum()
                     .unstack("FlowID")
                     .fillna(0))
    var_flow_year = var_flow_year.loc[years]  # sørg for samme indeks

    # Total varians per år = sum over alle FlowID
    var_total_year = var_flow_year.sum(axis=1)
    sigma_total = np.sqrt(var_total_year.values)  # stdavvik for totalbalansen per år

    # Inn-/ut-strømmer direkte fra Direction
    in_flows  = sorted(df_sp.loc[df_sp["Direction"] == "in",  "FlowID"].unique())
    out_flows = sorted(df_sp.loc[df_sp["Direction"] == "out", "FlowID"].unique())

    # Plot: stabling per år, + svart total-linje, + usikkerhetsbånd
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = plt.cm.tab20.colors
    color_map = {f: colors[i % len(colors)] for i, f in enumerate(flow_year.columns)}

    out_handles, out_labels = [], []
    in_handles, in_labels = [], []

    # Ut-strømmer (under null) – bygg fra reversed(out_flows) for å få riktig legend senere
    bottom_neg = np.zeros_like(years, dtype=float)
    for f in reversed(out_flows):
        y = flow_year[f].values if f in flow_year.columns else np.zeros_like(years, dtype=float)
        top = bottom_neg + y
        h = ax.fill_between(years, bottom_neg, top,
                            color=color_map.get(f, "grey"), alpha=0.8)
        out_handles.append(h)
        out_labels.append(f)
        bottom_neg = top

    # Inn-strømmer (over null)
    bottom_pos = np.zeros_like(years, dtype=float)
    for f in in_flows:
        y = flow_year[f].values if f in flow_year.columns else np.zeros_like(years, dtype=float)
        top = bottom_pos + y
        h = ax.fill_between(years, bottom_pos, top,
                            color=color_map.get(f, "grey"), alpha=0.8)
        in_handles.append(h)
        in_labels.append(f)
        bottom_pos = top

    # Totalbalanse per år (konsistent med det som vises)
    total = bottom_pos + bottom_neg
    line_total, = ax.plot(years, total,
                          color="black", linewidth=2, label="Total balanse (år)")

    # Usikkerhetsbånd: fill_between for total ± sigma_total
    band = ax.fill_between(years,
                           total - sigma_total,
                           total + sigma_total,
                           color="black", alpha=0.15,
                           label="±1σ total usikkerhet")

    # # (Valgfritt) stiplede linjer på toppen av båndet
    # line_total_plus, = ax.plot(years, total + sigma_total,
    #                            color="black", linewidth=1,
    #                            linestyle="--")
    # line_total_minus, = ax.plot(years, total - sigma_total,
    #                             color="black", linewidth=1,
    #                             linestyle="--")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel("År")
    ax.set_ylabel("N (kt/y)")
    ax.set_title(f"N-balanse for subpool {pool}.{subpool} — {ts}")
    ax.set_xlim(1990, 2023)

    # Legend: total, usikkerhetsbånd, så inn (øverst→nederst), så ut (øverst→nederst)
    handles_legend = (
        [line_total, band] +
        in_handles[::-1] +
        out_handles
    )
    labels_legend = (
        ["Total balanse (år)",
         "Total balanse ± usikkerhet (1σ)"] +
        in_labels[::-1] +
        out_labels
    )

    ax.legend(handles_legend, labels_legend,
              bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()

    # Filnavn og lagring
    os.makedirs(output_dir, exist_ok=True)
    suffix_part = f"_{suffix}" if suffix else ""
    fname = f"subpool_balance_{pool}.{subpool}{suffix_part}.png"
    fpath = os.path.join(output_dir, fname)

    plt.savefig(fpath, dpi=300)
    plt.close(fig)

    print(f"Figur lagret til: {fpath}")
