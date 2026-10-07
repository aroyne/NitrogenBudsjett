---
layout: default
title: Other Land Emissions (NOx)
parent: Other Land (FS.OL)
nav_order: 4
---

# Other Land Emissions (NOx)

<iframe src="../output_files/plots/FS_OL_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.OL-AT.AT-Emissions-NOx** is NOx from manure deposited by grazing animals on utmark (AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix).
- NOx from the soils of other land is neglected because no values are reported in the CRLTAP categories 4F1 and 4F2 (wetlands / other land).

#### Data sources

- Emissions from grazing animals (NFR 3Da3) reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), calculated in the national inventory with the manure model: N deposited during grazing multiplied by emission factors ([Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)).
- The inventory reports the emissions from grazing for all land types combined; it does not split innmark and utmark.

#### Assumptions

- The flow is the utmark share of the NOx from grazing animals (3Da3). The utmark share is the grazing manure per animal category (CRT Table 3.B(b)) weighted with the share of each category's grazing time spent on utmark in 2018 (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79): dairy cows 16%, suckler cows 30%, other cattle 32%, sheep 51%, goats 54% and horses 16% (each ±20%), reindeer 100% and farmed deer 0%. This gives 35–39% of the grazing manure. The shares are held at the 2018 survey values for all years; before 2009 the subsidy rules required a longer grazing period on utmark (eight instead of five weeks), so the share may have been somewhat higher.
- The same amount is removed from AG.SM-AT.AT-Emissions-NOx.

#### Interpretations and comparisons

- The flow is small, about 0.1 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
