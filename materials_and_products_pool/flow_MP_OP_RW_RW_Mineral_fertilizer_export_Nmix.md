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

#### Interpretations and comparisons

- The flow rises from about 430 kt N in 1990 to 650–790 kt N per year after 2010, about seven times the agricultural use of mineral fertilizer in Norway.
- The fertilizer is produced from ammonia made in Norway (AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2, about 345 kt N in 2024) and imported ammonia (RW.RW-MP.OP-Ammonia import -Nmix, about 500 kt N in 2024).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| FAOSTAT fertilizers by nutrient (export) | Modelled statistics | ±30 %, normal | 100% | 100% | [Ammonia Synthesis N2 Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html) |

### References

* FAO (2025). *Fertilizer by nutrient*. [https://www.fao.org/faostat/en/#data/RFN](https://www.fao.org/faostat/en/#data/RFN)
