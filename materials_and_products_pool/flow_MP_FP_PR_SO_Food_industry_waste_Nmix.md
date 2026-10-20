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
- From 2012 the flow also includes the food industry's share of mixed waste from "Industri" in table 10514 (35%, from [SSB table 14457](https://www.ssb.no/statbank1/table/14457/): 36% in 2015 and 33% in 2022). Before 2012 this waste was spread across the material types in table 05282, partly as wet organic waste (counted here) and partly as other materials (counted in MP.OP-PR.SO-Other industry waste-Nmix). The scaling of 1995–2011 therefore uses wet organic waste only, so the flow steps up by about 0.6 kt N in 2012 while the sum with other industry waste does not change. SSB table 14457 also shows that 99–100% of the wet organic waste from manufacturing comes from the food industry.

#### Interpretations and comparisons

- The flow is about 1.2–1.5 kt N per year until 2017 and 1.6–2.4 kt N from 2018.
- The industry sector (mainly food and fish processing) is the largest source of wet organic waste.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of wet organic waste | N content of waste | 0.004–0.0165, triangular | 78% | 89% | 1.00 | 1.00 | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) and 3 more |
| Waste accounts from 2012, industry (SSB 10514) | Modelled statistics | ±30 %, normal | 10% | 10% | 0.86 | 0.77 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html) |
| Splice SSB waste accounts 05282 to 10514, food industry waste | Splice between data sources | ±15 %, normal | 4% | – | 1.00 | – | none |
| Held constant or averaged (food industry waste:1995-1999) | Gap filling: held constant or averaged | ±15–35 %, lognormal, grows with distance to known year | 8% | – | 1.00 | – | none |

### References

* Chaudhary, M. & Skjerpen, C. (2025). *Matavfall og matsvinnstatistikk*.
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
