# report_generator.py
import os
import shutil
from datetime import datetime
from pybtex.database import parse_file

def generate_github_pages_report(plot_dir='output_files/plots', output_filename='index.md', bib_filename='library.bib'):
    if not os.path.exists(plot_dir):
        print(f"[INFO] Fant ikke mappen '{plot_dir}'. Rapporten ble ikke laget.")
        return

    plot_files = sorted([f for f in os.listdir(plot_dir) if f.endswith('.png')])
    if not plot_files:
        print(f"[INFO] Ingen plot-filer funnet i '{plot_dir}'.")
        return

    # Generer gjeldende dato for automatisk tidsstempling på forsiden
    current_date_str = datetime.now().strftime("%B %d, %Y")

    print("[RAPPORT] Sletter gamle midlertidige filer fra rotmappen for å unngå rot...")
    for f_old in os.listdir('.'):
        if (f_old.startswith("flow_") or f_old.startswith("pool_")) and f_old.endswith(".md"):
            os.remove(f_old)

    print("[RAPPORT] Bygger hierarkisk dokumentasjonsportal med egne pool-mapper...")

    # Felles tekstblokk for atmosfærisk deposisjon
    deposition_text = (
        "Atmospheric deposition was calculated using data from NILU which gives gridded "
        "deposition data for both oxidized and reduced N as averages for periods 1983-1987, "
        "1988-1992, 1997-2001, 2002-2006, 2007-2011 and 2012-2016. For 2017-2021 we use "
        "total NILU data for that period and scale with the distribution across land classes "
        "for the previous period. Values after 2021 are extrapolated. To find deposition on "
        "different land categories we use the map resource AR5 from NIBIO [^nibio_ar5_2016]. "
        "We find the total value of atmospheric deposition to the Norwegian mainland is, "
        "as given by NILU, 142 ktN in 2012-2016.\n\n"
        "As noted, our value for agricultural soils is much larger than given by FAOSTAT. "
        "Hohmann-Marriott (2025) used values from Blake et al. (2023) to arrive at an average "
        "N deposition rate of 80.85 ktN for the period 2017-2021. Hohmann-Marriott (2025) "
        "also reported values of 74.7 and 33.5 ktN per year using two different methods "
        "for estimating biome-dependent N deposition rates."
    )

    # ========================================================
    # 1. GENERER HOVEDLANDINGSSIDEN (index.md) - MED ADVARSEL
    # ========================================================
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Home\n")
        f.write("nav_order: 1\n")
        f.write("---\n\n")
        
        f.write("# Nitrogen Budget for Norway\n\n")
        f.write(f"**Last Updated:** {current_date_str}\n\n")
        
        f.write("{: .label .label-red }\n")
        f.write("Work in Progress\n\n")
        f.write("> **CRITICAL WARNING:** This project, including all underlying code, data parameterizations, ")
        f.write("and simulation results, is currently **under active development**. It is not yet validated or finalized. ")
        f.write("Using, copying, or relying on any part of this code or these results for research, decision-making, ")
        f.write("or any other application is **strongly discouraged** at this stage.\n\n")
        
        f.write("---\n\n")
        f.write("### Project Overview\n")
        f.write("Welcome to the interactive data and documentation portal for the Norwegian national nitrogen budget. ")
        f.write("This platform visualizes and centralizes the outputs from our Monte Carlo uncertainty analysis simulations.\n\n")
        f.write("Use the navigation menu on the left side to explore the individual nitrogen pools ")
        f.write("(e.g., Agriculture, Atmosphere, Rest of the World) and access detailed statistical time-series graphs, ")
        f.write("methodological explanations, and parameterizations for each specific flow.\n")

    # Hjelpefunksjon for å legge til BibTeX-referanser i bunnen av filene
    def append_bibtex_references(file_handle):
        file_handle.write("\n### References\n\n")
        if os.path.exists(bib_filename):
            try:
                bib_data = parse_file(bib_filename)
                for key, entry in bib_data.entries.items():
                    authors = entry.persons.get('author', [])
                    author_str = ", ".join([str(a) for a in authors]) if authors else "Unknown Author"
                    
                    year = entry.fields.get('year', 'n.d.')
                    title = entry.fields.get('title', 'No title').replace('{', '').replace('}', '')
                    journal = entry.fields.get('journal', entry.fields.get('publisher', entry.fields.get('booktitle', '')))
                    volume = entry.fields.get('volume', '')
                    pages = entry.fields.get('pages', '')
                    
                    pub_details = f" *{journal}*" if journal else ""
                    if volume: pub_details += f" {volume}"
                    if pages: pub_details += f", pp. {pages}"
                    
                    file_handle.write(f"[^{key}]: {author_str} ({year}). *{title}*.{pub_details}.\n")
            except Exception as e:
                file_handle.write(f"*Error parsing BibTeX file:* `{str(e)}`\n")
        else:
            file_handle.write(f"*Reference file '{bib_filename}' not found in root directory.*\n")

    # ========================================================
    # 2. OPPRETT UNDERMAPPE FOR ATMOSPHERE POOL OG GENERER FILER
    # ========================================================
    at_folder = "atmosphere_pool"
    os.makedirs(at_folder, exist_ok=True)

    with open(os.path.join(at_folder, "pool_atmosphere.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Atmosphere (AT)\n")
        f.write("nav_order: 2\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Pool: Atmosphere (AT)\n\n")
        f.write("This section contains all documented nitrogen flows leaving the Atmosphere pool.\n")

    menu_counter = 1
    for filename in plot_files:
        if not filename.startswith("AT_AT_"):
            continue

        flow_file_name = f"flow_{filename.replace('.png', '')}.md"
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')
        full_flow_path = os.path.join(at_folder, flow_file_name)

        exact_flow_code, display_name = "AT.AT-Unknown-Flow", "Unknown Atmospheric Flow"
        
        if "agsm" in norm and "fixation" in norm: exact_flow_code, display_name = "AT.AT-AG.SM-Biological N2 fixation-N2", "Biological N2 Fixation (Agricultural Soils)"
        elif "agsm" in norm and "deposition" in norm and "oxn" in norm: exact_flow_code, display_name = "AT.AT-AG.SM-Deposition-OXN", "Oxidized N Deposition (Agricultural Soils)"
        elif "agsm" in norm and "deposition" in norm and "rdn" in norm: exact_flow_code, display_name = "AT.AT-AG.SM-Deposition-RDN", "Reduced N Deposition (Agricultural Soils)"
        elif "fsfo" in norm and "fixation" in norm: exact_flow_code, display_name = "AT.AT-FS.FO-N2 fixation-N2", "N2 Fixation (Forest)"
        elif "fsfo" in norm and "deposition" in norm and "oxn" in norm: exact_flow_code, display_name = "AT.AT-FS.FO-Deposition-OXN", "Oxidized N Deposition (Forest)"
        elif "fsfo" in norm and "deposition" in norm and "rdn" in norm: exact_flow_code, display_name = "AT.AT-FS.FO-Deposition-RDN", "Reduced N Deposition (Forest)"
        elif "fsol" in norm and "fixation" in norm: exact_flow_code, display_name = "AT.AT-FS.OL-Biological N2 fixation-N2", "Biological N2 Fixation (Other Land)"
        elif "fsol" in norm and "deposition" in norm and "oxn" in norm: exact_flow_code, display_name = "AT.AT-FS.OL-Deposition-OXN", "Oxidized N Deposition (Other Land)"
        elif "fsol" in norm and "deposition" in norm and "rdn" in norm: exact_flow_code, display_name = "AT.AT-FS.OL-Deposition-RDN", "Reduced N Deposition (Other Land)"
        elif "hshs" in norm and "deposition" in norm and "oxn" in norm: exact_flow_code, display_name = "AT.AT-HS.HS-Deposition-OXN", "Oxidized N Deposition (Settlements)"
        elif "hshs" in norm and "deposition" in norm and "rdn" in norm: exact_flow_code, display_name = "AT.AT-HS.HS-Deposition-RDN", "Reduced N Deposition (Settlements)"
        elif "hysw" in norm and "deposition" in norm and "oxn" in norm: exact_flow_code, display_name = "AT.AT-HY.SW-Deposition-OXN", "Oxidized N Deposition (Surface Water)"
        elif "hysw" in norm and "deposition" in norm and "rdn" in norm: exact_flow_code, display_name = "AT.AT-HY.SW-Deposition-RDN", "Reduced N Deposition (Surface Water)"
        elif "hysw" in norm and "fixation" in norm: exact_flow_code, display_name = "AT.AT-HY.SW-N2 fixation-N2", "N2 Fixation (Surface Water)"
        elif "mpop" in norm and "synthesis" in norm: exact_flow_code, display_name = "AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2", "Ammonia Synthesis N2 Fixation"
        elif "rwrw" in norm and "outflow" in norm and "oxn" in norm: exact_flow_code, display_name = "AT.AT-RW.RW-Atmospheric outflow-OXN", "Atmospheric Outflow (Oxidized N)"
        elif "rwrw" in norm and "outflow" in norm and "rdn" in norm: exact_flow_code, display_name = "AT.AT-RW.RW-Atmospheric outflow-RDN", "Atmospheric Outflow (Reduced N)"

        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write("layout: default\n")
            f.write(f"title: {display_name}\n")
            f.write("parent: Atmosphere (AT)\n")
            f.write(f"nav_order: {menu_counter}\n")
            f.write("---\n\n")
            menu_counter += 1

            f.write(f"# {display_name}\n\n")
            f.write(f"![{exact_flow_code}](../{plot_dir}/{filename})\n\n")
            f.write("### Flow Description\n")

            if exact_flow_code == "AT.AT-AG.SM-Biological N2 fixation-N2":
                f.write("**AT.AT-AG.SM-Biological N2 fixation-N2**\n\n[^schappi_annexes_2025] advises using data from the EUROSTAT Gross nutrient balance...")
            elif exact_flow_code in ["AT.AT-AG.SM-Deposition-OXN", "AT.AT-AG.SM-Deposition-RDN", "AT.AT-FS.FO-Deposition-OXN", "AT.AT-FS.FO-Deposition-RDN", "AT.AT-FS.OL-Deposition-OXN", "AT.AT-FS.OL-Deposition-RDN", "AT.AT-HS.HS-Deposition-OXN", "AT.AT-HS.HS-Deposition-RDN", "AT.AT-HY.SW-Deposition-RDN"]:
                f.write(f"**{exact_flow_code}**\n\n" + deposition_text + "\n\n")
            elif exact_flow_code == "AT.AT-HY.SW-Deposition-OXN":
                f.write("**AT.AT-HY.SW-Deposition-OXN**\n\n" + deposition_text + "\n\nFor comparison, the data used in the TEOTIL model...")
            else:
                f.write(f"*Flow details for {exact_flow_code}*\n\n")

            append_bibtex_references(f)

    # ========================================================
    # 3. OPPRETT UNDERMAPPE FOR REST OF THE WORLD (RW) POOL
    # ========================================================
    rw_folder = "rest_of_the_world_pool"
    os.makedirs(rw_folder, exist_ok=True)

    with open(os.path.join(rw_folder, "pool_rest_of_the_world.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Rest of the world (RW)\n")
        f.write("nav_order: 3\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Pool: Rest of the world (RW)\n\n")
        f.write("This section contains all documented nitrogen inflows and transfers originating from the Rest of the world (RW) pool. ")
        f.write("Click on the individual sub-flows in the left-hand menu to view graphs and methodological explanations.\n\n")
        f.write("### Flows that are zero or neglected:\n\n")
        f.write("* **RW.RW-MP.FP-Sea fish (landings)-Nmix** is set to zero because all wild fish catch is accounted for under HY.\n")
        f.write("* **RW.RW-AG.SM-Manure import-Nmix** is assumed small and neglected as advised by Schäppi (2025) [^schappi_annexes_2025].\n")
        f.write("* **RW.RW-HY.SW-Import of surface water-Nmix** are assumed negligible due to Norwegian topography.\n")

    rw_menu_counter = 1
    for filename in plot_files:
        if not filename.startswith("RW_RW_"):
            continue

        flow_file_name = f"flow_{filename.replace('.png', '')}.md"
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')
        full_flow_path = os.path.join(rw_folder, flow_file_name)

        exact_flow_code = "RW.RW-Unknown-Flow"
        description = ""

        if "feed" in norm and "aquaculture" in norm:
            exact_flow_code = "RW.RW-HY.AC-Aquaculture feed import-Nmix"
            display_name = "Aquaculture Feed Import"
            description = (
                "The flow **RW.RW-HY.AC-Aquaculture feed import-Nmix** has been added to account for the substantial "
                "import of feed to aquaculture. We assume a constant import fraction of 0.92 as given by Aas et al. (2022) [^aas_utilization_2022] "
                "for the year 2020. The amount of feed used is based on the amount of fish produced, calculated using data from "
                "Fiskeridirektoratet [^fiskeridirektoratet_06002_2025] on sold farmed fish, assuming average protein (N) retention of 35.75% "
                "([^aas_utilization_2022]), 2.8% nitrogen content in fish and shellfish (Schäppi (2025) [^schappi_annexes_2025], p. 254) "
                "and 3% feed waste (Wang et al., 2013 [^wang_chemical_2013])."
            )
        elif "feed" in norm and "animal" in norm:
            exact_flow_code = "RW.RW-AG.MM-Animal feed import-Nmix"
            display_name = "Animal Feed Import"
            description = (
                "Data on imported animal feed is taken from Landbruksdirektoratet [^landbruksdirektoratet_kraftforstatistikk_2025] and we have used the detailed "
                "composition of animal feed given in Eidem & Ruud (2022) [^eidem_for-_2022] together with protein contents from FAO (2021) [^fao_annex_2021] "
                "and specific Jones factors from FAO (2023) [^fao_chapter_2023] to get nitrogen contents. Based on the Landbruksdirektoratet data, "
                "the N content of the total amount of feed is 0.02 kgN/kg feed. NIBIO Totalkalkylen [^nibio_totalkalkylen_2025] gives statistics for "
                "total amount of feed to Norwegian farm animals between 1959 and 2026. Table 6.10 in Bruholt & Longva (1994) [^bruholt_jordbruksstatistikk_1994] "
                "gives the domestically produced fraction of farm animal feed between 1985 and 1994. We combine these data to find values "
                "before 2000, using an average import fraction for 1995-1999."
            )
        elif "live" in norm and "animal" in norm:
            exact_flow_code = "RW.RW-AG.MM-Live animal import-Nmix"
            display_name = "Live Animal Import"
            description = (
                "Is taken from FAOSTAT Crops and livestock products [^faostat_crops_2025], assuming typical weights of animals from various sources, "
                "average 16% protein in whole animal and Jones factor 6.25 for nitrogen to protein (standard)."
            )
        elif "mineral" in norm and "fertilizer" in norm:
            exact_flow_code = "RW.RW-AG.SM-Mineral fertilizer import-Nmix"
            display_name = "Mineral Fertilizer Import"
            description = (
                "Is taken from FAOSTAT Fertilizer by nutrient (FAO, 2025) [^fao_fertilizer_2025]. Because anhydrous ammonia is not used directly "
                "as fertilizer in Norway, it is not counted as a fertilizer in this particular FAO statistic. We therefore include NH3 import "
                "in the flow **RW.RW-MP.OP-Other goods import-Nmix**."
            )
        elif "inflow" in norm and "oxn" in norm:
            exact_flow_code = "RW.RW-AT.AT-Atmospheric inflow-OXN"
            display_name = "Atmospheric Inflow (Oxidized N)"
            description = (
                "Is found from source-receptor data from EMEP [^emep_sr_2024], as advised by Schäppi (2025) [^schappi_annexes_2025]. There is a change "
                "in methodology in the EMEP reporting between 2002 and 2003 data."
            )
        elif "inflow" in norm and "rdn" in norm:
            exact_flow_code = "RW.RW-AT.AT-Atmospheric inflow-RDN"
            display_name = "Atmospheric Inflow (Reduced N)"
            description = (
                "Is found from source-receptor data from EMEP [^emep_sr_2024], as advised by Schäppi (2025) [^schappi_annexes_2025]. There is a change "
                "in methodology in the EMEP reporting between 2002 and 2003 data."
            )
        elif "fuel" in norm and "import" in norm and "transport" not in norm:
            exact_flow_code = "RW.RW-EF.EC-Fuel import-Nmix"
            display_name = "Fuel Import"
            description = "Is taken from trade data, SSB table 08801 for all fuel items except those for transport."
        elif "transport" in norm and "fuel" in norm:
            exact_flow_code = "RW.RW-EF.TR-Import of transport fuel-Nmix"
            display_name = "Transport Fuel Import"
            description = "Is taken from trade data, SSB table 08801 for all fuel items for transport."
        elif "food" in norm and "import" in norm:
            exact_flow_code = "RW.RW-MP.FP-Food import-Nmix"
            display_name = "Food Import"
            description = "Is taken from trade data, SSB table 08801. The HS codes and associated nitrogen contents used are found in supplementary file."
        elif "ammonia" in norm and "import" in norm:
            exact_flow_code = "RW.RW-MP.OP-Ammonia import-Nmix"
            display_name = "Ammonia Import"
            description = "Is taken from trade data, SSB table 08801."
        elif "other" in norm and "goods" in norm:
            exact_flow_code = "RW.RW-MP.OP-Other goods import-Nmix"
            display_name = "Other Goods Import"
            description = (
                "Is taken from trade data, SSB table 08801. Import of N2 is a large contributor but not included here "
                "because it does not contribute to the reactive nitrogen cycle."
            )
        elif "solid" in norm and "waste" in norm:
            exact_flow_code = "RW.RW-PR.SO-Solid waste import-Nmix"
            display_name = "Solid Waste Import"
            description = (
                "Is taken from trade data, SSB table 08801. We include imports of municipal waste, wastewater sludge, "
                "hazardous waste, plastic, paper and textile waste."
            )
            
        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write("layout: default\n")
            f.write(f"title: {display_name}\n")
            f.write("parent: Rest of the world (RW)\n")
            f.write(f"nav_order: {rw_menu_counter}\n")
            f.write("---\n\n")
            rw_menu_counter += 1

            f.write(f"# {display_name}\n\n")
            f.write(f"![{exact_flow_code}](../{plot_dir}/{filename})\n\n")
            f.write("### Flow Description\n")
            if description:
                f.write(f"{description}\n\n")
            else:
                f.write(f"*Flow details detected for file: `{filename}`.*\n\n")

            append_bibtex_references(f)

# ========================================================
    # 4. OPPRETT HIERARKISK PORTAL FOR AGRICULTURE (AG) POOL
    # ========================================================
    ag_folder = "agriculture_pool"
    os.makedirs(ag_folder, exist_ok=True)

    # 4a. Hovedside for Agriculture (Grandparent)
    with open(os.path.join(ag_folder, "pool_agriculture.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Agriculture (AG)\n") # <--- Dette er Grandparent-tittelen
        f.write("nav_order: 4\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Pool: Agriculture (AG)\n\n")
        f.write("Because biofuel production in Norway is typically done as part of the waste management sector, ")
        f.write("flows of agricultural wastes to biofuel production are directed to PR.SO and we do not include the subpool AG.BC.\n\n")
        f.write("This pool is divided into two operational sub-pools. Explore them using the side menu or links below:\n\n")
        f.write("* [Manure Management (AG.MM)](subpool_manure_management.html)\n")
        f.write("* [Soil Management (AG.SM)](subpool_soil_management.html)\n")

    # 4b. Sub-hovedside for Manure Management (Parent 1)
    with open(os.path.join(ag_folder, "subpool_manure_management.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Manure Management (AG.MM)\n") # <--- Denne må matche 'parent' under eksakt
        f.write("parent: Agriculture (AG)\n")
        f.write("nav_order: 1\n")
        f.write("has_children: true\n") # <--- VIKTIG: Denne må være true for å vise plottene
        f.write("---\n\n")
        f.write("# Subpool: Manure management, storage and animal husbandry (AG.MM)\n\n")
        f.write("### Flows that are zero or neglected:\n\n")
        f.write("* **AG.MM-RW.RW-Manure export-Nmix** is assumed small and neglected.\n")

    # 4c. Sub-hovedside for Soil Management (Parent 2)
    with open(os.path.join(ag_folder, "subpool_soil_management.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Soil Management (AG.SM)\n") # <--- Denne må matche 'parent' under eksakt
        f.write("parent: Agriculture (AG)\n")
        f.write("nav_order: 2\n")
        f.write("has_children: true\n") # <--- VIKTIG: Denne må være true for å vise plottene
        f.write("---\n\n")
        f.write("# Subpool: Soil management (AG.SM)\n\n")
        f.write("### Flows that are zero or neglected:\n\n")
        f.write("* **AG.SM-HY.SW-Overland flow-Nmix** is not included because all runoff and leaching is included in Leaching.\n")

# 4d. Sorter og generer filer for aktive flomplot under AG
    ag_mm_counter = 1
    ag_sm_counter = 1

    for filename in plot_files:
        # Siden filnavnene starter med understrek: AG_MM_... eller AG_SM_...
        if not (filename.upper().startswith("AG_MM_") or filename.upper().startswith("AG_SM_")):
            continue

        # Lag markdown-filnavn ved å fjerne .png/.PNG trygt
        base_name = filename.rsplit('.', 1)[0]
        flow_file_name = f"flow_{base_name}.md"
        full_flow_path = os.path.join(ag_folder, flow_file_name)

        # Lag en "vasket" versjon for å sjekke unike nøkkelord i resten av filnavnet
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')

        exact_flow_code = "AG-Unknown-Flow"
        display_name = "Unknown Agricultural Flow"
        parent_subpool = ""
        description = ""

        # MAPPING FOR MANURE MANAGEMENT (AG.MM)
        if filename.upper().startswith("AG_MM_"):
            parent_subpool = "Manure Management (AG.MM)"
            if "application" in norm:
                exact_flow_code = "AG.MM-AG.SM-Manure application-Nmix"
                display_name = "Manure Application"
                description = "Taken from EUROSTAT Gross nutrient balance as advised by Schäppi (2025) [^schappi_annexes_2025]. We interpolate the missing values between 2016 and 2020."
            elif "n2o" in norm:
                exact_flow_code = "AG.MM-AT.AT-Emissions-N2O"
                display_name = "Manure Emissions (N2O)"
                description = "Taken from UNFCCC Common reporting tables, Table 3."
            elif "nh3" in norm:
                exact_flow_code = "AG.MM-AT.AT-Emissions-NH3"
                display_name = "Manure Emissions (NH3)"
                description = "We have used data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by Schäppi (2025) [^schappi_annexes_2025], using the categories given in Table 29."
            elif "nox" in norm:
                exact_flow_code = "AG.MM-AT.AT-Emissions-NOx"
                display_name = "Manure Emissions (NOx)"
                description = "We have used data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by Schäppi (2025) [^schappi_annexes_2025], using the categories given in Table 29."
            elif "leaching" in norm:
                exact_flow_code = "AG.MM-HY.SW-Leaching-Nmix"
                display_name = "Manure Leaching"
                description = "Taken from UNFCCC Common reporting tables, Table 3."
            elif "product" in norm and "nonedible" not in norm and "op" not in norm:
                exact_flow_code = "AG.MM-MP.FP-Animal products-Nmix"
                display_name = "Animal Products"
                description = "Taken from FAOSTAT Crops and livestock products, with N contents taken from Schäppi (2025) [^schappi_annexes_2025]."
            elif "nonedible" in norm or "wool" in norm or ("animal" in norm and "op" in norm):
                exact_flow_code = "AG.MM-MP.OP-Non-edible animal products-Nmix"
                display_name = "Non-edible Animal Products"
                description = "Schäppi (2025) [^schappi_annexes_2025] advises using FAOSTAT Commodity Balances (non-food). For Norway this statistic only contains wool for 4 individual years and we therefore use data for wool from Landbruksdirektoratet (2025c) for 2005-2024; for earlier years, we use the number of sheep (SSB table 03710) and extrapolate from a linear regression found between sheep and wool for 2005-2024. In addition, we use numbers for raw hides and skins from FAOSTAT Crops and livestock products. N contents are taken from Schäppi (2025) [^schappi_annexes_2025]."
            elif "export" in norm or "live" in norm:
                exact_flow_code = "AG.MM-RW.RW-Live animal export-Nmix"
                display_name = "Live Animal Export"
                description = "Taken from FAOSTAT Crop and livestock products, assuming typical weights of animals from various sources, average 13 % protein in whole animal from FAO (FAO, 1953) and Jones factor 6.25 for nitrogen to protein (standard)."

        # MAPPING FOR SOIL MANAGEMENT (AG.SM)
        elif filename.upper().startswith("AG_SM_"):
            parent_subpool = "Soil Management (AG.SM)"
            if "fodder" in norm or "grass" in norm:
                exact_flow_code = "AG.SM-AG.MM-Fodder crops-Nmix"
                display_name = "Fodder Crops Production"
                description = "We have used data for grass and fodder production from SSB table 13648 «Avling i jordbruket (1000 tonn) og avling per dekar (kg), etter ymse jordbruksvekstar (F) 2021 – 2024» and 05772 «Avling i jordbruket, etter ymse jordbruksvekstar (1 000 tonn) (F) (avslutta serie) 2000 – 2020». Values prior to 2000 are found in the SSB Jordbruksstatistikk (Table 2.1/Table 20). The protein content of grass and fodder is known to be highly variable. We have assumed a protein content of 15 % based on 2025 analyses of 13 000 grass samples from all over Norway by Tine/NorFor, and 15 % N in protein (FAO, 2003).\n\nHohmann-Marriott (2025) used similar data sources but arrived at a smaller N flow (40- 45 ktN) using a protein content of 8 % and N content in protein of 15 % (Table S2)."
            elif "n2" in norm and "n2o" not in norm:
                exact_flow_code = "AG.SM-AT.AT-Emissions-N2"
                display_name = "Soil Emissions (N2 Denitrification)"
                description = "Schäppi (2025) [^schappi_annexes_2025] recommends using a value of 14 kgN/ha/year for denitrification if no other data are available. Together with a total agricultural area of 1 132 693 ha (NIBIO, 2026) this gives around 16 ktN/year."
            elif "n2o" in norm:
                exact_flow_code = "AG.SM-AT.AT-Emissions-N2O"
                display_name = "Soil Emissions (N2O)"
                description = "Taken from UNFCCC Common reporting tables, Table 3."
            elif "nh3" in norm:
                exact_flow_code = "AG.SM-AT.AT-Emissions-NH3"
                display_name = "Soil Emissions (NH3)"
                description = "We have used data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by Schäppi (2025) [^schappi_annexes_2025], using the categories given in Table 30."
            elif "nox" in norm:
                exact_flow_code = "AG.SM-AT.AT-Emissions-NOx"
                display_name = "Soil Emissions (NOx)"
                description = "We have used data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by Schäppi (2025) [^schappi_annexes_2025], using the categories given in Table 30."
            elif "leaching" in norm:
                exact_flow_code = "AG.SM-HY.SW-Leaching-Nmix"
                display_name = "Soil Leaching"
                description = "Taken from UNFCCC Common reporting tables, Table 3. The data agrees within the error range with what is reported in the TEOTIL3 model (Sample et al., 2024)."
            elif "food" in norm or "crop" in norm:
                exact_flow_code = "AG.SM-MP.FP-Food crop products-Nmix"
                display_name = "Food Crop Products"
                description = "Taken from EUROSTAT Gross nutrient balance as advised by Schäppi (2025) [^schappi_annexes_2025]: «Nutrient removal by harvest of crops» minus «Industrial crops». «Ornamental crops», which should also be removed, are negligible in Norway. For years with missing data, we have filled in the average of all other years."
            elif "industrial" in norm or "use" in norm or ("crop" in norm and "op" in norm):
                exact_flow_code = "AG.SM-MP.OP-Crop products for industrial use-Nmix"
                display_name = "Crop Products Use"
                description = "Taken from EUROSTAT Gross nutrient balance as advised by Schäppi (2025) [^schappi_annexes_2025]. For years with missing data, we have filled in the average of all other years."

        # Generer filen dersom den ble matchet
        if parent_subpool:
            with open(full_flow_path, 'w', encoding='utf-8') as f:
                f.write("---\n")
                f.write("layout: default\n")
                f.write(f"title: {display_name}\n")
                f.write(f"parent: {parent_subpool}\n")
                f.write(f"grand_parent: Agriculture (AG)\n")
                
                if filename.upper().startswith("AG_MM_"):
                    f.write(f"nav_order: {ag_mm_counter}\n")
                    ag_mm_counter += 1
                else:
                    f.write(f"nav_order: {ag_sm_counter}\n")
                    ag_sm_counter += 1
                    
                f.write("---\n\n")
                f.write(f"# {display_name}\n\n")
                f.write(f"![{exact_flow_code}](../{plot_dir}/{filename})\n\n")
                f.write("### Flow Description\n")
                if description:
                    f.write(f"{description}\n\n")
                else:
                    f.write(f"*Flow details detected for agricultural file: `{filename}`.*\n\n")

                append_bibtex_references(f)                
    print(f"[SUKSESS] Portalen er oppdatert med det dype hierarkiet for Agriculture (AG.MM og AG.SM)!")