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
        f.write("---\nlayout: default\ntitle: Home\nav_order: 1\n---\n\n")
        f.write("# Nitrogen Budget for Norway\n\n")
        
        # Siste oppdatert-merknad
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

        with open(full_flow_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write("layout: default\n")
            f.write