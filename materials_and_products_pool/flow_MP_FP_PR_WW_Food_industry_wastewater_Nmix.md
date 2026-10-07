---
layout: default
title: Food Industry Wastewater
parent: Food and Feed Processing (MP.FP)
nav_order: 7
---

# Food Industry Wastewater

<iframe src="../output_files/plots/MP_FP_PR_WW_Food_industry_wastewater_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**MP.FP-PR.WW-Food industry wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to water from individual industries, where industries are categorized as belonging to OP or FP, and their connection status to the municipal wastewater, based on the information given in the statistic. This flow counts the FP facilities that are connected to the municipal sewage network; facilities with unknown connection status are counted in MP.FP-HY.SW-Untreated wastewater-Nmix. Miljødirektoratet's data has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.

**How the numbers are derived**

- Facilities with discharge permits from Miljødirektoratet or the county governor (statsforvalteren) report their annual emissions to water as required by the permit ([reporting](https://www.miljodirektoratet.no/skjema/industri-rapportering/)); the values are self-reported by the facilities, measured or calculated, and published in [Norske utslipp](https://www.norskeutslipp.no).
- We use total nitrogen per facility and year from a data extract from Miljødirektoratet that also states whether the facility is connected to the municipal sewage network, and have assigned each facility manually to FP or OP (industry_categories.xlsx).
- The number of facilities reporting total nitrogen (all sectors) rises from 33 in 1989 to 122 in 2023, so part of the change over time reflects more facilities reporting rather than a change in emissions.
- A year missing inside a facility's reporting period is filled by linear interpolation between its neighbouring reported years.
- Facilities that are connected to the municipal network are counted in this flow.

**Interpretation**

- The flow is small, 0.03–0.3 kt N in most years.
- The 2022 report from Biomar's feed factory at Myre (574 t N, against 0.065 t in 2023 and 3.9 t in 2024) is left out as a reporting error, most likely kg reported as tonnes.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
