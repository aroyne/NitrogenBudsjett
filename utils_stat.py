import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go

def plot_pool_balance_interactive(df_flows, pool_code, output_dir="output_files/plots"):
    """
    Genererer et INTERAKTIVT og RESPONSIVT balansediagram (HTML) for en spesifikk pool eller subpool.
    Inngående strømmer stables oppover (positive), utgående strømmer stables nedover (negative).
    Viser KUN info for strømmen musen er nærmest.
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
    
    # Beregn netto balanse og akkumulert usikkerhet
    df_in_total_unc = df_in.groupby('year')['uncertainty'].apply(lambda x: np.sqrt((x**2).sum())).reindex(all_years, fill_value=0)
    df_out_total_unc = df_out.groupby('year')['uncertainty'].apply(lambda x: np.sqrt((x**2).sum())).reindex(all_years, fill_value=0)
    
    net_balance = df_in_grouped.sum(axis=1) - df_out_grouped.sum(axis=1)
    combined_unc = np.sqrt(df_in_total_unc**2 + df_out_total_unc**2)

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
        y=net_balance + combined_unc,
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scatter(
        x=all_years,
        y=net_balance - combined_unc,
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(0, 0, 0, 0.12)',
        name='Uncertainty (±1σ)',
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
            "Usikkerhet: ±%{text:.3f}<br>" +
            "<extra></extra>"
        ),
        text=combined_unc,
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
            range=[1990, 2023],
            tickmode='array',
            tickvals=list(np.arange(1990, 2021, 5)) + [2023],
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
        # --- FIX 2: "closest" isolerer hoveren til kun det sporet du rører ---
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
        # --- FIX 1: Fjernet width=1000, økt høyremargin (r=180) for å romme legend ---
        margin=dict(l=60, r=180, t=60, b=50),
        height=600
    )

    # Lagre med default_width='100%' for full responsivitet i iframes
    plot_filename = f"balance_{pool_code.replace('.', '_')}.html"
    filepath = os.path.join(output_dir, plot_filename)
    fig.write_html(filepath, include_plotlyjs='cdn', default_width='100%')
    
    print(f"[INFO] Interaktivt balanseplott generert for {pool_code} -> {filepath}")
    return plot_filename


def plot_pool_balance(df_flows, pool_code, output_dir="output_files/plots"):
    """
    Genererer et balansediagram for en spesifikk pool eller subpool.
    Deler legenden inn i to ryddige blokker: "Inngående strømmer" og "Utgående strømmer",
    og viser den fulle flomkoden (flow_name) for hver strøm.
    Rekkefølgen i legendene matcher stablingen i plottet (visuelt ovenfra og ned).
    """
    import os
    import numpy as np
    import matplotlib.pyplot as plt

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
    
    # Hent usikkerhetene (kvadratrot av summen av kvadrater)
    df_in_unc = df_in.groupby('year')['uncertainty'].apply(lambda x: np.sqrt((x**2).sum()))
    df_out_unc = df_out.groupby('year')['uncertainty'].apply(lambda x: np.sqrt((x**2).sum()))
    
    # Sørg for at alle årstall er synkronisert (1984-2025)
    all_years = sorted(list(set(df_flows['year'])))
    df_in_grouped = df_in_grouped.reindex(all_years, fill_value=0)
    df_out_grouped = df_out_grouped.reindex(all_years, fill_value=0)
    df_in_unc = df_in_unc.reindex(all_years, fill_value=0)
    df_out_unc = df_out_unc.reindex(all_years, fill_value=0)

    # 3. Beregn netto balanse og akkumulert usikkerhet
    total_in = df_in_grouped.sum(axis=1)
    total_out = df_out_grouped.sum(axis=1)
    net_balance = total_in - total_out
    
    combined_unc = np.sqrt(df_in_unc**2 + df_out_unc**2)

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
    poly_unc = ax.fill_between(all_years, net_balance - combined_unc, net_balance + combined_unc, 
                               color='black', alpha=0.12, zorder=4, linestyle='--')
    
    # Styling av akser
    ax.axhline(0, color='gray', linestyle='-', linewidth=0.8, zorder=3)
    ax.set_title(f"Mass Balance Overview: {pool_code}", fontsize=12, fontweight='bold', loc='left')
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Nitrogen Flow (kt N / year)", fontsize=10)
    
    # --- AKSEBEGRENSNINGER ---
    ax.set_xlim(1990, 2023)
    custom_ticks = list(np.arange(1990, 2021, 5)) + [2023]
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
    top_labels = ['Net Balance (Inn - Ut)', 'Uncertainty (±1σ)'] + in_labels_sorted
    
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

# def plot_global_sankey_interactive(df_flows, output_dir="output_files/plots"):
#     """
#     Genererer et interaktivt Sankey-diagram på HOVED-POOL-nivå (AT, EF, AG osv.)
#     begrenset til tidsperioden 1990-2023 med en slider for å bla gjennom årstall.
#     """
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Kloner og klargjør kilde/mål-kolonner
#     df = df_flows.copy()
    
#     # --- 1. BEGRENS TIL ÅRENE 1990 - 2023 ---
#     df = df[(df['year'] >= 1990) & (df['year'] <= 2023)]
    
#     if df.empty:
#         print("[WARN] Ingen data funnet for tidsperioden 1990-2023.")
#         return None
        
#     res = df['flow_name'].apply(extract_source_target)
    
#     # Trunkerer subpools til hoved-pools (f.eks. EF.TR -> EF)
#     df['source_pool'] = [r[0].split('.')[0] for r in res]
#     df['target_pool'] = [r[1].split('.')[0] for r in res]
    
#     # Filtrer bort ukjente eller interne feilstrømmer
#     df = df[(df['source_pool'] != "Unknown") & (df['target_pool'] != "Unknown")]
    
#     # Fjerner interne looper som oppstår ved sammenslåing (f.eks. EF -> EF)
#     df = df[df['source_pool'] != df['target_pool']]
    
#     if df.empty:
#         print("[WARN] Ingen gyldige strømmer funnet til å generere Sankey-diagram.")
#         return None

#     # Aggregerer verdiene på nytt etter sammenslåingen til hoved-pools
#     df = df.groupby(['year', 'source_pool', 'target_pool', 'flow_name'], as_index=False).agg({
#         'value': 'sum',
#         'uncertainty': lambda x: np.sqrt((x**2).sum())
#     })

#     # --- 2. OPPDATERT FARGE-MAPPING FOR NITROGENTYPER ---
#     def get_flow_color(flow_name):
#         fn = flow_name.upper()
#         if "N2O" in fn: 
#             return "rgba(156, 39, 176, 0.4)"       # Lilla
#         elif "N2" in fn and "NOX" not in fn: 
#             return "rgba(180, 180, 180, 0.4)"       # Grå
#         elif "NH3" in fn or "AMMONIA" in fn or "RDN" in fn: 
#             return "rgba(255, 152, 0, 0.4)"         # Oransje
#         elif "NOX" in fn or "OXN" in fn or "NITRITE" in fn or "NITRATE" in fn: 
#             return "rgba(244, 67, 54, 0.4)"         # Rød
#         elif "NMIX" in fn: 
#             return "rgba(76, 175, 80, 0.4)"          # Grønn
#         else: 
#             return "rgba(33, 150, 243, 0.4)"         # Blå (Fallback)

#     df['color'] = df['flow_name'].apply(get_flow_color)

#     # 3. Map unike hoved-nodes til statiske indekser
#     all_nodes = sorted(list(set(df['source_pool'].unique()) | set(df['target_pool'].unique())))
#     node_indices = {node: i for i, node in enumerate(all_nodes)}
    
#     # --- OPPDATERT: Unike farger for dine 9 spesifikke pools ---
#     node_color_map = {
#         "AT": "#1a365d",  # Deep Navy (Atmosfære)
#         "AG": "#2f855a",  # Skogsgrønn (Agriculture)
#         "EF": "#c53030",  # Mørkerød (Energy and Fuels)
#         "HY": "#2b6cb0",  # Klar blå (Hydrosfære)
#         "FS": "#2c7a7b",  # Sjøgrønn/Teal (Forestry / Skogbruk)
#         "HS": "#744210",  # Brun (Human Settlement / Avløp etc.)
#         "RW": "#4a5568",  # Skifergrå (Regulert vann/Reservoarer)
#         "PR": "#97266d",  # Vinrød/Plomme (Primary Processing / Industri)
#         "MP": "#d69e2e",  # Dempet gull/oransje (Manufacturing Products)
#     }
    
#     # Mapper fargene til rekkefølgen i all_nodes, med lys grå som sikkerhets-fallback
#     node_colors = [node_color_map.get(node, "#bdc3c7") for node in all_nodes]
    
#     # Statisk node-konfigurasjon med den nye fargelisten
#     static_node_config = dict(
#         pad=20, 
#         thickness=25, 
#         line=dict(color="black", width=0.5),
#         label=all_nodes, 
#         color=node_colors  
#     )
    
#     # 4. Klargjør tidsrammer (Frames)
#     all_years = sorted(list(df['year'].unique()))
#     frames = []
#     slider_steps = []

#     # Første tilgjengelige år i 1990-2023 serien som start-state
#     first_year = all_years[0]
#     df_first = df[df['year'] == first_year]
    
#     initial_sankey = go.Sankey(
#         node=static_node_config,
#         link=dict(
#             source=[node_indices[s] for s in df_first['source_pool']],
#             target=[node_indices[t] for t in df_first['target_pool']],
#             value=df_first['value'],
#             color=df_first['color'],
#             label=df_first['flow_name'],
#             line=dict(color="rgba(50, 50, 50, 0.3)", width=0.5)
#         )
#     )

#     # Bygg uavhengige frames for hvert år i perioden
#     for yr in all_years:
#         df_yr = df[df['year'] == yr]
        
#         frames.append(go.Frame(
#             data=[go.Sankey(
#                 node=static_node_config, 
#                 link=dict(
#                     source=[node_indices[s] for s in df_yr['source_pool']],
#                     target=[node_indices[t] for t in df_yr['target_pool']],
#                     value=df_yr['value'],
#                     color=df_yr['color'],
#                     label=df_yr['flow_name']
#                 )
#             )],
#             name=str(yr)
#         ))
        
#         slider_steps.append(dict(
#             method="animate",
#             args=[[str(yr)], dict(mode="immediate", frame=dict(duration=200, redraw=True), transition=dict(duration=0))],
#             label=str(yr)
#         ))

#     # 5. Sett sammen figuren og konfigurer layout
#     fig = go.Figure(data=[initial_sankey], frames=frames)

#     fig.update_layout(
#         title=dict(
#             text="Global Nitrogen Flow Evolution (1990-2023 - Main Pools)",
#             font=dict(size=18, family="Arial")
#         ),
#         height=750,
#         width=1100,
#         updatemenus=[dict(
#             type="buttons",
#             showactive=False,
#             x=0.05, y=-0.15, xanchor="right", yanchor="top",
#             buttons=[
#                 dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=400, redraw=True), fromcurrent=True)]),
#                 dict(label="⏸ Pause", method="animate", args=[[None], dict(mode="immediate", frame=dict(duration=0, redraw=True))])
#             ]
#         )],
#         sliders=[dict(
#             active=0,
#             steps=slider_steps,
#             x=0.08, y=-0.15,
#             currentvalue=dict(font=dict(size=14, color="navy"), prefix="Year: ", visible=True),
#             len=0.9
#         )]
#     )

#     filename = "global_nitrogen_sankey.html"
#     filepath = os.path.join(output_dir, filename)
#     fig.write_html(filepath, include_plotlyjs='cdn')
    
#     print(f"[SUCCESS] Interaktivt tidslinje-Sankey (1990-2023) generert -> {filepath}")
#     return filename



import os
import numpy as np
import plotly.graph_objects as go

def plot_global_sankey_interactive(df_flows, output_dir="output_files/plots"):
    """
    Genererer to interaktive Sankey-diagrammer på HOVED-POOL-nivå begrenset til 1990-2023:
    Låser den globale flytskalaen fullstendig ved bruk av en isolert skaleringsnode.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Kloner og klargjør kilde/mål-kolonner
    df_base = df_flows.copy()
    
    # --- 1. BEGRENS TIL ÅRENE 1990 - 2023 ---
    df_base = df_base[(df_base['year'] >= 1990) & (df_base['year'] <= 2023)]
    
    if df_base.empty:
        print("[WARN] Ingen data funnet for tidsperioden 1990-2023.")
        return None
        
    res = df_base['flow_name'].apply(extract_source_target)
    
    # Trunkerer subpools til hoved-pools (f.eks. EF.TR -> EF)
    df_base['source_pool'] = [r[0].split('.')[0] for r in res]
    df_base['target_pool'] = [r[1].split('.')[0] for r in res]
    
    # Filtrer bort ukjente eller interne feilstrømmer
    df_base = df_base[(df_base['source_pool'] != "Unknown") & (df_base['target_pool'] != "Unknown")]
    
    # Fjerner interne looper som oppstår ved sammenslåing (f.eks. EF -> EF)
    df_base = df_base[df_base['source_pool'] != df_base['target_pool']]
    
    if df_base.empty:
        print("[WARN] Ingen gyldige strømmer funnet til å generere Sankey-diagram.")
        return None

    # Aggregerer verdiene på nytt etter sammenslåingen til hoved-pools
    df_base = df_base.groupby(['year', 'source_pool', 'target_pool', 'flow_name'], as_index=False).agg({
        'value': 'sum',
        'uncertainty': lambda x: np.sqrt((x**2).sum())
    })

    # --- 2. FARGE-MAPPING FOR NITROGENTYPER ---
    def get_flow_color(flow_name):
        fn = flow_name.upper()
        if "N2O" in fn: 
            return "rgba(156, 39, 176, 0.4)"       # Lilla
        elif "N2" in fn and "NOX" not in fn: 
            return "rgba(180, 180, 180, 0.4)"       # Grå
        elif "NH3" in fn or "AMMONIA" in fn or "RDN" in fn: 
            return "rgba(255, 152, 0, 0.4)"         # Oransje
        elif "NOX" in fn or "OXN" in fn or "NITRITE" in fn or "NITRATE" in fn: 
            return "rgba(244, 67, 54, 0.4)"         # Rød
        elif "NMIX" in fn: 
            return "rgba(76, 175, 80, 0.4)"          # Grønn
        else: 
            return "rgba(33, 150, 243, 0.4)"         # Blå (Fallback)

    df_base['color'] = df_base['flow_name'].apply(get_flow_color)

    # 3. Map unike hoved-nodes + NYE USYNLIGE SKALERINGSNODER
    base_nodes = sorted(list(set(df_base['source_pool'].unique()) | set(df_base['target_pool'].unique())))
    
    # Vi legger til to kunstige noder dedikert KUN til å holde på skalaen
    all_nodes = base_nodes + ["SCALE_SRC", "SCALE_TRG"]
    node_indices = {node: i for i, node in enumerate(all_nodes)}
    
    # Fargemapping for reelle noder, de to skaleringsnodene gjøres 100% gjennomsiktige
    node_color_map = {
        "AT": "rgba(26, 54, 93, 0.4)",
        "HY": "rgba(43, 108, 176, 0.4)",
        "RW": "rgba(74, 85, 104, 0.4)",
        "AG": "#2f855a", "EF": "#c53030", "FS": "#2c7a7b", "HS": "#744210", "PR": "#97266d", "MP": "#d69e2e",
        "SCALE_SRC": "rgba(0,0,0,0)", # Usynlig
        "SCALE_TRG": "rgba(0,0,0,0)"  # Usynlig
    }
    node_colors = [node_color_map.get(node, "#bdc3c7") for node in all_nodes]
    
    # Plassering av noder (X-koordinater). Skaleringsnodene gjemmes helt øverst i venstre/høyre hjørne
    node_x_map = {
        "AT": 0.02, "AG": 0.40, "FS": 0.40, "EF": 0.65, "PR": 0.65, "MP": 0.65, "HS": 0.65, "HY": 0.98, "RW": 0.98,
        "SCALE_SRC": 0.01,
        "SCALE_TRG": 0.99
    }
    node_x = [node_x_map.get(node, 0.5) for node in all_nodes]
    
    # For å hindre at de usynlige nodene dytter ned de ekte nodene, tvinger vi dem til y=0 (helt øverst)
    node_y_map = {
        "SCALE_SRC": 0.001,
        "SCALE_TRG": 0.001
    }
    node_y = [node_y_map.get(node, None) for node in all_nodes] # None lar Plotly bestemme resten dynamisk

    static_node_config = dict(
        pad=20, 
        thickness=25, 
        line=dict(color="black", width=0.5),
        label=[n if "SCALE" not in n else "" for n in all_nodes], # Skjul merkelappen på skaleringsnodene
        color=node_colors,
        x=node_x,
        y=node_y
    )
    
    # Definer strømmene som skal skjules i versjon nr. 2
    hidden_keywords = ["AMMONIA IMPORT", "AMMONIA EXPORT", "AMMONIA SYNTHESIS", "FERTILIZER EXPORT"]
    filter_regex = "|".join(hidden_keywords)
    df_filtered = df_base[~df_base['flow_name'].str.upper().str.contains(filter_regex, na=False)].copy()

    # --- MAKSIMAL SYSTEMKAPASITET FOR STATISK SKALERING ---
    max_total_base = df_base.groupby('year')['value'].sum().max() * 1.05 # 5% ekstra margin
    max_total_filtered = df_filtered.groupby('year')['value'].sum().max() * 1.05

    # --- 4. INDRE FUNKSJON FOR Å BYGGE EN ENCELT HTML-FIGUR ---
    def build_sankey_figure(df_data, title_suffix, max_scale_value):
        all_years = sorted(list(df_data['year'].unique()))
        frames = []
        slider_steps = []

        def get_sankey_components(df_year_source, total_max):
            df_yr = df_year_source.copy()
            current_total = df_yr['value'].sum()
            remaining_buffer = total_max - current_total
            
            # Konverter reelle data til lister
            sources = [node_indices[s] for s in df_yr['source_pool']]
            targets = [node_indices[t] for t in df_yr['target_pool']]
            values = df_yr['value'].tolist()
            colors = df_yr['color'].tolist()
            labels = df_yr['flow_name'].tolist()
            
            # Kantlinje-konfigurasjon for de ekte strømmene
            line_colors = ["rgba(50, 50, 50, 0.3)"] * len(values)
            line_widths = [0.5] * len(values)
            
            # Hvis vi trenger å fylle opp skalaen, bruker vi de dedikerte usynlige nodene
            if remaining_buffer > 0:
                sources.append(node_indices["SCALE_SRC"])
                targets.append(node_indices["SCALE_TRG"])
                values.append(remaining_buffer)
                colors.append("rgba(0,0,0,0)") # 100% gjennomsiktig flyt
                labels.append("")               # Ingen tekst ved hover
                line_colors.append("rgba(0,0,0,0)") # Ingen kantlinjefarge
                line_widths.append(0.0)             # Ingen kantlinjebredde
                
            return dict(
                source=sources, target=targets, value=values, color=colors, label=labels,
                line=dict(color=line_colors, width=line_widths)
            )

        first_year = all_years[0]
        link_config_first = get_sankey_components(df_data[df_data['year'] == first_year], max_scale_value)
        
        initial_sankey = go.Sankey(
            node=static_node_config,
            link=link_config_first
        )

        for yr in all_years:
            link_config_yr = get_sankey_components(df_data[df_data['year'] == yr], max_scale_value)
            
            frames.append(go.Frame(
                data=[go.Sankey(
                    node=static_node_config, 
                    link=link_config_yr
                )],
                name=str(yr)
            ))
            
            slider_steps.append(dict(
                method="animate",
                args=[[str(yr)], dict(mode="immediate", frame=dict(duration=200, redraw=True), transition=dict(duration=0))],
                label=str(yr)
            ))

        fig = go.Figure(data=[initial_sankey], frames=frames)
        fig.update_layout(
            title=dict(
                text=f"Global Nitrogen Flow Evolution (1990-2023) - {title_suffix}",
                font=dict(size=18, family="Arial")
            ),
            height=750,
            margin=dict(l=20, r=20, t=60, b=20),
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                x=0.05, y=-0.15, xanchor="right", yanchor="top",
                buttons=[
                    dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=400, redraw=True), fromcurrent=True)]),
                    dict(label="⏸ Pause", method="animate", args=[[None], dict(mode="immediate", frame=dict(duration=0, redraw=True))])
                ]
            )],
            sliders=[dict(
                active=0,
                steps=slider_steps,
                x=0.08, y=-0.15,
                currentvalue=dict(font=dict(size=14, color="navy"), prefix="Year: ", visible=True),
                len=0.9
            )]
        )
        return fig

    # --- 5. GENERER OG LAGRE BEGGE FILENE ---
    fig_all = build_sankey_figure(df_base, "All Flows", max_total_base)
    filename_all = "global_nitrogen_sankey.html"
    filepath_all = os.path.join(output_dir, filename_all)
    fig_all.write_html(filepath_all, include_plotlyjs='cdn', default_width='100%')
    print(f"[SUCCESS] Komplett Sankey med låst global skalering generert -> {filepath_all}")
    
    fig_filtered = build_sankey_figure(df_filtered, "Fertilizer Trade Hidden", max_total_filtered)
    filename_filtered = "global_nitrogen_sankey_no_fertilizer.html"
    filepath_filtered = os.path.join(output_dir, filename_filtered)
    fig_filtered.write_html(filepath_filtered, include_plotlyjs='cdn', default_width='100%')
    print(f"[SUCCESS] Filtrert Sankey med låst global skalering generert -> {filepath_filtered}")
    
    return filename_all


def extract_source_target(flow_name):
        """
        Altetende splitter som garanterer at kilde og mottaker blir funnet,
        uansett om det brukes bindestrek, understrek eller punktum.
        """
        fn = flow_name.upper().strip()
        
        # Standard: Hvis den bruker bindestrek (f.eks. AG.MM-AT.AT-Emissions)
        if '-' in fn:
            parts = fn.split('-')
            return parts[0].strip(), parts[1].strip()
        
        # Hvis den bruker understrek (f.eks. AG_MM_AT_AT_EMISSIONS eller AG_SM_LEACHING)
        if '_' in fn:
            parts = fn.split('_')
            
            # Tilfelle A: AG_MM_AT_AT_... (Lengre strenger)
            if len(parts) >= 4 and parts[0] == "AG" and parts[2] in ["AT", "RW", "HY", "MP", "FS", "PR"]:
                src = f"{parts[0]}.{parts[1]}"  # AG.MM
                tgt = f"{parts[2]}.{parts[3]}"  # AT.AT
                return src, tgt
                
            # Tilfelle B: Intern strøm AG_MM_AG_SM_...
            if len(parts) >= 4 and parts[0] == "AG" and parts[2] == "AG":
                src = f"{parts[0]}.{parts[1]}"  # AG.MM
                tgt = f"{parts[2]}.{parts[3]}"  # AG.SM
                return src, tgt

            # Tilfelle C: Enklere format som f.eks. AG_MM_LEACHING (hvor mottaker må gjettes ut fra kontekst)
            if parts[0] == "AG" and parts[1] in ["MM", "SM"]:
                src = f"AG.{parts[1]}"
                # Gjetter mål basert på unike nøkkelord hvis full kode mangler i navnet
                if "LEACHING" in parts or "HY" in parts: tgt = "HY.SW"
                elif "EMISSIONS" in parts or "AT" in parts: tgt = "AT.AT"
                elif "PRODUCT" in parts or "MP" in parts: tgt = "MP.FP"
                elif "EXPORT" in parts or "RW" in parts: tgt = "RW.RW"
                elif "APPLICATION" in parts: tgt = "AG.SM"
                elif "FODDER" in parts: tgt = "AG.MM"
                else: tgt = "Unknown"
                return src, tgt

        # Nød-fallback: Hvis den starter med AG.MM eller AG.SM direkte (f.eks. som ren tekst)
        if fn.startswith("AG.MM"): return "AG.MM", "Unknown"
        if fn.startswith("AG.SM"): return "AG.SM", "Unknown"
        
        return "Unknown", "Unknown"
    
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
        
        yearly_sums = df_flow.groupby('year')['value'].sum()
        years_with_data = df_flow[df_flow['value'].notna()]['year'].unique().tolist()
        
        if not years_with_data:
            print(f"  [INFO] Flow '{flow}' has no data in the entire period. Skipping.")
            continue
            
        start_year = min(years_with_data)
        end_year = max(years_with_data)
        
        expected_years = set(range(start_year, end_year + 1))
        missing_years = expected_years - set(years_with_data)
        
        if missing_years:
            print(f"  [ALARM / ERROR] Flow '{flow}' has missing data gaps in years: {sorted(list(missing_years))}")
        
        df_trimmed = df_flow[(df_flow['year'] >= start_year) & (df_flow['year'] <= end_year)].copy()
        # df_trimmed['value'] = df_trimmed['value'].fillna(0.0)
        
        trimmed_chunks.append(df_trimmed)

    if not trimmed_chunks:
        print("[ABORTED] No flows contained valid data after trimming intervals.")
        return
        
    df_all_trimmed = pd.concat(trimmed_chunks, ignore_index=True)

    # 2. Calculate statistics across all sim_ids
    print("[STATISTICS] Calculating medians and 95% confidence intervals...")
    summary_df = df_all_trimmed.groupby(['flow_name', 'year'])['value'].agg(
        median=np.median,
        mean=np.mean,
        p2_5=lambda x: np.percentile(x, 2.5),
        p97_5=lambda x: np.percentile(x, 97.5),
        std=np.std
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

    # 4. Export to Excel
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, 'MC_Reporting_Statistics.xlsx')
    
    summary_df_rounded = summary_df.round({
        'median': 4, 'mean': 4, 'p2_5': 4, 'p97_5': 4, 'std': 4,
        'unc_down_percent': 2, 'unc_up_percent': 2, 'cv_percent': 2
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

    # ========================================================
    # INTEGRASJON: GENERERING AV BALANSEPLOTT FOR POOLER
    # ========================================================
    print("\n[PLOTTING] Preparing mass balance datasets for pools and subpools...")
    
    df_balance_input = summary_df.copy()
    
    # def extract_source_target(flow_name):
    #     """
    #     Altetende splitter som garanterer at kilde og mottaker blir funnet.
    #     """
    #     fn = flow_name.upper().strip()
        
    #     if '-' in fn:
    #         parts = fn.split('-')
    #         return parts[0].strip(), parts[1].strip()
        
    #     if '_' in fn:
    #         parts = fn.split('_')
    #         if len(parts) >= 4 and parts[0] == "AG" and parts[2] in ["AT", "RW", "HY", "MP", "FS", "PR"]:
    #             return f"{parts[0]}.{parts[1]}", f"{parts[2]}.{parts[3]}"
    #         if len(parts) >= 4 and parts[0] == "AG" and parts[2] == "AG":
    #             return f"{parts[0]}.{parts[1]}", f"{parts[2]}.{parts[3]}"
    #         if parts[0] == "AG" and parts[1] in ["MM", "SM"]:
    #             src = f"AG.{parts[1]}"
    #             if "LEACHING" in parts or "HY" in parts: tgt = "HY.SW"
    #             elif "EMISSIONS" in parts or "AT" in parts: tgt = "AT.AT"
    #             elif "PRODUCT" in parts or "MP" in parts: tgt = "MP.FP"
    #             elif "EXPORT" in parts or "RW" in parts: tgt = "RW.RW"
    #             elif "APPLICATION" in parts: tgt = "AG.SM"
    #             elif "FODDER" in parts: tgt = "AG.MM"
    #             else: tgt = "Unknown"
    #             return src, tgt
        
    #     if fn.startswith("AG.MM"): return "AG.MM", "Unknown"
    #     if fn.startswith("AG.SM"): return "AG.SM", "Unknown"
    #     return "Unknown", "Unknown"

    # 1. Bruk splittefunksjonen til å tildele kilde (source), mottaker (target) og verdi/usikkerhet
    res = df_balance_input['flow_name'].apply(extract_source_target)
    df_balance_input['source'] = [r[0] for r in res]
    df_balance_input['target'] = [r[1] for r in res]
    
    # plot_pool_balance forventer kolonnene 'value' og 'uncertainty'
    df_balance_input['value'] = df_balance_input['median']
    df_balance_input['uncertainty'] = df_balance_input['std']  # Bruker standardavviket som 1σ usikkerhet
    
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
            
        plot_pool_balance(df_temppool, pool, output_dir=plot_dir)
        plot_pool_balance_interactive(df_temppool, pool, output_dir=plot_dir)
        
    print("\n" + "="*60)
    print("[SUCCESS] All MC iterations processed, statistics saved, and plots generated successfully.")
    
    print("\n[PLOTTING] Generating global interactive Sankey diagram across all years...")
    plot_global_sankey_interactive(df_balance_input, output_dir=plot_dir)
        
    print("\n" + "="*60)
    print("[SUCCESS] All MC iterations processed, statistics saved, and plots generated successfully.")
    
