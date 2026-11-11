---
layout: default
title: Energy conversion emissions (NOx)
parent: Energy conversion (EF.EC)
nav_order: 2
---

# Energy conversion emissions (NOx)

<iframe src="../output_files/plots/EF_EC_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.EC-AT.AT-Emissions-NOx** is NO<sub>x</sub> from energy industries and fugitive emissions in the oil and gas sector, using the categories given in Table 11 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- Public electricity and heat production (1A1a, 0.35–0.7 kt N/year<!--range:nfr/1A1a/NOx:1990-2024-->) is included in full, also waste incineration with energy recovery. Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> (chapter 1.4.1.2 and Table 48) count the waste part under PR.SO, but here the incinerated waste is delivered to EF.EC (PR.SO-EF.EC-Waste to energy-Nmix), so its emissions are counted here too. The waste part, estimated with the waste share of the 1.A.1.a fuel use in the CRT (10–48 %, 48 % in 2024), is 0.06–0.32 kt N/year.
- NH<sub>3</sub> emissions from these categories are reported as zero or not occurring, and NH<sub>3</sub> from 1A1a is below 0.001 kt N/year, which is why there is no EF.EC NH<sub>3</sub> flow.

#### Data sources

- Emissions reported by Norway to the UN Convention on Long-range Transboundary Air Pollution (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The reported emissions are not measured but calculated in the national inventory, mainly as activity data (fuel consumption by fuel type and source category, from the national energy statistics) multiplied by emission factors, following the EMEP/EEA Guidebook (European Environment Agency, 2023)<!--cite:eea_guidebook_2023-->; for some large point sources, plant-specific reported emissions are used. The methods are documented in the Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.

#### Interpretations

- Oil and gas extraction (1A1c, mainly gas turbines on offshore installations) dominates the flow: its NO<sub>x</sub> emissions rose from 7.6 kt N/year<!--val:nfr/1A1c/NOx:1990--> in 1990 to about 14.6 kt N<!--mean:nfr/1A1c/NOx:2005-2015--> in 2005–2015 with increasing petroleum production and have since fallen to 10.0 kt N<!--val:nfr/1A1c/NOx:2024--> in 2024.
- Refineries (1A1b) and fugitive emissions including flaring (1B2) contribute up to 0.5 and 0.9 kt N/year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, Manufacture of solid fuels and other energy industries (NFR 1A1c) | Inventory with published uncertainty | ±20 %, normal | 99% | 99% | 0.85 | 0.91 | none |

### References

* <span id="ref-eea_guidebook_2023" data-cite="European Environment Agency" data-year="2023"></span>European Environment Agency (2023). *EMEP/EEA air pollutant emission inventory guidebook 2023* (EMEP/EEA joint report 06/2023). [eea.europa.eu](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023)
* <span id="ref-emep_officially_2025" data-cite="EMEP" data-year="2025"></span>EMEP (2025). *Officially reported emission data*. [ceip.at](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* <span id="ref-miljodirektoratet_iir_2026" data-cite="Miljødirektoratet" data-year="2026"></span>Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
