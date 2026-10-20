---
layout: default
title: Food crop products
parent: Soil Management (AG.SM)
nav_order: 7
---

# Food crop products

<iframe src="../output_files/plots/AG_SM_MP_FP_Food_crop_products_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.SM-MP.FP-Food crop products-Nmix** is the N in harvested crops other than fodder and industrial crops. «Ornamental crops», which should also be removed, are negligible in Norway.

#### Data sources

- Eurostat's Gross Nutrient Balance ([aei_pr_gnb](https://ec.europa.eu/eurostat/databrowser/view/aei_pr_gnb/default/table)), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, calculates nutrient removal by harvest as crop production multiplied by an N content per crop, based on Norwegian crop statistics.
- Eurostat GNB has no values for 2017–2019 and has not yet published 2024.
- SSB's cereal harvest ([table 07479](https://www.ssb.no/statbank/table/07479)) for these years, since cereals carry most of the N.

#### Assumptions

- The flow is "Nutrient removal by harvest of crops" minus "industrial crops"; fodder crops and grazing are reported separately in the balance and are not included.
- For 2017–2019 and 2024 the cereal N is the cereal harvest times the N per tonne of cereal harvest in the balance (interpolated between 2016 and 2020, or the 2023 value for 2024), and the other crops are interpolated between 2016 and 2020 or held at the 2023 value.

#### Interpretations and comparisons

- The flow is 16–32 kt N per year and follows the size of the cereal harvest, since cereals make up about 88% of the N.
- Most of the cereal is used for animal feed and returns to AG.MM via MP.FP-AG.MM-Farm animal feed-Nmix.
- The low values in 2018 (16 kt N) and 2023 (19 kt N) are the drought years with poor cereal harvests, and the high value in 1990 (32 kt N) a good harvest.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| Eurostat gross nutrient balance | Modelled statistics | ±40 %, normal | 100% | 97% | [Crop products for industrial use](../agriculture_pool/flow_AG_SM_MP_OP_Crop_products_for_industrial_use_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Held constant or averaged (2023+) | Gap filling: held constant or averaged | ±15–15 %, lognormal, grows with distance to known year | – | 2% | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
