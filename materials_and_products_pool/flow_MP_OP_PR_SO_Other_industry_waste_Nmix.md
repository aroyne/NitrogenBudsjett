---
layout: default
title: Other Industry Waste
parent: Other Producing Industry (MP.OP)
nav_order: 10
---

# Other Industry Waste

<iframe src="../output_files/plots/MP_OP_PR_SO_Other_industry_waste_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**MP.OP-PR.SO-Other industry waste-Nmix**: we use data from SSB table 05282 “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og kilde” (1995-2011) and 10514 «Avfallsregnskap for Norge, etter kilde og materialtype (1 000 tonn) 2012 – 2023» with N contents taken from Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> and typical, assumed values are chosen if none are given. The statistic does not separate between food and other industry waste. We make the assumption that everything in the category “wet organic waste” is from the food industry, and all other waste is assigned to other producing industry. Here we also include all waste from “other industries” (annen eller uspesifisert næring). The category “contaminated waste” is very irregularly reported (placed in different sectors in different years) and has therefore been excluded.

There is a change in categorization between the two tables, where the main difference is in the category “other waste” and “mixed waste”. To ensure continuity between the data series we chose a lower value for “other waste” than for “mixed waste”. Values between 1990 and 1994 are extrapolated from 1995 given the change in industry waste reported between 1992 and 1995 reported by SSB (1997)<!--cite:ssb_naturressurser_1997-->.

**How the numbers are derived.** SSB's waste accounts ([Avfallsregnskapet](https://www.ssb.no/natur-og-miljo/avfall/statistikk/avfallsregnskapet); tables [05282](https://www.ssb.no/statbank/table/05282) for 1995–2011 and [10514](https://www.ssb.no/statbank/table/10514) from 2012) give the generated amount of waste by material type and source sector. SSB combines several sources: a periodic survey of about 1,600 manufacturing companies, the companies' own reporting to Miljødirektoratet in the years between, statistics on hazardous waste and waste from construction, figures from the recycling industry, and, where data are missing, estimates based on turnover or number of employees. This flow uses the materials paper, plastics, wood, textiles, other materials, hazardous waste and (from 2012) mixed waste from the source sectors "Bergverk og utvinning", "Industri" and "Annen eller uspesifisert næring", plus wet organic waste from "Bergverk og utvinning". N contents are mainly from Table 50 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf): paper 0.28%, plastics 2.1%, wood 0.25%, textiles 1%, hazardous waste 0.1%; mixed waste (0.9%) and other materials (0.2%) are assumed values.

**Interpretation.** The flow is about 9–10 kt N per year in the mid-1990s, falls to 6–7 kt N after 2010 and is about 6 kt N in 2024. In 2024 mixed waste accounts for about 60% of the N, and hazardous waste and plastics for about 15% each. Since the N contents of mixed waste and other materials are assumed, the level is uncertain.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
* SSB (1997). *Naturressurser og miljø 1997*.
