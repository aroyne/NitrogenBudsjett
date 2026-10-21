---
layout: default
title: Feed to Coastal Aquaculture
parent: Food and Feed Processing (MP.FP)
nav_order: 4
---

# Feed to Coastal Aquaculture

<iframe src="../output_files/plots/MP_FP_HY_AC_Feed_to_coastal_aquaculture_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-HY.AC-Feed to coastal aquaculture-Nmix** is the domestically supplied share of the feed used in coastal aquaculture – about 89% in the mid-1980s, falling to 8% by 2020 as the import fraction rises; the remaining, imported share is accounted for in RW.RW-HY.AC-Aquaculture feed import-Nmix.

#### Data sources

- The harvested amount of farmed salmon, rainbow trout and trout from Fiskeridirektoratet's sales statistics (table A.06.002; Fiskeridirektoratet, 2025<!--cite:fiskeridirektoratet_06002_2025-->), which are compiled from the sales reported by the fish farms.

#### Assumptions

- The amount of feed per tonne of produced fish is found by assuming a whole-fish protein (N) retention rising from 26% in 1990 to a 35.75% plateau from 2010 onward (see the [methodological note](../hydrosphere_pool/subpool_aquaculture.html) on the Aquaculture (HY.AC) subpool page for details and sources). Feed N is thus calculated from production, not from reported feed sales.
- The domestically supplied part is total feed N × (1 − import fraction), where the import fraction is built from the marine share of the feed and the share of the marine ingredients that is imported (see the methodological note).

#### Interpretations and comparisons

- The domestically supplied feed stays at about 9–13 kt N per year, while total feed N (this flow plus RW.RW-HY.AC-Aquaculture feed import-Nmix) rises from about 14 kt N in 1990 to about 128 kt N in 2024.
- The domestic share therefore falls from about 70% in 1990 to 8% in 2024: the growth of the industry has been met with imported marine and plant ingredients.
- Hohmann-Marriott (2025)<!--cite:hohmann-marriott_nitrogen_2025--> found the nitrogen content in aquaculture feed in 2020 to be 124 kt N, which is very similar to our results.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Imported share of fish feed | Parameter | 0.89–0.95, normal | 16% | 88% | −2.81 | −11.50 | [Aquaculture Feed Import](../rest_of_the_world_pool/flow_RW_RW_HY_AC_Aquaculture_feed_import_Nmix.html) |
| N content of fish and seafood | Parameter | ±10 %, normal | 19% | 7% | 1.00 | 1.00 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture production](../hydrosphere_pool/flow_HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html), [Wild fish catch](../hydrosphere_pool/flow_HY_CW_MP_FP_Fish_(wild_catch)_Nmix.html) and 2 more |
| N retention in farmed salmon, from 2010 | Parameter | 0.33–0.39, normal | <1% | 4% | −0.16 | −0.91 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture Feed Import](../rest_of_the_world_pool/flow_RW_RW_HY_AC_Aquaculture_feed_import_Nmix.html) |
| Fisheries and aquaculture statistics (Directorate of Fisheries) (aquaculture) | Registered data | ±5 %, normal, drawn per year | 5% | 2% | 1.00 | 1.00 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture production](../hydrosphere_pool/flow_HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html), [Aquaculture Feed Import](../rest_of_the_world_pool/flow_RW_RW_HY_AC_Aquaculture_feed_import_Nmix.html) |
| N retention in farmed salmon, 1990 | Parameter | ±20 %, normal | 48% | – | −0.80 | – | [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture Feed Import](../rest_of_the_world_pool/flow_RW_RW_HY_AC_Aquaculture_feed_import_Nmix.html) |
| Marine share of fish feed, 1990 | Parameter | ±10 % (min–max), triangular | 11% | – | 0.98 | – | [Aquaculture Feed Import](../rest_of_the_world_pool/flow_RW_RW_HY_AC_Aquaculture_feed_import_Nmix.html) |

### References

* Fiskeridirektoratet (2025). *A.06.002 Matfisk. Salg av laks, regnbueørret og ørret, etter art (Fylke) (1994-2024)*. [https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__A%20Akvakultur__A.06%20Salg/A06002.px/](https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__A%20Akvakultur__A.06%20Salg/A06002.px/)
* Hohmann-Marriott, M. F. (2025). A Nitrogen budget for Norway analysis of Nitrogen flows from societal and natural sources (1961–2020). *PLOS ONE, 20*(2), e0313598. [https://doi.org/10.1371/journal.pone.0313598](https://doi.org/10.1371/journal.pone.0313598)
