#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:50:36 2026

@author: anja
"""
# report_generator.py
import os
from pybtex.database import parse_file

def generate_github_pages_report(plot_dir='output_files/plots', output_filename='index.md', bib_filename='referanser.bib'):
    """
    Skanner plot-mappen og genererer index.md med utfyllende tekst,
    figurer og automatiske referanser fra Zotero.
    """
    if not os.path.exists(plot_dir):
        print(f"[INFO] Fant ikke mappen '{plot_dir}'. Rapporten ble ikke laget.")
        return

    plot_files = sorted([f for f in os.listdir(plot_dir) if f.endswith('.png')])
    if not plot_files:
        print(f"[INFO] Ingen PNG-filer funnet i '{plot_dir}'.")
        return

    print("[RAPPORT] Starter generering av den store rapportsiden...")

    with open(output_filename, 'w', encoding='utf-8') as f:
        # Tittel og introduksjon
        f.write("# Vedlegg: Resultater fra Monte Carlo-simuleringer\n\n")
        f.write("Dette dokumentet inneholder en detaljert oversikt over tidsutvikling, ")
        f.write("usikkerhetsintervaller og massebalanser for den norske nitrogenmodellen.\n\n")
        
        # Her kan du skrive lange avsnitt med tekst om metoden, bakgrunn osv.
        f.write("### Metodebeskrivelse\n")
        f.write("Modellen kjører en Monte Carlo-simulering der det legges på støy basert på ")
        f.write("usikkerhetstyper spesifisert i datagrunnlaget. Dette gir oss mulighet til å ")
        f.write("analysere feilforplantning gjennom komplekse nitrogenstrømmer.\n\n")
        
        f.write("---\n\n")
        
        # 2. Klikkbar Innholdsfortegnelse
        f.write("## Innholdsfortegnelse\n")
        for filename in plot_files:
            clean_name = filename.replace('.png', '').replace('_', ' ')
            anchor = filename.replace('.png', '').lower().replace('_', '-')
            f.write(f"* [{clean_name}](#{anchor})\n")
        f.write("\n---\n\n")

        # 3. Loope gjennom alle figurer og legge til spesifikk tekst
        for filename in plot_files:
            clean_name = filename.replace('.png', '').replace('_', ' ')
            f.write(f"## {clean_name}\n\n")
            f.write(f"![{clean_name}]({plot_dir}/{filename})\n\n")
            
            # Tips: Her kan du bruke 'if'-setninger for å legge til skreddersydd tekst til spesifikke figurer!
            if "ammonia_synthesis" in filename.lower():
                f.write("*Kommentar til figuren:* Her ser vi effekten av den høye ammoniakkimporten i 2006, ")
                f.write("som i enkelte støytilfeller tvinger den biologiske fikseringen under null [^faostat2025].\n\n")
            
            f.write("---\n\n")

        # 4. Referanseliste fra Zotero helt til slutt
        f.write("## Referanser\n\n")
        if os.path.exists(bib_filename):
            bib_data = parse_file(bib_filename)
            for key, entry in bib_data.entries.items():
                authors = entry.persons.get('author', [])
                author_str = ", ".join([str(a) for a in authors]) if authors else "Ukjent forfatter"
                year = entry.fields.get('year', 'u.å.')
                title = entry.fields.get('title', 'Ingen tittel')
                journal = entry.fields.get('journal', entry.fields.get('publisher', ''))
                f.write(f"[^{key}]: {author_str} ({year}). *{title}*. {journal}\n")
        else:
            f.write("*Ingen referansefil (referanser.bib) funnet.*\n")

    print(f"[SUKSESS] Hele rapportdokumentet '{output_filename}' er oppdatert.")