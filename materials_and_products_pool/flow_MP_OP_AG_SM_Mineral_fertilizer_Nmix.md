---
layout: default
title: Mineral Fertilizer for Agriculture
parent: Other Producing Industry (MP.OP)
nav_order: 1
---

# Mineral Fertilizer for Agriculture

<iframe src="../output_files/plots/MP_OP_AG_SM_Mineral_fertilizer_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-AG.SM-Mineral fertilizer-Nmix** is domestically produced mineral fertilizer used in agriculture.

#### Data sources

- FAOSTAT's [Fertilizers by Nutrient](https://www.fao.org/faostat/en/#data/RFN) (FAO, 2025<!--cite:fao_fertilizer_2025-->) gives agricultural use, production, import and export of nitrogen fertilizers in tonnes N.
- For Norway, agricultural use is reported as official values (for 1995–2000 taken from an external organization), while imports are FAO estimates from 2002 onwards and official values or values from an external organization before that.

#### Assumptions

- The flow is agricultural use minus imports, so all imported fertilizer is assumed to be used in agriculture (it enters AG.SM directly as RW.RW-AG.SM-Mineral fertilizer import-Nmix).

#### Interpretations

- Agricultural use is 85–112 kt N per year<!--range:MP.OP-AG.SM-Mineral fertilizer-Nmix+RW.RW-AG.SM-Mineral fertilizer import-Nmix:1990-2024-->, but the domestically produced part falls from about 80–105 kt N<!--range:MP.OP-AG.SM-Mineral fertilizer-Nmix:1990-1999--> in the 1990s to about 55 kt N<!--mean:MP.OP-AG.SM-Mineral fertilizer-Nmix:2018-2024--> in 2018–2024, because imports have increased from 7–30 kt N<!--range:RW.RW-AG.SM-Mineral fertilizer import-Nmix:1990-1999--> to 39–53 kt N<!--range:RW.RW-AG.SM-Mineral fertilizer import-Nmix:2018-2024-->.
- The value for 2022 is higher (72 kt N<!--val:MP.OP-AG.SM-Mineral fertilizer-Nmix:2022-->) because imports were lower that year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| FAOSTAT fertilizers by nutrient (use) | Modelled statistics | ±30 %, normal | 95% | 84% | 1.30 | 1.80 | [Ammonia Synthesis N<sub>2</sub> Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html), [Mineral Fertilizer for HS](../materials_and_products_pool/flow_MP_OP_HS_HS_Mineral_fertilizer_Nmix.html) |
| FAOSTAT fertilizers by nutrient (import) | Modelled statistics | ±30 %, normal | 5% | 16% | −0.30 | −0.80 | [Ammonia Synthesis N<sub>2</sub> Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html), [Mineral Fertilizer Import](../rest_of_the_world_pool/flow_RW_RW_AG_SM_Mineral_fertilizer_import_Nmix.html) |

### References

* FAO (2025). *Fertilizer by nutrient*. [fao.org](https://www.fao.org/faostat/en/#data/RFN)
