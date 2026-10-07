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
- Miljødirektoratet's data has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.

#### Interpretations and comparisons

- The flow is about 0.3–0.5 kt N per year until 2012 and 0.6–0.9 kt N from 2013.
- From 2013 a number of salmon slaughterhouses and fish processing plants report emissions, which explains much of the increase.
- The largest single source over the period is DuPont Nutrition Norge (formerly FMC, alginate production from seaweed), with about 0.2 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
