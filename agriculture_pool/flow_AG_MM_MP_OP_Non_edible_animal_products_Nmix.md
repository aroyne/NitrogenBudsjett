---
layout: default
title: Non-edible Animal Products
parent: Manure Management (AG.MM)
nav_order: 7
---

# Non-edible Animal Products

<iframe src="../output_files/plots/AG_MM_MP_OP_Non_edible_animal_products_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.MM-MP.OP-Non-edible animal products-Nmix** is the N in wool and raw hides and skins.

#### Data sources

- Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> advises using FAOSTAT Commodity Balances (non-food). For Norway this statistic only contains wool for 4 individual years.
- The amount of wool delivered by farmers from 2005, compiled from Landbruksdirektoratet's delivery data (Landbruksdirektoratet, 2025)<!--cite:landbruksdirektoratet_leveransedata-slakt-2005-2012_2025-->.
- The number of winter-fed sheep (SSB table 03710).
- Production of raw hides and skins from FAOSTAT Crops and livestock products.
- N contents from Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- Before 2005, wool is estimated as the number of winter-fed sheep (SSB table 03710) times a fixed ratio of 3.8 kg wool per sheep, fitted to sheep numbers and wool delivered in 2005–2024 (least squares through the origin).

#### Interpretations

- The flow is about 1.2–1.3 kt N per year<!--range:AG.MM-MP.OP-Non-edible animal products-Nmix:1990-2015--> until 2015 and falls to about 1.0 kt N<!--val:AG.MM-MP.OP-Non-edible animal products-Nmix:2024--> in 2024.
- Hides and skins are 0.59–0.70 kt N per year with no trend. Wool is 0.58–0.66 kt N per year until 2015 (about half of the flow) and falls to 0.45 kt N in 2024 (43%), so the decline comes from wool.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| FAOSTAT crops and livestock products (production) | Registered data | ±10 %, normal, drawn per year | 8% | 38% | 0.50 | 0.57 | [Animal Products](../agriculture_pool/flow_AG_MM_MP_FP_Animal_products_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of animal product: Raw hides and skins | Parameter | ±10 % | 8% | 36% | 0.50 | 0.57 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of wool | Parameter | ±10 %, normal | 8% | 21% | 0.50 | 0.43 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Wool deliveries (Norwegian Agriculture Agency) | Registered data | ±5 %, normal, drawn per year | – | 5% | – | 0.43 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Number of sheep (SSB 03710) | Registered data | ±5 %, normal, drawn per year | 2% | – | 0.50 | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Wool per sheep per year | Parameter | ±30 %, normal | 73% | – | 0.50 | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |

### References

* <span id="ref-landbruksdirektoratet_leveransedata-slakt-2005-2012_2025" data-cite="Landbruksdirektoratet" data-year="2025"></span>Landbruksdirektoratet (2025). *leveransedata-slakt-2005-2012*. [github.com](https://github.com/LandbruksdirektoratetGIT/opendata/tree/main/datasets/leveransedata-slakt-2005-2012)
* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
