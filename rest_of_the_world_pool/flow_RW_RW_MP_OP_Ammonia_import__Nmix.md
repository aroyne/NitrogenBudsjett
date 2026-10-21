---
layout: default
title: Ammonia Import
parent: Rest of the world (RW)
nav_order: 10
---

# Ammonia Import

<iframe src="../output_files/plots/RW_RW_MP_OP_Ammonia_import__Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-MP.OP-Ammonia import-Nmix** is imported ammonia (HS 2814), anhydrous and in aqueous solution.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.

#### Interpretations and comparisons

- The flow is about 170–490 kt N per year, one of the largest N flows in the model; the ammonia is used in fertilizer production at Herøya and most of the N leaves Norway again as exported mineral fertilizer.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Traded quantities (SSB 08801) (NH3) | Registered data | ±5 %, normal, drawn per year | 100% | 100% | 1.00 | 1.00 | [Ammonia Synthesis N2 Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
