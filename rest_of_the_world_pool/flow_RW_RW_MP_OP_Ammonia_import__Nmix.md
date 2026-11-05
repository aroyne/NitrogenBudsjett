---
layout: default
title: Ammonia Import
parent: Rest of the world (RW)
nav_order: 10
---

# Ammonia Import

<iframe src="../output_files/plots/RW_RW_MP_OP_Ammonia_import__Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-MP.OP-Ammonia import-Nmix** is imported ammonia (HS 2814), anhydrous and in aqueous solution.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- Ammonia (HS 2814.10) has 82.35% N (stoichiometry). Ammonia in aqueous solution (HS 2814.20) is given 20% N (commercial ammonia solution is about 24–25% NH<sub>3</sub>; range 8–29% N).

#### Interpretations

- The flow is about 170–490 kt N per year, one of the largest N flows in the model; the ammonia is used in fertilizer production at Herøya and most of the N leaves Norway again as exported mineral fertilizer.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-04). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Traded quantities (SSB 08801) (NH<sub>3</sub>) | Registered data | ±5 %, normal, drawn per year | 100% | 100% | 1.00 | 1.00 | [Ammonia Synthesis N<sub>2</sub> Fixation](../atmosphere_pool/flow_AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
