#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from calculations.utils import read_trade_data

def load_all_data(selected_pools):
    """Sentral datalaster som sørger for at tunge I/O-operasjoner kun skjer ÉN gang."""
    preloaded = {}
    
    # 1. ATMOSFÆRE-DATA
    SR_needing_pools = {'at', 'rw'}
    if not SR_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader data for Atmosfære (atm_in_out.xlsx)...")
        try:
            df_atm_raw = pd.read_excel('data_files/atm_in_out.xlsx', sheet_name='Ark1', header=None)
            preloaded['atm_in_out'] = df_atm_raw
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade atm_in_out.xlsx: {e}")
            
    trade_needing_pools = {'at', 'rw', 'mp', 'pr', 'ef'}
    if not trade_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader komplett varehandelsstatistikk koblet mot alle kategorier...")
        try:
            # Last inn hele rådatafilen (6 mill rader) via din vaskefunksjon
            df_trade_raw = read_trade_data('data_files/Tab_08801_1988_2024.csv')
            
            # Hent ut hele mappingen fra NParameters
            from calculations.n_params import NParameters
            params_excel = NParameters("data_files/N_parameters.xlsx")
            df_mapping = params_excel.get_trade_mapping()
            
            # Sikre at mappingen har kolonnene flate
            if 'konv' not in df_mapping.columns:
                df_mapping = df_mapping.reset_index()
                
            # Sørg for tekst-matching på varenummer på tvers av hele settet
            df_trade_raw['HS_code_str'] = df_trade_raw['HS_code'].astype(str).str.strip()
            v_col = 'Varenr' if 'Varenr' in df_mapping.columns else 'varenr'
            df_mapping['varenr_str'] = df_mapping[v_col].astype(str).str.strip()
            
            # Gjør den tunge basemergen for ALLE varenumre én gang for alle
            df_prepared_all = df_trade_raw.merge(
                df_mapping[[v_col, 'konv', 'type', 'varenr_str']],
                left_on='HS_code_str',
                right_on='varenr_str',
                how='inner'
            )
            
            # --- ULTRA-OPTIMALISERING: Pre-aggreger tonnasje per år, import/eksport, type OG konv-type ---
            print("[INFO] Komprimerer 6 mill rader handelsdata til en kjapp volum-matrise...")
            
            # ENDRING: Legg til 'type' i listen inni .groupby([...])
            df_volum_aggregated = df_prepared_all.groupby(['year', 'impeks', 'type', 'konv'])['amount'].sum().reset_index()
            
            # Lagre denne superlette matrisen
            preloaded['compressed_trade_volume'] = df_volum_aggregated
            
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade den generelle handelsdataen: {e}")
            
    # 3. FAOSTAT GJØDSELDATA
    if 'at' in selected_pools:
        print("[I/O] Pre-loader FAOSTAT gjødseldata (FAOSTAT_data_en_11-25-2025.csv)...")
        try:
            df_faostat = pd.read_csv('data_files/FAOSTAT_data_en_11-25-2025.csv')
            preloaded['faostat_fertilizer'] = df_faostat[['Year', 'Value']].copy()
        except Exception as e:
            print(f"[ADVARSEL] Kunne ikke pre-loade FAOSTAT-data: {e}")
            
    # 4. DEPONERINGSDATA
    if 'at' in selected_pools:
        print("[I/O] Pre-loader NILU deponeringsdata (N_per_class_period_distributed_unallocated_long.csv)...")
        try:
            preloaded['deposition_data'] = pd.read_csv('data_files/N_per_class_period_distributed_unallocated_long.csv')
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade deponeringsdata: {e}")
            
    # 5. IMPORT AV DYREFÔR
    if 'rw' in selected_pools:
        print("[I/O] Pre-loader Landbruksdirektoratets kraftfôrstatistikk (Årlig råvareforbruk.xlsx)...")
        # 1. Hent data fra Landbruksdirektoratets kraftfôrstatistikk
        # Forventer år i kolonne 1 (A), karbohydrat i kolonne 3 (C), protein i kolonne 9 (I)
        df_raavarer = pd.read_excel('data_files/Årlig råvareforbruk.xlsx', sheet_name='Varegrupper')
        # Klipp ut de eksakte radene (rader 5 til 30 i Excel tilsvarer vanligvis index 3 til 28 i Pandas, avhengig av header)
        # Det tryggeste er å gi kolonnene navn, men her bruker vi iloc for å speile din originale kode:
        df_raavarer_clean = pd.DataFrame({
            'year': df_raavarer.iloc[3:28, 0].astype(int),
            'value_carb': df_raavarer.iloc[3:28, 2].astype(float),
            'value_prot': df_raavarer.iloc[3:28, 8].astype(float)
        }).reset_index(drop=True)
    if 'rw' in selected_pools:
        print("[I/O] Pre-loader NIBIO Totalkalkylen innkjøpt kraftfôr (NibioStatistics-4.xlsx)...")    
        # 2. Hent data fra NIBIO Totalkalkylen
        # Forventer år i kolonne 1 (A), tonn i kolonne 2 (B), dom_frac i kolonne 5 (E)
        df_totalkalkyle = pd.read_excel('data_files/NibioStatistics-4.xlsx', sheet_name='Sum innkjøpt kraftfôr ukorr.')
        df_totalkalkyle_clean = pd.DataFrame({
            'year': df_totalkalkyle.iloc[26:41, 0].astype(int), # Tilsvarende rad 28 til 43 i Excel
            'value': df_totalkalkyle.iloc[26:41, 1].astype(float),
            'dom_frac': df_totalkalkyle.iloc[26:41, 4].astype(float)
        }).reset_index(drop=True)
    
    # Legg dem inn i preloaded_data-ordboken:
    preloaded['feed_raavarer'] = df_raavarer_clean
    preloaded['feed_totalkalkyle'] = df_totalkalkyle_clean
    
    
    aq_needing_pools = {'hy', 'rw'}
    if not aq_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader data for akvakultur(A.06.002_20251111-140559.xlsx,akvakultur_1984_1994.xlsx)  ...")    
        # ==========================================
        # DATAINNLESING FOR AKVAKULTUR (MC-KLAR)
        # ==========================================
        
        # 1. LES INN MODERNE DATA (Fra 1994 og utover)
        # Siden årstallene ligger i rad 3, og dataene i rad 5-44, leser vi inn uten header først
        df_aqua_modern_raw = pd.read_excel(
            'data_files/A.06.002_20251111-140559.xlsx', 
            sheet_name='A.06.002', 
            header=None
        )
        
        # Rad 3 i Excel er index 2 i Pandas. Kolonne 3 (C) og utover er index 2 og utover.
        years_modern = df_aqua_modern_raw.iloc[2, 2:].astype(int).tolist()
        
        # Klipp ut rad 5 til 44 (index 4 til 43 i Pandas) for kolonnene fra C og utover
        # Erstatter '-' med 0 med en gang, slik at tabellen blir numerisk og rask å summere
        df_modern_data_cells = df_aqua_modern_raw.iloc[4:43, 2:].replace('-', 0).astype(float)
        
        # Gi kolonnene navn etter årstallene, slik at find_aquaculture_production enkelt kan løpe gjennom dem
        df_modern_data_cells.columns = years_modern
        preloaded['aqua_modern'] = df_modern_data_cells
        
        
        # 2. LES INN GAMLE DATA (Før 1994)
        # Rad 2 til 12 i Excel blir index 1 til 11 i Pandas (hvis vi leser uten header)
        df_aqua_old_raw = pd.read_excel(
            'data_files/akvakultur_1984_1994.xlsx', 
            sheet_name='Ark1', 
            header=None
        )
        
        # Hent ut år (kolonne A/index 0) og verdi (kolonne B/index 1) for radene 2 til 12
        df_old_clean = pd.DataFrame({
            'year': df_aqua_old_raw.iloc[1:11, 0].astype(int),
            'value': df_aqua_old_raw.iloc[1:11, 1].astype(float)
        }).reset_index(drop=True)
        
        preloaded['aqua_old'] = df_old_clean
        
    if 'rw' in selected_pools:
        print("[I/O] Pre-loader FAOSTAT data for levende dyr (FAOSTAT_data_en_11-12-2025)...")    
        
        # ==========================================
        # DATAINNLESING FOR LEVENDE DYR (MC-KLAR)
        # ==========================================
        
        # 1. Les inn og grovfiltrer FAOSTAT-dataen med en gang for å spare minne
        df_fao_raw = pd.read_csv('data_files/FAOSTAT_data_en_11-12-2025.csv')
        df_fao_filtered = df_fao_raw[
            (df_fao_raw['Element'] == 'Import quantity') & 
            (df_fao_raw['Value'] != 0)
        ][['Item', 'Year', 'Unit', 'Value']].copy()
        
        preloaded['fao_live_animals'] = df_fao_filtered
        
    fert_needing_pools = {'rw'}
    if not fert_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader FAOSTAT data for gjødselimport (FAOSTAT_data_en_11-12-2025-2)...")    
        # ==========================================
        # DATAINNLESING FOR MINERALGJØDSEL (MC-KLAR)
        # ==========================================
        
        # Les inn og grovfiltrer FAOSTAT-gjødseldata med en gang
        df_fert_raw = pd.read_csv('data_files/FAOSTAT_data_en_11-12-2025-2.csv')
        df_fert_filtered = df_fert_raw[
            (df_fert_raw['Element'] == 'Import quantity') & 
            (df_fert_raw['Value'] != 0)
        ][['Year', 'Value']].copy()
        
        # Lagre i preloaded_data
        preloaded['fao_mineral_fertilizer'] = df_fert_filtered
        
    return preloaded