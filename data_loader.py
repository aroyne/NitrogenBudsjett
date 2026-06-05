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

    return preloaded