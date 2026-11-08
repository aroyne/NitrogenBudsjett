---
layout: default
title: Game Meat from Other Land
parent: Other Land (FS.OL)
nav_order: 6
---

# Game Meat from Other Land

<iframe src="../output_files/plots/FS_OL_HS_HS_Game_meat_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.OL-HS.HS-Game meat-Nmix** is the N in meat from wild reindeer shot in ordinary hunting. Wild reindeer live in mountain areas (other land). This flow is not in the flow tables of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- Small game (grouse, hare, ducks and others) is not included. About 350 000–400 000 animals were shot per year in 2019–2023 and 0.7–1.3 million in the 1990s (SSB table 03886), which gives at most a few hundred tonnes of meat, about 0.01 kt N or less.

#### Data sources

- SSB's calculated total carcass weight of wild reindeer shot in ordinary hunting (table 10820, from the 1986–1987 season).
- N content of game meat 2.5% of the carcass weight ("Meat, other" in Table 21 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->).

#### Assumptions

- Each hunting season is assigned to the year it starts.

#### Interpretations

- The flow is below 0.01 kt N per year (about 0.008 kt N<!--val:FS.OL-HS.HS-Game meat-Nmix:1990--> around 1990 and 0.003 kt N<!--val:FS.OL-HS.HS-Game meat-Nmix:2024--> in 2024).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of game meat | Parameter | ±20 %, normal | 81% | 81% | 1.00 | 1.00 | [Game Meat from Forests](../forests_and_semi_natural_pool/flow_FS_FO_HS_HS_Game_meat_Nmix.html) |
| Hunting statistics, calculated carcass weight (SSB) | Modelled statistics | ±10 %, normal | 19% | 19% | 1.00 | 1.00 | [Game Meat from Forests](../forests_and_semi_natural_pool/flow_FS_FO_HS_HS_Game_meat_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
