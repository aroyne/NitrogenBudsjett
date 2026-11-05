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

- Typical live weights per animal type, mostly from IPCC (2006), Vol. 4, Ch. 10, Tables 10A-5 to 10A-9 (Western Europe or developed countries), an average of 16% protein in the whole animal (range 14–22%) and the standard Jones factor 6.25 for nitrogen to protein.

#### Interpretations

- The flow is negligible, below 0.05 kt N per year; Norway imports very few live animals.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Average live weight of horses | Parameter | ±30 %, normal | 36% | 50% | 0.75 | 0.98 | [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html) |
| Protein content of live animals | Parameter | 0.14–0.22, triangular | 48% | 39% | 1.00 | 1.00 | [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html) |
| FAOSTAT crops and livestock products (live animals) | Registered data | ±10 %, normal, drawn per year | 7% | 6% | 1.00 | 1.00 | [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html) |
| Protein-to-N conversion factor (Jones factor) | Parameter | ±10 %, normal | 6% | 5% | −0.91 | −0.91 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html), [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html) and 10 more |
