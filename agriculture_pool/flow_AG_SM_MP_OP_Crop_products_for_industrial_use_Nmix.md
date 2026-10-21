---
layout: default
title: Crop products for industrial use
parent: Soil Management (AG.SM)
nav_order: 8
---

# Crop products for industrial use

<iframe src="../output_files/plots/AG_SM_MP_OP_Crop_products_for_industrial_use_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.SM-MP.OP-Crop products for industrial use-Nmix** is the N in harvested industrial crops (in Norway mainly oilseeds).

#### Data sources

- Eurostat's Gross Nutrient Balance ([aei_pr_gnb](https://ec.europa.eu/eurostat/databrowser/view/aei_pr_gnb/default/table)), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, calculates nutrient removal by harvest as crop production multiplied by an N content per crop, based on Norwegian crop statistics.
- The flow is "Nutrient removal by harvest of industrial crops".

#### Assumptions

- For years with missing data, we have filled in the average of all other years.
- Eurostat GNB has not yet published a 2024 figure at the time of writing; the 2024 value is a 3-year average of 2021–2023 (this flow is small and volatile with no clear trend).

#### Interpretations and comparisons

- The flow is small, 0.3–0.8 kt N per year, with large variation from year to year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Eurostat gross nutrient balance | Modelled statistics | ±40 %, normal | 100% | 98% | 1.00 | 1.00 | [Food crop products](../agriculture_pool/flow_AG_SM_MP_FP_Food_crop_products_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Held constant or averaged (industrial crops:2021-2023) | Gap filling: held constant or averaged | ±15–15 %, lognormal, grows with distance to known year | – | 2% | – | 1.00 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
