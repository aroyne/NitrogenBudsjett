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
        if (f_old.startswith("flow_") or f_old.startswith("pool_") or f_old.startswith("subpool_")) and f_old.endswith(".md"):
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

    # HELPEFUNKSJON: Sjekker om et spesifikt balanseplott eksisterer
    def get_balance_image_markdown(pool_code, relative_depth=""):
        """Returnerer bilde-markdown hvis balanseplottet eksisterer, ellers tom streng."""
        balance_file = f"balance_{pool_code.replace('.', '_')}.png"
        if balance_file in plot_files:
            return (
                f"\n---\n\n"
                f"## Mass Balance Overview (1990-2023)\n\n"
                f"The chart below illustrates the integrated nitrogen mass balance for **{pool_code}**. "
                f"It includes total system inflows (positive stack), total outflows (negative stack), "
                f"and the net balance line with estimated uncertainty bounds (±1σ).\n\n"
                f"![Mass Balance {pool_code}]({relative_depth}{plot_dir}/{balance_file})\n"
            )
        return ""

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
        f.write("(e.g., Forests and Semi-natural Vegetation, Agriculture, Atmosphere, Hydrosphere, Rest of the World) ")
        f.write("and access detailed statistical time-series graphs, methodological explanations, and parameterizations for each specific flow.\n")

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
        
        f.write(get_balance_image_markdown("AT", relative_depth="../"))

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
        
        f.write(get_balance_image_markdown("RW", relative_depth="../"))
        
        f.write("\n### Flows that are zero or neglected:\n\n")
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

    with open(os.path.join(ag_folder, "pool_agriculture.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Agriculture (AG)\n")
        f.write("nav_order: 4\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Pool: Agriculture (AG)\n\n")
        f.write("Because biofuel production in Norway is typically done as part of the waste management sector, ")
        f.write("flows of agricultural wastes to biofuel production are directed to PR.SO and we do not include the subpool AG.BC.\n\n")
        f.write("This pool is divided into two operational sub-pools. Explore them using the side menu or links below:\n\n")
        f.write("* [Manure Management (AG.MM)](subpool_manure_management.html)\n")
        f.write("* [Soil Management (AG.SM)](subpool_soil_management.html)\n")
        
        f.write(get_balance_image_markdown("AG", relative_depth="../"))

    with open(os.path.join(ag_folder, "subpool_manure_management.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Manure Management (AG.MM)\n")
        f.write("parent: Agriculture (AG)\n")
        f.write("nav_order: 1\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Manure management, storage and animal husbandry (AG.MM)\n\n")
        
        f.write(get_balance_image_markdown("AG.MM", relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **AG.MM-RW.RW-Manure export-Nmix** is assumed small and neglected.\n")

    with open(os.path.join(ag_folder, "subpool_soil_management.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Soil Management (AG.SM)\n")
        f.write("parent: Agriculture (AG)\n")
        f.write("nav_order: 2\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Soil management (AG.SM)\n\n")
        
        f.write(get_balance_image_markdown("AG.SM", relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **AG.SM-HY.SW-Overland flow-Nmix** is not included because all runoff and leaching is included in Leaching.\n")

    ag_mm_counter = 1
    ag_sm_counter = 1

    for filename in plot_files:
        if not (filename.upper().startswith("AG_MM_") or filename.upper().startswith("AG_SM_")):
            continue

        base_name = filename.rsplit('.', 1)[0]
        flow_file_name = f"flow_{base_name}.md"
        full_flow_path = os.path.join(ag_folder, flow_file_name)
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')

        exact_flow_code = "AG-Unknown-Flow"
        display_name = "Unknown Agricultural Flow"
        parent_subpool = ""
        description = ""

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
                description = "Schäppi (2025) [^schappi_annexes_2025] advises using FAOSTAT Commodity Balances (non-food)..."
            elif "export" in norm or "live" in norm:
                exact_flow_code = "AG.MM-RW.RW-Live animal export-Nmix"
                display_name = "Live Animal Export"
                description = "Taken from FAOSTAT Crop and livestock products, assuming typical weights..."

        elif filename.upper().startswith("AG_SM_"):
            parent_subpool = "Soil Management (AG.SM)"
            if "fodder" in norm or "grass" in norm:
                exact_flow_code = "AG.SM-AG.MM-Fodder crops-Nmix"
                display_name = "Fodder Crops Production"
                description = "We have used data for grass and fodder production..."

        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write("layout: default\n")
            f.write(f"title: {display_name}\n")
            f.write(f"parent: {parent_subpool}\n")
            f.write(f"nav_order: {ag_mm_counter if 'MM' in parent_subpool else ag_sm_counter}\n")
            f.write("---\n\n")
            if 'MM' in parent_subpool: ag_mm_counter += 1
            else: ag_sm_counter += 1

            f.write(f"# {display_name}\n\n")
            f.write(f"![{exact_flow_code}](../{plot_dir}/{filename})\n\n")
            f.write("### Flow Description\n")
            f.write(f"{description}\n\n")
            append_bibtex_references(f)

    # ========================================================
    # 5. OPPRETT HIERARKISK PORTAL FOR FORESTS AND SEMI-NATURAL VEGETATION (FS) POOL
    # ========================================================
    fs_folder = "forests_and_semi_natural_pool"
    os.makedirs(fs_folder, exist_ok=True)

    # 5a. Hovedside for Forests and semi-natural vegetation (Grandparent)
    with open(os.path.join(fs_folder, "pool_forests_and_semi_natural.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Forests and semi-natural vegetation (FS)\n")
        f.write("nav_order: 5\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Pool: Forests and semi-natural vegetation (FS)\n\n")
        f.write("Because of limited data on OL and because data on leaching are combined for WL and OL, ")
        f.write("we have chosen to combine WL and OL into the OL subpool in this study.\n\n")
        f.write("We have considered including meat from hunting of wild animals in flows from this subpool, but chosen not to. ")
        f.write("According to (Steinset, 2021), the amount of wild game caught in 2019 was around 6000 tonnes, ")
        f.write("which gives around 0.2 ktN and thus smaller than any of the included flows.\n\n")
        f.write("This pool is divided into two operational sub-pools. Explore them using the side menu or links below:\n\n")
        f.write("* [Forests (FS.FO)](subpool_forests.html)\n")
        f.write("* [Other Land (FS.OL)](subpool_other_land.html)\n")
        
        f.write(get_balance_image_markdown("FS", relative_depth="../"))

    # 5b. Sub-hovedside for Forests (FS.FO) (Parent 1)
    with open(os.path.join(fs_folder, "subpool_forests.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Forests (FS.FO)\n")
        f.write("parent: Forests and semi-natural vegetation (FS)\n")
        f.write("nav_order: 1\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Forests (FS.FO)\n\n")
        
        f.write(get_balance_image_markdown("FS.FO", relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **FS.FO-AT.AT-Emissions-NOx** is neglected because no values are reported in the CRLTAP/WebDab categories 4A1 and 4A2 (forest soils).\n")
        f.write("* **FS.FO-EF.EC-Fuel wood for co-fired power plants-Nmix** is set to zero because we assume such facilities do not exist in Norway.\n")
        f.write("* **FS.FO-EF.IC-Fuel wood for industry-Nmix** is ignored because wood is typically not harvested specifically to be used for fuel in industry in Norway. The use of wood waste in the producing industry is reported as self-produced bioenergy in the SSB statistic, but this is a flow that goes from MP.OP to EF.IC.\n")
        f.write("* Because the N-flow in forest fertilization is not large, we have chosen to ignore the associated N2O emissions that were included in the Swedish NBB (Moldan et al., 2025).\n")

    # 5c. Sub-hovedside for Other Land (FS.OL) (Parent 2)
    with open(os.path.join(fs_folder, "subpool_other_land.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Other Land (FS.OL)\n")
        f.write("parent: Forests and semi-natural vegetation (FS)\n")
        f.write("nav_order: 2\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Other land (FS.OL)\n\n")
        
        f.write(get_balance_image_markdown("FS.OL", relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **FS.OL-AT.AT-Emissions-NOx** is neglected because no values are reported in the CRLTAP/WebDab categories 4F1 and 4F2 (wetlands / other land NOx).\n")

    fs_fo_counter = 1
    fs_ol_counter = 1

    for filename in plot_files:
        if not (filename.upper().startswith("FS_FO_") or filename.upper().startswith("FS_OL_")):
            continue

        base_name = filename.rsplit('.', 1)[0]
        flow_file_name = f"flow_{base_name}.md"
        full_flow_path = os.path.join(fs_folder, flow_file_name)
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')

        exact_flow_code = "FS-Unknown-Flow"
        display_name = "Unknown Forestry Flow"
        parent_subpool = ""
        description = ""

        if filename.upper().startswith("FS_FO_"):
            parent_subpool = "Forests (FS.FO)"
            if "emissionsn2" in norm and "n2o" not in norm:
                exact_flow_code = "FS.FO-AT.AT-Emissions-N2"
                display_name = "Forest Emissions (N2)"
                description = "Calculated based on N2O emissions from UNFCCC Common reporting tables, Table 4 and assuming a mean N2:N2O ratio of 19.5 as discussed in (Schäppi, 2025)."
            elif "emissionsn2o" in norm:
                exact_flow_code = "FS.FO-AT.AT-Emissions-N2O"
                display_name = "Forest Emissions (N2O)"
                description = "Taken from UNFCCC Common reporting tables, Table 4."
            elif "households" in norm or "fuelwood" in norm:
                exact_flow_code = "FS.FO-EF.OE-Fuel wood for households-Nmix"
                display_name = "Fuel Wood for Households"
                description = "Taken from SSB table 09702 'Energibalansen. Vedforbruk i boliger og fritidsboliger 1990 – 2024' and we assume a mean N content of 4.0 kg/t (between coniferous and non-coniferous wood; see FS.FO-MP.OP-Industrial round wood-Nmix)."
            elif "leaching" in norm:
                exact_flow_code = "FS.FO-HY.SW-Leaching-Nmix"
                display_name = "Forest Leaching"
                description = "Found in data supplied by NIVA, produced in the TEOTIL3 model (Sample et al., 2024). For the period 1990-2013, we have used TEOTIL data published by Miljødirektoratet for nitrogen from nitrogen flows that reach the coast, where we have found that values for leaching from forest in the period 2013-2023 are a fraction 0.59 of what is reported by Miljødirektoratet as «Bakgrunn», to within a 2% error."
            elif "roundwood" in norm or "industrial" in norm:
                exact_flow_code = "FS.FO-MP.OP-Industrial round wood-Nmix"
                display_name = "Industrial Round Wood"
                description = (
                    "Taken from FAOSTAT Forestry production and trade: industrial roundwood, which gives values under bark. "
                    "The values given here are very close to those reported in SSB table 08979 'Avvirkning for salg (1 000 m3) 1996 – 2024'. "
                    "We have also compared with data in Eurostat, which gives total amount of round removed (over or under bark) including use for firewood in households and industry. "
                    "Following the Swedish NBB (Moldan et al., 2025), we use an average wood density of 0.45 t/m3 for all wood categories, "
                    "and N-contents of 3.4 kg/t for coniferous and 4.3 kg/t for non-coniferous trees (ktN/mill m3 wood harvested).\n\n"
                #     "**Comparison & Discrepancies:**\n"
                #     "* For comparison, Moldan et al. (2025) found 36.4 ktN for industrial roundwood in 2015, or 2.3 times more than the flow we have found for Norway for the same year. In 2015 the FAOSTAT reported total value of industrial round wood is 6.6 times larger than that reported for Norway, so even though we have used the same parameters, they seem to end up with a smaller N content. *(Note: Ask Moldan regarding this reason)*\n"
                #     "* Hohmann-Marriott (2025) reports much larger values, with a total production of around 700 ktN for 2020, even though he used a lower N content (0.14 and 0.17 % N by weight for coniferous and noniferous wood, respectively) for a total amount of 120 million m3 of felled wood in 2020. In the statistics we use, table 08979 (the same as Hofmann used), the value is 10.242 million m3 for 2020. *(Note: Contact Hohmann to ask if he could have misread with a factor of 10 error? He reports using density values of 0.4 and 0.5 t/m3, which should have given the same result as what we got).* "
                 )

        elif filename.upper().startswith("FS_OL_"):
            parent_subpool = "Other Land (FS.OL)"
            if "grazing" in norm:
                exact_flow_code = "FS.OL-AG.MM-Grazing-Nmix"
                display_name = "Organised Grazing"
                description = (
                    "Calculated using data from NIBIO on organised grazing (NIBIO, 2025a) together with estimated fodder intake for different animal groups "
                    "taken from Table 1.2 in (Hegrenes & Asheim, 2006), assuming an average protein content of 150 g pr FEm and the standard Jones factor "
                    "for the nitrogen content of protein. *(Note: Check if this trend is a continuous increase, see file OBB_fylke... in data_files)*"
                )
            elif "emissionsn2" in norm and "n2o" not in norm:
                exact_flow_code = "FS.OL-AT.AT-Emissions-N2"
                display_name = "Other Land Emissions (N2)"
                description = "Calculated from N2O emissions from UNFCCC Common reporting tables, Table 4, assuming a mean N2:N2O ratio of 19.5 as has been calculated from studies of forest ecosystems, as discussed in (Schäppi, 2025)."
            elif "emissionsn2o" in norm:
                exact_flow_code = "FS.OL-AT.AT-Emissions-N2O"
                display_name = "Other Land Emissions (N2O)"
                description = "Taken from UNFCCC Common reporting tables, Table 4, where the only reported values are from wetlands."
            elif "leaching" in norm:
                exact_flow_code = "FS.OL-HY.SW-Leaching-Nmix"
                display_name = "Other Land Leaching"
                description = "Found in data supplied by NIVA, produced in the TEOTIL3 model (Sample et al., 2024), where it is aggregated with the value for WL. For the period 1990-2013, we have used TEOTIL data published by Miljødirektoratet for nitrogen from nitrogen flows that reach the coast, where we have found that values for leaching from forest in the period 2013-2023 are a fraction 0.42 of what is reported by Miljødirektoratet as «Bakgrunn», to within a 3 % error."

        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write("layout: default\n")
            f.write(f"title: {display_name}\n")
            f.write(f"parent: {parent_subpool}\n")
            f.write(f"nav_order: {fs_fo_counter if 'FO' in parent_subpool else fs_ol_counter}\n")
            f.write("---\n\n")
            if 'FO' in parent_subpool: fs_fo_counter += 1
            else: fs_ol_counter += 1

            f.write(f"# {display_name}\n\n")
            f.write(f"![{exact_flow_code}](../{plot_dir}/{filename})\n\n")
            f.write("### Flow Description\n")
            f.write(f"{description}\n\n")
            append_bibtex_references(f)

    # ========================================================
    # 6. OPPRETT HIERARKISK PORTAL FOR HYDROSPHERE (HY) POOL
    # ========================================================
    hy_folder = "hydrosphere_pool"
    os.makedirs(hy_folder, exist_ok=True)

    # 6a. Hovedside for Hydrosphere (Grandparent)
    with open(os.path.join(hy_folder, "pool_hydrosphere.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Hydrosphere (HY)\n")
        f.write("nav_order: 6\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Pool: Hydrosphere (HY)\n\n")
        f.write("We have chosen to not include the pool groundwater (GW) because N concentrations and dynamics ")
        f.write("in Norway are largely unknown (Kværnø et al., 2024 [^kvaerno_2024]).\n\n")
        f.write("The hydrosphere ecosystem is split into three operational modules. Explore them below:\n\n")
        f.write("* [Surface Water (HY.SW)](subpool_surface_water.html)\n")
        f.write("* [Coastal Water (HY.CW)](subpool_coastal_water.html)\n")
        f.write("* [Aquaculture (HY.AC)](subpool_aquaculture.html)\n")
        
        f.write(get_balance_image_markdown("HY", relative_depth="../"))

    # 6b. Sub-hovedside for Surface Water (Parent 1)
    with open(os.path.join(hy_folder, "subpool_surface_water.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Surface Water (HY.SW)\n")
        f.write("parent: Hydrosphere (HY)\n")
        f.write("nav_order: 1\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Surface water (HY.SW)\n\n")
        
        f.write(get_balance_image_markdown("HY.SW", relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **HY.SW-AT.AT-Emissions-NOx** is assumed negligible.\n")
        f.write("* **HY.SW-RW.RW-Export of surface water-Nmix** is assumed negligible due to Norwegian topography.\n")

    # 6c. Sub-hovedside for Coastal Water (Parent 2)
    with open(os.path.join(hy_folder, "subpool_coastal_water.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Coastal Water (HY.CW)\n")
        f.write("parent: Hydrosphere (HY)\n")
        f.write("nav_order: 2\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Coastal water (HY.CW)\n\n")
        
        f.write(get_balance_image_markdown("HY.CW", relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **HY.CW-AT.AT-Emissions-N2** is neglected as we do not use mass balance on this subpool.\n")
        f.write("* **HY.CW-AT.AT-Emissions-N2O** and **HY.CW-AT.AT-Emissions-NOx** are neglected as we lack a clearly defined area for coastal waters.\n")
        f.write("* **HY.CW-PR.SO-Biomass for energy production-Nmix** is neglected because organic material from the processing of caught or farmed fish is assigned to the MP.FS subpool; there is no harvest of material from the ocean only for bioenergy purposes.\n")
        f.write("* **Recreational fishing** is not included in the official guidelines, and we have also chosen to neglect it here. According to Ferter et al. (2023) [^ferter_2023] around 15 kt fish was caught in recreational fishing yearly in 2018-2019. This is less than 1 % of the fish caught in commercial fishing operations.\n")

    # 6d. Sub-hovedside for Aquaculture (Parent 3) - Fullført her:
    with open(os.path.join(hy_folder, "subpool_aquaculture.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Aquaculture (HY.AC)\n")
        f.write("parent: Hydrosphere (HY)\n")
        f.write("nav_order: 3\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Aquaculture (HY.AC)\n\n")
        
        f.write(get_balance_image_markdown("HY.AC", relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **HY.AC-MP.FP-Freshwater fish and seafood-Nmix**, **HY.AC-HY.SW-Waste feed-Nmix** and **HY.AC-HY.SW-Excretia-Nmix** are set to zero because practically all aquaculture in Norway is done in coastal waters.\n")
        f.write("* **HY.AC-AT.AT-Emissions-NH3** is set to zero assuming negligible ammonia emissions from these coastal marine cages.\n")
        
    # ========================================================
    # 7. OPPRETT HIERARKISK PORTAL FOR ENERGY AND FUELS (EF) POOL
    # ========================================================
    ef_folder = "energy_and_fuels_pool"
    os.makedirs(ef_folder, exist_ok=True)

    # 7a. Hovedside for Energy and fuels (Grandparent)
    with open(os.path.join(ef_folder, "pool_energy_and_fuels.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Energy and fuels (EF)\n")
        f.write("nav_order: 7\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Pool: Energy and fuels (EF)\n\n")
        f.write(
            "In the guidelines, there are N2 flows assigned to and from EF sectors associated with nitrogen "
            "conversions in the combustion process. We have chosen to ignore these here because they can only "
            "be found by mass balance and, by doing so, they may hide other imbalances that could be significant. "
            "They also do not make any significant contributions to the flows of reactive N.\n\n"
        )
        f.write(
            "Note on subpools: it is not always clear where flows end up. For example, industrial waste fuels from "
            "MP.OP is assigned to manufacturing industries EF.IC, meaning that waste for fuel is kept within the "
            "industrial sector. This is not necessarily the case.\n\n"
        )
        f.write("This pool is divided into four operational sub-pools. Explore them using the side menu or links below:\n\n")
        f.write("* [Energy conversion (EF.EC)](subpool_energy_conversion.html)\n")
        f.write("* [Manufacturing industries and construction (EF.IC)](subpool_industry.html)\n")
        f.write("* [Transportation (EF.TR)](subpool_transport.html)\n")
        f.write("* [Other energy and fuels (EF.OE)](subpool_other_energy.html)\n\n")
        
        f.write(get_balance_image_markdown("EF", relative_depth="../"))

    # 7b. Sub-hovedside for Energy conversion (EF.EC)
    with open(os.path.join(ef_folder, "subpool_energy_conversion.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Energy conversion (EF.EC)\n")
        f.write("parent: Energy and fuels (EF)\n")
        f.write("nav_order: 1\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Energy conversion (EF.EC)\n\n")
        f.write(
            "This subpool includes extraction of fossil fuels from geological sources, which is a large sector "
            "in Norway. Because of this there is no mass balance for EF.EC; nitrogen bound to extracted fuels "
            "arises in the sector, and outflows are therefore significantly larger than inflows.\n\n"
        )
        f.write(get_balance_image_markdown("EF.EC", relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write(
            "* **EF.EC-AT.AT-Emissions-NH3**: Data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by "
            "Schäppi (2025) [^schappi_annexes_2025], using the categories given in Table 11, give values that are "
            "consistently below 0.001 ktN/year, which is negligible in this context.\n"
        )

    # 7c. Sub-hovedside for Manufacturing industries and construction (EF.IC)
    with open(os.path.join(ef_folder, "subpool_industry.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Manufacturing industries and construction (EF.IC)\n")
        f.write("parent: Energy and fuels (EF)\n")
        f.write("nav_order: 2\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Manufacturing industries and construction (EF.IC)\n\n")
        f.write(get_balance_image_markdown("EF.IC", relative_depth="../"))

    # 7d. Sub-hovedside for Transportation (EF.TR)
    with open(os.path.join(ef_folder, "subpool_transport.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Transportation (EF.TR)\n")
        f.write("parent: Energy and fuels (EF)\n")
        f.write("nav_order: 3\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Transportation (EF.TR)\n\n")
        f.write(get_balance_image_markdown("EF.TR", relative_depth="../"))

    # 7e. Sub-hovedside for Other energy and fuels (EF.OE)
    with open(os.path.join(ef_folder, "subpool_other_energy.md"), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("layout: default\n")
        f.write("title: Other energy and fuels (EF.OE)\n")
        f.write("parent: Energy and fuels (EF)\n")
        f.write("nav_order: 4\n")
        f.write("has_children: true\n")
        f.write("---\n\n")
        f.write("# Subpool: Other energy and fuels (EF.OE)\n\n")
        f.write(get_balance_image_markdown("EF.OE", relative_depth="../"))

    # 7f. Generer flow-sider for EF-subpoolene
    ef_ec_counter = 1
    ef_ic_counter = 1
    ef_tr_counter = 1
    ef_oe_counter = 1

    for filename in plot_files:
        # Vi antar navnekonvensjon som starter med EF_EC_, EF_IC_, EF_TR_ eller EF_OE_
        upper = filename.upper()
        if not (upper.startswith("EF_EC_") or upper.startswith("EF_IC_") or upper.startswith("EF_TR_") or upper.startswith("EF_OE_")):
            continue

        base_name = filename.rsplit('.', 1)[0]
        flow_file_name = f"flow_{base_name}.md"
        full_flow_path = os.path.join(ef_folder, flow_file_name)
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')

        exact_flow_code = "EF-Unknown-Flow"
        display_name = "Unknown Energy and fuels Flow"
        parent_subpool = ""
        description = ""

        # -------------------
        # Energy conversion (EF.EC)
        # -------------------
        if upper.startswith("EF_EC_"):
            parent_subpool = "Energy conversion (EF.EC)"

            if "emissions" in norm and "nox" in norm:
                exact_flow_code = "EF.EC-AT.AT-Emissions-NOx"
                display_name = "Energy conversion emissions (NOx)"
                description = (
                    "EF.EC-AT.AT-Emissions-NOx: We have used data from CLRTAP Inventory Submissions (EMEP, 2025) "
                    "as advised by Schäppi (2025) [^schappi_annexes_2025], using the categories given in Table 11."
                )
            elif "emissions" in norm and "n2o" in norm:
                exact_flow_code = "EF.EC-AT.AT-Emissions-N2O"
                display_name = "Energy conversion emissions (N2O)"
                description = (
                    "EF.EC-AT.AT-Emissions-N2O is taken from UNFCCC Common Reporting Tables, Table 1, using the "
                    "categories given in Table 11 by Schäppi (2025) [^schappi_annexes_2025]."
                )
            elif "fuel" in norm and "industry" in norm:
                exact_flow_code = "EF.EC-EF.IC-Fuel for industry-Nmix"
                display_name = "Fuel for industry"
                description = (
                    "EF.EC-EF.IC-Fuel for industry-Nmix: As advised by Schäppi (2025) [^schappi_annexes_2025], we have "
                    "found this in the UNFCCC Common Reporting Tables (Table 1) which gives amount of energy consumed "
                    "in TJ, together with net caloric values from Table 1.2 in Garg et al. (2006) [^garg_2006] and "
                    "nitrogen contents from Table 15 in Schäppi (2025) [^schappi_annexes_2025]."
                )
            elif "fuel" in norm and "heating" in norm:
                exact_flow_code = "EF.EC-EF.OE-Fuel for heating-Nmix"
                display_name = "Fuel for heating"
                description = (
                    "EF.EC-EF.OE-Fuel for heating-Nmix: As advised by Schäppi (2025) [^schappi_annexes_2025], we have "
                    "found this in the UNFCCC Common Reporting Tables (Table 1) which gives amount of energy consumed "
                    "in TJ, together with net caloric values from Table 1.2 in Garg et al. (2006) [^garg_2006] and "
                    "nitrogen contents from Table 15 in Schäppi (2025) [^schappi_annexes_2025]."
                )
            elif "fuel" in norm and "transport" in norm:
                exact_flow_code = "EF.EC-EF.TR-Fuel for transport-Nmix"
                display_name = "Fuel for transport"
                description = (
                    "EF.EC-EF.TR-Fuel for transport-Nmix: As advised by Schäppi (2025) [^schappi_annexes_2025], we have "
                    "found this in the UNFCCC Common Reporting Tables (Table 1) which gives amount of energy consumed "
                    "in TJ, together with net caloric values from Table 1.2 in Garg et al. (2006) [^garg_2006] and "
                    "nitrogen contents from Table 15 in Schäppi (2025) [^schappi_annexes_2025]."
                )
            elif "feedstock" in norm:
                exact_flow_code = "EF.EC-MP.OP-Fuel used as feedstock-Nmix"
                display_name = "Fuel used as feedstock"
                description = (
                    "EF.EC-MP.OP-Fuel used as feedstock-Nmix: We use SSB table 11561 ('Energibalansen') to obtain GWh "
                    "of coal and oil used as feedstock. We convert GWh to TJ, divide by net caloric values for coal and "
                    "oil, and multiply by N fractions from Schäppi (2025) [^schappi_annexes_2025]. Other minor feedstock "
                    "categories listed in the guidelines are neglected as advised by Schäppi (2025)."
                )
            elif "export" in norm and "transport" not in norm:
                exact_flow_code = "EF.EC-RW.RW-Fuel export-Nmix"
                display_name = "Fuel export"
                description = (
                    "EF.EC-RW.RW-Fuel export-Nmix is the nitrogen content in exported fuels. We use trade data in SSB "
                    "table 08801 to account for all petroleum products excluding those assumed to be used in the transport sector."
                )

        # -------------------
        # Manufacturing industries and construction (EF.IC)
        # -------------------
        elif upper.startswith("EF_IC_"):
            parent_subpool = "Manufacturing industries and construction (EF.IC)"

            if "emissions" in norm and "n2o" in norm:
                exact_flow_code = "EF.IC-AT.AT-Emissions-N2O"
                display_name = "Industrial emissions (N2O)"
                description = (
                    "EF.IC-AT.AT-Emissions-N2O is taken from UNFCCC Common Reporting Tables, Table 1, using the "
                    "categories given in Table 12 by Schäppi (2025) [^schappi_annexes_2025]."
                )
            elif "emissions" in norm and "nh3" in norm:
                exact_flow_code = "EF.IC-AT.AT-Emissions-NH3"
                display_name = "Industrial emissions (NH3)"
                description = (
                    "EF.IC-AT.AT-Emissions-NH3 denotes ammonia emissions from fuel combustion in industry. We have "
                    "used data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by Schäppi (2025) "
                    "[^schappi_annexes_2025], using the categories given in Table 12."
                )
            elif "emissions" in norm and "nox" in norm:
                exact_flow_code = "EF.IC-AT.AT-Emissions-NOx"
                display_name = "Industrial emissions (NOx)"
                description = (
                    "EF.IC-AT.AT-Emissions-NOx denotes NOx emissions from fuel combustion in industry. We have used "
                    "data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by Schäppi (2025) "
                    "[^schappi_annexes_2025], using the categories given in Table 12."
                )

        # -------------------
        # Transportation (EF.TR)
        # -------------------
        elif upper.startswith("EF_TR_"):
            parent_subpool = "Transportation (EF.TR)"

            if "emissions" in norm and "n2o" in norm:
                exact_flow_code = "EF.TR-AT.AT-Emissions-N2O"
                display_name = "Transport emissions (N2O)"
                description = (
                    "EF.TR-AT.AT-Emissions-N2O is taken from UNFCCC Common Reporting Tables, Table 1, using the "
                    "categories given in Table 13 by Schäppi (2025) [^schappi_annexes_2025]."
                )
            elif "emissions" in norm and "nh3" in norm:
                exact_flow_code = "EF.TR-AT.AT-Emissions-NH3"
                display_name = "Transport emissions (NH3)"
                description = (
                    "EF.TR-AT.AT-Emissions-NH3 denotes ammonia emissions from fuel combustion in the transport "
                    "sector. We have used data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by "
                    "Schäppi (2025) [^schappi_annexes_2025], using the categories given in Table 13."
                )
            elif "emissions" in norm and "nox" in norm:
                exact_flow_code = "EF.TR-AT.AT-Emissions-NOx"
                display_name = "Transport emissions (NOx)"
                description = (
                    "EF.TR-AT.AT-Emissions-NOx denotes NOx emissions from fuel combustion in the transport sector. "
                    "We have used data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by Schäppi (2025) "
                    "[^schappi_annexes_2025], using the categories given in Table 13."
                )
            elif "export" in norm or "transportfuel" in norm:
                exact_flow_code = "EF.TR-RW.RW-Export of transport fuels-Nmix"
                display_name = "Export of transport fuels"
                description = (
                    "EF.TR-RW.RW-Export of transport fuels-Nmix is export of fuels for transport. We use trade data in "
                    "SSB table 08801 to account for all petroleum products assumed to be used in the transport sector."
                )

        # -------------------
        # Other energy and fuels (EF.OE)
        # -------------------
        elif upper.startswith("EF_OE_"):
            parent_subpool = "Other energy and fuels (EF.OE)"

            if "emissions" in norm and "n2o" in norm:
                exact_flow_code = "EF.OE-AT.AT-Emissions-N2O"
                display_name = "Other energy emissions (N2O)"
                description = (
                    "EF.OE-AT.AT-Emissions-N2O is taken from UNFCCC Common Reporting Tables, Table 1, using the "
                    "categories given in Table 14 by Schäppi (2025) [^schappi_annexes_2025]."
                )
            elif "emissions" in norm and "nh3" in norm:
                exact_flow_code = "EF.OE-AT.AT-Emissions-NH3"
                display_name = "Other energy emissions (NH3)"
                description = (
                    "EF.OE-AT.AT-Emissions-NH3 is ammonia emissions from fuel combustion in residential, commercial "
                    "and other sectors that are not already covered. We have used data from CLRTAP Inventory "
                    "Submissions (EMEP, 2025) as advised by Schäppi (2025) [^schappi_annexes_2025], using the "
                    "categories given in Table 14."
                )
            elif "emissions" in norm and "nox" in norm:
                exact_flow_code = "EF.OE-AT.AT-Emissions-NOx"
                display_name = "Other energy emissions (NOx)"
                description = (
                    "EF.OE-AT.AT-Emissions-NOx is NOx emissions from fuel combustion in residential, commercial and "
                    "other sectors that are not already covered. We have used data from CLRTAP Inventory Submissions "
                    "(EMEP, 2025) as advised by Schäppi (2025) [^schappi_annexes_2025], using the categories given "
                    "in Table 14."
                )

        # Skriv ut Markdown-fil for denne strømmen
        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write("layout: default\n")
            f.write(f"title: {display_name}\n")
            f.write(f"parent: {parent_subpool}\n")
            if "EF.EC" in exact_flow_code:
                f.write(f"nav_order: {ef_ec_counter}\n")
                ef_ec_counter += 1
            elif "EF.IC" in exact_flow_code:
                f.write(f"nav_order: {ef_ic_counter}\n")
                ef_ic_counter += 1
            elif "EF.TR" in exact_flow_code:
                f.write(f"nav_order: {ef_tr_counter}\n")
                ef_tr_counter += 1
            elif "EF.OE" in exact_flow_code:
                f.write(f"nav_order: {ef_oe_counter}\n")
                ef_oe_counter += 1
            else:
                f.write("nav_order: 99\n")
            f.write("---\n\n")

            f.write(f"# {display_name}\n\n")
            f.write(f"![{exact_flow_code}](../{plot_dir}/{filename})\n\n")
            f.write("### Flow Description\n")
            if description:
                f.write(f"{description}\n\n")
            else:
                f.write(f"*Flow details detected for file: `{filename}` (code: {exact_flow_code}).*\n\n")

            append_bibtex_references(f)
