#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loads every source data file the calculations/ modules need, gated by which
pools are requested (selected_pools). Most entries in DATA_MAP go through the
generic per-method loading loop below and end up under their own dict key,
but a handful of methods load one workbook and split it into several output
keys instead - for those, the DATA_MAP key itself (e.g. 'ag_gnb', 'ag_grovfor',
'aqua_data', 'avlop_sewage', 'hy_teotil3', 'fs_obb_grazing',
'fao_live_animals_all', 'ag_faostat_production_all', 'ag_manure_crt') exists only to gate
loading by pool membership and is never read back; the actual data lives
under the differently-named keys set inside that method's branch.
"""
import os
import re
import pandas as pd
import openpyxl
import warnings
from calculations.utils import read_trade_data

# Suppresses openpyxl's specific header/footer warning.
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.worksheet.header_footer")


def _find_crt_row(sheet, path, header_window=200, item_window=12):
    """
    Locates a data row in a UNFCCC CRT Table1.A(a) sheet by following a
    sequence of column-B label substrings (e.g. ['1.A.3.c.  Railways',
    'Liquid fuels']), rather than a hardcoded row number - CRT row numbers
    shift between submission years as UNFCCC adds/removes sub-rows (verified:
    several rows moved by 2-3 positions between the 2024 and 2026 Norwegian
    submissions). The first label is searched from the top of the sheet
    (a section header can be anywhere); each subsequent label is searched
    only in the few rows right after the previous match, since CRT sheets
    always list a category's Liquid/Solid/Gaseous/Other fossil/Biomass
    fuel-type breakdown immediately below that category's header.
    """
    anchor = 1
    found = None
    for i, label in enumerate(path):
        window = header_window if i == 0 else item_window
        found = None
        for r in range(anchor, anchor + window):
            cell_val = sheet.cell(row=r, column=2).value
            if cell_val is not None and label in str(cell_val):
                found = r
                break
        if found is None:
            raise ValueError(f"CRT row label path {path!r} failed at {label!r} (searched rows {anchor}-{anchor + window - 1})")
        anchor = found + 1
    return found


def _crt_iter_workbooks(crt_folder):
    """Yields (year, workbook) for every per-year xlsx in a UNFCCC CRT
    submission folder, read-only. Caller is responsible for closing each
    workbook (and for opening the specific sheet(s) it needs)."""
    for fname in os.listdir(crt_folder):
        if not fname.endswith('.xlsx'):
            continue
        match = re.search(r'-(\d{4})-\d{8}', fname)
        if not match:
            continue
        year = int(match.group(1))
        wb = openpyxl.load_workbook(os.path.join(crt_folder, fname), data_only=True, read_only=True)
        yield year, wb


def _crt_cell(sheet, label_path, column):
    """Resolves label_path to a row via _find_crt_row and returns that row's
    value in `column` as a float, or None for CRT's non-numeric flags
    (IE/NA/NE/NO) and other non-numeric cells."""
    row = _find_crt_row(sheet, label_path)
    try:
        return float(sheet.cell(row=row, column=column).value)
    except (TypeError, ValueError):
        return None


def _read_crt_fuel_series(crt_folder, sheet_name, row_specs):
    """
    Reads TJ fuel consumption (column C, "Consumption, TJ") from a UNFCCC CRT
    submission folder (one workbook per inventory year) and converts to N.
    row_specs is a list of (label_path, ncv_divisor, n_content_frac) tuples;
    each label_path is resolved to a row via _find_crt_row for every year's
    workbook independently, so a row shift in one year's template can't
    silently misalign a different year's reading.
    """
    values = {}
    for fname in os.listdir(crt_folder):
        if not fname.endswith('.xlsx'):
            continue
        match = re.search(r'-(\d{4})-\d{8}', fname)
        if not match:
            continue
        year = int(match.group(1))
        wb = openpyxl.load_workbook(os.path.join(crt_folder, fname), data_only=True, read_only=True)
        sheet = wb[sheet_name]
        value = 0.0
        for label_path, ncv, n_frac in row_specs:
            row = _find_crt_row(sheet, label_path)
            cell_value = sheet.cell(row=row, column=3).value
            try:
                value += float(cell_value) / ncv * n_frac
            except (TypeError, ValueError):
                # CRT reports non-numeric flags (IE/NA/NE/NO) for combinations
                # with no estimate; treated as zero, matching the original
                # compilation notebooks' handling of the same flags.
                pass
        values[year] = value
        wb.close()
    return values


def load_all_data(selected_pools):
    preloaded = {}
    print(f"\n[DATA_LOADER] Kalles med selected_pools: {selected_pools}")

    # =========================================================================
    # 1. CONFIGURATION MAP
    # =========================================================================
    # Format: 'preloaded_key': ( {relevant_pools}, 'filepath', 'load_method', {extra_kwargs} )
    DATA_MAP = {
        'atm_in_out': ({'at', 'rw'}, 'data_files/atm_in_out.xlsx', 'excel', {'sheet_name': 'Ark1', 'header': None}),
        'faostat_fertilizer_production': ({'at'}, 'data_files/FAOSTAT_data_en_11-25-2025.csv', 'csv', {}),
        'faostat_fertilizer_use': ({'mp'}, 'data_files/FAOSTAT_data_en_11-21-2025.csv', 'csv', {}),
        'fao_mineral_fertilizer': ({'rw', 'mp'}, 'data_files/FAOSTAT_data_en_11-12-2025-2.csv', 'csv', {}),
        'deposition_data': ({'at', 'ag'}, 'data_files/N_per_class_period_distributed_unallocated_long.csv', 'csv', {}),
        'feed_raavarer_norsk': ({'mp'}, 'data_files/Årlig råvareforbruk.xlsx', 'excel_feed_raavarer_norsk', {}),
        'feed_raavarer_import': ({'rw'}, 'data_files/Årlig råvareforbruk.xlsx', 'excel_feed_raavarer_import', {}),        'feed_totalkalkyle': ({'rw','mp'}, 'data_files/NibioStatistics-4.xlsx', 'excel_feed_totalkalkyle', {}),
        'aqua_data': ({'hy', 'rw', 'mp'}, 'data_files/A.06.002_20251111-140559.xlsx', 'excel_aquaculture', {}),
        'fao_live_animals_all': ({'ag', 'rw'}, 'data_files/FAOSTAT_data_en_11-12-2025.csv', 'csv_live_animals', {}),
        'hy_kyst_tilforsel': ({'hy','fs','hs'}, 'data_files/Tilførsel av nitrogen til kystområdene fordelt på kilder.xlsx', 'excel', {'sheet_name': 'Data fra Miljødirektoratet'}),
        'hy_teotil3': ({'hy','fs','hs'}, 'data_files/teotil3_n_summary.xlsx', 'openpyxl_teotil', {}),
        'hy_art_raw': ({'hy'}, 'data_files/art.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Sheet 1'}),
        'hy_fiske_old_raw': ({'hy'}, 'data_files/fiske_1990_2000.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Ark1'}),
        'avlop_sewage': ({'hy', 'pr'}, 'data_files/05280_20251113-113329.xlsx', 'openpyxl_sewage', {}),
        'ag_gnb': ({'ag','mp'}, 'data_files/aei_pr_gnb__custom_18744910_spreadsheet.xlsx', 'openpyxl_gnb', {}),
        'ag_manure_crt': ({'ag'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_manure_applied', {}),
        'ag_innmark_grazing_raw': ({'ag'}, 'data_files/NibioStatisticsNewTK.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Eng, beite'}),
        'ag_grovfor': ({'ag'}, 'grovfor_filer_samling', 'excel_grovfor', {}),  # filepath unused - method loads 3 fixed files directly
        'ag_crltap_raw_lines': ({'ag','ef','mp','pr'}, 'data_files/webdabData1868031.txt', 'text_lines', {}),
        'unfccc_ark1_raw': ({'ag'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_n2o_ag', {}),
        'ag_leaching_csv': ({'ag'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_nr_ag', {}),
        'ag_faostat_production_all': ({'ag','mp'}, 'data_files/FAOSTAT_data_en_11-18-2025.csv', 'csv_faostat_production', {}),
        'wool_production': ({'ag','mp'}, 'data_files/ull.xlsx', 'excel', {'skiprows': 3}),
        'ssb_sheep_numbers': ({'ag','mp'}, 'data_files/03710_20260128-152225.xlsx', 'excel', {'skiprows': 2}),
        'fs_unfccc_emissions_raw': ({'fs'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_n2o_hs_fs', {}),
        'fs_firewood_raw': ({'fs'}, 'data_files/09702_20251120-133716.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'VedTonn'}),
        'fs_obb_grazing': ({'fs'}, 'data_files/OBB_Fylke_1970-2025.xlsx', 'openpyxl_obb_grazing', {}),
        'faostat_forestry': ({'fs'}, 'data_files/FAOSTAT_data_en_2-20-2026.csv', 'csv_forestry', {}),
        'fuel_for_industry': ({'ef'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_fuel_industry', {}),
        'fuel_for_transport': ({'ef'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_fuel_transport', {}),
        'fuel_for_heating': ({'ef'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_fuel_heating', {}),
        'n2o_ec_data': ({'ef'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_n2o_ec', {}),
        'n2o_so_raw': ({'pr'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_n2o_so', {}),
        'n2o_ww_raw': ({'pr'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_n2o_ww', {}),
        'n2o_nox_op_raw': ({'mp'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_n2o_op', {}),
        'trade_fuels_n_content': ({'ef'}, 'data_files/N_content_fuels.xlsx', 'excel', {}),
        'ssb_energy_balance_11561': ({'ef','mp'}, 'data_files/11561_20251113-154607.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'EnergibalansenGWh'}),
        'hs_pop_size_06913': ({'hs'}, 'data_files/06913_20251113-124117.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Folkemengde'}),
        'hs_pop_age_groups_07459': ({'hs'}, 'data_files/07459_20251119-151434.xlsx', 'excel', {'sheet_name': 'Personer1', 'skiprows': 3, 'header': None}),
        'hs_smoking_stats_05307': ({'hs'}, 'data_files/05307_20251119-152214.xlsx', 'excel', {'sheet_name': 'Dagroyk', 'skiprows': 3, 'header': None}),
        'hs_unfccc_n2o_raw': ({'hs'}, 'data_files/NOR-CRT-2026-V1.0-20260311-135213_awaiting_submission', 'crt_n2o_hs_fs', {}),
        'hs_luc_crltap_raw_lines': ({'hs'}, 'data_files/webdabData1868031.txt', 'text_lines', {}),
        'mp_sau_saakorn_raw': ({'mp'}, 'data_files/NibioStatistics-5.xlsx', 'excel', {'sheet_name': 'Sum innkjøpt såkorn', 'header': None}),
        'mp_oljefroe_raw': ({'mp'}, 'data_files/NibioStatistics-5.xlsx', 'excel', {'sheet_name': 'Oljefrø til modning', 'header': None}),
        'mp_erter_raw': ({'mp'}, 'data_files/NibioStatistics-5.xlsx', 'excel', {'sheet_name': 'Erter', 'header': None}),
        'mp_engfroe_raw': ({'mp'}, 'data_files/NibioStatistics-5.xlsx', 'excel', {'sheet_name': 'Sum engfrø', 'header': None}),
        'mp_rotvekst_groennsak_raw': ({'mp'}, 'data_files/NibioStatistics-5.xlsx', 'excel', {'sheet_name': 'Sum rotvekst- og grønnsakfrø', 'header': None}),
        'mildir_emissions': ({'mp'}, 'data_files/Årlig utslipp til vann - Landbasert 02-02-2026.xlsx', 'excel_mildir_emissions', {}),
        'industry_categories': ({'mp'}, 'data_files/industry_categories.xlsx', 'excel_industry_categories', {}),
        'ssb_waste_05281': ({'pr', 'mp'}, 'data_files/05281_20260121-140338.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Avfall'}),
        'ssb_05282': ({'hs','mp','pr'}, 'data_files/05282_20260211-091021.xlsx', 'openpyxl_single_sheet', {'sheet_name': '05282'}),
        'ssb_05543_raw': ({'mp'}, 'data_files/05543_20251217-111610.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Areal'}),
        'ssb_06913': ({'mp'}, 'data_files/06913_20251113-124117.xlsx', 'excel_population', {}),
        'ssb_06376': ({'mp'}, 'data_files/06376_20260129-155937.xlsx', 'excel_ssb_generic', {'sheet': '06376'}),
        'ssb_10249': ({'mp'}, 'data_files/10249_20260129-155747.xlsx', 'excel_ssb_generic', {'sheet': '10249'}),
        'ssb_waste_10513': ({'pr', 'mp'}, 'data_files/10513_20260916-120243.xlsx', 'openpyxl_single_sheet', {'sheet_name': '10513'}),
        'ssb_10514': ({'hs','mp','pr'}, 'data_files/10514_20260916-101643.xlsx', 'openpyxl_single_sheet', {'sheet_name': '10514'}),
        'ssb_waste_12359': ({'pr'}, 'data_files/12359_20251211-153434.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Mengde'}),
        'ssb_13695': ({'mp'}, 'data_files/13695_20260916-120402.xlsx', 'excel_ssb_generic', {'sheet': '13695'}),
        'ssb_bio_08205': ({'mp'}, 'data_files/08205_20251104-141305.xlsx', 'excel_ssb_generic', {'sheet': 'Energibruk'}),
        'ssb_bio_hist': ({'mp'}, 'data_files/egentilvirket_bioenergi_industri.xlsx', 'excel_ssb_generic', {'sheet': 'Ark1'}),
        'ssb_hist_industry_waste': ({'mp','pr'}, 'data_files/kommunalt_avfall_1985_1995.xlsx', 'excel_ssb_generic', {'sheet': 'avfallsmengder'}),
        'skoggjoedsling_foer_1995_raw': ({'mp'}, 'data_files/skoggjødsling_før_1995.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Ark1'}),
        'waste_historical_fractions': ({'pr', 'mp'}, 'data_files/kommunalt_avfall_1985_1995.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'forbrenning og gjenvinning'}),
        'biogass_tall': ({'pr'}, 'data_files/biogass_tall.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'biorest'}),
        'ssb_waste_12818': ({'pr'}, 'data_files/12818_20260526-110921.xlsx', 'openpyxl_single_sheet', {'sheet_name': '12818'}),
        'deponi_utslipp': ({'pr'}, 'data_files/Utslipp_deponi.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Utslipp'}),
        'deponi_tilkobling': ({'pr'}, 'data_files/Utslipp_deponi.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'tilkobling'}),
        'biogass_manure': ({'pr'}, 'data_files/Biogass.xlsx', 'openpyxl_single_sheet', {'sheet_name': 'Tabell'}),
        'sewage_sludge_modern': ({'pr'}, 'data_files/05279_20260121-103739.xlsx', 'openpyxl_single_sheet_df', {'sheet_name': 'Slam'}),
        'sewage_sludge_historical': ({'pr'}, 'data_files/slamdisponering.xlsx', 'openpyxl_single_sheet_df', {'sheet_name': 'Ark1'}),
        'avlop_utslipp_historical': ({'pr'}, 'data_files/utslipp_avløp.xlsx', 'openpyxl_single_sheet_df', {'sheet_name': 'Ark1'}),
        'avlop_sewage_cleaning': ({'hy', 'pr'}, 'data_files/nitrogenrensing_avløp.xlsx', 'excel', {'sheet_name': 'Ark1', 'nrows': 31}),
        }

    # =========================================================================
    # 2. TRADE DATA
    # =========================================================================
    trade_needing_pools = {'at', 'rw', 'mp', 'pr', 'ef', 'ag'}
    if not trade_needing_pools.isdisjoint(selected_pools):
        print("[I/O] Pre-loader komplett varehandelsstatistikk...")
        df_trade_raw = read_trade_data('data_files/Tab_08801_1988_2024.csv')
        from calculations.n_params import NParameters
        df_mapping = NParameters("parameters/N_parameters.xlsx").get_trade_mapping()
        if 'konv' not in df_mapping.columns:
            df_mapping = df_mapping.reset_index()

        df_trade_raw['HS_code_str'] = df_trade_raw['HS_code'].astype(str).str.strip()
        v_col = 'Varenr' if 'Varenr' in df_mapping.columns else 'varenr'
        df_mapping['varenr_str'] = df_mapping[v_col].astype(str).str.strip()

        df_prepared_all = df_trade_raw.merge(
            df_mapping[[v_col, 'konv', 'type', 'varenr_str']],
            left_on='HS_code_str', right_on='varenr_str', how='inner'
        )
        preloaded['compressed_trade_volume'] = df_prepared_all.groupby(['year', 'impeks', 'type', 'konv'])['amount'].sum().reset_index()

    # =========================================================================
    # 3. GENERIC LOADING, DRIVEN BY THE MAP ABOVE
    # =========================================================================
    for key, (pools, filepath, method, kwargs) in DATA_MAP.items():
        if pools.isdisjoint(selected_pools):
            continue  # none of the selected pools need this file
            
        print(f"[I/O] Pre-loader data for {key} ({filepath.split('/')[-1] if '/' in filepath else filepath})...")
        if method == 'excel':
            preloaded[key] = pd.read_excel(filepath, **kwargs)
            if key == 'wool_production':
                preloaded[key] = preloaded[key][['år', 'ull']].copy()
            elif key == 'ssb_sheep_numbers':
                preloaded[key] = preloaded[key][['År', 'Husdyr (sau)']].copy()

        elif method == 'csv':
            df = pd.read_csv(filepath, **kwargs)
            if key in ['faostat_fertilizer', 'fao_mineral_fertilizer', 'faostat_fertilizer_production']:
                preloaded[key] = df[['Year', 'Element', 'Value']].copy()
            else:
                preloaded[key] = df
        elif method == 'text_lines':
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                preloaded[key] = f.readlines()

        elif method == 'crt_manure_applied':
            # UNFCCC CRT (Common Reporting Table) submission, one workbook per
            # inventory year. Table3.D gives two relevant rows (both t N/year):
            # "Animal manure applied to soils" (FAM, IPCC 2006 Eq. 11.4 -
            # managed manure N net of storage/housing losses) and "Urine and
            # dung deposited by grazing animals" (PRP - manure deposited
            # directly on pasture, never routed through storage or spreading).
            fam_values = {}
            prp_values = {}
            for fname in os.listdir(filepath):
                if not fname.endswith('.xlsx'):
                    continue
                match = re.search(r'-(\d{4})-\d{8}', fname)
                if not match:
                    continue
                year = int(match.group(1))
                wb_crt = openpyxl.load_workbook(os.path.join(filepath, fname), data_only=True, read_only=True)
                ws_crt = wb_crt['Table3.D']
                for row in ws_crt.iter_rows(min_row=10, max_row=17, values_only=True):
                    if row[1] and 'Animal manure applied' in str(row[1]):
                        fam_values[year] = row[3]
                    if row[1] and 'Urine and dung deposited' in str(row[1]):
                        prp_values[year] = row[3]
                wb_crt.close()
            preloaded['ag_manure_applied_crt'] = fam_values
            preloaded['ag_manure_prp_crt'] = prp_values

        elif method == 'crt_fuel_industry':
            # UNFCCC CRT Table1.A(a)s2, "1.A.2 Manufacturing industries and
            # construction" top-level aggregate (already the sum of all its
            # sub-sectors, so no need to read further down the sheet).
            # NCVs from IPCC (2006) Table 1.2, N contents from Table 15 in
            # Schäppi (2025) Annexes.
            row_specs = [
                (['1.A.2 Manufacturing industries and construction', 'Liquid fuels'], 44, 0.0015),
                (['1.A.2 Manufacturing industries and construction', 'Solid fuels'], 25, 0.014),
                (['1.A.2 Manufacturing industries and construction', 'Other fossil fuels'], 30, 0.005),
                (['1.A.2 Manufacturing industries and construction', 'Biomass'], 30, 0.005),
            ]
            values = _read_crt_fuel_series(filepath, 'Table1.A(a)s2', row_specs)
            preloaded[key] = pd.DataFrame(sorted(values.items()), columns=['year', 'value'])

        elif method == 'crt_fuel_heating':
            # UNFCCC CRT Table1.A(a)s4, "1.A.4 Other sectors" top-level
            # aggregate (commercial/institutional + residential +
            # agriculture/forestry/fishing combined, stationary and mobile).
            row_specs = [
                (['1.A.4  Other sectors', 'Liquid fuels'], 44, 0.0015),
                (['1.A.4  Other sectors', 'Solid fuels'], 25, 0.014),
                (['1.A.4  Other sectors', 'Other fossil fuels'], 30, 0.005),
                (['1.A.4  Other sectors', 'Biomass'], 30, 0.005),
            ]
            values = _read_crt_fuel_series(filepath, 'Table1.A(a)s4', row_specs)
            preloaded[key] = pd.DataFrame(sorted(values.items()), columns=['year', 'value'])

        elif method == 'crt_fuel_transport':
            # UNFCCC CRT Table1.A(a)s3. Domestic aviation's value sits
            # directly on its own header row (already a pre-aggregated
            # total), so that entry's label path is a single element.
            row_specs = [
                (['1.A.3.a.  Domestic aviation'], 44.1, 0.001),
                (['1.A.3.b.  Road transportation', 'Diesel oil'], 43, 0.000133),
                (['1.A.3.b.  Road transportation', 'Biomass'], 27, 0.01),
                (['1.A.3.c.  Railways', 'Liquid fuels'], 44, 0.0015),
                (['1.A.3.c.  Railways', 'Solid fuels'], 25, 0.014),
                (['1.A.3.d.  Domestic Navigation', 'Residual fuel oil'], 40.4, 0.0045),
                (['1.A.3.d.  Domestic Navigation', 'Gas/diesel oil'], 43, 0.000133),
            ]
            values = _read_crt_fuel_series(filepath, 'Table1.A(a)s3', row_specs)
            preloaded[key] = pd.DataFrame(sorted(values.items()), columns=['year', 'value'])

        elif method == 'crt_n2o_ec':
            # UNFCCC CRT Table1, column E (N2O, kt), converted to N via the
            # N2/N2O molar-mass ratio (28/44 = 0.6364). Four IPCC top-level
            # categories map to the model's EC/IC/TR/OE subsectors.
            rows = []
            for year, wb in _crt_iter_workbooks(filepath):
                sheet = wb['Table1']
                ec = sum(v for v in (
                    _crt_cell(sheet, ['1.A.1. Energy industries'], 5),
                    _crt_cell(sheet, ['1.B.1. Solid fuels'], 5),
                    _crt_cell(sheet, ['1.B.2.a. Oil'], 5),
                    _crt_cell(sheet, ['1.B.2.b. Natural gas'], 5),
                    _crt_cell(sheet, ['1.B.2.d. Other'], 5),
                ) if v is not None) * 0.6364
                ic = (_crt_cell(sheet, ['1.A.2. Manufacturing industries and construction'], 5) or 0.0) * 0.6364
                tr = (_crt_cell(sheet, ['1.A.3. Transport'], 5) or 0.0) * 0.6364
                oe = sum(v for v in (
                    _crt_cell(sheet, ['1.A.4. Other sectors'], 5),
                    _crt_cell(sheet, ['1.A.5. Other'], 5),
                ) if v is not None) * 0.6364
                rows.append({'year': year, 'value_EC': ec, 'value_IC': ic, 'value_TR': tr, 'value_OE': oe})
                wb.close()
            preloaded[key] = pd.DataFrame(rows).sort_values('year').reset_index(drop=True)

        elif method == 'crt_n2o_so':
            # UNFCCC CRT Table5, "5.C. Incineration and open burning of
            # waste", column E (N2O, kt) - converted to N further downstream
            # (pr_mc.py applies N2O_to_N_factor from N_parameters.xlsx).
            rows = []
            for year, wb in _crt_iter_workbooks(filepath):
                v = _crt_cell(wb['Table5'], ['5.C. Incineration and open burning of waste'], 5)
                rows.append({'year': year, 'value': v})
                wb.close()
            preloaded[key] = pd.DataFrame(rows).sort_values('year').reset_index(drop=True)

        elif method == 'crt_n2o_ww':
            # UNFCCC CRT Table5, "5.D. Wastewater treatment and discharge",
            # column E (N2O, kt) - converted to N downstream in pr_mc.py.
            rows = []
            for year, wb in _crt_iter_workbooks(filepath):
                v = _crt_cell(wb['Table5'], ['5.D. Wastewater treatment and discharge'], 5)
                rows.append({'year': year, 'value': v})
                wb.close()
            preloaded[key] = pd.DataFrame(rows).sort_values('year').reset_index(drop=True)

        elif method == 'crt_n2o_op':
            # UNFCCC CRT Table2(I), column E (N2O, kt), summed over the
            # IPCC subcategories that report a nonzero N2O figure for other
            # producing industry (2A Mineral industry and 2D Non-energy
            # products always report zero N2O in this compilation, so are
            # skipped). Only mp_mc.py's N2O use of this table is live - the
            # matching NOx column (2A/2B/2C/2G/2H, column K) was computed by
            # the original N2O_NOx_OP.ipynb but never read by any
            # calculations/*.py file (MP.OP's NOx comes from the CRLTAP
            # webdab file instead), so it is not reproduced here.
            rows = []
            for year, wb in _crt_iter_workbooks(filepath):
                sheet = wb['Table2(I)']
                n2o = sum(v for v in (
                    _crt_cell(sheet, ['2.B.  Chemical industry'], 5),
                    _crt_cell(sheet, ['2.C.  Metal industry'], 5),
                    _crt_cell(sheet, ['2.G.  Other product manufacture and use'], 5),
                    _crt_cell(sheet, ['2.H.  Other'], 5),
                ) if v is not None)
                rows.append({'year': year, 'N2O': n2o})
                wb.close()
            preloaded[key] = pd.DataFrame(rows).sort_values('year').reset_index(drop=True)

        elif method == 'crt_n2o_ag':
            # UNFCCC CRT Table3 (agriculture summary), column E (N2O, kt).
            # "3.B. Manure management" -> MM, "3.D. Agricultural soils" -> SM.
            # Originally compiled by hand into N2O_NOx_AG.xlsx (no notebook
            # found for it); the NOx column that file also had is dropped -
            # AG's NOx comes from the CRLTAP webdab file instead and this
            # column was never read by any calculations/*.py file.
            rows = []
            for year, wb in _crt_iter_workbooks(filepath):
                sheet = wb['Table3']
                mm = _crt_cell(sheet, ['3.B. Manure management'], 5)
                sm = _crt_cell(sheet, ['3.D. Agricultural soils'], 5)
                rows.append({'year': year, 1: mm, 2: sm})
                wb.close()
            df = pd.DataFrame(rows).sort_values('year').reset_index(drop=True)
            preloaded[key] = df[['year', 1, 2]]

        elif method == 'crt_n2o_hs_fs':
            # UNFCCC CRT Table4 (LULUCF summary), column E (N2O, kt).
            # "4.E. Settlements" -> HS, "4.A. Forest land" -> FS.FO. Kept in
            # the original file's 9-column layout (year, HS N2O/NOx, FS.FO
            # N2O/NOx, FS.OL N2O/NOx, FS.WL N2O/NOx) so hs_mc.py/fs_mc.py's
            # existing column-index reads (column 1 / column 3) still work
            # unchanged; FS.OL and FS.WL are left blank - fs_mc.py already
            # omits their N2O/N2 emissions deliberately (see fs_mc.py), and
            # the NOx columns were never read by any calculations/*.py file
            # (same CRLTAP-webdab reasoning as elsewhere).
            rows = []
            for year, wb in _crt_iter_workbooks(filepath):
                sheet = wb['Table4']
                hs_n2o = _crt_cell(sheet, ['4.E. Settlements'], 5)
                fo_n2o = _crt_cell(sheet, ['4.A. Forest land'], 5)
                rows.append({0: year, 1: hs_n2o, 2: None, 3: fo_n2o, 4: None,
                             5: None, 6: None, 7: None, 8: None})
                wb.close()
            df = pd.DataFrame(rows).sort_values(0).reset_index(drop=True)
            preloaded[key] = df

        elif method == 'crt_nr_ag':
            # UNFCCC CRT Table3.D ("3.D.2.b. Nitrogen leaching and run-off",
            # column D, t N -> kt N) and Table3.B(b) ("3.B.5. Indirect N2O
            # emissions", column T, kg N -> kt N) - soil-management (SM) and
            # manure-management (MM) leaching/runoff respectively.
            rows = []
            for year, wb in _crt_iter_workbooks(filepath):
                sm = _crt_cell(wb['Table3.D'], ['3.D.2.b.   Nitrogen leaching and run-off'], 4)
                sm = sm / 1000 if sm is not None else None
                mm = _crt_cell(wb['Table3.B(b)'], ['3.B.5. Indirect N2O emissions'], 20)
                mm = mm * 1e-6 if mm is not None else None
                rows.append({'year': year, 'Nr_SM': sm, 'Nr_MM': mm})
                wb.close()
            preloaded[key] = pd.DataFrame(rows).sort_values('year').reset_index(drop=True)

        elif method == 'openpyxl_single_sheet':
            wb = openpyxl.load_workbook(filepath, data_only=True)
            preloaded[key] = pd.DataFrame(list(wb[kwargs['sheet_name']].values))

        elif method == 'openpyxl_single_sheet_df':
            wb = openpyxl.load_workbook(filepath, data_only=True)
            preloaded[key] = pd.DataFrame(list(wb[kwargs['sheet_name']].values))

        elif method == 'excel_feed_raavarer_norsk':
            df = pd.read_excel(filepath, sheet_name='Varegrupper')
            preloaded[key] = pd.DataFrame({
                'year': df.iloc[3:28, 0].astype(int),
                'value_carb': df.iloc[3:28, 1].astype(float),  # column B (index 1) = domestic carbohydrate raw materials
                'value_prot': df.iloc[3:28, 7].astype(float)   # column H (index 7) = domestic protein raw materials
            }).reset_index(drop=True)

        elif method == 'excel_feed_raavarer_import':
            df = pd.read_excel(filepath, sheet_name='Varegrupper')
            preloaded[key] = pd.DataFrame({
                'year': df.iloc[3:28, 0].astype(int),
                'value_carb': df.iloc[3:28, 2].astype(float),  # column C (index 2) = imported carbohydrate raw materials
                'value_prot': df.iloc[3:28, 8].astype(float)   # column I (index 8) = imported protein raw materials
            }).reset_index(drop=True)

        elif method == 'excel_feed_totalkalkyle':
            df = pd.read_excel(filepath, sheet_name='Sum innkjøpt kraftfôr ukorr.')
            preloaded[key] = pd.DataFrame({
                'year': df.iloc[26:41, 0].astype(int),
                'value': df.iloc[26:41, 1].astype(float),
                'dom_frac': df.iloc[26:41, 4].astype(float)
            }).reset_index(drop=True)

        elif method == 'excel_aquaculture':
            df_modern = pd.read_excel(filepath, sheet_name='A.06.002', header=None)
            years_modern = df_modern.iloc[2, 2:].astype(int).tolist()
            df_cells = df_modern.iloc[4:43, 2:].replace('-', 0).astype(float)
            df_cells.columns = years_modern
            preloaded['aqua_modern'] = df_cells

            df_old = pd.read_excel('data_files/akvakultur_1984_1994.xlsx', sheet_name='Ark1', header=None)
            preloaded['aqua_old'] = pd.DataFrame({
                'year': df_old.iloc[1:11, 0].astype(int),
                'value': df_old.iloc[1:11, 1].astype(float)
            }).reset_index(drop=True)

        elif method == 'csv_live_animals':
            df_fao_raw = pd.read_csv(filepath)
            preloaded['fao_live_animals'] = df_fao_raw[(df_fao_raw['Element'] == 'Import quantity') & (df_fao_raw['Value'] != 0)][['Item', 'Year', 'Unit', 'Value']].copy()
            preloaded['fao_live_animals_export'] = df_fao_raw[(df_fao_raw['Element'] == 'Export quantity') & (df_fao_raw['Value'] != 0)][['Item', 'Year', 'Unit', 'Value']].copy()

        elif method == 'csv_fertilizer_import':
            df_fert = pd.read_csv(filepath)
            preloaded[key] = df_fert[(df_fert['Element'] == 'Import quantity') & (df_fert['Value'] != 0)][['Year', 'Value']].copy()

        elif method == 'openpyxl_teotil':
            wb = openpyxl.load_workbook(filepath, data_only=True)
            preloaded['hy_teotil3_to_coast'] = pd.DataFrame(list(wb['totn_to_coast'].values))
            preloaded['hy_teotil3_by_source'] = pd.DataFrame(list(wb['totn_by_source'].values))
            preloaded['hy_teotil3_retention'] = pd.DataFrame(list(wb['totn_retention'].values))

        elif method == 'openpyxl_sewage':
            wb_05280 = openpyxl.load_workbook(filepath, data_only=True)
            preloaded['hy_ssb_05280_raw'] = pd.DataFrame(list(wb_05280['Nitrogen'].values))
            wb_utslipp = openpyxl.load_workbook('data_files/utslipp_avløp.xlsx', data_only=True)
            preloaded['hy_utslipp_avlop_raw'] = pd.DataFrame(list(wb_utslipp['Ark1'].values))

        elif method == 'openpyxl_gnb':
            wb_gnb = openpyxl.load_workbook(filepath, data_only=True)
            preloaded['ag_gnb_workbook'] = wb_gnb
            preloaded['gnb_sheet30_raw'] = pd.DataFrame(list(wb_gnb['Sheet 30'].values))

        elif method == 'excel_grovfor':
            wb_13648 = openpyxl.load_workbook('data_files/13648_20260916-101847.xlsx', data_only=True)
            wb_05772 = openpyxl.load_workbook('data_files/05772_20251210-142618.xlsx', data_only=True)
            wb_old = openpyxl.load_workbook('data_files/grovfor_før_2000.xlsx', data_only=True)
            preloaded['ag_ssb_13648'] = wb_13648
            preloaded['ag_ssb_05772'] = wb_05772
            preloaded['ag_grovfor_old'] = wb_old
            preloaded['ssb_13648_raw'] = pd.DataFrame(list(wb_13648['13648'].values))
            preloaded['ssb_05772_raw'] = pd.DataFrame(list(wb_05772['Gronfor'].values))
            preloaded['grovfor_old_raw'] = pd.DataFrame(list(wb_old['Ark1'].values))

        elif method == 'csv_faostat_production':
            df_fao = pd.read_csv(filepath)
            preloaded['ag_faostat_production'] = df_fao
            preloaded['fao_animal_production_clean'] = df_fao[(df_fao['Element'] == 'Production') & (df_fao['Value'] != 0) & (~df_fao['Item'].str.contains('hides', case=False, na=False))][['Item', 'Year', 'Value']].copy()
            preloaded['fao_hides_clean'] = df_fao[(df_fao['Element'] == 'Production') & (df_fao['Value'] != 0) & (df_fao['Item'].str.contains('hides', case=False, na=False))][['Item', 'Year', 'Value']].copy()

        elif method == 'openpyxl_obb_grazing':
            # Converts every relevant sheet from the organised-grazing workbook to a
            # DataFrame in one pass; fs_mc.py indexes each obb_<sheet>_raw key directly.
            wb_obb = openpyxl.load_workbook(filepath, data_only=True)
            preloaded['fs_obb_workbook'] = wb_obb

            target_sheets = [
                'Sau1990-99', 'Sau2000-09', 'Sau2010-19', 'Sau2020-29',
                'Storfe og geit1993-2019', 'Storfe og geit2020-29'
            ]
            for sheet_name in target_sheets:
                preloaded[f"obb_{sheet_name}_raw"] = pd.DataFrame(list(wb_obb[sheet_name].values))

        elif method == 'csv_forestry':
            df_raw = pd.read_csv(filepath)
            preloaded[key] = df_raw

        elif method == 'csv_ef_fuel':
            df = pd.read_csv(filepath)
            preloaded[key] = df[['year', 'value']].copy()
        elif method == 'excel_ssb_generic':
            sheet_name = kwargs.get('sheet') if 'sheet' in kwargs else kwargs.get('sheet_name')
            df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
            preloaded[key] = df

        elif method == 'excel_mildir_emissions':
            preloaded[key] = pd.read_excel(filepath, header=0)

        elif method == 'excel_industry_categories':
            preloaded[key] = pd.read_excel(filepath)

        elif method == 'excel_population':
            df = pd.read_excel(filepath, skiprows=2, skipfooter=42)
            df = df.set_index('Unnamed: 0')
            preloaded[key] = df

    return preloaded