---
layout: default
title: Excretia
parent: Aquaculture (HY.AC)
nav_order: 1
---

# Excretia

<iframe src="../output_files/plots/HY_AC_HY_CW_Excretia_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HY.AC-HY.CW-Excretia-Nmix** is the N excreted by farmed fish to coastal water: the eaten feed N that is not retained in the fish.
- N in dead and discarded fish taken out of the sea is subtracted from excretion and counted in **HY.AC-MP.FP-Coastal fish and seafood-Nmix** instead.

#### Data sources

- Sold farmed salmon and trout by year from Fiskeridirektoratet (2025)<!--cite:fiskeridirektoratet_06002_2025--> (table A.06.002, 1994 onward; historical compilation for 1984–1993).

#### Assumptions

- Harvested fish are multiplied by 2.8% N (Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 254).
- Feed N is the harvested N divided by an apparent whole-system retention that rises linearly from 26% in 1990 (Ytrestøyl et al., 2015<!--cite:ytrestoyl_utilisation_2015-->) to 35.75% in 2010 (Aas et al., 2022<!--cite:aas_utilization_2022-->) and is constant after. The rise is attributed to less feed waste, so the biological retention of eaten feed is held constant and the feed waste falls from about 29% of the feed in 1990 to the measured 3% (Wang et al., 2013<!--cite:wang_chemical_2013-->) in 2010; see the [methodological note](subpool_aquaculture.html) on the Aquaculture (HY.AC) subpool page.
- Found through mass balance by assuming N that does not become fish or waste feed is excreted, using the same aquafeed budget as the other aquafeed flows (see the [methodological note](subpool_aquaculture.html) for details and sources).

#### Interpretations and comparisons

- The flow rises from about 1.5 kt N in 1984 to 77 kt N in 2024, following production, and is the largest N input to Norwegian coastal waters from a single source after the inflow from land.
- Our combined losses from aquaculture to coastal waters (excretion plus waste feed) are 6–18% higher than TEOTIL3 (Sample et al., 2024)<!--cite:sample_teotil3_2024--> for 2013–2023, and considerably higher than Miljødirektoratet's earlier estimates before 2005.
- The total feed N in our budget agrees with reported feed sales (Sjømat Norge, via Fiskeridirektoratet's key figures) to within 2% for 2019–2023, so the difference lies in how much of the feed N is assumed retained in the fish. We use the whole-system apparent retention of 35.75% from Aas et al. (2022)<!--cite:aas_utilization_2022-->, which counts all losses of feed ingredients, feed and fish as unretained, and a lower retention further back in time (Ytrestøyl et al., 2015)<!--cite:ytrestoyl_utilisation_2015-->. TEOTIL3 instead calculates losses as N in reported feed (5.84% N) minus N in the biomass growth of the farmed fish (2.96% N), including fish that are later lost, which implies a retention of about 44%, close to the 45% protein retention for 2012 reported by Torrissen et al. (2016)<!--cite:torrisen_naeringsutslipp_2016-->.
- Our estimate should therefore be seen as an upper bound for the losses to coastal water.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N retention in farmed salmon, from 2010 | Parameter | 0.33–0.39, normal | 52% | 52% | −1.47 | −1.46 | [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Feed to Coastal Aquaculture](../materials_and_products_pool/flow_MP_FP_HY_AC_Feed_to_coastal_aquaculture_Nmix.html), [Aquaculture Feed Import](../rest_of_the_world_pool/flow_RW_RW_HY_AC_Aquaculture_feed_import_Nmix.html) |
| N content of fish and seafood | Parameter | ±10 %, normal | 36% | 36% | 1.00 | 1.00 | [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture production](../hydrosphere_pool/flow_HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html), [Wild fish catch](../hydrosphere_pool/flow_HY_CW_MP_FP_Fish_(wild_catch)_Nmix.html), [Shellfish](../hydrosphere_pool/flow_HY_CW_MP_FP_Shellfish_Nmix.html) and 2 more |
| Fisheries and aquaculture statistics (Directorate of Fisheries) (aquaculture) | Registered data | ±5 %, normal, drawn per year | 9% | 9% | 1.02 | 1.02 | [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture production](../hydrosphere_pool/flow_HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html), [Feed to Coastal Aquaculture](../materials_and_products_pool/flow_MP_FP_HY_AC_Feed_to_coastal_aquaculture_Nmix.html), [Aquaculture Feed Import](../rest_of_the_world_pool/flow_RW_RW_HY_AC_Aquaculture_feed_import_Nmix.html) |

### References

* Aas, T. S., Åsgård, T., & Ytrestøyl, T. (2022). Utilization of feed resources in the production of Atlantic salmon (Salmo salar) in Norway: An update for 2020. *Aquaculture Reports, 26*, 101316. [https://doi.org/10.1016/j.aqrep.2022.101316](https://doi.org/10.1016/j.aqrep.2022.101316)
* Fiskeridirektoratet (2025). *A.06.002 Matfisk. Salg av laks, regnbueørret og ørret, etter art (Fylke) (1994-2024)*. [https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__A%20Akvakultur__A.06%20Salg/A06002.px/](https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__A%20Akvakultur__A.06%20Salg/A06002.px/)
* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
* Torrissen, O., Hansen, P. K., Aure, J., Husa, V., Andersen, S., Strohmeier, T., & Olsen, R. E. (2016). *Næringsutslipp fra havbruk - nasjonale og regionale perspektiv*. [https://www.hi.no/resources/publikasjoner/rapport-fra-havforskningen/2016/21-2016_neringsutslipp_fra_havbruk_ot.pdf](https://www.hi.no/resources/publikasjoner/rapport-fra-havforskningen/2016/21-2016_neringsutslipp_fra_havbruk_ot.pdf)
* Wang, X., Andresen, K., Handå, A., Jensen, B., Reitan, K., & Olsen, Y. (2013). Chemical composition and release rate of waste discharge from an Atlantic salmon farm with an evaluation of IMTA feasibility. *Aquaculture Environment Interactions, 4*(2), 147-162. [https://doi.org/10.3354/aei00079](https://doi.org/10.3354/aei00079)
* Ytrestøyl, T., Aas, T. S., & Åsgård, T. (2015). Utilisation of feed resources in production of Atlantic salmon (Salmo salar) in Norway. *Aquaculture, 448*, 365-374. [https://doi.org/10.1016/j.aquaculture.2015.06.023](https://doi.org/10.1016/j.aquaculture.2015.06.023)
