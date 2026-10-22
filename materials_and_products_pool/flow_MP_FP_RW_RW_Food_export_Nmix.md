---
layout: default
title: Food Export
parent: Food and Feed Processing (MP.FP)
nav_order: 9
---

# Food Export

<iframe src="../output_files/plots/MP_FP_RW_RW_Food_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-RW.RW-Food export-Nmix** is exported food: cereals and plants, meat, fish, dairy products and eggs, and other food.

#### Data sources

- Export quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from the customs declarations for goods crossing the border ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)).

#### Assumptions

- Each commodity code is assigned a commodity type and an N content in the trade mapping sheet of N_parameters.xlsx, and quantities are multiplied by the N content.
- Klippfisk (salted and dried fish) and tørrfisk (dried fish) have their own N contents, 10.3% and 12.6%, from the protein content in the Norwegian food composition table ([Matvaretabellen](https://www.matvaretabellen.no/klippfisk-saltet-og-torket/): 64.3 and 78.5 g protein per 100 g; N = protein/6.25). Other fish products, including salted but not dried fish, use 2.8% N.

#### Interpretations and comparisons

- Fish and fish products (fresh, frozen and processed, including farmed salmon) make up about 97% of the flow, 73 of 75 kt N in 2024, of which klippfisk is 8.2 kt N and tørrfisk 0.4 kt N.
- The flow rises from 26 kt N in 1990 to 75–81 kt N from 2010 and has been roughly stable since, as the growth in farmed fish has been offset by lower wild catches (see HY.AC-MP.FP-Coastal fish and seafood-Nmix and HY.CW-MP.FP-Fish (wild catch)-Nmix).
- Exports of meat and of cheese are each below 0.5 kt N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: fish fresh frozen | N content of traded goods | ±20 %, normal | 84% | 91% | 0.72 | 0.86 | [Feed Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Feed_export_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| Traded quantities (SSB 08801) (kjøtt/fisk/meieri/egg) | Registered data | ±5 %, normal, drawn per year | 10% | 8% | 0.97 | 0.99 | [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| N content of traded goods: dried salted fish | N content of traded goods | ±20 %, normal | 5% | 1% | 0.17 | 0.11 | [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
