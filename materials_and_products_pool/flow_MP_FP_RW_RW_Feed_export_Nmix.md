---
layout: default
title: Feed Export
parent: Food and Feed Processing (MP.FP)
nav_order: 8
---

# Feed Export

<iframe src="../output_files/plots/MP_FP_RW_RW_Feed_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-RW.RW-Feed export-Nmix** is exported feed, fish feed and pet food, and fish waste and by-products not fit for human consumption (HS 0511), whether or not they are declared for feed.

#### Data sources

- Export quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from the customs declarations for goods crossing the border ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)).

#### Assumptions

- Each commodity code is assigned a commodity type and an N content in the trade mapping sheet of N_parameters.xlsx, and quantities are multiplied by the N content.

#### Interpretations and comparisons

- The flow rises from about 7 kt N in 1990 to about 20 kt N in 2024.
- In 2024 it consists mainly of oilseed cake and meal (about 7 kt N), pet food (about 6 kt N, up from 0.2 kt N in 1990) and fish products and by-products (about 6 kt N).
- The peak in 2002–2005 (15–17 kt N) comes from exports of fish waste and by-products not for feed, which reached about 8 kt N in 2003.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: pet food | N content of traded goods | ±40 %, normal | 2% | 61% | 0.05 | 0.31 | none |
| N content of traded goods: oilcrops | N content of traded goods | ±20 %, normal | 56% | 22% | 0.52 | 0.37 | [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| N content of traded goods: fish fresh frozen | N content of traded goods | ±20 %, normal | 18% | 7% | 0.29 | 0.20 | [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| N content of traded goods: organic | N content of traded goods | ±40 %, normal | 17% | 5% | 0.14 | 0.08 | [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) and 1 more |
| Traded quantities (SSB 08801) (for) | Registered data | ±5 %, normal, drawn per year | 5% | 5% | 0.67 | 0.66 | none |
