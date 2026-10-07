---
layout: default
title: Food Industry Waste
parent: Food and Feed Processing (MP.FP)
nav_order: 6
---

# Food Industry Waste

<iframe src="../output_files/plots/MP_FP_PR_SO_Food_industry_waste_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-PR.SO-Food industry waste-Nmix** is food waste from the food industry, including the primary sector (fisheries and slaughter houses).

#### Data sources

- SSB's waste accounts ([Avfallsregnskapet](https://www.ssb.no/natur-og-miljo/avfall/statistikk/avfallsregnskapet)): table [05282](https://www.ssb.no/statbank/table/05282) “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og kilde” (1995–2011) and table [10514](https://www.ssb.no/statbank/table/10514) «Avfallsregnskap for Norge, etter kilde og materialtype (1 000 tonn)» (2012 onward) give the generated amount of waste by material type and source sector. The statistic does not separate between food and other industry waste.
- SSB combines several sources: a periodic survey of about 1,600 manufacturing companies, the companies' own reporting to Miljødirektoratet in the years between, statistics on hazardous waste and waste from construction, figures from the recycling industry, and, where data are missing, estimates based on turnover or number of employees.
- According to Chaudhary & Skjerpen (2025)<!--cite:chaudhary_matavfall_2025--> everything in the industry category “wet organic waste” is from the food industry.
- Prior to 2012, the category “wet organic waste” included park and garden waste and some other mixed waste. The values reported from 1995 to 2011 are therefore significantly larger than from 2012.

#### Assumptions

- This flow uses wet organic waste ("Våtorganisk avfall") from the source sectors "Jord-, skogbruk og fiske", "Industri" and "Annen eller uspesifisert næring", multiplied by an N content of 0.9% (Table 50 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->).
- We assume that the 2011 value should have been equal to that in 2012, and scale the values prior to 2011 by the ratio between the 2011 and 2012 value.
- For 1990–1994 we extrapolate using the mean value for 1995–1999.

#### Interpretations and comparisons

- The flow is about 1.2–1.5 kt N per year until 2017 and 1.6–2.4 kt N from 2018.
- The industry sector (mainly food and fish processing) is the largest source of wet organic waste.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Chaudhary, M. & Skjerpen, C. (2025). *Matavfall og matsvinnstatistikk*.
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
