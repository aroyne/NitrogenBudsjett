import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime  # <-- NYTT: For tidsstempling

# Angi standard figurstørrelse globalt for å unngå .figure()
plt.rcParams['figure.figsize'] = (10, 6)

def process_and_export_mc_results(all_records):
    """
    Tar imot en liste med ordbøker fra ALLE MC-iterasjoner.
    Beregner statistikk, lagrer til Excel og plotter med:
      - Fast x-akse (1984-2025)
      - Y-akse som starter på 0
      - Tydelig usikkerhetsintervall
      - Tidsstempel for debugging nederst i høyre hjørne
    """
    if not all_records:
        print("[ADVARSEL] Ingen resultater å behandle.")
        return

    # Generer et tidsstempel for akkurat denne kjøringen
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "="*60)
    print("[STATISTIKK] Starter statistisk analyse av MC-resultater...")
    print(f"[DEBUG] Kjøringen prosesseres nå: {current_time_str}")
    
    # 1. Konverter til en stor DataFrame og vask datatyper
    df_all = pd.DataFrame(all_records)
    df_all['value'] = pd.to_numeric(df_all['value'], errors='coerce')
    
    total_simulations = df_all['sim_id'].nunique()
    print(f"[STATISTIKK] Detekterte {total_simulations} unike Monte Carlo-iterasjoner.")
    
    # Lag en liste for å samle opp ferdig trimmede data per strøm
    trimmed_chunks = []
    unique_flows = df_all['flow_name'].unique()
    
    print("[STATISTIKK] Analyserer og trimmer tidsintervaller per strøm...")
    
    for flow in unique_flows:
        df_flow = df_all[df_all['flow_name'] == flow]
        
        # Finn ut hvilke år som har faktiske data (verdi over 0) på tvers av simuleringer
        yearly_sums = df_flow.groupby('year')['value'].sum()
        years_with_data = yearly_sums[yearly_sums != 0].index.tolist()
        
        if not years_with_data:
            print(f"  [INFO] Strøm '{flow}' har ingen data i hele perioden. Hopper over.")
            continue
            
        start_year = min(years_with_data)
        end_year = max(years_with_data)
        
        # SJEKK FOR INNEKLEMTE ÅR UTEN DATA
        expected_years = set(range(start_year, end_year + 1))
        missing_years = expected_years - set(years_with_data)
        
        if missing_years:
            print(f"  [ALARM / FEIL] Strøm '{flow}' har inneklemte år uten data: {sorted(list(missing_years))}")
        
        # Trim datasettet for denne strømmen til kun å gjelde det aktive intervallet
        df_trimmed = df_flow[(df_flow['year'] >= start_year) & (df_flow['year'] <= end_year)].copy()
        df_trimmed['value'] = df_trimmed['value'].fillna(0.0)
        
        trimmed_chunks.append(df_trimmed)

    if not trimmed_chunks:
        print("[AVBRUTT] Ingen strømmer hadde gyldige data etter trimming.")
        return
        
    # Sett sammen igjen alle de trimmede bitene til én stor DataFrame
    df_all_trimmed = pd.concat(trimmed_chunks, ignore_index=True)

    # 2. Beregn statistikk per strøm per år på tvers av alle sim_id
    print("[STATISTIKK] Beregner median og 95% konfidensintervaller...")
    summary_df = df_all_trimmed.groupby(['flow_name', 'year'])['value'].agg(
        median=np.median,
        mean=np.mean,
        p2_5=lambda x: np.percentile(x, 2.5),
        p97_5=lambda x: np.percentile(x, 97.5),
        std=np.std
    ).reset_index()

    # 3. Beregn usikkerhetsparametere (asymmetrisk % og symmetrisk CV%)
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

    # 4. EKSPORT TIL EXCEL
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, 'MC_Rapportering_Statistikk.xlsx')
    
    summary_df_rounded = summary_df.round({
        'median': 4, 'mean': 4, 'p2_5': 4, 'p97_5': 4, 'std': 4,
        'unc_down_percent': 2, 'unc_up_percent': 2, 'cv_percent': 2
    })
    summary_df_rounded.to_excel(excel_path, index=False)
    print(f"[SUKSESS] Internasjonal rapport lagret til: {excel_path}")

    # 5. GENERER TIDSPLOTT
    print("[PLOTTING] Genererer tidsplott for hver nitrogenstrøm...")
    plot_dir = os.path.join(output_dir, 'plots')
    os.makedirs(plot_dir, exist_ok=True)

    for flow in summary_df['flow_name'].unique():
        df_flow = summary_df[summary_df['flow_name'] == flow].sort_values('year')
        
        plt.clf()
        
        # Tegn konfidensintervall (skygge + stiplede linjer)
        plt.fill_between(
            df_flow['year'], 
            df_flow['p2_5'], 
            df_flow['p97_5'], 
            color='skyblue', 
            alpha=0.4, 
            label='95% Konfidensintervall (MC)'
        )
        plt.plot(df_flow['year'], df_flow['p2_5'], color='steelblue', linestyle=':', linewidth=1, alpha=0.7)
        plt.plot(df_flow['year'], df_flow['p97_5'], color='steelblue', linestyle=':', linewidth=1, alpha=0.7)
        
        # Plott medianen
        plt.plot(
            df_flow['year'], 
            df_flow['median'], 
            color='navy', 
            linewidth=2.5, 
            label='Median (50-persentil)'
        )
        
        flow_start = df_flow['year'].min()
        flow_end = df_flow['year'].max()
        
        # Tittel og akse-innstillinger
        short_name = flow.split('-')[-2] if '-' in flow else flow
        component = flow.split('-')[-1] if '-' in flow else ''
        plt.title(f"Tidsutvikling med MC-usikkerhet:\n{short_name} ({component})", fontsize=12, fontweight='bold')
        
        plt.xlim(1984, 2025)
        plt.xticks(np.arange(1984, 2026, 5))
        
        plt.ylim(bottom=0)
        current_ymax = plt.ylim()[1]
        plt.ylim(top=current_ymax * 1.15 if current_ymax > 0 else 10)
        
        # Merknad om reelt datagrunnlag (nederst til venstre)
        plt.text(1985, plt.ylim()[1] * 0.05, 
                 f"Datagrunnlag: {flow_start}-{flow_end}", 
                 fontsize=9, style='italic', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        # --- NYTT: DISKRET TIDSSTEMPEL FOR SJEKK AV SIST OPPDATERT (nederst til høyre) ---
        plt.text(2024.5, plt.ylim()[1] * 0.05, 
                 f"Oppdatert: {current_time_str}", 
                 fontsize=8, color='gray', ha='right', style='italic')
        
        plt.xlabel("År", fontsize=10)
        plt.ylabel("Nitrogenmengde (kt N / år)", fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.legend(loc='upper left')
        
        # Lagre plottet som PNG
        safe_filename = flow.replace('.', '_').replace('-', '_').replace(' ', '_') + '.png'        
        plt.savefig(os.path.join(plot_dir, safe_filename), dpi=150, bbox_inches='tight')        

    print(f"[SUKSESS] Plott lagret og tidsstemplet [{current_time_str}] i: {plot_dir}")
    print("="*60 + "\n")