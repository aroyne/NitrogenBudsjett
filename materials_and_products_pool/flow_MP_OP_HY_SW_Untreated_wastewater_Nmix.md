---
layout: default
title: Untreated Wastewater (Other Industry)
parent: Other Producing Industry (MP.OP)
nav_order: 9
---

# Untreated Wastewater (Other Industry)

<iframe src="../output_files/plots/MP_OP_HY_SW_Untreated_wastewater_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**MP.OP-HY.SW-Untreated wastewater-Nmix** is found using data from Miljødirektoratet (personal communication, 2026) on emissions to water from individual industries, where industries are categorized as belonging to OP or FP based on the information given in the statistic, and counting those that are not reported to be connected to municipal wastewater treatment. In OP we include industries that process petroleum products that could arguably also have been designated as a separate flow in the EF pool. These emissions are also reported by Miljødirektoratet (Miljødirektoratet, 2025)<!--cite:miljodirektoratet_norske_2025-->, but as of February 2026 the publicly available data did not include information on connection to municipal wastewater. The database does not distinguish between emissions to surface and coastal waters, so even though several large industries discharge their wastewater to the coast, we assign this entire flow to SW in order to avoid double counting. Miljødirektoratet's data has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.

**How the numbers are derived**

- Facilities with discharge permits from Miljødirektoratet or the county governor (statsforvalteren) report their annual emissions to water as required by the permit ([reporting](https://www.miljodirektoratet.no/skjema/industri-rapportering/)); the values are self-reported by the facilities, measured or calculated, and published in [Norske utslipp](https://www.norskeutslipp.no).
- We use total nitrogen per facility and year from a data extract from Miljødirektoratet that also states whether the facility is connected to the municipal sewage network, and have assigned each facility manually to FP or OP (industry_categories.xlsx).
- The number of facilities reporting total nitrogen (all sectors) rises from 33 in 1989 to 122 in 2023, so part of the change over time reflects more facilities reporting rather than a change in emissions.
- A year missing inside a facility's reporting period is filled by linear interpolation between its neighbouring reported years.
- Facilities that are not connected to the municipal network, or whose connection is unknown, are counted in this flow.

**Interpretation**

- The flow falls from 3.5 kt N in 1990 (5.0 kt N in 1989) to 1.4 kt N in 2024.
- The fertilizer and chemical industry dominates: in 1990 Herøya industrial park (1.5 kt N), Yara Glomfjord (0.86 kt N) and Hydro Rjukan (0.32 kt N) were the largest sources, and in 2023 Yara Porsgrunn and Yara Glomfjord together account for about 0.9 kt N.
- Other sources are Borregaard (about 0.1 kt N), the Mongstad refinery and pulp and paper mills.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Miljødirektoratet (2025). *Norske utslipp - Utslipp til luft og vann og generert avfall, Nitrogen totalt*. [https://www.norskeutslipp.no/no/Komponenter/Utslipp/Nitrogen-totalt/?ComponentType=utslipp&ComponentPageID=226](https://www.norskeutslipp.no/no/Komponenter/Utslipp/Nitrogen-totalt/?ComponentType=utslipp&ComponentPageID=226)
