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

- Before 2005, wool is estimated from the number of sheep with a linear regression between sheep numbers and wool delivered in 2005–2024.

#### Interpretations and comparisons

- The flow is about 1.2–1.3 kt N per year until 2015 and falls to about 1.0 kt N in 2024.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| FAOSTAT crops and livestock products (production) | Registered data | ±10 %, normal, drawn per year | 8% | 38% | [Animal Products](../agriculture_pool/flow_AG_MM_MP_FP_Animal_products_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of animal product: Raw hides and skins | Parameter | ±10 % | 8% | 36% | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of wool | Parameter | ±10 %, normal | 8% | 21% | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Wool deliveries (Norwegian Agriculture Agency) | Registered data | ±5 %, normal, drawn per year | – | 5% | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Number of sheep (SSB 03710) | Registered data | ±5 %, normal, drawn per year | 2% | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Wool per sheep per year | Parameter | ±30 %, normal | 73% | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |

### References

* Landbruksdirektoratet (2025). *leveransedata-slakt-2005-2012*. [https://github.com/LandbruksdirektoratetGIT/opendata/tree/main/datasets/leveransedata-slakt-2005-2012](https://github.com/LandbruksdirektoratetGIT/opendata/tree/main/datasets/leveransedata-slakt-2005-2012)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
