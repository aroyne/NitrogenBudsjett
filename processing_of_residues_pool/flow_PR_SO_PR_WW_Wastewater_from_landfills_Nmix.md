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

- Landfills with discharge permits report their annual emissions of total nitrogen to water to Miljødirektoratet, published in [Norske utslipp](https://www.norskeutslipp.no) (Miljødirektoratet, 2026<!--cite:miljodirektoratet_norske_2026-->; Utslipp_deponi.xlsx); the values are measured or calculated by the landfill operators. Reported data only cover a single landfill in 2009–2010 and are not representative.
- Methane from landfills in the national inventory (CRT Table 5, 5.A), which is calculated with a first-order decay model of the waste landfilled in earlier years and so follows the decomposition that also produces leachate. Methane from landfills fell from 82.5 kt in 1990 to 51.6 kt in 2010 and 28.6 kt in 2024.

#### Assumptions

- Each landfill is classified as connected or not connected to a municipal sewage network from publicly available information; where this was not possible, half of the emissions are assigned to each of PR.SO-HY.SW-Leaching-Nmix and PR.SO-PR.WW-Wastewater from landfills-Nmix.
- 1990–2010 are the mean of 2011 onward scaled with methane from landfills.

#### Interpretations and comparisons

- The flow is about 0.5–1.3 kt N per year since 2011.
- The extrapolated values fall from about 1.3 kt N in 1990 to 0.8 kt N in 2010, following the decline in landfill methane.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| Facility reports of N to water (Norwegian Environment Agency) (støleheia avfallsanlegg - deponi (avfall sør husholdning as)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 36% | none |
| Facility reports of N to water (Norwegian Environment Agency) (bjorstaddalen næring deponi (bjorstaddalen næring as)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 28% | none |
| Facility reports of N to water (Norwegian Environment Agency) (sele avfallsplass - deponi (ivar iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 8% | none |
| Facility reports of N to water (Norwegian Environment Agency) (grønmo avfallsanlegg - deponi (nedlagt - avslutningsfase) (etterdrift) (oslo kommune eiendoms- og byfornyelsesetaten)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 4% | none |
| Facility reports of N to water (Norwegian Environment Agency) (solgård avfallsplass - deponi (movar iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 3% | none |
| Facility reports of N to water (Norwegian Environment Agency) (roaf miljøpark - deponi (romerike avfallsforedling iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 3% | none |
| Facility reports of N to water (Norwegian Environment Agency) (glør roverudmyra deponi kategori 2, ordinært avfall (renovasjonsselskapet glør iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | 1% | 2% | none |
| Facility reports of N to water (Norwegian Environment Agency) (esval miljøpark - ordinært deponi (esval miljøpark nes kf)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 2% | none |
| Extrapolation (landfill N:CH4 index) | Gap filling: extrapolation | ±50–50 %, lognormal, grows with distance to known year | 97% | – | [Leaching from Landfills](../processing_of_residues_pool/flow_PR_SO_HY_SW_Leaching_Nmix.html) |

### References

* Miljødirektoratet (2026). *Norske Utslipp*. [norskeutslipp.no](norskeutslipp.no)
