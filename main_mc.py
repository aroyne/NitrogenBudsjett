#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI entry point and Monte Carlo driver for the nitrogen budget model: loads
source data and parameters once, draws all MC input values up front from one
seed (mc_sampler.py), runs the requested number of MC iterations across the
selected pools, then hands the collected results off to utils_stat.py for
statistical aggregation, to report_generator.py for the GitHub Pages report,
and optionally writes the aggregated medians/CVs back into the official
Report.xlsx template.
"""
import os
import sys
import json
import time
import argparse
import pandas as pd
import openpyxl

# Ensures the repo root is on the Python path regardless of the caller's cwd.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_all_data
from calculations.n_params import NParameters
from mc_sampler import MCSampler, DEFAULT_SEED, TRUNCATED_NORMAL_DRAWS
from calculations import utils as calc_utils
from report_generator import generate_github_pages_report
from utils_stat import process_and_export_mc_results

REPORT_PATH = "Report.xlsx"
SHEET_NAME = "2a. Database N flows"

class YearNotFoundError(Exception): pass


def parse_arguments():
    """Handles command-line arguments for the MC run."""
    parser = argparse.ArgumentParser(description="Monte Carlo framework for the nitrogen model.")
    parser.add_argument(
        '--pool',
        type=str,
        required=True,
        help="Which pool(s) to run (e.g. 'at', 'rw', 'all')"
    )
    parser.add_argument(
        '--nsim',
        type=int,
        default=100,
        help="Number of Monte Carlo iterations to run"
    )
    parser.add_argument(
        '--no-excel',
        action='store_true',
        help="Skip writing results to the official Excel report"
    )
    parser.add_argument(
        '--export-raw-mc',
        action='store_true',
        help="Also export every individual MC iteration's per-flow-year values "
             "(not just the median/percentile summary) to "
             "output_files/MC_Raw_Simulations.csv.gz, for uncertainty-aware "
             "trend analysis (calculations_for_article.py), and every drawn "
             "input value to output_files/MC_Raw_Parameters.csv.gz"
    )
    parser.add_argument(
        '--uncertainty-contributions',
        action='store_true',
        help="After the MC run, run a first-order sensitivity analysis "
             "(uncertainty_contributions.py, about 8 minutes) and write "
             "output_files/MC_uncertainty_contributions.csv, used for the "
             "Uncertainty table on each flow page"
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=DEFAULT_SEED,
        help="Master seed for all MC draws; the same seed reproduces the same run"
    )
    return parser.parse_args()


def write_mc_flows_to_international_report(summary_df):
    """
    Writes aggregated results directly into the official Excel template,
    using the exact column layout of the '2a. Database N flows' sheet.
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
    print("[EXCEL] Skriver oppdaterte MC-resultater (sentralverdi og usikkerhet) til Excel-databasen...")

    # Column layout of the '2a. Database N flows' sheet.
    FIRST_DATA_ROW = 3     # data starts on row 3, after the two header rows

    CODE_COL = 3           # column C: 'Flow Code' (the full unique name)
    VALUE_COL = 14         # column N: 'Value' (kt N)
    UNCERTAINTY_COL = 15   # column O: 'Uncertainty' (%)
    YEAR_COL = 16          # column P: 'Year'
    DATASOURCE_COL = 17    # column Q: 'Data sources'
    COMMENT_COL = 18       # column R: 'Comment'

    for _, row_data in summary_df.iterrows():
        flow_name = str(row_data["flow_name"]).strip()
        year = int(row_data["year"]) 
        value = row_data["central"]
        uncertainty_percent = row_data["uncertainty_percent"]
        comment = row_data.get("comment", "")
        data_sources = row_data.get("data_sources", "")

        year_found = False
        flow_found = False

        # Scan the sheet row by row.
        for row in range(FIRST_DATA_ROW, sheet.max_row + 1):
            cell_value = sheet.cell(row=row, column=YEAR_COL).value

            if cell_value is None:
                continue

            try:
                # Column P's year is sometimes stored as a string or a date.
                year_in_row = int(float(str(cell_value).strip()))
            except (ValueError, TypeError):
                continue

            # If the year matches, check whether the flow code in column C also matches.
            if year_in_row == year:
                year_found = True
                name_in_row = sheet.cell(row=row, column=CODE_COL).value or ""
                
                if str(name_in_row).strip() == flow_name:
                    # Write the values into their exact columns.
                    sheet.cell(row=row, column=VALUE_COL, value=value)

                    # Uncertainty is stored as a real fraction in Excel (e.g. 0.20 for 20%).
                    sheet.cell(row=row, column=UNCERTAINTY_COL, value=uncertainty_percent / 100.0)
                    
                    if data_sources:
                        sheet.cell(row=row, column=DATASOURCE_COL, value=data_sources)
                    if comment:
                        sheet.cell(row=row, column=COMMENT_COL, value=comment)
                        
                    flow_found = True
                    break

        if year_found and not flow_found:
            # Logged rather than raised: not every flow is necessarily reported in this template.
            print(f"[INFO] Strømkode '{flow_name}' ble ikke funnet for året {year} i Excel-malen. Hopper over.")
        if not year_found:
            raise YearNotFoundError(
                f"Året {year} mangler helt eller har feil format i kolonne P (16) i Excel-malen! "
                f"Sjekk rad {FIRST_DATA_ROW} og nedover."
            )

    workbook.save(REPORT_PATH)
    print("[SUCCESS] Det offisielle Excel-dokumentet er oppdatert på en strukturert måte!")


POOL_ORDER = ['at', 'rw', 'ag', 'hy', 'fs', 'ef', 'hs', 'mp', 'pr']


def run_once(preloaded_data, current_params, dataset_noise, current_trade_factors, selected_pools):
    """
    Runs the selected pools once with the given parameter values and returns
    the flow records of all pools, without any statistics or report output.
    Pools run in POOL_ORDER; mp's mass-balance residual (Consumer goods) is
    computed inside mp from flows it computes itself.
    """
    from calculations.at_mc import execute_calculations_at
    from calculations.rw_mc import execute_calculations_rw
    from calculations.ag_mc import execute_calculations_ag
    from calculations.hy_mc import execute_calculations_hy
    from calculations.fs_mc import execute_calculations_fs
    from calculations.ef_mc import execute_calculations_ef
    from calculations.hs_mc import execute_calculations_hs
    from calculations.mp_mc import execute_calculations_mp
    from calculations.pr_mc import execute_calculations_pr

    runners = {
        'at': lambda: execute_calculations_at(preloaded_data, current_params, dataset_noise, current_trade_factors),
        'rw': lambda: execute_calculations_rw(preloaded_data, current_params, dataset_noise, current_trade_factors),
        'ag': lambda: execute_calculations_ag(preloaded_data, current_params, dataset_noise, current_trade_factors),
        'hy': lambda: execute_calculations_hy(preloaded_data, current_params, dataset_noise),
        'fs': lambda: execute_calculations_fs(preloaded_data, current_params, dataset_noise),
        'ef': lambda: execute_calculations_ef(preloaded_data, current_params, dataset_noise, current_trade_factors),
        'hs': lambda: execute_calculations_hs(preloaded_data, current_params, dataset_noise, current_trade_factors),
        'mp': lambda: execute_calculations_mp(preloaded_data, current_params, dataset_noise, current_trade_factors),
        'pr': lambda: execute_calculations_pr(preloaded_data, current_params, dataset_noise, current_trade_factors),
    }
    calc_utils.RESIDUAL_FLOOR_LOG.clear()
    records = []
    for pool in POOL_ORDER:
        if pool in selected_pools:
            records.extend(runners[pool]())
    return records


def write_residual_floor_report(floor_records, nsim, path='output_files/MC_residual_floors.csv'):
    """
    How often each residual flow was negative and set to 0
    (calculations.utils.floor_residual_at_zero), per flow and year: share of
    the random iterations, whether the deterministic run was floored, and the
    median of the negative values. Written to path and printed.
    """
    cols = ['flow_name', 'year', 'sim_id', 'value']
    # A residual computed in a shared function called from two pools is
    # logged twice per iteration.
    df = pd.DataFrame(floor_records, columns=cols).drop_duplicates(['flow_name', 'year', 'sim_id'])
    n_random = max(nsim - 1, 1)
    rnd = df[df['sim_id'] > 0]
    summary = rnd.groupby(['flow_name', 'year']).agg(
        n_floored=('value', 'size'), median_negative_value=('value', 'median')).reset_index()
    summary['share_floored'] = summary['n_floored'] / n_random
    det = set(map(tuple, df.loc[df['sim_id'] == 0, ['flow_name', 'year']].to_numpy()))
    summary['deterministic_floored'] = [(f, y) in det for f, y in zip(summary['flow_name'], summary['year'])]
    summary.to_csv(path, index=False)
    print(f"[INFO] Avkapping ved 0 i rester: {len(summary)} strøm-år berørt, skrevet til {path}.")
    for flow, g in summary.groupby('flow_name'):
        print(f"  {flow}: {len(g)} år, maks {100 * g['share_floored'].max():.1f} % av iterasjonene"
              f"{' (også deterministisk: ' + str(sorted(g.loc[g.deterministic_floored, 'year'])) + ')' if g.deterministic_floored.any() else ''}")


def setup_iteration(base_params, sampler, i):
    """
    Pushes iteration i's drawn values onto base_params and returns
    (current_params, dataset_noise, current_trade_factors). Iteration 0 is
    the deterministic baseline.
    """
    param_overrides, dataset_noise, trade_factors = sampler.iteration(i)
    base_params.override_global_params(param_overrides)
    return base_params, dataset_noise, trade_factors


def main():
    args = parse_arguments()

    pool_input = args.pool.lower().strip()
    if pool_input == 'all':
        selected_pools = list(POOL_ORDER)
    else:
        selected_pools = [p.strip() for p in pool_input.split(',')]
        unknown = set(selected_pools) - set(POOL_ORDER)
        if unknown:
            raise ValueError(f"Ukjente pooler: {sorted(unknown)}")

    print("="*60)
    print("[INFO] Starter MC-rammeverk.")
    print(f"[INFO] Aktiverte pooler: {', '.join(selected_pools).upper()}")
    print(f"[INFO] Antall ønskede iterasjoner: {args.nsim}")
    print(f"[INFO] Frø: {args.seed}")
    print("="*60)

    # 1. PRE-LOAD DATA AND PARAMETERS ONCE
    preloaded_data = load_all_data(selected_pools)

    print("[INFO] Pre-loader N_parameters.xlsx inn i RAM...")
    base_params = NParameters("parameters/N_parameters.xlsx")
    if 'trade_params' not in preloaded_data:
        preloaded_data['trade_params'] = base_params.get_trade_params()

    print("[INFO] Trekker alle MC-verdier på forhånd...")
    sampler = MCSampler(base_params, preloaded_data['trade_params'], args.nsim, seed=args.seed)
    print(f"[INFO] {TRUNCATED_NORMAL_DRAWS[0]} normalfordelte trekk under 0 er trukket på nytt.")

    all_mc_records = []
    floor_records = []

    print(f"\n[INFO] Starter simuleringsløkke: Kjører {args.nsim} iterasjoner...")
    start_time = time.time()

    for i in range(args.nsim):
        if args.nsim <= 10 or i % (10 if args.nsim <= 100 else 50) == 0:
            print(f"[INFO] Starter iterasjon {i} av {args.nsim}")

        current_params, dataset_noise, current_trade_factors = setup_iteration(base_params, sampler, i)
        records = run_once(preloaded_data, current_params, dataset_noise, current_trade_factors, selected_pools)

        for row in records:
            row_copy = row.copy()
            row_copy['sim_id'] = i
            all_mc_records.append(row_copy)
        floor_records.extend((f, y, i, v) for f, y, v in calc_utils.RESIDUAL_FLOOR_LOG)

    elapsed_time = time.time() - start_time
    print(f"[SUKSESS] Simulering av {args.nsim} runder fullført på {elapsed_time:.4f} sekunder.")

    os.makedirs('output_files', exist_ok=True)
    write_residual_floor_report(floor_records, args.nsim)
    run_info = {'seed': args.seed, 'nsim': args.nsim, 'pools': selected_pools,
                'finished': time.strftime('%Y-%m-%d %H:%M:%S')}
    with open('output_files/MC_run_info.json', 'w') as f:
        json.dump(run_info, f, indent=2)

    if args.export_raw_mc:
        print("[INFO] Eksporterer rå per-iterasjon-data (--export-raw-mc)...")
        raw_df = pd.DataFrame(all_mc_records)
        raw_path = 'output_files/MC_Raw_Simulations.csv.gz'
        raw_df.to_csv(raw_path, index=False, compression='gzip')
        print(f"[SUKSESS] Rådata skrevet til {raw_path} ({len(raw_df):,} rader).")
        param_path = 'output_files/MC_Raw_Parameters.csv.gz'
        sampler.to_long().to_csv(param_path, index=False, compression='gzip')
        print(f"[SUKSESS] Trukne parameterverdier skrevet til {param_path}.")

    # 3. STATISTICAL ANALYSIS, EXCEL EXPORT AND PLOTTING
    summary_df = process_and_export_mc_results(all_mc_records)

    if args.no_excel:
        print("[INFO] Kjører UTEN å skrive til offisiell Excel-mal (--no-excel er aktiv).")
    else:
        write_mc_flows_to_international_report(summary_df)

    if args.uncertainty_contributions:
        import uncertainty_contributions
        print("[INFO] Beregner bidrag til usikkerhet per strøm (--uncertainty-contributions)...")
        setup_iteration(base_params, sampler, 0)
        uncertainty_contributions.write(*uncertainty_contributions.compute(
            run_once, preloaded_data, base_params, selected_pools, args.seed))

    # 4. WEBSITE GENERATION
    generate_github_pages_report()

if __name__ == '__main__':
    main()
