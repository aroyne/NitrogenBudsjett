import os
import sys
import time
import argparse
import numpy as np
import pandas as pd
import os


# Sørg for at rotmappen ligger i Python-path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_all_data
from calculations.n_params import NParameters
from report_generator import generate_github_pages_report

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
    return parser.parse_args()

def draw_from_pert(low, likely, high):
    """Hjelpefunksjon for PERT-distribusjon."""
    range_val = high - low
    if range_val == 0:
        return likely
    alpha = 1 + 4 * (likely - low) / range_val
    beta = 1 + 4 * (high - likely) / range_val
    return low + np.random.beta(alpha, beta) * range_val

def generate_mc_parameters_fast(base_params, df_global, df_datasets, is_deterministic=False):
    """
    Trekker globale parametere OG genererer unike støyfaktorer for datasettene.
    Bruker de eksakte kolonnenavnene fra N_parameters.xlsx.
    """
    if is_deterministic:
        return base_params, {}
        
    # --- 1. GLOBALE PARAMETERE ---
    custom_dict = {}
    df_perturbed = df_global.copy()
    
    # Antar at global-arket bruker samme standardnavn:
    for idx, row in df_perturbed.iterrows():
        pid = row['parameter_id']
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
        
    base_params.override_global_params(custom_dict)
    if hasattr(base_params, '_tables') and 'global_parameters' in base_params._tables:
        base_params._tables['global_parameters'] = df_perturbed
    elif hasattr(base_params, 'tables') and 'global_parameters' in base_params.tables:
        base_params.tables['global_parameters'] = df_perturbed

    # --- 2. STØYFAKTORER FOR DATASETT (Nå med de eksakte kolonnenavnene) ---
    dataset_noise_dict = {}
    
    for _, row in df_datasets.iterrows():
        # Slår opp direkte med de korrekte kolonnenavnene fra bildene dine
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
            # Absolutt usikkerhet (Sentrert rundt 0.0, trekker standardisert avvik mellom -1 og +1)
            base_val = 0.0
            abs_min = -1.0
            abs_max = 1.0
            std_dev = 1.0 / 1.96
            
            if 'pert' in dist_type:
                noise_val = draw_from_pert(abs_min, base_val, abs_max)
            else:
                noise_val = np.random.normal(base_val, std_dev)
        
        # Lagre strukturen slik at beregningsfunksjonene i at_mc.py får alt de trenger
        dataset_noise_dict[ds_id] = {
            'value': noise_val,
            'type': unc_type,
            'low_bound': low_b,
            'upp_bound': upp_b
        }

    return base_params, dataset_noise_dict

# def generate_mc_parameters_fast(base_params, df_global, df_datasets, is_deterministic=False):
#     """
#     Trekker globale parametere OG genererer unike støyfaktorer for datasettene.
#     Tar strengt hensyn til om usikkerheten er oppgitt som 'perc' eller 'abs' 
#     i kolonnen 'uncertainty_type'.
#     """
#     if is_deterministic:
#         return base_params, {}
        
#     # --- 1. GLOBALE PARAMETERE ---
#     custom_dict = {}
#     df_perturbed = df_global.copy()
    
#     col_lower = [c for c in df_perturbed.columns if 'lower_bound' in c][0]
#     col_upper = [c for c in df_perturbed.columns if 'upper_bound' in c][0]
#     col_unc_type = [c for c in df_perturbed.columns if 'uncertainty_type' in c or c.startswith('uncertainty_') and c != col_lower and c != col_upper][0]
#     col_dist_type = [c for c in df_perturbed.columns if 'distribution_type' in c or 'dist' in c][0]

#     for idx, row in df_perturbed.iterrows():
#         pid = row['parameter_id']
#         val = float(row['value'])
        
#         low_b = row[col_lower]
#         upp_b = row[col_upper]
#         unc_type = str(row[col_unc_type]).lower().strip() if not pd.isna(row[col_unc_type]) else 'perc'
#         dist_type = str(row[col_dist_type]).lower().strip() if not pd.isna(row[col_dist_type]) else 'norm'
        
#         if pd.isna(low_b) or pd.isna(upp_b) or (low_b == 0 and upp_b == 0):
#             custom_dict[pid] = val
#             continue
            
#         low_b = float(low_b)
#         upp_b = float(upp_b)
        
#         # --- Sjekk uncertainty_type for globale parametere ---
#         if unc_type == 'perc':
#             abs_min = val * (1 - low_b / 100.0)
#             abs_max = val * (1 + upp_b / 100.0)
#             std_dev = ((low_b + upp_b) / 2.0 / 100.0) * val
#         elif unc_type == 'abs':
#             abs_min = val - low_b
#             abs_max = val + upp_b
#             std_dev = (low_b + upp_b) / 2.0 / 1.96  # Antar 95% KI for normalfordeling
#         else:
#             # Fallback hvis ukjent type
#             abs_min = val * (1 - low_b / 100.0)
#             abs_max = val * (1 + upp_b / 100.0)
#             std_dev = ((low_b + upp_b) / 2.0 / 100.0) * val

#         if 'pert' in dist_type:
#             chosen_val = draw_from_pert(abs_min, val, abs_max)
#         elif 'log' in dist_type:
#             cv = std_dev / val if val > 0 else 0.1
#             sigma_log = np.sqrt(np.log(1 + cv**2))
#             mu_log = np.log(val) - (sigma_log ** 2) / 2
#             chosen_val = np.random.lognormal(mu_log, sigma_log)
#         else:
#             chosen_val = np.random.normal(val, std_dev)

#         if val >= 0 and chosen_val < 0:
#             chosen_val = 0.0
            
#         custom_dict[pid] = chosen_val
#         df_perturbed.at[idx, 'value'] = chosen_val
        
#     base_params.override_global_params(custom_dict)
    
#     if hasattr(base_params, '_tables') and 'global_parameters' in base_params._tables:
#         base_params._tables['global_parameters'] = df_perturbed
#     elif hasattr(base_params, 'tables') and 'global_parameters' in base_params.tables:
#         base_params.tables['global_parameters'] = df_perturbed

#     # --- 2. STØYFAKTORER FOR DATASETT (Med 'abs' vs 'perc' logikk) ---
#     # --- INNE I GENERATE_MC_PARAMETERS_FAST (DEL 2: DATASETT) ---
#     dataset_noise_dict = {}
    
#     for _, row in df_datasets.iterrows():
#         ds_id = str(row[d_name]).strip()
#         low_b = float(row[d_lower]) if not pd.isna(row[d_lower]) else 0.0
#         upp_b = float(row[d_upper]) if not pd.isna(row[d_upper]) else 0.0
#         unc_type = str(row[d_unc_type]).lower().strip() if not pd.isna(row[d_unc_type]) else 'perc'
#         dist_type = str(row[d_dist_type]).lower().strip() if not pd.isna(row[d_dist_type]) else 'pert'
        
#         if unc_type == 'perc':
#             # PROSENT: Sentrert rundt 1.0. Grenser blir f.eks. 0.9 og 1.1 for 10%
#             base_val = 1.0
#             abs_min = base_val * (1 - low_b / 100.0)
#             abs_max = base_val * (1 + upp_b / 100.0)
#             std_dev = ((low_b + upp_b) / 2.0 / 100.0) * base_val
            
#             if 'pert' in dist_type:
#                 noise_val = draw_from_pert(abs_min, base_val, abs_max)
#             elif 'log' in dist_type:
#                 cv = std_dev / base_val
#                 sigma_log = np.sqrt(np.log(1 + cv**2))
#                 mu_log = np.log(base_val) - (sigma_log ** 2) / 2
#                 noise_val = np.random.lognormal(mu_log, sigma_log)
#             else:
#                 noise_val = np.random.normal(base_val, std_dev)
                
#         else:
#             # ABSOLUTT: Sentrert rundt 0.0. Vi trekker et tall mellom -1 og +1
#             base_val = 0.0
#             abs_min = -1.0
#             abs_max = 1.0
#             std_dev = 1.0 / 1.96 # Standardavvik for en standard normalfordeling
            
#             if 'pert' in dist_type:
#                 noise_val = draw_from_pert(abs_min, base_val, abs_max)
#             else:
#                 # Normalfordeling sentrert rundt 0 med std=1
#                 noise_val = np.random.normal(base_val, std_dev)
        
#         # Lagre både verdien og typen så beregningsfunksjonen vet hva den har fått!
#         dataset_noise_dict[ds_id] = {
#             'value': noise_val,
#             'type': unc_type,
#             'low_bound': low_b,
#             'upp_bound': upp_b
#         }

#     return base_params, dataset_noise_dict


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

    # 1. PRE-LOAD DATA (Tung fil-I/O skjer kun ÉN gang her)
    preloaded_data = load_all_data(selected_pools)
    
    # --- 1. PRE-LOAD PARAMETERE KUN ÉN GANG HER (FØR LOOPEN) ---
    print("[INFO] Pre-loader N_parameters.xlsx inn i RAM...")
    base_params = NParameters("data_files/N_parameters.xlsx")
    df_global_static = base_params.get_table('global_parameters') # Holdes i minnet
    
    # Hent ut tabellen over globale parametere med distribusjoner og grenser
    df_global_static = base_params.get_table('global_parameters')
    
    # Lag en ren ordbok med de originale deterministiske verdiene for nullstilling
    original_clean_dict = dict(zip(df_global_static['parameter_id'], df_global_static['value']))
    
    df_dataset_uncertainties = base_params.get_table('dataset_uncertainties')

    
    # --- NY SIKKERHETSSJEKK FOR HANDELSDATA (Fikser advarselen din) ---
    # Sørg for at 'trade_params' ligger i preloaded_data slik at at_mc.py finner det
    if 'trade_params' not in preloaded_data:
        preloaded_data['trade_params'] = base_params.get_trade_params()
        
    # Noen ganger lagrer data_loader tabellen under navnet 'trade' eller 'trade_data'.
    # Vi mapper den om til 'prepared_trade_all' hvis at_mc.py krever det navnet:
    if 'prepared_trade_all' not in preloaded_data:
        if 'trade' in preloaded_data:
            preloaded_data['prepared_trade_all'] = preloaded_data['trade']
        elif 'trade_data' in preloaded_data:
            preloaded_data['prepared_trade_all'] = preloaded_data['trade_data']
        elif 'ssb_trade' in preloaded_data:
            preloaded_data['prepared_trade_all'] = preloaded_data['ssb_trade']

    # --- DIAGNOSTISK SJEKK FOR Å SE HVA SOM MANGLER HVIS DET FORTSATT IKKE GÅR ---
    # print("[DEBUG] prepared_trade_all finnes:", preloaded_data.get('prepared_trade_all') is not None)
    # print("[DEBUG] trade_params finnes:", preloaded_data.get('trade_params') is not None)
    
    # Liste for å samle opp absolutt alle rader fra alle iterasjoner
    all_mc_records = []
    
    print(f"\n[INFO] Starter simuleringsløkke: Kjører {args.nsim} iterasjoner...")
    start_time = time.time()

    for i in range(args.nsim):
        if i == 0:
            # Første runde: Helt deterministisk. 
            # Vi tvinger objektet til å bruke den originale, rene tabellen.
            if hasattr(base_params, '_tables'):
                base_params._tables['global_parameters'] = df_global_static.copy()
            elif hasattr(base_params, 'tables'):
                base_params.tables['global_parameters'] = df_global_static.copy()
            base_params.override_global_params(original_clean_dict)
            current_params = base_params
            
            # --- KRITISK FIKS: Definer en tom ordbok for den deterministiske runden ---
            dataset_noise = {} 
            
        else:
            # Følgende runder: Nullstill først til originalen, og generer så NY støy i tabellen
            if hasattr(base_params, '_tables'):
                base_params._tables['global_parameters'] = df_global_static.copy()
            elif hasattr(base_params, 'tables'):
                base_params.tables['global_parameters'] = df_global_static.copy()
            base_params.override_global_params(original_clean_dict)
            
            # --- RETTET: Husk å sende med df_dataset_uncertainties her ---
            current_params, dataset_noise = generate_mc_parameters_fast(
                base_params, 
                df_global_static, 
                df_dataset_uncertainties,  # <--- Denne må med!
                is_deterministic=False
            )
        
        iteration_output = {}
        
        # 2. KJØR BEREGNINGER FOR AKTIVERTE POOLER
        if 'at' in selected_pools:
            from calculations.at_mc import execute_calculations_mc
            # Nå eksisterer dataset_noise uansett om i == 0 eller i > 0!
            iteration_output['at'] = execute_calculations_mc(preloaded_data, current_params, dataset_noise)
        
        iteration_output = {}
        
        # 2. KJØR BEREGNINGER FOR AKTIVERTE POOLER
        if 'at' in selected_pools:
            from calculations.at_mc import execute_calculations_mc
            iteration_output['at'] = execute_calculations_mc(preloaded_data, current_params, dataset_noise)

        # --- DIAGNOSTISK SJEKK FOR ITERASJON 0 (DETERMINISTISK) ---
        if i == 0 and 'at' in iteration_output:
            print("\n" + "="*60)
            print("DIAGNOSTISK SJEKK (Iterasjon 0 / Deterministisk):")
            
            at_res = iteration_output['at']
            value_rdn = None
            value_oxn = None
            verdi_2020_ammonia = None
            verdi_2020_ag = None
            verdi_2020_fo = None
            verdi_2020_ol = None
            verdi_2020_sw = None
            verdi_dep_oxn = None
            verdi_dep_rdn = None
            
            for r in at_res:
                if r['year'] == 2020:
                    if r['flow_name'] == 'AT.AT-RW.RW-Atmospheric outflow-RDN':
                        value_rdn = r['value']
                    elif r['flow_name'] == 'AT.AT-RW.RW-Atmospheric outflow-OXN':
                        value_oxn = r['value']
                    elif r['flow_name'] == 'AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2':
                        verdi_2020_ammonia = r['value']
                    elif r['flow_name'] == 'AT.AT-AG.SM-Biological N2 fixation-N2':
                        verdi_2020_ag = r['value']
                    elif r['flow_name'] == 'AT.AT-FS.FO-N2 fixation-N2':
                        verdi_2020_fo = r['value']
                    elif r['flow_name'] == 'AT.AT-FS.OL-N2 fixation-N2':
                        verdi_2020_ol = r['value']
                    elif r['flow_name'] == 'AT.AT-HY.SW-N2 fixation-N2':
                        verdi_2020_sw = r['value']
                    elif r['flow_name'] == 'AT.AT-AG.SM-Deposition-OXN':
                        verdi_dep_oxn = r['value']
                    elif r['flow_name'] == 'AT.AT-AG.SM-Deposition-RDN':
                        verdi_dep_rdn = r['value']
                        
            print(f"  RDN outflow for år 2020: {value_rdn:.4f} kt N" if value_rdn is not None else "  RDN: Ikke funnet")
            print(f"  OXN outflow for år 2020: {value_oxn:.4f} kt N" if value_oxn is not None else "  OXN: Ikke funnet")
            
            if verdi_2020_ammonia is not None:
                print(f"  Ammoniakksyntese for år 2020: {verdi_2020_ammonia:.4f} kt N")
            if verdi_2020_ag is not None:
                print(f"  AG Biological N2 fixation for år 2020: {verdi_2020_ag:.4f} kt N")
            if verdi_2020_fo is not None:
                print(f"  FO N2 fixation for år 2020: {verdi_2020_fo:.4f} kt N")
            if verdi_2020_ol is not None:
                print(f"  OL N2 fixation for år 2020: {verdi_2020_ol:.4f} kt N")
            if verdi_2020_sw is not None:
                print(f"  SW N2 fixation for år 2020: {verdi_2020_sw:.4f} kt N")
            if verdi_dep_oxn is not None:
                print(f"  Deposition OXN (jordbruk) for år 2020: {verdi_dep_oxn:.4f} kt N")
            if verdi_dep_rdn is not None:
                print(f"  Deposition RDN (jordbruk) for år 2020: {verdi_dep_rdn:.4f} kt N")
                
            print("="*60 + "\n")

        # --- SAMLE OPP OG TAGGE DATA MED SIM_ID ---
        for pool_name, pool_results in iteration_output.items():
            for row in pool_results:
                row_copy = row.copy()
                row_copy['sim_id'] = i
                all_mc_records.append(row_copy)

    elapsed_time = time.time() - start_time
    print(f"[SUKSESS] Simulering av {args.nsim} runder fullført på {elapsed_time:.4f} sekunder.")

    # --- 3. STATISTISK ANALYSE, EXCEL-EKSPORT OG PLOTTING ---
    from utils_stat import process_and_export_mc_results
    process_and_export_mc_results(all_mc_records)
    
    generate_github_pages_report()

if __name__ == '__main__':
    main()