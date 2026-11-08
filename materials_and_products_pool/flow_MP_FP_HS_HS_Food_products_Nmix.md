---
layout: default
title: Food Products to Consumers
parent: Food and Feed Processing (MP.FP)
nav_order: 3
---

# Food Products to Consumers

<iframe src="../output_files/plots/MP_FP_HS_HS_Food_products_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-HS.HS-Food products-Nmix** is food products to consumers – households, restaurants, canteens and institutions – and pet food.
- The flow includes food that is later wasted in retail, food service and households. Food waste upstream of MP.FP (agriculture, seafood landing) or within the food industry is not included, since it is covered by other flows.
- Cross-border shopping is not included.
- Horse feed is accounted for under the agriculture pool.

#### Data sources

- Protein in the food supply at wholesale level ("engrosnivå", matforsyningsstatistikken) per person per day, from Helsedirektoratet's annual report Utviklingen i norsk kosthold (Helsedirektoratet, 2025, Table 7; earlier years from the 2017, 2022, 2023 and 2024 editions)<!--cite:helsedirektoratet_kosthold_2025-->. The food supply is calculated by NIBIO from statistics of production, import, export and sales of food, and gives the edible amount of food available to the whole population. Values are published for 1980, 1990, 2000, 2005 and every year from 2010.
- Population on 1 January from SSB ([table 06913](https://www.ssb.no/statbank/table/06913)).
- Nitrogen intake per cat and dog per year from Table 19 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, and the number of cats and dogs from available statistics from a variety of sources.

#### Assumptions

- Protein per person per day is multiplied by 365 and by the population, and divided by the Jones factor 6.25.
- Years between the published years are linearly interpolated (1984–1989, 1991–1999, 2001–2004 and 2006–2009).
- We have assumed (based on available statistics) that cats and dogs consume >90% of pet food. The number of cats and dogs is taken from linear trend lines fitted to counts for 1999, 2001, 2004, 2022 and 2023 (from veterinary, industry and news sources) and extended to 1985–1998 and 2024 (about 580 000 dogs and 760 000 cats in 2024), with 4.73 and 3.04 kg N per animal per year.

#### Interpretations

- The flow rises from about 26 kt N<!--val:MP.FP-HS.HS-Food products-Nmix:1990--> in 1990 to 37–38 kt N<!--range:MP.FP-HS.HS-Food products-Nmix:2022-2024--> in 2022–2024, of which pet food is about 5 kt N in 2024.
- The increase is driven by population growth (4.2 million in 1990, 5.6 million in 2024), a rise in protein per person from 94 to 100–106 g per day, and the growing number of pets.
- SSB's diet statistics based on food sold in grocery stores ([Kosthald](https://www.ssb.no/kosthald), [table 13695](https://www.ssb.no/statbank/table/13695)) give about 73 g protein per person per day in 2024, about 28 g less than the wholesale level. The difference is food eaten outside the home, food bought at kiosks and petrol stations, and waste in wholesale and retail, which the grocery sales do not cover.
- Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> advises using FAO statistics on food availability for human food consumption (FAO Food Balance Sheets, from 2010), which give a bit more than 40 kt N per year. The food balance sheets give meat as carcass weight and fish as live-weight equivalents, including bones, heads and other parts that are removed in processing, while the wholesale-level food supply used here gives the edible amount.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Food supply at wholesale level (Helsedirektoratet) | Modelled statistics | ±10 %, normal | 38% | 50% | 0.88 | 0.87 | none |
| Protein-to-N conversion factor (Jones factor) | Parameter | ±10 %, normal | 32% | 42% | −0.80 | −0.79 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html), [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html) and 10 more |
| N in pet food per dog per year | Parameter | ±30 %, normal | 2% | 3% | 0.06 | 0.07 | none |
| Annual N intake per cat from pet food | Parameter | ±30 %, normal | 2% | 2% | 0.06 | 0.06 | none |
| Population (SSB 06913) | Registered data | ±2 %, normal, drawn per year | 2% | 2% | 0.88 | 0.87 | [Municipal Wastewater](../humans_and_settlements_pool/flow_HS_HS_PR_WW_Municipal_wastewater_Nmix.html) |
| Interpolation (1990-2000) | Gap filling: interpolation | ±7–13 %, lognormal, grows with distance to known year | 25% | – | 0.88 | – | none |

### References

* Helsedirektoratet (2025). *Utviklingen i norsk kosthold 2025*. [helsedirektoratet.no](https://www.helsedirektoratet.no/rapporter/utviklingen-i-norsk-kosthold-2025)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
