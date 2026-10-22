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

#### Interpretations and comparisons

- Agricultural use is fairly stable at 100–112 kt N per year, but the domestically produced part falls from about 80–90 kt N in the 1990s to about 55 kt N in 2018–2024, because imports have increased from 12–30 kt N to 39–51 kt N.
- The value for 2022 is higher (72 kt N) because imports were lower that year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| FAOSTAT fertilizers by nutrient (use) | Modelled statistics | ±30 %, normal | 95% | 84% | 1.30 | 1.80 | [Ammonia Synthesis N2 Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html), [Mineral Fertilizer for HS](../materials_and_products_pool/flow_MP_OP_HS_HS_Mineral_fertilizer_Nmix.html) |
| FAOSTAT fertilizers by nutrient (import) | Modelled statistics | ±30 %, normal | 5% | 16% | −0.30 | −0.80 | [Ammonia Synthesis N2 Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html), [Mineral Fertilizer Import](../rest_of_the_world_pool/flow_RW_RW_AG_SM_Mineral_fertilizer_import_Nmix.html) |

### References

* FAO (2025). *Fertilizer by nutrient*. [https://www.fao.org/faostat/en/#data/RFN](https://www.fao.org/faostat/en/#data/RFN)
