---
layout: default
title: Shellfish
parent: Coastal Water (HY.CW)
nav_order: 2
---

# Shellfish

<iframe src="../output_files/plots/HY_CW_MP_FP_Shellfish_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HY.CW-MP.FP-Shellfish-Nmix** combines the catch of shellfish and crustaceans and wild-harvested macroalgae (seaweed). The macroalgae harvest is almost all kelp (Laminaria hyperborea).
- **The flow includes Antarctic krill, which is part of the Norwegian catch statistics but is caught in the Southern Ocean, not in Norwegian coastal waters. Krill accounts for most of the growth in the flow after 2005 (about 9 kt N in 2024).**

#### Data sources

- Catch of crustaceans and molluscs and harvest of macroalgae (wet weight) from Fiskeridirektoratet (2025)<!--cite:fiskeridirektoratet_fangst_2025-->: from the catch statistics by species from 2000, and from a historical compilation for 1990–1999.
- N content of kelp: 1–2% N in dry matter (Sjøtun et al., 1996; Schiener et al., 2015)<!--cite:sjotun_seasonal_1996,schiener_seasonal_2015--> and 11–16% dry matter.

#### Assumptions

- Shellfish and crustaceans: 2.8% N (Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 254, UNECE Guidance Annex 6 Table 12).
- Macroalgae: 0.2% N in wet weight (range 0.1–0.4%). The 4% N given for aquatic plants in Table 21 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> would correspond to about 25% protein and must refer to dry weight.

#### Interpretations

- The flow is about 2–2.5 kt N per year up to 2005 and rises to 11 kt N in 2024, almost entirely from Antarctic krill (no catch in 2000 and 2005, 320 kt in 2024, about 9 kt N), which is caught in the Southern Ocean; snow crab and king crab contribute much less.
- Kelp contributes about 0.3–0.4 kt N per year.
- All the krill is landed in Uruguay (Fiskeridirektoratet table F.06.002) and never enters Norway. It does not appear as export to Uruguay in SSB table 08801 (nothing before 2024, 6 kt fish and crustacean meal in 2024), so the krill N (0.3 kt N in 2006, about 9 kt N in 2024) is added to MP.FP-RW.RW-Food export-Nmix.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of fish and seafood | Parameter | ±10 %, normal | 25% | 75% | 0.81 | 0.97 | [Excretia](../hydrosphere_pool/flow_HY_AC_HY_CW_Excretia_Nmix.html), [Waste feed](../hydrosphere_pool/flow_HY_AC_HY_CW_Waste_feed_Nmix.html), [Aquaculture production](../hydrosphere_pool/flow_HY_AC_MP_FP_Coastal_fish_and_seafood_Nmix.html), [Wild fish catch](../hydrosphere_pool/flow_HY_CW_MP_FP_Fish_(wild_catch)_Nmix.html) and 3 more |
| Fisheries and aquaculture statistics (Directorate of Fisheries) (landings) | Registered data | ±5 %, normal, drawn per year | 9% | 20% | 1.00 | 1.00 | [Wild fish catch](../hydrosphere_pool/flow_HY_CW_MP_FP_Fish_(wild_catch)_Nmix.html), [Food Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Food_export_Nmix.html) |
| N content of harvested kelp | Parameter | 0.001–0.004, lognormal | 66% | 5% | 0.19 | 0.03 | none |

### References

* Fiskeridirektoratet (2025). *Fangst fordelt på art (offisiell statistikk)*. [fiskeridir.no](https://www.fiskeridir.no/statistikk-tall-og-analyse/data-og-statistikk-om-yrkesfiske/fangst/fangst-fordelt-pa-art-offisiell-statistikk)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
* Schiener, P., Black, K. D., Stanley, M. S., & Green, D. H. (2015). The seasonal variation in the chemical composition of the kelp species Laminaria digitata, Laminaria hyperborea, Saccharina latissima and Alaria esculenta. *Journal of Applied Phycology, 27*, 363-373. [https://doi.org/10.1007/s10811-014-0327-1](https://doi.org/10.1007/s10811-014-0327-1)
* Sjøtun, K., Fredriksen, S., & Rueness, J. (1996). Seasonal growth and carbon and nitrogen content in canopy and first-year plants of Laminaria hyperborea (Laminariales, Phaeophyceae). *Phycologia, 35*(1), 1-8. [https://doi.org/10.2216/i0031-8884-35-1-1.1](https://doi.org/10.2216/i0031-8884-35-1-1.1)
