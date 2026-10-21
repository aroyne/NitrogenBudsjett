---
layout: default
title: Aquaculture Feed Import
parent: Rest of the world (RW)
nav_order: 8
---

# Aquaculture Feed Import

<iframe src="../output_files/plots/RW_RW_HY_AC_Aquaculture_feed_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-HY.AC-Aquaculture feed import-Nmix** is the imported part of the feed N used in coastal aquaculture.

#### Data sources

- Sold farmed fish from Fiskeridirektoratet (2025)<!--cite:fiskeridirektoratet_06002_2025-->, with 2.8% nitrogen content in fish and shellfish (Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 254).
- The composition of Norwegian salmon feed (share of marine ingredients 89% in 1990 and 22% in 2020) and the import share of 92% in 2020 from Aas et al. (2022)<!--cite:aas_utilization_2022-->.

#### Assumptions

- Total feed N for aquaculture is the harvested fish N divided by the apparent whole-system retention, with a feed-waste fraction estimated to fall from ~29% in 1990 to the measured 3% (Wang et al., 2013)<!--cite:wang_chemical_2013--> by 2010; see the [methodological note](../hydrosphere_pool/subpool_aquaculture.html) on the Aquaculture (HY.AC) subpool page for how this is derived from the apparent whole-fish retention trend.
- The imported share combines the share of marine ingredients, the imported part of the marine ingredients (rising from almost none before 1985), and plant-based ingredients counted as fully imported. It rises from about 11% in the mid-1980s to 92% in 2020 (see the [methodological note](../hydrosphere_pool/subpool_aquaculture.html)).

#### Interpretations and comparisons

- The flow rises from 0.4 kt N in 1985 to about 119 kt N in 2024, following the growth of aquaculture and the shift from domestic fish meal to imported plant-based ingredients.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of fish and seafood | Parameter | ±10 %, normal | 15% | 52% | 1.00 | 1.00 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture production](../hydrosphere_pool/flow_HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html), [Wild fish catch](../hydrosphere_pool/flow_HY_CW_MP_FP_Fish_(wild_catch)_Nmix.html) and 2 more |
| N retention in farmed salmon, from 2010 | Parameter | 0.33–0.39, normal | <1% | 29% | −0.16 | −0.91 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Feed to Coastal Aquaculture](../materials_and_products_pool/flow_MP_FP_HY_AC_Feed_to_coastal_aquaculture_Nmix.html) |
| Fisheries and aquaculture statistics (Directorate of Fisheries) (aquaculture) | Registered data | ±5 %, normal, drawn per year | 4% | 13% | 1.00 | 1.00 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture production](../hydrosphere_pool/flow_HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html), [Feed to Coastal Aquaculture](../materials_and_products_pool/flow_MP_FP_HY_AC_Feed_to_coastal_aquaculture_Nmix.html) |
| Imported share of fish feed | Parameter | 0.89–0.95, normal | 24% | 5% | 4.02 | 1.00 | [Feed to Coastal Aquaculture](../materials_and_products_pool/flow_MP_FP_HY_AC_Feed_to_coastal_aquaculture_Nmix.html) |
| N retention in farmed salmon, 1990 | Parameter | ±20 %, normal | 36% | – | −0.80 | – | [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Feed to Coastal Aquaculture](../materials_and_products_pool/flow_MP_FP_HY_AC_Feed_to_coastal_aquaculture_Nmix.html) |
| Marine share of fish feed, 1990 | Parameter | ±10 % (min–max), triangular | 21% | – | −1.54 | – | [Feed to Coastal Aquaculture](../materials_and_products_pool/flow_MP_FP_HY_AC_Feed_to_coastal_aquaculture_Nmix.html) |

### References

* Aas, T. S., Åsgård, T., & Ytrestøyl, T. (2022). Utilization of feed resources in the production of Atlantic salmon (Salmo salar) in Norway: An update for 2020. *Aquaculture Reports, 26*, 101316. [https://doi.org/10.1016/j.aqrep.2022.101316](https://doi.org/10.1016/j.aqrep.2022.101316)
* Fiskeridirektoratet (2025). *A.06.002 Matfisk. Salg av laks, regnbueørret og ørret, etter art (Fylke) (1994-2024)*. [https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__A%20Akvakultur__A.06%20Salg/A06002.px/](https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__A%20Akvakultur__A.06%20Salg/A06002.px/)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
* Wang, X., Andresen, K., Handå, A., Jensen, B., Reitan, K., & Olsen, Y. (2013). Chemical composition and release rate of waste discharge from an Atlantic salmon farm with an evaluation of IMTA feasibility. *Aquaculture Environment Interactions, 4*(2), 147-162. [https://doi.org/10.3354/aei00079](https://doi.org/10.3354/aei00079)
