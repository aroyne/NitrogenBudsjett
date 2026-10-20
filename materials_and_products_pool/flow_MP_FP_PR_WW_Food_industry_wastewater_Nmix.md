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
#### Flow description

- **MP.FP-PR.WW-Food industry wastewater-Nmix** is N discharged from food industry facilities that are connected to the municipal sewage network; facilities with unknown connection status are counted in MP.FP-HY.SW-Untreated wastewater-Nmix.

#### Data sources

- Data from Miljødirektoratet (personal communication, 2026) on emissions to water from individual industries: facilities with discharge permits from Miljødirektoratet or the county governor (statsforvalteren) report their annual emissions to water as required by the permit ([reporting](https://www.miljodirektoratet.no/skjema/industri-rapportering/)); the values are self-reported by the facilities, measured or calculated, and published in [Norske utslipp](https://www.norskeutslipp.no).
- We use total nitrogen per facility and year from a data extract from Miljødirektoratet that also states whether the facility is connected to the municipal sewage network. The number of facilities reporting total nitrogen (all sectors) rises from 33 in 1989 to 122 in 2023, so part of the change over time reflects more facilities reporting rather than a change in emissions.

#### Assumptions

- Each facility is assigned manually to FP or OP (industry_categories.xlsx), based on the information given in the statistic.
- A year missing inside a facility's reporting period is filled by linear interpolation between its neighbouring reported years.
- The 2022 report from Biomar's feed factory at Myre (574 t N, against 0.065 t in 2023 and 3.9 t in 2024) is left out as a reporting error, most likely kg reported as tonnes.
- Miljødirektoratet's data has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±15 %) applied to reflect that it is not a real, independently observed value.

#### Interpretations and comparisons

- The flow is small, 0.03–0.3 kt N in most years.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Facility reports of N to water (Norwegian Environment Agency) (Findus avd. Tønsberg) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 37% | – | 0.23 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Seagarden) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 16% | – | 0.22 | none |
| Held constant or averaged (2023+) | Gap filling: held constant or averaged | ±15–15 %, lognormal, grows with distance to known year | – | 12% | – | 1.00 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Nortura SA Steinkjer) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 9% | – | 0.11 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Nortura Hærland) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 8% | – | 0.10 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Nortura SA, Avd Bjerka) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 4% | – | 0.08 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Fatland Oslo) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 3% | – | 0.06 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Ringnes Bryggeri) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 2% | – | 0.06 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Nordfjord kjøtt, Loen) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 2% | – | 0.05 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Tine SA avd. Verdal) | Survey or self-reported data | ±30 %, normal, drawn per year | – | 2% | – | 0.05 | none |
| Facility reports of N to water (Norwegian Environment Agency) (TINE Meieriet Oslo) | Survey or self-reported data | ±30 %, normal, drawn per year | 10% | 2% | 0.19 | 0.04 | none |
| Facility reports of N to water (Norwegian Environment Agency) (Idun Fabrikker A.S) | Survey or self-reported data | ±30 %, normal, drawn per year | 8% | – | 0.36 | – | none |
| Facility reports of N to water (Norwegian Environment Agency) (Norsk Protein A/S, avd. Fredrikstad) | Survey or self-reported data | ±30 %, normal, drawn per year | 64% | – | 0.49 | – | none |
| Facility reports of N to water (Norwegian Environment Agency) (Norsk Protein AS, Ingeberg, Hamar) | Survey or self-reported data | ±30 %, normal, drawn per year | 17% | – | 0.25 | – | none |
