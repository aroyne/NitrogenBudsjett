---
layout: default
title: Energy conversion emissions (NOx)
parent: Energy conversion (EF.EC)
nav_order: 2
---

# Energy conversion emissions (NOx)

<iframe src="../output_files/plots/EF_EC_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
EF.EC-AT.AT-Emissions-NOx: We have used data from CLRTAP Inventory Submissions EMEP (2025)<!--cite:emep_officially_2025--> as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, using the categories given in Table 11.

**How the numbers are derived**

- The emissions reported to CLRTAP are not measured but calculated in the national inventory, mainly as activity data (fuel consumption by fuel type and source category, from the national energy statistics) multiplied by emission factors, following the [EMEP/EEA Guidebook 2023](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023); for some large point sources, plant-specific reported emissions are used.
- The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).
- The values are reported in Gg NOx (as NO2) or Gg NH3 and converted to N with the factors 14/46 and 14/17, respectively.

**Interpretation**

- Oil and gas extraction (1A1c, mainly gas turbines on offshore installations) dominates the flow: its NOx emissions rose from 25 Gg in 1990 to about 48 Gg in 2005–2015 with increasing petroleum production and have since fallen to 33 Gg in 2024, partly due to electrification of offshore installations with power from shore and NOx-reducing measures financed by the NOx Fund ([Næringslivets NOx-fond](https://www.nox-fondet.no/)).
- Refineries (1A1b) and fugitive emissions including flaring (1B2) contribute up to 1–2 Gg each.
- Public electricity and heat production (1A1a, about 1–2 Gg NOx, mainly waste incineration and district heating) is not included here but counted in the processing of residues pool (PR.SO-AT.AT), as recommended in chapter 1.4.1.2 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, to avoid double counting.
- NH3 emissions from these categories are reported as zero or not occurring, which is why there is no EF.EC NH3 flow.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
