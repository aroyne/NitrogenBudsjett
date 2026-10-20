---
layout: default
title: Solid Waste Import
parent: Rest of the world (RW)
nav_order: 12
---

# Solid Waste Import

<iframe src="../output_files/plots/RW_RW_PR_SO_Solid_waste_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-PR.SO-Solid waste import-Nmix** is the N in imported municipal and other waste, wastewater sludge, hazardous waste, and plastic, paper and textile waste.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.

#### Interpretations and comparisons

- The flow is small, below 1 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: mixed waste | N content of traded goods | ±50 %, triangular | – | 46% | – | 0.23 | [Solid Waste Export](../processing_of_residues_pool/flow_PR_SO_RW_RW_Solid_waste_export_Nmix.html) |
| N content of traded goods: rubber | N content of traded goods | ±20 %, normal | <1% | 22% | 0.05 | 0.28 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html) and 1 more |
| N content of traded goods: paper waste | N content of traded goods | ±20 %, normal | 90% | 21% | 0.81 | 0.40 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html) |
| N content of traded goods: plastic waste | N content of traded goods | 0.002–0.008, lognormal | 2% | 7% | 0.03 | 0.05 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html) |
| Traded quantities (SSB 08801) (papiravfall) | Registered data | ±5 %, normal, drawn per year | 6% | 1% | 0.81 | 0.40 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html) |
