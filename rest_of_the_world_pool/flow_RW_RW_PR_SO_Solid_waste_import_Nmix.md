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

- The quantities are multiplied by an N content per waste type, mostly from Table 50 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: municipal waste and residual products from the chemical industry 0.9% (household and similar wastes), paper and cardboard 0.28%, textiles 1.0% and clinical waste 0.1%; sewage sludge 3% (as for domestic sludge), rubber 1.3% (Table 23) and plastics 0.4%, the share of N in imported plastics (SSB 08801, HS 39) from the N-containing polymers polyurethane, polyamide, polyacrylonitrile and cellulose nitrate (Table 23 in Schäppi et al. (2025) gives the N contents of these polymers; Table 50 gives 2.1% for plastic waste, more than the N that enters Norway in plastics).

#### Interpretations

- The flow is small, below 1 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: rubber | N content of traded goods | 0.005–0.02, triangular | 3% | 43% | 0.05 | 0.28 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html) and 1 more |
| N content of traded goods: mixed waste | N content of traded goods | ±50 %, triangular | – | 37% | – | 0.23 | [Solid Waste Export](../processing_of_residues_pool/flow_PR_SO_RW_RW_Solid_waste_export_Nmix.html) |
| N content of traded goods: paper waste | N content of traded goods | ±20 %, normal | 60% | 13% | 0.81 | 0.40 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html) |
| N content of traded goods: textile waste | N content of traded goods | 0.0017–0.029 (min–max), triangular | 32% | 4% | 0.11 | 0.04 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html), [Export for Reuse](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_reuse_Nmix.html) and 1 more |
| Traded quantities (SSB 08801) (papiravfall) | Registered data | ±5 %, normal, drawn per year | 4% | 1% | 0.81 | 0.40 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html) |

### References

* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
