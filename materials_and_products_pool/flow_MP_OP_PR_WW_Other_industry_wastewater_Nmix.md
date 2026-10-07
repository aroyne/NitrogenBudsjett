---
layout: default
title: Other Industry Wastewater
parent: Other Producing Industry (MP.OP)
nav_order: 11
---

# Other Industry Wastewater

<iframe src="../output_files/plots/MP_OP_PR_WW_Other_industry_wastewater_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**MP.OP-PR.WW-Other industry wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to water from individual industries, where industries are categorized as belonging to OP or FP based on the information given in the statistic, and counting those that are not reported to be connected to municipal wastewater treatment. These emissions are also reported by Miljødirektoratet (Miljødirektoratet, 2025)<!--cite:miljodirektoratet_norske_2025-->, but as of February 2026 the publicly available data did not include information on connection to municipal wastewater. Miljødirektoratet's data has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.

**How the numbers are derived**

- Facilities with discharge permits from Miljødirektoratet or the county governor (statsforvalteren) report their annual emissions to water as required by the permit ([reporting](https://www.miljodirektoratet.no/skjema/industri-rapportering/)); the values are self-reported by the facilities, measured or calculated, and published in [Norske utslipp](https://www.norskeutslipp.no).
- We use total nitrogen per facility and year from a data extract from Miljødirektoratet that also states whether the facility is connected to the municipal sewage network, and have assigned each facility manually to FP or OP (industry_categories.xlsx).
- The number of facilities reporting total nitrogen (all sectors) rises from 33 in 1989 to 122 in 2023, so part of the change over time reflects more facilities reporting rather than a change in emissions.
- A year missing inside a facility's reporting period is filled by linear interpolation between its neighbouring reported years.
- Facilities that are connected to the municipal network are counted in this flow.

**Interpretation**

- The flow is small, below 0.2 kt N per year: few of the OP facilities that report nitrogen discharge to the municipal network.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Miljødirektoratet (2025). *Norske utslipp - Utslipp til luft og vann og generert avfall, Nitrogen totalt*. [https://www.norskeutslipp.no/no/Komponenter/Utslipp/Nitrogen-totalt/?ComponentType=utslipp&ComponentPageID=226](https://www.norskeutslipp.no/no/Komponenter/Utslipp/Nitrogen-totalt/?ComponentType=utslipp&ComponentPageID=226)
