---
layout: default
title: Live Animal Export
parent: Manure Management (AG.MM)
nav_order: 8
---

# Live Animal Export

<iframe src="../output_files/plots/AG_MM_RW_RW_Live_animal_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.MM-RW.RW-Live animal export-Nmix** is the N in exported live animals.

#### Data sources

- FAOSTAT's trade statistics for live animals ([TCL](https://www.fao.org/faostat/en/#data/TCL), Crops and livestock products) give the number of animals exported per year and animal category. FAOSTAT reports poultry in thousands of animals.
- Average live weights per category from the IPCC 2006 Guidelines (Vol. 4, Ch. 10, Annex 10A) and other sources.

#### Assumptions

- Poultry numbers are converted from thousands to animals.
- The number is multiplied by an average live weight per category (e.g. other cattle 420 kg, breeding pigs 198 kg, sheep 48.5 kg, goats 38.5 kg, horses 377 kg, laying hens 1.8 kg; animal_weights in N_parameters.xlsx), an average of 16% protein in the whole animal based on typical values in Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> and the standard Jones factor 6.25 for nitrogen to protein.

#### Interpretations and comparisons

- The flow is very small, below 0.03 kt N per year.
- Pigs and horses make up most of the exported animals.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Protein content of live animals | Parameter | 0.14–0.22, triangular | 50% | 49% | 1.00 | 1.00 | [Live Animal Import](../rest_of_the_world_pool/flow_RW_RW_AG_MM_Live_animal_import_Nmix.html) |
| Average live weight of pigs | Parameter | ±30 %, normal | 8% | 33% | 0.30 | 0.70 | [Live Animal Import](../rest_of_the_world_pool/flow_RW_RW_AG_MM_Live_animal_import_Nmix.html) |
| FAOSTAT crops and livestock products (live animals) | Registered data | ±10 %, normal, drawn per year | 7% | 7% | 1.00 | 1.00 | [Live Animal Import](../rest_of_the_world_pool/flow_RW_RW_AG_MM_Live_animal_import_Nmix.html) |
| Protein-to-N conversion factor (Jones factor) | Parameter | ±10 %, normal | 6% | 6% | −0.91 | −0.91 | [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html), [Grazing on Unmanaged Land](../forests_and_semi_natural_pool/flow_FS_OL_AG_MM_Grazing_Nmix.html), [Seeds and Planting Material](../materials_and_products_pool/flow_MP_FP_AG_SM_Seeds_and_planting_material__Nmix.html), [Food Products to Consumers](../materials_and_products_pool/flow_MP_FP_HS_HS_Food_products_Nmix.html) and 1 more |
| Average live weight of horses | Parameter | ±30 %, normal | 29% | 5% | 0.65 | 0.28 | [Live Animal Import](../rest_of_the_world_pool/flow_RW_RW_AG_MM_Live_animal_import_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
