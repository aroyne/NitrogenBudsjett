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
- Public electricity and heat production (1A1a, 0.35–0.7 kt N/year) is split between waste incineration and other heat and power plants by the waste share of the 1.A.1.a fuel use in the CRT (17–50 %, about 50 % in 2024). The waste part is counted in PR.SO-AT.AT, as recommended in chapter 1.4.1.2 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, and the rest (plants burning wood, oil and gas) is included here. The inventory does not split 1A1a NO<sub>x</sub> by fuel, so the split assumes the same NO<sub>x</sub> per TJ for waste and other fuels.
- NH<sub>3</sub> emissions from these categories are reported as zero or not occurring, and NH<sub>3</sub> from 1A1a is below 0.001 kt N/year, which is why there is no EF.EC NH<sub>3</sub> flow.

#### Data sources

- Emissions reported by Norway to the UN Convention on Long-range Transboundary Air Pollution (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The reported emissions are not measured but calculated in the national inventory, mainly as activity data (fuel consumption by fuel type and source category, from the national energy statistics) multiplied by emission factors, following the [EMEP/EEA Guidebook 2023](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023); for some large point sources, plant-specific reported emissions are used. The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).

#### Interpretations and comparisons

- Oil and gas extraction (1A1c, mainly gas turbines on offshore installations) dominates the flow: its NO<sub>x</sub> emissions rose from 7.6 kt N/year in 1990 to about 14.6 kt N in 2005–2015 with increasing petroleum production and have since fallen to 10.0 kt N in 2024.
- Refineries (1A1b) and fugitive emissions including flaring (1B2) contribute up to 0.3–0.6 kt N/year each.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-10-22). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, Manufacture of solid fuels and other energy industries (NFR 1A1c) | Inventory with published uncertainty | ±20 %, normal | 99% | 100% | 0.89 | 0.97 | none |

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
