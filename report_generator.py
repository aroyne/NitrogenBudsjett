# report_generator.py
import os
# import shutil
import re
from datetime import datetime
# from pybtex.database import parse_file

# ==============================================================================
# FELLES TEKSTBLOKKER OG HJELPEFUNKSJONER
# ==============================================================================

DEPOSITION_TEXT = (
    "Atmospheric deposition was calculated using data from NILU which gives gridded "
    "deposition data for both oxidized and reduced N as averages for periods 1983-1987, "
    "1988-1992, 1997-2001, 2002-2006, 2007-2011 and 2012-2016. For 2017-2021 we use "
    "total NILU data for that period and scale with the distribution across land classes "
    "for the previous period. Values after 2021 are extrapolated. To find deposition on "
    "different land categories we use the map resource AR5 from NIBIO \\\\citet{nibio_ar5_2016}. "
    "We find the total value of atmospheric deposition to the Norwegian mainland is, "
    "as given by NILU, 142 ktN in 2012-2016.\n\n"
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


def append_bibtex_references(file_handle, bib_filename=None):
    """
    Skanner filen for siteringer (\citep{key}), leser bib-filen,
    og genererer en ren Markdown-referanseliste som fungerer på GitHub Pages.
    """
    if not bib_filename or not os.path.exists(bib_filename):
        file_handle.write("\n### References\n\nNo bibliography file provided or found.\n")
        return

    # 1. Gå til starten av filen og les alt som er skrevet hittil for å finne siteringsnøkler
    file_handle.flush()
    try:
        with open(file_handle.name, 'r', encoding='utf-8') as f_read:
            content = f_read.read()
    except Exception:
        # Hvis filen ikke kan leses (f.eks. hvis den er låst/i skrivemodus),
        # legger vi til en fallback-tagg eller melding
        file_handle.write("\n### References\n\n(References dynamically generated via Python require file readability)\n")
        return

    # Finn alle nøkler inni \citep{nøkkel} eller \citet{nøkkel}
    # Støtter også kommaseparerte lister, f.eks. \citep{key1,key2}
    raw_keys = re.findall(r'\\cite[pt]\{\s*([^}]+)\s*\}', content)
    cited_keys = set()
    for k_group in raw_keys:
        for k in k_group.split(','):
            cited_keys.add(k.strip())

    if not cited_keys:
        return  # Ingen referanser ble brukt på denne siden, trenger ikke referanse-overskrift

    # 2. Enkel parsing av .bib-filen for å hente ut forfatter, år og tittel
    references_dict = {}
    current_entry = None
    
    with open(bib_filename, 'r', encoding='utf-8') as bib_file:
        for line in bib_file:
            line_stripped = line.strip()
            # Finn starten på en entry, f.eks. @article{malik_drivers_2022,
            match_start = re.match(r'@\w+\{\s*([^,]+),', line_stripped)
            if match_start:
                current_entry = match_start.group(1).strip()
                references_dict[current_entry] = {}
                continue
            
            if current_entry and '=' in line_stripped:
                key, val = line_stripped.split('=', 1)
                key = key.strip().lower()
                # Fjern krøllparenteser, hermetegn og komma på slutten
                val = re.sub(r'[{"},\s]+$', '', val.strip())
                val = re.sub(r'^[{"\s]+', '', val)
                if key in ['author', 'title', 'year', 'journal', 'booktitle']:
                    references_dict[current_entry][key] = val

    # 3. Bygg referanselisten (i tilnærmet APA-stil) for akkurat de kildene som er brukt
    file_handle.write("\n### References\n\n")
    
    formatted_refs = []
    for key in sorted(cited_keys):
        if key in references_dict:
            entry = references_dict[key]
            author = entry.get('author', 'Unknown Author')
            year = entry.get('year', 'n.d.')
            title = entry.get('title', 'Untitled')
            source = entry.get('journal') or entry.get('booktitle') or ""
            
            ref_str = f"* {author} ({year}). *{title}*."
            if source:
                ref_str += f" {source}."
            formatted_refs.append(ref_str)
        else:
            # Hvis nøkkelen ikke ble funnet i .bib-filen
            formatted_refs.append(f"* Missing reference data for key: `{key}`")

    # Skriv listen til filen
    for ref in formatted_refs:
        file_handle.write(f"{ref}\n")
    
def format_apa_authors(author_str):
    """
    Tar en BibTeX author-streng (f.eks. 'Winiwarter, Wilfried and Hayashi, Kentaro')
    og formaterer den til APA7: 'Winiwarter, W., Hayashi, K., & ...'
    """
    if not author_str or author_str == 'Unknown Author':
        return 'Unknown Author'
    
    # BibTeX separerer forfattere med " and "
    raw_authors = author_str.split(" and ")
    formatted_names = []
    
    for auth in raw_authors:
        auth = auth.strip()
        if "," in auth:
            # Format: Etternavn, Fornavn [Mellomnavn]
            parts = auth.split(",", 1)
            last_name = parts[0].strip()
            first_names = parts[1].strip().split()
            
            # Gjør fornavn om til initialer (f.eks. Wilfried -> W.)
            initials = []
            for name in first_names:
                # Sjekk om det allerede er en initial eller forkortelse
                if name.endswith('.'):
                    initials.append(name)
                else:
                    initials.append(f"{name[0]}.")
            
            initials_str = " ".join(initials)
            formatted_names.append(f"{last_name}, {initials_str}")
        else:
            # Fallback hvis navnet ikke har komma (f.eks. organisasjoner som NIBIO)
            formatted_names.append(auth)
            
    # Sett sammen navnene i henhold til APA7-regler for lister
    num_authors = len(formatted_names)
    if num_authors == 1:
        return formatted_names[0]
    elif num_authors == 2:
        return f"{formatted_names[0]} & {formatted_names[1]}"
    else:
        # APA7 bruker komma før og-tegnet (&) ved 3 eller flere forfattere
        all_but_last = ", ".join(formatted_names[:-1])
        return f"{all_but_last}, & {formatted_names[-1]}"
    

def fix_all_citations_in_folder(folder_path, bib_filename):
    if not os.path.exists(bib_filename):
        print(f"Bib-fil ikke funnet: {bib_filename}")
        return

    # 1. Pars .bib-filen
    references_dict = {}
    current_entry = None
    
    with open(bib_filename, 'r', encoding='utf-8') as bib_file:
        for line in bib_file:
            line_stripped = line.strip()
            match_start = re.match(r'@\w+\{\s*([^,]+),', line_stripped)
            if match_start:
                current_entry = match_start.group(1).strip()
                references_dict[current_entry] = {}
                continue
            
            if current_entry and '=' in line_stripped:
                key, val = line_stripped.split('=', 1)
                key = key.strip().lower()
                
                val = re.sub(r'[{"},\s]+$', '', val.strip())
                val = re.sub(r'^[{"\s]+', '', val)
                
                if key in ['url', 'doi']:
                    val = val.rstrip(']')
                
                if key in ['author', 'year', 'title', 'journal', 'booktitle', 'publisher', 'url', 'doi']:
                    references_dict[current_entry][key] = val

    # Interne hjelpefunksjoner for siteringer i teksten (\citep og \citet)
    def citep_replacer(match):
        keys = [k.strip() for k in match.group(1).split(',')]
        parts = []
        for key in keys:
            if key in references_dict:
                author = references_dict[key].get('author', 'Unknown')
                short_author = author.split(',')[0].strip()
                year = references_dict[key].get('year', 'n.d.')
                parts.append(f"{short_author}, {year}")
            else:
                parts.append(key)
        return f"({'; '.join(parts)})"

    def citet_replacer(match):
        keys = [k.strip() for k in match.group(1).split(',')]
        parts = []
        for key in keys:
            if key in references_dict:
                author = references_dict[key].get('author', 'Unknown')
                short_author = author.split(',')[0].strip()
                year = references_dict[key].get('year', 'n.d.')
                parts.append(f"{short_author} ({year})")
            else:
                parts.append(f"{key} (n.d.)")
        return ", ".join(parts)

    # 2. Gå igjennom alle filer
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(root, filename)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '\\citep' in content or '\\citet' in content:
                    raw_keys = re.findall(r'\\+cite[pt]\{\s*([^}]+)\s*\}', content)
                    cited_keys = set()
                    for k_group in raw_keys:
                        for k in k_group.split(','):
                            cited_keys.add(k.strip())
                    
                    updated_content = re.sub(r'\\+citep\{\s*([^}]+)\s*\}', citep_replacer, content)
                    updated_content = re.sub(r'\\+citet\{\s*([^}]+)\s*\}', citet_replacer, updated_content)
                    
                    if "### References" in updated_content:
                        base_content = updated_content.split("### References")[0].strip()
                    else:
                        base_content = updated_content.strip()
                        
                    ref_block = "\n\n### References\n\n"
                    formatted_refs = []
                    
                    for key in sorted(cited_keys):
                        if key in references_dict:
                            entry = references_dict[key]
                            
                            # Formater forfattere etter APA7-regler
                            raw_author = entry.get('author', 'Unknown Author')
                            author = format_apa_authors(raw_author)
                            
                            year = entry.get('year', 'n.d.')
                            title = entry.get('title', 'Untitled')
                            
                            # Hent kilde/utgiver
                            source = entry.get('journal') or entry.get('booktitle') or entry.get('publisher') or ""
                            
                            doi = entry.get('doi', '')
                            url = entry.get('url', '')
                            
                            # 1. Forfatter (År).
                            ref_str = f"* {author} ({year})."
                            
                            # 2. Tittel i kursiv
                            ref_str += f" *{title}*."
                            
                            # 3. Kilde/Utgiver (hvis den ikke er identisk med forfatteren, f.eks. NIBIO)
                            if source and source.lower() != raw_author.lower():
                                # Fjern eventuelle backslasher BibTeX legger til før tegn (f.eks. \& -> &)
                                source_clean = source.replace(r'\&', '&')
                                ref_str += f" {source_clean}."
                                
                            # 4. Lenke-håndtering i APA7: Prioriter alltid DOI over URL
                            if doi:
                                # Standardiser DOI-lenken slik at den alltid blir en gyldig https://doi.org/...
                                doi_clean = doi.lower().replace("doi.org/", "").replace("https://", "").replace("http://", "")
                                doi_url = f"https://doi.org/{doi_clean}"
                                ref_str += f" [{doi_url}]({doi_url})"
                            elif url:
                                ref_str += f" [{url}]({url})"
                                
                            formatted_refs.append(ref_str)
                        else:
                            formatted_refs.append(f"* Missing reference data for key: `{key}`")
                            
                    ref_block += "\n".join(formatted_refs) + "\n"
                    final_content = base_content + ref_block
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    print(f"Oppdaterte referanser (APA7-vask) i filen: {filename}")

                    
# ==============================================================================
# SPESIFIKKE FUNKSJONER FOR HVER ENKELT POOL
# ==============================================================================

def build_landing_page(output_filename, current_date_str, bib_filename):
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
        f.write("and access detailed statistical time-series graphs, methodological explanations, and parameterizations for each specific flow.\n\n")
        f.write("For flows connected to the hydrosphere, and for land-relateds emissions and nitrogen deposition, "
                "we only consider the Norwegian mainland. For emissions to air reported through the UNFCCC framework we "
                "also include emissions from Norwegian economic activity on Svalbard (these are minor and mainly related to coal extraction, "
                "which has now been discontinued). We also include emissions and N flows that originate in petroleum extraction on the Norwegian "
                "continental shelf.\n"
                "This NNB is built using the guidelines from \\citep{winiwarter_inms_2025}. Where flows are omitted or added to better fit "
                "the Norwegian nitrogen system, this is commented. ")
        append_bibtex_references(f, bib_filename)
        
        


def process_atmosphere_pool(at_folder, plot_files, plot_dir, bib_filename):
    """Genererer alle sider knyttet til Atmosphere (AT) poolen med ren LaTeX-siteringssyntaks."""
    with open(os.path.join(at_folder, "pool_atmosphere.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Atmosphere (AT)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Pool: Atmosphere (AT)\n\nThis section contains all documented nitrogen flows leaving the Atmosphere pool.\n")
        f.write(get_balance_image_markdown("AT", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **AT.AT-EF.EC-Combustion N2 fixation-N2**, **AT.AT-EF.IC-Combustion N2 fixation-N2** and **AT.AT-EF.OE-Combustion N2 fixation-N2** "
                "are neglected because we have chosen to ignore nitrogen fixation in combustion processes. In fuel combustion, some bound N is "
                "converted to NOx, and some atmospheric N2 is also converted to N2. The amount of resulting NOx depends on the combustion conditions "
                "and on the use of catalytic converters. It is possible to estimate an N2 fixation rate based on mass balance, but we have chosen not "
                "to do so because it does not add useful understanding of the flows of reactive N in the NNB.\n")
        f.write("* **AT.AT-HY.CW-Deposition-OXN**, **AT.AT-HY.CW-Deposition-RDN** and **AT.AT-HY.CW-N2 fixation-N2** are neglected because we lack an "
                "accurate area for coastal waters and do not attempt to make a mass balance for CW. \n")


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
                # Byttet ut [ukjent_nøkkel] med en narrativ LaTeX-sitatvariant \citet{}
                f.write(f"""**{exact_flow_code}**
                    \\citet{{schappi_annexes_2025}} advises using data from the EUROSTAT Gross nutrient balance, but there \
                    is an error in this dataset for Norway which is currently being corrected (as of February 2026; personal correspondence, \
                    EUROSTAT). According to the EUROSTAT metadata, the BNF in this statistic is calculated based on the area of leguminous crops and \
                    fization coefficients. The production of leguminous crops (peas, beans etc) in Norway is very low and we assume that agricultural \
                    BNF is for the most part determined by leguminous crops such as clover grown on pastures and in fodder production. \
                    \\citet{{bleken_nitrogen_1997}} based their estimate for BNF from the sale of clover seeds: a sale of about 145 t seeds was \
                    estimated to be used to plant 95 000 ha of grass/clover mixtures (655 ha/t seeds). Together with a rate of BNF of 80 kgN/ha on \
                    this area, they found a total of 7.6 ktN per year and summed up to 8 ktN to account for BNF from free-living orghanisms and \
                    other sources. The rate of 80 kgN/ha agrees relatively well with later studies of agricultural BNF in Norway, where average \
                    values between 10 and 100 kgN/ha have been found; the highest values in particularly productive areas were up to 260 kgN/ha \
                    (https://orgprints.org/id/eprint/37546/1/NORSØK%20Rapport%20nr.%203%202020%20Engbelgvekster.pdf). Yearly statistics of clover \
                    seed sales are not available, but according to NIBIO Totalkalkylen (NIBIO, 2025b), the area where grass/clover mixes may be \
                    sown for pasture and fodder production (fulldyrka eng) has remained constant to within about 3 % from 1995 up to today. Our \
                    best estimate for BNF, and for consistency with the previous study, is therefore to assume a constant value of 8 ktN/year. \
                    In Sweden \\citep{{moldan_where_2025}} the value was found to be 34 kT in 2015, which is more in line with the values found before 2000.""")
            elif exact_flow_code in ["AT.AT-FS.FO-Deposition-OXN", "AT.AT-FS.FO-Deposition-RDN", "AT.AT-FS.OL-Deposition-OXN", "AT.AT-FS.OL-Deposition-RDN", "AT.AT-HS.HS-Deposition-OXN", "AT.AT-HS.HS-Deposition-RDN"]:
                f.write(f"**{exact_flow_code}**\n\n" + DEPOSITION_TEXT + "\n\n")
            elif exact_flow_code in ["AT.AT-HY.SW-Deposition-RDN","AT.AT-HY.SW-Deposition-RDN"]:
                f.write(f"**{exact_flow_code}**\n\n" + DEPOSITION_TEXT + "For comparison, the data used in the TEOTIL model gives 3.5 ktN in 2013 and "
                        "3.0 ktN in 2023. These comparable but slightly lower values are the results of different datasets used and different data "
                        "treatment. ")
            elif exact_flow_code in ["AT.AT-AG.SM-Deposition-OXN", "AT.AT-AG.SM-Deposition-RDN"]:
                f.write(f"**{exact_flow_code}**\n\n" + DEPOSITION_TEXT + "\n\nAs noted, our value for agricultural soils is much larger than given by ""FAOSTAT. "
                        "\\\\citet{hohmann-marriott_nitrogen_2025} used values from \\\\citet{blake_deposition_2023} to arrive at an average "
                        "N deposition rate of 80.85 ktN for the period 2017-2021. \\\\citet{hohmann-marriott_nitrogen_2025} "
                        "also reported values of 74.7 and 33.5 ktN per year using two different methods "
                        "for estimating biome-dependent N deposition rates.")
            elif exact_flow_code == "AT.AT-FS.FO-N2 fixation-N2":
                f.write(f"**{exact_flow_code}**\n\n" + "\n\nFollowing the Swedish NBB \\cite{{moldan_where_2025}}, we use an N-fixation "
                        "rate of 1.5 kg/ha/year and a forested area of 12.0 mill ha as given by SSB for 2019-2023 (table 14368); we assume this value is "
                        "constant for our entire time period. This gives an annual N-fixation rate of 18.0 ktN. For comparison, the value for Sweden "
                        "in 2015 was found to be 39.5 ktN \\cite{{moldan_where_2025}}. IN PROGRESS")
            elif exact_flow_code == "AT.AT-FS.OL-N2 fixation-N2":
                f.write(f"**{exact_flow_code}**\n\n" + "\n\nIN PROGRESS")
            elif exact_flow_code == "AT.AT-HY.SW-N2 Fixation-N2":
                f.write(f"**{exact_flow_code}**\n\n" + "According to NIBIO, the surface water area is 20 457 km2 "
                        "https://arealbarometer.nibio.no/nb/norge/. According to  \\citep{{schappi_annexes_2025}}, the biological fixation rate can vary "
                        "between < 0.1 tN/km2 in ologotrophic and mesotrophic lakes to up to 10 tN/km2 in eutrophic lakes. Most lakes in Norway are not "
                        "eutrophic and we use a low value of 0.1 tN/km2, which gives 2 ktN/year.")
            elif exact_flow_code == "AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2":
                f.write(f"**{exact_flow_code}**\n\n" + "is found through mass balance where we use data from FAOSTAT Fertilizer by nutrient, domestic "
                        "fertilizer production, and subtracted the amount of ammonia imported from SSB trade data (table 08801). The result is a very "
                        "variable curve which probably does not reflect year to year production well and could be a result of how trade statistics are "
                        "reported.")
            elif exact_flow_code == "AT.AT-RW.RW-Atmospheric outflow-OXN":
                f.write(f"**{exact_flow_code}**\n\n" + "is found using source-receptor data from \\citep{{emep_sr_2024}}, as advised by \\citep{{schappi_annexes_2025}}.")
            elif exact_flow_code == "AT.AT-RW.RW-Atmospheric outflow-RDN":
                f.write(f"**{exact_flow_code}**\n\n" + "is found using source-receptor data from \\citep{{emep_sr_2024}}, as advised by \\citep{{schappi_annexes_2025}}.")
            else:
                f.write(f"*Flow details for {exact_flow_code}*\n\n")

            # Kaller din oppdaterte versjon som kun skriver ut `{% bibliography --cited %}`
            append_bibtex_references(f, bib_filename)

def process_rest_of_the_world_pool(rw_folder, plot_files, plot_dir, bib_filename):
    """Genererer alle sider knyttet til Rest of the World (RW) poolen med oppdaterte LaTeX-sitat-referanser."""
    with open(os.path.join(rw_folder, "pool_rest_of_the_world.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Rest of the world (RW)\nnav_order: 3\nhas_children: true\n---\n\n")
        f.write("# Pool: Rest of the world (RW)\n\nThis section contains all documented nitrogen inflows and transfers originating from the Rest of the world (RW) pool. ")
        f.write("Click on the individual sub-flows in the left-hand menu to view graphs and methodological explanations.\n\n")
        f.write(get_balance_image_markdown("RW", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **RW.RW-MP.FP-Sea fish (landings)-Nmix** is set to zero because all wild fish catch is accounted for under HY.\n")
        f.write("* **RW.RW-AG.SM-Manure import-Nmix** is assumed small and neglected based on regional boundary assumptions for agricultural surpluses \\\\citep{schulte-uebbing_planetary_2022}.\n")
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
                "We assume a constant import fraction of 0.92 as given by \\citet{aas_utilization_2022} for the year 2020. "
                "The amount of feed used is based on the amount of fish produced, calculated using data from \\citet{fiskeridirektoratet_06002_2025}"
                "on sold farmed fish, assuming average protein (N) retention of 35,75 % \\citep{aas_utilization_2022}, 2.8 % nitrogen content "
                "in fish and shellfish  \\citet{schappi_annexes_2025}, p. 254) and 3% feed waste \citet{wang_chemical_2013}."
            )
        elif "feed" in norm and "animal" in norm:
            exact_flow_code = "RW.RW-AG.MM-Animal feed import-Nmix"
            display_name = "Animal Feed Import"
            description = (
                "Data on imported animal feed is taken from Landbruksdirektoratet and we have used the detailed "
                "composition of animal feed together with protein contents from FAO and specific Jones factors to get nitrogen contents.\n\n "
                "Based on the Landbruksdirektoratet data, the N content of the total amount of feed is 0.02 kgN/kg feed. "
                "NIBIO Totalkalkylen gives statistics for total amount of feed to Norwegian farm animals between 1959 and 2026Table 6.10 in "
                "\\citep{bruholt_jordbruksstatistikk_1994} gives the domestically produced fraction of farm animal feed between 1985 and 1994. "
                "We combine these data to find values before 2000, using an average import fraction for 1995-1999"
            )
        elif "live" in norm and "animal" in norm:
            exact_flow_code = "RW.RW-AG.MM-Live animal import-Nmix"
            display_name = "Live Animal Import"
            description = (
                "Is taken from FAOSTAT Crops and livestock products, assuming typical weights of animals from various sources, "
                "average 16% protein in whole animal and Jones factor 6.25 for nitrogen to protein (standard)."
            )
        elif "mineral" in norm and "fertilizer" in norm:
            exact_flow_code = "RW.RW-AG.SM-Mineral fertilizer import-Nmix"
            display_name = "Mineral Fertilizer Import"
            description = (
                "Is taken from FAOSTAT Fertilizer by nutrient \\citet{fao_fertilizer_2025}. Because anhydrous "
                "ammonia is not used directly as fertilizer in Norway, it is not counted as a fertilizer in this particular FAO statistic. "
                "We therefore include NH3 import in the flow **RW.RW-MP.OP-Other goods import-Nmix**."
            )
        elif "inflow" in norm and "oxn" in norm:
            exact_flow_code = "RW.RW-AT.AT-Atmospheric inflow-OXN"
            display_name = "Atmospheric Inflow (Oxidized N)"
            description = (
                "Is found from source-receptor data from EMEP, as advised by \\citep{schappi_annexes_2025}. There is a change "
                "in methodology in the EMEP reporting between 2002 and 2003 data."
            )
        elif "inflow" in norm and "rdn" in norm:
            exact_flow_code = "RW.RW-AT.AT-Atmospheric inflow-RDN"
            display_name = "Atmospheric Inflow (Reduced N)"
            description = (
                "Is found from source-receptor data from EMEP, as advised by \\citep{schappi_annexes_2025}. There is a change "
                "in methodology in the EMEP reporting between 2002 and 2003 data."
            )
        elif "fuel" in norm and "import" in norm and "transport" not in norm:
            exact_flow_code = "RW.RW-EF.EC-Fuel import-Nmix"
            display_name = "Fuel Import"
            description = (
                "Is taken from trade data, SSB table 08801 for all fuel items except those for transport."
            )
        elif "transport" in norm and "fuel" in norm:
            exact_flow_code = "RW.RW-EF.TR-Import of transport fuel-Nmix"
            display_name = "Transport Fuel Import"
            description = "Is taken from trade data, SSB table 08801 for all fuel items for transport."
        elif "food" in norm and "import" in norm:
            exact_flow_code = "RW.RW-MP.FP-Food import-Nmix"
            display_name = "Food Import"
            description = (
                "Is taken from trade data, SSB table 08801."
            )
        elif "ammonia" in norm and "import" in norm:
            exact_flow_code = "RW.RW-MP.OP-Ammonia import-Nmix"
            display_name = "Ammonia Import"
            description = (
                "Is taken from trade data, SSB table 08801."
            )
        elif "other" in norm and "goods" in norm:
            exact_flow_code = "RW.RW-MP.OP-Other goods import-Nmix"
            display_name = "Other Goods Import"
            description = (
                "Is taken from trade data, SSB table 08801. Import of N2 is a large contributor but not included here because it "
                "does not contribute to the reactive nitrogen cycle."
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
            
            # Legger til bibliografitaggen for den gitte siden ({% bibliography --cited %})
            append_bibtex_references(f, bib_filename)
            
            
def process_agriculture_pool(ag_folder, plot_files, plot_dir, bib_filename):
    """Genererer hovedsiden, subpools og alle strømmer for Agriculture (AG) med oppdatert LaTeX-syntaks."""
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
        f.write("\n### Flows that are zero or neglected:\n\n* **AG.MM-RW.RW-Manure export-Nmix** is assumed small and neglected.\\\\citep{schulte-uebbing_planetary_2022}\n")
        f.write("\n\n* **AG.MM-PR.SO-Manure for biofuel production-Nmix** is neglected because the Eurostat data used to calculate manure "
                "application to soil includes manure that has been processed for biogas. SSB table 12359 gives the amount of manure processed "
                "for biogas or through composting. Composting values are negligible compared with biogas.  The nitrogen content of manure for "
                "biogas production is found to rise from zero before 2012 to around 0.5 kt/year in 2023 (data from "
                "\citet{landbruksdirektoratet_biogass_2025}, a value which is still negligible compared with the total amount of manure "
                "application. We therefore do not introduce a correction for the amount of nitrogen lost through biogas processing.  ")

    with open(os.path.join(ag_folder, "subpool_soil_management.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Soil Management (AG.SM)\nparent: Agriculture (AG)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Subpool: Soil management (AG.SM)\n\n")
        f.write(get_balance_image_markdown("AG.SM", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **AG.SM-HY.SW-Overland flow-Nmix**, **AG.SM-FS.OL-Overland flow-Nmix** "
                "and **AG.SM-FS.WL-Overland flow-Nmix** are neglected as suggested by \\\\citet{schappi_annexes_2025}: "
                "«In a first approximation it can be assumed that N losses to hydrosphere or forests and semi-natural vegetation occur "
                "mainly via leaching. If no country specific data is available on fractions for overland flow of N, the overland flows can "
                "be neglected for simplification purposes». is not included because all runoff and leaching is included in Leaching.\n"
                "* **AG.SM-PR.SO-Farm crops substrate-Nmix** is farm crops substrate for biofuels production and composting. According "
                "to data in SSB table 12359 «Biologisk behandling av avfall, etter materialtype (1 000 tonn) 2017 – 2023» for category "
                "«Landbruksavfall, etande”, these values are small enough to be neglected. Since we only have values given for a few years, "
                "we have chosen to neglect this flow.\n" 
                "* **AG.SM-HY.SW-Overland flow-Nmix** is not included because all runoff and leaching is included in  **AG.SM-HY.SW-Leaching-Nmix**.\n"
                )

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
                description = "Taken from EUROSTAT Gross nutrient balance as advised by \\\\citet{schappi_annexes_2025}. We interpolate the missing values between 2016 and 2020."
            elif "n2o" in norm:
                exact_flow_code = "AG.MM-AT.AT-Emissions-N2O"
                display_name = "Manure Emissions (N2O)"
                description = "Taken from UNFCCC Common reporting tables, Table 3."
            elif "nh3" in norm:
                exact_flow_code = "AG.MM-AT.AT-Emissions-NH3"
                display_name = "Manure Emissions (NH3)"
                description = "We have used data from CLRTAP Inventory Submissions \\\\citep{emep_officially_2025} as advised by \\\\citet{schappi_annexes_2025}, using the categories given in Table 29."
            elif "nox" in norm:
                exact_flow_code = "AG.MM-AT.AT-Emissions-NOx"
                display_name = "Manure Emissions (NOx)"
                description = "We have used data from CLRTAP Inventory Submissions \\\\citep{emep_officially_2025} as advised by \\\\citet{schappi_annexes_2025}, using the categories given in Table 29."
            elif "leaching" in norm:
                exact_flow_code = "AG.MM-HY.SW-Leaching-Nmix"
                display_name = "Manure Leaching"
                description = "Taken from UNFCCC Common reporting tables, Table 3."
            elif "product" in norm and "nonedible" not in norm and "op" not in norm:
                exact_flow_code = "AG.MM-MP.FP-Animal products-Nmix"
                display_name = "Animal Products"
                description = "Taken from FAOSTAT Crops and livestock products, with N contents taken from \\\\citet{schappi_annexes_2025}."
            elif "nonedible" in norm or "wool" in norm or ("animal" in norm and "op" in norm):
                exact_flow_code = "AG.MM-MP.OP-Non-edible animal products-Nmix"
                display_name = "Non-edible Animal Products"
                description = "\\\\citet{schappi_annexes_2025} advises using FAOSTAT Commodity Balances (non-food). For Norway this statistic "
                "only contains wool for 4 individual years and we therefore use data for wool from Landbruksdirektoratet "
                "\\\\citep{landbruksdirektoratet_leveransedata-slakt-2005-2012_2025} for 2005-2024; for earlier years, we use the number of "
                "sheep (SSB table 03710) and extrapolate from a linear regression found between sheep and wool for 2005-2024. In addition, "
                "we use numbers for raw hides and skins from FAOSTAT Crops and livestock products. N contents are taken from "
                "\\\\citet{schappi_annexes_2025}."
            elif "export" in norm or "live" in norm:
                exact_flow_code = "AG.MM-RW.RW-Live animal export-Nmix"
                display_name = "Live Animal Export"
                description = "Taken from FAOSTAT Crop and livestock products, assuming typical weights of animals from various sources, average "
                "16 % protein in whole animal based on typical values in \\\\citet{schappi_annexes_2025} and Jones factor 6.25 for nitrogen to "
                "protein (standard) "

        elif filename.upper().startswith("AG_SM_"):
            parent_subpool = "Soil Management (AG.SM)"
            if "fodder" in norm or "grass" in norm:
                exact_flow_code = "AG.SM-AG.MM-Fodder crops-Nmix"
                display_name = "Fodder Crops Production"
                description = "We have used data for grass and fodder production from SSB table 13648 «Avling i jordbruket (1000 tonn) og avling "
                "per dekar (kg), etter ymse jordbruksvekstar (F) 2021 – 2024» and 05772 «Avling i jordbruket, etter ymse jordbruksvekstar (1 000 tonn) "
                "(F) (avslutta serie) 2000 – 2020». Values prior to 2000 are found in the SSB Jordbruksstatistikk (Table 2.1/Table 20). The protein "
                "content of grass and fodder is known to be highly variable. We have assumed a protein content of 15 % based on 2025 analyses of "
                "13 000 grass samples from all over Norway by Tine/NorFor, and 15 % N in protein (FAO, 2003). \n\n"
                "\citet{hohmann-marriott_nitrogen_2025} used similar data sources but arrived at a smaller N flow (40-45 ktN) using a protein content "
                "of 8 % and N content in protein of 15 % (Table S2).  "
            elif "emissionsn2" in norm:
                exact_flow_code = "AG.SM-AT.AT-Emissions-N2"
                display_name = "N2 emissions from denitrification"
                description = "\\\\citet{schappi_annexes_2025} recommends using a value of 14 kgN/ha/year for denitrification if no other data are available. "
                "Together with a total agricultural area of 1 132 693 ha (NIBIO, 2026) this gives around 16 ktN/year."
            elif "emissionsn2o" in norm:
                exact_flow_code = "AG.SM-AT.AT-Emissions-N2O"
                display_name = "N2O emissions from denitrification"
                description = "N2O emissions are taken from UNFCCC Common reporting tables, Table 3"
            elif "emissionsnox" in norm:
                exact_flow_code = "AG.SM-AT.AT-Emissions-NOx"
                display_name = "NOx emissions from soil management"
                description = "We have used data from CLRTAP Inventory Submissions \\citet{emep_officially_2025} as advised by \\\\citet{schappi_annexes_2025}, using the categories "
                "given in Table 30. "
            elif "emissionsnh3" in norm:
                exact_flow_code = "AG.SM-AT.AT-Emissions-NH3"
                display_name = "NH3 emissions"
                description = "We have used data from CLRTAP Inventory Submissions \\citet{emep_officially_2025} as advised by \\\\citet{schappi_annexes_2025}, using the categories "
                "given in Table 30. "
            elif "leaching" in norm:
                exact_flow_code = "AG.SM-HY.SW-Leaching-Nmix"
                display_name = "Leaching from soil management"
                description = "Leaching from soil management is taken from UNFCCC Common reporting tables, Table 3. The data agrees within the error "
                "range with what is reported in the TEOTIL3 \\citet{model sample_kildefordelte_2024}"
            elif "foodcrop" in norm:
                exact_flow_code = "AG.SM-MP.FP-Food crop products-Nmix"
                display_name = "Food crop products"
                description = "Food crop products are  taken from EUROSTAT Gross nutrient balance as advised by \\\\citet{schappi_annexes_2025}: «Nutrient "
                "removal by harvest of crops» minus «Industrial crops». «Ornamenal crops», which should also be removed, are negligible in Norway. "
                "For years with missing data, we have filled in the average of all other years. "
            elif "industrial" in norm:
                exact_flow_code = "AG.SM-MP.OP-Crop products for industrial use-Nmix"
                display_name = "Crop products for industrial use"
                description = "Crop products for industrial use is taken from EUROSTAT Gross nutrient balance as advised by "
                "\\\\citet{schappi_annexes_2025}. For years with missing data, we have filled in the average of all other years. "
        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: {parent_subpool}\n")
            if 'MM' in parent_subpool:
                f.write(f"nav_order: {ag_mm_counter}\n---\n\n")
                ag_mm_counter += 1
            else:
                f.write(f"nav_order: {ag_sm_counter}\n---\n\n")
                ag_sm_counter += 1

            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n{description}\n\n")
            
            # Legger til bibliografitaggen {% bibliography --cited %}
            append_bibtex_references(f, bib_filename)

def process_forests_pool(fs_folder, plot_files, plot_dir, bib_filename):
    """Genererer hovedsiden, subpools og alle strømmer for Forests and semi-natural vegetation (FS) med oppdatert LaTeX-syntaks."""
    with open(os.path.join(fs_folder, "pool_forests_and_semi_natural.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Forests and semi-natural vegetation (FS)\nnav_order: 5\nhas_children: true\n---\n\n")
        f.write("# Pool: Forests and semi-natural vegetation (FS)\n\nBecause of limited data on OL and because data on leaching are combined for WL and OL, ")
        f.write("we have chosen to combine WL and OL into the OL subpool in this study.\n\n")
        f.write("We have considered including meat from hunting of wild animals in flows from this subpool, but chosen not to. ")
        f.write("According to \\\\citet{steinset_verdi_2021}, the amount of wild game caught in 2019 was around 6000 tonnes, ")
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
        f.write("* Because the N-flow in forest fertilization is not large, we have chosen to ignore the associated N2O emissions that were included in the Swedish NBB \\\\citep{moldan_where_2025}.\n")

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
                description = "Calculated based on N2O emissions from UNFCCC Common reporting tables, Table 4 and assuming a mean N2:N2O ratio of 19.5 as discussed by \\\\citet{schappi_annexes_2025}."
            elif "emissionsn2o" in norm:
                exact_flow_code = "FS.FO-AT.AT-Emissions-N2O"
                display_name = "Forest Emissions (N2O)"
                description = "Taken from UNFCCC Common reporting tables, Table 4."
            elif "households" in norm or "fuelwood" in norm:
                exact_flow_code = "FS.FO-EF.OE-Fuel wood for households-Nmix"
                display_name = "Fuel Wood for Households"
                description = "Taken from SSB table 09702 'Energibalansen. Vedforbruk i boliger og fritidsboliger 1990 – 2024' and we assume a mean N content of 4.0 kg/t (between coniferous and non-coniferous wood; see **FS.FO-MP.OP-Industrial round wood-Nmix**)."
            elif "leaching" in norm:
                exact_flow_code = "FS.FO-HY.SW-Leaching-Nmix"
                display_name = "Forest Leaching"
                description = "Found in data supplied by NIVA, produced in the TEOTIL3 model \\\\citep{sample_teotil3_2024}. For the period 1990-2013, we have used TEOTIL data published by Miljødirektoratet for nitrogen from nitrogen flows that reach the coast, where we have found that values for leaching from forest in the period 2013-2023 are a fraction 0.59 of what is reported by Miljødirektoratet as «Bakgrunn», to within a 2% error."
            elif "roundwood" in norm or "industrial" in norm:
                exact_flow_code = "FS.FO-MP.OP-Industrial round wood-Nmix"
                display_name = "Industrial Round Wood"
                description = "Taken from FAOSTAT Forestry production and trade: industrial roundwood, which gives values under bark."
                "The values given here are very close to those reported in SSB table 08979 “Avvirkning for salg (1 000 m³) 1996 – 2024”. "
                "We have also compared with data in Eurostat, which gives total amount of round removed (over or under bark) including use for "
                "firewood in households and industry. Following the Swedish NBB \\citep{moldan_where_2025}, we use an average wood density "
                "of 0.45 t/m3 for all wood categories, and N-contents of 3.4 kg/t for coniferous and 4.3 kg/t for non-coniferous trees. "
                "ktN/mill m3 wood harvested. IN PROGRESS"

        elif filename.upper().startswith("FS_OL_"):
            parent_subpool = "Other Land (FS.OL)"
            if "grazing" in norm:
                exact_flow_code = "FS.OL-AG.MM-Grazing-Nmix"
                display_name = "Organised Grazing"
                description = "Calculated using data from NIBIO on organised grazing \\\\citep{nibio_beitestatistikk_2025} together with "
                "estimated fodder intake for different animal groups taken from Table 1.2 in \\citep{hegrenes_verdi_2006}, "
                "assuming an average protein content of 150 g pr FEm and the standard Jones factor for the nitrogen content of protein. "
            elif "emissionsn2" in norm and "n2o" not in norm:
                exact_flow_code = "FS.OL-AT.AT-Emissions-N2"
                display_name = "Other Land Emissions (N2)"
                description = "Calculated from N2O emissions from UNFCCC Common reporting tables, Table 4, assuming a mean N2:N2O ratio of 19.5 "
                "as has been calculated from studies of forest ecosystems, as discussed in \\\\citet{schappi_annexes_2025}. IN PROGRESS"
            elif "emissionsn2o" in norm:
                exact_flow_code = "FS.OL-AT.AT-Emissions-N2O"
                display_name = "Other Land Emissions (N2O)"
                description = "Taken from UNFCCC Common reporting tables, Table 4, where the only reported values are from wetlands."
            elif "leaching" in norm:
                exact_flow_code = "FS.OL-HY.SW-Leaching-Nmix"
                display_name = "Other Land Leaching"
                description = "Found in data supplied by NIVA, produced in the TEOTIL3 model \\\\citep{sample_teotil3_2024}, "
                "where it is aggregated with the value for WL. For the period 1990-2013, we have used TEOTIL data published by "
                "Miljødirektoratet for nitrogen from nitrogen flows that reach the coast, where we have found that values for leaching "
                "from forest in the period 2013-2023 are a fraction 0.42 of what is reported by Miljødirektoratet as «Bakgrunn», "
                "to within a to within a 3 % error. "

        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: {parent_subpool}\n")
            if 'FO' in parent_subpool:
                f.write(f"nav_order: {fs_fo_counter}\n---\n\n")
                fs_fo_counter += 1
            else:
                f.write(f"nav_order: {fs_ol_counter}\n---\n\n")
                fs_ol_counter += 1

            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n{description}\n\n")
            
            # Legger til bibliografitaggen {% bibliography --cited %}
            append_bibtex_references(f, bib_filename)
            

def process_hydrosphere_pool(hy_folder, plot_files, plot_dir, bib_filename):
    """Genererer hovedsiden og alle under-hovedsider for Hydrosphere (HY) poolen med oppdatert LaTeX-syntaks."""
    with open(os.path.join(hy_folder, "pool_hydrosphere.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Hydrosphere (HY)\nnav_order: 6\nhas_children: true\n---\n\n")
        f.write("# Pool: Hydrosphere (HY)\n\nWe have chosen to not include the pool groundwater (GW) because N concentrations and dynamics ")
        f.write("in Norway are largely unknown \\\\citep{kvaerno_2024}.\n\n")
        f.write("The hydrosphere ecosystem is split into three operational modules. Explore them below:\n\n")
        f.write("* [Surface Water (HY.SW)](subpool_surface_water.html)\n* [Coastal Water (HY.CW)](subpool_coastal_water.html)\n* [Aquaculture (HY.AC)](subpool_aquaculture.html)\n")
        f.write(get_balance_image_markdown("HY", plot_files, plot_dir, relative_depth="../"))
        append_bibtex_references(f, bib_filename)

    with open(os.path.join(hy_folder, "subpool_surface_water.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Surface Water (HY.SW)\nparent: Hydrosphere (HY)\nnav_order: 1\nhas_children: true\n---\n\n")
        f.write("# Subpool: Surface water (HY.SW)\n\n")
        f.write(get_balance_image_markdown("HY.SW", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **HY.SW-AT.AT-Emissions-NOx** is assumed negligible.\n* **HY.SW-RW.RW-Export of surface water-Nmix** is assumed negligible due to Norwegian topography.\n")
        append_bibtex_references(f, bib_filename)

    with open(os.path.join(hy_folder, "subpool_coastal_water.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Coastal Water (HY.CW)\nparent: Hydrosphere (HY)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Subpool: Coastal water (HY.CW)\n\n")
        f.write(get_balance_image_markdown("HY.CW", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **HY.CW-AT.AT-Emissions-N2** is neglected as we do not use mass balance on this subpool.\n* **HY.CW-AT.AT-Emissions-N2O** and **HY.CW-AT.AT-Emissions-NOx** are neglected as we lack a clearly defined area for coastal waters.\n* **HY.CW-PR.SO-Biomass for energy production-Nmix** is neglected because organic material from the processing of caught or farmed fish is assigned to the MP.FS subpool...\n* **Recreational fishing** is not included in the official guidelines, and we have also chosen to neglect it here...\n")
        append_bibtex_references(f, bib_filename)

    with open(os.path.join(hy_folder, "subpool_aquaculture.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Aquaculture (HY.AC)\nparent: Hydrosphere (HY)\nnav_order: 3\nhas_children: true\n---\n\n")
        f.write("# Subpool: Aquaculture (HY.AC)\n\n")
        f.write(get_balance_image_markdown("HY.AC", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **HY.AC-MP.FP-Freshwater fish and seafood-Nmix**, **HY.AC-HY.SW-Waste feed-Nmix** and **HY.AC-HY.SW-Excretia-Nmix** are set to zero...\n* **HY.AC-AT.AT-Emissions-NH3** is set to zero assuming negligible ammonia emissions from these coastal marine cages.\n")
        append_bibtex_references(f, bib_filename)
        
    hy_sw_counter, hy_cw_counter, hy_ac_counter = 1, 1, 1

    for filename in plot_files:
        if not (filename.upper().startswith("HY_SW_") or filename.upper().startswith("HY_CW_") or filename.upper().startswith("HY_AC_")):
            continue

        base_name = filename.rsplit('.', 1)[0]
        flow_file_name = f"flow_{base_name}.md"
        full_flow_path = os.path.join(hy_folder, flow_file_name)
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')

        exact_flow_code = "HY-Unknown-Flow"
        display_name = "Unknown Hydrosphere Flow"
        parent_subpool = ""
        description = ""

        if filename.upper().startswith("HY.SW_"):
            parent_subpool = "Surface water (HY.SW)"
            if "emissionsn2" in norm and "n2o" not in norm:
                exact_flow_code = "HY.SW-AT.AT-Emissions-N2"
                display_name = "N2 emissions from denitrification in surface waters"
                description = "N2 is taken from data on N retention in surface waters supplied by NIVA, produced in the TEOTIL3 model "
                "\\citet{sample_teotil3_2024}, by assuming that all N retained in SW is lost to denitrification, with an assumed fraction "
                "1 % as N2O and the rest as N2. For years prior to 2013, we have used a retention rate of 7 % which is the typical "
                "value from the NIVA data and calculated the denitrification amount as 0.07/(1-0.07)* **HY.SW-HY.CW-Inflow to coastal waters-Nmix**."
            elif "emissionsn2o" in norm:
                exact_flow_code = "HY.SW-AT.AT-Emissions-N2O"
                display_name = "Surface water N2O emissions"
                description = "Uses data on N retention in surface waters supplied by NIVA, produced in the TEOTIL3 model \\citet{sample_teotil3_2024}, "
                "and assuming that all N retained in SW is lost to denitrification, with an assumed fraction 1 % as N2O and the rest as N2."
            elif "inflow" in norm:
                exact_flow_code = "HY.SW-HY.CW-Inflow to coastal waters-Nmix"
                display_name = "Inflow to coastal waters"
                description = "Found from data supplied by NIVA, produced in the TEOTIL3 model \\citet{sample_teotil3_2024}. Before 2013 we have "
                "used values from table 7.2 in \\citet{sample_kildefordelte_2025}. These values includes wastewater discharge, so to avoid double "
                "counting we subtract the flow *PR.WW-HY.CW-Treated wastewater discharge-Nmix* where we have already assigned all treated "
                "wastewater discharge to CW. "
        elif filename.upper().startswith("HY.CW_"):
            parent_subpool = "Coastal Water (HY.CW)"
            if "wildcatch" in norm:
                exact_flow_code = "HY.CW-MP.FP-Fish (wild catch)-Nmix "
                display_name = "Wild fish catch"
                description = "found using data from \\citet{fiskeridirektoratet_fangst_2025} on total wild fish catch. According to "
                "\\\\citet{schappi_annexes_2025}, p254: N content in fish and shellfish: 2.8% according to UNECE Guidance, Annex 6 Table 12. "
                "Our results are very close to those of \\citet{hohmann-marriott_nitrogen_2025} (also when looking at shellfish and aquaculture). "
            elif "shellfish" in norm:
                exact_flow_code = "HY.CW-MP.FP-Shellfish-Nmix"
                display_name = "Shellfish"
                description = "We use data from \\citet{fiskeridirektoratet_fangst_2025} on total wild fish catch. According to "
                "\\\\citet{schappi_annexes_2025}, p254: N content in fish and shellfish: 2.8% according to UNECE Guidance, Annex 6 Table 12. "
                
    with open(full_flow_path, 'w', encoding='utf-8') as f:
        f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: {parent_subpool}\n")
        if 'SW' in parent_subpool:
            f.write(f"nav_order: {hy_sw_counter}\n---\n\n")
            hy_sw_counter += 1
        elif 'CW' in parent_subpool:
            f.write(f"nav_order: {hy_cw_counter}\n---\n\n")
            hy_cw_counter += 1
        else:
            f.write(f"nav_order: {hy_ac_counter}\n---\n\n")
            hy_ac_counter += 1

        f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n{description}\n\n")
        
        # Legger til bibliografitaggen {% bibliography --cited %}
        append_bibtex_references(f, bib_filename)


        
        
def process_humans_and_settlements_pool(hs_folder, plot_files, plot_dir, bib_filename):
    """Genererer hovedsiden og alle understrømmer for Humans and settlements (HS) poolen med oppdatert LaTeX-syntaks."""
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
        append_bibtex_references(f, bib_filename)

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
                "while occasional smokers smoke 100 per year. This data is used with equation 46 in \\\\citet{schappi_annexes_2025}, taken from "
                "\\\\citet{sutton_2000}, which relates ammonia emissions to age and cigarette smoking."
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
                "Data are supplied by NIVA, produced in the TEOTIL3 model \\\\citep{sample_teotil3_2024}. For the period 1990-2013, "
                "we have used TEOTIL data \\\\citep{sample_teotil_data_2025} for nitrogen from urban areas that reach the coast, and used a "
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
                "with N contents taken from \\\\citet{schappi_annexes_2025} and typical, assumed values are chosen if none are given. We include "
                "households, services (tjenesteytende næringer), construction (Bygge- og anleggsvirksomhet), municipal services "
                "(power and water), and waste management.\n\n"
                "Detailed data are not available prior to 1995, but trends in municipal and other waste are described by \\\\citet{ssb_avfall_1997}. "
                "Household waste per inhabitant increased from about 200 kg/person to 289 kg/person in 1995 \\\\citep[figure 4.1]{ssb_avfall_1997}, "
                "with an assumed linear increase in the years between. Based on this we assume a constant N content per unit mass "
                "and extrapolate from 1995 values back to 1990."
            )
        elif "wastewater" in norm or "municipal" in norm:
            exact_flow_code = "HS.HS-PR.WW-Municipal wastewater-Nmix"
            display_name = "Municipal Wastewater"
            description = (
                "**HS.HS-PR.WW-Municipal wastewater-Nmix** are based on population data from SSB and assuming an average value "
                "of 4.65 kg N / person / year for municipal wastewater as advised by \\\\citet{schappi_annexes_2025}. This corresponds to "
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
    """Genererer hovedsiden, subpools og alle strømmer for Energy and Fuels (EF) med oppdatert LaTeX-syntaks."""
    with open(os.path.join(ef_folder, "pool_energy_and_fuels.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Energy and fuels (EF)\nnav_order: 7\nhas_children: true\n---\n\n")
        f.write("# Pool: Energy and fuels (EF)\n\nIn the guidelines, there are N2 flows assigned to and from EF sectors associated with nitrogen conversions in the combustion process...\n")
        f.write("This pool is divided into four operational sub-pools. Explore them using the side menu or links below:\n\n")
        f.write("* [Energy conversion (EF.EC)](subpool_energy_conversion.html)\n* [Manufacturing industries and construction (EF.IC)](subpool_industry.html)\n* [Transportation (EF.TR)](subpool_transport.html)\n* [Other energy and fuels (EF.OE)](subpool_other_energy.html)\n\n")
        f.write(get_balance_image_markdown("EF", plot_files, plot_dir, relative_depth="../"))
        append_bibtex_references(f, bib_filename)

    # Opprett subpools
    with open(os.path.join(ef_folder, "subpool_energy_conversion.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Energy conversion (EF.EC)\nparent: Energy and fuels (EF)\nnav_order: 1\nhas_children: true\n---\n\n# Subpool: Energy conversion (EF.EC)\n\n")
        f.write(get_balance_image_markdown("EF.EC", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n* **EF.EC-AT.AT-Emissions-NH3**: Data from CLRTAP Inventory Submissions...\n")
        append_bibtex_references(f, bib_filename)

    with open(os.path.join(ef_folder, "subpool_industry.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Manufacturing industries and construction (EF.IC)\nparent: Energy and fuels (EF)\nnav_order: 2\nhas_children: true\n---\n\n# Subpool: Manufacturing industries and construction (EF.IC)\n\n")
        f.write(get_balance_image_markdown("EF.IC", plot_files, plot_dir, relative_depth="../"))
        append_bibtex_references(f, bib_filename)

    with open(os.path.join(ef_folder, "subpool_transport.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Transportation (EF.TR)\nparent: Energy and fuels (EF)\nnav_order: 3\nhas_children: true\n---\n\n# Subpool: Transportation (EF.TR)\n\n")
        f.write(get_balance_image_markdown("EF.TR", plot_files, plot_dir, relative_depth="../"))
        append_bibtex_references(f, bib_filename)

    with open(os.path.join(ef_folder, "subpool_other_energy.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Other energy and fuels (EF.OE)\nparent: Energy and fuels (EF)\nnav_order: 4\nhas_children: true\n---\n\n# Subpool: Other energy and fuels (EF.OE)\n\n")
        f.write(get_balance_image_markdown("EF.OE", plot_files, plot_dir, relative_depth="../"))
        append_bibtex_references(f, bib_filename)

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
                description = "EF.EC-EF.IC-Fuel for industry-Nmix: As advised by \\\\citet{schappi_annexes_2025}..."
            elif "fuel" in norm and "heating" in norm:
                exact_flow_code = "EF.EC-EF.OE-Fuel for heating-Nmix"
                display_name = "Fuel for heating"
                description = "EF.EC-EF.OE-Fuel for heating-Nmix: As advised by \\\\citet{schappi_annexes_2025}..."
            elif "fuel" in norm and "transport" in norm:
                exact_flow_code = "EF.EC-EF.TR-Fuel for transport-Nmix"
                display_name = "Fuel for transport"
                description = "EF.EC-EF.TR-Fuel for transport-Nmix: As advised by \\\\citet{schappi_annexes_2025}..."
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
    """Genererer hovedsiden, subpools og alle strømmer for Materials and products in industry (MP) med oppdatert LaTeX-syntaks."""
    
    # 1. GENERER HOVEDSIDE FOR POOLEN (pool_materials_and_products.md)
    with open(os.path.join(mp_folder, "pool_materials_and_products.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Materials and products (MP)\nnav_order: 6\nhas_children: true\n---\n\n")
        f.write("# Pool: Materials and products in industry (MP)\n\n")
        f.write("This pool covers chemical, processing, food, and manufacturing industries in Norway, split into two primary segments:\n\n")
        f.write("* [Food and Feed Processing (MP.FP)](subpool_food_and_feed.html)\n")
        f.write("* [Other Producing Industry (MP.OP)](subpool_other_industry.html)\n")
        f.write(get_balance_image_markdown("MP", plot_files, plot_dir, relative_depth="../"))
        append_bibtex_references(f, bib_filename)

    # 2. SUBPOOL: FOOD AND FEED PROCESSING (MP.FP)
    with open(os.path.join(mp_folder, "subpool_food_and_feed.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Food and Feed Processing (MP.FP)\nparent: Materials and products (MP)\nnav_order: 1\nhas_children: true\n---\n\n")
        f.write("# Subpool: Food and feed processing (MP.FP)\n\n")
        f.write(get_balance_image_markdown("MP.FP", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **MP.FP-HY.AC-Feed to freshwater aquaculture-Nmix** is set to zero because it is assumed all (except a negligible amount) aquaculture takes place in coastal waters.\n")
        f.write("* **MP.FP-PR.SO-Organic waste as biofuels substrate-Nmix** and **MP.FP-PR.SO-Organic waste for composting-Nmix** are not given as separate flows; instead they are included in the flow **MP.FP-PR.SO-Food industry waste-Nmix** because official statistics do not clearly indicate what origin waste flows end up in different end uses.\n")
        append_bibtex_references(f, bib_filename)

    # 3. SUBPOOL: OTHER PRODUCING INDUSTRY (MP.OP)
    with open(os.path.join(mp_folder, "subpool_other_industry.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Other Producing Industry (MP.OP)\nparent: Materials and products (MP)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Subpool: Other producing industry (MP.OP)\n\n")
        f.write(get_balance_image_markdown("MP.OP", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **MP.OP-EF.TR-Ammonia as fuel-NH3** is set to zero because there is negligible use of ammonia as fuel today.\n")
        append_bibtex_references(f, bib_filename)

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
                    "\\\\citep{landbruksdirektoratet_matkorn_2025} and used the detailed composition of animal feed given in \\\\citet{eidem_ruud_2022} together with protein contents "
                    "from \\\\citet{fao_feed_2021} and specific Jones factors from \\\\citet{fao_jones_2023} to get nitrogen contents.\\n\\n"
                    "Based on the Landbruksdirektoratet data, the N content of the total amount of feed is 0.02 kgN/kg feed. NIBIO Totalkalkylen "
                    "gives statistics for total amount of feed to Norwegian farm animals between 1959 and 2026. Table 6.10 in \\\\citet{bruholt_longva_1994} "
                    "gives the domestically produced fraction of farm animal feed between 1985 and 1994. We combine these data to find values before 2000, "
                    "using an average import fraction for 1995-1999.\\n\\n"
                    "\\\\citet{hohmann-marriott_nitrogen_2025} found the domestic supply of animal feed in 2010 to be around 35 ktN, based on FAO statistics of production, "
                    "export and import of seed cake, which is a dominant ingredient in farm animal feed. This is less than we found when combining domestic and imported animal feed. "
                    "*(Note: This estimate might be too low, as it leads to a surplus here and a deficit in the AG.MM pool).*"
                )
            elif "seed" in norm or "planting" in norm:
                exact_flow_code = "MP.FP-AG.SM-Seeds and planting material-Nmix"
                display_name = "Seeds and Planting Material"
                description = (
                    "**MP.FP-AG.SM-Seeds and planting material-Nmix** is taken from Gross nutrient balance in the Eurostat database as advised by \\\\citet{schappi_annexes_2025}. "
                    "There is data missing from 2017 to 2019; because there is a large reported increase between 2016 and 2020, we assume a constant increase in the "
                    "missing time period and fill in data from this interpolation."
                )
            elif "food" in norm and "product" in norm and "export" not in norm:
                exact_flow_code = "MP.FP-HS.HS-Food products-Nmix"
                display_name = "Food Products to Consumers"
                description = (
                    "**MP.FP-HS.HS-Food products-Nmix** is food products consumed by private households including restaurants and pets. \\\\citet{schappi_annexes_2025} "
                    "advises using FAO statistics on food availability for human food consumption, but this only gives data back to 2009. The values in this statistic "
                    "gives a bit more than 40 ktN per year. We have chosen to use data on food sales to consumers from SSB (table 13695: Næringsinnhald per dag frå "
                    "selde mat- og drikkevarer 2018 – 2023, table 10249: Forbrukte mengder av mat- og drikkevarer per person per år, etter varegruppe (kg/liter) (avslutta serie) "
                    "1999 – 2012 and table 06376: Forbrukte mengder av mat- og drikkevarer per person per år, etter varegruppe (kg/liter) (avslutta serie) 1958-1959 - 1996-1998). "
                    "The latter series gives values for 3 year averages, and we have assigned the averages to each individual year.\\n\\n"
                    "From 2018 the statistics are given in terms of protein content. Previous to this, the amounts of various food categories are given, and we have used "
                    "protein contents found in Matvaretabellen \\\\citep{mattilsynet_matvaretabellen_2006} as this reflects common foods found in Norwegian retail. Population data are taken from SSB "
                    "and we have used the Jones factor of 6.25 for nitrogen content in protein.\\n\\n"
                    "For pet food, we have assumed (based on available statistics) that cats and dogs consume > 90 % of pet food. Horses are accounted for under the agriculture pool. "
                    "The nitrogen intake per animal per year is taken from Table 19 in \\\\citet{schappi_annexes_2025} and the number of cats and dogs between 1985 and 2025 is assumed using "
                    "a trendline based on available statistics from a variety of sources."
                )
            elif "coastal" in norm or ("feed" in norm and "aquaculture" in norm):
                exact_flow_code = "MP.FP-HY.AC-Feed to coastal aquaculture-Nmix"
                display_name = "Feed to Coastal Aquaculture"
                description = (
                    "**MP.FP-HY.AC-Feed to coastal aquaculture-Nmix**: the amount of feed per ton of produced fish is found by assuming an "
                    "average protein (N) retention of 35.37 % based on values from \\\\citet{aas_aquaculture_2022}. The amount of produced fish is found by using data "
                    "from Fiskeridirektoratet \\\\citep{fiskeridirektoratet_statistikk_2025} on sold farmed fish.\\n\\n"
                    "\\\\citet{hohmann-marriott_nitrogen_2025} found the nitrogen content in aquaculture feed in 2020 to be 124 ktN, which is very similar to our results."
                )
            elif "untreated" in norm and "fp" in norm:
                exact_flow_code = "MP.FP-HY.SW-Untreated wastewater-Nmix"
                display_name = "Untreated Wastewater (Food Industry)"
                description = (
                    "**MP.FP-HY.SW-Untreated wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to water "
                    "from individual industries, where industries are categorized as belonging to OP or FP, and their connection status to the municipal wastewater, "
                    "based on the information given in the statistic. If no information on connection status was given we have assigned the values to Untreated wastewater. "
                    "The database does not distinguish between emissions to surface and coastal waters, so even though several large industries discharge their wastewater "
                    "to the coast, we assign this entire flow to SW in order to avoid double counting.\\n\\n"
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
                    "«Avfallsregnskap for Norge, etter kilde og materialtype (1 000 tonn) 2012 – 2023» and the category “wet organic waste” with N content from \\\\citet{schappi_annexes_2025}. "
                    "The statistic does not separate between food and other industry waste. According to \\\\citet{chaudhary_skjerpen_2025} everything in the industry category "
                    "“wet organic waste” is from the food industry.\\n\\n"
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
                    "(total domestic use) – (import), where both use and import are given in FAOSTAT Fertilizer by nutrient \\\\citep{fao_fertilizer_2025}."
                )
            elif "n2o" in norm:
                exact_flow_code = "MP.OP-AT.AT-Emissions-N2O"
                display_name = "Industrial Emissions (N2O)"
                description = (
                    "**MP.OP-AT.AT-Emissions-N2O** are taken from UNFCCC common reporting tables, Table 3 as advised by \\\\citet{schappi_annexes_2025}. "
                    "Emissions are substantial, at least before 2009, and the main source of emissions is from nitric acid production."
                )
            elif "nh3" in norm:
                exact_flow_code = "MP.OP-AT.AT-Emissions-NH3"
                display_name = "Industrial Emissions (NH3)"
                description = "We have used data from CLRTAP Inventory Submissions \\\\citep{emep_clrtap_2025} as advised by \\\\citet{schappi_annexes_2025}, using the categories given in Table 20."
            elif "nox" in norm:
                exact_flow_code = "MP.OP-AT.AT-Emissions-NOx"
                display_name = "Industrial Emissions (NOx)"
                description = "We have used data from CLRTAP Inventory Submissions \\\\citep{emep_clrtap_2025} as advised by \\\\citet{schappi_annexes_2025}, using the categories given in Table 20."
            elif "fuel" in norm and "waste" in norm:
                exact_flow_code = "MP.OP-EF.IC-Industrial waste fuels-Nmix"
                display_name = "Industrial Waste Fuels"
                description = (
                    "**MP.OP-EF.IC-Industrial waste fuels-Nmix** is wood waste used as biofuel in the industries where the waste originates, reported as "
                    "\"egentilvirket bioenergi\" in the SSB statistic (table 08205). Producers of wood and paper products obtain a significant fraction of their "
                    "energy through this source. “Egentilvirket bioenergi” encompasses “black liquor” as well as wood waste. For lack of better compositional details "
                    "we have assumed values for the entire flow corresponding to wood, although this brings significant uncertainty.\\n\\n"
                    "The net caloric value of 15.6 for conversion is taken from table 1.2 in \\\\citet{garg_ipcc_2006} and we assume a mean N content of 4.0 kg/t "
                    "(between coniferous and non-coniferous wood; see FS.FO-MP.OP-Industrial round wood-Nmix).\\n\\n"
                    "SSB has not reported data on this energy category before 1998, but the size of these industries was relatively constant through the period 1991-2001 "
                    "\\\\citep{spilde_aasestad_2004}. For years 1990-1997 we have therefore used the average for the next 10 years (1998-2007)."
                )
            elif "forest" in norm or "fertilization" in norm:
                exact_flow_code = "MP.OP-FS.FO-Mineral fertilizer-Nmix"
                display_name = "Forest Fertilization Nitrogen"
                description = (
                    "**MP.OP-FS.FO-Mineral fertilizer-Nmix** is nitrogen for forest fertilization. This flow is not part of the guidelines but has been "
                    "added because it is a significant flow in Norway, as was also done in the Swedish NNB \\\\citep{moldan_swedish_2025}. We have used data from SSB on "
                    "area of forest fertilized and assumed a standard value of 15 kgN/da \\\\citep{dalen_skog_2017}. Fertilized area before 1997 is taken from Figure 2 in "
                    "\\\\citet{landbruksdirektoratet_skog_2021}."
                )
            elif "consumer" in norm and "goods" in norm:
                exact_flow_code = "MP.OP-HS.HS-Consumer goods-Nmix"
                display_name = "Consumer Goods (Mass Balance)"
                description = (
                    "**MP.OP-HS.HS-Consumer goods-Nmix** is calculated by mass balance, assuming that all incoming flows to OP that are not accounted for "
                    "in outgoing flows end up in domestic consumer goods. We have excluded N2 fixation for ammonia synthesis, and mineral fertilizer flows. "
                    "We also exclude emissions to air from the balance because they result mainly from fertilizer production.\\n\\n"
                    "**Incoming flows:**\\n"
                    "* AG.SM-MP.OP-Crop products for industrial use-Nmix\\n"
                    "* AG.MM-MP.OP-Non-edible animal products-Nmix\\n"
                    "* PR.SO-MP.OP-Recycling-Nmix\\n"
                    "* EF.EC-MP.OP-Fuel used as feedstock-Nmix\\n"
                    "* FS.FO-MP.OP-Industrial round wood-Nmix\\n"
                    "* RW.RW-MP.OP-Other goods import -Nmix\\n\\n"
                    "**Outgoing flows:**\\n"
                    "* MP.OP-PR.SO-Other industry waste-Nmix\\n"
                    "* MP.OP-PR.WW-Other industry wastewater-Nmix\\n"
                    "* MP.OP-HY.SW-Untreated wastewater-Nmix\\n"
                    "* MP.OP-RW.RW-Other goods export-Nmix\\n"
                    "* MP.OP-EF.IC-Industrial waste fuels-Nmix\\n\\n"
                    "For comparison, \\\\citet{moldan_swedish_2025} found flows from MP to HS of 15.9 ktN in the form of wood products (produced – export – waste) "
                    "and 52.2 ktN in the form of chemical products, also found by mass balance, and identified as “plastics, deicing agents, glue, paint, tensides, etc.”, "
                    "giving a total of 68.1 ktN which, given that the Swedish population is larger than that of Norway, agrees well with our findings."
                )
            elif "mineral" in norm and "fertilizer" in norm and "hs" in norm:
                exact_flow_code = "MP.OP-HS.HS-Mineral fertilizer-Nmix"
                display_name = "Non-Agricultural Mineral Fertilizer"
                description = (
                    "**MP.OP-HS.HS-Mineral fertilizer-Nmix**: as advised by \\\\citet{schappi_annexes_2025}, we assume a default value of 2% of total mineral "
                    "fertilizer for non-agricultural use. Data for fertilizer use in agriculture are taken from FAOSTAT Fertilizer by nutrient \\\\citep{fao_fertilizer_2025}."
                )
            elif "untreated" in norm and "op" in norm:
                exact_flow_code = "MP.OP-HY.SW-Untreated wastewater-Nmix"
                display_name = "Untreated Wastewater (Other Industry)"
                description = (
                    "**MP.OP-HY.SW-Untreated wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to water "
                    "from individual industries, where industries are categorized as belonging to OP or FP based on the information given in the statistic, and counting "
                    "those that are not reported to be connected to municipal wastewater treatment. These emissions are also reported by Miljødirektoratet \\\\citep{miljodirektoratet_norske_2025}, but "
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
                    "with N contents taken from \\\\citet{schappi_annexes_2025} and typical, assumed values are chosen if none are given. The statistic does not separate between food "
                    "and other industry waste. We make the assumption that everything in the category “wet organic waste” is from the food industry, and all other waste "
                    "is assigned to other producing industry. Here we also include all waste from “other industries” (annen eller uspesifisert næring). The category "
                    "“contaminated waste” is very irregularly reported (placed in different sectors in different years) and has therefore been excluded.\\n\\n"
                    "There is a change in categorization between the two tables, where the main difference is in the category “other waste” and “mixed waste”. To ensure "
                    "continuity between the data series we chose a lower value for “other waste” than for “mixed waste”. Values between 1990 and 1994 are extrapolated "
                    "from 1995 given the change in industry waste reported between 1992 and 1995 reported by \\\\citet{ssb_avfall_1997}."
                )
            elif "wastewater" in norm and "op" in norm:
                exact_flow_code = "MP.OP-PR.WW-Other industry wastewater-Nmix"
                display_name = "Other Industry Wastewater"
                description = (
                    "**MP.OP-PR.WW-Other industry wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to "
                    "water from individual industries, where industries are categorized as belonging to OP or FP based on the information given in the statistic, and counting "
                    "those that are not reported to be connected to municipal wastewater treatment. These emissions are also reported by Miljødirektoratet \\\\citep{miljodirektoratet_norske_2025}, but as of "
                    "February 2026 the publicly available data did not include information on connection to municipal wastewater."
                )
            elif "fertilizer" in norm and "export" in norm:
                exact_flow_code = "MP.OP-RW.RW-Mineral fertilizer export-Nmix"
                display_name = "Mineral Fertilizer Export"
                description = "**MP.OP-RW.RW-Mineral fertilizer export-Nmix** is taken from FAOSTAT Fertilizer by nutrient \\\\citep{fao_fertilizer_2025}."
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
    """Genererer hovedsiden, subpools og alle strømmer for Processing of residues (PR) med oppdatert LaTeX-syntaks."""
    # 1. Generer hovedsiden for poolen
    with open(os.path.join(pr_folder, "pool_processing_of_residues.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Processing of residues (PR)\nnav_order: 9\nhas_children: true\n---\n\n")
        f.write("# Pool: Processing of residues (PR)\n\n")
        f.write("This pool accounts for the treatment and processing of waste and wastewater residues in Norway.\n\n")
        f.write("This pool is divided into two operational sub-pools. Explore them using the side menu or links below:\n\n")
        f.write("* [Solid Waste (PR.SO)](subpool_solid_waste.html)\n* [Wastewater (PR.WW)](subpool_wastewater.html)\n\n")
        f.write(get_balance_image_markdown("PR", plot_files, plot_dir, relative_depth="../"))
        append_bibtex_references(f, bib_filename)

    # 2. Generer subpool-side for Solid Waste (PR.SO)
    with open(os.path.join(pr_folder, "subpool_solid_waste.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Solid Waste (PR.SO)\nparent: Processing of residues (PR)\nnav_order: 1\nhas_children: true\n---\n\n")
        f.write("# Subpool: Solid Waste (PR.SO)\n\n")
        f.write(get_balance_image_markdown("PR.SO", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* **PR.SO-AG.SM-Manure co-digestation-Nmix** is tracked under agricultural sub-allocations where applicable and excluded here to prevent double counting.\n")
        append_bibtex_references(f, bib_filename)

    # 3. Generer subpool-side for Wastewater (PR.WW)
    with open(os.path.join(pr_folder, "subpool_wastewater.md"), 'w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Wastewater (PR.WW)\nparent: Processing of residues (PR)\nnav_order: 2\nhas_children: true\n---\n\n")
        f.write("# Subpool: Wastewater (PR.WW)\n\n")
        f.write(get_balance_image_markdown("PR.WW", plot_files, plot_dir, relative_depth="../"))
        f.write("\n### Flows that are zero or neglected:\n\n")
        f.write("* Direct industrial untreated sewer overflows are consolidated into total treated flows or omitted where minor regional boundaries apply \\\\citep{schulte_uebbing_planetary_2022}.\n")
        append_bibtex_references(f, bib_filename)

    pr_so_counter, pr_ww_counter = 1, 1

    # 4. Gå igjennom og generer individuelle strømmer fordelt på subpools
    for filename in plot_files:
        if not (filename.startswith("PR_SO_") or filename.startswith("PR_WW_")):
            continue

        base_name = filename.rsplit('.', 1)[0]
        flow_file_name = f"flow_{base_name}.md"
        full_flow_path = os.path.join(pr_folder, flow_file_name)
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')

        exact_flow_code = "PR-Unknown-Flow"
        display_name = "Unknown Residue Flow"
        parent_subpool = ""
        flow_description = ""

        # --- Solid Waste (PR.SO) Subpool ---
        if filename.startswith("PR_SO_"):
            parent_subpool = "Solid Waste (PR.SO)"
            
            if "efec" in norm and "waste" in norm:
                exact_flow_code = "PR.SO-EF.EC-Waste to energy-Nmix"
                display_name = "Waste to energy (Incineration)"
                flow_description = (
                    f"**{exact_flow_code}** is found from SSB tables 05281 “Avfallsregnskap for Norge (1 000 tonn), "
                    "etter statistikkvariabel, behandlingsmåte, materialtype og år “ (1995-2011) and 10513 “Avfallsregnskap "
                    "for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og behandlingsmåte” (2012-2023), "
                    "using N content values from global waste and incineration estimates \\\\citep{{smil_nitrogen_1999}}.\\n\\n"
                    "For years prior to 1995, we use the overall fraction of waste to incineration given in historical "
                    "records and assume that the overall N content of the waste is equal to the 1995 value. For years with missing data, "
                    "we interpolate."
                )
            elif "agsm" in norm and "biologically" in norm:
                exact_flow_code = "PR.SO-AG.SM-Biologically treated organic waste-Nmix"
                display_name = "Biologically treated organic waste to Ag"
                flow_description = (
                    f"**{exact_flow_code}** includes all forms of organic waste except sewage sludge that is organically treated "
                    "and used in agricultural soils. Biological treatment of organic waste includes both composting and biogas production, "
                    "but in Norway, most of the waste composted in the municipal waste sector is used on the private sector, not in agriculture. "
                    "We therefore only include biogas digestate in this flow.\\n\\n"
                    "According to Biogass Norge, biogas digestate is produced from sewage sludge, manure, fish waste and sludge, and food waste. "
                    "General frameworks for urban and regional nitrogen recycling from waste management are detailed in \\\\citep{{kaltenegger_urban_2023}}. "
                    "From 2018 to 2020, we use data on the disposal of biologically produced waste from SSB table 12818 where we find the N "
                    "content of what is used in agriculture by scaling the N content of the amount used in 2021.\\n\\n"
                    "From 2012 to 2017, we use data on biogas treatment of different waste categories from SSB table 10513 “Avfallsregnskap "
                    "for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og behandlingsmåte” assuming that 85 % of this is "
                    "used in agriculture with a loss of 10 % N during biological treatment.\\n\\n"
                    "According to SSB, there were 8 biogas plants in 2011 and 35 in 2017. We therefore assume values before 2012 to be "
                    "negligible and set those flows to zero."
                )
            elif "atat" in norm and "n2o" in norm:
                exact_flow_code = "PR.SO-AT.AT-Emissions-N2O"
                display_name = "N2O Emissions (Solid Waste)"
                flow_description = f"**{exact_flow_code}** is taken from UNFCCC Common reporting tables, where we have included emissions from landfills, waste incineration and biofuel production. Global trends of changing reactive nitrogen emissions are evaluated in \\\\citep{{malik_drivers_2022}}."
            elif "atat" in norm and "nh3" in norm:
                exact_flow_code = "PR.SO-AT.AT-Emissions-NH3"
                display_name = "NH3 Emissions (Solid Waste)"
                flow_description = f"**{exact_flow_code}**: We have used data from CLRTAP Inventory Submissions, using the categories given in Table 48 and 31 (emissions from category 1A1 Energy industries are all assigned to the EF pool). Dynamics of atmospheric deposition and chemically reduced forms are supported by \\\\citep{{ackerman_global_2019}}."
            elif "atat" in norm and "nox" in norm:
                exact_flow_code = "PR.SO-AT.AT-Emissions-NOx"
                display_name = "NOx Emissions (Solid Waste)"
                flow_description = f"**{exact_flow_code}**: We have used data from CLRTAP Inventory Submissions, using the categories given in Table 48 and 31 (emissions from category 1A1 Energy industries are all assigned to the EF pool). General atmospheric pathways of combustion emissions follow \\\\citep{{fowler_global_2013}}."
            elif "hshs" in norm and "biologically" in norm:
                exact_flow_code = "PR.SO-HS.HS-Biologically treated organic waste-Nmix"
                display_name = "Biologically treated organic waste to HS"
                flow_description = (
                    f"**{exact_flow_code}** includes all forms of organic waste except sewage sludge that is organically treated "
                    "and used in agricultural soils. Biological treatment of organic waste includes both composting and biogas production, "
                    "but in Norway, most of the waste composted in the municipal waste sector is used on the private sector, not in agriculture.\\n\\n"
                    "SSB statistics on composted organic waste also includes some composted wastewater sludge, but there is no exact statistics "
                    "on the amount. Opportunities and limitations regarding the agronomic use of human excreta and urban compost are reviewed in \\\\citep{{starck_fate_2023}} and \\\\citep{{kaltenegger_urban_2023}}.\\n\\n"
                    "From 2018, we use data on the disposal of biologically produced waste from SSB table 12818 assuming a typical N content "
                    "of compost, although a smaller fraction is also biogas digestate.\\n\\n"
                    "For 2012-2017, we use data on composted organic waste from SSB table 10513 “Avfallsregnskap for Norge (1 000 tonn) and "
                    "scale the nitrogen value in 2018 for consistency.\\n\\n"
                    "There are no official data prior to 2012, but we know that there was organic waste composted and used in the private sector. "
                    "In lack of other data we extrapolate the 2012 value back to 1990."
                )
            elif "hysw" in norm and "leaching" in norm:
                exact_flow_code = "PR.SO-HY.SW-Leaching-Nmix"
                display_name = "Leaching from Landfills"
                flow_description = (
                    f"**{exact_flow_code}** is taken from emissions data to water from landfills, where we have "
                    "categorized landfills as being connected to municipal wastewater or not based on publicly available data. "
                    "The environmental pressure of such nutrient surpluses on aquatic ecosystems is contextualized within planetary and regional boundaries by \\\\citep{{schulte_uebbing_planetary_2022}}. "
                    "Where the categorization was not possible, the resulting emissions have been split evenly between the leaching and wastewater "
                    "flows from landfills. As no data are available before 2009 we have extrapolated using the average value."
                )
            elif "prww" in norm and "wastewater" in norm:
                exact_flow_code = "PR.SO-PR.WW-Wastewater from landfills-Nmix"
                display_name = "Wastewater from Landfills"
                flow_description = (
                    f"**{exact_flow_code}** is taken from landfill emissions data, where we have "
                    "categorized landfills as being connected to municipal wastewater or not based on publicly available data. "
                    "Regional limits for non-agricultural nitrogen loads into sewage systems are detailed in \\\\citep{{schulte_uebbing_planetary_2022}}. "
                    "Where the categorization was not possible, the resulting emissions have been split evenly. As no data are available before 2009 we have extrapolated using the average value."
                )
            elif "prww" in norm and "biofuels" in norm:
                exact_flow_code = "PR.SO-PR.WW-Biofuels production wastewater-Nmix"
                display_name = "Biofuels Production Wastewater"
                flow_description = (
                    f"**{exact_flow_code}** is found by assuming that the incoming N to biofuel production not retained in digestate ends "
                    "up in the wastewater. For details see PR.SO-HS.HS-Digestate fertilizer-Nmix. Value baselines before 2012 are set to zero."
                )
            elif "mpop" in norm and "recycling" in norm:
                exact_flow_code = "PR.SO-MP.OP-Recycling-Nmix"
                display_name = "Material Recycling"
                flow_description = (
                    f"**{exact_flow_code}** is found from SSB tables 05281 “Avfallsregnskap for Norge (1 000 tonn), etter statistikkvariabel, "
                    "behandlingsmåte, materialtype og år “ (1995-2011) and 10513 “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, "
                    "statistikkvariabel, år og behandlingsmåte” (2012-2023). The international background of embedding nitrogen in commodity and trade loops "
                    "is outlined in \\\\citep{{oita_substantial_2016}}. We have not included the categories sludge, garden waste and wet organic material reported as being assigned to material recycling, "
                    "because this use is rather for soil production or fertilizer and does not belong in the MP.OP subpool."
                )
            elif "rwrw" in norm and "recycling" in norm:
                exact_flow_code = "PR.SO-RW.RW-Export for recycling-Nmix"
                display_name = "Export for Recycling"
                flow_description = f"**{exact_flow_code}** is plastic, paper and textile waste which has been collected for recycling and exported to recycling facilities outside of Norway. Data taken from trade data, SSB table 08801. The footprint of non-food manufacturing trade shifts is discussed in \\\\citep{{hamilton_trade_2018}}."
            elif "rwrw" in norm and "reuse" in norm:
                exact_flow_code = "PR.SO-RW.RW-Export for reuse-Nmix"
                display_name = "Export for Reuse"
                flow_description = f"**{exact_flow_code}** is exported used textiles. Data taken from trade data, SSB table 08801, and follows global non-food trade patterns described in \\\\citep{{hamilton_trade_2018}}."
            elif "rwrw" in norm and "solid" in norm:
                exact_flow_code = "PR.SO-RW.RW-Solid waste export-Nmix"
                display_name = "Solid Waste Export"
                flow_description = f"**{exact_flow_code}** is taken from trade data, SSB table 08801. The impact of escalating international commodity trade on domestic vs. rest-of-world nitrogen footprints is quantified in \\\\citep{{malik_drivers_2022}} and \\\\citep{{lassaletta_nitrogen_2016}}. No export in these categories is reported before 2002, so we set all previous years to zero."

        # --- Wastewater (PR.WW) Subpool ---
        elif filename.startswith("PR_WW_"):
            parent_subpool = "Wastewater (PR.WW)"
            
            if "agsm" in norm:
                exact_flow_code = "PR.WW-AG.SM-Sewage sludge fertilizer-Nmix"
                display_name = "Sewage Sludge Fertilizer to Ag"
                flow_description = f"**{exact_flow_code}** is taken from SSB table 05279 “Avløpsslam, etter slamdisponering, statistikkvariabel, år og region”. Mass balance studies of sewage sludge allocation to crops highlight a major opportunity to shift towards synthetic fertilizer substitution \\\\citep{{starck_fate_2023}}\\\\citep{{kaltenegger_urban_2023}}. For years 1993-2001 we use data from the SSB Naturressurser og miljø series."
            elif "atat" in norm and "n2" in norm and not "n2o" in norm:
                exact_flow_code = "PR.WW-AT.AT-Emissions-N2"
                display_name = "N2 Emissions (Wastewater)"
                flow_description = f"**{exact_flow_code}** is found by using data on N emissions and removal rates from wastewater treatment plants equipped with nitrogen removal. The dynamics of losing significant shares of excreted nitrogen as inert N2 via WWTP denitrification are detailed in \\\\citep{{starck_fate_2023}} and \\\\citep{{fowler_global_2013}}. Where specific data were missing we assumed a default 70 % removal rate."
            elif "atat" in norm and "n2o" in norm:
                exact_flow_code = "PR.WW-AT.AT-Emissions-N2O"
                display_name = "N2O Emissions (Wastewater)"
                flow_description = f"**{exact_flow_code}** are taken from UNFCCC Common reporting tables, Table 5. The risk of unintended greenhouse gas footprints from major reactive nitrogen value chains is examined in \\\\citep{{bertagni_minimizing_2023}}."
            elif "hshs" in norm:
                exact_flow_code = "PR.WW-HS.HS-Sewage sludge fertilizer-Nmix"
                display_name = "Sewage Sludge Fertilizer to HS"
                flow_description = f"**{exact_flow_code}** is taken from SSB table 05279, including all sludge used for green areas and for soil production. Linear urban pathways where nutrient outputs aggregate heavily in municipal infrastructure are outlined in \\\\citep{{kaltenegger_urban_2023}}. For years 1993-2001 we use data from the SSB Naturressurser og miljø series."
            elif "hycw" in norm:
                exact_flow_code = "PR.WW-HY.CW-Treated wastewater discharge-Nmix"
                display_name = "Treated Wastewater Discharge to CW"
                flow_description = f"**{exact_flow_code}** is taken from SSB table 05280 “Totale utslipp av fosfor og nitrogen fra avløpssektoren”. The critical necessity of mitigating coastal aquatic eutrophication from wastewater discharges is documented in \\\\citep{{staalstrom_utredning_2022}} and \\\\citep{{schulte_uebbing_planetary_2022}}. Due to lack of available data we set the values in 1990-1996 to be equal to that in 1997."
            elif "prso" in norm and "landfill" in norm:
                exact_flow_code = "PR.WW-PR.SO-Sewage sludge landfill-Nmix"
                display_name = "Sewage Sludge to Landfill"
                flow_description = f"**{exact_flow_code}** is taken from SSB table 05279, including both sludge that is landfilled and sludge used for top cover on landfills. Global and historical trajectories of crop and livestock system nutrient allocations show a distinct contrast to such structural landfilling losses \\\\citep{{lassaletta_nitrogen_2016}}. For years 1993-2001 we use data from the SSB Naturressurser og miljø series."

        # Skriv ut filen med riktig forelder og nav_order-teller
        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write(f"---\nlayout: default\ntitle: {display_name}\nparent: {parent_subpool}\n")
            if "PR.SO" in parent_subpool:
                f.write(f"nav_order: {pr_so_counter}\n---\n\n")
                pr_so_counter += 1
            else:
                f.write(f"nav_order: {pr_ww_counter}\n---\n\n")
                pr_ww_counter += 1

            f.write(f"# {display_name}\n\n![{exact_flow_code}](../{plot_dir}/{filename})\n\n### Flow Description\n")
            f.write(f"{flow_description}\n\n")
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

    # Liste over alle pool-mappene vi bruker
    pool_folders = [
        "atmosphere_pool",
        "rest_of_the_world_pool",
        "agriculture_pool",
        "forests_and_semi_natural_pool",
        "hydrosphere_pool",
        "humans_and_settlements_pool",
        "energy_and_fuels_pool",
        "materials_and_products_pool",
        "processing_of_residues_pool"
    ]

    print("[RAPPORT] Sletter gamle midlertidige filer fra pool-mappene for å unngå rot...")
    # Slett gamle filer i rotmappen (f.eks. gamle index.md eller feilplasserte filer)
    for f_old in os.listdir('.'):
        if (f_old.startswith("flow_") or f_old.startswith("pool_") or f_old.startswith("subpool_")) and f_old.endswith(".md"):
            os.remove(f_old)
            
    # Slett gamle filer inni selve pool-mappene, slik at vi starter med blanke ark
    for folder in pool_folders:
        if os.path.exists(folder):
            for f_old in os.listdir(folder):
                if f_old.endswith(".md"):
                    os.remove(os.path.join(folder, f_old))

    print("[RAPPORT] Bygger hierarkisk dokumentasjonsportal med egne pool-mapper...")

    # 1. Hovedlandingsside (index.md legges i rotmappen)
    build_landing_page(output_filename, current_date_str, bib_filename)

    # 2. Atmosphere Pool
    os.makedirs(pool_folders[0], exist_ok=True)
    process_atmosphere_pool(pool_folders[0], plot_files, plot_dir, bib_filename)

    # 3. Rest of the World Pool
    os.makedirs(pool_folders[1], exist_ok=True)
    process_rest_of_the_world_pool(pool_folders[1], plot_files, plot_dir, bib_filename)

    # 4. Agriculture Pool
    os.makedirs(pool_folders[2], exist_ok=True)
    process_agriculture_pool(pool_folders[2], plot_files, plot_dir, bib_filename)

    # 5. Forests Pool
    os.makedirs(pool_folders[3], exist_ok=True)
    process_forests_pool(pool_folders[3], plot_files, plot_dir, bib_filename)

    # 6. Hydrosphere Pool
    os.makedirs(pool_folders[4], exist_ok=True)
    process_hydrosphere_pool(pool_folders[4], plot_files, plot_dir, bib_filename)

    # 7. Humans and Settlements Pool
    os.makedirs(pool_folders[5], exist_ok=True)
    process_humans_and_settlements_pool(pool_folders[5], plot_files, plot_dir, bib_filename)

    # 8. Energy and Fuels Pool
    os.makedirs(pool_folders[6], exist_ok=True)
    process_energy_and_fuels_pool(pool_folders[6], plot_files, plot_dir, bib_filename)
    
    # 9. Materials and Products Pool
    os.makedirs(pool_folders[7], exist_ok=True)
    process_materials_pool(pool_folders[7], plot_files, plot_dir, bib_filename)
    
    # 10. Processing of residues Pool
    os.makedirs(pool_folders[8], exist_ok=True)
    process_processing_of_residues_pool(pool_folders[8], plot_files, plot_dir, bib_filename)
    
    # 11. Fikse format på referanser i ALLE mapper automatisk
    # Siden fix_all_citations_in_folder bruker os.walk(), vil "." (gjeldende mappe) 
    # gjøre at den finkjemmer både rotmappen og alle undermappene vi nettopp lagde.
    print("[RAPPORT] Konverterer LaTeX-siteringer til ren tekst...")
    fix_all_citations_in_folder(".", bib_filename)

    print("[RAPPORT] Portalbygging fullført suksessfullt!")
'''
Du kan slå sammen og konvertere Markdown-filene dine til en ferdig PDF ved å kjøre følgende i terminalen:
pandoc pool_rest_of_the_world.md flow_*.md \
  --citeproc \
  --bibliography=references.bib \
  --csl=apa.csl \
  -V geometry:margin=1in \
  -o nitrogen_rapport.pdf
'''