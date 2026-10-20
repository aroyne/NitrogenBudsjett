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
- Only individual products are used, not FAOSTAT's aggregates.

#### Interpretations and comparisons

- The flow rises from about 17 kt N in 1990 to 19 kt N in 2024.
- Milk is the largest product but decreases from 10.6 to 7.9 kt N, while chicken meat increases from 0.6 to 3.3 kt N, pork from 2.1 to 3.3 kt N and eggs from 1.0 to 1.4 kt N.
- Beef is stable at about 2.1 kt N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| FAOSTAT crops and livestock products (production) | Registered data | ±10 %, normal, drawn per year | 73% | 81% | [Non-edible Animal Products](../agriculture_pool/flow_AG_MM_MP_OP_Non_edible_animal_products_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of animal product: Milk, Total | Parameter | ±10 % | 24% | 13% | none |
| N content of animal product: Meat of pig with the bone, fresh or chilled | Parameter | ±10 % | 1% | 2% | none |
| N content of animal product: Meat of chickens, fresh or chilled | Parameter | ±10 % | <1% | 2% | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
