"""
Numbers quoted in the article, collected in one table per topic:

  1. balance of every pool and subpool,
  2. NUE for agriculture,
  3. the other figures quoted in the manuscript, by manuscript section.

Each row gives the mean of the median series over a start and an end period,
the 2.5-97.5 % interval of the same mean across MC iterations (variant (i):
each iteration is one consistent time series), and the Mann-Kendall p-value
of the median series. Series that depend on Fodder crops (how N is split
between AG.MM and AG.SM) end in 2018-2020 and are tested for trend over
1990-2020, because SSB changed the method for eng til slått in 2021 and the
resulting step is not corrected.

Series definitions are taken from calculations_for_article.py so the two
scripts cannot disagree; that script's method note
(claude_tekst/2026-09-25_calculations_for_article_metodenotat.md) documents
each definition. Writes claude_tekst/artikkeltall.md.

Run after main_mc.py --pool all --nsim 1000 --export-raw-mc.
"""
import datetime
import os
import subprocess
import sys

import numpy as np
import pandas as pd

import calculations_for_article as cfa

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'article_figures'))
from make_total_balance import BOUNDARY_SUBPOOLS  # noqa: E402
from make_total_balance_excl_oil_fertilizer import EXCLUDED_FLOWS as OIL_FERTILIZER_FLOWS  # noqa: E402

OUTPUT_NOTE = 'claude_tekst/artikkeltall.md'
OUTPUT_WORD_TABLE = 'claude_tekst/artikkeltall_balansetabell.xlsx'
YEARS = list(cfa.ANALYSIS_YEARS)
START = (1990, 1992)
END = (2022, 2024)
END_FODDER = (2018, 2020)

POOLS = {
    'EF': ['EF.EC', 'EF.IC', 'EF.TR', 'EF.OE'],
    'MP': ['MP.FP', 'MP.OP'],
    'AG': ['AG.MM', 'AG.SM'],
    'FS': ['FS.FO', 'FS.OL'],
    'PR': ['PR.SO', 'PR.WW'],
    'HS': [],
    'AT': [],
    'HY': ['HY.SW', 'HY.CW', 'HY.AC'],
    'RW': [],
}
# Row labels in the manuscript's balance table, which names one-subpool
# pools HS and AT by pool code and RW by its subpool code.
WORD_TABLE_LABELS = {'RW': 'RW.RW'}
# Balances that depend on how Fodder crops splits N between AG.MM and AG.SM.
FODDER_DEPENDENT_POOLS = {'AG.MM', 'AG.SM'}

FS_GRAZING = ['FS.OL-AG.MM-Grazing-Nmix']
FORESTRY_PRODUCTS = ['FS.FO-EF.OE-Fuel wood for households-Nmix', 'FS.FO-MP.OP-Industrial round wood-Nmix']
EMISSION_SPECIES = ['NOx', 'NH3', 'N2O']
GOTHENBURG_BASE_YEAR = 2005


# =============================================================================
# Series not defined in calculations_for_article.py
# =============================================================================

def share_of_pool_inputs(df, flows, prefix, years=cfa.ANALYSIS_YEARS):
    """flows as a share (%) of all inflows to the pool or subpool prefix."""
    return 100 * cfa.sum_flows(df, flows, years) / cfa.sum_flows(df, cfa._pool_flows(df, prefix, 'in'), years)


def national_balance(df, years=cfa.ANALYSIS_YEARS, exclude=()):
    """Inflows minus outflows across the boundary of the whole economy (AT.AT,
    HY.CW and RW.RW), as in article_figures/make_total_balance.py: a flow
    counts when exactly one end is a boundary subpool."""
    inflows, outflows = [], []
    for f in df['flow_name'].unique():
        if f in exclude:
            continue
        source, target = f.split('-')[0], f.split('-')[1]
        if (source in BOUNDARY_SUBPOOLS) == (target in BOUNDARY_SUBPOOLS):
            continue
        (inflows if source in BOUNDARY_SUBPOOLS else outflows).append(f)
    return cfa.sum_flows(df, inflows, years) - cfa.sum_flows(df, outflows, years)


def emissions_total(df, species, years=cfa.ANALYSIS_YEARS):
    """National emissions of one species (kt N/yr): every flow named
    '<pool>-AT.AT-Emissions-<species>', as in
    article_figures/make_emissions_timeseries.py."""
    flows = [f for f in df['flow_name'].unique() if f.endswith(f'-AT.AT-Emissions-{species}')]
    return cfa.sum_flows(df, flows, years)


# =============================================================================
# Statistics per row
# =============================================================================

_MATRICES = {}


def mc_matrix(fn, sims, function):
    """cfa.mc_series_matrix, computed once per series (keyed by its
    'Beregning' label, which identifies the calculation)."""
    if function not in _MATRICES:
        _MATRICES[function] = cfa.mc_series_matrix(fn, sims, YEARS)
    return _MATRICES[function]


def _mean(series_or_row, period):
    a, b = period
    cols = [YEARS.index(y) for y in range(a, b + 1)]
    return series_or_row[..., cols].mean(axis=-1)


def summarize(label, fn, df, sims, fodder=False, mc=True, function=''):
    """One table row: start/end period means as the median and 2.5-97.5 %
    interval across MC iterations of each iteration's own period mean
    (variant (i)), or of the median series if the row has no MC, and the
    Mann-Kendall p-value of the median series over 1990-2024 (1990-2020 if
    fodder). For balances the median of the sum is used rather than the sum
    of the medians, which can fall outside the interval (e.g. HY.AC, which
    balances exactly in every iteration)."""
    end = END_FODDER if fodder else END
    series = fn(df)
    values = series.reindex(YEARS).values
    trend_years = [y for y in YEARS if y <= end[1]]
    _, _, p = cfa.mann_kendall(values[:len(trend_years)])
    row = {'label': label, 'function': function, 'fodder': fodder, 'end': end,
           'start_value': _mean(values, START), 'end_value': _mean(values, end),
           'p': p, 'trend_end': trend_years[-1], 'mc': mc}
    if mc:
        matrix = mc_matrix(fn, sims, function)
        row['start_value'], *row['start_ci'] = np.percentile(_mean(matrix, START), [50, 2.5, 97.5])
        row['end_value'], *row['end_ci'] = np.percentile(_mean(matrix, end), [50, 2.5, 97.5])
    return row


def period_value(label, fn, df, sims, period, function=''):
    """Mean over one period, median and 2.5-97.5 % across MC iterations."""
    matrix = mc_matrix(fn, sims, function)
    value, *ci = np.percentile(_mean(matrix, period), [50, 2.5, 97.5])
    return {'label': label, 'function': function, 'period': period, 'value': value, 'ci': ci}


def ratio_row(label, fn, df, sims, start, end, function=''):
    """Mean over end divided by mean over start within each MC iteration,
    median and 2.5-97.5 %."""
    matrix = mc_matrix(fn, sims, function)
    value, *ci = np.percentile(_mean(matrix, end) / _mean(matrix, start), [50, 2.5, 97.5])
    return {'label': label, 'function': function, 'start': start, 'end': end, 'value': value, 'ci': ci}


# =============================================================================
# Formatting
# =============================================================================

def fmt(x):
    if not np.isfinite(x):
        return '–'
    if abs(x) >= 100:
        return f"{x:.0f}"
    if abs(x) >= 10:
        return f"{x:.1f}"
    return f"{x:.2f}"


def fmt_p(p):
    return '<0.001' if p < 0.001 else f"{p:.3f}"


def period_label(period):
    return str(period[0]) if period[0] == period[1] else f"{period[0]}–{str(period[1])[2:]}"


def value_ci(value, ci):
    return f"{fmt(value)} [{fmt(ci[0])}, {fmt(ci[1])}]"


def trend_table(rows):
    out = ["| Størrelse | 1990–92 [MC (i) 2,5–97,5 %] | Slutt [MC (i) 2,5–97,5 %] | MK p (periode) | Beregning |",
           "|---|---:|---:|---:|---|"]
    for r in rows:
        mark = ' †' if r['fodder'] else ''
        if r['mc']:
            start, end = value_ci(r['start_value'], r['start_ci']), value_ci(r['end_value'], r['end_ci'])
        else:
            start, end = fmt(r['start_value']), fmt(r['end_value'])
        out.append(f"| {r['label']}{mark} | {start} | {period_label(r['end'])}: {end} "
                   f"| {fmt_p(r['p'])} (1990–{r['trend_end']}) | `{r['function']}` |")
    return "\n".join(out)


def single_table(rows):
    out = ["| Størrelse | Periode | Verdi [MC (i) 2,5–97,5 %] | Beregning |", "|---|---|---:|---|"]
    for r in rows:
        if 'start' in r:
            period = f"{period_label(r['end'])} / {period_label(r['start'])}"
        else:
            period = period_label(r['period'])
        out.append(f"| {r['label']} | {period} | {value_ci(r['value'], r['ci'])} | `{r['function']}` |")
    return "\n".join(out)


# =============================================================================
# Main
# =============================================================================

def pool_rows(df, sims):
    rows = []
    for pool, subpools in POOLS.items():
        rows.append(summarize(f"**{pool}**", lambda d, p=pool: cfa.pool_balance(d, p), df, sims,
                              function=f"pool_balance('{pool}')"))
        rows[-1]['code'] = WORD_TABLE_LABELS.get(pool, pool)
        for sub in subpools:
            rows.append(summarize(f"&nbsp;&nbsp;{sub}", lambda d, p=sub: cfa.pool_balance(d, p), df, sims,
                                  fodder=sub in FODDER_DEPENDENT_POOLS, function=f"pool_balance('{sub}')"))
            rows[-1]['code'] = sub
    rows.append(summarize("**Hele økonomien** (mot AT.AT, HY.CW, RW.RW)", national_balance, df, sims,
                          function='national_balance'))
    rows.append(summarize("**Hele økonomien uten olje og gjødselproduksjon**",
                          lambda d: national_balance(d, exclude=OIL_FERTILIZER_FLOWS), df, sims,
                          function='national_balance(exclude=…)'))
    return rows


def nue_rows(df, sims):
    q2 = lambda d: cfa.q2_corrected_ag_whole_nue(d)[1]  # noqa: E731
    return [
        summarize("Q1a AG-NUE, hele jordbruket (eksterne strømmer)", cfa.q1a_ag_whole_nue, df, sims, function='q1a_ag_whole_nue'),
        summarize("Q1b AG.MM-NUE", cfa.q1b_ag_mm_nue, df, sims, fodder=True, function='q1b_ag_mm_nue'),
        summarize("Q1c AG.SM-NUE", cfa.q1c_ag_sm_nue, df, sims, fodder=True, function='q1c_ag_sm_nue'),
        summarize("Q2 AG-NUE korrigert for fôrimport", q2, df, sims, fodder=True, function='q2_corrected_ag_whole_nue'),
        summarize("Q3 matsystem-NUE, landbasert", cfa.q3_food_system_nue, df, sims, function='q3_food_system_nue'),
        summarize("Q3 matsystem-NUE med villfisk og akvakultur", cfa.q3_food_system_nue_incl_fish, df, sims,
                  function='q3_food_system_nue_incl_fish'),
        summarize("Fjørfe + svin, andel av N i husdyrprodukter (%) (uten MC)",
                  lambda d: cfa.poultry_pork_share_of_animal_products(), df, sims, mc=False,
                  function='poultry_pork_share_of_animal_products'),
    ]


def other_rows(df, sims):
    s = lambda label, fn, function, **kw: summarize(label, fn, df, sims, function=function, **kw)  # noqa: E731
    sections = {
        'MP': [
            s("Ammoniakkimport (kt N/år)", cfa.ammonia_import, 'ammonia_import'),
            s("Eksport av mineralgjødsel (kt N/år)", cfa.fertilizer_export, 'fertilizer_export'),
        ],
        'AG': [
            s("Samlede N-tap fra jordbruket (kt N/år)", cfa.ag_losses_total, 'ag_losses_total'),
            s("Fôrtap som lukker AG.MM-balansen (% av Fodder crops)", cfa.fodder_loss_to_close_mm,
              'fodder_loss_to_close_mm', fodder=True),
            s("Fôrtap som lukker AG.SM-balansen (% av Fodder crops)", cfa.fodder_loss_to_close_sm,
              'fodder_loss_to_close_sm', fodder=True),
            s("Fodder crops inkl. innmarksbeite (kt N/år)", lambda d: cfa.sum_flows(d, cfa.FODDER_CROPS),
              'sum_flows(FODDER_CROPS)', fodder=True),
        ],
        'FS': [
            s("Beite, andel av tilførsel til FS.OL (%)",
              lambda d: share_of_pool_inputs(d, FS_GRAZING, 'FS.OL'), "share_of_pool_inputs(FS_GRAZING, 'FS.OL')"),
            s("Skogprodukter, andel av tilførsel til FS.FO (%)",
              lambda d: share_of_pool_inputs(d, FORESTRY_PRODUCTS, 'FS.FO'),
              "share_of_pool_inputs(FORESTRY_PRODUCTS, 'FS.FO')"),
        ],
        'PR': [
            s("Avfall til energi (kt N/år)", cfa.waste_to_energy, 'waste_to_energy'),
            s("Gjenvinning inkl. eksport til gjenvinning og ombruk (kt N/år)", cfa.recycling_all, 'recycling_all'),
            s("N fjernet som N2 i avløpsrensing, andel (%)", cfa.ww_n2_removal_share, 'ww_n2_removal_share'),
        ],
        'HS': [
            s("Husholdnings- og næringsavfall (kt N/år)", cfa.household_waste, 'household_waste'),
            s("Matvarer + forbruksvarer, andel av tilførsel til HS (%)", cfa.hs_food_and_consumer_goods_share,
              'hs_food_and_consumer_goods_share'),
        ],
        'AT': [
            s("AT-balanse uten N2-fiksering til ammoniakk (kt N/år)",
              lambda d: cfa.at_balance(d, exclude=cfa.AMMONIA_SYNTHESIS), 'at_balance(exclude=AMMONIA_SYNTHESIS)'),
            s("AT-balanse, redusert N (kt N/år)", lambda d: cfa.at_balance(d, species='RDN'), "at_balance(species='RDN')"),
            s("AT-balanse, oksidert N (kt N/år)", lambda d: cfa.at_balance(d, species='OXN'), "at_balance(species='OXN')"),
            s("Grensekryssende innstrøm minus utstrøm (kt N/år)", cfa.cross_border_net_inflow, 'cross_border_net_inflow'),
            s("N2-fiksering til ammoniakkproduksjon (kt N/år)",
              lambda d: cfa.sum_flows(d, cfa.AMMONIA_SYNTHESIS), 'sum_flows(AMMONIA_SYNTHESIS)'),
            s("Nedfall totalt, land og ferskvann (kt N/år)", cfa.deposition_total, 'deposition_total'),
            s("Biologisk N2-fiksering, alle pooler (kt N/år)", cfa.bnf_total, 'bnf_total'),
            s("Nedfall på jordbruksareal, AG.SM (kt N/år)", lambda d: cfa.sum_flows(d, cfa.DEPOSITION_SM),
              'sum_flows(DEPOSITION_SM)'),
        ],
        'HY': [
            s("Tilførsel til kystvann fra HY.SW (kt N/år)", lambda d: cfa.sum_flows(d, cfa.INFLOW_TO_COASTAL_WATERS),
              'sum_flows(INFLOW_TO_COASTAL_WATERS)'),
            s("Akvakulturproduksjon (kt N/år)", lambda d: cfa.sum_flows(d, cfa.AQUACULTURE_PRODUCTION),
              'sum_flows(AQUACULTURE_PRODUCTION)'),
            s("Ekskresjon, andel av akvakulturfôr (%)", cfa.excreta_share_of_aquafeed, 'excreta_share_of_aquafeed'),
            s("Ekskresjon, andel av tilførsel til HY.CW (%)",
              lambda d: cfa.cw_input_share(d, cfa.AQUACULTURE_EXCRETA), 'cw_input_share(AQUACULTURE_EXCRETA)'),
            s("Tilførsel fra HY.SW, andel av tilførsel til HY.CW (%)",
              lambda d: cfa.cw_input_share(d, cfa.INFLOW_TO_COASTAL_WATERS), 'cw_input_share(INFLOW_TO_COASTAL_WATERS)'),
            s("Renset avløpsvann, andel av tilførsel til HY.CW (%)",
              lambda d: cfa.cw_input_share(d, cfa.TREATED_WASTEWATER), 'cw_input_share(TREATED_WASTEWATER)'),
            s("Villfisk og skalldyr, i forhold til tilførsel til HY.CW (%)",
              lambda d: cfa.cw_input_share(d, cfa.WILD_CATCH_AND_SHELLFISH), 'cw_input_share(WILD_CATCH_AND_SHELLFISH)'),
        ],
        'Utslipp': [
            s(f"Utslipp {sp}, hele landet (kt N/år)", lambda d, sp=sp: emissions_total(d, sp), f"emissions_total('{sp}')")
            for sp in EMISSION_SPECIES
        ],
    }
    singles = [
        period_value("Samlede N-tap fra jordbruket (kt N/år)", cfa.ag_losses_total, df, sims, (1990, 1991), 'ag_losses_total'),
        period_value("Fôrtap som lukker AG.MM-balansen (% av Fodder crops)", cfa.fodder_loss_to_close_mm, df, sims,
                     (2018, 2020), 'fodder_loss_to_close_mm'),
        period_value("N fjernet som N2 i avløpsrensing, andel (%)", cfa.ww_n2_removal_share, df, sims, (2023, 2023),
                     'ww_n2_removal_share'),
        ratio_row("Akvakulturproduksjon, forhold slutt/start", lambda d: cfa.sum_flows(d, cfa.AQUACULTURE_PRODUCTION),
                  df, sims, START, END, 'sum_flows(AQUACULTURE_PRODUCTION)'),
    ]
    for sp in EMISSION_SPECIES:
        for year in (2020, 2023, 2024):
            singles.append(ratio_row(f"Utslipp {sp}, {year} i forhold til {GOTHENBURG_BASE_YEAR}",
                                     lambda d, sp=sp: emissions_total(d, sp), df, sims,
                                     (GOTHENBURG_BASE_YEAR, GOTHENBURG_BASE_YEAR), (year, year),
                                     f"emissions_total('{sp}')"))
    return sections, singles


def write_word_table(rows):
    """The pool/subpool balance table laid out as in the manuscript (one row
    per pool or subpool, three value columns), rounded to whole kt N. Copy
    the value cells in Excel and paste them into the selected cells of the
    Word table ("Overwrite cells")."""
    whole = lambda x: str(round(x))  # noqa: E731 (round() returns an int, so never '-0')
    out = []
    for r in rows:
        if 'code' not in r:
            continue
        mark = '†' if r['fodder'] else ''
        out.append({
            'Pool/subpool': r['code'],
            '1990-1992 median [2.5-97.5 %]': f"{whole(r['start_value'])} [{whole(r['start_ci'][0])}, {whole(r['start_ci'][1])}]",
            '2022-2024 median [2.5-97.5 %]': f"{whole(r['end_value'])} [{whole(r['end_ci'][0])}, {whole(r['end_ci'][1])}]{mark}",
            'Mann-Kendall p': fmt_p(r['p']) + mark,
        })
    table = pd.DataFrame(out)
    with pd.ExcelWriter(OUTPUT_WORD_TABLE) as writer:
        table.to_excel(writer, index=False, sheet_name='Balanser')
        note = pd.DataFrame({'Merknad': [
            "† 2018-2020 i stedet for 2022-2024, og trend testet for 1990-2020 (Fodder crops, SSBs metodeskifte i 2021).",
            "Verdi: median av periodesnittet over MC-iterasjonene (variant (i)). Intervall: 2,5-97,5 % av samme snitt.",
            "MK p: Mann-Kendall på medianserien. Kt N/år, avrundet til hele tall.",
        ]})
        note.to_excel(writer, index=False, sheet_name='Merknader')
    print(f"Skrevet: {OUTPUT_WORD_TABLE}")


def household_waste_shares_table():
    base, q = cfa.household_waste_sector_shares()
    out = ["| Sektor | " + " | ".join(base.index) + " |", "|---|" + "---:|" * len(base.index)]
    for sector in base.columns:
        cells = [f"{base.loc[p, sector]:.1f} [{q.loc[p, (sector, 0.025)]:.1f}, {q.loc[p, (sector, 0.975)]:.1f}]"
                 for p in base.index]
        out.append(f"| {sector} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def check_ag_balances(df):
    """The generic pool_balance and the explicit AG.MM/AG.SM flow lists in
    calculations_for_article.py must give the same balance."""
    for prefix, explicit in (('AG.MM', cfa.ag_mm_balance), ('AG.SM', cfa.ag_sm_balance)):
        diff = (cfa.pool_balance(df, prefix) - explicit(df)).abs().max()
        if diff > 1e-9:
            raise ValueError(f"pool_balance('{prefix}') differs from the explicit flow list by up to {diff:.3g} kt N")


def main():
    df = cfa.load_stats()
    check_ag_balances(df)
    sims = cfa.load_raw_simulations(all_flows=True)
    head = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
    stats_time = datetime.datetime.fromtimestamp(os.path.getmtime(cfa.STATS_FILE)).strftime('%Y-%m-%d %H:%M')

    pools = pool_rows(df, sims)
    nue = nue_rows(df, sims)
    sections, singles = other_rows(df, sims)

    parts = [f"""# Tall til artikkelen

**Generert** av `article_numbers.py`. Ikke rediger for hånd; kjør skriptet på nytt etter hver modellkjøring.

- Modellkjøring: `{cfa.STATS_FILE}` skrevet {stats_time}, {len(sims)} MC-iterasjoner
- Git HEAD ved generering: `{head}`

**Lesing av tabellene.** Hver MC-iterasjon gir ett snitt over perioden (variant (i), feil fullt korrelert i tid). Verdien er medianen av disse snittene, og intervallet er 2,5- og 97,5-persentilen. Rader uten MC viser snittet av medianserien. MK p er Mann-Kendall-testen på medianserien. Forholdstall mot 2005 for NOx og NH3 har nesten ingen MC-spredning, fordi usikkerheten i disse er en faktor som er lik for alle år og faller bort i forholdet. Rader merket † avhenger av hvordan Fodder crops fordeler N mellom AG.MM og AG.SM. SSB endret metoden for eng til slått i 2021, og spranget er ikke korrigert, så for disse radene er sluttperioden 2018–20 og trenden testet for 1990–2020. Kolonnen «Beregning» viser funksjonen i `calculations_for_article.py` (eller i dette skriptet), dokumentert i `claude_tekst/2026-09-25_calculations_for_article_metodenotat.md`. Alle balanser er tilførsel minus fraførsel (kt N/år), uten interne strømmer mellom delpooler i samme pool.

## 1. Balanser for pooler og delpooler (kt N/år)

{trend_table(pools)}

## 2. NUE for jordbruket (%)

{trend_table(nue)}
"""]
    parts.append("## 3. Andre tall i manuskriptet\n")
    for name, rows in sections.items():
        parts.append(f"### {name}\n\n{trend_table(rows)}\n")
    parts.append(f"### Enkeltperioder og forholdstall\n\n{single_table(singles)}\n")
    parts.append(f"### Andel av husholdnings- og næringsavfall per sektor (%) [MC over N-innhold i avfallet]\n\n"
                 f"`household_waste_sector_shares`\n\n{household_waste_shares_table()}\n")

    write_word_table(pools)
    with open(OUTPUT_NOTE, 'w') as f:
        f.write("\n".join(parts))
    print(f"Skrevet: {OUTPUT_NOTE}")


if __name__ == '__main__':
    main()
