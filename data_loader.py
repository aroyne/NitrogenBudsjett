#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import openpyxl
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
            
    # OPPDATERT: Lagt til 'ag' i trade_needing_pools
    trade_needing_pools = {'at', 'rw', 'mp', 'pr', 'ef', 'ag'}
    if not trade_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader komplett varehandelsstatistikk koblet mot alle kategorier...")
        try:
            df_trade_raw = read_trade_data('data_files/Tab_08801_1988_2024.csv')
            
            from calculations.n_params import NParameters
            params_excel = NParameters("data_files/N_parameters.xlsx")
            df_mapping = params_excel.get_trade_mapping()
            
            if 'konv' not in df_mapping.columns:
                df_mapping = df_mapping.reset_index()
                
            df_trade_raw['HS_code_str'] = df_trade_raw['HS_code'].astype(str).str.strip()
            v_col = 'Varenr' if 'Varenr' in df_mapping.columns else 'varenr'
            df_mapping['varenr_str'] = df_mapping[v_col].astype(str).str.strip()
            
            df_prepared_all = df_trade_raw.merge(
                df_mapping[[v_col, 'konv', 'type', 'varenr_str']],
                left_on='HS_code_str',
                right_on='varenr_str',
                how='inner'
            )
            
            print("[INFO] Komprimerer 6 mill rader handelsdata til en kjapp volum-matrise...")
            df_volum_aggregated = df_prepared_all.groupby(['year', 'impeks', 'type', 'konv'])['amount'].sum().reset_index()
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
            
    # 4. DEPONERINGSDATA (OPPDATERT: Lagt til 'ag' i sjekken hvis aktuelt)
    deposition_needing_pools = {'at', 'ag'}
    if not deposition_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader NILU deponeringsdata (N_per_class_period_distributed_unallocated_long.csv)...")
        try:
            preloaded['deposition_data'] = pd.read_csv('data_files/N_per_class_period_distributed_unallocated_long.csv')
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade deponeringsdata: {e}")
            
    # 5. IMPORT AV DYREFÔR
    if 'rw' in selected_pools:
        print("[I/O] Pre-loader Landbruksdirektoratets kraftfôrstatistikk (Årlig råvareforbruk.xlsx)...")
        df_raavarer = pd.read_excel('data_files/Årlig råvareforbruk.xlsx', sheet_name='Varegrupper')
        df_raavarer_clean = pd.DataFrame({
            'year': df_raavarer.iloc[3:28, 0].astype(int),
            'value_carb': df_raavarer.iloc[3:28, 2].astype(float),
            'value_prot': df_raavarer.iloc[3:28, 8].astype(float)
        }).reset_index(drop=True)
        preloaded['feed_raavarer'] = df_raavarer_clean

    if 'rw' in selected_pools:
        print("[I/O] Pre-loader NIBIO Totalkalkylen innkjøpt kraftfôr (NibioStatistics-4.xlsx)...")    
        df_totalkalkyle = pd.read_excel('data_files/NibioStatistics-4.xlsx', sheet_name='Sum innkjøpt kraftfôr ukorr.')
        df_totalkalkyle_clean = pd.DataFrame({
            'year': df_totalkalkyle.iloc[26:41, 0].astype(int),
            'value': df_totalkalkyle.iloc[26:41, 1].astype(float),
            'dom_frac': df_totalkalkyle.iloc[26:41, 4].astype(float)
        }).reset_index(drop=True)
        preloaded['feed_totalkalkyle'] = df_totalkalkyle_clean
    
    # 6. AKVAKULTUR
    aq_needing_pools = {'hy', 'rw'}
    if not aq_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader data for akvakultur...")    
        df_aqua_modern_raw = pd.read_excel('data_files/A.06.002_20251111-140559.xlsx', sheet_name='A.06.002', header=None)
        years_modern = df_aqua_modern_raw.iloc[2, 2:].astype(int).tolist()
        df_modern_data_cells = df_aqua_modern_raw.iloc[4:43, 2:].replace('-', 0).astype(float)
        df_modern_data_cells.columns = years_modern
        preloaded['aqua_modern'] = df_modern_data_cells
        
        df_aqua_old_raw = pd.read_excel('data_files/akvakultur_1984_1994.xlsx', sheet_name='Ark1', header=None)
        df_old_clean = pd.DataFrame({
            'year': df_aqua_old_raw.iloc[1:11, 0].astype(int),
            'value': df_aqua_old_raw.iloc[1:11, 1].astype(float)
        }).reset_index(drop=True)
        preloaded['aqua_old'] = df_old_clean
        
    # 7. FAOSTAT LEVENDE DYR
    live_animals_needing_pools = {'ag','rw'}
    if not live_animals_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader FAOSTAT data for levende dyr...")    
        df_fao_raw = pd.read_csv('data_files/FAOSTAT_data_en_11-12-2025.csv')
        df_fao_filtered = df_fao_raw[(df_fao_raw['Element'] == 'Import quantity') & (df_fao_raw['Value'] != 0)][['Item', 'Year', 'Unit', 'Value']].copy()
        preloaded['fao_live_animals'] = df_fao_filtered
        df_fao_export = df_fao_raw[(df_fao_raw['Element'] == 'Export quantity') & (df_fao_raw['Value'] != 0)][['Item', 'Year', 'Unit', 'Value']].copy()
        preloaded['fao_live_animals_export'] = df_fao_export
        
    # 8. MINERALGJØDSELIMPORT
    fert_needing_pools = {'rw'}
    if not fert_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader FAOSTAT data for gjødselimport...")    
        df_fert_raw = pd.read_csv('data_files/FAOSTAT_data_en_11-12-2025-2.csv')
        df_fert_filtered = df_fert_raw[(df_fert_raw['Element'] == 'Import quantity') & (df_fert_raw['Value'] != 0)][['Year', 'Value']].copy()
        preloaded['fao_mineral_fertilizer'] = df_fert_filtered

    
    # TEOTIL Avløp fra Report.xlsx
    kyst_needing_pools = {'hy'}
    if not kyst_needing_pools.isdisjoint(selected_pools):
        try:
            df_kyst = pd.read_excel('data_files/Tilførsel av nitrogen til kystområdene fordelt på kilder.xlsx', sheet_name='Data fra Miljødirektoratet')
            preloaded['hy_kyst_tilforsel'] = df_kyst
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade kysttilførsel-Excel: {e}")

    # TEOTIL3 N Summary (totn_to_coast, totn_by_source, totn_retention)
    teotil3_needing_pools = {'hy'}
    if not teotil3_needing_pools.isdisjoint(selected_pools):
        try:
            wb_teotil3 = openpyxl.load_workbook('data_files/teotil3_n_summary.xlsx', data_only=True)
            preloaded['hy_teotil3_to_coast'] = pd.DataFrame(list(wb_teotil3['totn_to_coast'].values))
            preloaded['hy_teotil3_by_source'] = pd.DataFrame(list(wb_teotil3['totn_by_source'].values))
            preloaded['hy_teotil3_retention'] = pd.DataFrame(list(wb_teotil3['totn_retention'].values))
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade teotil3_n_summary.xlsx: {e}")

    # Fiskeridirektoratet: art.xlsx
    fangst_needing_pools = {'hy'}
    if not fangst_needing_pools.isdisjoint(selected_pools):
        try:
            wb_art = openpyxl.load_workbook('data_files/art.xlsx', data_only=True)
            preloaded['hy_art_raw'] = pd.DataFrame(list(wb_art['Sheet 1'].values))
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade art.xlsx: {e}")

    # Historisk fiske: fiske_1990_2000.xlsx
    fangst_old_needing_pools = {'hy'}
    if not fangst_old_needing_pools.isdisjoint(selected_pools):
        try:
            wb_fiske_old = openpyxl.load_workbook('data_files/fiske_1990_2000.xlsx', data_only=True)
            preloaded['hy_fiske_old_raw'] = pd.DataFrame(list(wb_fiske_old['Ark1'].values))
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade fiske_1990_2000.xlsx: {e}")

    # --- NYTT FOR AVLØP (SHARED FLOW) ---
    sewage_needing_pools = {'hy','pr'}
    if not sewage_needing_pools.isdisjoint(selected_pools):
        try:
            wb_05280 = openpyxl.load_workbook('data_files/05280_20251113-113329.xlsx', data_only=True)
            preloaded['hy_ssb_05280_raw'] = pd.DataFrame(list(wb_05280['Nitrogen'].values))
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade 05280_20251113-113329.xlsx: {e}")

        try:
            wb_utslipp = openpyxl.load_workbook('data_files/utslipp_avløp.xlsx', data_only=True)
            preloaded['hy_utslipp_avlop_raw'] = pd.DataFrame(list(wb_utslipp['Ark1'].values))
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade utslipp_avløp.xlsx: {e}")

    # =========================================================================
    # NYTT: NYE DATAINNLESINGER FOR LANDBRUKS-POOLEN (AG / AG_MC)
    # =========================================================================
    if 'ag' in selected_pools:
        print("[I/O] Pre-loader data spesifikt for Landbruk (ag)...")
        
        # Eurostat Gross Nutrient Balance (GNB) Excel-ark
        try:
            wb_gnb = openpyxl.load_workbook('data_files/aei_pr_gnb__custom_18744910_spreadsheet.xlsx', data_only=True)
            preloaded['ag_gnb_workbook'] = wb_gnb
            preloaded['gnb_sheet30_raw'] = pd.DataFrame(list(wb_gnb['Sheet 30'].values))
            if 'Sheet 12' in wb_gnb.sheetnames:
                preloaded['gnb_sheet12_raw'] = pd.DataFrame(list(wb_gnb['Sheet 12'].values))
            else:
                print("[ADVARSEL] Sheet 12 mangler i GNB-filen!")
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke laste Eurostat GNB Excel: {e}")

        # SSB Grovfôrtabeller
        try:
            wb_13648 = openpyxl.load_workbook('data_files/13648_20251117-154625.xlsx', data_only=True)
            wb_05772 = openpyxl.load_workbook('data_files/05772_20251210-142618.xlsx', data_only=True)
            wb_old = openpyxl.load_workbook('data_files/grovfor_før_2000.xlsx', data_only=True)
            
            preloaded['ag_ssb_13648'] = wb_13648
            preloaded['ag_ssb_05772'] = wb_05772
            preloaded['ag_grovfor_old'] = wb_old
            
            # NYTT: Konverter til DataFrames med en gang for å unngå openpyxl i MC-løkka
            preloaded['ssb_13648_raw'] = pd.DataFrame(list(wb_13648['Avling'].values))
            preloaded['ssb_05772_raw'] = pd.DataFrame(list(wb_05772['Gronfor'].values))
            preloaded['grovfor_old_raw'] = pd.DataFrame(list(wb_old['Ark1'].values))
            
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke laste SSB grovfôrtabeller: {e}")
            
        # CRLTAP Tekstfil (Sektordata for utslipp)
        try:
            # Siden denne leses rått via load_crltap_emissions_to_N i utils, lagrer vi banen eller innholdet.
            # Det tryggeste for open() i eksterne funksjoner er å lagre filbanen, eventuelt lese filen som streng-liste:
            with open('data_files/webdabData1863365.txt', 'r', encoding='utf-8', errors='ignore') as f:
                preloaded['ag_crltap_raw_lines'] = f.readlines()
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke pre-loade CRLTAP tekstfil: {e}")

        # UNFCCC N2O og NOx Excel
        try:
            wb_unfccc = openpyxl.load_workbook('data_files/N2O_NOx_AG.xlsx', data_only=True)
            preloaded['ag_unfccc_excel'] = wb_unfccc
            
            # NYTT: Konverter Ark1 til en ren DataFrame med en gang under I/O-steget
            preloaded['unfccc_ark1_raw'] = pd.DataFrame(list(wb_unfccc['Ark1'].values))
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke laste N2O_NOx_AG.xlsx: {e}")
            
        # Hydrologi / avrenningsdata CSV (Nr_AG--HY.csv)
        try:
            preloaded['ag_leaching_csv'] = pd.read_csv('data_files/Nr_AG--HY.csv')
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke laste Nr_AG--HY.csv: {e}")

        # FAOSTAT Animals and Production (FAOSTAT_data_en_11-18-2025.csv)
        try:
            df_fao = pd.read_csv('data_files/FAOSTAT_data_en_11-18-2025.csv')
            preloaded['ag_faostat_production'] = df_fao
            
            # NYTT: Gjør unna den tunge filtreringen med en gang under I/O-steget
            filtered_fao = df_fao[
                (df_fao['Element'] == 'Production') & 
                (df_fao['Value'] != 0) & 
                (~df_fao['Item'].str.contains('hides', case=False, na=False))
            ]
            # Ta kun vare på kolonnene vi faktisk trenger videre
            preloaded['fao_animal_production_clean'] = filtered_fao[['Item', 'Year', 'Value']].copy()
            
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke laste FAOSTAT animal production: {e}")
            
        # =========================================================================
        # REVIDERT: DATAINNLESINGER FOR HUDER OG ULL (AG / AG_MC)
        # =========================================================================
        try:
            print("[I/O] Laster og klargjør FAOSTAT-data for kjøtt, melk og huder...")
            # df_fao = pd.read_csv('data_files/FAOSTAT_data_en_11-18-2025.csv')
            # preloaded['ag_faostat_production'] = df_fao
            
            # A. Renset tabell for vanlige spiselige dyreprodukter (Uten huder)
            filtered_fao = df_fao[
                (df_fao['Element'] == 'Production') & 
                (df_fao['Value'] != 0) & 
                (~df_fao['Item'].str.contains('hides', case=False, na=False))
            ]
            preloaded['fao_animal_production_clean'] = filtered_fao[['Item', 'Year', 'Value']].copy()
            
            # B. Egen renset tabell for huder (Kun huder)
            filtered_hides = df_fao[
                (df_fao['Element'] == 'Production') & 
                (df_fao['Value'] != 0) & 
                (df_fao['Item'].str.contains('hides', case=False, na=False))
            ]
            preloaded['fao_hides_clean'] = filtered_hides[['Item', 'Year', 'Value']].copy()
            
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke laste FAOSTAT animal production: {e}")

        # C. Last inn ull-produksjon (Landbruksdirektoratet)
        try:
            print("[I/O] Pre-loader ulldata (ull.xlsx)...")
            df_wool_raw = pd.read_excel('data_files/ull.xlsx', skiprows=3)
            preloaded['wool_production'] = df_wool_raw[['år', 'ull']].copy()
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke laste ull.xlsx: {e}")

        # D. Last inn sauetall (SSB tabell 03710)
        try:
            print("[I/O] Pre-loader sauetall fra SSB (03710_20260128-152225.xlsx)...")
            df_sheep_raw = pd.read_excel('data_files/03710_20260128-152225.xlsx', skiprows=2)
            preloaded['ssb_sheep_numbers'] = df_sheep_raw[['År', 'Husdyr (sau)']].copy()
        except Exception as e:
            print(f"[KRITISK FEIL] Kunne ikke laste SSB-sauetall: {e}")
            
    return preloaded