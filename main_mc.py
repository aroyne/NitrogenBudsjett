#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse
import numpy as np
import pandas as pd
import openpyxl

# Sørg for at rotmappen ligger i Python-path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_all_data
from calculations.n_params import NParameters
from report_generator import generate_github_pages_report
from utils_stat import process_and_export_mc_results

# ==============================================================================
# EXCEL-KONFIGURASJON FOR INTERNASJONAL RAPPORTERING
# ==============================================================================
REPORT_PATH = "Report.xlsx"  # Endre til din faktiske bane
SHEET_NAME = "2a. Database N flows"                                       # Navnet på fanen i Excel
FIRST_DATA_ROW = 3     # Raden der de faktiske dataene starter

YEAR_COL = 1           # Kolonne A: Årstall
NAME_COL = 2           # Kolonne B: Strømkode / Flow Name
VALUE_COL = 3          # Kolonne C: Verdi (Median fra MC)
UNCERTAINTY_COL = 4    # Kolonne D: Symmetrisk usikkerhet (CV% / 100)
DATASOURCE_COL = 5     # Kolonne E: Datakilder
COMMENT_COL = 6        # Kolonne F: Kommentarer

class FlowNotFoundError(Exception): pass
class YearNotFoundError(Exception): pass


def parse_arguments():
    """Håndterer kommandolinjeargumenter for MC-kjøringen."""
    parser = argparse.ArgumentParser(description="Monte Carlo-rammeverk for Nitrogenmodellen.")
    parser.add_argument(
        '--pool', 
        type=str, 
        required=True, 
        help="Hvilken pool som skal kjøres (f.eks. 'at', 'rw', 'all')"
    )
    parser.add_argument(
        '--nsim', 
        type=int, 
        default=100, 
        help="Antall Monte Carlo-simuleringer (iterasjoner) som skal kjøres"
    )
    # Legg til denne:
    parser.add_argument(
        '--no-excel',
        action='store_true',
        help="Hopper over skriving av resultater til den offisielle Excel-rapporten"
    )
    return parser.parse_args()


def draw_from_pert(low, likely, high):
    """Hjelpefunksjon for PERT-distribusjon."""
    range_val = high - low
    if range_val == 0:
        return likely
    alpha = 1 + 4 * (likely - low) / range_val
    beta = 1 + 4 * (high - likely) / range_val
    return low + np.random.beta(alpha, beta) * range_val


def generate_mc_parameters_fast(base_params, df_global, df_datasets, df_animal_products_static, df_trade_params=None, df_animal_weights=None, is_deterministic=False):
    """
    Trekker globale parametere, genererer unike støyfaktorer for datasettene,
    OG genererer unike perturberte N-faktorer for handelsvarer, dyrevekter og dyreprodukter.
    Alt samles som flate nøkler inni custom_dict som sendes til base_params.
    """
    # --- ROBUST IDENTIFIKASJON AV ID FOR HANDELSDATA ---
    pid_col = None
    df_trade_local = None
    if df_trade_params is not None:
        df_trade_local = df_trade_params.copy()
        idx_name = str(df_trade_local.index.name).lower().strip() if df_trade_local.index.name else ''
        if idx_name in ['param_id', 'parameter_id', 'konv', 'id']:
            df_trade_local = df_trade_local.reset_index()
            
        clean_cols = {str(c).lower().strip(): c for c in df_trade_local.columns}
        for variant in ['param_id', 'parameter_id', 'konv', 'id']:
            if variant in clean_cols:
                pid_col = clean_cols[variant]
                break
                
        if pid_col is None and len(df_trade_local) > 0:
            if isinstance(df_trade_local[df_trade_local.columns[0]].iloc[0], str):
                pid_col = df_trade_local.columns[0]

    # --- DETERMINISTISK GREN (Runde i=0) ---
    if is_deterministic:
        static_trade = {}
        if df_trade_local is not None and pid_col is not None:
            keys = df_trade_local[pid_col].astype(str).str.strip()
            static_trade = dict(zip(keys, df_trade_local['value']))
            
        custom_dict = {}
        
        # Flate ut animal_weights deterministisk (Lik original)
        if df_animal_weights is not None:
            for _, row in df_animal_weights.iterrows():
                t_id = f"weight_{str(row.name).strip()}" if df_animal_weights.index.name == 'item_name' else f"weight_{str(row['item_name']).strip()}"
                custom_dict[t_id] = float(row['avg_weight_kg'])
                
        # Flate ut animal_products deterministisk (Nye harmoniserte måten)
        if df_animal_products_static is not None:
            for _, row in df_animal_products_static.iterrows():
                p_id = f"prod_{str(row['item']).strip()}"
                custom_dict[p_id] = float(row['N_content_percent'])
        
        base_params.override_global_params(custom_dict)

        return base_params, {}, static_trade
        
    # --- 1. GLOBALE PARAMETERE ---
    custom_dict = {}
    df_perturbed = df_global.copy()
    
    global_idx_name = str(df_perturbed.index.name).lower().strip() if df_perturbed.index.name else ''
    if global_idx_name in ['param_id', 'parameter_id', 'id'] or 'param_id' not in df_perturbed.columns:
        df_perturbed = df_perturbed.reset_index()
    
    global_pid_col = 'param_id'
    for c in df_perturbed.columns:
        if str(c).lower().strip() in ['param_id', 'parameter_id', 'id']:
            global_pid_col = c
            break
    
    for idx, row in df_perturbed.iterrows():
        pid = row[global_pid_col]
        val = float(row['value'])
        low_b = row['lower_bound']
        upp_b = row['upper_bound']
        unc_type = str(row['uncertainty_type']).lower().strip() if not pd.isna(row['uncertainty_type']) else 'perc'
        dist_type = str(row['distribution_type']).lower().strip() if not pd.isna(row['distribution_type']) else 'norm'
        
        if pd.isna(low_b) or pd.isna(upp_b) or (low_b == 0 and upp_b == 0):
            custom_dict[pid] = val
            continue
            
        low_b = float(low_b)
        upp_b = float(upp_b)
        
        if unc_type == 'perc':
            abs_min = val * (1 - low_b / 100.0)
            abs_max = val * (1 + upp_b / 100.0)
            std_dev = ((low_b + upp_b) / 2.0 / 100.0) * val
        else:
            abs_min = val - low_b
            abs_max = val + upp_b
            std_dev = (low_b + upp_b) / 2.0 / 1.96

        if 'pert' in dist_type:
            chosen_val = draw_from_pert(abs_min, val, abs_max)
        elif 'log' in dist_type:
            cv = std_dev / val if val > 0 else 0.1
            sigma_log = np.sqrt(np.log(1 + cv**2))
            mu_log = np.log(val) - (sigma_log ** 2) / 2
            chosen_val = np.random.lognormal(mu_log, sigma_log)
        else:
            chosen_val = np.random.normal(val, std_dev)

        if val >= 0 and chosen_val < 0:
            chosen_val = 0.0
            
        custom_dict[pid] = chosen_val
        df_perturbed.at[idx, 'value'] = chosen_val
        
    if hasattr(base_params, '_tables') and 'global_parameters' in base_params._tables:
        base_params._tables['global_parameters'] = df_perturbed
    elif hasattr(base_params, 'tables') and 'global_parameters' in base_params.tables:
        base_params.tables['global_parameters'] = df_perturbed

    # --- 2. STØYFAKTORER FOR DATASETT ---
    dataset_noise_dict = {}
    for _, row in df_datasets.iterrows():
        ds_id = str(row['dataset_name']).strip()
        low_b = float(row['lower_bound']) if not pd.isna(row['lower_bound']) else 0.0
        upp_b = float(row['upper_bound']) if not pd.isna(row['upper_bound']) else 0.0
        unc_type = str(row['uncertainty_type']).lower().strip() if not pd.isna(row['uncertainty_type']) else 'perc'
        dist_type = str(row['distribution_type']).lower().strip() if not pd.isna(row['distribution_type']) else 'pert'
        
        if unc_type == 'perc':
            base_val = 1.0
            abs_min = base_val * (1 - low_b / 100.0)
            abs_max = base_val * (1 + upp_b / 100.0)
            std_dev = ((low_b + upp_b) / 2.0 / 100.0) * base_val
            if 'pert' in dist_type:
                noise_val = draw_from_pert(abs_min, base_val, abs_max)
            elif 'log' in dist_type:
                cv = std_dev / base_val
                sigma_log = np.sqrt(np.log(1 + cv**2))
                mu_log = np.log(base_val) - (sigma_log ** 2) / 2
                noise_val = np.random.lognormal(mu_log, sigma_log)
            else:
                noise_val = np.random.normal(base_val, std_dev)
        else:
            base_val = 0.0
            abs_min = -1.0
            abs_max = 1.0
            std_dev = 1.0 / 1.96
            if 'pert' in dist_type:
                noise_val = draw_from_pert(abs_min, base_val, abs_max)
            else:
                noise_val = np.random.normal(base_val, std_dev)
        
        dataset_noise_dict[ds_id] = {'value': noise_val, 'type': unc_type, 'low_bound': low_b, 'upp_bound': upp_b}

    # --- 3. PERTURBERING AV TRADE_PARAMETERS ---
    trade_noise_dict = {}
    if df_trade_local is not None and pid_col is not None:
        for _, row in df_trade_local.iterrows():
            t_id = str(row[pid_col]).strip()
            val = float(row['value'])
            low_b = row['lower_bound'] if 'lower_bound' in row else 0.0
            upp_b = row['upper_bound'] if 'upper_bound' in row else 0.0
            unc_type = str(row['uncertainty_type']).lower().strip() if 'uncertainty_type' in row and not pd.isna(row['uncertainty_type']) else 'perc'
            dist_type = str(row['distribution_type']).lower().strip() if 'distribution_type' in row and not pd.isna(row['distribution_type']) else 'norm'
            
            if pd.isna(low_b) or pd.isna(upp_b) or (low_b == 0 and upp_b == 0):
                trade_noise_dict[t_id] = val
                continue
                
            low_b = float(low_b)
            upp_b = float(upp_b)
            
            if unc_type == 'perc':
                abs_min = val * (1 - low_b / 100.0)
                abs_max = val * (1 + upp_b / 100.0)
                std_dev = ((low_b + upp_b) / 2.0 / 100.0) * val
            else:
                abs_min = val - low_b
                abs_max = val + upp_b
                std_dev = (low_b + upp_b) / 2.0 / 1.96

            if 'pert' in dist_type:
                noise_val = draw_from_pert(abs_min, val, abs_max)
            elif 'log' in dist_type:
                cv = std_dev / val if val > 0 else 0.1
                sigma_log = np.sqrt(np.log(1 + cv**2))
                mu_log = np.log(val) - (sigma_log ** 2) / 2
                noise_val = np.random.lognormal(mu_log, sigma_log)
            else:
                noise_val = np.random.normal(val, std_dev)

            if val >= 0 and noise_val < 0:
                noise_val = 0.0
                
            trade_noise_dict[t_id] = noise_val
            
    # --- 4. PERTURBERING AV ANIMAL WEIGHTS ---
    if df_animal_weights is not None:
        for _, row in df_animal_weights.iterrows():
            t_id = f"weight_{str(row.name).strip()}" if df_animal_weights.index.name == 'item_name' else f"weight_{str(row['item_name']).strip()}"
            val = float(row['avg_weight_kg'])
            low_b = float(row['low_bound']) if 'low_bound' in row and not pd.isna(row['low_bound']) else 0.0
            upp_b = float(row['upp_bound']) if 'upp_bound' in row and not pd.isna(row['upp_bound']) else 0.0
            unc_type = str(row['type']).lower().strip() if 'type' in row and not pd.isna(row['type']) else 'perc'
            dist_type = str(row['distribution_type']).lower().strip() if 'distribution_type' in row and not pd.isna(row['distribution_type']) else 'norm'
            
            if low_b == 0 and upp_b == 0:
                custom_dict[t_id] = val
                continue
                
            if unc_type == 'perc':
                abs_min = val * (1 - low_b / 100.0)
                abs_max = val * (1 + upp_b / 100.0)
                std_dev = ((low_b + upp_b) / 2.0 / 100.0) * val
            else:
                abs_min = val - low_b
                abs_max = val + upp_b
                std_dev = (low_b + upp_b) / 2.0 / 1.96

            if 'pert' in dist_type:
                chosen_val = draw_from_pert(abs_min, val, abs_max)
            elif 'log' in dist_type:
                cv = std_dev / val if val > 0 else 0.1
                sigma_log = np.sqrt(np.log(1 + cv**2))
                mu_log = np.log(val) - (sigma_log ** 2) / 2
                chosen_val = np.random.lognormal(mu_log, sigma_log)
            else:
                chosen_val = np.random.normal(val, std_dev)

            if val >= 0 and chosen_val < 0:
                chosen_val = 0.0
                
            custom_dict[t_id] = chosen_val

    # --- 5. PERTURBERING AV ANIMAL PRODUCTS (NÅ HELT LIK SOM VEKTER) ---
    if df_animal_products_static is not None:
        for _, row in df_animal_products_static.iterrows():
            p_id = f"prod_{str(row['item']).strip()}"
            base_val = float(row['N_content_percent'])
            dist_type = str(row.get('distribution_type', 'norm')).strip().lower()
            u_val = float(row.get('upper_bound', 0.0)) / 100.0
            
            if u_val > 0:
                if dist_type == 'unif':
                    perturbed_val = base_val * np.random.uniform(1.0 - u_val, 1.0 + u_val)
                else:
                    perturbed_val = base_val * np.random.normal(1.0, u_val)
            else:
                perturbed_val = base_val
            
            if perturbed_val < 0: 
                perturbed_val = 0.0
            
            custom_dict[p_id] = perturbed_val

    # Send alle flate parametere inn sentralt
    base_params.override_global_params(custom_dict)
        
    return base_params, dataset_noise_dict, trade_noise_dict

def write_mc_flows_to_international_report(summary_df):
    """
    Skriver aggregerte resultater direkte til den offisielle Excel-malen.
    Basert på nøyaktig kolonne-mapping fra arket '2a. Database N flows'.
    """
    if not os.path.exists(REPORT_PATH):
        print(f"[INFO] Fant ikke Excel-malen på '{REPORT_PATH}'. Hopper over offisiell rapportering.")
        return

    print(f"[EXCEL] Åpner offisiell rapporteringsmal: {REPORT_PATH}...")
    workbook = openpyxl.load_workbook(REPORT_PATH)
    
    if SHEET_NAME not in workbook.sheetnames:
        print(f"[ALARM] Fant ikke fanen '{SHEET_NAME}' i Excel-arket. Avbryter skriving.")
        return
        
    sheet = workbook[SHEET_NAME]
    print("[EXCEL] Skriver oppdaterte MC-resultater (Median og CV%) til Excel-databasen...")

    # ==============================================================================
    # STRENG KOLONNE-MAPPING BASERT PÅ BILDER FRA MALEN
    # ==============================================================================
    FIRST_DATA_ROW = 3     # Data starter på rad 3 (etter overskriftene på rad 1 og 2)
    
    CODE_COL = 3           # Kolonne C: 'Flow Code' (Det fulle unike navnet)
    VALUE_COL = 14         # Kolonne N: 'Value' (kt N)
    UNCERTAINTY_COL = 15   # Kolonne O: 'Uncertainty' (%)
    YEAR_COL = 16          # Kolonne P: 'Year'
    DATASOURCE_COL = 17    # Kolonne Q: 'Data sources'
    COMMENT_COL = 18       # Kolonne R: 'Comment'

    for _, row_data in summary_df.iterrows():
        flow_name = str(row_data["flow_name"]).strip()
        year = int(row_data["year"]) 
        value = row_data["median"]
        cv_percent = row_data["cv_percent"]
        comment = row_data.get("comment", "")
        data_sources = row_data.get("data_sources", "")

        year_found = False
        flow_found = False

        # Gå gjennom tabellen vertikalt rad for rad
        for row in range(FIRST_DATA_ROW, sheet.max_row + 1):
            cell_value = sheet.cell(row=row, column=YEAR_COL).value
            
            if cell_value is None:
                continue
                
            try:
                # Sikker vask og konvertering av årstallet fra kolonne P
                year_in_row = int(float(str(cell_value).strip()))
            except (ValueError, TypeError):
                continue

            # Hvis vi matcher på året, sjekker vi om strømkoden i kolonne C også matcher
            if year_in_row == year:
                year_found = True
                name_in_row = sheet.cell(row=row, column=CODE_COL).value or ""
                
                if str(name_in_row).strip() == flow_name:
                    # Skriv data inn i de nøyaktige kolonnene
                    sheet.cell(row=row, column=VALUE_COL, value=value)
                    
                    # CV% lagres vanligvis som et reelt tall (f.eks. 0.20 for 20 %) i Excel
                    sheet.cell(row=row, column=UNCERTAINTY_COL, value=cv_percent / 100.0)
                    
                    if data_sources:
                        sheet.cell(row=row, column=DATASOURCE_COL, value=data_sources)
                    if comment:
                        sheet.cell(row=row, column=COMMENT_COL, value=comment)
                        
                    flow_found = True
                    break

        if year_found and not flow_found:
            # Vi logger i stedet for å krasje, i tilfelle enkelte strømmer ikke rapporteres i denne malen
            print(f"[INFO] Strømkode '{flow_name}' ble ikke funnet for året {year} i Excel-malen. Hopper over.")
        if not year_found:
            raise YearNotFoundError(
                f"Året {year} mangler helt eller har feil format i kolonne P (16) i Excel-malen! "
                f"Sjekk rad {FIRST_DATA_ROW} og nedover."
            )

    workbook.save(REPORT_PATH)
    print("[SUCCESS] Det offisielle Excel-dokumentet er oppdatert på en strukturert måte!")

    
def main():
    args = parse_arguments()
    
    pool_input = args.pool.lower().strip()
    if pool_input == 'all':
        selected_pools = ['at', 'rw', 'mp', 'pr', 'fs', 'hs', 'hy']
    else:
        selected_pools = [p.strip() for p in pool_input.split(',')]

    print("="*60)
    print("[INFO] Starter MC-rammeverk.")
    print(f"[INFO] Aktiverte pooler: {', '.join(selected_pools).upper()}")
    print(f"[INFO] Antall ønskede iterasjoner: {args.nsim}")
    print("="*60)

    # 1. PRE-LOAD DATA OG PARAMETERE KUN ÉN GANG
    preloaded_data = load_all_data(selected_pools)
    
    print("[INFO] Pre-loader N_parameters.xlsx inn i RAM...")
    base_params = NParameters("data_files/N_parameters.xlsx")
    df_global_static = base_params.get_table('global_parameters')
    original_clean_dict = dict(zip(df_global_static['parameter_id'], df_global_static['value']))
    df_dataset_uncertainties = base_params.get_table('dataset_uncertainties')
    
    # --- HER DEFINERER DU df_animal_weights ---
    print("[INFO] Henter animal_weights tabell fra base_params...")
    try:
        df_animal_weights = base_params.get_table('animal_weights')
    except Exception as e:
        print(f"[ADVARSEL] Fant ikke 'animal_weights' i base_params. Setter til None: {e}")
        df_animal_weights = None
        
    # Hent animal_products tabellen fra base_params
    print("[INFO] Henter animal_products tabell fra base_params...")
    try:
        df_animal_products_static = base_params.get_table('animal_products')
    except Exception as e:
        print(f"[KRITISK FEIL] Fant ikke 'animal_products' i base_params: {e}")
        df_animal_products_static = None
        
    # Sikkerhetssjekk og mapping for handelsdata
    if 'trade_params' not in preloaded_data:
        preloaded_data['trade_params'] = base_params.get_trade_params()
        
    if 'prepared_trade_all' not in preloaded_data:
        if 'trade' in preloaded_data:
            preloaded_data['prepared_trade_all'] = preloaded_data['trade']
        elif 'trade_data' in preloaded_data:
            preloaded_data['prepared_trade_all'] = preloaded_data['trade_data']
        elif 'ssb_trade' in preloaded_data:
            preloaded_data['prepared_trade_all'] = preloaded_data['ssb_trade']
            
    # # --- MIDLERTIDIG FEILSØKING FOR Å SJEKKE KOLONNER ---
    # df_trade_params = preloaded_data.get('trade_params')
    # if df_trade_params is not None:
    #     print("\n" + "="*60)
    #     print("[DEBUG] Sjekker trade_parameters fra data_loader:")
    #     print("Kolonnenavn (headers):", df_trade_params.columns.tolist())
    #     print("Indeks-navn (row index):", df_trade_params.index.name)
    #     print("Første rad med data:\n", df_trade_params.head(1).to_string())
    #     print("="*60 + "\n")
        
    #     # Framprovoser en kontrollert stopp så du slipper å kjøre hele MC
    #     import sys; sys.exit("[DEBUG STOPP] Kolonner er printet, avbryter kjøring.")

    all_mc_records = []
    
    print(f"\n[INFO] Starter simuleringsløkke: Kjører {args.nsim} iterasjoner...")
    start_time = time.time()

    for i in range(args.nsim):
        # Nullstill tabeller til statiske verdier før hver runde
        if hasattr(base_params, '_tables'):
            base_params._tables['global_parameters'] = df_global_static.copy()
        elif hasattr(base_params, 'tables'):
            base_params.tables['global_parameters'] = df_global_static.copy()
        base_params.override_global_params(original_clean_dict)

        if i == 0:
            # Første runde: Helt deterministisk baseline (is_deterministic=True)
            df_trade_params = preloaded_data['trade_params']
            current_params, dataset_noise, current_trade_factors = generate_mc_parameters_fast(
                base_params, 
                df_global_static, 
                df_dataset_uncertainties,
                df_animal_products_static,
                df_trade_params=df_trade_params,
                df_animal_weights=df_animal_weights,  # <-- LEGG TIL DENNE
                is_deterministic=True
            )
            dataset_noise = {}        
        else:
            # Følgende runder: Generer stokastisk støy
            df_trade_params = preloaded_data['trade_params']
            current_params, dataset_noise, current_trade_factors = generate_mc_parameters_fast(
                base_params, 
                df_global_static, 
                df_dataset_uncertainties,
                df_animal_products_static,
                df_trade_params=df_trade_params,
                df_animal_weights=df_animal_weights,  # <-- LEGG TIL DENNE
                is_deterministic=(i==0)
            )
            
        iteration_output = {}
        
        # 2. KJØR BEREGNINGER FOR AKTIVERTE POOLER
        if 'at' in selected_pools:
            from calculations.at_mc import execute_calculations_at
            iteration_output['at'] = execute_calculations_at(preloaded_data, current_params, dataset_noise, current_trade_factors)
            
        if 'rw' in selected_pools:
            from calculations.rw_mc import execute_calculations_rw  # Sjekk at funksjonsnavnet stemmer
            iteration_output['rw'] = execute_calculations_rw(preloaded_data, current_params, dataset_noise, current_trade_factors)
            
        if 'ag' in selected_pools:
            from calculations.ag_mc import execute_calculations_ag  # Sjekk at funksjonsnavnet stemmer
            iteration_output['ag'] = execute_calculations_ag(preloaded_data, current_params, dataset_noise, current_trade_factors)
            
        if 'hy' in selected_pools:
            from calculations.hy_mc import execute_calculations_hy  # Sjekk at funksjonsnavnet stemmer
            iteration_output['hy'] = execute_calculations_hy(preloaded_data, current_params, dataset_noise)
            
        # (Her legger du inn de andre poolene etter hvert: if 'rw' in selected_pools... osv.)

        # --- DIAGNOSTISK SJEKK FOR ITERASJON 0 (DETERMINISTISK) ---
        # if i == 0 and 'at' in iteration_output:
        #     print("\n" + "="*60)
        #     print("DIAGNOSTISK SJEKK (Iterasjon 0 / Deterministisk):")
        #     at_res = iteration_output['at']
            
        #     flows_to_check = {
        #         'AT.AT-RW.RW-Atmospheric outflow-RDN': 'RDN outflow for år 2020',
        #         'AT.AT-RW.RW-Atmospheric outflow-OXN': 'OXN outflow for år 2020',
        #         'AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2': 'Ammoniakksyntese for år 2020',
        #         'AT.AT-AG.SM-Biological N2 fixation-N2': 'AG Biological N2 fixation for år 2020',
        #         'AT.AT-FS.FO-N2 fixation-N2': 'FO N2 fixation for år 2020',
        #         'AT.AT-FS.OL-N2 fixation-N2': 'OL N2 fixation for år 2020',
        #         'AT.AT-HY.SW-N2 fixation-N2': 'SW N2 fixation for år 2020',
        #         'AT.AT-AG.SM-Deposition-OXN': 'Deposition OXN (jordbruk) for år 2020',
        #         'AT.AT-AG.SM-Deposition-RDN': 'Deposition RDN (jordbruk) for år 2020'
        #     }
            
        #     for r in at_res:
        #         if r['year'] == 2020 and r['flow_name'] in flows_to_check:
        #             print(f"  {flows_to_check[r['flow_name']]}: {r['value']:.4f} kt N")
        #     print("="*60 + "\n")

        # --- SAMLE OPP OG TAGGE DATA MED SIM_ID ---
        for pool_name, pool_results in iteration_output.items():
            for row in pool_results:
                row_copy = row.copy()
                row_copy['sim_id'] = i
                all_mc_records.append(row_copy)

    elapsed_time = time.time() - start_time
    print(f"[SUKSESS] Simulering av {args.nsim} runder fullført på {elapsed_time:.4f} sekunder.")

    # 3. STATISTISK ANALYSE, EXCEL-EKSPORT OG PLOTTING
    summary_df = process_and_export_mc_results(all_mc_records)
    
    if args.no_excel:
        print("[INFO] Kjører UTEN å skrive til offisiell Excel-mal (--no-excel er aktiv).")
    else:
        # Hvis flagget IKKE er med, kjører vi som vanlig
        write_mc_flows_to_international_report(summary_df)
    
    # 5. NETTSIDE-GENERERING
    generate_github_pages_report()


if __name__ == '__main__':
    main()