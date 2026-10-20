---
layout: default
title: Other Goods Import
parent: Rest of the world (RW)
nav_order: 11
---

# Other Goods Import

<iframe src="../output_files/plots/RW_RW_MP_OP_Other_goods_import__Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-MP.OP-Other goods import-Nmix** is the N in imported chemicals, plastics, rubber, leather, textiles, wood, furniture, toys and other goods.
- Import of N2 is a large contributor but not included here because it does not contribute to the reactive nitrogen cycle.
- Plastic waste is counted in RW.RW-PR.SO-Solid waste import-Nmix, and fish waste and by-products (HS 0511) in RW.RW-MP.FP-Food import-Nmix.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.
- Within the plastics and synthetic-textile trade categories, N content is assigned by base polymer rather than a single blended factor: nitrogen-containing polymers (polyamide/nylon, polyurethane, melamine and urea formaldehyde resins, polyacrylonitrile) use the N contents given in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, Table 23, while ordinary commodity plastics and fibres with no nitrogen in their polymer backbone (polyethylene, polypropylene, PVC, polystyrene, polyester, viscose/rayon, cotton) are assigned ~0.
- The same principle applies to clothing, footwear and other finished textile articles: items explicitly of wool use the protein-fibre N content from Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, Table 24 (as for silk), items with a leather component use the same N content as hides and skins, and items of cotton or unspecified synthetic/artificial fibre (predominantly polyester, which – like cotton – has no nitrogen in its polymer backbone) default to ~0.
- Roundwood, fuel wood, chips, sawdust and wood residues (HS 4401 and 4403) are given the N content of stem wood (1.2 g/kg for conifers and 1.4 g/kg for broadleaves, Table 45 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->), the same as domestic industrial round wood, while processed wood products use 0.2% (Table 22).
- Live plants, cut flowers and Christmas trees are given an assumed 0.3 % N, as for fresh vegetables.

#### Interpretations and comparisons

- The flow is about 21–31 kt N per year since 1995, with peaks of 42–46 kt N in 2014, 2015 and 2017 that come from imports of nitric acid (1.6–20.5 kt N per year), a raw material for the fertilizer industry.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: resin | N content of traded goods | ±20 %, normal | 8% | 20% | 0.09 | 0.15 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
| N content of traded goods: wood products | N content of traded goods | ±20 %, normal | 14% | 16% | 0.12 | 0.14 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| N content of traded goods: explosives | N content of traded goods | ±40 %, normal | <1% | 14% | 0.00 | 0.06 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of traded goods: detergent | N content of traded goods | ±20 %, normal | 7% | 14% | 0.09 | 0.12 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
| Traded quantities (SSB 08801) (kjemikalier) | Registered data | ±5 %, normal, drawn per year | 12% | 10% | 0.41 | 0.41 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
| N content of traded goods: roundwood conifer | N content of traded goods | 0.0007–0.0017, triangular | 18% | 5% | 0.06 | 0.04 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
| N content of traded goods: polyamide | N content of traded goods | ±20 %, normal | 8% | 4% | 0.09 | 0.07 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
| N content of traded goods: dicyanamid | N content of traded goods | ±20 %, normal | <1% | 4% | 0.00 | 0.07 | none |
| N content of traded goods: rubber | N content of traded goods | ±20 %, normal | 2% | 3% | 0.04 | 0.06 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Export for Recycling](../processing_of_residues_pool/flow_PR_SO_RW_RW_Export_for_recycling_Nmix.html) and 1 more |
| N content of traded goods: silk wool | N content of traded goods | ±20 %, normal | 3% | 2% | 0.05 | 0.05 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
| N content of traded goods: hides skins | N content of traded goods | ±20 %, normal | 4% | 2% | 0.06 | 0.04 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
| Traded quantities (SSB 08801) (tre) | Registered data | ±5 %, normal, drawn per year | 3% | 2% | 0.21 | 0.18 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
| N content of traded goods: roundwood nonconifer | N content of traded goods | 0.0009–0.0019, normal | 3% | <1% | 0.03 | 0.01 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html) |
| N content of traded goods: urea formaldehyde | N content of traded goods | ±15 %, normal | 13% | <1% | 0.15 | 0.00 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
