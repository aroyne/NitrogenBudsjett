#!/usr/bin/env python3
# -*- coding: utf-8 -*
import numpy as np
import pandas as pd
import scipy.stats as stats
import pickle
from calculations.n_params import NParameters
from calculations.utils import (
    EXPECTED_YEARS)
import calculations.at as at  # Vi importerer atmosfære-sektoren vår for å teste
import time

def generate_mc_parameter_sets(filename="data_files/N_parameters.xlsx", num_simulations=100):
    """Leser globale parametere, avfallsfraksjoner og datasett-usikkerheter, og genererer uavhengige MC-trekk."""
    import pandas as pd
    import numpy as np
    import scipy.stats as stats
    
    # 1. Les inn alle de tre arkene
    df_global = pd.read_excel(filename, sheet_name='global_parameters')
    df_waste = pd.read_excel(filename, sheet_name='waste_fractions')
    df_animal_products = pd.read_excel(filename, sheet_name='animal_products')
    df_datasets = pd.read_excel(filename, sheet_name='dataset_uncertainties')
    
    # Standardiser kolonnenavnene for sammenslåing
    df_global_clean = df_global[['parameter_id', 'value', 'distribution_type', 'uncertainty_type', 'lower_bound', 'upper_bound']].copy()    
    df_waste_clean = df_waste[['waste_category', 'N_frac', 'distribution_type', 'uncertainty_type', 'lower_bound', 'upper_bound']].copy()
    df_waste_clean.rename(columns={'waste_category': 'parameter_id', 'N_frac': 'value'}, inplace=True)
    df_animal_products_clean = df_animal_products[['item', 'N_content_percent', 'distribution_type', 'uncertainty_type', 'lower_bound', 'upper_bound']].copy()
    df_animal_products_clean.rename(columns={'item': 'parameter_id', 'N_content_percent': 'value'}, inplace=True)
    
    # For datasett bruker vi selve 'dataset_name' som id, og setter basisverdi til 1.0 (siden det er en multiplikator)
    df_datasets_clean = df_datasets[['dataset_name', 'distribution_type', 'uncertainty_type', 'lower_bound', 'upper_bound']].copy()
    df_datasets_clean.rename(columns={'dataset_name': 'parameter_id'}, inplace=True)
    df_datasets_clean['value'] = 1.0
    
    # Slå alt sammen til én felles masterliste
    df_all_params = pd.concat([df_global_clean, df_waste_clean, df_datasets_clean, df_animal_products_clean], ignore_index=True)
    
    mc_samples = {}
    
    for _, row in df_all_params.iterrows():
        p_id = str(row['parameter_id']).strip()
        if pd.isna(p_id) or p_id == 'nan':
            continue
            
        val = float(row['value'])
        dist = str(row.get('distribution_type', 'none')).strip()
        unc_type = str(row.get('uncertainty_type', 'none')).strip()
        
        if pd.isna(dist) or dist in ['none', 'nan'] or unc_type in ['none', 'nan']:
            mc_samples[p_id] = np.full(num_simulations, val)
            continue
            
        # Beregn absolutte grenser for PERT/normal basert på den oppgitte usikkerheten
        if 'perc' in unc_type:
            low = val * (1 - float(row['lower_bound']) / 100)
            high = val * (1 + float(row['upper_bound']) / 100)
        else:
            low = float(row['lower_bound'])
            high = float(row['upper_bound'])
            
        # --- TREKK VERDIER ---
        if dist == 'PERT' and low < high:
            range_width = high - low
            alpha = 1 + 4 * (val - low) / range_width
            beta_param = 1 + 4 * (high - val) / range_width
            mc_samples[p_id] = stats.beta.rvs(alpha, beta_param, loc=low, scale=range_width, size=num_simulations)
            
        elif dist in ['norm', 'normal']:
            std_dev = val * (float(row['upper_bound']) / 100) if 'perc' in unc_type else float(row['upper_bound'])
            mc_samples[p_id] = np.random.normal(val, std_dev, num_simulations)
            
        elif dist == 'log-normal':
            std_dev = val * (float(row['upper_bound']) / 100) if 'perc' in unc_type else float(row['upper_bound'])
            sigma_log = np.sqrt(np.log(1 + (std_dev / val) ** 2))
            mu_log = np.log(val) - 0.5 * sigma_log ** 2
            mc_samples[p_id] = np.random.lognormal(mu_log, sigma_log, num_simulations)
            
        else:
            mc_samples[p_id] = np.full(num_simulations, val)
            
    # Konverter til en liste av ordbøker
    parameter_sets = []
    for i in range(num_simulations):
        single_set = {p_id: mc_samples[p_id][i] for p_id in mc_samples}
        parameter_sets.append(single_set)
        
    return parameter_sets

if __name__ == "__main__":
    import calculations.shared_flow_calculations as shared
    from calculations.utils import read_trade_data
    
    N_sim = 1  # Vi starter med 100 runder for testing
    
    GNB_FILE = 'data_files/aei_pr_gnb__custom_18744910_spreadsheet.xlsx'

    
    # =========================================================================
    # TRINN 1: LES TUNGE FILER ÉN ENESTE GANG (FØR LOOPEN)
    # =========================================================================
    print("[MC START] Leser tunge databaser fra disk (vennligst vent)...")
    
    # 1. Les den store handelsdata-CSV-en
    df_trade_raw = read_trade_data('data_files/Tab_08801_1988_2024.csv')
    
    # Les inn energibalansen en gang for alle før loopen ---
    print("[MC START] Leser energibalansen fra disk...")
    df_energy_raw = pd.read_excel(
        'data_files/11561_20251113-154607.xlsx',
        sheet_name='EnergibalansenGWh',
        header=None  # Vi slår av header slik at radnumrene våre i iloc[] stemmer perfekt!
    )
    
    # les inn avfallsdata
    print("[MC START] Leser SSB avfallsstatistikk (05282 og 10514) fra disk...")
    df_waste_05282_raw = pd.read_excel(
        'data_files/05282_20260211-091021.xlsx',
        sheet_name='05282',
        header=None
    )
    df_waste_10514_raw = pd.read_excel(
        'data_files/10514_20260211-094101.xlsx',
        sheet_name='10514',
        header=None
    )
    
    # --- LES INN HISTORISK INDUSTRI- AVFALL ÉN GANG FØR LOOPEN ---
    print("Leser inn historiske avfallsdata for industri...")
    df_hist_waste_raw = pd.read_excel('data_files/kommunalt_avfall_1985_1995.xlsx', sheet_name='avfallsmengder')

    # 2. Last inn parameter-hjelpetabeller fra N_parameters
    params_init = NParameters("data_files/N_parameters.xlsx")
    trade_params = params_init.get_trade_params()
    trade_mapping = params_init.get_trade_mapping()
    
    # --- NYTT: Preparer ammoniakkdataene ÉN gang før loopen ---
    print("[MC START] Preparerer og grovfiltrerer handelsdata for ammoniakk...")
    types_to_keep_nh3 = ['NH3']
    impeks_import = 1
    
    # 1. Filtrer mapping-tabellen på NH3
    mapping_subset_nh3 = trade_mapping[trade_mapping['type'].isin(types_to_keep_nh3)].copy()
    
    # 2. Filtrer de 6 mill radene på Import (impeks=1)
    df_ammonia_prepared = df_trade_raw[df_trade_raw['impeks'] == impeks_import].copy()
    
    # 3. Gjør den tunge koblingen (merge) mot varenummer
    df_ammonia_prepared = df_ammonia_prepared.merge(
        mapping_subset_nh3[['Varenr', 'konv', 'type']],
        left_on='HS_code',
        right_on='Varenr',
        how='inner'
    )
    
    # --- NYTT: Preparer avfallsdata for resirkulering ÉN gang før loopen ---
    print("[MC START] Preparerer og grovfiltrerer handelsdata for avfallsekport...")
    types_to_keep_recycling = ['plastavfall', 'papiravfall', 'tekstilavfall']
    impeks_export = 2  # 2 betyr eksport
    
    # 1. Filtrer mapping-tabellen på de riktige avfallstypene
    mapping_subset_recycling = trade_mapping[trade_mapping['type'].isin(types_to_keep_recycling)].copy()
    
    # 2. Filtrer de 6 mill radene på Eksport (impeks=2)
    df_recycling_prepared = df_trade_raw[df_trade_raw['impeks'] == impeks_export].copy()
    
    # 3. Gjør den tunge koblingen (merge) mot varenummer
    df_recycling_prepared = df_recycling_prepared.merge(
        mapping_subset_recycling[['Varenr', 'konv', 'type']],
        left_on='HS_code',
        right_on='Varenr',
        how='inner'
    )
    
    # --- NYTT: Preparer data for ANDRE VARER EKSPORT ÉN gang før loopen ---
    print("[MC START] Preparerer og grovfiltrerer handelsdata for andre vareeksporter...")
    types_to_keep_other = [
        'organisk materiale', 'blomster', 'frø', 'kjemikalier', 'såpe', 
        'industrielt protein', 'plastprodukter', 'gummi', 'skinn', 
        'lærprodukter', 'tre', 'silke', 'ull', 'bomull', 'nylon', 
        'tekstil', 'møbler', 'plast', 'leker', 'NH3'
    ]
    
    # 1. Filtrer mapping-tabellen på de riktige varetypene for andre varer
    mapping_subset_other = trade_mapping[trade_mapping['type'].isin(types_to_keep_other)].copy()
    
    # 2. Siden vi allerede har filtrert df_trade_raw på impeks=2 for avfall, 
    # kan vi gjenbruke en kopi av df_recycling_prepared sitt rå-utgangspunkt for å spare minne/tid:
    df_other_export_prepared = df_trade_raw[df_trade_raw['impeks'] == impeks_export].copy()
    
    # 3. Gjør den tunge koblingen (merge) mot varenummer
    df_other_export_prepared = df_other_export_prepared.merge(
        mapping_subset_other[['Varenr', 'konv', 'type']],
        left_on='HS_code',
        right_on='Varenr',
        how='inner'
    )
    
    # --- NYTT: Preparer data for ANDRE VARER IMPORT ÉN gang før loopen ---
    print("[MC START] Preparerer og grovfiltrerer handelsdata for andre vareeksporter...")
    types_to_keep_other = [
        'organisk materiale','blomster','frø',
        'kjemikalier' ,'såpe' ,'industrielt protein',
        'plastprodukter' ,'gummi' ,'skinn' ,'lærprodukter' ,'tre' ,'silke' ,'ull',
        'bomull' ,'nylon' ,'tekstil' ,'møbler' ,'plast' ,'leker','plastavfall','tekstil_brukt'
    ]
    
    # 1. Filtrer mapping-tabellen på de riktige varetypene for andre varer
    mapping_subset_other = trade_mapping[trade_mapping['type'].isin(types_to_keep_other)].copy()
    
    # 2. Siden vi allerede har filtrert df_trade_raw på impeks=2 for avfall, 
    # kan vi gjenbruke en kopi av df_recycling_prepared sitt rå-utgangspunkt for å spare minne/tid:
    df_other_import_prepared = df_trade_raw[df_trade_raw['impeks'] == impeks_import].copy()
    
    # 3. Gjør den tunge koblingen (merge) mot varenummer
    df_other_import_prepared = df_other_import_prepared.merge(
        mapping_subset_other[['Varenr', 'konv', 'type']],
        left_on='HS_code',
        right_on='Varenr',
        how='inner'
    )
    
    print("[MC START] Forhåndssummerer andre vareeksporter...")
    df_other_export_prepared = df_other_export_prepared.groupby(['year', 'konv'], as_index=False)['amount'].sum()
    
    print("[MC START] Forhåndssummerer andre vareimporter...")
    df_other_import_prepared = df_other_import_prepared.groupby(['year', 'konv'], as_index=False)['amount'].sum()
    
    # --- NYTT: Preparer tekstildata for gjenbruk ÉN gang før loopen ---
    print("[MC START] Preparerer og grovfiltrerer handelsdata for gjenbrukstekstiler...")
    types_to_keep_reuse = ['tekstil_brukt']
    impeks_export = 2  # Eksport
    
    # 1. Filtrer mapping-tabellen på brukte tekstiler
    mapping_subset_reuse = trade_mapping[trade_mapping['type'].isin(types_to_keep_reuse)].copy()
    
    # 2. Filtrer de 6 mill radene på Eksport (impeks=2)
    df_reuse_prepared = df_trade_raw[df_trade_raw['impeks'] == impeks_export].copy()
    
    # 3. Gjør den tunge koblingen (merge) mot varenummer
    df_reuse_prepared = df_reuse_prepared.merge(
        mapping_subset_reuse[['Varenr', 'konv', 'type']],
        left_on='HS_code',
        right_on='Varenr',
        how='inner'
    )
    
    # --- NYTT: Preparer eksport av fast avfall ÉN gang før loopen ---
    print("[MC START] Preparerer og grovfiltrerer handelsdata for eksport av fast avfall...")
    types_to_keep_solid_waste = ['kommunalt_avfall', 'farlig_avfall', 'annet_avfall']
    
    # 1. Filtrer mapping-tabellen på de riktige avfallstypene
    mapping_subset_solid = trade_mapping[trade_mapping['type'].isin(types_to_keep_solid_waste)].copy()
    
    # 2. Hent rådata for eksport (impeks=2)
    df_solid_waste_prepared = df_trade_raw[df_trade_raw['impeks'] == impeks_export].copy()
    
    # 3. Gjør koblingen (merge) mot varenummer
    df_solid_waste_prepared = df_solid_waste_prepared.merge(
        mapping_subset_solid[['Varenr', 'konv', 'type']],
        left_on='HS_code',
        right_on='Varenr',
        how='inner'
    )
    
    # 4. Forhåndssummer mengder per år og konv (likt som for andre varer)
    print("[MC START] Forhåndssummerer eksport av fast avfall...")
    df_solid_waste_prepared = df_solid_waste_prepared.groupby(['year', 'konv'], as_index=False)['amount'].sum()
    
    
    # --- NYTT: Les inn akvakulturdata én gang for alle ---
    # Moderne data: Vi hopper over de to første radene slik at rad 3 (årstallene) blir kolonnenavn
    df_aqua_modern_raw = pd.read_excel(
        'data_files/A.06.002_20251111-140559.xlsx', 
        sheet_name='A.06.002',
        header=2  # Python starter på 0, så rad 3 blir indeks 2
    )
    # Vi beholder kun kolonnene som faktisk er årstall (f.eks. fra kolonne 3 og utover)
    # Du kan eventuelt trimme den hvis det trengs, men pandas leser stort sett dette fint.
    
    # Gamle data: Enkel tabell med år og mengde
    df_aqua_old_raw = pd.read_excel(
        'data_files/akvakultur_1984_1994.xlsx',
        sheet_name='Ark1'
    )
    
    print("[MC START] Genererer parametersett...")
    parameter_sets = generate_mc_parameter_sets(num_simulations=N_sim)
    
    # --- NYTT: Les inn avfallsfraksjoner en gang for alle før loopen ---
    print("[MC START] Leser avfallsfraksjoner fra N_parameters...")
    df_waste_params_raw = pd.read_excel(
        'data_files/N_parameters.xlsx',
        sheet_name='waste_fractions'
    )
    df_waste_params_raw.set_index('waste_category', inplace=True)
    
    print("[MC START] Leser Gross Nutrient Balance (Sheet 30) fra disk...")
    df_gnb_sheet30_raw = pd.read_excel(
        GNB_FILE,  # Bruker den eksisterende filbanen din
        sheet_name='Sheet 30',
        header=None
    )
    
    # --- NYTT: Preparer FAOSTAT skogsdata en gang for alle før loopen ---
    print("[MC START] Preparerer og grovfiltrerer FAOSTAT skogsdata...")
    df_fao_raw = pd.read_csv('data_files/FAOSTAT_data_en_2-20-2026.csv')
    
    # Grovfiltrer på produksjon med faktiske verdier med en gang
    df_fao_filtered = df_fao_raw[(df_fao_raw['Element'] == 'Production') & (df_fao_raw['Value'] != 0)].copy()
    
    # Del opp i to separate subsets basert på varetype for å eliminere tunge filteroperasjoner i loopen
    df_fao_conifer = df_fao_filtered[df_fao_filtered['Item'] == 'Industrial roundwood, coniferous'][['Year', 'Value']].copy()
    df_fao_nonconifer = df_fao_filtered[df_fao_filtered['Item'] == 'Industrial roundwood, non-coniferous'][['Year', 'Value']].copy()
    
    # Aggreger (sum) per år med en gang i tilfelle det er duplikate rader i rådataene
    df_wood_conifer_year = df_fao_conifer.groupby('Year', as_index=False)['Value'].sum()
    df_wood_nonconifer_year = df_fao_nonconifer.groupby('Year', as_index=False)['Value'].sum()

    # --- NYTT: Les inn industriell bioenergi en gang for alle før loopen ---
    print("[MC START] Leser industriell bioenergi (08205 og historiske data) fra disk...")
    df_bio_08205_raw = pd.read_excel(
        'data_files/08205_20251104-141305.xlsx',
        sheet_name='Energibruk',
        header=None
    )
    df_bio_hist_raw = pd.read_excel(
        'data_files/egentilvirket_bioenergi_industri.xlsx',
        sheet_name='Ark1',
        header=None
    )

    # --- LES INN DEPONIDATA ÉN GANG FØR LOOPEN ---
    print("Leser inn deponiutslipp...")
    df_deponi_utslipp_raw = pd.read_excel("data_files/Utslipp_deponi.xlsx", sheet_name="Utslipp")
    df_deponi_tilkobling_raw = pd.read_excel("data_files/Utslipp_deponi.xlsx", sheet_name="tilkobling")
    
    # --- LES INN ANIMALSKE PRODUKTER ÉN GANG FØR LOOPEN ---
    print("Leser inn data for animalske biprodukter...")
    df_faostat_raw = pd.read_csv('data_files/FAOSTAT_data_en_11-18-2025.csv')
    df_wool_raw    = pd.read_excel('data_files/ull.xlsx', skiprows=3)
    df_sheep_raw   = pd.read_excel('data_files/03710_20260128-152225.xlsx', skiprows=2)
    
    # --- NYTT: Preparer avløpsdata for øvrig industri ÉN gang før loopen ---
    print("[MC START] Leser og preparerer avløpsdata for øvrig industri...")
    df_emissions_raw = pd.read_excel('data_files/Årlig utslipp til vann - Landbasert 02-02-2026.xlsx', header=0)
    df_categories_raw = pd.read_excel('data_files/industry_categories.xlsx')
    
    # 1. Filtrer på nitrogen
    df_emissions_n = df_emissions_raw[df_emissions_raw['Komponent'] == 'nitrogen, totalt']
    
    # 2. Finn virksomhetene som skal beholdes
    categories_keep = df_categories_raw[
        (df_categories_raw['kategori'] == 'OP') & 
        (df_categories_raw['kommunalt nett?'] == 'ja')
    ]
    
    # 3. Filtrer utslippene og gjør om fra tonn til kilotonn (/ 1000) med en gang
    df_emissions_op = df_emissions_n[df_emissions_n['AnleggNavn'].isin(categories_keep['Virksomhet'])].copy()
    df_emissions_op['Mengde_kt'] = df_emissions_op['Mengde'] / 1000.0
    
    # 4. Grupper per år én gang for alle, og gjør om til en superkjapp Python-ordbok {år: verdi}
    # Vi henter kun år i range(1989, 2025) som du spesifiserte
    df_sum_by_year = df_emissions_op.groupby('År')['Mengde_kt'].sum()
    dict_industry_wastewater_prepared = {
        int(year): float(val) 
        for year, val in df_sum_by_year.items() 
        if 1989 <= year <= 2024
    }
    
    # --- NYTT: Preparer ubehandlet avløpsdata (OP) ÉN gang før loopen ---
    print("[MC START] Preparerer ubehandlet avløpsdata (OP)...")
    
    # 1. Finn virksomhetene med 'nei' eller 'ukjent' i kommunalt nett?
    categories_keep_untreated = df_categories_raw[
        (df_categories_raw['kategori'] == 'OP') & 
        (df_categories_raw['kommunalt nett?'].isin(['nei', 'ukjent']))
    ]
    
    # 2. Filtrer utslippene (gjenbruker df_emissions_n som vi allerede har filtrert på nitrogen)
    df_emissions_untreated = df_emissions_n[df_emissions_n['AnleggNavn'].isin(categories_keep_untreated['Virksomhet'])].copy()
    df_emissions_untreated['Mengde_kt'] = df_emissions_untreated['Mengde'] / 1000.0
    
    # 3. Grupper per år, og gjør om til ordbok for år < 2024 der verdi != 0
    df_sum_untreated_year = df_emissions_untreated.groupby('År')['Mengde_kt'].sum()
    dict_op_untreated_prepared = {
        int(year): float(val) 
        for year, val in df_sum_untreated_year.items() 
        if year < 2024 and val != 0
    }
    
    # --- NYTT: Preparer data for gjenvinning (recycling) ÉN gang før loopen ---
    print("[MC START] Leser og preparerer statistikk for materialgjenvinning...")
    
    # 1. Les ark 05281 (kolonne 4 til 21 -> indekser 3 til 20)
    df_05281_rec = pd.read_excel('data_files/05281_20260121-140338.xlsx', sheet_name='Avfall', header=None)
    years_05281 = df_05281_rec.iloc[2, 3:21].astype(int).tolist() # Rad 3
    
    # Vi henter ut de rene historiske mengde-vektorene (rader i excel - 1 for 0-indeks)
    data_05281 = {
        'years': years_05281,
        'paper': df_05281_rec.iloc[18, 3:21].astype(float).values,      # Rad 19
        'plastic': df_05281_rec.iloc[20, 3:21].astype(float).values,    # Rad 21
        'wood': df_05281_rec.iloc[23, 3:21].astype(float).values,       # Rad 24
        'textile': df_05281_rec.iloc[24, 3:21].astype(float).values,    # Rad 25
        'other': df_05281_rec.iloc[28, 3:21].astype(float).values,      # Rad 29
        'haz': df_05281_rec.iloc[29, 3:21].astype(float).values,        # Rad 30
        'contam': df_05281_rec.iloc[30, 3:21].astype(float).values     # Rad 31
    }

    # 2. Les ark 10513 (openpyxl brukte kolonne 2, 11, 20... med steg på 9)
    df_10513_rec = pd.read_excel('data_files/10513_20260212-104227.xlsx', sheet_name='10513', header=None)
    
    # Finn makskolonner i arket
    max_cols_in_df = df_10513_rec.shape[1]
    
    # Generer potensielle openpyxl-kolonner (2, 11, 20...) gjort om til 0-basert Pandas-indeks (1, 10, 19...)
    potential_cols = list(range(1, 110, 9))
    
    # Behold bare kolonneindekser som faktisk finnes i filen, og der rad 4 (indeks 3) ikke er tom
    cols_10513 = []
    years_10513 = []
    for c in potential_cols:
        if c < max_cols_in_df:
            val = df_10513_rec.iloc[3, c] # Les rad 4
            if pd.notna(val):
                cols_10513.append(c)
                years_10513.append(int(val))
    
    # Nå henter vi ut mengde-vektorene trygt kun for de gyldige kolonnene
    data_10513 = {
        'years': years_10513,
        'wood': df_10513_rec.iloc[8, [c+1 for c in cols_10513]].astype(float).values,     # Rad 9, col+1
        'paper': df_10513_rec.iloc[10, [c+1 for c in cols_10513]].astype(float).values,   # Rad 11, col+1
        'plastic': df_10513_rec.iloc[16, [c+1 for c in cols_10513]].astype(float).values, # Rad 17, col+1
        'rubber': df_10513_rec.iloc[17, [c+1 for c in cols_10513]].astype(float).values,  # Rad 18, col+1
        'textile': df_10513_rec.iloc[18, [c+1 for c in cols_10513]].astype(float).values, # Rad 19, col+1
        'haz': df_10513_rec.iloc[21, [c+1 for c in cols_10513]].astype(float).values,     # Rad 22, col+1
        'mixed': df_10513_rec.iloc[22, [c+1 for c in cols_10513]].astype(float).values,   # Rad 23, col+1
        'other': df_10513_rec.iloc[23, [c+1 for c in cols_10513]].astype(float).values,   # Rad 24, col+1
        'contam': df_10513_rec.iloc[24, [c+1 for c in cols_10513]].astype(float).values   # Rad 25, col+1
    }
    # 3. Les historisk gjenbruksandel (1985-1995)
    df_hist_rec = pd.read_excel('data_files/kommunalt_avfall_1985_1995.xlsx', sheet_name='forbrenning og gjenvinning', header=None)
    rec_frac_1985 = float(df_hist_rec.iloc[1, 1]) / 100 # Rad 2, Kol B
    rec_frac_1992 = float(df_hist_rec.iloc[2, 1]) / 100 # Rad 3, Kol B
    change_per_year = (rec_frac_1992 - rec_frac_1985) / 7
    
    # Hent ut de faste historiske fraksjonene for rad 3, 4, 5 (for år 1992, 1993, 1994)
    hist_fractions_92_94 = df_hist_rec.iloc[2:5, 1].astype(float).values / 100.0
    
    data_hist_rec = {
        'rec_frac_1985': rec_frac_1985,
        'change_per_year': change_per_year,
        'fractions_92_94': hist_fractions_92_94
    }
    
    # --- NYTT: Preparer avløpsslam til biogass ÉN gang før loopen ---
    print("[MC START] Leser og preparerer biogassdata for avløpsslam...")
    df_12359_raw = pd.read_excel('data_files/12359_20251211-153434.xlsx', sheet_name='Mengde', header=None)
    
    # openpyxl kolonne 4 til 11 betyr Pandas-indekser 3 til 10
    years_12359 = df_12359_raw.iloc[2, 3:11].astype(int).tolist()   # Rad 3
    amounts_12359 = df_12359_raw.iloc[73, 3:11].astype(float).values # Rad 74
    
    data_12359_prepared = {
        'years': years_12359,
        'amounts': amounts_12359
    }
    
    
    

    # =========================================================================
    # TRINN 2: SIMULERINGSLOOPEN (LYNRASK)
    # =========================================================================
    print(f"[MC LOOP] Starter {N_sim} simuleringsrunder...")
    
    mc_all_runs_results = []
    
    for i in range(N_sim):
        measure_time = (i == 0)
        current_round_params = parameter_sets[i]
        
        # Her skal alle resultatene for akkurat denne runden samles
        round_results = []
        
        try:
            # 1. Ammoniakkimport
            if measure_time: t0 = time.time()
            ammonia_import = shared.find_ammonia_import(
                prepared_trade_data=df_ammonia_prepared,
                current_params=current_round_params,
                trade_params=trade_params
            )
            if measure_time: print(f"[TID] ammonia_import: {(time.time() - t0)*1000:.2f} ms")
            
            # 2. Akvakulturproduksjon
            if measure_time: t0 = time.time()
            aquaculture_production = shared.find_aquaculture_production(
                df_aqua_modern=df_aqua_modern_raw,
                df_aqua_old=df_aqua_old_raw,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] aquaculture_production: {(time.time() - t0)*1000:.2f} ms")
            
            # 3. Eksport for resirkulering
            if measure_time: t0 = time.time()
            export_for_recycling = shared.find_export_for_recycling(
                df_recycling_prepared,
                current_params=current_round_params,
                trade_params=trade_params
            )
            if measure_time: print(f"[TID] export_for_recycling: {(time.time() - t0)*1000:.2f} ms")
            
            # 4. Eksport for gjenbruk
            if measure_time: t0 = time.time()
            export_for_reuse = shared.find_export_for_reuse(
                df_reuse_prepared,
                current_params=current_round_params,
                trade_params=trade_params
            )
            if measure_time: print(f"[TID] export_for_reuse: {(time.time() - t0)*1000:.2f} ms")
            
            # 5. Råstoff og brensel (Feedstock fuel)
            if measure_time: t0 = time.time()
            feedstock_fuel = shared.find_feedstock_fuel(
                df_energy=df_energy_raw,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] feedstock_fuel: {(time.time() - t0)*1000:.2f} ms")
            
            # 6. Husholdningsavfall
            if measure_time: t0 = time.time()
            household_waste = shared.find_household_waste(
                df_05282=df_waste_05282_raw,
                df_10514=df_waste_10514_raw,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] household_waste: {(time.time() - t0)*1000:.2f} ms")
            
            # 6b. NYTT: Matindustriavfall (Inkludert i MC-loopen!)
            if measure_time: t0 = time.time()
            food_industry_waste = shared.find_food_industry_waste(
                df_05282=df_waste_05282_raw,
                df_10514=df_waste_10514_raw,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] food_industry_waste: {(time.time() - t0)*1000:.2f} ms")

            # 7. Industrielle avlinger (NÅ RETTET: sender inn current_params!)
            if measure_time: t0 = time.time()
            industrial_crops = shared.find_industrial_crop_products(
                df_gnb_sheet30=df_gnb_sheet30_raw,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] industrial_crops: {(time.time() - t0)*1000:.2f} ms")
            
            # 8. Industrirundvirke
            if measure_time: t0 = time.time()
            industrial_wood = shared.find_industrial_round_wood(
                df_conifer_year=df_wood_conifer_year,
                df_nonconifer_year=df_wood_nonconifer_year,
                current_params=current_round_params,
                expected_years=EXPECTED_YEARS
            )
            if measure_time: print(f"[TID] industrial_wood: {(time.time() - t0)*1000:.2f} ms")
            
            # 9. Egentilvirket bioenergi i industrien
            if measure_time: t0 = time.time()
            industrial_waste_fuels = shared.find_industrial_waste_fuels(
                df_bio_08205=df_bio_08205_raw,
                df_bio_hist=df_bio_hist_raw,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] industrial_waste_fuels: {(time.time() - t0)*1000:.2f} ms")
            
            # 10. Deponiutslipp til vann
            if measure_time: t0 = time.time()
            landfill_tilkoblet, landfill_ikke = shared.find_landfill_emissions_to_water(
                df_uts=df_deponi_utslipp_raw,
                df_tilk=df_deponi_tilkobling_raw,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] landfill_tilkoblet: {(time.time() - t0)*1000:.2f} ms")
            
            # 11. Ikke-spiselige animalske produkter (Huder og ull)
            if measure_time: t0 = time.time()
            non_edible_animal_N = shared.find_non_edible_animal_products(
                df_faostat=df_faostat_raw,
                df_wool=df_wool_raw,
                df_sheep=df_sheep_raw,
                current_params=current_round_params,
            )
            if measure_time: print(f"[TID] non_edible_animal_N: {(time.time() - t0)*1000:.2f} ms")
            
            # 12. Eksport av andre handelsvarer (kjører på mikrosekunder!)
            if measure_time: t0 = time.time()
            other_goods_export_N = shared.find_other_goods_export(
                prepared_trade_data=df_other_export_prepared,
                current_params=current_round_params, 
                trade_params = trade_params
            )
            if measure_time: print(f"[TID] other_goods_export_N: {(time.time() - t0)*1000:.2f} ms")
            
            # 13. Import av andre handelsvarer (kjører på mikrosekunder!)
            if measure_time: t0 = time.time()
            other_goods_import_N = shared.find_other_goods_import(
                prepared_trade_data=df_other_import_prepared,
                current_params=current_round_params, 
                trade_params = trade_params
            )
            if measure_time: print(f"[TID] other_goods_import_N: {(time.time() - t0)*1000:.2f} ms")
            
            # 14. Øvrig industriavfall
            if measure_time: t0 = time.time()
            other_industry_waste_N = shared.find_other_industry_waste(
                df_05282=df_waste_05282_raw,
                df_10514=df_waste_10514_raw,
                df_hist_waste=df_hist_waste_raw,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] other_industry_waste_N: {(time.time() - t0)*1000:.2f} ms")
            
            
            # 15. Avløpsvann fra øvrig industri (Kjører nå på mikrosekunder!)
            if measure_time: t0 = time.time()
            other_industry_wastewater = shared.find_other_industry_wastewater(
                prepared_wastewater_dict=dict_industry_wastewater_prepared,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] other_industry_wastewater: {(time.time() - t0)*1000:.2f} ms")
            
            # 16. Ubehandlet avløpsvann fra industri (OP)
            if measure_time: t0 = time.time()
            op_untreated_wastewater = shared.find_op_untreated_wastewater(
                prepared_untreated_dict=dict_op_untreated_prepared,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] op_untreated_wastewater: {(time.time() - t0)*1000:.2f} ms")
            
            # 17. Materialgjenvinning (Recycling) - Kjører på under 1 ms!
            if measure_time: t0 = time.time()
            recycling = shared.find_recycling(
                data_05281=data_05281,
                data_10513=data_10513,
                data_hist_rec=data_hist_rec,
                current_params=current_round_params,
                household_waste=household_waste,
                industry_waste=other_industry_waste_N, # Bruker resultatet fra punkt 14
                export_resirk=export_for_recycling,    # Bruker resultatet fra punkt 3
                export_reuse=export_for_reuse          # Bruker resultatet fra punkt 4
            )
            if measure_time: print(f"[TID] recycling: {(time.time() - t0)*1000:.2f} ms")
            
            # 18. Avløpsslam til biogass
            if measure_time: t0 = time.time()
            sewage_sludge_biogas = shared.find_sewage_sludge_biogas(
                prepared_biogas_data=data_12359_prepared,
                current_params=current_round_params
            )
            if measure_time: print(f"[TID] sewage_sludge_biogas: {(time.time() - t0)*1000:.2f} ms")
            
            # 19. Eksport av fast avfall
            if measure_time: t0 = time.time()
            solid_waste_export = shared.find_solid_waste_export(
                prepared_waste_data=df_solid_waste_prepared,
                current_params=current_round_params,
                trade_params=trade_params
            )
            if measure_time: print(f"[TID] solid_waste_export: {(time.time() - t0)*1000:.2f} ms")
            
            # --- VALGFRITT KONTROLL-PRINT FOR RUNDE 0 ---
            if i == 0:
                print("\n[KONTROLL] Alt sjekket og sikret i Runde 0!")
                print(f"  Husholdningsavfall 1990 (ekstrapolert + trendstøy): {household_waste.get(1990, 0):.2f} kt N")
                print(f"  Matindustriavfall 1990 (ekstrapolert + trendstøy): {food_industry_waste.get(1990, 0):.2f} kt N")
                print(f"  Industrielle avlinger 2018 (hull fylt + trendstøy): {industrial_crops.get(2018, 0):.2f} kt N")
                print(f"  Bioenergi i industri 1995 (ekstrapolert + trendstøy): {industrial_waste_fuels.get(1995, 0):.2f} kt N")
                # Sjekk deponiutslipp
                print(f"  Deponi (tilkoblet) 2009 (interpolert + trendstøy): {landfill_tilkoblet.get(2009, 0):.4f} kt N")
                print(f"  Deponi (tilkoblet) 2020 (ekte data + kildestøy): {landfill_tilkoblet.get(2020, 0):.4f} kt N")
                print(f"  Deponi (ikke-tilkoblet) 2020 (ekte data + kildestøy): {landfill_ikke.get(2020, 0):.4f} kt N")
                # Sjekk animalske produkter
                print(f"  Animalske biprod. 2001 (interpolert ull + trendstøy): {non_edible_animal_N.get(2001, 0):.4f} kt N")
                print(f"  Animalske biprod. 2010 (ekte ulldata + kildestøy): {non_edible_animal_N.get(2010, 0):.4f} kt N")
                # Sjekk eksport av andre handelsvarer
                print(f"  Eksport andre varer 1995 (handelsstøy lagt på): {other_goods_export_N.get(1995, 0):.4f} kt N")
                print(f"  Eksport andre varer 2010 (handelsstøy lagt på): {other_goods_export_N.get(2010, 0):.4f} kt N")
                print(f"  Eksport andre varer 2022 (handelsstøy lagt på): {other_goods_export_N.get(2022, 0):.4f} kt N")
                # Sjekk import av andre handelsvarer
                print(f"  Import andre varer 1995 (handelsstøy lagt på): {other_goods_import_N.get(1995, 0):.4f} kt N")
                print(f"  Import andre varer 2010 (handelsstøy lagt på): {other_goods_import_N.get(2010, 0):.4f} kt N")
                print(f"  Import andre varer 2022 (handelsstøy lagt på): {other_goods_import_N.get(2022, 0):.4f} kt N")
                # Sjekk øvrig industriavfall
                print(f"  Øvrig industriavfall 1990 (interpolert + trendstøy): {other_industry_waste_N.get(1990, 0):.4f} kt N")
                print(f"  Øvrig industriavfall 1995 (ekte data + kildestøy): {other_industry_waste_N.get(1995, 0):.4f} kt N")
                print(f"  Øvrig industriavfall 2020 (ekte data + kildestøy): {other_industry_waste_N.get(2020, 0):.4f} kt N")
                print(f"  Øvrig ind. avløpsvann 2020 (norskeutslipp-støy lagt på): {other_industry_wastewater.get(2020, 0):.4f} kt N")
                print(f"  Ubehandlet ind. avløp 2015 (norskeutslipp-støy lagt på): {op_untreated_wastewater.get(2015, 0):.4f} kt N")
                print(f"  Gjenvinning 1992 (historisk beregnet): {recycling.get(1992, 0):.4f} kt N")
                print(f"  Gjenvinning 2005 (05281-statistikk): {recycling.get(2005, 0):.4f} kt N")
                print(f"  Gjenvinning 2020 (10513-statistikk): {recycling.get(2020, 0):.4f} kt N")
                # Siden kolonne 4 til 11 i arket ditt representerer spesifikke år, kan du plukke et år du vet finnes der
                print(f"  Avløpsslam biogass (Runde 0 støy lagt på): {list(sewage_sludge_biogas.values())[0]:.4f} kt N for år {list(sewage_sludge_biogas.keys())[0]}")
                print(f"  Eksport fast avfall 1995 (Runde 0 støy lagt på): {solid_waste_export.get(1995, 0):.4f} kt N")
                print(f"  Eksport fast avfall 2010 (Runde 0 støy lagt på): {solid_waste_export.get(2010, 0):.4f} kt N")
                print(f"  Eksport fast avfall 2022 (Runde 0 støy lagt på): {solid_waste_export.get(2022, 0):.4f} kt N")
                print("-" * 50)
                
        except Exception as e:
            print(f"[FEIL i RUNDE {i}]: {str(e)}")
            raise e
                
        except Exception as e:
                print(f"\n[CRASH] Loopen feilet i runde {i} i shared_flow_calculations!")
                print(f"Feilmelding: {e}")
                break
                
        # (Senere skal at.execute_calculations, ag.execute_calculations osv. legges inn her)
        
        if i % 10 == 0 and i > 0:
            print(f"  Completed {i}/{N_sim} rounds...")
            
    print("\n[MC TEST] Ferdig! Testen kjørte gjennom uten å knele maskinen.")