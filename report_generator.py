# report_generator.py
"""
Builds the GitHub Pages documentation portal from the Monte Carlo plots: the
landing page (index.md) and one page per pool, subpool and flow.

Every page has two parts. The top (frontmatter, heading, plot or mass-balance
embed) is regenerated on every run from the page table in report_pages.py.
The text below it lives between <!-- MANUAL:...:START/END --> markers in the
.md file itself and is never overwritten; flow descriptions and pool texts
are edited directly in the .md files.

A plot in output_files/plots without an entry in report_pages.py gets a new
flow page with a placeholder text, under the same parent as the existing
flows with the same pool and subpool code.
"""
import os
import re
from datetime import datetime

from report_pages import PAGES

POOL_FOLDERS = [
    "energy_and_fuels_pool",
    "materials_and_products_pool",
    "agriculture_pool",
    "forests_and_semi_natural_pool",
    "processing_of_residues_pool",
    "humans_and_settlements_pool",
    "atmosphere_pool",
    "hydrosphere_pool",
    "rest_of_the_world_pool",
]
NEW_PAGE_TEXT = "*No description yet.*"


def get_balance_image_markdown(pool_code, plot_files, plot_dir, relative_depth="", target_format = 'html'):
    """Returnerer bilde-markdown hvis balanseplottet eksisterer, ellers tom streng."""
    if target_format == "pdf":
        balance_file = f"balance_{pool_code.replace('.', '_')}.png"
        if balance_file in plot_files:
            return (
                f"\n---\n\n"
                f"## Mass Balance Overview (1990-2024)\n\n"
                f"The chart below illustrates the integrated nitrogen mass balance for **{pool_code}**. "
                f"It includes total system inflows (positive stack), total outflows (negative stack), "
                f"and the net balance line with estimated uncertainty bounds (±1σ).\n\n"
                f"![Mass Balance {pool_code}]({relative_depth}{plot_dir}/{balance_file})\n"
            )
    else:
        balance_file = f"balance_{pool_code.replace('.', '_')}.html"
        if balance_file in plot_files:
            return (
                f"\n---\n\n"
                f"## Interactive Mass Balance Overview (1990-2024)\n\n"
                f"Hover over the chart to inspect specific streams, or click legend items to toggle visibility.\n\n"
                f'<iframe src="{relative_depth}{plot_dir}/{balance_file}" '
                f'width="100%" height="600px" frameborder="0" scrolling="no"></iframe>\n'            )
    return ""


def get_flow_image_markdown(exact_flow_code, filename, plot_dir, target_format, relative_depth="../"):
    """
    Returns the markdown/HTML snippet embedding a single flow's plot: a static
    image for PDF, or an iframe to the interactive Plotly version (generated
    alongside the PNG in utils_stat.py's process_and_export_mc_results, same
    filename with a .html extension) for the website. Falls back to the
    static image if the interactive file isn't present.
    """
    if target_format != "pdf":
        html_filename = filename.rsplit('.', 1)[0] + '.html'
        return (
            f'<iframe src="{relative_depth}{plot_dir}/{html_filename}" '
            f'width="100%" height="400px" frameborder="0" scrolling="no"></iframe>'
        )
    return f"![{exact_flow_code}]({relative_depth}{plot_dir}/{filename})"


def _extract_manual_block(existing_path, block_name):
    """
    Returns the text saved between a page's <!-- MANUAL:{block_name}:START/END -->
    markers, or None if the page or the markers don't exist yet. Lets a page's
    hand-edited narrative text survive being regenerated for its auto-managed
    parts (frontmatter, heading, plot embed).
    """
    if not os.path.exists(existing_path):
        return None
    with open(existing_path, 'r', encoding='utf-8') as f:
        existing_content = f.read()
    start_marker = f"<!-- MANUAL:{block_name}:START -->"
    end_marker = f"<!-- MANUAL:{block_name}:END -->"
    match = re.search(re.escape(start_marker) + r'\n(.*?)\n' + re.escape(end_marker), existing_content, re.DOTALL)
    return match.group(1) if match else None


def _wrap_manual_block(text, block_name):
    return f"<!-- MANUAL:{block_name}:START -->\n{text}\n<!-- MANUAL:{block_name}:END -->\n"


def write_page_with_manual_block(full_path, header_block, default_body, block_name):
    """
    Writes an .md page whose top (frontmatter, heading, plot embed - built by
    the caller into header_block) is always regenerated fresh, while the
    narrative body below it is preserved verbatim from any existing hand-edit,
    found via the block's MANUAL markers. default_body only seeds the block
    the first time this exact page is written; once the markers exist, this
    function never overwrites what's between them.
    """
    existing_text = _extract_manual_block(full_path, block_name)
    body = existing_text if existing_text is not None else default_body
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(header_block)
        f.write(_wrap_manual_block(body, block_name))



def _frontmatter(page):
    lines = ["layout: default", f"title: {page['title']}"]
    if 'parent' in page:
        lines.append(f"parent: {page['parent']}")
    lines.append(f"nav_order: {page['nav_order']}")
    if page.get('has_children'):
        lines.append("has_children: true")
    return "---\n" + "\n".join(lines) + "\n---\n\n"


def _page_header(page, plot_files, plot_dir, target_format):
    """The regenerated top of a page, down to the MANUAL block."""
    if page['kind'] == 'flow':
        plot_png = page['file'][len('flow_'):-len('.md')] + '.png'
        return (_frontmatter(page) + f"# {page['title']}\n\n"
                + get_flow_image_markdown(page['title'], plot_png, plot_dir, target_format)
                + "\n\n### Description\n")
    body = page['intro']
    if page['balance']:
        body = body.replace('{BALANCE}', get_balance_image_markdown(
            page['balance'], plot_files, plot_dir, relative_depth="../", target_format=target_format))
    return _frontmatter(page) + body


def _new_flow_pages(plot_files):
    """Pages for flow plots that are not in report_pages.py yet. The pool
    folder and parent are taken from existing flows with the same first two
    code parts (e.g. 'AG_SM'); an unknown prefix raises a KeyError."""
    known = {p['file'] for p in PAGES}
    by_prefix = {}
    for p in PAGES:
        if p['kind'] == 'flow':
            prefix = '_'.join(p['file'][len('flow_'):].split('_')[:2])
            by_prefix.setdefault(prefix, p)
    new_pages = []
    for f in plot_files:
        if not f.endswith('.png') or f.startswith('balance_'):
            continue
        name = f"flow_{f[:-len('.png')]}.md"
        if name in known:
            continue
        sibling = by_prefix['_'.join(f.split('_')[:2])]
        nav = 1 + max(p['nav_order'] for p in PAGES + new_pages
                      if p['kind'] == 'flow' and p.get('parent') == sibling['parent'])
        new_pages.append({'folder': sibling['folder'], 'file': name, 'title': f[:-len('.png')].replace('_', ' '),
                          'nav_order': nav, 'parent': sibling['parent'], 'kind': 'flow'})
        print(f"[RAPPORT] Ny strømside uten beskrivelse: {sibling['folder']}/{name}")
    return new_pages


def write_pages(plot_files, plot_dir, bib_filename, target_format):
    """Writes every pool, subpool and flow page. Flow pages are only written
    when the flow's plot exists."""
    for page in PAGES + _new_flow_pages(plot_files):
        if page['kind'] == 'flow' and page['file'][len('flow_'):-len('.md')] + '.png' not in plot_files:
            continue
        os.makedirs(page['folder'], exist_ok=True)
        path = os.path.join(page['folder'], page['file'])
        block = "FLOW_DESCRIPTION" if page['kind'] == 'flow' else "POOL_TEXT"
        write_page_with_manual_block(path, _page_header(page, plot_files, plot_dir, target_format), NEW_PAGE_TEXT, block)
        with open(path, 'a', encoding='utf-8') as f:
            append_bibtex_references(f, bib_filename)


def append_bibtex_references(file_handle, bib_filename=None):
    """
    Writes a placeholder References section. The real, APA7-formatted
    reference list (and inline \\citep/\\citet replacement) is built once for
    every page at the end of the whole run, by fix_all_citations_in_folder -
    this only needs to handle the case where no bib file is available at all,
    since fix_all_citations_in_folder skips its pass entirely in that case.
    """
    if not bib_filename or not os.path.exists(bib_filename):
        file_handle.write("\n### References\n\nNo bibliography file provided or found.\n")
        return

    file_handle.flush()
    with open(file_handle.name, 'r', encoding='utf-8') as f_read:
        content = f_read.read()

    if '\\citep' in content or '\\citet' in content:
        file_handle.write("\n### References\n\n")

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
    

def get_short_author(raw_author_str):
    if not raw_author_str or raw_author_str == 'Unknown':
        return 'Unknown'
    
    # Splitter på " and " for å isolere hver forfatter
    authors = raw_author_str.split(" and ")
    last_names = []
    
    for auth in authors:
        auth = auth.strip()
        if "," in auth:
            # Hvis 'Etternavn, Fornavn', hent det som står før komma
            last_names.append(auth.split(",")[0].strip())
        else:
            # Every personal author in library.bib uses "Etternavn, Fornavn"
            # with a comma; an author string with no comma is therefore an
            # institutional name (e.g. "Norwegian Environment Agency") and
            # must be kept whole rather than reduced to its last word.
            last_names.append(auth.strip())
            
    # Formater i henhold til antall forfattere (APA7 i tekst)
    if len(last_names) == 1:
        return last_names[0]
    elif len(last_names) == 2:
        return f"{last_names[0]} & {last_names[1]}"
    else:
        return f"{last_names[0]} et al."

def fix_all_citations_in_folder(paths, bib_filename):
    """
    Resolves \\citep/\\citet markup and rebuilds the References list on
    every .md file in paths (generated pages, or folders of them). Each page
    is rewritten from its first '### References' line onward, so only report
    output may be passed - never the project root, which also holds notes
    and other hand-written Markdown.
    """
    if not os.path.exists(bib_filename):
        print(f"Bib-fil ikke funnet: {bib_filename}")
        return

    # 1. Pars .bib-filen (utvidet for APA7 detaljer)
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
                else:
                    # BibTeX bruker ofte {Ord}-beskyttelse rundt enkeltord inni verdien
                    # (for å bevare stor forbokstav); disse skal aldri vises til leseren.
                    val = val.replace('{', '').replace('}', '')
                
                if key in ['author', 'year', 'title', 'journal', 'booktitle', 'publisher', 'url', 'doi', 'volume', 'number', 'pages']:
                    references_dict[current_entry][key] = val
                    
    # Every resolved in-text citation is tagged with an invisible
    # <!--cite:key1,key2--> comment recording its BibTeX key(s). Once a
    # \citep{}/\citet{} is resolved to plain "(Author, Year)" text, that raw
    # markup is gone from the file - without this tag, a later rerun (e.g.
    # after a manual edit adds one new citation elsewhere on the same page)
    # would only find the new \citep{}/\citet{} still present and rebuild the
    # References list from that alone, silently dropping every
    # already-resolved reference even though its "(Author, Year)" text is
    # still sitting in the body. The tag makes every past citation
    # permanently rediscoverable, so the References list can be rebuilt
    # in full on every run, however many times the page is hand-edited.
    def citep_replacer(match):
        keys = [k.strip() for k in match.group(1).split(',')]
        parts = []
        for key in keys:
            if key in references_dict:
                author = references_dict[key].get('author', 'Unknown')
                short_author = get_short_author(author)
                year = references_dict[key].get('year', 'n.d.')
                parts.append(f"{short_author}, {year}")
            else:
                parts.append(key)
        return f"({'; '.join(parts)})<!--cite:{','.join(keys)}-->"

    def citet_replacer(match):
        keys = [k.strip() for k in match.group(1).split(',')]
        parts = []
        for key in keys:
            if key in references_dict:
                author = references_dict[key].get('author', 'Unknown')
                short_author = get_short_author(author)  # Bruker ny logikk her
                year = references_dict[key].get('year', 'n.d.')
                parts.append(f"{short_author} ({year})")
            else:
                parts.append(f"{key} (n.d.)")
        return ", ".join(parts) + f"<!--cite:{','.join(keys)}-->"


    # 2. Gå igjennom alle filer
    def _walk(paths):
        for path in paths:
            if os.path.isfile(path):
                yield os.path.dirname(path) or '.', [], [os.path.basename(path)]
            else:
                yield from os.walk(path)

    for root, dirs, files in _walk(paths):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(root, filename)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if '\\citep' in content or '\\citet' in content or '<!--cite:' in content:
                    raw_keys = re.findall(r'\\+cite[pt]\{\s*([^}]+)\s*\}', content)
                    tag_keys = re.findall(r'<!--cite:([^>]+)-->', content)
                    cited_keys = set()
                    for k_group in raw_keys + tag_keys:
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
                            
                            raw_author = entry.get('author', 'Unknown Author')
                            author = format_apa_authors(raw_author)
                            year = entry.get('year', 'n.d.')
                            title = entry.get('title', 'Untitled')
                            
                            journal = entry.get('journal') or entry.get('booktitle') or entry.get('publisher') or ""
                            volume = entry.get('volume', '')
                            number = entry.get('number', '')
                            pages = entry.get('pages', '')
                            
                            doi = entry.get('doi', '')
                            url = entry.get('url', '')
                            
                            # 1. Forfatter (År).
                            ref_str = f"* {author} ({year})."
                            
                            # 2. Tittel på artikkelen (Vanlig tekst i APA7 hvis journal er oppgitt)
                            if journal:
                                ref_str += f" {title}."
                            else:
                                ref_str += f" *{title}*."
                            
                            # 3. Journal, Volum(Issue), Sider
                            if journal:
                                journal_clean = journal.replace(r'\&', '&')
                                # Journal og Volum skal være i kursiv: *Journal, Volum*
                                if volume:
                                    ref_str += f" *{journal_clean}, {volume}*"
                                else:
                                    ref_str += f" *{journal_clean}*"
                                
                                # Issue/Number skal stå i vanlige parenteser rett bak volumet (ikke kursiv)
                                if number:
                                    ref_str += f"({number})"
                                    
                                # Sidetall legges til på slutten, separert med komma
                                if pages:
                                    # Erstatt eventuelle LaTeX-bindestreker (--) med vanlig bindestrek
                                    pages_clean = pages.replace('--', '-')
                                    ref_str += f", {pages_clean}."
                                else:
                                    ref_str += "."
                                
                            # 4. Lenke-håndtering (Klikkbare Markdown-lenker for GitHub Pages)
                            if doi:
                                # Vask doi-strengen for vanlige formateringsfeil fra .bib
                                doi_clean = doi.lower().replace("doi.org/", "").replace("https://", "").replace("http://", "")
                                doi_url = f"https://doi.org/{doi_clean}"
                                # APA7 anbefaler å vise hele URL-en som klikkbar lenke
                                ref_str += f" [{doi_url}]({doi_url})"
                            elif url:
                                # Gjør den vanlige nettside-urlen klikkbar
                                ref_str += f" [{url}]({url})"
                                
                            formatted_refs.append(ref_str)
                            
                    ref_block += "\n".join(formatted_refs) + "\n"
                    final_content = base_content + ref_block
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(final_content)

                    
# ==============================================================================
# SPESIFIKKE FUNKSJONER FOR HVER ENKELT POOL
# ==============================================================================

def build_landing_page(output_filename, current_date_str, bib_filename, target_format="html"):
    """Genererer hovedlandingssiden (index.md) med kritisk advarsel og oppdaterte Sankey-lenker."""
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
        
        if target_format == "html":
            f.write("### Interactive National Nitrogen Flow Map\n")
            f.write("The diagram below illustrates the integrated nitrogen economy of Norway. "
                    "Use the **slider at the bottom** or press **Play** to explore how the flow magnitudes "
                    "have evolved over time. Flows are color-coded by chemical/functional type "
                    "(e.g., gray for inert N₂, red for NOx, orange for NH₃/RDN, green for Nmix).\n\n")
            
            # Informasjon og bryter/lenke for å se diagrammet uten de dominerende strømmene ---
            f.write("> 💡 **Tip:** The national budget is highly dominated by fertilizer production and trade, and by "
                    "crude oil export. If you want to study the smaller, internal environmental and agricultural cycles "
                    "more closely, you can view the "
                    "**[Sankey Map with Dominant Trade Flows Hidden](output_files/plots/global_nitrogen_sankey_no_fertilizer.html)** "
                    "(fertilizer/ammonia trade and crude oil export removed).\n\n")
            
            # Standard visning (Viser alle strømmer)
            f.write('<iframe src="output_files/plots/global_nitrogen_sankey.html" '
                    'width="100%" height="900px" frameborder="0" scrolling="no"></iframe>\n\n')
            f.write("---\n\n")
        else:
            # Fallback-tekst hvis man bygger en statisk PDF via Pandoc
            f.write("> **Note on Interactive Content:** Interactive, animated Sankey diagrams showing the "
                    "evolution of national nitrogen flows (both complete and with fertilizer trade hidden) are available in the web-based "
                    "version of this report.\n\n")
            f.write("---\n\n")
            
        f.write("For flows connected to the hydrosphere, and for land-relateds emissions and nitrogen deposition, "
                "we only consider the Norwegian mainland. For emissions to air reported through the UNFCCC framework we "
                "also include emissions from Norwegian economic activity on Svalbard (these are minor and mainly related to coal extraction, "
                "which has now been discontinued). We also include emissions and N flows that originate in petroleum extraction on the Norwegian "
                "continental shelf.\n"
                "This NNB is built using the guidelines from \\citep{winiwarter_inms_2025}. Where flows are omitted or added to better fit "
                "the Norwegian nitrogen system, this is commented. ")
        append_bibtex_references(f, bib_filename)
        
        


def generate_github_pages_report(plot_dir='output_files/plots', output_filename='index.md', bib_filename='library.bib', target_format='html'):
    if not os.path.exists(plot_dir):
        print(f"[INFO] Fant ikke mappen '{plot_dir}'. Rapporten ble ikke laget.")
        return

    plot_files = sorted([f for f in os.listdir(plot_dir) if f.endswith('.png') or f.endswith('.html')])
    if not plot_files:
        print(f"[INFO] Ingen plot-filer funnet i '{plot_dir}'.")
        return

    current_date_str = datetime.now().strftime("%B %d, %Y")

    print("[RAPPORT] Sletter gamle midlertidige filer fra pool-mappene for å unngå rot...")
    for f_old in os.listdir('.'):
        if (f_old.startswith("flow_") or f_old.startswith("pool_") or f_old.startswith("subpool_")) and f_old.endswith(".md"):
            os.remove(f_old)

    print("[RAPPORT] Bygger hierarkisk dokumentasjonsportal med egne pool-mapper...")
    build_landing_page(output_filename, current_date_str, bib_filename)
    write_pages(plot_files, plot_dir, bib_filename, target_format)

    # Resolve citations and rebuild References on the generated pages only.
    print("[RAPPORT] Konverterer LaTeX-siteringer til ren tekst...")
    fix_all_citations_in_folder(POOL_FOLDERS + [output_filename], bib_filename)

    print("[RAPPORT] Portalbygging fullført suksessfullt!")

# You can merge and convert the generated Markdown files into a finished PDF
# by running the following in the terminal:
#
# pandoc pool_rest_of_the_world.md flow_*.md \
#   --citeproc \
#   --bibliography=references.bib \
#   --csl=apa.csl \
#   -V geometry:margin=1in \
#   -o nitrogen_rapport.pdf