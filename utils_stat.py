"""
Aggregates raw Monte Carlo iteration records into per-flow statistics
(process_and_export_mc_results: central values, 95% intervals, CV%), exports them to
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
    Interactive Plotly time-series plot (HTML) for a single N flow: the
    central value (deterministic run) plus a shaded 95% uncertainty band
    (2.5-97.5 percentile of the MC iterations). Two buttons above the plot switch between the flow in
    kt N/year and per capita in kg N/person/year.
    """
    os.makedirs(output_dir, exist_ok=True)

    df_flow = df_flow.sort_values('year')
    years = df_flow['year']

    # Population on 1 January (SSB 06913). Population is treated as exact, so
    # the percentiles can be divided by it directly.
    pop = population.reindex(years).values
    variants = [
        (df_flow[['p2_5', 'central', 'p97_5']].values, 'kt N/year', 'Nitrogen Flow (kt N / year)', '.3f', True),
        # Significant digits rather than fixed decimals: small flows are well
        # below 0.001 kg N/person/year.
        (df_flow[['p2_5', 'central', 'p97_5']].values * 1.0e6 / pop[:, None],  # kt N -> kg N
         'kg N/person/year', 'Nitrogen Flow (kg N / person / year)', '.3g', False),
    ]

    fig = go.Figure()

    for values, unit, _, fmt, visible in variants:
        p2_5, central, p97_5 = values[:, 0], values[:, 1], values[:, 2]
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
            x=years, y=central, visible=visible,
            mode='lines', line=dict(color='navy', width=2.5),
            name='Central value (deterministic)',
            customdata=np.stack([p2_5, p97_5], axis=-1),
            hovertemplate=(
                "<b>Year: %{x}</b><br>" +
                f"Central value: %{{y:{fmt}}} {unit}<br>" +
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

SANKEY_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plot", "sankey_template.html")

# Pools whose page gets a Sankey diagram of its subpools (plot_pool_sankey_interactive); a pool without
# subpools (HS.HS, AT.AT, RW.RW) is drawn as a single node.
POOL_SANKEYS = ['EF', 'AG', 'MP', 'FS', 'PR', 'HY', 'HS', 'AT', 'RW']

# Columns of the national diagram, left to right; AT and RW appear twice, as
# inputs/imports on the left and emissions/exports on the right.
NATIONAL_SANKEY_COLS = [['AT_in', 'RW_in'], ['FS', 'AG'], ['MP'], ['HS'], ['PR'], ['EF', 'HY'], ['AT_out', 'RW_out']]
NATIONAL_SANKEY_HEADS = ['Inputs', 'Primary production', 'Industry & trade', 'Households', 'Residues', '', 'Outputs']


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


def _sankey_years(df_flows):
    """
    Years shown in the Sankey diagrams: from 1990, and only years where at
    least 90 % of the flows have a value, so a final year with only a handful
    of flows calculated is left out.
    """
    df = df_flows[df_flows['year'] >= 1990]
    counts = df[df['value'].notna()].groupby('year')['flow_name'].nunique()
    years = sorted(counts[counts >= 0.9 * counts.max()].index.astype(int))
    return list(range(years[0], years[-1] + 1))


def _sankey_flow_records(df, years, node_of, name_of, hidden_regex=None):
    """
    One record per flow for the Sankey page: source/target node ids (from
    node_of(source code, is_source)), tooltip name, species and overview
    category, and the central value and 2.5/97.5 percentiles for every year. Flows
    that are zero in all years are left out.
    """
    category_map = _load_flow_categories()
    flows = []
    for flow_name, g in df.groupby('flow_name'):
        g = g.set_index('year').reindex(years)
        values = g['value'].fillna(0.0).clip(lower=0.0)
        if values.max() <= 0:
            continue
        s_code, t_code = extract_source_target(flow_name)
        flows.append({
            's': node_of(s_code, True),
            't': node_of(t_code, False),
            'name': name_of(flow_name, s_code, t_code),
            'sp': _get_species_key(flow_name),
            'cat': category_map.get(flow_name, 'other/unclassified'),
            'hide': bool(hidden_regex and re.search(hidden_regex, flow_name.upper())),
            'v': values.round(4).tolist(),
            'lo': g['p2_5'].fillna(0.0).clip(lower=0.0).round(4).tolist(),
            'hi': g['p97_5'].fillna(0.0).clip(lower=0.0).round(4).tolist(),
        })
    return flows


def _write_sankey_page(data, filename, output_dir):
    """Fills plot/sankey_template.html with data and writes it to output_dir/filename."""
    data = {
        'species': SANKEY_SPECIES_COLORS,
        'categories': SANKEY_CATEGORY_COLORS,
        'hiddenNames': sorted({f['name'] for f in data['flows'] if f['hide']}),
        **data,
    }
    with open(SANKEY_TEMPLATE, encoding='utf-8') as fh:
        html = fh.read().replace('__DATA__', json.dumps(data, separators=(',', ':')))
    out_path = os.path.join(output_dir, filename)
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f"[SUCCESS] Sankey-diagram generert -> {out_path}")
    return filename


def plot_global_sankey_interactive(df_flows, output_dir="output_files/plots"):
    """
    Writes the national pool-level Sankey diagram shown on the report's home
    page (global_nitrogen_sankey.html): one self-contained page, drawn by the
    JavaScript in plot/sankey_template.html, with a year slider, a toggle that
    hides the dominant trade flows (SANKEY_HIDDEN_KEYWORDS), and link
    colouring by N species or by Report.xlsx's overview category. The page
    receives every flow's central value and 2.5/97.5 percentiles; it sums them per
    pool pair itself and keeps the value-to-pixel scale fixed across all
    years.
    """
    os.makedirs(output_dir, exist_ok=True)
    years = _sankey_years(df_flows)

    df = df_flows[df_flows['year'] >= 1990].copy()
    ends = df['flow_name'].apply(extract_source_target)
    df['s'] = [e[0].split('.')[0] for e in ends]
    df['t'] = [e[1].split('.')[0] for e in ends]
    df = df[(df['s'] != df['t']) & df['s'].isin(SANKEY_POOLS) & df['t'].isin(SANKEY_POOLS)]

    def node_of(code, is_source):
        pool = code.split('.')[0]
        return pool + ('_in' if is_source else '_out') if pool in ('AT', 'RW') else pool

    roles = {'AT_in': 'inputs', 'RW_in': 'imports', 'AT_out': 'emissions', 'RW_out': 'exports'}
    nodes = {n: {'name': SANKEY_POOLS[n.split('_')[0]][0], 'color': SANKEY_POOLS[n.split('_')[0]][1],
                 'role': roles.get(n, '')} for col in NATIONAL_SANKEY_COLS for n in col}
    data = {
        'title': 'Sankey diagram of nitrogen flows in Norway',
        'years': years,
        'layout': {'cols': NATIONAL_SANKEY_COLS, 'colHeads': NATIONAL_SANKEY_HEADS,
                   'marginL': 120, 'marginR': 130, 'mainH': 470, 'nodeGap': 16},
        'nodes': nodes,
        'loopNote': 'Flows that go back to an earlier column (e.g. feed and fertilizer to agriculture, '
                    'fish catch to industry) are drawn as loops below the diagram.',
        'flows': _sankey_flow_records(df, years, node_of, lambda fn, s, t: '-'.join(fn.split('-')[2:]),
                                      "|".join(SANKEY_HIDDEN_KEYWORDS)),
    }
    return _write_sankey_page(data, "global_nitrogen_sankey.html", output_dir)


def _subpool_names():
    """Subpool code -> name, from the subpool page titles in report_pages.py, e.g. 'EF.EC' -> 'Energy conversion'."""
    from report_pages import PAGES
    names = {}
    for page in PAGES:
        m = re.match(r'(.*) \((\w+\.\w+)\)$', page['title'])
        if page['kind'] == 'subpool' and m:
            names[m.group(2)] = m.group(1)
    return names


def _subpool_columns(subpools, internal):
    """
    Column (0, 1, ...) of each subpool in a pool diagram. internal maps
    (source, target) subpool pairs to their largest yearly flow. Pairs are
    added largest first as long as they keep the graph acyclic; each subpool
    then sits one column right of its furthest upstream subpool, and the
    pairs left out are drawn as loops back to an earlier column.
    """
    edges = []
    def reaches(a, b):
        stack, seen = [a], set()
        while stack:
            n = stack.pop()
            if n == b:
                return True
            seen.add(n)
            stack += [t for s, t in edges if s == n and t not in seen]
        return False
    for (s, t), _ in sorted(internal.items(), key=lambda kv: -kv[1]):
        if not reaches(t, s):
            edges.append((s, t))
    col = {sp: 0 for sp in subpools}
    for _ in subpools:
        for s, t in edges:
            col[t] = max(col[t], col[s] + 1)
    return col


def plot_pool_sankey_interactive(df_flows, pool, output_dir="output_files/plots"):
    """
    Writes the Sankey diagram for one pool's page (sankey_<pool>.html), with
    the same page as the national diagram: the pool's subpools in the middle,
    flows from other pools on the left and to other pools on the right (other
    pools shown at pool level; the tooltip names their subpool), and the
    flows between the subpools. No flows are hidden.
    """
    os.makedirs(output_dir, exist_ok=True)
    years = _sankey_years(df_flows)

    df = df_flows[df_flows['year'] >= 1990].copy()
    ends = df['flow_name'].apply(extract_source_target)
    df['s'] = [e[0] for e in ends]
    df['t'] = [e[1] for e in ends]
    in_pool_s = df['s'].str.split('.').str[0] == pool
    in_pool_t = df['t'].str.split('.').str[0] == pool
    df = df[(in_pool_s | in_pool_t) & (df['s'] != df['t'])]

    subpools = sorted(set(df.loc[in_pool_s, 's']) | set(df.loc[in_pool_t, 't']))
    internal = df[df['s'].isin(subpools) & df['t'].isin(subpools)].groupby(['s', 't'])['value'].max().to_dict()
    sub_col = _subpool_columns(subpools, internal)
    n_sub_cols = max(sub_col.values()) + 1

    def node_of(code, is_source):
        if code in subpools:
            return code
        return code.split('.')[0] + ('_in' if is_source else '_out')

    def name_of(flow_name, s, t):
        name = '-'.join(flow_name.split('-')[2:])
        other = t if s in subpools else s
        if other in subpools or other.split('.')[0] == other.split('.')[1]:
            return name
        return f"{name} ({'to' if s in subpools else 'from'} {other})"

    flows = _sankey_flow_records(df, years, node_of, name_of)
    used = {f['s'] for f in flows} | {f['t'] for f in flows}
    pool_order = list(SANKEY_POOLS)
    sources = [p + '_in' for p in pool_order if p + '_in' in used]
    targets = [p + '_out' for p in pool_order if p + '_out' in used]
    cols = [sources] + [[sp for sp in subpools if sub_col[sp] == c] for c in range(n_sub_cols)] + [targets]

    names = _subpool_names()
    nodes = {sp: {'name': names.get(sp, SANKEY_POOLS[pool][0]), 'color': SANKEY_POOLS[pool][1], 'role': sp} for sp in subpools}
    for n in sources + targets:
        p = n.split('_')[0]
        nodes[n] = {'name': SANKEY_POOLS[p][0], 'color': SANKEY_POOLS[p][1], 'role': ''}

    data = {
        'title': f'Sankey diagram of nitrogen flows in the {SANKEY_POOLS[pool][0]} pool',
        'years': years,
        'layout': {'cols': cols, 'colHeads': ['From other pools'] + ['Subpools' if len(subpools) > 1 else ''] + [''] * (n_sub_cols - 1) + ['To other pools'],
                   'marginL': 150, 'marginR': 150, 'mainH': 400, 'nodeGap': 34},
        'nodes': nodes,
        'loopNote': 'Flows between subpools that go back to an earlier column are drawn as loops below the diagram.',
        'flows': flows,
    }
    return _write_sankey_page(data, f"sankey_{pool}.html", output_dir)


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
    # The interval comes from the random iterations; sim_id 0 is the
    # deterministic run (the central value), used only if it is the only one.
    use = (sign != 0) & ((df_all['sim_id'] > 0) | (df_all['sim_id'].max() == 0))
    net = signed[use].groupby(['year', 'sim_id'])['signed'].sum()
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

    # 2. Central value and MC statistics. The central value (best estimate) is
    # the deterministic run, sim_id 0. The interval and the other statistics
    # come from the random iterations, sim_id >= 1 (or from sim_id 0 alone in
    # a deterministic-only run).
    print("[STATISTICS] Calculating central values and 95% intervals...")
    is_random = df_all_trimmed['sim_id'] > 0
    df_mc = df_all_trimmed[is_random] if is_random.any() else df_all_trimmed
    central = df_all_trimmed[df_all_trimmed['sim_id'] == 0].set_index(['flow_name', 'year'])['value']
    summary_df = df_mc.groupby(['flow_name', 'year']).agg(
        median=('value', np.median),
        mean=('value', np.mean),
        p2_5=('value', lambda x: np.percentile(x, 2.5)),
        p97_5=('value', lambda x: np.percentile(x, 97.5)),
        std=('value', np.std),
        comment=('comment', 'first'),
        data_sources=('data_sources', 'first')
    ).reset_index()
    summary_df.insert(2, 'central', central.reindex(
        pd.MultiIndex.from_frame(summary_df[['flow_name', 'year']])).to_numpy())
    outside = ((summary_df['central'] < summary_df['p2_5']) | (summary_df['central'] > summary_df['p97_5'])).sum()
    if outside:
        print(f"[STATISTICS] {outside} flow-years have the central value outside the MC 95% interval.")

    # 3. Calculate uncertainty metrics
    summary_df['unc_down_percent'] = np.where(
        summary_df['central'] > 0,
        ((summary_df['central'] - summary_df['p2_5']) / summary_df['central']) * 100,
        0.0
    )
    summary_df['unc_up_percent'] = np.where(
        summary_df['central'] > 0,
        ((summary_df['p97_5'] - summary_df['central']) / summary_df['central']) * 100,
        0.0
    )
    summary_df['cv_percent'] = np.where(
        summary_df['mean'] > 0,
        (summary_df['std'] / summary_df['mean']) * 100,
        0.0
    )
    # Half-width of the 95% CI, expressed as a percentage of the central value - this is the
    # 'relative uncertainty' figure the reporting guidelines define, not the CV above.
    summary_df['uncertainty_percent'] = (summary_df['unc_down_percent'] + summary_df['unc_up_percent']) / 2

    # 4. Export to Excel
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, 'MC_Reporting_Statistics.xlsx')
    
    summary_df_rounded = summary_df.round({
        'central': 4, 'median': 4, 'mean': 4, 'p2_5': 4, 'p97_5': 4, 'std': 4,
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
            df_flow['central'],
            color='navy',
            linewidth=2.5,
            label='Central value (deterministic)'
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
    
    # The balance plots and the Sankey diagram use each flow's central value;
    # the Sankey diagram also reads 'uncertainty' (the flow's standard deviation).
    df_balance_input['value'] = df_balance_input['central']
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
    for pool in POOL_SANKEYS:
        plot_pool_sankey_interactive(df_balance_input, pool, output_dir=plot_dir)
        
    print("\n" + "="*60)
    print("[SUCCESS] All MC iterations processed, statistics saved, and plots generated successfully.")

    return summary_df
