---
layout: default
title: Wild fish catch
parent: Coastal Water (HY.CW)
nav_order: 1
---

# Wild fish catch

<iframe src="../output_files/plots/HY_CW_MP_FP_Fish_(wild_catch)_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HY.CW-MP.FP-Fish (wild catch)-Nmix** is the N in wild fish catch. The flow sums all "true fish" catch categories (pelagic, cod-family, other bottom/deep-water fish, skates and sharks) and explicitly excludes shellfish and seaweed, which are reported in HY.CW-MP.FP-Shellfish-Nmix.

#### Data sources

- Landed catch (live weight) from Fiskeridirektoratet's catch statistics by species (Fiskeridirektoratet, 2025<!--cite:fiskeridirektoratet_fangst_2025-->), 2000 onward.
- For 1990–1999, a historical compilation of pelagic and bottom fish catch from the same source.

#### Assumptions

- N content in fish 2.8% (range ±10%), according to Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 254, and UNECE Guidance, Annex 6 Table 12.

#### Interpretations and comparisons

- The flow rises from about 43 kt N in 1990 to about 70 kt N around 2000 and falls to 50 kt N in 2024, following the catch of pelagic fish such as herring, mackerel and blue whiting, which varies with stock sizes and quotas.
- Hohmann-Marriott (2025)<!--cite:hohmann-marriott_nitrogen_2025--> found 107 kt N from fisheries in 2018, mainly fish, against about 70 kt N here (63 kt N wild fish and 7 kt N shellfish). Their values for crustaceans (8 kt N) and aquaculture (38 kt N in 2018 and 41 kt N in 2020) are close to ours (HY.CW-MP.FP-Shellfish-Nmix and HY.AC-MP.FP-Coastal fish and seafood-Nmix).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of fish and seafood | Parameter | ±10 %, normal | 80% | 80% | 1.00 | 1.00 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture production](../hydrosphere_pool/flow_HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html), [Shellfish](../hydrosphere_pool/flow_HY_CW_MP_FP_Shellfish_Nmix.html) and 2 more |
| Fisheries and aquaculture statistics (Directorate of Fisheries) (landings) | Registered data | ±5 %, normal, drawn per year | 20% | 20% | 1.00 | 1.00 | [Shellfish](../hydrosphere_pool/flow_HY_CW_MP_FP_Shellfish_Nmix.html) |

### References

* Fiskeridirektoratet (2025). *Fangst fordelt på art (offisiell statistikk)*. [https://www.fiskeridir.no/statistikk-tall-og-analyse/data-og-statistikk-om-yrkesfiske/fangst/fangst-fordelt-pa-art-offisiell-statistikk](https://www.fiskeridir.no/statistikk-tall-og-analyse/data-og-statistikk-om-yrkesfiske/fangst/fangst-fordelt-pa-art-offisiell-statistikk)
* Hohmann-Marriott, M. F. (2025). A Nitrogen budget for Norway analysis of Nitrogen flows from societal and natural sources (1961–2020). *PLOS ONE, 20*(2), e0313598. [https://doi.org/10.1371/journal.pone.0313598](https://doi.org/10.1371/journal.pone.0313598)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
