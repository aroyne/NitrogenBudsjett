---
layout: default
title: Wastewater from Landfills
parent: Solid Waste (PR.SO)
nav_order: 9
---

# Wastewater from Landfills

<iframe src="../output_files/plots/PR_SO_PR_WW_Wastewater_from_landfills_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.SO-PR.WW-Wastewater from landfills-Nmix** is N in leachate from landfills connected to a municipal sewage network.

#### Data sources

- Landfills with discharge permits report their annual emissions of total nitrogen to water to Miljødirektoratet, published in [Norske utslipp](https://www.norskeutslipp.no) (Miljødirektoratet, 2026<!--cite:miljodirektoratet_norske_2026-->); the values are measured or calculated by the landfill operators. The reports start in 2011 (88 landfills); in 2009 and 2010 only one landfill reported, so these two years are not used. Five single reports are left out as outliers, since they are 20–360 times the landfill's own median and several hundred tonnes N in years when all landfills together report about 1 kt N: Stormyra (2015, 927 t), Glør (2011, 644 t), Røyken (2018, 425 t), Enger (2017, 131 t) and Norske Skog Skogn, Valum (2021, 125 t).
- Methane from landfills in the national inventory (CRT Table 5, 5.A), which is calculated with a first-order decay model of the waste landfilled in earlier years and so follows the decomposition that also produces leachate. Methane from landfills fell from 82.5 kt in 1990 to 51.6 kt in 2010 and 28.6 kt in 2024.

#### Assumptions

- Each landfill is classified as connected or not connected to a municipal sewage network from publicly available information; where this was not possible, half of the emissions are assigned to each of PR.SO-HY.SW-Leaching-Nmix and PR.SO-PR.WW-Wastewater from landfills-Nmix.
- 1990–2010 are the mean of 2011 onward scaled with methane from landfills.

#### Interpretations

- The flow is about 0.4–0.8 kt N per year<!--range:PR.SO-PR.WW-Wastewater from landfills-Nmix:2011-2024--> since 2011.
- The extrapolated values fall from about 1.3 kt N in 1990 to 0.8 kt N in 2010, following the decline in landfill methane.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Facility reports of N to water (Miljødirektoratet) (støleheia avfallsanlegg - deponi (avfall sør husholdning as)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 36% | 0.08 | 0.15 | none |
| Facility reports of N to water (Miljødirektoratet) (bjorstaddalen næring deponi (bjorstaddalen næring as)) | Survey or self-reported data | ±30 %, normal, drawn per year | 1% | 28% | 0.10 | 0.13 | none |
| Facility reports of N to water (Miljødirektoratet) (sele avfallsplass - deponi (ivar iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 8% | 0.07 | 0.07 | none |
| Facility reports of N to water (Miljødirektoratet) (grønmo avfallsanlegg - deponi (nedlagt - avslutningsfase) (etterdrift) (oslo kommune eiendoms- og byfornyelsesetaten)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 4% | 0.05 | 0.05 | none |
| Facility reports of N to water (Miljødirektoratet) (solgård avfallsplass - deponi (movar iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 3% | 0.05 | 0.04 | none |
| Facility reports of N to water (Miljødirektoratet) (roaf miljøpark - deponi (romerike avfallsforedling iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 3% | 0.04 | 0.04 | none |
| Facility reports of N to water (Miljødirektoratet) (glør roverudmyra deponi kategori 2, ordinært avfall (renovasjonsselskapet glør iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 2% | 0.05 | 0.04 | none |
| Facility reports of N to water (Miljødirektoratet) (esval miljøpark - ordinært deponi (esval miljøpark nes kf)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 2% | 0.03 | 0.04 | none |
| Extrapolation (landfill N:CH<sub>4</sub> index) | Gap filling: extrapolation | ±50–50 %, lognormal, grows with distance to known year | 98% | – | 1.00 | – | [Leaching from Landfills](../processing_of_residues_pool/flow_PR_SO_HY_SW_Leaching_Nmix.html) |

### References

* Miljødirektoratet (2026). *Norske Utslipp*. [norskeutslipp.no](https://www.norskeutslipp.no)
