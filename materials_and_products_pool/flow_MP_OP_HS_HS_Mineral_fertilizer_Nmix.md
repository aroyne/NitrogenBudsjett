---
layout: default
title: Mineral Fertilizer for HS
parent: Other Producing Industry (MP.OP)
nav_order: 8
---

# Mineral Fertilizer for HS

<iframe src="../output_files/plots/MP_OP_HS_HS_Mineral_fertilizer_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-HS.HS-Mineral fertilizer-Nmix** is mineral fertilizer used outside agriculture, in gardens, parks and sports grounds.

#### Data sources

- FAOSTAT's [Fertilizers by Nutrient](https://www.fao.org/faostat/en/#data/RFN) (FAO, 2025<!--cite:fao_fertilizer_2025-->) gives agricultural use, production, import and export of nitrogen fertilizers in tonnes N.
- No Norwegian data on fertilizer use in gardens, parks and sports grounds are used.

#### Assumptions

- As advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, we assume a default value of 2% of total mineral fertilizer for non-agricultural use (range 1–3%): agricultural use is multiplied by 0.02/0.98.

#### Interpretations and comparisons

- The flow is about 2 kt N per year and follows agricultural use.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Share of mineral fertiliser used outside agriculture | Parameter | 0.01–0.03, triangular | 76% | 76% | 1.02 | 1.02 | [Ammonia Synthesis N2 Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html) |
| FAOSTAT fertilizers by nutrient (use) | Modelled statistics | ±30 %, normal | 24% | 24% | 1.00 | 1.00 | [Ammonia Synthesis N2 Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html), [Mineral Fertilizer for Agriculture](../materials_and_products_pool/flow_MP_OP_AG_SM_Mineral_fertilizer_Nmix.html) |

### References

* FAO (2025). *Fertilizer by nutrient*. [https://www.fao.org/faostat/en/#data/RFN](https://www.fao.org/faostat/en/#data/RFN)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
