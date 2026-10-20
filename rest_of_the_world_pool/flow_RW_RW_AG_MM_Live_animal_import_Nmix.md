---
layout: default
title: Live Animal Import
parent: Rest of the world (RW)
nav_order: 2
---

# Live Animal Import

<iframe src="../output_files/plots/RW_RW_AG_MM_Live_animal_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-AG.MM-Live animal import-Nmix** is the N in imported live animals.

#### Data sources

- Numbers of imported live animals by type from FAOSTAT (trade in live animals, Crops and livestock products).

#### Assumptions

- Typical live weights per animal type from various sources (animal_weights sheet of N_parameters.xlsx), an average of 16% protein in the whole animal (range 14–22%) and the standard Jones factor 6.25 for nitrogen to protein.

#### Interpretations and comparisons

- The flow is negligible, below 0.05 kt N per year; Norway imports very few live animals.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| Average live weight of horses | Parameter | ±30 %, normal | 36% | 50% | [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html) |
| Protein content of live animals | Parameter | 0.14–0.22, triangular | 48% | 39% | [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html) |
| FAOSTAT crops and livestock products (live animals) | Registered data | ±10 %, normal, drawn per year | 7% | 6% | [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html) |
| Protein-to-N conversion factor (Jones factor) | Parameter | ±10 %, normal | 6% | 5% | [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html), [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html), [Grazing on Unmanaged Land](../forests_and_semi_natural_pool/flow_FS_OL_AG_MM_Grazing_Nmix.html), [Seeds and Planting Material](../materials_and_products_pool/flow_MP_FP_AG_SM_Seeds_and_planting_material__Nmix.html) and 1 more |
