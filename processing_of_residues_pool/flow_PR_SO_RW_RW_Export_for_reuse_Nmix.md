---
layout: default
title: Export for Reuse
parent: Solid Waste (PR.SO)
nav_order: 11
---

# Export for Reuse

<iframe src="../output_files/plots/PR_SO_RW_RW_Export_for_reuse_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.SO-RW.RW-Export for reuse-Nmix** is exported used textiles.

#### Data sources

- Export quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- Used clothing and other used textile articles (HS 6309) are given the N content of textile waste, 1.0% (Table 50 in Schäppi et al., 2025<!--cite:schappi_annexes_2025-->).

#### Interpretations

- The flow rises from 0.01 kt N<!--val:PR.SO-RW.RW-Export for reuse-Nmix:1990--> in 1990 to about 0.3 kt N per year<!--mean:PR.SO-RW.RW-Export for reuse-Nmix:2015-2024--> since 2015.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: textile waste | N content of traded goods | 0.0017–0.029 (min–max), triangular | 100% | 100% | 1.00 | 1.00 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html), [Other Goods Import](../rest_of_the_world_pool/flow_RW_RW_MP_OP_Other_goods_import__Nmix.html) and 1 more |

### References

* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
