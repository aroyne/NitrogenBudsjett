---
layout: default
title: Aquaculture production
parent: Aquaculture (HY.AC)
nav_order: 3
---

# Aquaculture production

<iframe src="../output_files/plots/HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HY.AC-MP.FP-Coastal fish and seafood-Nmix** is the N in farmed fish taken out of the sea: sold fish, and fish that die in the pens or are discarded at slaughter, since these are taken out of the sea (mainly to ensilage) rather than released to coastal water.
- Escaped fish and other losses remain part of the losses to coastal water.

#### Data sources

- Sold farmed salmon and trout by year from Fiskeridirektoratet (2025)<!--cite:fiskeridirektoratet_06002_2025--> (table A.06.002, 1994 onward; historical compilation for 1984–1993).
- Losses of farmed fish by cause, as numbers of fish, from Fiskeridirektoratet (table A.05.021a), from 2007 onward.
- The N content of 2.8% (Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 254) matches the measured whole-body composition of Norwegian farmed salmon (17.5% protein, i.e. 2.8% N; Ytrestøyl et al. (2015)<!--cite:ytrestoyl_utilisation_2015-->, Fig. 3).

#### Assumptions

- Sold fish are multiplied by 2.8% N.
- Only dead fish and slaughterhouse discards are included. Numbers are converted to biomass with an average weight of 0.7 kg per lost fish (range 0.5–1.9 kg), the estimate used by Torrissen et al. (2016)<!--cite:torrisen_naeringsutslipp_2016--> (based on Iversen et al., 2015).
- Before 2007, lost-fish N is estimated from the 2007–2011 average ratio of lost-fish N to harvested N.

#### Interpretations

- The flow rises from about 1 kt N<!--val:HY.AC-MP.FP-Coastal fish and seafood-Nmix:1984--> in 1984 to 48 kt N<!--val:HY.AC-MP.FP-Coastal fish and seafood-Nmix:2024--> in 2024, following the growth of salmon and trout farming.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of fish and seafood | Parameter | ±10 %, normal | 74% | 77% | 1.00 | 1.00 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Wild fish catch](../hydrosphere_pool/flow_HY_CW_MP_FP_Fish_(wild_catch)_Nmix.html), [Shellfish](../hydrosphere_pool/flow_HY_CW_MP_FP_Shellfish_Nmix.html) and 3 more |
| Fisheries and aquaculture statistics (Directorate of Fisheries) (aquaculture) | Registered data | ±5 %, normal, drawn per year | 17% | 18% | 0.97 | 0.97 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Feed to Coastal Aquaculture](../materials_and_products_pool/flow_MP_FP_HY_AC_Feed_to_coastal_aquaculture_Nmix.html), [Aquaculture Feed Import](../rest_of_the_world_pool/flow_RW_RW_HY_AC_Aquaculture_feed_import_Nmix.html) |
| Average weight of dead and discarded farmed fish | Parameter | 0.5–1.9, triangular | 7% | 6% | 0.03 | 0.03 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html) |

### References

* Fiskeridirektoratet (2025). *A.06.002 Matfisk. Salg av laks, regnbueørret og ørret, etter art (Fylke) (1994-2024)*. [statistikkbanken.fiskeridir.no](https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__A%20Akvakultur__A.06%20Salg/A06002.px/)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
* Torrissen, O., Hansen, P. K., Aure, J., Husa, V., Andersen, S., Strohmeier, T., & Olsen, R. E. (2016). *Næringsutslipp fra havbruk - nasjonale og regionale perspektiv* (21-2016). Havforskningsinstituttet. [hi.no](https://www.hi.no/resources/publikasjoner/rapport-fra-havforskningen/2016/21-2016_neringsutslipp_fra_havbruk_ot.pdf)
* Ytrestøyl, T., Aas, T. S., & Åsgård, T. (2015). Utilisation of feed resources in production of Atlantic salmon (Salmo salar) in Norway. *Aquaculture, 448*, 365-374. [https://doi.org/10.1016/j.aquaculture.2015.06.023](https://doi.org/10.1016/j.aquaculture.2015.06.023)
