---
layout: default
title: Leaching from Landfills
parent: Solid Waste (PR.SO)
nav_order: 7
---

# Leaching from Landfills

<iframe src="../output_files/plots/PR_SO_HY_SW_Leaching_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.SO-HY.SW-Leaching-Nmix** is N leached to surface water from landfills that are not connected to a municipal sewage network.

#### Data sources

- Landfills with discharge permits report their annual emissions of total nitrogen to water to Miljødirektoratet, published in [Norske utslipp](https://www.norskeutslipp.no) (Miljødirektoratet, 2026<!--cite:miljodirektoratet_norske_2026-->; Utslipp_deponi.xlsx); the values are measured or calculated by the landfill operators. Reported data only cover a single landfill in 2009–2010 and are not representative.
- Methane from landfills in the national inventory (CRT Table 5, 5.A), which is calculated with a first-order decay model of the waste landfilled in earlier years and so follows the decomposition that also produces leachate. Methane from landfills fell from 82.5 kt in 1990 to 51.6 kt in 2010 and 28.6 kt in 2024.

#### Assumptions

- Each landfill is classified as connected or not connected to a municipal sewage network from publicly available information; where this was not possible, half of the emissions are assigned to each of PR.SO-HY.SW-Leaching-Nmix and PR.SO-PR.WW-Wastewater from landfills-Nmix.
- 1990–2010 are the mean of 2011 onward scaled with methane from landfills.

#### Interpretations and comparisons

- The flow is about 0.2–1.3 kt N per year since 2011, with no clear trend.
- The extrapolated values fall from about 1.0 kt N in 1990 to 0.65 kt N in 2010, following the decline in landfill methane.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Facility reports of N to water (Norwegian Environment Agency) (lindum as avd drammen - avfallsdeponi (lindum as)) | Survey or self-reported data | ±30 %, normal, drawn per year | 4% | 66% | 0.26 | 0.32 | none |
| Facility reports of N to water (Norwegian Environment Agency) (norske skog skogn, deponi valum - industrideponi (norske skog skogn as)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 8% | 0.02 | 0.07 | none |
| Facility reports of N to water (Norwegian Environment Agency) (ngir kjevikdalen avfallsdeponi (nordhordland og gulen interkommunale renovasjonsselskap iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 5% | 0.03 | 0.04 | none |
| Facility reports of N to water (Norwegian Environment Agency) (iris - vikan - deponi for ordinært avfall (iris salten iks)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 3% | 0.02 | 0.04 | none |
| Facility reports of N to water (Norwegian Environment Agency) (franzefoss gjenvinning - eide avfallsdeponi (franzefoss gjenvinning as)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 3% | 0.04 | 0.05 | none |
| Facility reports of N to water (Norwegian Environment Agency) (ulsethsanden deponi - rockwool industrideponi (as rockwool)) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 3% | 0.06 | 0.04 | none |
| Extrapolation (landfill N:CH4 index) | Gap filling: extrapolation | ±50–50 %, lognormal, grows with distance to known year | 94% | – | 1.00 | – | [Wastewater from Landfills](../processing_of_residues_pool/flow_PR_SO_PR_WW_Wastewater_from_landfills_Nmix.html) |

### References

* Miljødirektoratet (2026). *Norske Utslipp*. [norskeutslipp.no](norskeutslipp.no)
