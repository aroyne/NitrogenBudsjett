#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
MC-VERSJON: Beregner nitrogenflyt for Market & Processing (MP).
Rådata ligger i preloaded_data, mens støyfaktorer for hvert datasett sendes inn via dataset_noise.
"""
import pandas as pd
import numpy as np

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    process_generic_trade_flow,
    load_crltap_emissions_to_N
)
from calculations.shared_flow_calculations import (
    find_aquaculture_production,
    find_feedstock_fuel,
    find_food_industry_waste,
    find_industrial_round_wood,
    find_industrial_waste_fuels,
    find_other_goods_export,
    find_other_industry_waste,
    find_other_industry_wastewater,
    find_op_untreated_wastewater,
    find_recycling,
    find_industrial_crop_products,
    find_non_edible_animal_products
    )

MP_OP_CRLTAP_SECTORS = ['2A', '2B', '2C', '2D', '2G', '2H']


def protein_per_group(current_params, mapping_sheet, group_index):
    """
    MC-VERSJON: Kobler SSB-koder mot perturberte proteinverdier i current_params.
    """
    # 1) Hent mappingtabellen fra parameterobjektet
    mapping = current_params.get_table(mapping_sheet)
    mapping = mapping.set_index('code').reindex(group_index)

    # 2) Slå opp den unike, perturberte verdien per matvaregruppe for denne iterasjonen
    protein_fractions = []
    for idx, row in mapping.iterrows():
        food_group = str(row['food_group']).strip()
        
        # Hvis matvaregruppen finnes, hent ut den unike MC-verdien, ellers 0.0
        if pd.notna(row['food_group']):
            f_id = f"food_protein_{food_group}"
            protein_pct = float(current_params.get(f_id))
        else:
            protein_pct = 0.0
            
        protein_fractions.append(protein_pct / 100.0) # Prosent -> Fraksjon

    return pd.Series(protein_fractions, index=group_index)


def execute_calculations_mp(preloaded_data, current_params, dataset_noise, current_trade_factors=None):
    """
    Hovedfunksjon for MP-poolen (MC). Mottar denne rundens parameter- og støyordbøker.
    Krasjer umiddelbart hvis kritiske inndata mangler.
    """
    results = []
    
    years = list(range(1984, 2026))  # 1984..2025 inclusive
    OP_out = pd.DataFrame({
        'year': years,
        'value': 0.0,               # float zeros; use 0 if you want ints
        'entries': 0    # need to count the right number of entries that year if comment to be 'ok'
    })
    OP_out.set_index('year', inplace=True)

    
    # Kaller den første delberegningen for såkorn og plantemateriale
    _add_seeds_and_planting_material_mc(results, preloaded_data, current_params, dataset_noise)
    _add_farm_animal_feed_mc(results, preloaded_data, current_params, dataset_noise)
    _add_food_industry_waste_mc(results, preloaded_data, current_params, dataset_noise)
    _add_food_industry_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    _add_food_products_mc(results, preloaded_data, current_params, dataset_noise)
    _add_fp_untreated_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    _add_aquaculture_feed_mc(results, preloaded_data, current_params, dataset_noise)
    _add_food_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_feed_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_ag_mineral_fertilizer_mc(results, preloaded_data, current_params, dataset_noise)
    _add_other_industry_waste_mc(results, preloaded_data, current_params, dataset_noise, OP_out)
    _add_industrial_waste_fuels_mc(results, preloaded_data, current_params, dataset_noise)
    _add_other_industry_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    _add_hs_mineral_fertilizer_mc(results, preloaded_data, current_params, dataset_noise)
    _add_fo_mineral_fertilizer_mc(results, preloaded_data, current_params, dataset_noise)
    _add_op_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_op_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_op_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise)
    _add_op_untreated_wastewater_mc(results, preloaded_data, current_params, dataset_noise)
    _add_mineral_fertilizer_export_mc(results, preloaded_data, current_params, dataset_noise)
    _add_other_goods_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    _add_consumer_goods_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise)
    
    return results


def _add_seeds_and_planting_material_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Beregner nitrogenmengde i innkjøpt såkorn og plantemateriale (MP -> AG).
    Data hentes fra NIBIO Totalkalkylen (NibioStatistics-5.xlsx).
    """
    flow_code = 'MP.FP-AG.SM-Seeds and planting material -Nmix'
    collected_years = set()
    data_sources = 'NIBIO Totalkalkylen'
    comment = 'ok (MC-støy lagt på)'
    
    # 1. Hent parametere for protein- og nitrogenfraksjoner fra current_params
    seed_cereal_prot  = float(current_params.get("seed_cereal_protein_frac"))
    seed_cereal_fac   = float(current_params.get("seed_cereal_protein_to_N"))
    seed_oil_prot     = float(current_params.get("seed_oilseed_protein_frac"))
    seed_pea_prot     = float(current_params.get("seed_pea_protein_frac"))
    seed_grass_prot   = float(current_params.get("seed_grass_protein_frac"))
    seed_rootveg_prot = float(current_params.get("seed_rootveg_protein_frac"))
    Jones             = float(current_params.get("Jones_factor"))
    
    # Beregn N-fraksjoner (protein_frac / protein_to_N_factor)
    seed_cereal_N  = seed_cereal_prot / seed_cereal_fac
    seed_oil_N     = seed_oil_prot / Jones
    seed_pea_N     = seed_pea_prot / Jones
    seed_grass_N   = seed_grass_prot / Jones
    seed_rootveg_N = seed_rootveg_prot / Jones
    
    # 2. Hent støyfaktor for Totalkalkylen
    key_dataset = 'Totalkalkylen'
    if not dataset_noise or key_dataset not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_dataset}' mangler i dataset_noise for {flow_code}!")
    noise_totalkalkylen = dataset_noise[key_dataset]['value']
    
    # Ordbok for å akkumulere verdiene per år på tvers av alle fanene
    year_values = {}
    
    # Definer fanene vi skal hente fra preloaded_data og tilhørende N-fraksjon
    sheets_to_process = [
        ('mp_sau_saakorn_raw', seed_cereal_N),       # 'Sum innkjøpt såkorn'
        ('mp_oljefroe_raw', seed_oil_N),             # 'Oljefrø til modning'
        ('mp_erter_raw', seed_pea_N),                # 'Erter'
        ('mp_engfroe_raw', seed_grass_N),            # 'Sum engfrø'
        ('mp_rotvekst_groennsak_raw', seed_rootveg_N) # 'Sum rotvekst- og grønnsakfrø'
    ]
    
    for preload_key, n_fraction in sheets_to_process:
        df_sheet = preloaded_data.get(preload_key)
        if df_sheet is None:
            raise ValueError(f"[KRITISK] '{preload_key}' mangler i preloaded_data for {flow_code}!")
            
        # Vi går gjennom radene dynamisk i stedet for fast range(27,69) for økt robusthet.
        # Men vi sjekker kolonne 0 for gyldige årstall.
        for r in range(len(df_sheet)):
            val_col0 = str(df_sheet.iloc[r, 0]).strip()
            
            # Hopp over overskrifter eller tomme celler i årskolonnen
            if val_col0.lower() in ['year', 'år', 'årstall', 'nan', '', 'none']:
                continue
                
            try:
                year = int(float(val_col0))
                if year in EXPECTED_YEARS:
                    # Hent mengde i tonn (kolonne 1 / B)
                    raw_val = df_sheet.iloc[r, 1]
                    if pd.isna(raw_val) or str(raw_val).strip().lower() in ['none', 'nan', '']:
                        tonn_verdi = 0.0
                    else:
                        tonn_verdi = float(raw_val)
                    
                    # Konverterer: tonn -> kt (* 1e-3), deretter * N-fraksjon
                    value_kt_N = tonn_verdi * 1e-3 * n_fraction
                    year_values[year] = year_values.get(year, 0.0) + value_kt_N
                    
            except (ValueError, TypeError):
                # Hvis vi treffer tekst eller fotnoter i bunnen av arket, hopper vi bare over raden
                continue

    # 3. Pakk ut de akkumulerte verdiene, legg på MC-støy og lagre i results
    for year, total_val in year_values.items():
        collected_years.add(year)
        
        # Legg på denne rundens unike Monte Carlo-støy for Totalkalkylen
        final_val = total_val * noise_totalkalkylen
        
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': max(0.0, final_val),
            'comment': comment,
            'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_farm_animal_feed_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Beregner innenlandsk nitrogenflyt i kraftfôr til husdyr (MP -> AG).
    """
    flow_code = 'MP.FP-AG.MM-Farm animal feed-Nmix'
    collected_years = set()
    
    # 1. Hent parametere
    N_content_carb = float(current_params.get("feed_carb_N_frac"))
    N_content_prot = float(current_params.get("feed_prot_N_frac"))
    
    if not dataset_noise or 'Kraftforstatistikk' not in dataset_noise or 'Totalkalkylen' not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkler mangler i dataset_noise for {flow_code}!")
        
    noise_kraftfor = dataset_noise['Kraftforstatistikk']['value']
    noise_totalkalkylen = dataset_noise['Totalkalkylen']['value']
    noise_trend_interpolation = dataset_noise['trend interpolation']['value']
    
    final_yearly_values = {}
    
    # 2. DEL 1: Landbruksdirektoratets kraftfôrstatistikk (2004->)
    df_raw = preloaded_data.get('feed_raavarer_norsk')
    if df_raw is None:
        raise ValueError(f"[KRITISK] 'feed_raavarer_norsk' mangler i preloaded_data!")
        
    N_cont_accumulator = 0.0
    valid_count = 0
    
    for r in range(len(df_raw)):
        try:
            year_val = df_raw.iloc[r, 0]
            if pd.isna(year_val):
                continue
                
            year = int(float(year_val))
            val_carb = float(df_raw.iloc[r, 1])
            val_prot = float(df_raw.iloc[r, 2])
            
            value_kt_N = (val_carb * N_content_carb + val_prot * N_content_prot) / 1000.0
            value_kt_N_noisy = value_kt_N * noise_kraftfor
            
            if year in EXPECTED_YEARS:
                final_yearly_values[year] = {
                    'value': max(0.0, value_kt_N_noisy),
                    'comment': 'ok',
                    'data_sources': 'Kraftfôrstatistikk'
                }
            
            total_tonn = val_carb + val_prot
            if total_tonn > 0:
                N_cont_accumulator += value_kt_N / total_tonn
                valid_count += 1
            
        except Exception as e:
            raise ValueError(f"[KRITISK] Feil på rad {r} i feed_raavarer: {e}")

    N_cont_before_2000 = (N_cont_accumulator / valid_count) * 1e3

    # 3. DEL 2: Totalkalkylen (1985-1999)
    df_tk = preloaded_data.get('feed_totalkalkyle')
    if df_tk is None:
        raise ValueError(f"[KRITISK] 'feed_totalkalkyle' mangler i preloaded_data!")

    for r in range(len(df_tk)):
        try:
            year_val = df_tk.iloc[r, 0]
            if pd.isna(year_val):
                continue
                
            year = int(float(year_val))
            value_tonn = float(df_tk.iloc[r, 1])
            
            if year < 1995:
                dom_frac = float(df_tk.iloc[r, 2])
            else:
                param_key_dom_frac = "feed_historical_dom_frac"
                dom_frac = float(current_params.get(param_key_dom_frac))
                
            value_kt_N_hist = value_tonn * 1e-3 * N_cont_before_2000 * dom_frac
            value_kt_N_hist_noisy = value_kt_N_hist * noise_totalkalkylen
            
            if year in EXPECTED_YEARS and year not in final_yearly_values:
                final_yearly_values[year] = {
                    'value': max(0.0, value_kt_N_hist_noisy),
                    'comment': 'ok',
                    'data_sources': 'Totalkalkylen'
                }
                
        except Exception as e:
            raise ValueError(f"[KRITISK] Feil på rad {r} i feed_totalkalkyle: {e}")

    # 4. DEL 3: Interpolering (2000-2003)
    val_1999 = final_yearly_values[1999]['value']
    val_2004 = final_yearly_values[2004]['value']
    slope = (val_2004 - val_1999) / 5.0
    
    for gap_year in [2000, 2001, 2002, 2003]:
        if gap_year in EXPECTED_YEARS:
            steps = gap_year - 1999
            interpolated_base = val_1999 + (slope * steps)
            final_interpolated_value = interpolated_base * noise_trend_interpolation
            
            final_yearly_values[gap_year] = {
                'value': max(0.0, final_interpolated_value),
                'comment': 'interpolated',
                'data_sources': 'Interpolert'
            }

    # 5. Pakk ut til resultatlisten
    for year in sorted(final_yearly_values.keys()):
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 'year': year, 'value': final_yearly_values[year]['value'],
            'comment': final_yearly_values[year]['comment'], 'data_sources': final_yearly_values[year]['data_sources']
        })

    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_food_industry_waste_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Henter matindustriavfall fra fellesberegningen og legger det til i resultatene.
    """
    flow_code = 'MP.FP-PR.SO-Food industry waste-Nmix'
    collected_years = set()
    
    df_05282 = preloaded_data.get('ssb_05282')
    df_10514 = preloaded_data.get('ssb_10514')
    
    if df_05282 is None or df_10514 is None:
        raise ValueError(f"[KRITISK] Datatabeller ssb_05282/ssb_10514 mangler i preloaded_data for {flow_code}!")
        
    # Henter de ferdig beregnede og støybelagte verdiene
    calculated_years = find_food_industry_waste(df_05282, df_10514, current_params, dataset_noise)
    
    # Pakk ut til resultatlisten
    for year in sorted(calculated_years.keys()):
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': calculated_years[year]['value'],
                'comment': calculated_years[year]['comment'],
                'data_sources': calculated_years[year]['data_sources']
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_food_industry_wastewater_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i avløpsvann fra matindustrien (MP.FP-PR.WW-Food industry wastewater-Nmix).
    STRIKT: Kjører KUN for perioden 1989-2023. Ingen data legges til etter 2023.
    """
    flow_code = 'MP.FP-PR.WW-Food industry wastewater-Nmix'
    collected_years = set()
    data_sources = 'Miljødirektoratet'
    
    # --- 1. DEFINE TARGET YEARS (Strengt låst til 1989-2023) ---
    target_years = {y for y in EXPECTED_YEARS if 1989 <= y <= 2023}
    
    # --- 2. HENT TABELLER FRA PRELOADED_DATA ---
    df_emissions_raw = preloaded_data.get('mildir_emissions')
    df_categories = preloaded_data.get('industry_categories')
    
    if df_emissions_raw is None or df_categories is None:
        raise ValueError(f"[KRITISK] Data ('mildir_emissions'/'industry_categories') mangler i preloaded_data for {flow_code}!")
        
    # --- 3. HENT OG VERIFISER STØY ---
    key_støy = 'norskeutslipp'
    if not dataset_noise or key_støy not in dataset_noise:
        raise KeyError(f"[KRITISK USIKKERHETSFEIL] Støy-nøkkel '{key_støy}' mangler i dataset_noise for {flow_code}!")
        
    if dataset_noise[key_støy]['type'] != 'perc':
        raise ValueError(f"[KRITISK KONFIGURASJONSFEIL] {flow_code} krever støytype 'perc'!")
        
    noise_factor = float(dataset_noise[key_støy]['value'])

    # --- 4. PROSESSER OG FILTRER DATA I RAM ---
    emissions = df_emissions_raw[df_emissions_raw['Komponent'] == 'nitrogen, totalt']
    categories_keep = df_categories[
        (df_categories['kategori'] == 'FP') & 
        (df_categories['kommunalt nett?'].str.lower() == 'ja')
    ]
    
    emissions_FP = emissions[emissions['AnleggNavn'].isin(categories_keep['Virksomhet'])]
    sum_by_year = emissions_FP.groupby(['År'])['Mengde'].sum().reset_index()
    
    # --- 5. BEREGNINGSLØKKE (KUN TOM. 2023) ---
    for index, row in sum_by_year.iterrows():
        try:
            year = int(row['År'])
            if year in target_years:
                collected_years.add(year)
                base_value = float(row['Mengde']) / 1000.0  # kg -> tonn
                value_noisy = max(0.0, base_value * noise_factor)

                results.append({
                    'flow_name': flow_code,
                    'year': year,
                    'value': value_noisy,
                    'comment': 'ok (MC-støy lagt på)',
                    'data_sources': data_sources
                })
        except (ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil på rad {index} for {flow_code}: {e}")

    # --- 6. SLUTTKONTROLL ---
    missing_years = target_years - collected_years
    report_missing_years(flow_code, missing_years, results)  
    
    
def _add_food_products_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON (Samlet): Beregner nitrogen i matvarer og kjæledyrfôr 
    (MP.FP-HS.HS-Food products-Nmix) og legger det direkte til i resultatene.
    """
    flow_code = 'MP.FP-HS.HS-Food products-Nmix'
    collected_years = set()
    year_values = {}
    
    # 1. Hent fysiske parametere fra current_params
    dog_N_per_year = float(current_params.get('dog_feed_N_per_year'))
    cat_N_per_year = float(current_params.get('cat_feed_N_per_year'))
    dog_slope      = float(current_params.get('dog_number_trend_slope'))
    dog_intercept  = float(current_params.get('dog_number_trend_intercept'))
    cat_slope      = float(current_params.get('cat_number_trend_slope'))
    cat_intercept  = float(current_params.get('cat_number_trend_intercept'))
    Jones          = float(current_params.get('Jones_factor'))
    
    # 2. Hent støyfaktorer fra dataset_noise
    required_noise = ['13695', '10249', '06376', '06913', 'trend interpolation']
    if not dataset_noise or any(k not in dataset_noise for k in required_noise):
        missing = [k for k in required_noise if not dataset_noise or k not in dataset_noise]
        raise KeyError(f"[KRITISK] Mangler støy-nøkler for matvarer: {missing}")
        
    noise_13695 = float(dataset_noise['13695']['value'])
    noise_10249 = float(dataset_noise['10249']['value'])
    noise_06376 = float(dataset_noise['06376']['value'])
    noise_pop = float(dataset_noise['06913']['value'])
    noise_trend = float(dataset_noise['trend interpolation']['value'])

    # 3. Hent datarammer fra preloaded_data
    df_13695 = preloaded_data.get('ssb_13695')
    df_pop = preloaded_data.get('ssb_06913')
    df_10249 = preloaded_data.get('ssb_10249')
    df_06376 = preloaded_data.get('ssb_06376')
    
    if any(df is None for df in [df_13695, df_pop, df_10249, df_06376]):
        raise ValueError(f"[KRITISK] Én eller flere datatabeller mangler i preloaded_data for {flow_code}!")
        
    df_items = current_params.get_table('protein_food_items')
    df_map_new = current_params.get_table('protein_map_new')
    df_map_old = current_params.get_table('protein_map_old')   
    
    if any(df is None for df in [df_items, df_map_new, df_map_old]):
        raise ValueError("[KRITISK] Protein-mappingtabeller mangler i preloaded_data!")

    # Intern hjelpefunksjon for kjæledyrfôr
    def pet_N_year(y):
        n_dogs = dog_slope * y + dog_intercept
        n_cats = cat_slope * y + cat_intercept
        return (n_dogs * dog_N_per_year + n_cats * cat_N_per_year) * 1e-6

    # --- DEL 1: 2018-2023 (Tabell 13695) ---
    for col in range(1, df_13695.shape[1]):
        try:
            year_val = df_13695.iloc[3, col]
            if pd.isna(year_val):
                continue
            year = int(float(year_val))
            
            # g/dag/pers -> kt/år/pers
            v_protein_pers = float(df_13695.iloc[6, col]) * 1e-9 * 365
            pop = float(df_pop.loc[year, 'Befolkning 1. januar']) * noise_pop
            
            v_human_N = (v_protein_pers * pop) / Jones
            total_N = (v_human_N * noise_13695) + pet_N_year(year)
            
            year_values[year] = {
                'value': max(0.0, total_N),
                'comment': 'ok',
                'data_sources': 'SSB'
            }
        except (ValueError, TypeError, KeyError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil i tabell 13695 kolonne {col}: {e}")

    # --- DEL 2: 1999-2012 (Tabell 10249) ---
    try:
        # 1. Start på iloc[4:] for å kaste tekst/årstallsrader ut av matvaremengdene
        mengde_10249 = df_10249.set_index(0).iloc[4:, 0::2].dropna(how='all')
        mengde_10249 = mengde_10249.astype(str).applymap(lambda s: s.replace(',','.') if pd.notna(s) else s)
        mengde_10249 = mengde_10249.apply(pd.to_numeric, errors='coerce')
        
        # 2. Beregn protein og nitrogen per person
        protein_map_10249 = protein_per_group(current_params, 'protein_map_new', mengde_10249.index)
        total_protein_pers_10249 = mengde_10249.mul(protein_map_10249, axis=0).sum(axis=0)
        total_N_pers_10249 = total_protein_pers_10249 / Jones * 1e-6
        
        # 3. Loop over kolonnene og slå opp årstall fra rad-indeks 2
        for col_idx, v_N_pers in total_N_pers_10249.items():
            # Feilsøkingen viste at årstallet står på rad 2 i df_10249
            year_val = df_10249.iloc[2, col_idx]
            
            # Hvis cellen over er tom, sjekk cellen til venstre (siden celler ofte er slått sammen i Excel)
            if pd.isna(year_val) and col_idx > 0:
                year_val = df_10249.iloc[2, col_idx - 1]
                
            if pd.isna(year_val):
                continue
                
            year = int(float(year_val))
            
            # Hent befolkning basert på det reelle årstallet
            pop = float(df_pop.loc[year, 'Befolkning 1. januar']) * noise_pop
            
            v_human_N = v_N_pers * pop
            total_N = (v_human_N * noise_10249) + pet_N_year(year)
            
            year_values[year] = {
                'value': max(0.0, total_N),
                'comment': 'ok',
                'data_sources': 'SSB'
            }
    except Exception as e:
        raise ValueError(f"[KRITISK] Feil under prosessering av tabell 10249: {e}")
        
    # --- DEL 3: 1984-1998 (Tabell 06376) ---
    try:
        # 1. Start på iloc[4:] for å kaste tekst/intervallsrader ut av matvaremengdene
        mengde_06376 = df_06376.set_index(0).iloc[4:, 0::2]
        mengde_06376 = mengde_06376.astype(str).applymap(lambda s: s.replace(',','.') if pd.notna(s) else s)
        mengde_06376 = mengde_06376.apply(pd.to_numeric, errors='coerce')
        
        # 2. Beregn protein og nitrogen per person
        protein_map_06376 = protein_per_group(current_params, 'protein_map_old', mengde_06376.index)
        total_protein_pers_06376 = mengde_06376.mul(protein_map_06376, axis=0).sum(axis=0)
        total_N_pers_06376 = total_protein_pers_06376 / Jones * 1e-6  # kgN -> ktN
        
        # 3. Bygg en ordbok som mapper kolonneindeksen om til det ekte tidsintervallet fra rad 3
        intervall_mapping = {}
        for col_idx in total_N_pers_06376.index:
            # Feilsøkingen viste at intervallene ligger på rad 3
            val_interval = df_06376.iloc[3, col_idx]
            
            # Håndter sammenslåtte celler i Excel (titt til venstre hvis tom)
            if pd.isna(val_interval) and col_idx > 0:
                val_interval = df_06376.iloc[3, col_idx - 1]
                
            if pd.notna(val_interval):
                intervall_mapping[col_idx] = str(val_interval).strip()

        # 4. Loop over årene og slå opp i intervall_mapping ved hjelp av kolonneindeksene
        for year in range(1984, 1999):
            pop = float(df_pop.loc[year, 'Befolkning 1. januar']) * noise_pop
            comment = 'ok'
            
            # Finn hvilken kolonneindeks som hører til hvilket intervall på rad 3
            idx_83_85 = next((k for k, v in intervall_mapping.items() if '1983-1985' in v), None)
            idx_89_91 = next((k for k, v in intervall_mapping.items() if '1989-1991' in v), None)
            idx_96_98 = next((k for k, v in intervall_mapping.items() if '1996-1998' in v), None)
            
            if any(idx is None for idx in [idx_83_85, idx_89_91, idx_96_98]):
                raise KeyError(f"[KRITISK] Fant ikke alle nødvendige tidsintervaller (1983-1985, 1989-1991, 1996-1998) i tabell 06376! Funnet: {list(intervall_mapping.values())}")

            if year < 1986:
                v_human_pers = total_N_pers_06376[idx_83_85]
                src = 'SSB'
            elif year < 1989:
                v_human_pers = (total_N_pers_06376[idx_83_85] + total_N_pers_06376[idx_89_91]) / 2.0
                src = 'interpolated'
            elif year < 1992:
                v_human_pers = total_N_pers_06376[idx_89_91]
                src = 'SSB'
            elif year < 1996:
                v_human_pers = (total_N_pers_06376[idx_89_91] + total_N_pers_06376[idx_96_98]) / 2.0
                src = 'interpolated'
            else:
                v_human_pers = total_N_pers_06376[idx_96_98]
                src = 'SSB'
                
            v_human_N = v_human_pers * pop
            total_N = (v_human_N * noise_06376) + pet_N_year(year)
            
            year_values[year] = {
                'value': max(0.0, total_N),
                'comment': comment,
                'data_sources': src
            }
    except Exception as e:
        raise ValueError(f"[KRITISK] Feil under prosessering av tabell 06376: {e}")    
        
    # --- DEL 4: Interpolering (2010-2011, 2013-2017) ---
    valid_years = [y for y in sorted(year_values.keys()) if y not in [2010, 2011, 2013, 2014, 2015, 2016, 2017]]
    y_arr = np.array(valid_years)
    v_arr = np.array([year_values[k]['value'] for k in y_arr])
    
    m, b = np.polyfit(y_arr, v_arr, 1)
    
    for year in list(range(2010, 2012)) + list(range(2013, 2018)):
        v_trend = m * year + b
        year_values[year] = {
            'value': max(0.0, v_trend * noise_trend),
            'comment': 'interpolated trendline',
            'data_sources': 'interpolated'
        }

    # --- DEL 5: Pakk ut alle årene til den sentrale resultatlisten ---
    for year in sorted(year_values.keys()):
        if year in EXPECTED_YEARS:
            collected_years.add(year)
            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': year_values[year]['value'],
                'comment': year_values[year]['comment'],
                'data_sources': year_values[year]['data_sources']
            })
            
    # Sluttkontroll
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_fp_untreated_wastewater_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i ubehandlet avløpsvann fra matindustrien (MP.FP-HY.SW-Untreated wastewater-Nmix).
    STRIKT: Kjører KUN for perioden 1990-2023. Ingen data legges til etter 2023.
    """
    flow_code = 'MP.FP-HY.SW-Untreated wastewater-Nmix'
    collected_years = set()
    data_sources = 'Miljødirektoratet'
    
    # --- 1. DEFINE TARGET YEARS (Strengt låst til 1990-2023 iht ekstrapoleringsmodell) ---
    target_years = {y for y in EXPECTED_YEARS if 1990 <= y <= 2023}
    
    # --- 2. HENT TABELLER FRA PRELOADED_DATA ---
    df_emissions_raw = preloaded_data.get('mildir_emissions')
    df_categories = preloaded_data.get('industry_categories')
    
    if df_emissions_raw is None or df_categories is None:
        raise ValueError(f"[KRITISK] Data ('mildir_emissions'/'industry_categories') mangler i preloaded_data for {flow_code}!")
        
    # --- 3. HENT OG VERIFISER STØY ---
    key_støy = 'norskeutslipp'
    if not dataset_noise or key_støy not in dataset_noise:
        raise KeyError(f"[KRITISK USIKKERHETSFEIL] Støy-nøkkel '{key_støy}' mangler i dataset_noise for {flow_code}!")
        
    if dataset_noise[key_støy]['type'] != 'perc':
        raise ValueError(f"[KRITISK KONFIGURASJONSFEIL] {flow_code} krever støytype 'perc'!")
        
    noise_factor = float(dataset_noise[key_støy]['value'])

    # --- 4. PROSESSER OG FILTRER DATA I RAM ---
    emissions = df_emissions_raw[df_emissions_raw['Komponent'] == 'nitrogen, totalt']
    categories_keep = df_categories[
        (df_categories['kategori'] == 'FP') & 
        (df_categories['kommunalt nett?'].str.lower().isin(['nei', 'ukjent']))
    ]
    
    emissions_FP = emissions[emissions['AnleggNavn'].isin(categories_keep['Virksomhet'])]
    sum_by_year = emissions_FP.groupby(['År'])['Mengde'].sum().reset_index()
    
    # Midlertidig lagring for reelle år for å kunne regne historisk snitt
    found_values_94_23 = {}
    mean_value_94_98 = 0.0
    
    # --- 5. BEREGNINGSLØKKE FOR REELLE DATA (1994 - 2023) ---
    for index, row in sum_by_year.iterrows():
        try:
            year = int(row['År'])
            if 1994 <= year <= 2023:
                base_value = float(row['Mengde']) / 1000.0  # kg -> tonn
                value_noisy = max(0.0, base_value * noise_factor)
                found_values_94_23[year] = value_noisy
                
                if 1994 <= year <= 1998:
                    mean_value_94_98 += value_noisy
        except (ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil på rad {index} for {flow_code}: {e}")

    # --- 6. GENERER DE EKSTRAPOLERTE ÅRENE (1990 - 1993) ---
    calculated_mean = (mean_value_94_98 / 5.0) if mean_value_94_98 > 0 else 0.0
    
    # --- 7. BYGG ENDELIGE RESULTATER FOR TARGET_YEARS (KUN TOM. 2023) ---
    for year in sorted(list(target_years)):
        if year < 1994:
            val = calculated_mean
            comment = 'ok (ekstrapolert fra 1994-1998 med MC-støy)'
            src = 'Ekstrapolert / Historisk snitt'
        elif year in found_values_94_23:
            val = found_values_94_23[year]
            comment = 'ok (MC-støy lagt på)'
            src = data_sources
        else:
            # Hopp over hvis et reelt år tilfeldigvis mangler helt i kilden før 2023
            continue
            
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': val,
            'comment': comment,
            'data_sources': src
        })

    # --- 8. SLUTTKONTROLL ---
    missing_years = target_years - collected_years
    report_missing_years(flow_code, missing_years, results)    

    
def _add_aquaculture_feed_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Innenlandsk produsert akvakulturfôr (Market Place til Havbruk).
    Beregnet via felles produksjonsmatrise med påført MC-støy.
    """
    flow_code = 'MP.FP-HY.AC-Feed to coastal aquaculture-Nmix'
    collected_years = set()
    
    # --- 1. SJEKK AT DATA ER TILGJENGELIG ---
    df_modern = preloaded_data.get('aqua_modern')
    df_old = preloaded_data.get('aqua_old')
    if df_modern is None or df_old is None:
        raise ValueError(f"[KRITISK] Havbruksdata ('aqua_modern'/'aqua_old') mangler i preloaded_data for {flow_code}!")

    # --- 2. HENT FELLES PRODUKSJONSMATRISE ---
    # Denne funksjonen påfører allerede Fiskeridirektoratets støyfaktor internt
    aquaculture_production = find_aquaculture_production(df_modern, df_old, current_params, dataset_noise)

    # --- 3. HENT GENERISKE PARAMETERE (STØYFARGET FRA MC-LOOPEN) ---
    import_fraction = float(current_params.get("aquafeed_import_fraction"))
    prot_ret = float(current_params.get("aquafeed_N_retention"))
    feed_waste = float(current_params.get("aquafeed_waste_fraction"))

    # --- 4. BEREGNINGSLØKKE ---
    for year, fish_harvested_N in aquaculture_production.items():
        if year not in EXPECTED_YEARS: 
            continue
        collected_years.add(year)
        
        # Sikkerhetsventil mot urealistiske parametere som vil gi ZeroDivision eller negative tall
        if prot_ret <= 0 or feed_waste >= 1:
            raise ValueError(f"[KRITISK PARAMETERFEIL] Ugyldige havbruksparametere for år {year} (retensjon: {prot_ret}, svinn: {feed_waste})!")
            
        # Beregn nitrogen i oppspist fôr og totalmengde fôr
        eaten_feed_N = fish_harvested_N / prot_ret
        total_feed_N = eaten_feed_N / (1 - feed_waste)
        
        # Isoler den innenlandske brøkdelen: (1 - import_fraction)
        domestic_feed_N = total_feed_N * (1.0 - import_fraction)
        domestic_feed_N = max(0.0, domestic_feed_N) # Sikrer mot negative tall
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(domestic_feed_N),
            'comment': 'ok (MC-støy beregnet via felles produksjonsmatrise)',
            'data_sources': 'Fiskeridirektoratet'
        })
        
    # Sjekk for manglende år mot det globale EXPECTED_YEARS-settet
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_food_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    """
    MC-VERSJON: Eksport av matvarer (Market Place til Rest of World).
    Gjenbruker den generiske kjernefunksjonen for handelsdata med fullstendig MC-støy.
    """
    flow_code = 'MP.FP-RW.RW-Food export-Nmix'
    types_to_keep = ['korn/planter', 'kjøtt/fisk/meieri/egg', 'mat']
    
    # Vi sender med results direkte, slik at kjernefunksjonen gjør 
    # både filtrering, støy-påføring, aggregering og append-logikk automatisk.
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code=flow_code,
        target_types=types_to_keep,
        is_import=False,  # <--- False betyr Eksport (impeks = 2)
        dataset_noise=dataset_noise,
        data_sources='SSB tab 08801'
    )
    
    
def _add_feed_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    """
    MC-VERSJON: Eksport av fôrvarer (Market Place til Rest of World).
    Gjenbruker den generiske kjernefunksjonen for handelsdata med fullstendig MC-støy.
    """
    flow_code = 'MP.FP-RW.RW-Feed export-Nmix'
    types_to_keep = ['for', 'fiskefor', 'kjæledyrfor']
    
    # Kjernefunksjonen håndterer all støy på mengde (SSB 08801) og produkt-N-faktorer
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code=flow_code,
        target_types=types_to_keep,
        is_import=False,  # Eksport (impeks = 2)
        dataset_noise=dataset_noise,
        data_sources='SSB tab 08801'
    )
    
def _add_ag_mineral_fertilizer_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Innenlandsk mineralgjødsel (Market Place til Agriculture Soil Management).
    STRIKT: Henter forbruk fra faostat_fertilizer (11-21) og isolerer import fra fao_mineral_fertilizer (11-12-2).
    Krasjer hardt ved datahull, negative verdier eller manglende støyfaktorer.
    """
    flow_code = 'MP.OP-AG.SM-Mineral fertilizer-Nmix'
    collected_years = set()
    comment = 'ok'
    data_sources = 'FAOSTAT Fertilizer by nutrient (Agricultural Use - Import)'
    
    # --- 1. VERIFISER AT DATASETTENE EKSISTERER I MINNE ---
    data_use = preloaded_data.get('faostat_fertilizer_use')       # Kun forbruksdata (11-21)
    data_trade = preloaded_data.get('fao_mineral_fertilizer') # Import/Eksport-samlefil (11-12-2)
    
    if data_use is None or data_trade is None:
        raise ValueError(f"[KRITISK] Gjødseldata ('faostat_fertilizer_use'/'fao_mineral_fertilizer') mangler fullstendig i preloaded_data!")

    # --- 2. HENT STØYFAKTOR (KRASJER HVIS DEN MANGLER) ---
    if 'Fertilizer by nutrient' not in dataset_noise:
        raise KeyError(f"[KRITISK USIKKERHETSFEIL] Fant ikke støyfaktoren 'Fertilizer by nutrient' i dataset_noise for {flow_code}!")
    
    noise_factor = float(dataset_noise['Fertilizer by nutrient']['value'])

    # --- 3. DEFINER GYLDIG TIDSROM BASERT PÅ KILDEDATA (Stopper i 2023) ---
    available_use_years = set(data_use['Year'].unique())
    available_trade_years = set(data_trade['Year'].unique())
    target_years = EXPECTED_YEARS & available_use_years & available_trade_years

    if not target_years:
        raise ValueError(f"[KRITISK DATAMANGLER] Ingen overlappende år funnet mellom EXPECTED_YEARS og gjødseldataene!")

    # --- 4. BEREGNINGSLØKKE ---
    for year in target_years:
        # Hent forbruk for året (11-21 har kun Agricultural Use, så vi trenger ikke filter her)
        n_amount_use = data_use[data_use['Year'] == year]
        
        # Isoler 'Import quantity' fra handelsfilen (11-12-2) for dette året
        df_year_trade = data_trade[data_trade['Year'] == year]
        clean_element = df_year_trade['Element'].astype(str).str.replace('"', '').str.lower().str.strip()
        n_amount_imp = df_year_trade[clean_element == 'import quantity']
        
        if n_amount_use.empty:
            raise ValueError(f"[KRITISK DATAHULL] Fant ikke forbruksdata for det påkrevde året {year}!")
        if n_amount_imp.empty:
            raise ValueError(f"[KRITISK DATAHULL] Fant ikke importdata for det påkrevde året {year}!")
            
        # Summerer verdiene for året (Dette samler opp alle under-rader og er 100 % trygt)
        raw_use_tonnes = float(n_amount_use['Value'].sum())
        raw_imp_tonnes = float(n_amount_imp['Value'].sum())
        
        # Påfør synkron MC-støy
        raw_use_perturbed = raw_use_tonnes * noise_factor
        raw_imp_perturbed = raw_imp_tonnes * noise_factor
        
        # Beregn differansen (Netto innenlandsk rest i tonn N) og del på 1000 for å få kt N
        value = (raw_use_perturbed - raw_imp_perturbed) / 1000.0
        
        # Strikt fysisk sjekk mot negative tall
        if value < 0:
            raise ValueError(f"[KRITISK MASSEBALANSEFEIL] År {year}: Generert import ({raw_imp_perturbed:.2f} t) overstiger forbruk ({raw_use_perturbed:.2f} t). Negativ strøm ({value:.4f} kt N) nektes!")
        
        collected_years.add(year)
        results.append({
             'flow_name': flow_code,
             'year': year,
             'value': float(value),
             'comment': comment,
             'data_sources': data_sources
         })
         
    # --- 5. ENDELIG KONTROLL ---
    missing_targets = target_years - collected_years
    if missing_targets:
        raise ValueError(f"[KRITISK DATAAVVIK] Følgende år ble ikke fullført i beregningen: {missing_targets}")
        
        
def _add_industrial_waste_fuels_mc(results, preloaded_data, current_params, dataset_noise):
    flow_code = 'MP.OP-EF.IC-Industrial waste fuels-Nmix'
    collected_years = set()
    
    comment = 'ok'
    data_sources = 'SSB'
    
    # Hent DataFrames fra den sentrale lasteren
    df_bio_08205 = preloaded_data['ssb_bio_08205']
    df_bio_hist = preloaded_data['ssb_bio_hist']
    
    # Kjør den MC-optimaliserte beregningen (returnerer nå kun year_values)
    year_values = find_industrial_waste_fuels(
        df_bio_08205, df_bio_hist, current_params, dataset_noise
    )
    
    for year, value in year_values.items():
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
            # 'uncertainty' er fjernet herfra
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_other_industry_waste_mc(results, preloaded_data, current_params, dataset_noise, OP_out):
    """
    MC-VERSJON: Beregner nitrogenflyt for øvrig industriavfall (MP -> OP).
    Krasjer umiddelbart hvis data eller støy mangler.
    """
    flow_code = 'MP.OP-PR.SO-Other industry waste-Nmix'
    collected_years = set()
    data_sources = 'SSB'
    
    # 1. Hent tabeller fra preloaded_data
    df_05282 = preloaded_data.get('ssb_05282')
    df_10514 = preloaded_data.get('ssb_10514')
    df_hist_waste = preloaded_data.get('ssb_hist_industry_waste') # Antatt navn i RAM
    
    if df_05282 is None or df_10514 is None or df_hist_waste is None:
        raise ValueError(f"[KRITISK] Datatabeller mangler i preloaded_data for {flow_code}!")
        
    # 2. Kjør kjerneberegningen
    industry_waste, industry_waste_unc = find_other_industry_waste(df_05282, df_10514, df_hist_waste, current_params, dataset_noise)    
    
    # 3. Pakk ut til resultater og akkumuler i OP_out matrix
    for year, value in industry_waste.items():
        if year in EXPECTED_YEARS:
            collected_years.add(year)   
            
            comment = 'extrapolated' if year < 1995 else 'ok'
            
            # Sikre at året faktisk eksisterer i den eksterne OP_out matrisen før vi adderer
            if year not in OP_out.index:
                raise KeyError(f"[KRITISK] År {year} mangler i OP_out-indeksen for {flow_code}!")
                
            OP_out.loc[year, 'value'] += value
            OP_out.loc[year, 'entries'] += 1
            
            # Finn usikkerhets-metadata hvis tilgjengelig, ellers 0.0
            støy_nøkkel = '05282' if year < 2012 else '10514'
            low_bound = dataset_noise.get(støy_nøkkel, {}).get('low_bound', 0.0)
            
            results.append({
                'flow_name': flow_code,
                'year': int(year),
                'value': max(0.0, value),
                'comment': comment,
                'data_sources': data_sources,
                'uncertainty': low_bound        
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_other_industry_wastewater_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i avløpsvann fra annen industri (MP.OP-PR.WW-Other industry wastewater-Nmix).
    STRIKT: Kjører KUN for perioden 1989-2023. Ingen data legges til etter 2023.
    """
    flow_code = 'MP.OP-PR.WW-Other industry wastewater-Nmix'
    collected_years = set()
    data_sources = 'Miljødirektoratet'
    
    # --- 1. DEFINE TARGET YEARS (Strengt låst til 1989-2023) ---
    target_years = {y for y in EXPECTED_YEARS if 1989 <= y <= 2023}
    
    # --- 2. HENT TABELLER FRA PRELOADED_DATA ---
    df_emissions_raw = preloaded_data.get('mildir_emissions')
    df_categories = preloaded_data.get('industry_categories')
    
    if df_emissions_raw is None or df_categories is None:
        raise ValueError(f"[KRITISK] Data ('mildir_emissions'/'industry_categories') mangler i preloaded_data for {flow_code}!")
        
    # --- 3. HENT OG VERIFISER STØY ---
    key_støy = 'norskeutslipp'
    if not dataset_noise or key_støy not in dataset_noise:
        raise KeyError(f"[KRITISK USIKKERHETSFEIL] Støy-nøkkel '{key_støy}' mangler i dataset_noise for {flow_code}!")
        
    if dataset_noise[key_støy]['type'] != 'perc':
        raise ValueError(f"[KRISK KONFIGURASJONSFEIL] {flow_code} krever støytype 'perc'!")
        
    noise_factor = float(dataset_noise[key_støy]['value'])

    # --- 4. PROSESSER OG FILTRER DATA I RAM ---
    emissions = df_emissions_raw[df_emissions_raw['Komponent'] == 'nitrogen, totalt']
    categories_keep = df_categories[
        (df_categories['kategori'] == 'OP') & 
        (df_categories['kommunalt nett?'].str.lower() == 'ja')
    ]
    
    emissions_filtered = emissions[emissions['AnleggNavn'].isin(categories_keep['Virksomhet'])]
    sum_by_year = emissions_filtered.groupby(['År'])['Mengde'].sum().reset_index()
    
    # --- 5. BEREGNINGSLØKKE (KUN TOM. 2023) ---
    for index, row in sum_by_year.iterrows():
        try:
            year = int(row['År'])
            if year in target_years:
                collected_years.add(year)
                base_value = float(row['Mengde']) / 1000.0  # kg -> tonn
                value_noisy = max(0.0, base_value * noise_factor)

                results.append({
                    'flow_name': flow_code,
                    'year': year,
                    'value': value_noisy,
                    'comment': 'ok (MC-støy lagt på)',
                    'data_sources': data_sources
                })
        except (ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil på rad {index} for {flow_code}: {e}")

    # --- 6. SLUTTKONTROLL ---
    missing_years = target_years - collected_years
    report_missing_years(flow_code, missing_years, results)
    
def _add_hs_mineral_fertilizer_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i mineralgjødsel brukt utenfor landbruket (MP.OP-HS.HS-Mineral fertilizer-Nmix).
    Bruker ferdiginnlastet FAOSTAT-data fra preloaded_data.
    Krasjer hardt ved manglende støy eller parametere.
    """
    flow_code = 'MP.OP-HS.HS-Mineral fertilizer-Nmix'
    collected_years = set()
    data_sources = 'FAOSTAT Fertilizer by nutrient'
    comment = 'ok (MC-støy lagt på)'
    
    # --- 1. HENT PARAMETERE FRA CURRENT_PARAMS ---
    # Henter den unike, perturberte andelen for denne MC-kjøringen
    nonag_share = float(current_params.get("fert_nonag_share_of_total_use"))
    ag_share = 1.0 - nonag_share
    
    if ag_share <= 0:
        raise ValueError(f"[KRITISK] Ugyldig ag_share ({ag_share}) beregnet for {flow_code}!")
        
    nonag_over_ag = nonag_share / ag_share
    
    # --- 2. HENT OG VERIFISER DATASETT-STØY ---
    key_støy = 'Fertilizer by nutrient'
    if not dataset_noise or key_støy not in dataset_noise:
        raise KeyError(f"[KRITISK USIKKERHETSFEIL] Støy-nøkkel '{key_støy}' mangler i dataset_noise for {flow_code}!")
        
    støy_type = dataset_noise[key_støy]['type']
    if støy_type != 'perc':
        raise ValueError(f"[KRITISK KONFIGURASJONSFEIL] {flow_code} krever støytype 'perc', men fant '{støy_type}'!")
        
    noise_factor = float(dataset_noise[key_støy]['value'])
    
    # --- 3. HENT FERDIG INNLASTET FAOSTAT-DATA ---
    df_faostat = preloaded_data.get('faostat_fertilizer_use')
    if df_faostat is None:
        raise ValueError(f"[KRITISK] 'faostat_fertilizer_use' mangler i preloaded_data for {flow_code}!")
        
    # --- 4. BEREGNINGSLØKKE FOR FORVENTEDE ÅR ---
    for year in EXPECTED_YEARS:
        # Antar df_faostat har kolonnene 'Year' og 'Value' ferdig vasket i rammen
        n_amount_use = df_faostat[df_faostat['Year'] == year]
        
        if n_amount_use.empty:
            continue
            
        collected_years.add(year)
        
        try:
            # Hent råverdi fra FAOSTAT
            raw_value = float(n_amount_use['Value'].values[0])
            
            # Basisverdi (konverteres / 1000 og ganges med forholdstallet)
            base_value = (raw_value / 1000.0) * nonag_over_ag
            
            # Påfør synkron støy fra FAOSTAT-datasettet
            value_noisy = base_value * noise_factor
            
            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': max(0.0, value_noisy),
                'comment': comment,
                'data_sources': data_sources
            })
        except (ValueError, TypeError, IndexError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Kunne ikke prosessere FAOSTAT-verdi for år {year}: {e}")
            
    # --- 5. SLUTTKONTROLL ---
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_fo_mineral_fertilizer_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i mineralgjødsel til skogbruk (MP.OP-FS.FO-Mineral fertilizer-Nmix).
    Posisjonsbasert (iloc) tolking av ubehandlede DataFrames fra preloaderen.
    """
    flow_code = 'MP.OP-FS.FO-Mineral fertilizer-Nmix'
    collected_years = set()
    final_yearly_values = {}
    
    # --- 1. HENT PARAMETERE FRA CURRENT_PARAMS ---
    forest_fert_N_per_da = float(current_params.get("forest_fert_N_per_da"))
    
    # --- 2. HENT OG VERIFISER STØYFAKTORER ---
    required_noise = ['05543', 'trend interpolation']
    if not dataset_noise or any(k not in dataset_noise for k in required_noise):
        missing = [k for k in required_noise if not dataset_noise or k not in dataset_noise]
        raise KeyError(f"[KRITISK] Mangler støy-nøkler for skoggjødsling: {missing}")
        
    noise_ssb = float(dataset_noise['05543']['value'])
    noise_trend = float(dataset_noise['trend interpolation']['value'])
    noise_hist = float(dataset_noise.get('skoggjødsling_historisk', dataset_noise['05543'])['value'])

    # --- 3. HENT DATAFRAMES FRA PRELOADED_DATA ---
    df_ssb_new = preloaded_data.get('ssb_05543_raw')
    df_hist = preloaded_data.get('skoggjoedsling_foer_1995_raw')
    
    if df_ssb_new is None or df_hist is None:
        raise ValueError(f"[KRITISK] Datatabeller ('ssb_05543_raw' / 'skoggjoedsling_foer_1995_raw') mangler i preloaded_data!")

    # --- 4. PROSESSER NYERE DATA (SSB Tabell 05543) ---
    # Starter fra rad 3 basert på diagnostikkutskriften din
    for idx in range(3, len(df_ssb_new)):
        try:
            row = df_ssb_new.iloc[idx]
            year_val = row.iloc[1]   # Kolonne indeks 1
            area_val = row.iloc[2]   # Kolonne indeks 2
            
            if pd.isna(year_val) or pd.isna(area_val):
                continue
                
            year = int(float(year_val))
            if year in EXPECTED_YEARS:
                area_da = float(area_val)
                # Formel: da * kg/da -> kgN. Konverter til ktN (/ 1e6)
                value_kt_N = (area_da * forest_fert_N_per_da) / 1e6
                
                final_yearly_values[year] = {
                    'value': max(0.0, value_kt_N * noise_ssb),
                    'comment': 'ok (MC-støy lagt på)',
                    'data_sources': 'SSB tabell 05543'
                }
        except (ValueError, TypeError, IndexError):
            continue

    # --- 5. PROSESSER HISTORISKE DATA (Før 1995) ---
    # Starter fra rad 1 ettersom rad 0 er tekst-header ("år", "gjødslet areal...")
    for idx in range(1, len(df_hist)):
        try:
            row = df_hist.iloc[idx]
            year_val = row.iloc[0]   # Kolonne indeks 0
            area_val = row.iloc[1]   # Kolonne indeks 1
            
            if pd.isna(year_val) or pd.isna(area_val):
                continue
                
            year = int(float(year_val))
            if year in EXPECTED_YEARS and year not in final_yearly_values:
                area_unit = float(area_val)
                # Gammel formel: area * forest_fert_N_per_da / 100
                value_kt_N_hist = (area_unit * forest_fert_N_per_da) / 1e2
                
                final_yearly_values[year] = {
                    'value': max(0.0, value_kt_N_hist * noise_hist),
                    'comment': 'ok (historisk data, MC-støy lagt på)',
                    'data_sources': 'Skoggjødsling før 1995'
                }
        except (ValueError, TypeError, IndexError):
            continue

    # --- 6. LINEÆR INTERPOLERING FOR HULL (f.eks. 1995 og 1996) ---
    all_found = sorted(final_yearly_values.keys())
    if all_found:
        min_year, max_year = min(all_found), max(all_found)
        for gap_year in range(min_year, max_year + 1):
            if gap_year in EXPECTED_YEARS and gap_year not in final_yearly_values:
                past_years = [y for y in all_found if y < gap_year]
                future_years = [y for y in all_found if y > gap_year]
                
                if past_years and future_years:
                    y0, y1 = max(past_years), min(future_years)
                    v0, v1 = final_yearly_values[y0]['value'], final_yearly_values[y1]['value']
                    
                    v_interp = v0 + (v1 - v0) * (gap_year - y0) / (y1 - y0)
                    
                    final_yearly_values[gap_year] = {
                        'value': max(0.0, v_interp * noise_trend),
                        'comment': f'interpolert trend mellom {y0} og {y1}',
                        'data_sources': 'Interpolert'
                    }

    # --- 7. OVERFØR TIL RESULTATER ---
    for year in sorted(final_yearly_values.keys()):
        collected_years.add(year)
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': final_yearly_values[year]['value'],
            'comment': final_yearly_values[year]['comment'],
            'data_sources': final_yearly_values[year]['data_sources']
        })

    # --- 8. SLUTTKONTROLL ---
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_op_NH3_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: NH3-utslipp til atmosfære fra produksjon/industri (MP.OP-AT.AT-Emissions-NH3).
    Gjenbruker load_crltap_emissions_to_N med industrispesifikke CRLTAP-sektorer.
    """
    flow_code = 'MP.OP-AT.AT-Emissions-NH3'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    # 1. Hent og valider globale parametere
    conv = float(current_params.get("NH3_to_N_factor"))
    
    # 2. Hent rådata fra RAM – krasj hardt hvis de mangler
    # Merk: Vi bruker samme rådatafil ('ag_crltap_raw_lines' / webdabData1863365.txt)
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    if raw_lines is None:
        raise ValueError(f"[KRITISK] 'ag_crltap_raw_lines' mangler i preloaded_data for {flow_code}!")

    # 3. Kall felles hjelpefunksjon med industrisektorene
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=MP_OP_CRLTAP_SECTORS,
        pollutant='NH3',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    # 4. Bygg resultatstrukturen
    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })

    # 5. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_op_NOx_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: NOx-utslipp til atmosfære fra produksjon/industri (MP.OP-AT.AT-Emissions-NOx).
    Gjenbruker load_crltap_emissions_to_N med industrispesifikke CRLTAP-sektorer.
    """
    flow_code = 'MP.OP-AT.AT-Emissions-NOx'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'CRLTAP Inventory Submissions'

    # 1. Hent og valider globale parametere
    conv = float(current_params.get("NOx_to_N_factor"))
    
    # 2. Hent rådata fra RAM
    raw_lines = preloaded_data.get('ag_crltap_raw_lines')
    if raw_lines is None:
        raise ValueError(f"[KRITISK] 'ag_crltap_raw_lines' mangler i preloaded_data for {flow_code}!")

    # 3. Kall felles hjelpefunksjon med industrisektorene
    sums = load_crltap_emissions_to_N(
        raw_lines=raw_lines,
        categories=MP_OP_CRLTAP_SECTORS,
        pollutant='NOx',
        conv_to_N=conv,
        dataset_noise=dataset_noise,
        noise_key='CRLTAP'
    )

    # 4. Bygg resultatstrukturen
    for year, value in sums.items():
        if year not in EXPECTED_YEARS:
            continue
        collected_years.add(year)
        results.append({
            'flow_name': flow_code, 
            'year': year, 
            'value': float(value),
            'comment': comment, 
            'data_sources': data_sources
        })

    # 5. Verifisering av årstall
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_op_N2O_emissions_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: N2O-utslipp til atmosfære fra produksjon/industri (MP.OP-AT.AT-Emissions-N2O).
    Henter ferdiginnlastet CSV-data fra RAM og påfører sentralt trukket datasettstøy.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'MP.OP-AT.AT-Emissions-N2O'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'UNFCCC CRT'

    # 1. Hent og valider globale parametere
    conv_N2O = float(current_params.get("N2O_to_N_factor"))
    
    # 2. Slå opp ferdig generert støy – krasj hvis nøkkelen mangler
    key_n2o = 'UNFCCC_emissions'
    if not dataset_noise or key_n2o not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_n2o}' mangler i dataset_noise for {flow_code}!")
    
    noise_val = dataset_noise[key_n2o]['value']
    noise_type = dataset_noise[key_n2o]['type']

    # 3. Hent ferdiglastet DataFrame fra RAM
    df_op_emissions = preloaded_data.get('n2o_nox_op_raw')
    if df_op_emissions is None:
        raise ValueError(f"[KRITISK] 'n2o_nox_op_raw' mangler i preloaded_data for {flow_code}!")

    # 4. Gå gjennom radene i den ferdiginnlastede CSV-filen
    for index, row in df_op_emissions.iterrows():
        try:
            year_val = row['year']
            n2o_val = row['N2O']
            
            if pd.isna(year_val) or pd.isna(n2o_val):
                continue
                
            year = int(year_val)
            if year not in EXPECTED_YEARS:
                continue
                
            collected_years.add(year)
            
            # Basisverdi konvertert til reell N-vekt
            base_value = float(n2o_val) * conv_N2O

            # Påfør støyen matematisk korrekt basert på støytype (Prosent eller Grenseverdi)
            if noise_type == 'perc':
                value = base_value * noise_val
            else:
                bound = dataset_noise[key_n2o]['upp_bound'] if noise_val >= 0 else dataset_noise[key_n2o]['low_bound']
                value = base_value + (noise_val * bound)

            # Sikre at fysiske utslipp aldri blir negative tall på grunn av støytrekk
            if value < 0: 
                value = 0.0

            results.append({
                'flow_name': flow_code, 
                'year': year, 
                'value': float(value),
                'comment': comment, 
                'data_sources': data_sources
            })
            
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Kunne ikke prosessere rad {index} i n2o_nox_op_raw: {e}")

    # 5. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_op_untreated_wastewater_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i ubehandlet avløpsvann fra industri (MP.OP-HY.SW-Untreated wastewater-Nmix).
    STRIKT: Kjører KUN for perioden 1989-2023. Ingen data legges til etter 2023.
    """
    flow_code = 'MP.OP-HY.SW-Untreated wastewater-Nmix'
    collected_years = set()
    data_sources = 'Miljødirektoratet'
    
    # --- 1. DEFINE TARGET YEARS (Strengt låst til 1989-2023) ---
    target_years = {y for y in EXPECTED_YEARS if 1989 <= y <= 2023}
    
    # --- 2. HENT TABELLER FRA PRELOADED_DATA ---
    df_emissions_raw = preloaded_data.get('mildir_emissions')
    df_categories = preloaded_data.get('industry_categories')
    
    if df_emissions_raw is None or df_categories is None:
        raise ValueError(f"[KRITISK] Data ('mildir_emissions'/'industry_categories') mangler i preloaded_data for {flow_code}!")
        
    # --- 3. HENT OG VERIFISER STØY ---
    key_støy = 'norskeutslipp'
    if not dataset_noise or key_støy not in dataset_noise:
        raise KeyError(f"[KRITISK USIKKERHETSFEIL] Støy-nøkkel '{key_støy}' mangler i dataset_noise for {flow_code}!")
        
    if dataset_noise[key_støy]['type'] != 'perc':
        raise ValueError(f"[KRITISK KONFIGURASJONSFEIL] {flow_code} krever støytype 'perc'!")
        
    noise_factor = float(dataset_noise[key_støy]['value'])

    # --- 4. PROSESSER OG FILTRER DATA I RAM ---
    emissions = df_emissions_raw[df_emissions_raw['Komponent'] == 'nitrogen, totalt']
    categories_keep = df_categories[
        (df_categories['kategori'] == 'OP') & 
        (df_categories['kommunalt nett?'].str.lower().isin(['nei', 'ukjent']))
    ]
    
    emissions_filtered = emissions[emissions['AnleggNavn'].isin(categories_keep['Virksomhet'])]
    sum_by_year = emissions_filtered.groupby(['År'])['Mengde'].sum().reset_index()
    
    # --- 5. BEREGNINGSLØKKE (KUN TOM. 2023) ---
    for index, row in sum_by_year.iterrows():
        try:
            year = int(row['År'])
            if year in target_years:
                collected_years.add(year)
                base_value = float(row['Mengde']) / 1000.0  # kg -> tonn
                value_noisy = max(0.0, base_value * noise_factor)

                results.append({
                    'flow_name': flow_code,
                    'year': year,
                    'value': value_noisy,
                    'comment': 'ok (MC-støy lagt på)',
                    'data_sources': data_sources
                })
        except (ValueError, TypeError) as e:
            raise ValueError(f"[KRITISK DATAFEIL] Feil på rad {index} for {flow_code}: {e}")

    # --- 6. SLUTTKONTROLL (Sjekker kun opp mot target_years) ---
    missing_years = target_years - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_mineral_fertilizer_export_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Mineral fertilizer export (MP.OP-RW.RW-Mineral fertilizer export-Nmix).
    Henter data fra RAM via eksisterende nøkkel 'fao_mineral_fertilizer' og påfører sentralt trukket datasettstøy.
    Krasjer umiddelbart hvis data eller støy-konfigurasjon mangler.
    """
    flow_code = 'MP.OP-RW.RW-Mineral fertilizer export-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på)'
    data_sources = 'FAOSTAT Fertilizer by Nutrient'

    # 1. Slå opp ferdig generert støy – krasj hvis nøkkelen mangler
    key_gjødsel = 'Fertilizer by nutrient'
    if not dataset_noise or key_gjødsel not in dataset_noise:
        raise KeyError(f"[KRITISK] Støy-nøkkel '{key_gjødsel}' mangler i dataset_noise for {flow_code}!")
    
    noise_val = dataset_noise[key_gjødsel]['value']
    noise_type = dataset_noise[key_gjødsel]['type']

    # 2. Hent ferdiglastet DataFrame fra RAM med din eksisterende nøkkel
    df_faostat = preloaded_data.get('fao_mineral_fertilizer')
    if df_faostat is None:
        raise ValueError(f"[KRITISK] 'fao_mineral_fertilizer' mangler i preloaded_data for {flow_code}!")

    # 3. Prosesser og filtrer data i RAM (Export quantity og verdi ulik 0)
    filtered_df = df_faostat[
        (df_faostat['Element'] == 'Export quantity') & 
        (df_faostat['Value'] != 0) & 
        (df_faostat['Value'].notna())
    ]
    
    # Lag en kjapp oppslags-ordbok for reelle årstall -> verdi
    fao_dict = {}
    for _, row in filtered_df.iterrows():
        try:
            fao_dict[int(row['Year'])] = float(row['Value'])
        except (ValueError, TypeError):
            continue

    # 4. Bygg tidsserien basert på EXPECTED_YEARS
    for year in sorted(list(EXPECTED_YEARS)):
        if year in fao_dict:
            collected_years.add(year)
            
            # Verdi / 1000 for enhetskonvertering
            base_value = fao_dict[year] / 1000.0

            # Påfør støyen matematisk korrekt basert på støytype
            if noise_type == 'perc':
                value = base_value * noise_val
            else:
                bound = dataset_noise[key_gjødsel]['upp_bound'] if noise_val >= 0 else dataset_noise[key_gjødsel]['low_bound']
                value = base_value + (noise_val * bound)

            # Sikre mot urealistiske negative eksportverdier etter støy
            if value < 0:
                value = 0.0

            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value),
                'comment': comment,
                'data_sources': data_sources
            })

    # 5. Sjekk om alle forventede år ble samlet inn
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    
    
def _add_other_goods_export_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    """
    MC-VERSJON: Eksport av andre varer (MP.OP-RW.RW-Other goods export-Nmix).
    Gjenbruker den generiske handelsløsningen for MC med full tidsserie (ingen 2023-kutt).
    """
    process_generic_trade_flow(
        results=results, 
        preloaded_data=preloaded_data, 
        current_params=current_params,
        current_trade_factors=current_trade_factors, 
        flow_code='MP.OP-RW.RW-Other goods export-Nmix',
        target_types=[
            'organisk materiale', 'blomster', 'frø', 'kjemikalier', 'såpe', 
            'industrielt protein', 'plastprodukter', 'gummi', 'skinn', 'lærprodukter', 
            'tre', 'silke', 'ull', 'bomull', 'nylon', 'tekstil', 'møbler', 
            'plast', 'leker', 'NH3'
        ],
        is_import=False, 
        dataset_noise=dataset_noise
    )
    
    
import pandas as pd
import numpy as np

def _add_consumer_goods_mc(results, preloaded_data, current_params, current_trade_factors, dataset_noise):
    """
    MC-VERSJON: Beregner massebalansen for forbruksvarer (MP.OP-HS.HS-Consumer goods-Nmix).
    STRIKT: Kjører for perioden 1990-2023 (synkront med avløpsdata).
    Kaster feil hvis noen av de 5 nødvendige utstrømmene mangler i results.
    """
    flow_code = 'MP.OP-HS.HS-Consumer goods-Nmix'
    collected_years = set()
    
    # 1. Definer gyldige årstall for massebalansen (1990-2023)
    target_years = {y for y in EXPECTED_YEARS if 1990 <= y <= 2023}
    
    # Forventet antall uavhengige strømmer per år for fullstendig balanse
    N_IN = 6
    N_OUT = 5

    inflow_totals = {}
    outflow_totals = {}
    inflow_count = {}
    outflow_count = {}

    def add_flow(year, val, totals_dict, count_dict):
        if val == 0 or val is None or pd.isna(val):
            return
        totals_dict[year] = totals_dict.get(year, 0.0) + float(val)
        count_dict[year] = count_dict.get(year, 0) + 1

# =========================================================================
    # --- INFLOWS (MED SPORING AV ENKELTSTRØMMER) -----------------------------
    # =========================================================================
    inflow_tracker = {
        'crops': 0,
        'animal': 0,
        'recycling': 0,
        'feedstock': 0,
        'roundwood': 0,
        'other_import': 0
    }

    # 1) Crop products for industrial use
    df_gnb = preloaded_data.get('gnb_sheet30_raw')
    if df_gnb is not None:
        crops_dict = find_industrial_crop_products(df_gnb, dataset_noise)
        if crops_dict: inflow_tracker['crops'] = len(crops_dict)
        for year, val in crops_dict.items():
            add_flow(year, val, inflow_totals, inflow_count)

    # 2) Non-edible animal products
    df_hides = preloaded_data.get('fao_hides_clean')
    df_wool = preloaded_data.get('wool_production')
    df_sheep = preloaded_data.get('ssb_sheep_numbers')
    if all(df is not None for df in [df_hides, df_wool, df_sheep]):
        animal_dict = find_non_edible_animal_products(df_hides, df_wool, df_sheep, current_params, dataset_noise)
        if animal_dict: inflow_tracker['animal'] = len(animal_dict)
        for year, val in animal_dict.items():
            add_flow(year, val, inflow_totals, inflow_count)

# 6) SHARED INFLOW: Recycling (PR.SO-MP.OP-Recycling-Nmix)
    existing_flows = {}
    for res in results:
        existing_flows.setdefault(res['flow_name'], {})[res['year']] = res['value']

    recycling_flow_code = 'PR.SO-MP.OP-Recycling-Nmix'
    if recycling_flow_code in existing_flows:
        # Alternativ A: PR har kjørt først og lagt resultatet i results
        for year, val in existing_flows[recycling_flow_code].items():
            add_flow(year, val, inflow_totals, inflow_count)
    else:
        # Alternativ B: MP kjører før PR. Vi kjører den originale funksjonen lokalt.
        t_params = current_params.get_trade_params() if hasattr(current_params, 'get_trade_params') else current_params
        
        local_recycling_dict = find_recycling(
            preloaded_data=preloaded_data,
            current_params=current_params,
            dataset_noise=dataset_noise,
            prepared_trade_recycling=None,  # Fallback hvis varehandel ikke trengs lokalt
            prepared_trade_reuse=None,
            trade_params=t_params
        )
        for year, val in local_recycling_dict.items():
            add_flow(year, val, inflow_totals, inflow_count)
            
    # 4) Fuel used as feedstock
    feedstock_dict, _ = find_feedstock_fuel(preloaded_data, current_params, dataset_noise)
    if feedstock_dict: inflow_tracker['feedstock'] = len(feedstock_dict)
    for year, val in feedstock_dict.items():
        add_flow(year, val, inflow_totals, inflow_count)

    # 5) Industrial round wood
    roundwood_dict, _ = find_industrial_round_wood(preloaded_data, current_params, dataset_noise)
    if roundwood_dict: inflow_tracker['roundwood'] = len(roundwood_dict)
    for year, val in roundwood_dict.items():
        add_flow(year, val, inflow_totals, inflow_count)

    # 6) Other goods import
    temp_import_results = []
    process_generic_trade_flow(
        results=temp_import_results, preloaded_data=preloaded_data, current_params=current_params,
        current_trade_factors=current_trade_factors, flow_code='RW.RW-MP.OP-Other goods import -Nmix',
        target_types=[
            'organisk materiale','blomster','frø','kjemikalier','såpe','industrielt protein',
            'plastprodukter','gummi','skinn','lærprodukter','tre','silke','ull',
            'bomull','nylon','tekstil','møller','plast','leker','plastavfall','tekstil_brukt'
        ],
        is_import=True, dataset_noise=dataset_noise
    )
    if temp_import_results: inflow_tracker['other_import'] = len(temp_import_results)
    for res in temp_import_results:
        add_flow(res['year'], res['value'], inflow_totals, inflow_count)

    # Print rapporten før vi går til balansen
    print("\n--- STATUS FOR INNLØPS-STRØMMER (Antall år levert) ---")
    for kilde, antall in inflow_tracker.items():
        print(f"  {kilde}: {antall} år med data")
    print("----------------------------------------------------\n")
    
    
    # =========================================================================
    # --- OUTFLOWS (Hentes STRIKT fra resultater kjørt tidligere) -------------
    # =========================================================================

    # Bygg oppslag fra results
    existing_outflows = {}
    for res in results:
        f_name = res['flow_name']
        f_year = res['year']
        existing_outflows.setdefault(f_name, {})[f_year] = res['value']

    # Liste over de 5 påkrevde utstrømmene
    required_outflows = [
        'MP.OP-PR.SO-Other industry waste-Nmix',
        'MP.OP-PR.WW-Other industry wastewater-Nmix',
        'MP.OP-HY.SW-Untreated wastewater-Nmix',
        'MP.OP-RW.RW-Other goods export-Nmix',
        'MP.OP-EF.IC-Industrial waste fuels-Nmix'
    ]

    # Verifiser og legg til alle 5
    for out_code in required_outflows:
        if out_code not in existing_outflows:
            raise ValueError(
                f"[KRITISK FEIL] Utstrømmen '{out_code}' ble ikke funnet i 'results'. "
                f"Denne må beregnes og legges til FØR _add_consumer_goods_mc kjøres."
            )
        for year, val in existing_outflows[out_code].items():
            add_flow(year, val, outflow_totals, outflow_count)


    # =========================================================================
    # --- NET CONSUMER GOODS PER YEAR (MED FEILSØKINGSPRINT) ------------------
    # =========================================================================
    print(f"\n=== FEILSØKING FOR {flow_code} ===")
    print(f"Mål: N_IN={N_IN} strømmer, N_OUT={N_OUT} strømmer")
    
    for year in sorted(list(target_years)):
        in_val = inflow_totals.get(year, 0.0)
        out_val = outflow_totals.get(year, 0.0)

        n_in = inflow_count.get(year, 0)
        n_out = outflow_count.get(year, 0)

        collected_years.add(year)

        # Print status for hvert år så vi ser hvor det svikter
        print(f"År {year}: Inputs={n_in}/{N_IN} ({in_val:.4f} kt N) | Outputs={n_out}/{N_OUT} ({out_val:.4f} kt N)")

        if n_in == N_IN and n_out == N_OUT:
            value = in_val - out_val
            if value < 0:
                print(f"  [MERK] Negativ balanse i {year}: {value:.4f} kt N (Blir klippet til 0.0)")
            comment = 'ok (MC-balanse komplett)'
            data_sources = 'Massebalanse (Inflows - Outflows)'
        else:
            value = 0.0
            comment = f'Ufullstendig: fant {n_in}/{N_IN} inputs og {n_out}/{N_OUT} outputs'
            data_sources = 'Manglende ledd i massebalanse'

        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(max(0.0, value)),
            'comment': comment,
            'data_sources': data_sources
        })

    print("=== FEILSØKING FERDIG ===\n")

    # Sluttkontroll mot mål-årene
    missing_years = target_years - collected_years
    report_missing_years(flow_code, missing_years, results)