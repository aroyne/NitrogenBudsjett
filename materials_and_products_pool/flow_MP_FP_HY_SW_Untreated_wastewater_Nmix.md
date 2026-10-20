---
layout: default
title: Untreated Wastewater (Food Industry)
parent: Food and Feed Processing (MP.FP)
nav_order: 5
---

# Untreated Wastewater (Food Industry)

<iframe src="../output_files/plots/MP_FP_HY_SW_Untreated_wastewater_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-HY.SW-Untreated wastewater-Nmix** is N discharged to water from food industry facilities that are not connected to the municipal sewage network.
- The database does not distinguish between emissions to surface and coastal waters, so even though several large industries discharge their wastewater to the coast, we assign this entire flow to SW in order to avoid double counting.

#### Data sources

- Data from Miljødirektoratet (personal communication, 2026) on emissions to water from individual industries: facilities with discharge permits from Miljødirektoratet or the county governor (statsforvalteren) report their annual emissions to water as required by the permit ([reporting](https://www.miljodirektoratet.no/skjema/industri-rapportering/)); the values are self-reported by the facilities, measured or calculated, and published in [Norske utslipp](https://www.norskeutslipp.no).
- We use total nitrogen per facility and year from a data extract from Miljødirektoratet that also states whether the facility is connected to the municipal sewage network. The number of facilities reporting total nitrogen (all sectors) rises from 33 in 1989 to 122 in 2023, so part of the change over time reflects more facilities reporting rather than a change in emissions.
- The values reported for 1989–1992 are significantly lower than for later years.

#### Assumptions

- Each facility is assigned manually to FP or OP (industry_categories.xlsx), based on the information given in the statistic.
- A year missing inside a facility's reporting period is filled by linear interpolation between its neighbouring reported years.
- Facilities that are not connected to the municipal network, or whose connection is unknown, are counted in this flow.
- We extrapolate back to 1990 using the mean value for 1994–1998.
- Miljødirektoratet's data has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±15 %) applied to reflect that it is not a real, independently observed value.

#### Interpretations and comparisons

- The flow is about 0.3–0.5 kt N per year until 2012 and 0.6–0.9 kt N from 2013.
- From 2013 a number of salmon slaughterhouses and fish processing plants report emissions, which explains much of the increase.
- The largest single source over the period is DuPont Nutrition Norge (formerly FMC, alginate production from seaweed), with about 0.2 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Facility reports of N to water (Norwegian Environment Agency) (DuPont Nutrition Norge AS (tidligere FMC)) | Survey or self-reported data | ±30 %, normal, drawn per year | 73% | 57% | 0.92 | 0.26 | none |
| Held constant or averaged (2023+) | Gap filling: held constant or averaged | ±15–15 %, lognormal, grows with distance to known year | – | 13% | – | 1.00 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Biproduktanlegget på Kverva - laks - Nutrimar AS) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 13% | – | 0.09 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Innovamar - slakteri og fiskeforedling - Kverva) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 3% | – | 0.06 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Hav Line - Slakteskipet Norwegian Gannet) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 2% | – | 0.05 | none |
| Held constant or averaged (1994-1998) | Gap filling: held constant or averaged | ±15–30 %, lognormal, grows with distance to known year | 27% | – | 1.00 | – | none |
