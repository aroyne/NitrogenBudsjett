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
- The catch statistics cover all catch by Norwegian vessels, landed in Norway or abroad, and not catch landed in Norway by foreign vessels (the total equals Norwegian vessels in Fiskeridirektoratet's table F.06.001, [statistics bank](https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__F_Fiskeri__F_06_Fangst/)).

#### Assumptions

- N content in fish 2.8% (range ±10%), according to Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 254, and UNECE Guidance, Annex 6 Table 12.

#### Interpretations

- Of the fish (excluding krill), 125–430 kt live weight per year (3.5–12 kt N) is landed directly abroad, mainly blue whiting, herring and capelin landed in Denmark, Iceland, Ireland, the UK and the Faroe Islands (Fiskeridirektoratet table F.06.002). This fish never enters Norway, but is counted here as an input to MP.FP. SSB includes such direct landings in the export statistics, and thus in MP.FP-RW.RW-Food export-Nmix, from July 2010 ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)). For 2010–2023 the exports to these countries match the landings (for example Ireland 2012: 68.4 kt landed, 68.6 kt exported; Iceland 2018: 96.1 and 95.9 kt). Before 2010 they are missing from the exports (Ireland 2008: 34.5 kt landed, 1.7 kt exported), and from 2024, when the data source changed from Fiskeridirektoratet to customs declarations, they are recorded as industrial fish not fit for human consumption (HS 0511.9111) rather than as fresh or frozen fish (Iceland 2024: 65.2 kt landed, 24.7 kt fresh or frozen and 40.5 kt industrial fish exported). For the years before 2010 the landings abroad that are not in the exports are added to MP.FP-RW.RW-Food export-Nmix, so that they do not stay in MP.FP.
- The flow rises from about 43 kt N in 1990 to about 70 kt N around 2000 and falls to 50 kt N in 2024, following the catch of pelagic fish such as herring, mackerel and blue whiting, which varies with stock sizes and quotas.
- Hohmann-Marriott (2025)<!--cite:hohmann-marriott_nitrogen_2025--> found 107 kt N from fisheries in 2018, mainly fish, against about 70 kt N here (63 kt N wild fish and 7 kt N shellfish). Their values for crustaceans (8 kt N) and aquaculture (38 kt N in 2018 and 41 kt N in 2020) are close to ours (HY.CW-MP.FP-Shellfish-Nmix and HY.AC-MP.FP-Coastal fish and seafood-Nmix).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-04). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of fish and seafood | Parameter | ±10 %, normal | 80% | 80% | 1.00 | 1.00 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture production](../hydrosphere_pool/flow_HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html), [Shellfish](../hydrosphere_pool/flow_HY_CW_MP_FP_Shellfish_Nmix.html) and 3 more |
| Fisheries and aquaculture statistics (Directorate of Fisheries) (landings) | Registered data | ±5 %, normal, drawn per year | 20% | 20% | 1.00 | 1.00 | [Shellfish](../hydrosphere_pool/flow_HY_CW_MP_FP_Shellfish_Nmix.html), [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html) |

### References

* Fiskeridirektoratet (2025). *Fangst fordelt på art (offisiell statistikk)*. [https://www.fiskeridir.no/statistikk-tall-og-analyse/data-og-statistikk-om-yrkesfiske/fangst/fangst-fordelt-pa-art-offisiell-statistikk](https://www.fiskeridir.no/statistikk-tall-og-analyse/data-og-statistikk-om-yrkesfiske/fangst/fangst-fordelt-pa-art-offisiell-statistikk)
* Hohmann-Marriott, M. F. (2025). A Nitrogen budget for Norway analysis of Nitrogen flows from societal and natural sources (1961–2020). *PLOS ONE, 20*(2), e0313598. [https://doi.org/10.1371/journal.pone.0313598](https://doi.org/10.1371/journal.pone.0313598)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
