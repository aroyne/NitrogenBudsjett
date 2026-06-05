#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 09:37:11 2026

@author: anja
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 09:30:00 2026

@author: anja
"""
import pandas as pd
import numpy as np

from calculations.utils import (
    EXPECTED_YEARS,
    report_missing_years,
    process_generic_trade_flow
)

def execute_calculations_rw(preloaded_data, current_params, dataset_noise, current_trade_factors):
    """
    MC-VERSJON: Beregner nitrogenflyt for rest-of-world (RW) uten fil-I/O i løkka.
    """
    results = []
    
    # 1. Hent ut den forhåndsinnleste rå-DataFramen fra datalasteren for 'rw_in_out' eller tilsvarende
    # (Justert navnet her så det matcher din datalaster-konvensjon fra at_mc)
    df_rw = preloaded_data.get('atm_in_out')
    
    if df_rw is None:
        print("[ADVARSEL] Data for 'atm_in_out' mangler i preloaded_data.")
        return results

    # 2. Kjør de omskrevne funksjonene med støyhåndtering
    _add_fuel_import(results, preloaded_data, current_params, current_trade_factors)
    _add_transport_fuel_import(results, preloaded_data, current_params, current_trade_factors)
    _add_solid_waste_import(results, preloaded_data, current_params, current_trade_factors)
    _add_food_import(results, preloaded_data, current_params, current_trade_factors)
    _add_other_goods_import(results, preloaded_data, current_params, current_trade_factors)
    _add_ammonia_import(results, preloaded_data, current_params, current_trade_factors)
    _add_animal_feed_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_aquaculture_feed_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_live_animal_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_mineral_fertilizer_import_mc(results, preloaded_data, current_params, dataset_noise)
    _add_rw_outflow_oxn_mc(results, df_rw, current_params, dataset_noise)
    _add_rw_outflow_rdn_mc(results, df_rw, current_params, dataset_noise)
    
    return results


def _add_fuel_import(results, preloaded_data, current_params, current_trade_factors):
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code='RW.RW-EF.EC-Fuel import-Nmix',
        target_types='fuel',       # Sendes inn som en ren streng
        is_import=True
    )        

def _add_transport_fuel_import(results, preloaded_data, current_params, current_trade_factors):
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code='RW.RW-EF.EC-Transport fuel import-Nmix',
        target_types='transport_fuel',       # Sendes inn som en ren streng
        is_import=True
    )        

def _add_solid_waste_import(results, preloaded_data, current_params, current_trade_factors):
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code='RW.RW-PR.SO-Solid waste import-Nmix',
        target_types=['kommunalt_avfall','annet_avfall','slam','farlig_avfall','tekstilavfall','plastavfall','papiravfall'],
        is_import=True
    )
    
    
def _add_food_import(results, preloaded_data, current_params, current_trade_factors):
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code='RW.RW-MP.FP-Food import-Nmix',
        target_types=['korn/planter', 'kjøtt/fisk/meieri/egg', 'mat'],
        is_import=True
    )
    
    
def _add_other_goods_import(results, preloaded_data, current_params, current_trade_factors):
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code='RW.RW-MP.OP-Other goods import -Nmix',
        target_types=['organisk materiale','blomster','frø',
     'kjemikalier' ,'såpe' ,'industrielt protein',
     'plastprodukter' ,'gummi' ,'skinn' ,'lærprodukter' ,'tre' ,'silke' ,'ull',
     'bomull' ,'nylon' ,'tekstil' ,'møbler' ,'plast' ,'leker','plastavfall','tekstil_brukt'],
        is_import=True
    )
    
    
def _add_ammonia_import(results, preloaded_data, current_params, current_trade_factors):
    process_generic_trade_flow(
        results=results,
        preloaded_data=preloaded_data,
        current_params=current_params,
        current_trade_factors=current_trade_factors,
        flow_code='RW.RW-MP.OP-Ammonia import -Nmix',
        target_types='NH3',       # Sendes inn som en ren streng
        is_import=True
    )        

def _add_animal_feed_import_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i importert kraftfôr.
    Bruker ferdiginnleste data fra RAM og påfører simulert støy per runde.
    """
    flow_code = 'RW.RW-AG.MM-Animal feed import-Nmix'
    collected_years = set()
    
    # Hent DataFrames fra preloaded_data
    df_raavarer = preloaded_data.get('feed_raavarer')
    df_totalkalkyle = preloaded_data.get('feed_totalkalkyle')
    
    if df_raavarer is None or df_totalkalkyle is None:
        print(f"[ADVARSEL] Mangler fôrdata i preloaded_data for {flow_code}.")
        return

    # --- 1. HENT PERTURBERTE PARAMETERE OG DATASET-STØY ---
    # N-fraksjoner (allerede perturbert i current_params)
    N_content_carb = float(current_params.get("feed_carb_N_frac", 0.015))  # Sett inn fornuftig default hvis mangler
    N_content_prot = float(current_params.get("feed_prot_N_frac", 0.070))  # Sett inn fornuftig default hvis mangler
    
    # Datasetstøy for Landbruksdirektoratets kraftfôrstatistikk
    key_kraft = 'Kraftforstatistikk'
    has_noise_kraft = dataset_noise and key_kraft in dataset_noise
    noise_kraft = dataset_noise[key_kraft]['value'] if has_noise_kraft else 1.0
    # Hvis usikkerheten din er 'abs', må logikken under justeres, men her antar vi 'perc' (f.eks. svinger rundt 1.0)
    
    # Datasetstøy for NIBIO Totalkalkylen
    key_total = 'Totalkalkylen'
    has_noise_total = dataset_noise and key_total in dataset_noise
    noise_total = dataset_noise[key_total]['value'] if has_noise_total else 1.0

    # --- 2. BEREGN FOR NYERE ÅR (Landbruksdirektoratet) ---
    N_cont_sum = 0
    valid_count = 0
    
    for _, row in df_raavarer.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        
        base_carb = float(row['value_carb'])
        base_prot = float(row['value_prot'])
        
        # Påfør dataset-støy på råvaremengdene (hvis prosentvis støy)
        if has_noise_kraft and dataset_noise[key_kraft]['type'] == 'perc':
            value_carb = base_carb * noise_kraft
            value_prot = base_prot * noise_kraft
        else:
            # Hvis absolutt støy, eller ingen støy:
            value_carb = base_carb
            value_prot = base_prot
            
        # Beregn Nitrogenmengde (tonn -> kt)
        imported_feed_N = (value_carb * N_content_carb + value_prot * N_content_prot) / 1000
        
        # Fysisk sperre
        if imported_feed_N < 0:
            imported_feed_N = 0.0
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': imported_feed_N,
            'comment': 'ok (MC-støy lagt på)',
            'data_sources': 'Landbruksdirektoratets kraftfôrstatistikk - årlig råvareforbruk'
        })
        
        # Akkumuler for å beregne historisk snitt (bruker de u-støyede basisverdiene for stabil historikk, eller støyede om ønskelig)
        if (base_carb + base_prot) > 0:
            N_cont_sum += ((base_carb * N_content_carb + base_prot * N_content_prot) / (base_carb + base_prot))
            valid_count += 1

    # Beregn gjennomsnittlig N-innhold per tonn vare (skalert til kg/tonn eller ren fraksjon etter din opprinnelige formel)
    # Din opprinnelige formel gjorde: N_cont_before_2000 = (imported_feed_N / (carb+prot)) * 1e3 -> som tilsvarer ren fraksjon * 1
    # Siden imported_feed_N var i kt, blir imported_feed_N / (t) * 1e3 = (t_N * 1e-3) / t * 1e3 = t_N / t (ren fraksjon).
    N_cont_before_2000 = (N_cont_sum / valid_count) if valid_count > 0 else 0.025  # default fallback

    # --- 3. BEREGN FOR ELDRE ÅR (NIBIO Totalkalkylen, år før 2000) ---
    for _, row in df_totalkalkyle.iterrows():
        year = int(row['year'])
        collected_years.add(year)
        
        base_feed_tonn = float(row['value'])
        
        # Påfør dataset-støy på kraftfôrmengden
        if has_noise_total and dataset_noise[key_total]['type'] == 'perc':
            feed_tonn = base_feed_tonn * noise_total
        else:
            feed_tonn = base_feed_tonn
            
        if year < 1995:            
            dom_frac = float(row['dom_frac'])
            comment = 'ok (MC-støy lagt på)'
        else:
            dom_frac = 0.694
            comment = 'interpolated (MC-støy lagt på)'
            
        # Formel: tonn * 1e-3 (til kt) * N-fraksjons-snitt * import-andel (1 - innenlandsk andel)
        value_kt_N = feed_tonn * 1e-3 * N_cont_before_2000 * (1 - dom_frac)
        
        if value_kt_N < 0:
            value_kt_N = 0.0
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value_kt_N,
            'comment': comment,
            'data_sources': 'NIBIO Totalkalkylen'
        })

    # --- 4. RAPPORTER MANGLENDE ÅR ---
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

from calculations.shared_flow_calculations import find_aquaculture_production

def _add_aquaculture_feed_import_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogen i importert fôr til akvakultur.
    Henter og støysetter produksjonsdata internt før fôrberegningen kjøres.
    """
    flow_code = 'RW.RW-HY.AC-Aquaculture feed import-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på parametere og datagrunnlag)'
    data_sources = 'Fiskeridirektoratet'
    
    # --- PUNKT 1: HENT RÅDATA FRA PRELOADED_DATA ---
    df_modern = preloaded_data.get('aqua_modern')
    df_old = preloaded_data.get('aqua_old')
    
    if df_modern is None or df_old is None:
        print(f"[ADVARSEL] Mangler akvakultur-rådata i preloaded_data for {flow_code}.")
        return

    # --- PUNKT 2: GENERER FERDIGSTØYSATT PRODUKSJON (kt N) ---
    aquaculture_production = find_aquaculture_production(
        df_modern, 
        df_old, 
        current_params, 
        dataset_noise
    )

    # --- PUNKT 3: HENT PERTURBERTE PARAMETERE FOR FÔR ---
    import_fraction = float(current_params.get("aquafeed_import_fraction", 0.80))
    prot_ret = float(current_params.get("aquafeed_N_retention", 0.35))
    feed_waste = float(current_params.get("aquafeed_waste_fraction", 0.05))

    # --- PUNKT 4: LOOP OVER TIDSSERIEN OG BEREGN FÔRIMPORT ---
    for year, fish_harvested_N in aquaculture_production.items():
        if year not in EXPECTED_YEARS:
            continue
            
        collected_years.add(year)
        
        # Beregn spist fôr (kt N)
        if prot_ret > 0:
            eaten_feed_N = fish_harvested_N / prot_ret
        else:
            eaten_feed_N = 0.0
            
        # Beregn totalt fôrbruk (inkludert spill)
        if feed_waste < 1:
            total_feed_N = eaten_feed_N / (1 - feed_waste)
        else:
            total_feed_N = 0.0
            
        # Beregn den importerte andelen
        imported_feed_N = total_feed_N * import_fraction
        
        # Fysisk sperre
        if imported_feed_N < 0:
            imported_feed_N = 0.0
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': float(imported_feed_N),
            'comment': comment,
            'data_sources': data_sources
        })
        
    # --- 5. RAPPORTER MANGLENDE ÅR ---
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_live_animal_import_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogenmengde fra import av levende dyr.
    Følger modellens standard: Henter FERDIG perturberte parametere og dataset-støy.
    """
    flow_code = 'RW.RW-AG.MM-Live animal import-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy ferdig beregnet sentralt)'
    data_sources = 'FAOSTAT Crops and livestock products'
    
    final_data = preloaded_data.get('fao_live_animals')
    if final_data is None:
        print(f"[ADVARSEL] Mangler fao_live_animals i preloaded_data for {flow_code}.")
        return

    # --- 1. GLOBALE PARAMETERE (Ferdig perturbert fra parameter-generatoren) ---
    prot_frac = float(current_params.get("live_animal_protein_frac", 0.15))
    prot_to_N = float(current_params.get("Jones_factor", 6.25))

    # --- 2. DATASET-STØY FOR FAOSTAT ---
    key_fao = 'Crops and livestock products'
    has_noise_fao = dataset_noise and key_fao in dataset_noise
    noise_fao = dataset_noise[key_fao]['value'] if has_noise_fao else 1.0

    # --- 3. REKNE UT N-MENGDE PER RAD (Vektorised i Pandas) ---
    # Vi oppretter en kopi for denne runden
    df_round = final_data.copy()

    # Påfør dataset-støy på antall dyr (Value) hvis det er prosentvis usikkerhet
    if has_noise_fao and dataset_noise[key_fao]['type'] == 'perc':
        df_round['perturbed_value'] = df_round['Value'] * noise_fao
    else:
        df_round['perturbed_value'] = df_round['Value']

    # Slå opp den ferdig perturberte vekten fra current_params basert på dyrenavnet ('Item')
    # Hvis et dyr ikke finnes i current_params, faller vi tilbake på en standardvekt (f.eks. 100 kg)
    def get_perturbed_weight(item_name):
        param_key = f"weight_{str(item_name).strip()}"
        return float(current_params.get(param_key, 100.0))

    # Lag en kolonne med vektene som ble trukket i denne MC-runden
    df_round['perturbed_weight'] = df_round['Item'].apply(get_perturbed_weight)

    # Standard formel for kt N
    df_round['N_amount'] = (
        df_round['perturbed_weight']
        * df_round['perturbed_value']
        * prot_frac
        * 1e-6
        / prot_to_N
    )

    # --- 4. AGGREGER OG LAGRE ---
    total_N_per_year = df_round.groupby('Year')['N_amount'].sum().to_dict()
    
    for year in sorted(EXPECTED_YEARS):
        if year in total_N_per_year:
            collected_years.add(year)
            value = total_N_per_year[year]
            
            if value < 0:
                value = 0.0
                
            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': float(value), 
                'comment': comment,
                'data_sources': data_sources
            })
            
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_mineral_fertilizer_import_mc(results, preloaded_data, current_params, dataset_noise):
    """
    MC-VERSJON: Beregner nitrogenmengde fra import av mineralgjødsel.
    Følger modellens standard: Henter ferdig rådata fra RAM og påfører datasetstøy.
    """
    flow_code = 'RW.RW-AG.SM-Mineral fertilizer import-Nmix'
    collected_years = set()
    comment = 'ok (MC-støy ferdig beregnet sentralt)'
    data_sources = 'FAOSTAT Fertilizer by Nutrient'
    
    # Hent ferdig vasket data fra preloaded_data
    final_data = preloaded_data.get('fao_mineral_fertilizer')
    if final_data is None:
        print(f"[ADVARSEL] Mangler fao_mineral_fertilizer i preloaded_data for {flow_code}.")
        return

    # --- 1. HENT DATASET-STØY FOR MINERALGJØDSEL ---
    key_fert = 'Fertilizer by nutrient'
    has_noise_fert = dataset_noise and key_fert in dataset_noise
    noise_fert = dataset_noise[key_fert]['value'] if has_noise_fert else 1.0
    
    # --- 2. AGGREGER OG PÅFØR STØY VEKTORISERT I PANDAS ---
    # Grupperer etter år i tilfelle det skulle være flere rader per år i rådataene
    # Konverterer direkte til en ordbok {Year: Value} for lynraskt oppslag
    total_fert_per_year = final_data.groupby('Year')['Value'].sum().to_dict()
    
    # --- 3. LOOP OVER EXPECTED YEARS OG LEGG I RESULTS ---
    for year in sorted(EXPECTED_YEARS):
        if year in total_fert_per_year:
            collected_years.add(year)
            
            # Hent basistall (tonn)
            base_value = float(total_fert_per_year[year])
            
            # Påfør dataset-støy (støyen er ferdig sentrert rundt 1.0 for 'perc' i din generator)
            if has_noise_fert and dataset_noise[key_fert]['type'] == 'perc':
                perturbed_value = base_value * noise_fert
            else:
                perturbed_value = base_value
            
            # Konverter fra tonn til kilotonn (t -> kt)
            value_kt = perturbed_value / 1000.0
            
            # Fysisk sperre mot negative verdier
            if value_kt < 0:
                value_kt = 0.0
                
            results.append({
                'flow_name': flow_code,
                'year': year,
                'value': value_kt, 
                'comment': comment,
                'data_sources': data_sources
            })
            
    # --- 4. RAPPORTER MANGLENDE ÅR ---
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)
    

def _add_rw_outflow_oxn_mc(results, df_rw, current_params, dataset_noise):
    flow_code = 'RW.RW-AT.AT-Atmospheric inflow-OXN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på uncertainty_type)'
    
    # Antar samme rad-oppsett (Excel rad 6-46 blir Pandas indeks 5-45) som df_atm
    for r in range(5, 45):
        if r >= len(df_rw):
            break
            
        year_val = df_rw.iloc[r, 0]  # Kolonne 1 (A) -> Indeks 0
        if pd.isna(year_val):
            continue
            
        year = int(year_val)
        collected_years.add(year)
        
        # Sjekk status i Kolonne 6 (F) -> Indeks 5 for å velge riktig datasett-nøkkel
        status_val = str(df_rw.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            
        # Hent basisverdi fra Kolonne 2 (B) -> indeks 1 for OXN og gjør om fra 100 tN til ktN  
        base_value = float(df_rw.iloc[r, 1]) / 10  
        
        # --- STØYLOGIKK ---
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        if dataset_noise and not has_noise and not hasattr(_add_rw_outflow_oxn_mc, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            print(f"          Kjører deterministisk (støy = 0) for denne strømmen inntil Excel oppdateres.")
            setattr(_add_rw_outflow_oxn_mc, f"warned_{dataset_key}", True)
            
        if has_noise:
            noise_info = dataset_noise[dataset_key]
            noise_val = noise_info['value']
            unc_type = noise_info['type']
            
            if unc_type == 'perc':
                value = base_value * noise_val
            else:
                if noise_val >= 0:
                    value = base_value + (noise_val * noise_info['upp_bound'])
                else:
                    value = base_value + (noise_val * noise_info['low_bound'])
        else:
            value = base_value
            
        if value < 0:
            value = 0.0
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)


def _add_rw_outflow_rdn_mc(results, df_rw, current_params, dataset_noise):
    flow_code = 'RW.RW-AT.AT-Atmospheric inflow-RDN'
    collected_years = set()
    comment = 'ok (MC-støy lagt på basert på uncertainty_type)'
    
    for r in range(5, 45): 
        if r >= len(df_rw):
            break
            
        year_val = df_rw.iloc[r, 0]  # Kolonne A -> Indeks 0
        if pd.isna(year_val):
            continue
            
        year = int(year_val)
        collected_years.add(year)
        
        status_val = str(df_rw.iloc[r, 5]).strip()
        if status_val == 'interpolated':
            dataset_key = 'trend interpolation'
            data_sources = 'interpolated'
        else:
            dataset_key = 'Source-receptor'
            data_sources = 'EMEP SR tables'
            
        # Hent basisverdi fra Kolonne D (4) -> Indeks 3 og gjør om fra 100 tN til ktN  
        base_value = float(df_rw.iloc[r, 3]) / 10  
        
        # --- STØYLOGIKK ---
        has_noise = dataset_noise and dataset_key in dataset_noise
        
        if dataset_noise and not has_noise and not hasattr(_add_rw_outflow_rdn_mc, f"warned_{dataset_key}"):
            print(f"  [ALARM] Ingen gyldig usikkerhet funnet for '{dataset_key}' i dataset_uncertainties!")
            print(f"          Kjører deterministisk (støy = 0) for denne strømmen inntil Excel oppdateres.")
            setattr(_add_rw_outflow_rdn_mc, f"warned_{dataset_key}", True)
            
        if has_noise:
            noise_info = dataset_noise[dataset_key]
            noise_val = noise_info['value']
            unc_type = noise_info['type']
            
            if unc_type == 'perc':
                value = base_value * noise_val
            else:
                if noise_val >= 0:
                    value = base_value + (noise_val * noise_info['upp_bound'])
                else:
                    value = base_value + (noise_val * noise_info['low_bound'])
        else:
            value = base_value
            
        if value < 0:
            value = 0.0
            
        results.append({
            'flow_name': flow_code,
            'year': year,
            'value': value, 
            'comment': comment,
            'data_sources': data_sources
        })
        
    missing_years = EXPECTED_YEARS - collected_years
    report_missing_years(flow_code, missing_years, results)