#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 07:36:42 2026

@author: anja
"""
def load_all_data(selected_pools):
    preloaded = {}
    if 'at' in selected_pools:
        # Kun les inn hvis vi skal kjøre atmosfære
        import pandas as pd
        df_raw = pd.read_excel('data_files/atm_in_out.xlsx', sheet_name='Ark1')
        # Gjør den groveste rensingen her (f.eks. plukk ut rader/kolonner)
        preloaded['atm_in_out'] = df_raw
    return preloaded