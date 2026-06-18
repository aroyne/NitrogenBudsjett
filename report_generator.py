# report_generator.py
import os
import shutil
from datetime import datetime
from pybtex.database import parse_file

# ==============================================================================
# FELLES TEKSTBLOKKER OG HJELPEFUNKSJONER
# ==============================================================================

DEPOSITION_TEXT = (
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


def get_balance_image_markdown(pool_code, plot_files, plot_dir, relative_depth=""):
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


def append_bibtex_references(file_handle, bib_filename):
    """Parser BibTeX-filen og legger til formaterte referanser i bunnen av en fil."""
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


# ==============================================================================
# SPESIFIKKE FUNKSJONER FOR HVER ENKELT POOL
# ==============================================================================

def build_landing_page(output_filename, current_date_str):
    """Genererer hovedlandingssiden (index.md) med kritisk advarsel."""
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Home\nnav_order: 1\n---\n\n")
        f.write("# Nitrogen Budget for Norway\n\n")
        f.write(f"**Last Updated:** {current_date_str}\n\n")
        f.write("{: .label .label-red }\nWork in Progress\n\n")
        f.write("> **CRITICAL WARNING:** This project, including all underlying code, data parameterizations, ")
        f.write("and simulation results, is currently **under active development**. It is not yet validated or finalized. ")
        f.write("Using, copying, or relying on any part of this code or these results for research, decision-making, ")
        f.write("or any other application is **strongly discouraged** at this stage.\n\n")
        f.write("---\n\n### Project Overview\n")
        f.write("Welcome to the interactive data and documentation portal for the Norwegian national nitrogen budget. ")
        f.write("This platform visualizes and centralizes the outputs from our Monte Carlo uncertainty analysis simulations.\n\n")
        f.write("Use the navigation menu on the left side to explore the individual nitrogen pools ")
        f.write("(e.g., Forests and Semi-natural Vegetation, Agriculture, Atmosphere, Hydrosphere, Rest of the World) ")
        f.write("and access detailed statistical time-series graphs, methodological explanations, and parameterizations for each specific flow.\n")


def process_atmosphere_pool(at_folder, plot_files, plot_dir, bib_filename):
    """Genererer alle sider knyttet til Atmosphere (AT) poolen."""
    with open(os.path.join(at_folder, "pool_atmosphere.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Atmosphere (AT)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Pool: Atmosphere (AT)\n\nThis section contains all documented nitrogen flows leaving the Atmosphere pool.\n")
        f.write(get_balance_image_markdown("AT", plot_files, plot_dir, relative_depth="../"))

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
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: Atmosphere (AT)\nnav_order: {menu_counter}\n---\n\n")
            menu_counter += 1
            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n")

            if exact_flow_code == "AT.AT-AG.SM-Biological N2 fixation-N2":
                f.write("**AT.AT-AG.SM-Biological N2 fixation-N2**\n\n[^schappi_annexes_2025] advises using data from the EUROSTAT Gross nutrient balance...")
            elif exact_flow_code in ["AT.AT-AG.SM-Deposition-OXN", "AT.AT-AG.SM-Deposition-RDN", "AT.AT-FS.FO-Deposition-OXN", "AT.AT-FS.FO-Deposition-RDN", "AT.AT-FS.OL-Deposition-OXN", "AT.AT-FS.OL-Deposition-RDN", "AT.AT-HS.HS-Deposition-OXN", "AT.AT-HS.HS-Deposition-RDN", "AT.AT-HY.SW-Deposition-RDN"]:
                f.write(f"**{exact_flow_code}**\n\n" + DEPOSITION_TEXT + "\n\n")
            elif exact_flow_code == "AT.AT-HY.SW-Deposition-OXN":
                f.write("**AT.AT-HY.SW-Deposition-OXN**\n\n" + DEPOSITION_TEXT + "\n\nFor comparison, the data used in the TEOTIL model...")
            else:
                f.write(f"*Flow details for {exact_flow_code}*\n\n")

            append_bibtex_references(f, bib_filename)


def process_rest_of_the_world_pool(rw_folder, plot_files, plot_dir, bib_filename):
    """Genererer alle sider knyttet til Rest of the World (RW) poolen."""
    with open(os.path.join(rw_folder, "pool_rest_of_the_world.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Rest of the world (RW)\nnav_order: 3\nhas_children: true\n---\n\n")
        f.write("# Pool: Rest of the world (RW)\n\nThis section contains all documented nitrogen inflows and transfers originating from the Rest of the world (RW) pool. ")
        f.write("Click on the individual sub-flows in the left-hand menu to view graphs and methodological explanations.\n\n")
        f.write(get_balance_image_markdown("RW", plot_files, plot_dir, relative_depth="../"))
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
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: Rest of the world (RW)\nnav_order: {rw_menu_counter}\n---\n\n")
            rw_menu_counter += 1
            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n")
            if description:
                f.write(f"{description}\n\n")
            else:
                f.write(f"*Flow details detected for file: `{filename}`.*\n\n")
            append_bibtex_references(f, bib_filename)


def process_agriculture_pool(ag_folder, plot_files, plot_dir, bib_filename):
    """Genererer hovedsiden, subpools og alle strømmer for Agriculture (AG)."""
    with open(os.path.join(ag_folder, "pool_agriculture.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Agriculture (AG)\nnav_order: 4\nhas_children: true\n---\n\n")
        f.write("# Pool: Agriculture (AG)\n\nBecause biofuel production in Norway is typically done as part of the waste management sector, ")
        f.write("flows of agricultural wastes to biofuel production are directed to PR.SO and we do not include the subpool AG.BC.\n\n")
        f.write("This pool is divided into two operational sub-pools. Explore them using the side menu or links below:\n\n")
        f.write("* [Manure Management (AG.MM)](subpool_manure_management.html)\n")
        f.write("* [Soil Management (AG.SM)](subpool_soil_management.html)\n")
        f.write(get_balance_image_markdown("AG", plot_files, plot_dir, relative_depth="../"))

    with open(os.path.join(ag_folder, "subpool_manure_management.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Manure Management (AG.MM)\nparent: Agriculture (AG)\nnav_order: 1\nhas_children: true\n---\n\n")
        f.write("# Subpool: Manure management, storage and animal husbandry (AG.MM)\n\n")
        f.write(get_balance_image_markdown("AG.MM", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **AG.MM-RW.RW-Manure export-Nmix** is assumed small and neglected.\n")

    with open(os.path.join(ag_folder, "subpool_soil_management.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Soil Management (AG.SM)\nparent: Agriculture (AG)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Subpool: Soil management (AG.SM)\n\n")
        f.write(get_balance_image_markdown("AG.SM", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **AG.SM-HY.SW-Overland flow-Nmix** is not included because all runoff and leaching is included in Leaching.\n")

    ag_mm_counter, ag_sm_counter = 1, 1

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
                description = "We have used data from CLRTAP Inventory Submissions [^emep_officially_2025] as advised by Schäppi (2025) [^schappi_annexes_2025], using the categories given in Table 29."
            elif "nox" in norm:
                exact_flow_code = "AG.MM-AT.AT-Emissions-NOx"
                display_name = "Manure Emissions (NOx)"
                description = "We have used data from CLRTAP Inventory Submissions [^emep_officially_2025] as advised by Schäppi (2025) [^schappi_annexes_2025], using the categories given in Table 29."
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
                description = "Schäppi (2025) [^schappi_annexes_2025] advises using FAOSTAT Commodity Balances (non-food). For Norway this statistic only contains wool for 4 individual years and we therefore use data for wool from Landbruksdirektoratet[^landbruksdirektoratet_leveransedata-slakt-2005-2012_2025] for 2005-2024; for earlier years, we use the number of sheep (SSB table 03710) and extrapolate from a linear regression found between sheep and wool for 2005-2024. In addition, we use numbers for raw hides and skins from FAOSTAT Crops and livestock products. N contents are taken from [^schappi_annexes_2025]."
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
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: {parent_subpool}\n")
            if 'MM' in parent_subpool:
                f.write(f"nav_order: {ag_mm_counter}\n---\n\n")
                ag_mm_counter += 1
            else:
                f.write(f"nav_order: {ag_sm_counter}\n---\n\n")
                ag_sm_counter += 1

            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n{description}\n\n")
            append_bibtex_references(f, bib_filename)


def process_forests_pool(fs_folder, plot_files, plot_dir, bib_filename):
    """Genererer hovedsiden, subpools og alle strømmer for Forests and semi-natural vegetation (FS)."""
    with open(os.path.join(fs_folder, "pool_forests_and_semi_natural.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Forests and semi-natural vegetation (FS)\nnav_order: 5\nhas_children: true\n---\n\n")
        f.write("# Pool: Forests and semi-natural vegetation (FS)\n\nBecause of limited data on OL and because data on leaching are combined for WL and OL, ")
        f.write("we have chosen to combine WL and OL into the OL subpool in this study.\n\n")
        f.write("We have considered including meat from hunting of wild animals in flows from this subpool, but chosen not to. ")
        f.write("According to (Steinset, 2021), the amount of wild game caught in 2019 was around 6000 tonnes, ")
        f.write("which gives around 0.2 ktN and thus smaller than any of the included flows.\n\n")
        f.write("This pool is divided into two operational sub-pools. Explore them using the side menu or links below:\n\n")
        f.write("* [Forests (FS.FO)](subpool_forests.html)\n* [Other Land (FS.OL)](subpool_other_land.html)\n")
        f.write(get_balance_image_markdown("FS", plot_files, plot_dir, relative_depth="../"))

    with open(os.path.join(fs_folder, "subpool_forests.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Forests (FS.FO)\nparent: Forests and semi-natural vegetation (FS)\nnav_order: 1\nhas_children: true\n---\n\n")
        f.write("# Subpool: Forests (FS.FO)\n\n")
        f.write(get_balance_image_markdown("FS.FO", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **FS.FO-AT.AT-Emissions-NOx** is neglected because no values are reported in the CRLTAP/WebDab categories 4A1 and 4A2 (forest soils).\n")
        f.write("* **FS.FO-EF.EC-Fuel wood for co-fired power plants-Nmix** is set to zero because we assume such facilities do not exist in Norway.\n")
        f.write("* **FS.FO-EF.IC-Fuel wood for industry-Nmix** is ignored because wood is typically not harvested specifically to be used for fuel in industry in Norway. The use of wood waste in the producing industry is reported as self-produced bioenergy in the SSB statistic, but this is a flow that goes from MP.OP to EF.IC.\n")
        f.write("* Because the N-flow in forest fertilization is not large, we have chosen to ignore the associated N2O emissions that were included in the Swedish NBB (Moldan et al., 2025).\n")

    with open(os.path.join(fs_folder, "subpool_other_land.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Other Land (FS.OL)\nparent: Forests and semi-natural vegetation (FS)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Subpool: Other land (FS.OL)\n\n")
        f.write(get_balance_image_markdown("FS.OL", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **FS.OL-AT.AT-Emissions-NOx** is neglected because no values are reported in the CRLTAP/WebDab categories 4F1 and 4F2 (wetlands / other land NOx).\n")

    fs_fo_counter, fs_ol_counter = 1, 1

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
                description = "Calculated based on N2O emissions from UNFCCC Common reporting tables, Table 4 and assuming a mean N2:N2O ratio of 19.5 as discussed in (Schäppi, 2025) [^schappi_annexes_2025]."
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
                description = "Taken from FAOSTAT Forestry production and trade: industrial roundwood, which gives values under bark..."

        elif filename.upper().startswith("FS_OL_"):
            parent_subpool = "Other Land (FS.OL)"
            if "grazing" in norm:
                exact_flow_code = "FS.OL-AG.MM-Grazing-Nmix"
                display_name = "Organised Grazing"
                description = "Calculated using data from NIBIO on organised grazing (NIBIO, 2025a) together with estimated fodder intake for different animal groups..."
            elif "emissionsn2" in norm and "n2o" not in norm:
                exact_flow_code = "FS.OL-AT.AT-Emissions-N2"
                display_name = "Other Land Emissions (N2)"
                description = "Calculated from N2O emissions from UNFCCC Common reporting tables, Table 4, assuming a mean N2:N2O ratio of 19.5..."
            elif "emissionsn2o" in norm:
                exact_flow_code = "FS.OL-AT.AT-Emissions-N2O"
                display_name = "Other Land Emissions (N2O)"
                description = "Taken from UNFCCC Common reporting tables, Table 4, where the only reported values are from wetlands."
            elif "leaching" in norm:
                exact_flow_code = "FS.OL-HY.SW-Leaching-Nmix"
                display_name = "Other Land Leaching"
                description = "Found in data supplied by NIVA, produced in the TEOTIL3 model (Sample et al., 2024)..."

        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: {parent_subpool}\n")
            if 'FO' in parent_subpool:
                f.write(f"nav_order: {fs_fo_counter}\n---\n\n")
                fs_fo_counter += 1
            else:
                f.write(f"nav_order: {fs_ol_counter}\n---\n\n")
                fs_ol_counter += 1

            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n{description}\n\n")
            append_bibtex_references(f, bib_filename)


def process_hydrosphere_pool(hy_folder, plot_files, plot_dir):
    """Genererer hovedsiden og alle under-hovedsider for Hydrosphere (HY) poolen."""
    with open(os.path.join(hy_folder, "pool_hydrosphere.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Hydrosphere (HY)\nnav_order: 6\nhas_children: true\n---\n\n")
        f.write("# Pool: Hydrosphere (HY)\n\nWe have chosen to not include the pool groundwater (GW) because N concentrations and dynamics ")
        f.write("in Norway are largely unknown (Kværnø et al., 2024 [^kvaerno_2024]).\n\n")
        f.write("The hydrosphere ecosystem is split into three operational modules. Explore them below:\n\n")
        f.write("* [Surface Water (HY.SW)](subpool_surface_water.html)\n* [Coastal Water (HY.CW)](subpool_coastal_water.html)\n* [Aquaculture (HY.AC)](subpool_aquaculture.html)\n")
        f.write(get_balance_image_markdown("HY", plot_files, plot_dir, relative_depth="../"))

    with open(os.path.join(hy_folder, "subpool_surface_water.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Surface Water (HY.SW)\nparent: Hydrosphere (HY)\nnav_order: 1\nhas_children: true\n---\n\n")
        f.write("# Subpool: Surface water (HY.SW)\n\n")
        f.write(get_balance_image_markdown("HY.SW", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **HY.SW-AT.AT-Emissions-NOx** is assumed negligible.\n* **HY.SW-RW.RW-Export of surface water-Nmix** is assumed negligible due to Norwegian topography.\n")

    with open(os.path.join(hy_folder, "subpool_coastal_water.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Coastal Water (HY.CW)\nparent: Hydrosphere (HY)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Subpool: Coastal water (HY.CW)\n\n")
        f.write(get_balance_image_markdown("HY.CW", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **HY.CW-AT.AT-Emissions-N2** is neglected as we do not use mass balance on this subpool.\n* **HY.CW-AT.AT-Emissions-N2O** and **HY.CW-AT.AT-Emissions-NOx** are neglected as we lack a clearly defined area for coastal waters.\n* **HY.CW-PR.SO-Biomass for energy production-Nmix** is neglected because organic material from the processing of caught or farmed fish is assigned to the MP.FS subpool...\n* **Recreational fishing** is not included in the official guidelines, and we have also chosen to neglect it here...\n")

    with open(os.path.join(hy_folder, "subpool_aquaculture.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Aquaculture (HY.AC)\nparent: Hydrosphere (HY)\nnav_order: 3\nhas_children: true\n---\n\n")
        f.write("# Subpool: Aquaculture (HY.AC)\n\n")
        f.write(get_balance_image_markdown("HY.AC", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **HY.AC-MP.FP-Freshwater fish and seafood-Nmix**, **HY.AC-HY.SW-Waste feed-Nmix** and **HY.AC-HY.SW-Excretia-Nmix** are set to zero...\n* **HY.AC-AT.AT-Emissions-NH3** is set to zero assuming negligible ammonia emissions from these coastal marine cages.\n")


def process_humans_and_settlements_pool(hs_folder, plot_files, plot_dir, bib_filename):
    """Genererer hovedsiden og alle understrømmer for Humans and settlements (HS) poolen."""
    with open(os.path.join(hs_folder, "pool_humans_and_settlements.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Humans and settlements (HS)\nnav_order: 7\nhas_children: true\n---\n\n")
        f.write("# Pool: Humans and settlements (HS)\n\n")
        f.write(get_balance_image_markdown("HS", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **HS.HS-AT.AT-LUC emissions-NH3** is assumed negligible as no NH3 emissions are given in the CLRTAP inventory submissions.\n")
        f.write("* **HS.HS-AT.AT-LUC emissions-NOx** is set to zero because none is reported in UNFCCC Common reporting tables, Table 4.\n")
        f.write("* **HS.HS-HY.SW-Untreated wastewater-Nmix** and **HS.HS-HY.CW-Untreated wastewater-Nmix** are set to zero because wastewater treatment is mandated by law.\n")
        f.write("* **HS.HS-PR.SO-Organic waste biofuel substrate-Nmix** and **HS.HS-PR.SO-Organic waste for composting-Nmix** are not given as separate flows; instead they are included in the flow **HS.HS-PR.SO-Household waste-Nmix** because official statistics do not clearly indicate what origin waste flows end up in different end uses.\n")
        f.write("* **HS.HS-MP.OP-Recycling-Nmix** is not reported here because the flow of wastes from all origins to recycling is assigned to the PR.OS subpool to better reflect the Norwegian waste management and statistics structure.\n")

    hs_menu_counter = 1
    for filename in plot_files:
        if not filename.upper().startswith("HS_HS_"):
            continue

        flow_file_name = f"flow_{filename.replace('.png', '')}.md"
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')
        full_flow_path = os.path.join(hs_folder, flow_file_name)

        exact_flow_code = "HS.HS-Unknown-Flow"
        display_name = "Unknown Humans and Settlements Flow"
        description = ""

        if "emissionsnh3" in norm:
            exact_flow_code = "HS.HS-AT.AT-Emissions-NH3"
            display_name = "Ammonia Body Emissions"
            description = (
                "**HS.HS-AT.AT-Emissions-NH3** are ammonia emissions from the human body. We use population data from SSB "
                "together with SSB data on smoking (table 05307) and assume that daily smokers smoke 750 cigarettes per year, "
                "while occasional smokers smoke 100 per year. This data is used with equation 46 in (Schäppi, 2025), taken from "
                "Sutton (2000), which relates ammonia emissions to age and cigarette smoking."
            )
        elif "luc" in norm and "n2o" in norm:
            exact_flow_code = "HS.HS-AT.AT-LUC emissions-N2O"
            display_name = "LUC Emissions (N2O)"
            description = "**HS.HS-AT.AT-LUC emissions-N2O** is taken from UNFCCC Common reporting tables, Table 4."
        elif "overland" in norm or "runoff" in norm:
            exact_flow_code = "HS.HS-HY.SW-Overland flow-Nmix"
            display_name = "Urban Overland Flow"
            description = (
                "**HS.HS-HY.SW-Overland flow-Nmix** is a flow that has been added to account for runoff from urban areas. "
                "Some of this may actually end up directly in CW, but we have not been able to separate the two. "
                "Data are supplied by NIVA, produced in the TEOTIL3 model (Sample et al., 2024). For the period 1990-2013, "
                "we have used TEOTIL data (Sample, 2025) for nitrogen from urban areas that reach the coast, and used a "
                "retention rate of 5% which is consistent (with a 7% standard deviation) with the TEOTIL3 data from NIVA. "
                "The constant values for 1990-2012 is what is reported by Miljødirektoratet."
            )
        elif "household" in norm and "waste" in norm:
            exact_flow_code = "HS.HS-PR.SO-Household waste-Nmix"
            display_name = "Household and Settlement Waste"
            description = (
                "**HS.HS-PR.SO-Household waste-Nmix** includes all types of solid waste from settlements which are processed "
                "in the sub-pool “solid waste” through incineration, landfilling, biofuel production or composting. We use data "
                "from SSB table 05282 “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og kilde” "
                "(1995-2011) and 10514 «Avfallsregnskap for Norge, etter kilde og materialtype (1 000 tonn) 2012 – 2023» "
                "with N contents taken from (Schäppi, 2025) and typical, assumed values are chosen if none are given. We include "
                "households, services (tjenesteytende næringer), construction (Bygge- og anleggsvirksomhet), municipal services "
                "(power and water), and waste management.\n\n"
                "Detailed data are not available prior to 1995, but trends in municipal and other waste are described in (SSB, 1997). "
                "Household waste per inhabitant increased from about 200 kg/person to 289 kg/person in 1995 ((SSB, 1997), figure 4.1), "
                "with an assumed linear increase in the years between. Based on this we assume a constant N content per unit mass "
                "and extrapolate from 1995 values back to 1990."
            )
        elif "wastewater" in norm or "municipal" in norm:
            exact_flow_code = "HS.HS-PR.WW-Municipal wastewater-Nmix"
            display_name = "Municipal Wastewater"
            description = (
                "**HS.HS-PR.WW-Municipal wastewater-Nmix** are based on population data from SSB and assuming an average value "
                "of 4.65 kg N / person / year for municipal wastewater as advised by (Schäppi, 2025). This corresponds to "
                "12.7 g N / person / day."
            )

        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: Humans and settlements (HS)\nnav_order: {hs_menu_counter}\n---\n\n")
            hs_menu_counter += 1
            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n")
            if description:
                f.write(f"{description}\n\n")
            else:
                f.write(f"*Flow details detected for file: `{filename}` (code: {exact_flow_code}).*\n\n")
            append_bibtex_references(f, bib_filename)

def process_energy_and_fuels_pool(ef_folder, plot_files, plot_dir, bib_filename):
    """Genererer hovedsiden, subpools og alle strømmer for Energy and Fuels (EF)."""
    with open(os.path.join(ef_folder, "pool_energy_and_fuels.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Energy and fuels (EF)\nnav_order: 7\nhas_children: true\n---\n\n")
        f.write("# Pool: Energy and fuels (EF)\n\nIn the guidelines, there are N2 flows assigned to and from EF sectors associated with nitrogen conversions in the combustion process...\n")
        f.write("This pool is divided into four operational sub-pools. Explore them using the side menu or links below:\n\n")
        f.write("* [Energy conversion (EF.EC)](subpool_energy_conversion.html)\n* [Manufacturing industries and construction (EF.IC)](subpool_industry.html)\n* [Transportation (EF.TR)](subpool_transport.html)\n* [Other energy and fuels (EF.OE)](subpool_other_energy.html)\n\n")
        f.write(get_balance_image_markdown("EF", plot_files, plot_dir, relative_depth="../"))

    # Opprett subpools
    with open(os.path.join(ef_folder, "subpool_energy_conversion.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Energy conversion (EF.EC)\nparent: Energy and fuels (EF)\nnav_order: 1\nhas_children: true\n---\n\n# Subpool: Energy conversion (EF.EC)\n\n")
        f.write(get_balance_image_markdown("EF.EC", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **EF.EC-AT.AT-Emissions-NH3**: Data from CLRTAP Inventory Submissions...\n")

    with open(os.path.join(ef_folder, "subpool_industry.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Manufacturing industries and construction (EF.IC)\nparent: Energy and fuels (EF)\nnav_order: 2\nhas_children: true\n---\n\n# Subpool: Manufacturing industries and construction (EF.IC)\n\n")
        f.write(get_balance_image_markdown("EF.IC", plot_files, plot_dir, relative_depth="../"))

    with open(os.path.join(ef_folder, "subpool_transport.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Transportation (EF.TR)\nparent: Energy and fuels (EF)\nnav_order: 3\nhas_children: true\n---\n\n# Subpool: Transportation (EF.TR)\n\n")
        f.write(get_balance_image_markdown("EF.TR", plot_files, plot_dir, relative_depth="../"))

    with open(os.path.join(ef_folder, "subpool_other_energy.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Other energy and fuels (EF.OE)\nparent: Energy and fuels (EF)\nnav_order: 4\nhas_children: true\n---\n\n# Subpool: Other energy and fuels (EF.OE)\n\n")
        f.write(get_balance_image_markdown("EF.OE", plot_files, plot_dir, relative_depth="../"))

    ef_ec_counter = ef_ic_counter = ef_tr_counter = ef_oe_counter = 1

    for filename in plot_files:
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

        if upper.startswith("EF_EC_"):
            parent_subpool = "Energy conversion (EF.EC)"
            if "emissions" in norm and "nox" in norm:
                exact_flow_code = "EF.EC-AT.AT-Emissions-NOx"
                display_name = "Energy conversion emissions (NOx)"
                description = "EF.EC-AT.AT-Emissions-NOx: We have used data from CLRTAP Inventory Submissions..."
            elif "emissions" in norm and "n2o" in norm:
                exact_flow_code = "EF.EC-AT.AT-Emissions-N2O"
                display_name = "Energy conversion emissions (N2O)"
                description = "EF.EC-AT.AT-Emissions-N2O is taken from UNFCCC Common Reporting Tables..."
            elif "fuel" in norm and "industry" in norm:
                exact_flow_code = "EF.EC-EF.IC-Fuel for industry-Nmix"
                display_name = "Fuel for industry"
                description = "EF.EC-EF.IC-Fuel for industry-Nmix: As advised by Schäppi (2025)..."
            elif "fuel" in norm and "heating" in norm:
                exact_flow_code = "EF.EC-EF.OE-Fuel for heating-Nmix"
                display_name = "Fuel for heating"
                description = "EF.EC-EF.OE-Fuel for heating-Nmix: As advised by Schäppi (2025)..."
            elif "fuel" in norm and "transport" in norm:
                exact_flow_code = "EF.EC-EF.TR-Fuel for transport-Nmix"
                display_name = "Fuel for transport"
                description = "EF.EC-EF.TR-Fuel for transport-Nmix: As advised by Schäppi (2025)..."
            elif "feedstock" in norm:
                exact_flow_code = "EF.EC-MP.OP-Fuel used as feedstock-Nmix"
                display_name = "Fuel used as feedstock"
                description = "EF.EC-MP.OP-Fuel used as feedstock-Nmix: We use SSB table 11561..."
            elif "export" in norm and "transport" not in norm:
                exact_flow_code = "EF.EC-RW.RW-Fuel export-Nmix"
                display_name = "Fuel export"
                description = "EF.EC-RW.RW-Fuel export-Nmix is the nitrogen content in exported fuels..."

        elif upper.startswith("EF_IC_"):
            parent_subpool = "Manufacturing industries and construction (EF.IC)"
            if "emissions" in norm and "n2o" in norm:
                exact_flow_code = "EF.IC-AT.AT-Emissions-N2O"
                display_name = "Industrial emissions (N2O)"
                description = "EF.IC-AT.AT-Emissions-N2O is taken from UNFCCC Common Reporting Tables..."
            elif "emissions" in norm and "nh3" in norm:
                exact_flow_code = "EF.IC-AT.AT-Emissions-NH3"
                display_name = "Industrial emissions (NH3)"
                description = "EF.IC-AT.AT-Emissions-NH3 denotes ammonia emissions from fuel combustion in industry..."
            elif "emissions" in norm and "nox" in norm:
                exact_flow_code = "EF.IC-AT.AT-Emissions-NOx"
                display_name = "Industrial emissions (NOx)"
                description = "EF.IC-AT.AT-Emissions-NOx denotes NOx emissions from fuel combustion in industry..."

        elif upper.startswith("EF_TR_"):
            parent_subpool = "Transportation (EF.TR)"
            if "emissions" in norm and "n2o" in norm:
                exact_flow_code = "EF.TR-AT.AT-Emissions-N2O"
                display_name = "Transport emissions (N2O)"
                description = "EF.TR-AT.AT-Emissions-N2O is taken from UNFCCC Common Reporting Tables..."
            elif "emissions" in norm and "nh3" in norm:
                exact_flow_code = "EF.TR-AT.AT-Emissions-NH3"
                display_name = "Transport emissions (NH3)"
                description = "EF.TR-AT.AT-Emissions-NH3 denotes ammonia emissions from fuel combustion..."
            elif "emissions" in norm and "nox" in norm:
                exact_flow_code = "EF.TR-AT.AT-Emissions-NOx"
                display_name = "Transport emissions (NOx)"
                description = "EF.TR-AT.AT-Emissions-NOx denotes NOx emissions from fuel combustion..."
            elif "export" in norm or "transportfuel" in norm:
                exact_flow_code = "EF.TR-RW.RW-Export of transport fuels-Nmix"
                display_name = "Export of transport fuels"
                description = "EF.TR-RW.RW-Export of transport fuels-Nmix is export of fuels for transport..."

        elif upper.startswith("EF_OE_"):
            parent_subpool = "Other energy and fuels (EF.OE)"
            if "emissions" in norm and "n2o" in norm:
                exact_flow_code = "EF.OE-AT.AT-Emissions-N2O"
                display_name = "Other energy emissions (N2O)"
                description = "EF.OE-AT.AT-Emissions-N2O is taken from UNFCCC Common Reporting Tables..."
            elif "emissions" in norm and "nh3" in norm:
                exact_flow_code = "EF.OE-AT.AT-Emissions-NH3"
                display_name = "Other energy emissions (NH3)"
                description = "EF.OE-AT.AT-Emissions-NH3 is ammonia emissions from fuel combustion..."
            elif "emissions" in norm and "nox" in norm:
                exact_flow_code = "EF.OE-AT.AT-Emissions-NOx"
                display_name = "Other energy emissions (NOx)"
                description = "EF.OE-AT.AT-Emissions-NOx is NOx emissions from fuel combustion..."

        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: {parent_subpool}\n")
            if "EF.EC" in exact_flow_code: f.write(f"nav_order: {ef_ec_counter}\n---\n\n"); ef_ec_counter += 1
            elif "EF.IC" in exact_flow_code: f.write(f"nav_order: {ef_ic_counter}\n---\n\n"); ef_ic_counter += 1
            elif "EF.TR" in exact_flow_code: f.write(f"nav_order: {ef_tr_counter}\n---\n\n"); ef_tr_counter += 1
            elif "EF.OE" in exact_flow_code: f.write(f"nav_order: {ef_oe_counter}\n---\n\n"); ef_oe_counter += 1
            else: f.write("nav_order: 99\n---\n\n")

            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n")
            f.write(f"{description}\n\n" if description else f"*Flow details detected for file: `{filename}` (code: {exact_flow_code}).*\n\n")
            append_bibtex_references(f, bib_filename)

def process_materials_pool(mp_folder, plot_files, plot_dir, bib_filename):
    """Genererer hovedsiden, subpools og alle strømmer for Materials and products in industry (MP)."""
    
    # 1. GENERER HOVEDSIDE FOR POOLEN (pool_materials_and_products.md)
    with open(os.path.join(mp_folder, "pool_materials_and_products.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Materials and products (MP)\nnav_order: 6\nhas_children: true\n---\n\n")
        f.write("# Pool: Materials and products in industry (MP)\n\n")
        f.write("This pool covers chemical, processing, food, and manufacturing industries in Norway, split into two primary segments:\n\n")
        f.write("* [Food and Feed Processing (MP.FP)](subpool_food_and_feed.html)\n")
        f.write("* [Other Producing Industry (MP.OP)](subpool_other_industry.html)\n")
        f.write(get_balance_image_markdown("MP", plot_files, plot_dir, relative_depth="../"))

    # 2. SUBPOOL: FOOD AND FEED PROCESSING (MP.FP)
    with open(os.path.join(mp_folder, "subpool_food_and_feed.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Food and Feed Processing (MP.FP)\nparent: Materials and products (MP)\nnav_order: 1\nhas_children: true\n---\n\n")
        f.write("# Subpool: Food and feed processing (MP.FP)\n\n")
        f.write(get_balance_image_markdown("MP.FP", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **MP.FP-HY.AC-Feed to freshwater aquaculture-Nmix** is set to zero because it is assumed all (except a negligible amount) aquaculture takes place in coastal waters.\n")
        f.write("* **MP.FP-PR.SO-Organic waste as biofuels substrate-Nmix** and **MP.FP-PR.SO-Organic waste for composting-Nmix** are not given as separate flows; instead they are included in the flow **MP.FP-PR.SO-Food industry waste-Nmix** because official statistics do not clearly indicate what origin waste flows end up in different end uses.\n")

    # 3. SUBPOOL: OTHER PRODUCING INDUSTRY (MP.OP)
    with open(os.path.join(mp_folder, "subpool_other_industry.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Other Producing Industry (MP.OP)\nparent: Materials and products (MP)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Subpool: Other producing industry (MP.OP)\n\n")
        f.write(get_balance_image_markdown("MP.OP", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **MP.OP-EF.TR-Ammonia as fuel-NH3** is set to zero because there is negligible use of ammonia as fuel today.\n")

    mp_fp_counter, mp_op_counter = 1, 1

    # 4. ITERER OVER ALLE FILER FOR Å IDENTIFISERE STRØMMER TILHØRENDE MP
    for filename in plot_files:
        if not (filename.upper().startswith("MP_FP_") or filename.upper().startswith("MP_OP_")):
            continue

        base_name = filename.rsplit('.', 1)[0]
        flow_file_name = f"flow_{base_name}.md"
        full_flow_path = os.path.join(mp_folder, flow_file_name)
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')

        exact_flow_code = "MP-Unknown-Flow"
        display_name = "Unknown Industrial Flow"
        parent_subpool = ""
        description = ""

        # Sorter under mat og fôr (MP.FP)
        if filename.upper().startswith("MP_FP_"):
            parent_subpool = "Food and Feed Processing (MP.FP)"
            
            if "farm" in norm and "feed" in norm:
                exact_flow_code = "MP.FP-AG.MM-Farm animal feed-Nmix"
                display_name = "Farm Animal Feed"
                description = (
                    "**MP.FP-AG.MM-Farm animal feed-Nmix** is feed to farm animals. We have used data on domestic feed supply from Landbruksdirektoratet "
                    "(Landbruksdirektoratet, 2025b) and used the detailed composition of animal feed given in (Eidem & Ruud, 2022) together with protein contents "
                    "from (FAO, 2021) and specific Jones factors from (FAO, 2023) to get nitrogen contents.\n\n"
                    "Based on the Landbruksdirektoratet data, the N content of the total amount of feed is 0.02 kgN/kg feed. NIBIO Totalkalkylen "
                    "gives statistics for total amount of feed to Norwegian farm animals between 1959 and 2026. Table 6.10 in (Bruholt & Longva, 1994) "
                    "gives the domestically produced fraction of farm animal feed between 1985 and 1994. We combine these data to find values before 2000, "
                    "using an average import fraction for 1995-1999.\n\n"
                    "(Hohmann-Marriott, 2025) found the domestic supply of animal feed in 2010 to be around 35 ktN, based on FAO statistics of production, "
                    "export and import of seed cake, which is a dominant ingredient in farm animal feed. This is less than we found when combining domestic and imported animal feed. "
                    "*(Note: This estimate might be too low, as it leads to a surplus here and a deficit in the AG.MM pool).*"
                )
            elif "seed" in norm or "planting" in norm:
                exact_flow_code = "MP.FP-AG.SM-Seeds and planting material-Nmix"
                display_name = "Seeds and Planting Material"
                description = (
                    "**MP.FP-AG.SM-Seeds and planting material-Nmix** is taken from Gross nutrient balance in the Eurostat database as advised by (Schäppi, 2025). "
                    "There is data missing from 2017 to 2019; because there is a large reported increase between 2016 and 2020, we assume a constant increase in the "
                    "missing time period and fill in data from this interpolation."
                )
            elif "food" in norm and "product" in norm and "export" not in norm:
                exact_flow_code = "MP.FP-HS.HS-Food products-Nmix"
                display_name = "Food Products to Consumers"
                description = (
                    "**MP.FP-HS.HS-Food products-Nmix** is food products consumed by private households including restaurants and pets. (Schäppi, 2025) "
                    "advises using FAO statistics on food availability for human food consumption, but this only gives data back to 2009. The values in this statistic "
                    "gives a bit more than 40 ktN per year. We have chosen to use data on food sales to consumers from SSB (table 13695: Næringsinnhald per dag frå "
                    "selde mat- og drikkevarer 2018 – 2023, table 10249: Forbrukte mengder av mat- og drikkevarer per person per år, etter varegruppe (kg/liter) (avslutta serie) "
                    "1999 – 2012 and table 06376: Forbrukte mengder av mat- og drikkevarer per person per år, etter varegruppe (kg/liter) (avslutta serie) 1958-1959 - 1996-1998). "
                    "The latter series gives values for 3 year averages, and we have assigned the averages to each individual year.\n\n"
                    "From 2018 the statistics are given in terms of protein content. Previous to this, the amounts of various food categories are given, and we have used "
                    "protein contents found in Matvaretabellen (Mattilsynet, 2006) as this reflects common foods found in Norwegian retail. Population data are taken from SSB "
                    "and we have used the Jones factor of 6.25 for nitrogen content in protein.\n\n"
                    "For pet food, we have assumed (based on available statistics) that cats and dogs consume > 90 % of pet food. Horses are accounted for under the agriculture pool. "
                    "The nitrogen intake per animal per year is taken from Table 19 in (Schäppi, 2025) and the number of cats and dogs between 1985 and 2025 is assumed using "
                    "a trendline based on available statistics from a variety of sources."
                )
            elif "coastal" in norm or ("feed" in norm and "aquaculture" in norm):
                exact_flow_code = "MP.FP-HY.AC-Feed to coastal aquaculture-Nmix"
                display_name = "Feed to Coastal Aquaculture"
                description = (
                    "**MP.FP-HY.AC-Feed to coastal aquaculture-Nmix**: the amount of feed per ton of produced fish is found by assuming an "
                    "average protein (N) retention of 35.37 % based on values from (Aas et al., 2022). The amount of produced fish is found by using data "
                    "from Fiskeridirektoratet (Fiskeridirektoratet, 2025a) on sold farmed fish.\n\n"
                    "(Hohmann-Marriott, 2025) found the nitrogen content in aquaculture feed in 2020 to be 124 ktN, which is very similar to our results."
                )
            elif "untreated" in norm and "fp" in norm:
                exact_flow_code = "MP.FP-HY.SW-Untreated wastewater-Nmix"
                display_name = "Untreated Wastewater (Food Industry)"
                description = (
                    "**MP.FP-HY.SW-Untreated wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to water "
                    "from individual industries, where industries are categorized as belonging to OP or FP, and their connection status to the municipal wastewater, "
                    "based on the information given in the statistic. If no information on connection status was given we have assigned the values to Untreated wastewater. "
                    "The database does not distinguish between emissions to surface and coastal waters, so even though several large industries discharge their wastewater "
                    "to the coast, we assign this entire flow to SW in order to avoid double counting.\n\n"
                    "The values reported before for 1989-1992 are significantly lower than for later years. We therefore extrapolate back to 1990 using the mean value for 1994-1998."
                )
            elif "wastewater" in norm and "fp" in norm:
                exact_flow_code = "MP.FP-PR.WW-Food industry wastewater-Nmix"
                display_name = "Food Industry Wastewater"
                description = (
                    "**MP.FP-PR.WW-Food industry wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to water "
                    "from individual industries, where industries are categorized as belonging to OP or FP, and their connection status to the municipal wastewater, "
                    "based on the information given in the statistic. If no information on connection status was given we have assigned the values to Untreated wastewater. "
                    "The database does not distinguish between emissions to surface and coastal waters, so even though several large industries discharge their wastewater "
                    "to the coast, we assign this entire flow to SW in order to avoid double counting."
                )
            elif "waste" in norm and "fp" in norm:
                exact_flow_code = "MP.FP-PR.SO-Food industry waste-Nmix"
                display_name = "Food Industry Waste"
                description = (
                    "**MP.FP-PR.SO-Food industry waste-Nmix** is food waste from the food industry, including the primary sector (fisheries and slaughter houses). "
                    "We use data from SSB table 05282 “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og kilde” (1995-2011) and 10514 "
                    "«Avfallsregnskap for Norge, etter kilde og materialtype (1 000 tonn) 2012 – 2023» and the category “wet organic waste” with N content from (Schäppi, 2025). "
                    "The statistic does not separate between food and other industry waste. According to (Chaudhary & Skjerpen, 2025) everything in the industry category "
                    "“wet organic waste” is from the food industry.\n\n"
                    "Prior to 2012, the category “wet organic waste” included park- and garden waste and some other mixed waste. The values reported from 1995 to 2011 "
                    "are therefore significantly larger than from 2012. To compensate from this we make the assumption that the 2011 value should have been equal to that in 2012, "
                    "and scale the values prior to 2011 by the ratio between the 2011 and 2012 value. For 1990-1994 we extrapolate using the mean value for years 1995-1999 (5 years)."
                )
            elif "feed" in norm and "export" in norm:
                exact_flow_code = "MP.FP-RW.RW-Feed export-Nmix"
                display_name = "Feed Export"
                description = "Using trade data from SSB, table 08801."
            elif "food" in norm and "export" in norm:
                exact_flow_code = "MP.FP-RW.RW-Food export-Nmix"
                display_name = "Food Export"
                description = "Using trade data from SSB, table 08801."

        # Sorter under øvrig industri (MP.OP)
        elif filename.upper().startswith("MP_OP_"):
            parent_subpool = "Other Producing Industry (MP.OP)"
            
            if "mineral" in norm and "fertilizer" in norm and "export" not in norm and "hs" not in norm:
                exact_flow_code = "MP.OP-AG.SM-Mineral fertilizer-Nmix"
                display_name = "Produced Mineral Fertilizer"
                description = (
                    "**MP.OP-AG.SM-Mineral fertilizer-Nmix** is domestically produced mineral fertilizer used in agriculture, found as "
                    "(total domestic use) – (import), where both use and import are given in FAOSTAT Fertilizer by nutrient (FAO, 2025)."
                )
            elif "n2o" in norm:
                exact_flow_code = "MP.OP-AT.AT-Emissions-N2O"
                display_name = "Industrial Emissions (N2O)"
                description = (
                    "**MP.OP-AT.AT-Emissions-N2O** are taken from UNFCCC common reporting tables, Table 3 as advised by (Schäppi, 2025). "
                    "Emissions are substantial, at least before 2009, and the main source of emissions is from nitric acid production."
                )
            elif "nh3" in norm:
                exact_flow_code = "MP.OP-AT.AT-Emissions-NH3"
                display_name = "Industrial Emissions (NH3)"
                description = "We have used data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by (Schäppi, 2025), using the categories given in Table 20."
            elif "nox" in norm:
                exact_flow_code = "MP.OP-AT.AT-Emissions-NOx"
                display_name = "Industrial Emissions (NOx)"
                description = "We have used data from CLRTAP Inventory Submissions (EMEP, 2025) as advised by (Schäppi, 2025), using the categories given in Table 20."
            elif "fuel" in norm and "waste" in norm:
                exact_flow_code = "MP.OP-EF.IC-Industrial waste fuels-Nmix"
                display_name = "Industrial Waste Fuels"
                description = (
                    "**MP.OP-EF.IC-Industrial waste fuels-Nmix** is wood waste used as biofuel in the industries where the waste originates, reported as "
                    "\"egentilvirket bioenergi\" in the SSB statistic (table 08205). Producers of wood and paper products obtain a significant fraction of their "
                    "energy through this source. “Egentilvirket bioenergi” encompasses “black liquor” as well as wood waste. For lack of better compositional details "
                    "we have assumed values for the entire flow corresponding to wood, although this brings significant uncertainty.\n\n"
                    "The net caloric value of 15.6 for conversion is taken from table 1.2 in (Garg et al., 2006) and we assume a mean N content of 4.0 kg/t "
                    "(between coniferous and non-coniferous wood; see FS.FO-MP.OP-Industrial round wood-Nmix).\n\n"
                    "SSB has not reported data on this energy category before 1998, but the size of these industries was relatively constant through the period 1991-2001 "
                    "(Spilde & Aasestad, 2004). For years 1990-1997 we have therefore used the average for the next 10 years (1998-2007)."
                )
            elif "forest" in norm or "fertilization" in norm:
                exact_flow_code = "MP.OP-FS.FO-Mineral fertilizer-Nmix"
                display_name = "Forest Fertilization Nitrogen"
                description = (
                    "**MP.OP-FS.FO-Mineral fertilizer-Nmix** is nitrogen for forest fertilization. This flow is not part of the guidelines but has been "
                    "added because it is a significant flow in Norway, as was also done in the Swedish NNB (Moldan et al., 2025). We have used data from SSB on "
                    "area of forest fertilized and assumed a standard value of 15 kgN/da (Dalen, 2017). Fertilized area before 1997 is taken from Figure 2 in "
                    "(Landbruksdirektoratet, 2021)."
                )
            elif "consumer" in norm and "goods" in norm:
                exact_flow_code = "MP.OP-HS.HS-Consumer goods-Nmix"
                display_name = "Consumer Goods (Mass Balance)"
                description = (
                    "**MP.OP-HS.HS-Consumer goods-Nmix** is calculated by mass balance, assuming that all incoming flows to OP that are not accounted for "
                    "in outgoing flows end up in domestic consumer goods. We have excluded N2 fixation for ammonia synthesis, and mineral fertilizer flows. "
                    "We also exclude emissions to air from the balance because they result mainly from fertilizer production.\n\n"
                    "**Incoming flows:**\n"
                    "* AG.SM-MP.OP-Crop products for industrial use-Nmix\n"
                    "* AG.MM-MP.OP-Non-edible animal products-Nmix\n"
                    "* PR.SO-MP.OP-Recycling-Nmix\n"
                    "* EF.EC-MP.OP-Fuel used as feedstock-Nmix\n"
                    "* FS.FO-MP.OP-Industrial round wood-Nmix\n"
                    "* RW.RW-MP.OP-Other goods import -Nmix\n\n"
                    "**Outgoing flows:**\n"
                    "* MP.OP-PR.SO-Other industry waste-Nmix\n"
                    "* MP.OP-PR.WW-Other industry wastewater-Nmix\n"
                    "* MP.OP-HY.SW-Untreated wastewater-Nmix\n"
                    "* MP.OP-RW.RW-Other goods export-Nmix\n"
                    "* MP.OP-EF.IC-Industrial waste fuels-Nmix\n\n"
                    "For comparison, (Moldan et al., 2025) found flows from MP to HS of 15.9 ktN in the form of wood products (produced – export – waste) "
                    "and 52.2 ktN in the form of chemical products, also found by mass balance, and identified as “plastics, deicing agents, glue, paint, tensides, etc.”, "
                    "giving a total of 68.1 ktN which, given that the Swedish population is larger than that of Norway, agrees well with our findings."
                )
            elif "mineral" in norm and "fertilizer" in norm and "hs" in norm:
                exact_flow_code = "MP.OP-HS.HS-Mineral fertilizer-Nmix"
                display_name = "Non-Agricultural Mineral Fertilizer"
                description = (
                    "**MP.OP-HS.HS-Mineral fertilizer-Nmix**: as advised by (Schäppi, 2025), we assume a default value of 2% of total mineral "
                    "fertilizer for non-agricultural use. Data for fertilizer use in agriculture are taken from FAOSTAT Fertilizer by nutrient (FAO, 2025)."
                )
            elif "untreated" in norm and "op" in norm:
                exact_flow_code = "MP.OP-HY.SW-Untreated wastewater-Nmix"
                display_name = "Untreated Wastewater (Other Industry)"
                description = (
                    "**MP.OP-HY.SW-Untreated wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to water "
                    "from individual industries, where industries are categorized as belonging to OP or FP based on the information given in the statistic, and counting "
                    "those that are not reported to be connected to municipal wastewater treatment. These emissions are also reported on (Miljødirektoratet, 2025), but "
                    "as of February 2026 the publicly available data did not include information on connection to municipal wastewater. The database does not distinguish "
                    "between emissions to surface and coastal waters, so even though several large industries discharge their wastewater to the coast, we assign this entire "
                    "flow to SW in order to avoid double counting."
                )
            elif "waste" in norm and "op" in norm:
                exact_flow_code = "MP.OP-PR.SO-Other industry waste-Nmix"
                display_name = "Other Industry Waste"
                description = (
                    "**MP.OP-PR.SO-Other industry waste-Nmix**: we use data from SSB table 05282 “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, "
                    "statistikkvariabel, år og kilde” (1995-2011) and 10514 «Avfallsregnskap for Norge, etter kilde og materialtype (1 000 tonn) 2012 – 2023» "
                    "with N contents taken from (Schäppi, 2025) and typical, assumed values are chosen if none are given. The statistic does not separate between food "
                    "and other industry waste. We make the assumption that everything in the category “wet organic waste” is from the food industry, and all other waste "
                    "is assigned to other producing industry. Here we also include all waste from “other industries” (annen eller uspesifisert næring). The category "
                    "“contaminated waste” is very irregularly reported (placed in different sectors in different years) and has therefore been excluded.\n\n"
                    "There is a change in categorization between the two tables, where the main difference is in the category “other waste” and “mixed waste”. To ensure "
                    "continuity between the data series we chose a lower value for “other waste” than for “mixed waste”. Values between 1990 and 1994 are extrapolated "
                    "from 1995 given the change in industry waste reported between 1992 and 1995 reported in (SSB, 1997)."
                )
            elif "wastewater" in norm and "op" in norm:
                exact_flow_code = "MP.OP-PR.WW-Other industry wastewater-Nmix"
                display_name = "Other Industry Wastewater"
                description = (
                    "**MP.OP-PR.WW-Other industry wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to "
                    "water from individual industries, where industries are categorized as belonging to OP or FP based on the information given in the statistic, and counting "
                    "those that are reported to be connected to municipal wastewater treatment. These emissions are also reported on (Miljødirektoratet, 2025), but as of "
                    "February 2026 the publicly available data did not include information on connection to municipal wastewater."
                )
            elif "fertilizer" in norm and "export" in norm:
                exact_flow_code = "MP.OP-RW.RW-Mineral fertilizer export-Nmix"
                display_name = "Mineral Fertilizer Export"
                description = "**MP.OP-RW.RW-Mineral fertilizer export-Nmix** is taken from FAOSTAT Fertilizer by nutrient (FAO, 2025)."
            elif "other" in norm and "goods" in norm and "export" in norm:
                exact_flow_code = "MP.OP-RW.RW-Other goods export-Nmix"
                display_name = "Other Goods Export"
                description = (
                    "**MP.OP-RW.RW-Other goods export-Nmix** is taken from SSB trade data (table 08801) on goods that can be characterized as flowers, chemicals, "
                    "soap, industrial protein, leather, wood and textiles. Ammonia export is also included in this flow."
                )

        # Skriv ut filen for den gjeldende strømmen
        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: {parent_subpool}\n")
            if 'Food' in parent_subpool:
                f.write(f"nav_order: {mp_fp_counter}\n---\n\n")
                mp_fp_counter += 1
            else:
                f.write(f"nav_order: {mp_op_counter}\n---\n\n")
                mp_op_counter += 1

            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n{description}\n\n")
            append_bibtex_references(f, bib_filename)

def process_processing_of_residues_pool(pr_folder, plot_files, plot_dir, bib_filename):
    """Genererer alle sider knyttet til Processing of residues (PR) poolen med [^nøkkel] referanser."""
    # 1. Generer hovedsiden for poolen
    with open(os.path.join(pr_folder, "pool_processing_of_residues.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Processing of residues (PR)\nnav_order: 9\nhas_children: true\n---\n\n")
        f.write("# Pool: Processing of residues (PR)\n\n")
        f.write("This pool accounts for the treatment and processing of waste and wastewater residues in Norway.\n\n")
        f.write(get_balance_image_markdown("PR", plot_files, plot_dir, relative_depth="../"))

    menu_counter = 1
    for filename in plot_files:
        if not (filename.startswith("PR_SO_") or filename.startswith("PR_WW_")):
            continue

        flow_file_name = f"flow_{filename.replace('.png', '')}.md"
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')
        full_flow_path = os.path.join(pr_folder, flow_file_name)

        exact_flow_code, display_name = "PR-Unknown-Flow", "Unknown Residue Flow"
        flow_description = ""

        # Mapping og tekst-tildeling med [^nøkkel] format
        if "prso" in norm and "efec" in norm and "waste" in norm:
            exact_flow_code = "PR.SO-EF.EC-Waste to energy-Nmix"
            display_name = "Waste to energy (Incineration)"
            flow_description = (
                f"**{exact_flow_code}** is found from SSB tables 05281 “Avfallsregnskap for Norge (1 000 tonn), "
                "etter statistikkvariabel, behandlingsmåte, materialtype og år “ (1995-2011) and 10513 “Avfallsregnskap "
                "for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og behandlingsmåte” (2012-2023), "
                "using N content values from [^schappi_2025].\n\n"
                "For years prior to 1995, we use the overall fraction of waste to incineration given in [^ssb_1997] "
                "and assume that the overall N content of the waste is equal to the 1995 value. For years with missing data, "
                "we interpolate."
            )
        elif "prso" in norm and "agsm" in norm and "biologically" in norm:
            exact_flow_code = "PR.SO-AG.SM-Biologically treated organic waste-Nmix"
            display_name = "Biologically treated organic waste to Ag"
            flow_description = (
                f"**{exact_flow_code}** includes all forms of organic waste except sewage sludge that is organically treated "
                "and used in agricultural soils. Biological treatment of organic waste includes both composting and biogas production, "
                "but in Norway, most of the waste composted in the municipal waste sector is used on the private sector, not in agriculture. "
                "We therefore only include biogas digestate in this flow.\n\n"
                "According to Biogass Norge, biogas digestate is produced from sewage sludge, manure, fish waste and sludge, and food waste. "
                "Biogass Norge [^biogass_norge_2025] and personal communication gives data on the amount of nitrogen in digestate "
                "used as fertilizer and in the HS sector from 2021 to 2025. From 2018 to 2020, we use data on the disposal of "
                "biologically produced waste from SSB table 12818 where we find the N content of what is used in agriculture by "
                "scaling the N content of the amount used in 2021 between the SSB table and the data from Biogass Norge.\n\n"
                "From 2012 to 2017, we use data on biogas treatment of different waste categories from SSB table 10513 “Avfallsregnskap "
                "for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og behandlingsmåte” assuming that 85 % of this is "
                "used in agriculture with a loss of 10 % N during biological treatment.\n\n"
                "According to SSB, there were 8 biogas plants in 2011 and 35 in 2017. We therefore assume values before 2012 to be "
                "negligible and set those flows to zero."
            )
        elif "prso" in norm and "atat" in norm and "n2o" in norm:
            exact_flow_code = "PR.SO-AT.AT-Emissions-N2O"
            display_name = "N2O Emissions (Solid Waste)"
            flow_description = f"**{exact_flow_code}** is taken from UNFCCC Common reporting tables, where we have included emissions from landfills, waste incineration and biofuel production."
        elif "prso" in norm and "atat" in norm and "nh3" in norm:
            exact_flow_code = "PR.SO-AT.AT-Emissions-NH3"
            display_name = "NH3 Emissions (Solid Waste)"
            flow_description = f"**{exact_flow_code}**: We have used data from CLRTAP Inventory Submissions [^emep_2025] as advised by [^schappi_2025], using the categories given in Table 48 and 31 (emissions from category 1A1 Energy industries are all assigned to the EF pool)."
        elif "prso" in norm and "atat" in norm and "nox" in norm:
            exact_flow_code = "PR.SO-AT.AT-Emissions-NOx"
            display_name = "NOx Emissions (Solid Waste)"
            flow_description = f"**{exact_flow_code}**: We have used data from CLRTAP Inventory Submissions [^emep_2025] as advised by [^schappi_2025], using the categories given in Table 48 and 31 (emissions from category 1A1 Energy industries are all assigned to the EF pool)."
        elif "prso" in norm and "hshs" in norm and "biologically" in norm:
            exact_flow_code = "PR.SO-HS.HS-Biologically treated organic waste-Nmix"
            display_name = "Biologically treated organic waste to HS"
            flow_description = (
                f"**{exact_flow_code}** includes all forms of organic waste except sewage sludge that is organically treated "
                "and used in agricultural soils. Biological treatment of organic waste includes both composting and biogas production, "
                "but in Norway, most of the waste composted in the municipal waste sector is used on the private sector, not in agriculture.\n\n"
                "SSB statistics on composted organic waste also includes some composted wastewater sludge, but there is no exact statistics "
                "on the amount. Reports indicate that this is a minor (less than 15 % of sludge) and decreasing fraction of sewage sludge, "
                "which is already included in the flows from PR.WW. There is therefore some double counting which serves to make this flow "
                "(PR.SO-HS.HS) artificially large.\n\n"
                "From 2018, we use data on the disposal of biologically produced waste from SSB table 12818 assuming a typical N content "
                "of compost, although a smaller fraction is also biogas digestate.\n\n"
                "For 2012-2017, we use data on composted organic waste from SSB table 10513 “Avfallsregnskap for Norge (1 000 tonn) and "
                "scale the nitrogen value in 2018 with that found from table 12818 for consistency.\n\n"
                "There are no official data prior to 2012, but we know that there was organic waste composted and used in the private sector. "
                "In lack of other data we extrapolate the 2012 value back to 1990."
            )
        elif "prso" in norm and "hysw" in norm and "leaching" in norm:
            exact_flow_code = "PR.SO-HY.SW-Leaching-Nmix"
            display_name = "Leaching from Landfills"
            flow_description = (
                f"**{exact_flow_code}** is taken from [^miljodirektoratet_2026], emissions to water from landfills, where we have "
                "categorized landfills as being connected to municipal wastewater or not based on publicly available data. Where the "
                "categorization was not possible, the resulting emissions have been split evenly between the leaching and wastewater "
                "flows from landfills. As no data are available before 2009 we have extrapolated using the average value. This probably "
                "underestimates the real value because landfilling was more prevalent in previous years."
            )
        elif "prso" in norm and "prww" in norm and "wastewater" in norm:
            exact_flow_code = "PR.SO-PR.WW-Wastewater from landfills-Nmix"
            display_name = "Wastewater from Landfills"
            flow_description = (
                f"**{exact_flow_code}** is taken from [^miljodirektoratet_2026], emissions to water from landfills, where we have "
                "categorized landfills as being connected to municipal wastewater or not based on publicly available data. Where the "
                "categorization was not possible, the resulting emissions have been split evenly between the leaching and wastewater "
                "flows from landfills. As no data are available before 2009 we have extrapolated using the average value. This probably "
                "underestimates the real value because landfilling was more prevalent in previous years."
            )
        elif "prso" in norm and "prww" in norm and "biofuels" in norm:
            exact_flow_code = "PR.SO-PR.WW-Biofuels production wastewater-Nmix"
            display_name = "Biofuels Production Wastewater"
            flow_description = (
                f"**{exact_flow_code}** is found by assuming that the incoming N to biofuel production not retained in digestate ends "
                "up in the wastewater. For details see PR.SO-HS.HS-Digestate fertilizer-Nmix. Values before 2012 are set to zero."
            )
        elif "prso" in norm and "mpop" in norm and "recycling" in norm:
            exact_flow_code = "PR.SO-MP.OP-Recycling-Nmix"
            display_name = "Material Recycling"
            flow_description = (
                f"**{exact_flow_code}** is found from SSB tables 05281 “Avfallsregnskap for Norge (1 000 tonn), etter statistikkvariabel, "
                "behandlingsmåte, materialtype og år “ (1995-2011) and 10513 “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, "
                "statistikkvariabel, år og behandlingsmåte” (2012-2023), using N content values from [^schappi_2025]. We have not "
                "included the categories sludge, garden waste and wet organic material reported as being assigned to material recycling, "
                "because this use is rather for soil production or fertilizer and does not belong in the MP.OP subpool."
            )
        elif "prso" in norm and "rwrw" in norm and "recycling" in norm:
            exact_flow_code = "PR.SO-RW.RW-Export for recycling-Nmix"
            display_name = "Export for Recycling"
            flow_description = f"**{exact_flow_code}** is plastic, paper and textile waste which has been collected for recycling and exported to recycling facilities outside of Norway. Data taken from trade data, SSB table 08801."
        elif "prso" in norm and "rwrw" in norm and "reuse" in norm:
            exact_flow_code = "PR.SO-RW.RW-Export for reuse-Nmix"
            display_name = "Export for Reuse"
            flow_description = f"**{exact_flow_code}** is exported used textiles. Data taken from trade data, SSB table 08801."
        elif "prso" in norm and "rwrw" in norm and "solid" in norm:
            exact_flow_code = "PR.SO-RW.RW-Solid waste export-Nmix"
            display_name = "Solid Waste Export"
            flow_description = f"**{exact_flow_code}** is taken from trade data, SSB table 08801 with N contents taken from Table 50 in [^schappi_2025] for municipal waste, sewage sludge, hazardous and other waste. No export in these categories is reported before 2002, so we set all previous years to zero. The increase seen from 2022 to 2023 is in the category municipal waste."
        
        # --- Wastewater (PR.WW) flows ---
        elif "prww" in norm and "agsm" in norm:
            exact_flow_code = "PR.WW-AG.SM-Sewage sludge fertilizer-Nmix"
            display_name = "Sewage Sludge Fertilizer to Ag"
            flow_description = f"**{exact_flow_code}** is taken from SSB table 05279 “Avløpsslam, etter slamdisponering, statistikkvariabel, år og region”. We use a N content of 2.6 % as given in Table 54 in [^schappi_2025]. For years 1993-2001 we use data from the SSB Naturressurser og miljø series. For years 1990-1992 we use the average value of the 1993-1995."
        elif "prww" in norm and "atat" in norm and "n2" in norm and not "n2o" in norm:
            exact_flow_code = "PR.WW-AT.AT-Emissions-N2"
            display_name = "N2 Emissions (Wastewater)"
            flow_description = f"**{exact_flow_code}** is found by using data on N emissions and removal rates from the six wastewater treatment plants that were equipped with nitrogen removal up to 2025. Where specific data on nitrogen removal fraction were missing we assumed a default 70 %, and we extrapolated or interpolated between existing data where reported emission data were missing. The amount of N released as N2 was calculated as N_released*removal_rate/(1-removal_rate)."
        elif "prww" in norm and "atat" in norm and "n2o" in norm:
            exact_flow_code = "PR.WW-AT.AT-Emissions-N2O"
            display_name = "N2O Emissions (Wastewater)"
            flow_description = f"**{exact_flow_code}** are taken from UNFCCC Common reporting tables, Table 5."
        elif "prww" in norm and "hshs" in norm:
            exact_flow_code = "PR.WW-HS.HS-Sewage sludge fertilizer-Nmix"
            display_name = "Sewage Sludge Fertilizer to HS"
            flow_description = f"**{exact_flow_code}** is taken from SSB table 05279 “Avløpsslam, etter slamdisponering, statistikkvariabel, år og region”, including all sludge used for green areas and for soil production [^schappi_2025]. For years 1993-2001 we use data from the SSB Naturressurser og miljø series. For years 1990-1992 we use the average value of the 1993-1995. We use a N content of 2.6 % as given in Table 54 in [^schappi_2025]."
        elif "prww" in norm and "hycw" in norm:
            exact_flow_code = "PR.WW-HY.CW-Treated wastewater discharge-Nmix"
            display_name = "Treated Wastewater Discharge to CW"
            flow_description = f"**{exact_flow_code}** is taken from SSB table 05280 “Totale utslipp av fosfor og nitrogen fra avløpssektoren (F) 2002 – 2024”. Data back to 1997 are found in the series SSB Naturressurser og miljø. Due to lack of available data we set the values in 1990-1996 to be equal to that in 1997."
        elif "prww" in norm and "prso" in norm and "landfill" in norm:
            exact_flow_code = "PR.WW-PR.SO-Sewage sludge landfill-Nmix"
            display_name = "Sewage Sludge to Landfill"
            flow_description = f"**{exact_flow_code}** is taken from SSB table 05279 “Avløpsslam, etter slamdisponering, statistikkvariabel, år og region”, including both sludge that is landfilled and sludge used for top cover on landfills [^schappi_2025]. For years 1993-2001 we use data from the SSB Naturressurser og miljø series. For years 1990-1992 we use the average value of the 1993-1995. We use a N content of 2.6 % as given in Table 54 in [^schappi_2025]."
        else:
            exact_flow_code = f"PR-Flow-{filename.replace('.png', '')}"
            display_name = f"Residues Flow ({filename.replace('.png', '')})"
            flow_description = f"*Flow details for {exact_flow_code}*"

        # Skriv ut filen
        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: Processing of residues (PR)\nnav_order: {menu_counter}\n---\n\n")
            menu_counter += 1
            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n\n")
            f.write(flow_description + "\n\n")
            append_bibtex_references(f, bib_filename)
            
# ==============================================================================
# HOVEDFUNKSJON (ORKESTRATOR)
# ==============================================================================

def generate_github_pages_report(plot_dir='output_files/plots', output_filename='index.md', bib_filename='library.bib'):
    if not os.path.exists(plot_dir):
        print(f"[INFO] Fant ikke mappen '{plot_dir}'. Rapporten ble ikke laget.")
        return

    plot_files = sorted([f for f in os.listdir(plot_dir) if f.endswith('.png')])
    if not plot_files:
        print(f"[INFO] Ingen plot-filer funnet i '{plot_dir}'.")
        return

    current_date_str = datetime.now().strftime("%B %d, %Y")

    print("[RAPPORT] Sletter gamle midlertidige filer fra rotmappen for å unngå rot...")
    for f_old in os.listdir('.'):
        if (f_old.startswith("flow_") or f_old.startswith("pool_") or f_old.startswith("subpool_")) and f_old.endswith(".md"):
            os.remove(f_old)

    print("[RAPPORT] Bygger hierarkisk dokumentasjonsportal med egne pool-mapper...")

    # 1. Hovedlandingsside
    build_landing_page(output_filename, current_date_str)

    # 2. Atmosphere Pool
    at_folder = "atmosphere_pool"
    os.makedirs(at_folder, exist_ok=True)
    process_atmosphere_pool(at_folder, plot_files, plot_dir, bib_filename)

    # 3. Rest of the World Pool
    rw_folder = "rest_of_the_world_pool"
    os.makedirs(rw_folder, exist_ok=True)
    process_rest_of_the_world_pool(rw_folder, plot_files, plot_dir, bib_filename)

    # 4. Agriculture Pool
    ag_folder = "agriculture_pool"
    os.makedirs(ag_folder, exist_ok=True)
    process_agriculture_pool(ag_folder, plot_files, plot_dir, bib_filename)

    # 5. Forests Pool
    fs_folder = "forests_and_semi_natural_pool"
    os.makedirs(fs_folder, exist_ok=True)
    process_forests_pool(fs_folder, plot_files, plot_dir, bib_filename)

    # 6. Hydrosphere Pool
    hy_folder = "hydrosphere_pool"
    os.makedirs(hy_folder, exist_ok=True)
    process_hydrosphere_pool(hy_folder, plot_files, plot_dir)

    # 7. Humans and Settlements Pool
    hs_folder = "humans_and_settlements_pool"
    os.makedirs(hs_folder, exist_ok=True)
    process_humans_and_settlements_pool(hs_folder, plot_files, plot_dir, bib_filename)

    # 8. Energy and Fuels Pool
    ef_folder = "energy_and_fuels_pool"
    os.makedirs(ef_folder, exist_ok=True)
    process_energy_and_fuels_pool(ef_folder, plot_files, plot_dir, bib_filename)
    
    # 9. Materials and Products Pool
    mp_folder = "materials_and_products_pool"
    os.makedirs(mp_folder, exist_ok=True)
    process_materials_pool(mp_folder, plot_files, plot_dir, bib_filename)
    
    # 10. Materials and Products Pool
    mp_folder = "materials_and_products_pool"
    os.makedirs(mp_folder, exist_ok=True)
    process_materials_pool(mp_folder, plot_files, plot_dir, bib_filename)

    # === NYTT TILLEGG: Processing of residues Pool ===
    pr_folder = "processing_of_residues_pool"
    os.makedirs(pr_folder, exist_ok=True)
    process_processing_of_residues_pool(pr_folder, plot_files, plot_dir, bib_filename)

    print("[RAPPORT] Portalbygging fullført suksessfullt!")

    print("[RAPPORT] Portalbygging fullført suksessfullt!")