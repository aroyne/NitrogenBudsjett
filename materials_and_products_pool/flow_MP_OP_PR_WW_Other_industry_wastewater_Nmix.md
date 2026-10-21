---
layout: default
title: Other Industry Wastewater
parent: Other Producing Industry (MP.OP)
nav_order: 11
---

# Other Industry Wastewater

<iframe src="../output_files/plots/MP_OP_PR_WW_Other_industry_wastewater_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-PR.WW-Other industry wastewater-Nmix** is N discharged from other producing industry facilities to the municipal sewage network, found by counting those that are reported to be connected to municipal wastewater treatment.

#### Data sources

- Data from Miljødirektoratet (personal communication, 2026) on emissions to water from individual industries: facilities with discharge permits from Miljødirektoratet or the county governor (statsforvalteren) report their annual emissions to water as required by the permit ([reporting](https://www.miljodirektoratet.no/skjema/industri-rapportering/)); the values are self-reported by the facilities, measured or calculated, and published in [Norske utslipp](https://www.norskeutslipp.no).
- We use total nitrogen per facility and year from a data extract from Miljødirektoratet that also states whether the facility is connected to the municipal sewage network. The number of facilities reporting total nitrogen (all sectors) rises from 33 in 1989 to 122 in 2023, so part of the change over time reflects more facilities reporting rather than a change in emissions.
- These emissions are also reported by Miljødirektoratet (Miljødirektoratet, 2025)<!--cite:miljodirektoratet_norske_2025-->, but as of February 2026 the publicly available data did not include information on connection to municipal wastewater.

#### Assumptions

- Each facility is assigned manually to FP or OP (industry_categories.xlsx), based on the information given in the statistic.
- A year missing inside a facility's reporting period is filled by linear interpolation between its neighbouring reported years.
- Facilities that are connected to the municipal network are counted in this flow.
- Miljødirektoratet's data has not been updated for 2024 at the time of writing; the 2024 value is held at the 2023 value.

#### Interpretations and comparisons

- The flow is small, below 0.2 kt N per year: few of the OP facilities that report nitrogen discharge to the municipal network.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Facility reports of N to water (Norwegian Environment Agency) (Biosirk Norge AS, avd. Trehørningen, Hamar) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 88% | – | 0.77 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Facility reports of N to water (Norwegian Environment Agency) (Biosirk Norge AS avd Grødaland) | Survey or self-reported data | ±30 %, normal, drawn per year | <1% | 7% | 0.05 | 0.22 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Held constant or averaged (2023+) | Gap filling: held constant or averaged | ±15–15 %, lognormal, grows with distance to known year | – | 5% | – | 1.00 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Facility reports of N to water (Norwegian Environment Agency) (Aarenes Lærfabrikk A.S) | Survey or self-reported data | ±30 %, normal, drawn per year | 86% | – | 0.82 | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Facility reports of N to water (Norwegian Environment Agency) (Kverneland Klepp Avd. Øksnevad -galvano) | Survey or self-reported data | ±30 %, normal, drawn per year | 13% | – | 0.30 | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |

### References

* Miljødirektoratet (2025). *Norske utslipp - Utslipp til luft og vann og generert avfall, Nitrogen totalt*. [https://www.norskeutslipp.no/no/Komponenter/Utslipp/Nitrogen-totalt/?ComponentType=utslipp&ComponentPageID=226](https://www.norskeutslipp.no/no/Komponenter/Utslipp/Nitrogen-totalt/?ComponentType=utslipp&ComponentPageID=226)
