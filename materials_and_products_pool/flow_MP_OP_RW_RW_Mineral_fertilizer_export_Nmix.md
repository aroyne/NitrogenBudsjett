---
layout: default
title: Mineral Fertilizer Export
parent: Other Producing Industry (MP.OP)
nav_order: 12
---

# Mineral Fertilizer Export

<iframe src="../output_files/plots/MP_OP_RW_RW_Mineral_fertilizer_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-RW.RW-Mineral fertilizer export-Nmix** is exported mineral fertilizer.

#### Data sources

- FAOSTAT's [Fertilizers by Nutrient](https://www.fao.org/faostat/en/#data/RFN) (FAO, 2025<!--cite:fao_fertilizer_2025-->) gives agricultural use, production, import and export of nitrogen fertilizers in tonnes N.
- For Norway, export quantities are official values for 1990–1992, values from an external organization for 1993–2001 and FAO estimates based on trade data from 2002.
- SSB's trade statistics (table 08801) do not show Norway's fertilizer exports, which are confidential and reported under a combined commodity code, so FAOSTAT is used.

#### Interpretations

- The flow rises from about 430 kt N<!--val:MP.OP-RW.RW-Mineral fertilizer export-Nmix:1990--> in 1990 to 650–790 kt N per year<!--range:MP.OP-RW.RW-Mineral fertilizer export-Nmix:2011-2024--> after 2010, about seven times the agricultural use of mineral fertilizer in Norway.
- The fertilizer is produced from ammonia made in Norway (AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2, about 345 kt N<!--val:AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2:2024--> in 2024) and imported ammonia (RW.RW-MP.OP-Ammonia import -Nmix, about 500 kt N<!--val:RW.RW-MP.OP-Ammonia import -Nmix:2024--> in 2024).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| FAOSTAT fertilizers by nutrient (export) | Modelled statistics | ±30 %, normal | 100% | 100% | 1.00 | 1.00 | [Ammonia Synthesis N<sub>2</sub> Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html) |

### References

* <span id="ref-fao_fertilizer_2025" data-cite="FAO" data-year="2025"></span>FAO (2025). *Fertilizer by nutrient*. [fao.org](https://www.fao.org/faostat/en/#data/RFN)
