import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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
    
    def extract_source_target(flow_name):
        """
        Altetende splitter som garanterer at kilde og mottaker blir funnet.
        """
        fn = flow_name.upper().strip()
        
        if '-' in fn:
            parts = fn.split('-')
            return parts[0].strip(), parts[1].strip()
        
        if '_' in fn:
            parts = fn.split('_')
            if len(parts) >= 4 and parts[0] == "AG" and parts[2] in ["AT", "RW", "HY", "MP", "FS", "PR"]:
                return f"{parts[0]}.{parts[1]}", f"{parts[2]}.{parts[3]}"
            if len(parts) >= 4 and parts[0] == "AG" and parts[2] == "AG":
                return f"{parts[0]}.{parts[1]}", f"{parts[2]}.{parts[3]}"
            if parts[0] == "AG" and parts[1] in ["MM", "SM"]:
                src = f"AG.{parts[1]}"
                if "LEACHING" in parts or "HY" in parts: tgt = "HY.SW"
                elif "EMISSIONS" in parts or "AT" in parts: tgt = "AT.AT"
                elif "PRODUCT" in parts or "MP" in parts: tgt = "MP.FP"
                elif "EXPORT" in parts or "RW" in parts: tgt = "RW.RW"
                elif "APPLICATION" in parts: tgt = "AG.SM"
                elif "FODDER" in parts: tgt = "AG.MM"
                else: tgt = "Unknown"
                return src, tgt
        
        if fn.startswith("AG.MM"): return "AG.MM", "Unknown"
        if fn.startswith("AG.SM"): return "AG.SM", "Unknown"
        return "Unknown", "Unknown"

    # --- HER ER KODEN SOM MANGLER FOR Å UTVIKLE OG GENERERE PLOTTENE ---
    
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
        
    print("\n" + "="*60)
    print("[SUCCESS] All MC iterations processed, statistics saved, and plots generated successfully.")
    
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