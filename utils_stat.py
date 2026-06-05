import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def process_and_export_mc_results(all_records):
    """
    Receives a list of dictionaries from ALL MC iterations.
    Calculates statistics, exports a raw debug Excel sheet, generates plots,
    and returns the summarized DataFrame containing medians, CV%, comments, 
    and data sources for final reporting.
    """
    if not all_records:
        print("[WARNING] No records available to process.")
        return None

    # Generer et tidsstempel for denne simuleringskjøringen
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "="*60)
    print("[STATISTICS] Starting statistical analysis of MC results...")
    
    # 1. Konverter til DataFrame og rens datatyper
    df_all = pd.DataFrame(all_records)
    df_all['value'] = pd.to_numeric(df_all['value'], errors='coerce')
    
    total_simulations = df_all['sim_id'].nunique()
    print(f"[STATISTICS] Detected {total_simulations} unique Monte Carlo iterations.")
    
    trimmed_chunks = []
    unique_flows = df_all['flow_name'].unique()
    
    print("[STATISTICS] Analyzing and trimming time intervals per flow...")
    
    for flow in unique_flows:
        df_flow = df_all[df_all['flow_name'] == flow]
        
        # Identifiser aktive år med data på tvers av simuleringskjøringer
        yearly_sums = df_flow.groupby('year')['value'].sum()
        years_with_data = yearly_sums[yearly_sums != 0].index.tolist()
        
        if not years_with_data:
            print(f"  [INFO] Flow '{flow}' has no data in the entire period. Skipping.")
            continue
            
        start_year = min(years_with_data)
        end_year = max(years_with_data)
        
        # Sjekk om det er uventede hull i datarekken
        expected_years = set(range(start_year, end_year + 1))
        missing_years = expected_years - set(years_with_data)
        if missing_years:
            print(f"  [ALARM / ERROR] Flow '{flow}' has missing data gaps in years: {sorted(list(missing_years))}")
        
        df_trimmed = df_flow[(df_flow['year'] >= start_year) & (df_flow['year'] <= end_year)].copy()
        df_trimmed['value'] = df_trimmed['value'].fillna(0.0)
        
        trimmed_chunks.append(df_trimmed)

    if not trimmed_chunks:
        print("[ABORTED] No flows contained valid data after trimming intervals.")
        return None
        
    df_all_trimmed = pd.concat(trimmed_chunks, ignore_index=True)

    # 2. Beregn statistikk på tvers av sim_ids og hold på tekstfelter
    print("[STATISTICS] Calculating medians, CV% and aggregating text fields...")
    
    # Her bruker vi en ordbok i .agg() for å gjøre spesifikke operasjoner per kolonne.
    # Siden tekstene er like på tvers av sim_ids, henter vi bare den første ('first').
    summary_df = df_all_trimmed.groupby(['flow_name', 'year']).agg(
        median=('value', np.median),
        mean=('value', np.mean),
        std=('value', np.std),
        p2_5=('value', lambda x: np.percentile(x, 2.5)),
        p97_5=('value', lambda x: np.percentile(x, 97.5)),
        data_sources=('data_sources', 'first'),
        comment=('comment', 'first')
    ).reset_index()

    # 3. Beregn usikkerhetsmetrikker (Inkludert symmetrisk cv_percent)
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

    # 4. Eksporter en rå teknisk kopi til Excel (for feilsøking/historikk)
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, 'MC_Reporting_Statistics.xlsx')
    
    summary_df_rounded = summary_df.round({
        'median': 4, 'mean': 4, 'p2_5': 4, 'p97_5': 4, 'std': 4,
        'unc_down_percent': 2, 'unc_up_percent': 2, 'cv_percent': 2
    })
    summary_df_rounded.to_excel(excel_path, index=False)
    print(f"[SUCCESS] Technical statistical report saved to: {excel_path}")

    # 5. GENERER GRAFER
    plot_dir = os.path.join(output_dir, 'plots')
    if os.path.exists(plot_dir):
        shutil.rmtree(plot_dir)
    os.makedirs(plot_dir, exist_ok=True)

    print("[PLOTTING] Generating fresh time-series plots...")

    for flow in summary_df['flow_name'].unique():
        df_flow = summary_df[summary_df['flow_name'] == flow].sort_values('year')
        
        plt.figure(figsize=(10, 3.6))
        
        # Skyggelegg 95% konfidensintervall
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
        
        # Tegn medianen
        plt.plot(
            df_flow['year'], 
            df_flow['median'], 
            color='navy', 
            linewidth=2.5, 
            label='Median (50th percentile)'
        )
        
        flow_start = df_flow['year'].min()
        flow_end = df_flow['year'].max()
        
        short_name = flow.split('-')[-2] if '-' in flow else flow
        component = flow.split('-')[-1] if '-' in flow else ''
        
        plt.title(f"MC Uncertainty Trends: {short_name} ({component})", fontsize=11, fontweight='bold', loc='left')
        
        plt.xlim(1984, 2025)
        plt.xticks(np.arange(1984, 2026, 5))
        plt.ylim(bottom=0)
        current_ymax = plt.ylim()[1]
        plt.ylim(top=current_ymax * 1.15 if current_ymax > 0 else 10)
        
        plt.text(1985, plt.ylim()[1] * 0.05, f"Data Range: {flow_start}-{flow_end}", 
                 fontsize=9, style='italic', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        plt.text(2024.5, plt.ylim()[1] * 0.05, f"Updated: {current_time_str}", 
                 fontsize=8, color='gray', ha='right', style='italic')
        
        plt.xlabel("Year", fontsize=10)
        plt.ylabel("Nitrogen Flow (kt N / year)", fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.legend(loc='upper left')
        
        safe_filename = flow.replace('.', '_').replace('-', '_').replace(' ', '_') + '.png'        
        plt.savefig(os.path.join(plot_dir, safe_filename), dpi=150, bbox_inches='tight')        
        plt.close()

    print(f"[SUCCESS] All fresh plots saved in: {plot_dir}")
    print("="*60 + "\n")
    
    # VIKTIG: Returnerer tabellen slik at main_mc.py kan sende den til rapporteringen din!
    return summary_df