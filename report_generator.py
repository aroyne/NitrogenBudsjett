# report_generator.py
import os
import shutil
from datetime import datetime
from pybtex.database import parse_file

def generate_github_pages_report(plot_dir='output_files/plots', output_filename='index.md', bib_filename='referanser.bib'):
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
        "different land categories we use the map resource AR5 from NIBIO [^NIBIO2016]. "
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
        
        # Tydelig advarselsboks (Callout i Just the Docs-temaet)
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
        f.write("(e.g., Atmosphere, Hydrosphere) and access detailed statistical time-series graphs, ")
        f.write("methodological explanations, and parameterizations for each specific flow.\n")

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
        f.write("This section contains all documented nitrogen flows leaving the Atmosphere pool. ")
        f.write("Click on the individual sub-flows in the left-hand menu to view detailed graphs, ")
        f.write("methodological backgrounds, and Monte Carlo uncertainty intervals.\n")

    # Generer datter-filer (flows) inni mappen
    menu_counter = 1
    for filename in plot_files:
        if not filename.startswith("AT_AT_"):
            continue

        clean_name = filename.replace('.png', '').replace('AT_AT_', '').replace('_', ' ')
        flow_file_name = f"flow_{filename.replace('.png', '')}.md"
        norm = filename.lower().replace('-', '').replace('_', '').replace('.', '')

        full_flow_path = os.path.join(at_folder, flow_file_name)

        # HER SKRIVES DATTERFILENE - PASSED PÅ AT ALT SKRIVES KORREKT
        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write("layout: default\n")
            f.write(f"title: {clean_name}\n")
            f.write("parent: Atmosphere (AT)\n")
            f.write(f"nav_order: {menu_counter}\n")
            f.write("---\n\n")
            
            menu_counter += 1

            f.write(f"# {clean_name}\n\n")
            f.write(f"![{clean_name}](../{plot_dir}/{filename})\n\n")
            f.write("### Flow Description\n")

            # Tekstsjekker
            if "agsm" in norm and "fixation" in norm:
                f.write("**AT.AT-AG.SM-Biological N2 fixation-N2**\n\n")
                f.write("[^Schäppi2025] advises using data from the EUROSTAT Gross nutrient balance, but there is an error in this dataset for Norway which is currently being corrected (as of February 2026; personal correspondence, EUROSTAT). According to the EUROSTAT metadata, the BNF in this statistic is calculated based on the area of leguminous crops and fixation coefficients. The production of leguminous crops (peas, beans etc) in Norway is very low and we assume that agricultural BNF for the most part determined by leguminous crops such as clover grown on pastures and in fodder production.\n\n(Bleken & Bakken, 1997) based their estimate for BNF from the sale of clover seeds: a sale of about 145 t seeds was estimated to be used to plant 95 000 ha of grass/clover mixtures (655 ha/t seeds). Together with a rate of BNF of 80 kgN/ha on this area, they found a total of 7.6 ktN per year and summed up to 8 ktN to account for BNF from free-living organisms and other sources. The rate of 80 kgN/ha agrees relatively well with later studies of agricultural BNF in Norway, where average values between 10 and 100 kgN/ha have been found; the highest values in particularly productive areas were up to 260 kgN/ha. Yearly statistics of clover seed sales are not available, but according to NIBIO Totalkalkylen [^NIBIO2025b], the area where grass/clover mixes may be sown for pasture and fodder production (fulldyrka eng) has remained constant to within about 3 % from 1995 up to today. Our best estimate for BNF, and for consistency with the previous study, is therefore to assume a constant value of 8 ktN/year. In Sweden [^Moldan2025] the value was found to be 34 kT in 2015, which is more in line with the values found before 2000.\n\n")
            elif "agsm" in norm and "deposition" in norm and "oxn" in norm:
                f.write("**AT.AT-AG.SM-Deposition-OXN**\n\n" + deposition_text + "\n\n")
            elif "agsm" in norm and "deposition" in norm and "rdn" in norm:
                f.write("**AT.AT-AG.SM-Deposition-RDN**\n\n" + deposition_text + "\n\n")
            elif "fsfo" in norm and "fixation" in norm:
                f.write("**AT.AT-FS.FO-N2 fixation-N2**\n\nFollowing the Swedish NBB [^Moldan2025], we use an N-fixation rate of 1.5 kg/ha/year and a forested area of 12.0 mill ha as given by SSB for 2019-2023 (table 14368); we assume this value is constant for our entire time period. This gives an annual N-fixation rate of 18.0 ktN. For comparison, the value for Sweden in 2015 was found to be 39.5 ktN [^Moldan2025].\n\n")
            elif "fsfo" in norm and "deposition" in norm and "oxn" in norm:
                f.write("**AT.AT-FS.FO-Deposition-OXN**\n\n" + deposition_text + "\n\n")
            elif "fsfo" in norm and "deposition" in norm and "rdn" in norm:
                f.write("**AT.AT-FS.FO-Deposition-RDN**\n\n" + deposition_text + "\n\n")
            elif "fsol" in norm and "deposition" in norm and "oxn" in norm:
                f.write("**AT.AT-FS.OL-Deposition-OXN**\n\n" + deposition_text + "\n\n")
            elif "fsol" in norm and "deposition" in norm and "rdn" in norm:
                f.write("**AT.AT-FS.OL-Deposition-RDN**\n\n" + deposition_text + "\n\n")
            elif "hshs" in norm and "deposition" in norm and "oxn" in norm:
                f.write("**AT.AT-HS.HS-Deposition-OXN**\n\n" + deposition_text + "\n\n")
            elif "hshs" in norm and "deposition" in norm and "rdn" in norm:
                f.write("**AT.AT-HS.HS-Deposition-RDN**\n\n" + deposition_text + "\n\n")
            elif "hysw" in norm and "deposition" in norm and "oxn" in norm:
                f.write("**AT.AT-HY.SW-Deposition-OXN**\n\n" + deposition_text + "\n\nFor comparison, the data used in the TEOTIL model gives 3.5 ktN in 2013 and 3.0 ktN in 2023. These comparable but slightly lower values are the results of different datasets used and different data treatment.\n\n")
            elif "hysw" in norm and "deposition" in norm and "rdn" in norm:
                f.write("**AT.AT-HY.SW-Deposition-RDN**\n\n" + deposition_text + "\n\n")
            elif "hysw" in norm and "fixation" in norm:
                f.write("**AT.AT-HY.SW-N2 fixation-N2**\n\nAccording to NIBIO, the surface water area is 20 457 km2 (https://arealbarometer.nibio.no/nb/norge/). According to [^Schäppi2025], the biological fixation rate can vary between < 0.1 tN/km2 in oligotrophic and mesotrophic lakes to up to 10 tN/km2 in eutrophic lakes. Most lakes in Norway are not eutrophic and we use a low value of 0.1 tN/km2, which gives 2 ktN/year.\n\n")
            elif "mpop" in norm and "synthesis" in norm:
                f.write("**AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2**\n\nis found through mass balance where we use data from FAOSTAT Fertilizer by nutrient, domestic fertilizer production, and subtracted the amount of ammonia imported from SSB trade data (table 08801). The result is a very variable curve which probably does not reflect year to year production well and could be a result of how trade statistics are reported.\n\n")
            elif "rwrw" in norm and "outflow" in norm and "oxn" in norm:
                f.write("**AT.AT-RW.RW-Atmospheric outflow-OXN**\n\nIs found using source-receptor data from EMEP [^EMEP2024], as advised by [^Schäppi2025].\n\n")
            elif "rwrw" in norm and "outflow" in norm and "rdn" in norm:
                f.write("**AT.AT-RW.RW-Atmospheric outflow-RDN**\n\nIs found using source-receptor data from EMEP [^EMEP2024], as advised by [^Schäppi2025].\n\n")
            else:
                f.write(f"*Atmospheric outflow plot detected. Filename: `{filename}`.*\n\n")

            # Referanser
            f.write("\n### References\n\n")
            if os.path.exists(bib_filename):
                bib_data = parse_file(bib_filename)
                for key, entry in bib_data.entries.items():
                    authors = entry.persons.get('author', [])
                    author_str = ", ".join([str(a) for a in authors]) if authors else "Unknown Author"
                    year = entry.fields.get('year', 'n.d.')
                    title = entry.fields.get('title', 'No title')
                    journal = entry.fields.get('journal', entry.fields.get('publisher', ''))
                    f.write(f"[^{key}]: {author_str} ({year}). *{title}*. {journal}\n")
            else:
                f.write("*No reference file found.*\n")

    print("[SUKSESS] Portalen er oppdatert med fulle datterfiler!")