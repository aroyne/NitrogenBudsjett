---
layout: default
title: Animal Products
parent: Manure Management (AG.MM)
nav_order: 6
---

# Animal Products

<iframe src="../output_files/plots/AG_MM_MP_FP_Animal_products_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.MM-MP.FP-Animal products-Nmix** is the N in meat, milk and eggs produced in Norway.

#### Data sources

- FAOSTAT's production statistics ([Crops and livestock products](https://www.fao.org/faostat/en/#data/QCL)) give the production of meat (carcass weight), milk and eggs in Norway, based on the official statistics Norway reports to FAO.
- N contents from Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- Each product is multiplied by its N content (for example 2.5% for beef, 2.56% for pork, 3.0% for chicken, 2.6% for mutton).

#### Interpretations

- The flow rises from about 17 kt N<!--val:AG.MM-MP.FP-Animal products-Nmix:1990--> in 1990 to 19 kt N<!--val:AG.MM-MP.FP-Animal products-Nmix:2024--> in 2024.
- Milk is the largest product but decreases from 10.6 to 7.9 kt N, while chicken meat increases from 0.6 to 3.3 kt N, pork from 2.1 to 3.3 kt N and eggs from 1.0 to 1.4 kt N.
- Beef is stable at about 2.1 kt N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| FAOSTAT crops and livestock products (production) | Registered data | ±10 %, normal, drawn per year | 73% | 81% | 1.00 | 1.00 | [Non-edible Animal Products](../agriculture_pool/flow_AG_MM_MP_OP_Non_edible_animal_products_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of animal product: Milk, Total | Parameter | ±10 % | 24% | 13% | 0.59 | 0.41 | none |
| N content of animal product: Meat of pig with the bone, fresh or chilled | Parameter | ±10 % | 1% | 2% | 0.13 | 0.17 | none |
| N content of animal product: Meat of chickens, fresh or chilled | Parameter | ±10 % | <1% | 2% | 0.04 | 0.16 | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
