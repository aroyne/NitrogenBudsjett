"""
Aggregates raw Monte Carlo iteration records into per-flow statistics
(process_and_export_mc_results: medians, 95% CIs, CV%), exports them to
MC_Reporting_Statistics.xlsx, and generates the time-series, pool-balance and
Sankey plots used in the GitHub Pages report.
"""
import os
import re
import json
import shutil
import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go
from data_loader import load_population

def plot_pool_balance_interactive(df_flows, pool_code, net_interval, output_dir="output_files/plots"):
    """
    Genererer et INTERAKTIVT og RESPONSIVT balansediagram (HTML) for en spesifikk pool eller subpool.
    Inngående strømmer stables oppover (positive), utgående strømmer stables nedover (negative).
    Viser KUN info for strømmen musen er nærmest.

    net_interval: (lower, upper) Series by year, the 2.5-97.5 percentiles of
    the pool's net balance computed within each MC iteration (see
    _net_balance_interval).
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Filtrer ut inngående og utgående strømmer for denne poolen
    df_in = df_flows[df_flows['target'].str.startswith(pool_code, na=False)]
    df_out = df_flows[df_flows['source'].str.startswith(pool_code, na=False)]
    
    if df_in.empty and df_out.empty:
        print(f"[WARN] Ingen data funnet for pool-balanse: {pool_code}")
        return None

    # Sørg for at alle årstall er synkronisert
    all_years = sorted(list(set(df_flows['year'])))
    
    # Grupper per år og fullt flomnavn
    df_in_grouped = df_in.groupby(['year', 'flow_name'])['value'].sum().unstack(fill_value=0).reindex(all_years, fill_value=0)
    df_out_grouped = df_out.groupby(['year', 'flow_name'])['value'].sum().unstack(fill_value=0).reindex(all_years, fill_value=0)
    
    net_balance = df_in_grouped.sum(axis=1) - df_out_grouped.sum(axis=1)
    band_lo = net_interval[0].reindex(all_years)
    band_hi = net_interval[1].reindex(all_years)

    # Opprett tom Plotly-figur
    fig = go.Figure()

    # --- 2. STACK INNGÅENDE STRØMMER (Positive) ---
    for col in df_in_grouped.columns:
        fig.add_trace(go.Scatter(
            x=all_years,
            y=df_in_grouped[col],
            mode='lines',
            name=f"IN: {col}",
            stackgroup='one',  
            groupnorm='',      
            hovertemplate=(
                f"<b>IN: {col}</b><br>" +
                "År: %{x}<br>" +
                "Verdi: %{y:.3f} kt N/year<br>" +
                "<extra></extra>"  
            ),
            legendgroup="Inngående",
            legendgrouptitle_text="══ SYSTEM INFLOW ══"
        ))

    # --- 3. STACK UTGÅENDE STRØMMER (Negative) ---
    for col in df_out_grouped.columns:
        fig.add_trace(go.Scatter(
            x=all_years,
            y=-df_out_grouped[col], 
            mode='lines',
            name=f"OUT: {col}",
            stackgroup='two',  
            hovertemplate=(
                f"<b>OUT: {col}</b><br>" +
                "År: %{x}<br>" +
                "Verdi: %{text:.3f} kt N/year<br>" + 
                "<extra></extra>"
            ),
            text=df_out_grouped[col], 
            legendgroup="Utgående",
            legendgrouptitle_text="══ SYSTEM OUTFLOW ══"
        ))

    # --- 4. USIKKERHETSBÅND ---
    fig.add_trace(go.Scatter(
        x=all_years,
        y=band_hi,
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=all_years,
        y=band_lo,
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(0, 0, 0, 0.12)',
        name='95% interval (MC)',
        hoverinfo='skip',
        legendgroup="Netto",
        legendgrouptitle_text="══ NET BALANCE ══"
    ))

    # --- 5. NETTO BALANSELINJE ---
    fig.add_trace(go.Scatter(
        x=all_years,
        y=net_balance,
        mode='lines',
        line=dict(color='black', width=3),
        name='Net Balance (Inn - Ut)',
        hovertemplate=(
            "<b>Net Balance</b><br>" +
            "År: %{x}<br>" +
            "Netto: %{y:.3f} kt N/year<br>" +
            "95% interval: %{customdata[0]:.3f} – %{customdata[1]:.3f}<br>" +
            "<extra></extra>"
        ),
        customdata=np.stack([band_lo.values, band_hi.values], axis=-1),
        legendgroup="Netto"
    ))

    # --- 6. LAYOUT OG STYLING ---
    fig.update_layout(
        title=dict(
            text=f"Mass Balance Overview: {pool_code}",
            font=dict(size=16, family="Arial, sans-serif", color="black")
        ),
        xaxis=dict(
            title="Year",
            range=[1990, 2024],
            tickmode='array',
            tickvals=list(np.arange(1990, 2021, 5)) + [2024],
            gridcolor='rgba(200, 200, 200, 0.4)',
            showspikes=True,      
            spikethickness=1,
            spikedash="dot",
            spikemode="across"
        ),
        yaxis=dict(
            title="Nitrogen Flow (kt N / year)",
            gridcolor='rgba(200, 200, 200, 0.4)',
            zeroline=True,
            zerolinecolor='gray',
            zerolinewidth=1
        ),
        # "closest" isolates the hover tooltip to only the trace under the cursor.
        hovermode="closest",
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            x=1.02, # Plassert rett utenfor plottet
            y=1.0,
            xanchor='left',
            yanchor='top',
            font=dict(size=10),
            traceorder="grouped" 
        ),
        # Wide right margin (r=180) makes room for the legend.
        margin=dict(l=60, r=180, t=60, b=50),
        height=600
    )

    # Lagre med default_width='100%' for full responsivitet i iframes
    plot_filename = f"balance_{pool_code.replace('.', '_')}.html"
    filepath = os.path.join(output_dir, plot_filename)
    fig.write_html(filepath, include_plotlyjs='cdn', default_width='100%')
    
    print(f"[INFO] Interaktivt balanseplott generert for {pool_code} -> {filepath}")
    return plot_filename


def plot_flow_timeseries_interactive(df_flow, flow_name, population, output_dir="output_files/plots"):
    """
    Interactive Plotly time-series plot (HTML) for a single N flow: median line
    (most likely value) plus a shaded 95% uncertainty band (2.5-97.5
    percentile). Two buttons above the plot switch between the flow in
    kt N/year and per capita in kg N/person/year.
    """
    os.makedirs(output_dir, exist_ok=True)

    df_flow = df_flow.sort_values('year')
    years = df_flow['year']

    # Population on 1 January (SSB 06913). Population is treated as exact, so
    # the percentiles can be divided by it directly.
    pop = population.reindex(years).values
    variants = [
        (df_flow[['p2_5', 'median', 'p97_5']].values, 'kt N/year', 'Nitrogen Flow (kt N / year)', '.3f', True),
        # Significant digits rather than fixed decimals: small flows are well
        # below 0.001 kg N/person/year.
        (df_flow[['p2_5', 'median', 'p97_5']].values * 1.0e6 / pop[:, None],  # kt N -> kg N
         'kg N/person/year', 'Nitrogen Flow (kg N / person / year)', '.3g', False),
    ]

    fig = go.Figure()

    for values, unit, _, fmt, visible in variants:
        p2_5, median, p97_5 = values[:, 0], values[:, 1], values[:, 2]
        fig.add_trace(go.Scatter(
            x=years, y=p97_5, visible=visible,
            mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=years, y=p2_5, visible=visible,
            mode='lines', line=dict(width=0), fill='tonexty',
            fillcolor='rgba(70, 130, 180, 0.3)',
            name='95% Confidence Interval (MC)',
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=years, y=median, visible=visible,
            mode='lines', line=dict(color='navy', width=2.5),
            name='Median (most likely value)',
            customdata=np.stack([p2_5, p97_5], axis=-1),
            hovertemplate=(
                "<b>Year: %{x}</b><br>" +
                f"Most likely value: %{{y:{fmt}}} {unit}<br>" +
                f"95% interval: %{{customdata[0]:{fmt}}} – %{{customdata[1]:{fmt}}} {unit}" +
                "<extra></extra>"
            )
        ))

    n_traces = 3
    buttons = [
        dict(label=unit, method='update',
             args=[{'visible': [j == i for j in range(len(variants)) for _ in range(n_traces)]},
                   {'yaxis.title.text': axis_title}])
        for i, (_, unit, axis_title, _, _) in enumerate(variants)
    ]

    fig.update_layout(
        title=dict(text=flow_name, font=dict(size=13, family="Arial, sans-serif", color="black"),
                   y=0.97, yanchor='top'),
        xaxis=dict(
            title="Year", range=[1984, 2025],
            gridcolor='rgba(200, 200, 200, 0.4)',
            showspikes=True, spikethickness=1, spikedash="dot", spikemode="across"
        ),
        yaxis=dict(
            title=variants[0][2],
            gridcolor='rgba(200, 200, 200, 0.4)',
            rangemode='tozero'
        ),
        updatemenus=[dict(
            type='buttons', direction='right', buttons=buttons, active=0,
            x=1.0, xanchor='right', y=1.02, yanchor='bottom',
            pad=dict(r=0, t=0), font=dict(size=10),
            bgcolor='white', bordercolor='rgba(150, 150, 150, 0.6)'
        )],
        hovermode="closest",
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(x=0.01, y=0.99, xanchor='left', yanchor='top', font=dict(size=10)),
        margin=dict(l=60, r=20, t=70, b=45),
        height=380
    )

    safe_filename = flow_name.replace('.', '_').replace('-', '_').replace(' ', '_') + '.html'
    filepath = os.path.join(output_dir, safe_filename)
    fig.write_html(filepath, include_plotlyjs='cdn', default_width='100%')
    return safe_filename


def plot_pool_balance(df_flows, pool_code, net_interval, output_dir="output_files/plots"):
    """
    Genererer et balansediagram for en spesifikk pool eller subpool.
    Deler legenden inn i to ryddige blokker: "Inngående strømmer" og "Utgående strømmer",
    og viser den fulle flomkoden (flow_name) for hver strøm.
    Rekkefølgen i legendene matcher stablingen i plottet (visuelt ovenfra og ned).

    net_interval: (lower, upper) Series by year, the 2.5-97.5 percentiles of
    the pool's net balance computed within each MC iteration (see
    _net_balance_interval).
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. Filtrer ut inngående og utgående strømmer for denne poolen
    df_in = df_flows[df_flows['target'].str.startswith(pool_code, na=False)]
    df_out = df_flows[df_flows['source'].str.startswith(pool_code, na=False)]
    
    if df_in.empty and df_out.empty:
        print(f"[WARN] Ingen data funnet for pool-balanse: {pool_code}")
        return None

    # 2. Grupper per år og fullt flomnavn (flow_name) for stacking
    df_in_grouped = df_in.groupby(['year', 'flow_name'])['value'].sum().unstack(fill_value=0)
    df_out_grouped = df_out.groupby(['year', 'flow_name'])['value'].sum().unstack(fill_value=0)
    
    # Sørg for at alle årstall er synkronisert (1984-2025)
    all_years = sorted(list(set(df_flows['year'])))
    df_in_grouped = df_in_grouped.reindex(all_years, fill_value=0)
    df_out_grouped = df_out_grouped.reindex(all_years, fill_value=0)

    # 3. Beregn netto balanse og usikkerhetsbåndet
    total_in = df_in_grouped.sum(axis=1)
    total_out = df_out_grouped.sum(axis=1)
    net_balance = total_in - total_out
    band_lo = net_interval[0].reindex(all_years)
    band_hi = net_interval[1].reindex(all_years)

    # 4. Plottingen
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    
    # Lagre plot-objekter (handles) for å kunne bygge legendene manuelt etterpå
    in_handles = []
    out_handles = []
    
    # Stack inngående (Positive verdier)
    if not df_in_grouped.empty:
        # stackplot returnerer en liste med PolyCollection-objekter (ett for hvert lag)
        polys_in = ax.stackplot(all_years, df_in_grouped.values.T, alpha=0.7)
        in_handles = list(polys_in)
    
    # Stack utgående (Negative verdier)
    if not df_out_grouped.empty:
        polys_out = ax.stackplot(all_years, (-df_out_grouped).values.T, alpha=0.7)
        out_handles = list(polys_out)
    
    # Tegn den svarte balanselinjen og usikkerhetsbåndet
    line_balance, = ax.plot(all_years, net_balance, color='black', linewidth=2, zorder=5)
    poly_unc = ax.fill_between(all_years, band_lo, band_hi, 
                               color='black', alpha=0.12, zorder=4, linestyle='--')
    
    # Styling av akser
    ax.axhline(0, color='gray', linestyle='-', linewidth=0.8, zorder=3)
    ax.set_title(f"Mass Balance Overview: {pool_code}", fontsize=12, fontweight='bold', loc='left')
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Nitrogen Flow (kt N / year)", fontsize=10)
    
    # --- AKSEBEGRENSNINGER ---
    ax.set_xlim(1990, 2024)
    custom_ticks = list(np.arange(1990, 2021, 5)) + [2024]
    ax.set_xticks(custom_ticks)
    ax.grid(True, linestyle='--', alpha=0.4)

    # ========================================================
    # AVANSERT LEGEND-HÅNDTERING MED KORREKT VISUELL REKKEFØLGE
    # ========================================================
    
    # 1. Hent de opprinnelige merkelappene kronologisk fra DataFrame-kolonnene
    in_labels = list(df_in_grouped.columns)
    out_labels = list(df_out_grouped.columns)
    
    # Sortering for Inngående (Positive):
    # Siste kolonne ligger øverst i plottet, så vi reverserer listene 
    # for å få den øverst i den øverste legend-blokken.
    in_handles_sorted = list(reversed(in_handles))
    in_labels_sorted = list(reversed(in_labels))
    
    # Sortering for Utgående (Negative):
    # Siste kolonne pushes lengst NED i plottet (bort fra 0). 
    # Ved å beholde den opprinnelige rekkefølgen havner den også nederst i legend-blokken.
    out_handles_sorted = out_handles
    out_labels_sorted = out_labels
    
    # 2. Opprett den første legenden for INNGÅENDE (øverst til høyre)
    # Vi inkluderer Net Balance og Uncertainty øverst i denne blokken
    top_handles = [line_balance, poly_unc] + in_handles_sorted
    top_labels = ['Net Balance (Inn - Ut)', '95% interval (MC)'] + in_labels_sorted
    
    legend_in = ax.legend(
        top_handles, 
        top_labels, 
        bbox_to_anchor=(1.05, 1.0), 
        loc='upper left', 
        fontsize=8, 
        title="══ SYSTEM INFLOW & NET ══",
        title_fontsize=9,
        frameon=True
    )
    legend_in._legend_box.align = "left"
    ax.add_artist(legend_in)
    
    # 3. Opprett den andre legenden for UTGÅENDE (plassert under den første)
    if out_handles_sorted:
        # Dynamisk plassering basert på antall inngående strømmer
        approx_offset = max(0.0, 0.55 - (len(in_labels) * 0.03))
        
        legend_out = ax.legend(
            out_handles_sorted, 
            out_labels_sorted, 
            bbox_to_anchor=(1.05, approx_offset), 
            loc='upper left', 
            fontsize=8, 
            title="══ SYSTEM OUTFLOW ══",
            title_fontsize=9,
            frameon=True
        )
        legend_out._legend_box.align = "left"

    plt.tight_layout()
    
    # Lagre filen
    plot_filename = f"balance_{pool_code.replace('.', '_')}.png"
    filepath = os.path.join(output_dir, plot_filename)
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    
    print(f"[INFO] Balanseplott generert for {pool_code} -> {filepath}")
    return plot_filename

SANKEY_SPECIES_COLORS = {
    'Nmix': "rgba(76, 175, 80, 0.6)",
    'N2': "rgba(140, 140, 140, 0.6)",
    'NH3 / RDN': "rgba(255, 152, 0, 0.6)",
    'NOx / OXN': "rgba(244, 67, 54, 0.6)",
    'N2O': "rgba(156, 39, 176, 0.6)",
}

SANKEY_CATEGORY_COLORS = {
    'useful output': "rgba(76, 175, 80, 0.6)",
    'N wasted': "rgba(244, 67, 54, 0.6)",
    'import': "rgba(33, 150, 243, 0.6)",
    'recycling': "rgba(255, 152, 0, 0.6)",
    'other/unclassified': "rgba(160, 160, 160, 0.6)",
}

SANKEY_POOLS = {
    "AT": ("Atmosphere", "#1a365d"),
    "RW": ("Rest of the world", "#4a5568"),
    "AG": ("Agriculture", "#2f855a"),
    "FS": ("Forests & semi-natural", "#2c7a7b"),
    "MP": ("Materials & products", "#d69e2e"),
    "HS": ("Humans & settlements", "#744210"),
    "PR": ("Processing of residues", "#97266d"),
    "EF": ("Energy & fuels", "#c53030"),
    "HY": ("Hydrosphere", "#2b6cb0"),
}

# Flow name keywords for the dominant trade flows that the "hide" view of the
# Sankey diagram leaves out, so the smaller internal flows become legible.
SANKEY_HIDDEN_KEYWORDS = ["AMMONIA IMPORT", "AMMONIA EXPORT", "AMMONIA SYNTHESIS", "FERTILIZER EXPORT", "FUEL EXPORT"]

SANKEY_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plot", "national_sankey_template.html")


def _get_species_key(flow_name):
    """Species group of a flow, from the species suffix of its flow code (e.g. '...-N2O')."""
    species = flow_name.strip().split('-')[-1].strip()
    if species in ('NH3', 'RDN'):
        return 'NH3 / RDN'
    if species in ('NOx', 'OXN'):
        return 'NOx / OXN'
    return species


def _load_flow_categories(report_path='Report.xlsx', sheet_name='2a. Database N flows'):
    """
    Loads the manually-maintained flow -> overview-category mapping from the
    official Report.xlsx template ('2a. Database N flows', column C = flow
    code, column U = overViewType: useful output / N wasted / import /
    recycling / -), keyed by flow code. The two spellings of 'N wasted' found
    in the template ('N wasted' and 'N wastedd') are merged into one category.
    """
    category_map = {}
    if not os.path.exists(report_path):
        return category_map
    wb_report = openpyxl.load_workbook(report_path, data_only=True)
    if sheet_name not in wb_report.sheetnames:
        return category_map
    sheet = wb_report[sheet_name]
    for row in range(3, sheet.max_row + 1):
        code = sheet.cell(row=row, column=3).value
        raw_cat = sheet.cell(row=row, column=21).value
        if code is None or raw_cat is None:
            continue
        cat = str(raw_cat).strip()
        if cat.lower() in ('n wasted', 'n wastedd'):
            cat = 'N wasted'
        elif cat == '-':
            cat = 'other/unclassified'
        category_map[str(code).strip()] = cat
    return category_map


def plot_global_sankey_interactive(df_flows, output_dir="output_files/plots"):
    """
    Writes the national pool-level Sankey diagram shown on the report's home
    page (global_nitrogen_sankey.html): one self-contained page, drawn by the
    JavaScript in plot/national_sankey_template.html, with a year slider, a
    toggle that hides the dominant trade flows (SANKEY_HIDDEN_KEYWORDS), and
    link colouring by N species or by Report.xlsx's overview category.

    Only years where at least 90 % of the flows have a value are included, so
    a final year with only a handful of flows calculated is left out. The
    page receives every flow's median and 2.5/97.5 percentiles; it sums them
    per pool pair itself and keeps the value-to-pixel scale fixed across all
    years.
    """
    os.makedirs(output_dir, exist_ok=True)

    df = df_flows[df_flows['year'] >= 1990].copy()
    ends = df['flow_name'].apply(extract_source_target)
    df['s'] = [e[0].split('.')[0] for e in ends]
    df['t'] = [e[1].split('.')[0] for e in ends]
    df = df[(df['s'] != df['t']) & df['s'].isin(SANKEY_POOLS) & df['t'].isin(SANKEY_POOLS)]

    counts = df[df['value'].notna()].groupby('year')['flow_name'].nunique()
    years = sorted(counts[counts >= 0.9 * counts.max()].index.astype(int))
    years = list(range(years[0], years[-1] + 1))

    category_map = _load_flow_categories()
    hidden_regex = "|".join(SANKEY_HIDDEN_KEYWORDS)
    flows = []
    for flow_name, g in df.groupby('flow_name'):
        g = g.set_index('year').reindex(years)
        values = g['value'].fillna(0.0).clip(lower=0.0)
        if values.max() <= 0:
            continue
        flows.append({
            's': g['s'].dropna().iloc[0],
            't': g['t'].dropna().iloc[0],
            'name': '-'.join(flow_name.split('-')[2:]),
            'sp': _get_species_key(flow_name),
            'cat': category_map.get(flow_name, 'other/unclassified'),
            'hide': bool(re.search(hidden_regex, flow_name.upper())),
            'v': values.round(4).tolist(),
            'lo': g['p2_5'].fillna(0.0).clip(lower=0.0).round(4).tolist(),
            'hi': g['p97_5'].fillna(0.0).clip(lower=0.0).round(4).tolist(),
        })

    data = {
        'years': years,
        'pools': {code: {'name': name, 'color': color} for code, (name, color) in SANKEY_POOLS.items()},
        'species': SANKEY_SPECIES_COLORS,
        'categories': SANKEY_CATEGORY_COLORS,
        'hiddenNames': sorted({f['name'] for f in flows if f['hide']}),
        'flows': flows,
    }
    with open(SANKEY_TEMPLATE, encoding='utf-8') as fh:
        html = fh.read().replace('__DATA__', json.dumps(data, separators=(',', ':')))
    out_path = os.path.join(output_dir, "global_nitrogen_sankey.html")
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f"[SUCCESS] Sankey-diagram generert -> {out_path}")
    return "global_nitrogen_sankey.html"


def extract_source_target(flow_name):
    """
    Splits a flow_code like 'AG.MM-AT.AT-Emissions-N2O' into its source and
    target sub-pool codes ('AG.MM', 'AT.AT'). Every flow_name produced by the
    calculations/ modules uses this hyphenated format.
    """
    fn = flow_name.upper().strip()
    parts = fn.split('-')
    return parts[0].strip(), parts[1].strip()


def _net_balance_interval(df_all, source, target, pool_code, lo=2.5, hi=97.5):
    """
    2.5-97.5 percentiles, by year, of a pool's or sub-pool's net balance
    (inflows minus outflows) computed within each MC iteration. Summing the
    flows inside each iteration keeps the correlation between them - shared
    parameters, and flows derived from each other such as mass-balance
    residuals - which a band built from each flow's standard deviation in
    quadrature would ignore. Flows are selected with the same rule as the
    balance plots: for a top-level pool, main-pool codes with internal flows
    between its own sub-pools removed; for a sub-pool, its full code.
    source/target: each row's source and target sub-pool codes (as from
    extract_source_target), split once for all pools by the caller.
    """
    if '.' not in pool_code:
        source = source.str.split('.').str[0]
        target = target.str.split('.').str[0]
        keep = source != target
    else:
        keep = pd.Series(True, index=df_all.index)
    sign = (target.str.startswith(pool_code) & keep).astype(float) - (source.str.startswith(pool_code) & keep).astype(float)
    signed = df_all.assign(signed=df_all['value'].fillna(0.0) * sign)
    net = signed[sign != 0].groupby(['year', 'sim_id'])['signed'].sum()
    q = net.groupby(level='year').quantile([lo / 100, hi / 100]).unstack()
    return q.iloc[:, 0], q.iloc[:, 1]


def process_and_export_mc_results(all_records):
    """
    Receives a list of dictionaries from ALL MC iterations.
    Calculates statistics, exports to Excel, and generates plots.
    """
    if not all_records:
        print("[WARNING] No records available to process.")
        return

    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "="*60)
    print("[STATISTICS] Starting statistical analysis of MC results...")
    print(f"[DEBUG] Processing run at: {current_time_str}")
    
    # 1. Convert to DataFrame and clean data types
    df_all = pd.DataFrame(all_records)
    df_all['value'] = pd.to_numeric(df_all['value'], errors='coerce')
    
    total_simulations = df_all['sim_id'].nunique()
    print(f"[STATISTICS] Detected {total_simulations} unique Monte Carlo iterations.")
    
    trimmed_chunks = []
    unique_flows = df_all['flow_name'].unique()
    
    print("[STATISTICS] Analyzing and trimming time intervals per flow...")
    
    for flow in unique_flows:
        df_flow = df_all[df_all['flow_name'] == flow]

        years_with_data = df_flow[df_flow['value'].notna()]['year'].unique().tolist()
        
        if not years_with_data:
            print(f"  [INFO] Flow '{flow}' has no data in the entire period. Skipping.")
            continue
            
        start_year = min(years_with_data)
        end_year = max(years_with_data)

        expected_years = set(range(start_year, end_year + 1))
        missing_years = expected_years - set(years_with_data)

        if missing_years:
            raise ValueError(
                f"Flow '{flow}' has missing data gaps within its own active range "
                f"({start_year}-{end_year}): {sorted(missing_years)}."
            )

        df_trimmed = df_flow[(df_flow['year'] >= start_year) & (df_flow['year'] <= end_year)].copy()
        trimmed_chunks.append(df_trimmed)

    if not trimmed_chunks:
        print("[ABORTED] No flows contained valid data after trimming intervals.")
        return
        
    df_all_trimmed = pd.concat(trimmed_chunks, ignore_index=True)

    # 2. Calculate statistics across all sim_ids
    print("[STATISTICS] Calculating medians and 95% confidence intervals...")
    summary_df = df_all_trimmed.groupby(['flow_name', 'year']).agg(
        median=('value', np.median),
        mean=('value', np.mean),
        p2_5=('value', lambda x: np.percentile(x, 2.5)),
        p97_5=('value', lambda x: np.percentile(x, 97.5)),
        std=('value', np.std),
        comment=('comment', 'first'),
        data_sources=('data_sources', 'first')
    ).reset_index()

    # 3. Calculate uncertainty metrics
    summary_df['unc_down_percent'] = np.where(
        summary_df['median'] > 0, 
        ((summary_df['median'] - summary_df['p2_5']) / summary_df['median']) * 100, 
        0.0
    )
    summary_df['unc_up_percent'] = np.where(
        summary_df['median'] > 0, 
        ((summary_df['p97_5'] - summary_df['median']) / summary_df['median']) * 100, 
        0.0
    )
    summary_df['cv_percent'] = np.where(
        summary_df['mean'] > 0,
        (summary_df['std'] / summary_df['mean']) * 100,
        0.0
    )
    # Half-width of the 95% CI, expressed as a percentage of the median - this is the
    # 'relative uncertainty' figure the reporting guidelines define, not the CV above.
    summary_df['uncertainty_percent'] = (summary_df['unc_down_percent'] + summary_df['unc_up_percent']) / 2

    # 4. Export to Excel
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, 'MC_Reporting_Statistics.xlsx')
    
    summary_df_rounded = summary_df.round({
        'median': 4, 'mean': 4, 'p2_5': 4, 'p97_5': 4, 'std': 4,
        'unc_down_percent': 2, 'unc_up_percent': 2, 'cv_percent': 2, 'uncertainty_percent': 2
    })
    summary_df_rounded.to_excel(excel_path, index=False)
    print(f"[SUCCESS] Statistical report saved to: {excel_path}")

    # 5. GENERATE TIME-SERIES PLOTS
    plot_dir = os.path.join(output_dir, 'plots')
    
    if os.path.exists(plot_dir):
        print(f"[PLOTTING] Cleaning old directory '{plot_dir}' to avoid stale generation leaks...")
        shutil.rmtree(plot_dir)
    os.makedirs(plot_dir, exist_ok=True)

    print("[PLOTTING] Generating fresh time-series plots for each nitrogen flow...")
    population = load_population()

    for flow in summary_df['flow_name'].unique():
        df_flow = summary_df[summary_df['flow_name'] == flow].sort_values('year')
        
        plt.figure(figsize=(10, 3.6))
        
        plt.fill_between(
            df_flow['year'], 
            df_flow['p2_5'], 
            df_flow['p97_5'], 
            color='skyblue', 
            alpha=0.4, 
            label='95% Confidence Interval (MC)'
        )
        plt.plot(df_flow['year'], df_flow['p2_5'], color='steelblue', linestyle=':', linewidth=1, alpha=0.7)
        plt.plot(df_flow['year'], df_flow['p97_5'], color='steelblue', linestyle=':', linewidth=1, alpha=0.7)
        
        plt.plot(
            df_flow['year'], 
            df_flow['median'], 
            color='navy', 
            linewidth=2.5, 
            label='Median (50th percentile)'
        )
        
        flow_start = df_flow['year'].min()
        flow_end = df_flow['year'].max()
        
        plt.title(f"{flow}", fontsize=11, fontweight='bold', loc='left')        
        plt.xlim(1984, 2025)
        plt.xticks(np.arange(1984, 2026, 5))
        
        plt.ylim(bottom=0)
        current_ymax = plt.ylim()[1]
        plt.ylim(top=current_ymax * 1.15 if current_ymax > 0 else 10)
        
        plt.text(1985, plt.ylim()[1] * 0.05, 
                 f"Data Range: {flow_start}-{flow_end}", 
                 fontsize=9, style='italic', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        plt.text(2024.5, plt.ylim()[1] * 0.05, 
                 f"Updated: {current_time_str}", 
                 fontsize=8, color='gray', ha='right', style='italic')
        
        plt.xlabel("Year", fontsize=10)
        plt.ylabel("Nitrogen Flow (kt N / year)", fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.legend(loc='upper left')
        
        safe_filename = flow.replace('.', '_').replace('-', '_').replace(' ', '_') + '.png'
        plt.savefig(os.path.join(plot_dir, safe_filename), dpi=150, bbox_inches='tight')
        plt.close()

        plot_flow_timeseries_interactive(df_flow, flow, population, output_dir=plot_dir)

    # ========================================================
    # INTEGRASJON: GENERERING AV BALANSEPLOTT FOR POOLER
    # ========================================================
    print("\n[PLOTTING] Preparing mass balance datasets for pools and subpools...")
    
    df_balance_input = summary_df.copy()
    
    # Assigns source/target pools using the module-level extract_source_target helper.
    res = df_balance_input['flow_name'].apply(extract_source_target)
    df_balance_input['source'] = [r[0] for r in res]
    df_balance_input['target'] = [r[1] for r in res]
    
    # The balance plots use each flow's median; the Sankey diagram also reads
    # 'uncertainty' (the flow's standard deviation).
    df_balance_input['value'] = df_balance_input['median']
    df_balance_input['uncertainty'] = df_balance_input['std']
    
    # 2. Hent ut alle unike pool-koder som faktisk er til stede i dataene
    all_codes = set(df_balance_input['source'].unique()) | set(df_balance_input['target'].unique())
    all_codes.discard('Unknown')
    
    pools_to_plot = sorted(list(all_codes))
    
    # Automatisk finn og legg til overordnede hovedpooler (f.eks. 'AG' fra 'AG.MM', 'HY' fra 'HY.SW')
    main_pools = set()
    for p in pools_to_plot:
        if '.' in p:
            main_code = p.split('.')[0]
            main_pools.add(main_code)
            
    for main_code in main_pools:
        if main_code not in pools_to_plot:
            pools_to_plot.append(main_code)
            
    pools_to_plot.sort()

    print(f"[PLOTTING] Detected active pools for balance plots: {pools_to_plot}")
    
    # Source/target sub-pool codes for every MC record, split once here rather
    # than inside _net_balance_interval for each pool.
    flow_ends = df_all_trimmed['flow_name'].str.upper().str.strip().str.split('-', n=2, expand=True)
    flow_source = flow_ends[0].str.strip()
    flow_target = flow_ends[1].str.strip()

    print("[PLOTTING] Executing balance plots for active system pools...")
    for pool in pools_to_plot:
        # Lag en kopi av dataene for denne spesifikke iterasjonen
        df_temppool = df_balance_input.copy()
        
        # Hvis vi plotter en hovedpool (f.eks. 'AG' eller 'HY' uten punktum)
        if '.' not in pool:
            # Endre source/target til å bare være hovedkoden (før punktum)
            df_temppool['source_main'] = df_temppool['source'].apply(lambda x: x.split('.')[0])
            df_temppool['target_main'] = df_temppool['target'].apply(lambda x: x.split('.')[0])
            
            # Filtrer ut interne strømmer (f.eks. AG.MM til AG.SM blir intern for AG og skal bort)
            df_temppool = df_temppool[df_temppool['source_main'] != df_temppool['target_main']]
            
            # Forbered kolonner for plottefunksjonen slik at startswith(pool) fungerer
            df_temppool['source'] = df_temppool['source_main']
            df_temppool['target'] = df_temppool['target_main']
            
        net_interval = _net_balance_interval(df_all_trimmed, flow_source, flow_target, pool)
        plot_pool_balance(df_temppool, pool, net_interval, output_dir=plot_dir)
        plot_pool_balance_interactive(df_temppool, pool, net_interval, output_dir=plot_dir)

    print("\n[PLOTTING] Generating global interactive Sankey diagram across all years...")
    plot_global_sankey_interactive(df_balance_input, output_dir=plot_dir)
        
    print("\n" + "="*60)
    print("[SUCCESS] All MC iterations processed, statistics saved, and plots generated successfully.")

    return summary_df
