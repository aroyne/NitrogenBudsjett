---
layout: default
title: Export for Recycling
parent: Solid Waste (PR.SO)
nav_order: 10
---

# Export for Recycling

<iframe src="../output_files/plots/PR_SO_RW_RW_Export_for_recycling_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.SO-RW.RW-Export for recycling-Nmix** is plastic, paper and textile waste which has been collected for recycling and exported to recycling facilities outside of Norway.

#### Data sources

- Export quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.

#### Interpretations and comparisons

- The flow rises from about 0.2 kt N in 1990 to about 2 kt N per year since 2017, mainly plastic waste for recycling.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: rubber | N content of traded goods | 0.005–0.02, triangular | <1% | 53% | 0.01 | 0.29 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Other Goods Import](../rest_of_the_world_pool/flow_RW_RW_MP_OP_Other_goods_import__Nmix.html) and 1 more |
| N content of traded goods: paper waste | N content of traded goods | ±20 %, normal | 91% | 23% | 0.95 | 0.56 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Solid Waste Import](../rest_of_the_world_pool/flow_RW_RW_PR_SO_Solid_waste_import_Nmix.html) |
| N content of traded goods: plastic waste | N content of traded goods | 0.002–0.008, lognormal | 3% | 22% | 0.04 | 0.15 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Solid Waste Import](../rest_of_the_world_pool/flow_RW_RW_PR_SO_Solid_waste_import_Nmix.html) |
| Traded quantities (SSB 08801) (papiravfall) | Registered data | ±5 %, normal, drawn per year | 6% | 1% | 0.95 | 0.56 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Solid Waste Import](../rest_of_the_world_pool/flow_RW_RW_PR_SO_Solid_waste_import_Nmix.html) |
