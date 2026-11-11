---
layout: default
title: Untreated Wastewater (Other Industry)
parent: Other Producing Industry (MP.OP)
nav_order: 9
---

# Untreated Wastewater (Other Industry)

<iframe src="../output_files/plots/MP_OP_HY_SW_Untreated_wastewater_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-HY.SW-Untreated wastewater-Nmix** is N discharged to water from other producing industry facilities that are not reported to be connected to municipal wastewater treatment.
- The database does not distinguish between emissions to surface and coastal waters, so even though several large industries discharge their wastewater to the coast, we assign this entire flow to SW to avoid double counting.

#### Data sources

- Data from Miljødirektoratet (personal communication, 2026) on emissions to water from individual industries: facilities with discharge permits from Miljødirektoratet or the county governor (statsforvalteren) report their annual emissions to water as required by the permit ([reporting](https://www.miljodirektoratet.no/skjema/industri-rapportering/)); the values are self-reported by the facilities, measured or calculated, and published in [Norske utslipp](https://www.norskeutslipp.no).
- We use total nitrogen per facility and year from a data extract from Miljødirektoratet that also states whether the facility is connected to the municipal sewage network. The number of facilities reporting total nitrogen (all sectors) rises from 33 in 1989 to 122 in 2023, so part of the change over time reflects more facilities reporting rather than a change in emissions.
- These emissions are also reported by Miljødirektoratet (Miljødirektoratet, 2025)<!--cite:miljodirektoratet_norske_2025-->, but as of February 2026 the publicly available data did not include information on connection to municipal wastewater.

#### Assumptions

- One unexpectedly large value from a single facility is left out as a reporting error.
- Each facility is assigned manually to FP or OP, based on the information given in the statistic.
- A year missing inside a facility's reporting period is filled by linear interpolation between its neighbouring reported years.
- Facilities that are not connected to the municipal network, or whose connection is unknown, are counted in this flow.
- Miljødirektoratet's data has not been updated for 2024 at the time of writing; the 2024 value is held at the 2023 value.

#### Interpretations

- The flow falls from 3.5 kt N<!--val:MP.OP-HY.SW-Untreated wastewater-Nmix:1990--> in 1990 (5.0 kt N<!--val:MP.OP-HY.SW-Untreated wastewater-Nmix:1989--> in 1989) to 1.4 kt N<!--val:MP.OP-HY.SW-Untreated wastewater-Nmix:2024--> in 2024.
- The fertilizer and chemical industry dominates: in 1990 Herøya industrial park (1.5 kt N), Yara Glomfjord (0.86 kt N) and Hydro Rjukan (0.32 kt N) were the largest sources, and in 2023 Yara Porsgrunn and Yara Glomfjord together account for about 0.9 kt N.
- Other sources are Borregaard (about 0.1 kt N), the Mongstad refinery and pulp and paper mills.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Facility reports of N to water (Miljødirektoratet) (Yara Porsgrunn) | Survey or self-reported data | ±30 %, normal, drawn per year | 47% | 66% | 0.47 | 0.41 | none |
| Facility reports of N to water (Miljødirektoratet) (Yara Glomfjord) | Survey or self-reported data | ±30 %, normal, drawn per year | 21% | 20% | 0.23 | 0.22 | none |
| Held constant or averaged (2023+) | Gap filling: held constant or averaged | ±15–15 %, lognormal, grows with distance to known year | – | 9% | – | 1.00 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Facility reports of N to water (Miljødirektoratet) (Herøya Industripark) | Survey or self-reported data | ±30 %, normal, drawn per year | 29% | – | 0.42 | – | none |

### References

* <span id="ref-miljodirektoratet_norske_2025" data-cite="Miljødirektoratet" data-year="2025"></span>Miljødirektoratet (2025). *Norske utslipp - Utslipp til luft og vann og generert avfall, Nitrogen totalt*. [norskeutslipp.no](https://www.norskeutslipp.no/no/Komponenter/Utslipp/Nitrogen-totalt/?ComponentType=utslipp&ComponentPageID=226)
