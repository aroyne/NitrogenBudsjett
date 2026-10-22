---
layout: default
title: Other Goods Export
parent: Other Producing Industry (MP.OP)
nav_order: 13
---

# Other Goods Export

<iframe src="../output_files/plots/MP_OP_RW_RW_Other_goods_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-RW.RW-Other goods export-Nmix** is exported goods that can be characterized as flowers, chemicals, soap, industrial protein, leather, wood, textiles, and ammonia.
- Fish waste and by-products (HS 0511) are counted in MP.FP-RW.RW-Feed export-Nmix.

#### Data sources

- Export quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from the customs declarations for goods crossing the border ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)).

#### Assumptions

- Each commodity code is assigned a commodity type and an N content in the trade mapping sheet of N_parameters.xlsx, and quantities are multiplied by the N content.
- Within the plastics and synthetic-textile trade categories, N content is assigned by base polymer rather than a single blended factor: nitrogen-containing polymers (polyamide/nylon, polyurethane, melamine and urea formaldehyde resins, polyacrylonitrile) use the N contents given in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, Table 23, while ordinary commodity plastics and fibres with no nitrogen in their polymer backbone (polyethylene, polypropylene, PVC, polystyrene, polyester, viscose/rayon, cotton) are assigned ~0.
- The same principle applies to clothing, footwear and other finished textile articles: items explicitly of wool use the protein-fibre N content from Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, Table 24 (as for silk), items with a leather component use the same N content as hides and skins, and items of cotton or unspecified synthetic/artificial fibre (predominantly polyester, which – like cotton – has no nitrogen in its polymer backbone) default to ~0.
- Roundwood, fuel wood, chips, sawdust and wood residues (HS 4401 and 4403) are given the N content of stem wood (1.2 g/kg for conifers and 1.4 g/kg for broadleaves, Table 45 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->), the same as domestic industrial round wood, while processed wood products use 0.2% (Table 22).

#### Interpretations and comparisons

- The flow is about 7–10 kt N per year until 2013, 11–12 kt N in 2014–2017 and 20–33 kt N from 2018.
- The significant increase from 2018 is due to export of nitric acid, which started that year. Nitric acid is an intermediary in fertilizer production but not counted as fertilizer, so it shows up in this flow.
- The rise from 2013 comes from roundwood exports, which grew from about 0.5 to 3–4 million tonnes per year after several Norwegian pulp and paper mills closed.
- In 2024 roundwood, chips and wood residues (6.4 kt N) and nitric acid (7.7 kt N) are the largest items, followed by processed wood products (2.7 kt N), hides and leather (1.0 kt N), wool (0.8 kt N) and detergents (0.75 kt N).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: wood products | N content of traded goods | 0.001–0.0049, triangular | 97% | 54% | 0.49 | 0.11 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html), [Other Goods Import](../rest_of_the_world_pool/flow_RW_RW_MP_OP_Other_goods_import__Nmix.html) |
| N content of traded goods: roundwood conifer | N content of traded goods | 0.0007–0.0017, triangular | 1% | 35% | 0.08 | 0.21 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Import](../rest_of_the_world_pool/flow_RW_RW_MP_OP_Other_goods_import__Nmix.html) |
| Traded quantities (SSB 08801) (kjemikalier) | Registered data | ±5 %, normal, drawn per year | <1% | 3% | 0.07 | 0.52 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Goods Import](../rest_of_the_world_pool/flow_RW_RW_MP_OP_Other_goods_import__Nmix.html) |
| N content of traded goods: nitric acid | N content of traded goods | ±5 %, normal | – | 3% | – | 0.51 | [Other Goods Import](../rest_of_the_world_pool/flow_RW_RW_MP_OP_Other_goods_import__Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
