---
layout: default
title: Feed Export
parent: Food and Feed Processing (MP.FP)
nav_order: 8
---

# Feed Export

<iframe src="../output_files/plots/MP_FP_RW_RW_Feed_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-RW.RW-Feed export-Nmix** is exported feed, fish feed and pet food, and fish waste and by-products not fit for human consumption (HS 0511), whether or not they are declared for feed.

#### Data sources

- Export quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from the customs declarations for goods crossing the border ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)).

#### Assumptions

- Each commodity code is assigned an N content, mostly from Tables 21 and 25 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, and quantities are multiplied by it.

#### Interpretations

- The flow is 11 kt N<!--val:MP.FP-RW.RW-Feed export-Nmix:1990--> in 1990, 15–27 kt N<!--range:MP.FP-RW.RW-Feed export-Nmix:1991-2007--> in 1991–2007, 15–17 kt N<!--range:MP.FP-RW.RW-Feed export-Nmix:2008-2014--> in 2008–2014 and rises to 33 kt N<!--val:MP.FP-RW.RW-Feed export-Nmix:2024--> in 2024.
- Fish meal (HS 2301 20) is the largest part in the 1990s (7–17 kt N per year in 1992–1998, from 64–154 kt fish meal) and again from 2020 (8–11 kt N). In 2024 the flow also contains oilseed cake and meal (7 kt N), pet food (6 kt N, up from 0.2 kt N in 1990), fresh and frozen fish not for human consumption (6 kt N) and meat meal (3 kt N).
- The 6 kt of fish and crustacean meal exported to Uruguay in 2024 (about 0.6 kt N) is probably krill meal landed there by Norwegian vessels; the krill landed abroad is otherwise added to MP.FP-RW.RW-Food export-Nmix (see that flow).
- The dip in 1993 comes from the export of soybean meal (HS 2304), which fell from 124 kt in 1992 to 16 kt in 1993 and was back at 118 kt in 1994.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: pet food | N content of traded goods | ±40 %, normal | 1% | 39% | 0.02 | 0.19 | none |
| N content of traded goods: fish meal | N content of traded goods | ±20 %, normal | 69% | 26% | 0.60 | 0.30 | none |
| N content of traded goods: oilcrops | N content of traded goods | ±20 %, normal | 18% | 14% | 0.26 | 0.23 | [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| Traded quantities (SSB 08801) (for) | Registered data | ±5 %, normal, drawn per year | 9% | 11% | 0.87 | 0.79 | none |
| N content of traded goods: fish fresh frozen | N content of traded goods | ±20 %, normal | 3% | 5% | 0.12 | 0.12 | [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| N content of traded goods: meat meal | N content of traded goods | ±20 %, normal | <1% | 4% | 0.00 | 0.13 | none |

### References

* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
