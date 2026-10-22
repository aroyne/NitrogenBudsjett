---
layout: default
title: Food Import
parent: Rest of the world (RW)
nav_order: 9
---

# Food Import

<iframe src="../output_files/plots/RW_RW_MP_FP_Food_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-MP.FP-Food import-Nmix** is the N in imported food commodities, including fish waste and by-products not fit for human consumption (HS 0511), which are processed in the food and feed industry.
- Soybeans and soybean meal (HS 1201 and 1208.10) are not included. Soybeans are imported mainly for feed and crushed in Norway (Eidem & Ruud, 2022)<!--cite:eidem_for-_2022-->. The soy meal used in feed for farm animals is counted in RW.RW-AG.MM-Animal feed import-Nmix, and the soy used in fish feed is part of RW.RW-HY.AC-Aquaculture feed import-Nmix, where all plant-based ingredients are counted as imported. Imported soybeans amount to 18–25 kt N/year.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.
- Vegetables are assigned N content by product form. Fresh, chilled, frozen and preserved vegetables, potatoes and tomatoes use the fresh-weight N contents in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, Table 21 (0.2–0.3 %). Dried peas and beans use the N content of pulses (3.6 %, Table 21), tomato paste 0.7 % (USDA FoodData Central), and other dried vegetables and potato flakes an estimated 1.6 %.

#### Interpretations and comparisons

- The flow rises from about 16 kt N in 1990 to 25–32 kt N per year since 2010.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: fish fresh frozen | N content of traded goods | ±20 %, normal | 31% | 43% | 0.25 | 0.30 | [Feed Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Feed_export_Nmix.html), [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html) |
| N content of traded goods: wheat | N content of traded goods | ±20 %, normal | 44% | 25% | 0.30 | 0.22 | [Feed Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Feed_export_Nmix.html), [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html) |
| N content of traded goods: organic | N content of traded goods | ±40 %, normal | 1% | 14% | 0.02 | 0.08 | [Feed Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Feed_export_Nmix.html), [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) and 1 more |
| Traded quantities (SSB 08801) (korn/planter) | Registered data | ±5 %, normal, drawn per year | 12% | 6% | 0.63 | 0.44 | [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html) |
| Traded quantities (SSB 08801) (kjøtt/fisk/meieri/egg) | Registered data | ±5 %, normal, drawn per year | 2% | 3% | 0.27 | 0.31 | [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html) |
| N content of traded goods: cereals | N content of traded goods | ±20 %, normal | 3% | <1% | 0.07 | 0.03 | [Feed Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Feed_export_Nmix.html), [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) and 1 more |
| N content of traded goods: barley | N content of traded goods | ±20 %, normal | 2% | – | 0.08 | – | [Feed Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Feed_export_Nmix.html) |

### References

* Eidem, B. & Ruud, T. (2022). *Fôr- og husdyrbaserte verdikjeder i norsk matproduksjon – nåsituasjon og begreper*.
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
