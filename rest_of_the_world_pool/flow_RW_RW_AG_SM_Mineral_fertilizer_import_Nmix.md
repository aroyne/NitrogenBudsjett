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
- Because anhydrous ammonia is not used directly as fertilizer in Norway, it is not counted as a fertilizer in the FAO statistic; NH<sub>3</sub> import is accounted for in the flow RW.RW-MP.OP-Ammonia import-Nmix.

#### Data sources

- The import quantity of fertilizer N from FAOSTAT Fertilizers by Nutrient (FAO, 2025<!--cite:fao_fertilizer_2025-->).

#### Assumptions

- Imported fertilizer is counted as used in agriculture, and MP.OP-AG.SM-Mineral fertilizer-Nmix is FAOSTAT's agricultural use minus this import.

#### Interpretations

- The flow varies between about 6 and 51 kt N per year and has been 39–51 kt N since 2018, so a growing share of the fertilizer used in Norwegian agriculture is imported.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| FAOSTAT fertilizers by nutrient (import) | Modelled statistics | ±30 %, normal | 100% | 100% | 1.00 | 1.00 | [Ammonia Synthesis N<sub>2</sub> Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html), [Mineral Fertilizer for Agriculture](../materials_and_products_pool/flow_MP_OP_AG_SM_Mineral_fertilizer_Nmix.html) |

### References

* FAO (2025). *Fertilizer by nutrient*. [https://www.fao.org/faostat/en/#data/RFN](https://www.fao.org/faostat/en/#data/RFN)
