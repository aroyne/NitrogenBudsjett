---
layout: default
title: Game Meat from Forests
parent: Forests (FS.FO)
nav_order: 7
---

# Game Meat from Forests

<iframe src="../output_files/plots/FS_FO_HS_HS_Game_meat_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.FO-HS.HS-Game meat-Nmix** is the N in meat from moose, red deer and roe deer shot in ordinary hunting. These animals live mainly in forest. The meat is assumed to be eaten in households, mostly by the hunters themselves. This flow is not in the flow tables of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- Animals killed outside ordinary hunting (traffic, culling) and offal left in the field are not included.

#### Data sources

- SSB's hunting statistics ([Jakt](https://www.ssb.no/jord-skog-jakt-og-fiskeri/jakt)): calculated total carcass weight of moose (table 10817) and red deer (table 10818) from the 1998–1999 hunting season, and the number of moose (06036), red deer (06037) and roe deer (03947) shot. SSB calculates the carcass weight from the number of animals shot by age and sex and average carcass weights.
- Average carcass weight of roe deer, 14.5 kg, as used by SSB in its hunting statistics (SSB, 1977)<!--cite:ssb_jaktstatistikk_1977-->.
- N content of game meat 2.5% of the carcass weight ("Meat, other", which includes game, in Table 21 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->).

#### Assumptions

- Each hunting season is assigned to the year it starts.
- Before 1998, moose and red deer are the number shot times the average carcass weight per animal shot in 1998–2002.
- Roe deer are the number shot times 14.5 kg (±20%). The 2016 season is missing in table 03947 and is interpolated between 2015 and 2017; the 2023 and 2024 seasons are not yet in the table and are held at the 2022 level.

#### Interpretations

- The flow is about 0.12–0.19 kt N per year. Moose accounts for most of it (79% of the carcass weight in 1990, 52% in 2024); red deer has grown from 12% to 41%, and roe deer is 7–9%.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of game meat | Parameter | ±20 %, normal | 35% | 81% | 1.00 | 1.00 | [Game Meat from Other Land](../forests_and_semi_natural_pool/flow_FS_OL_HS_HS_Game_meat_Nmix.html) |
| Hunting statistics, calculated carcass weight (SSB) | Modelled statistics | ±10 %, normal | 8% | 19% | 1.00 | 1.00 | [Game Meat from Other Land](../forests_and_semi_natural_pool/flow_FS_OL_HS_HS_Game_meat_Nmix.html) |
| Extrapolation (game meat elg <1998) | Gap filling: extrapolation | ±30–50 %, lognormal, grows with distance to known year | 55% | – | 0.77 | – | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
* SSB (1977). *Jaktstatistikk 1976* (Norges offisielle statistikk A 889). Statistisk sentralbyrå.
