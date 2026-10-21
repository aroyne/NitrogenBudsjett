---
layout: default
title: Mineral Fertilizer Import
parent: Rest of the world (RW)
nav_order: 3
---

# Mineral Fertilizer Import

<iframe src="../output_files/plots/RW_RW_AG_SM_Mineral_fertilizer_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-AG.SM-Mineral fertilizer import-Nmix** is imported mineral fertilizer N.
- Because anhydrous ammonia is not used directly as fertilizer in Norway, it is not counted as a fertilizer in the FAO statistic; NH3 import is accounted for in the flow RW.RW-MP.OP-Ammonia import-Nmix.

#### Data sources

- The import quantity of fertilizer N from FAOSTAT Fertilizers by Nutrient (FAO, 2025<!--cite:fao_fertilizer_2025-->).

#### Assumptions

- Imported fertilizer is counted as used in agriculture, and MP.OP-AG.SM-Mineral fertilizer-Nmix is FAOSTAT's agricultural use minus this import.

#### Interpretations and comparisons

- The flow varies between about 6 and 51 kt N per year and has been 39–51 kt N since 2018, so a growing share of the fertilizer used in Norwegian agriculture is imported.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| FAOSTAT fertilizers by nutrient (import) | Modelled statistics | ±30 %, normal | 100% | 100% | 1.00 | 1.00 | [Ammonia Synthesis N2 Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html), [Mineral Fertilizer for Agriculture](../materials_and_products_pool/flow_MP_OP_AG_SM_Mineral_fertilizer_Nmix.html) |

### References

* FAO (2025). *Fertilizer by nutrient*. [https://www.fao.org/faostat/en/#data/RFN](https://www.fao.org/faostat/en/#data/RFN)
