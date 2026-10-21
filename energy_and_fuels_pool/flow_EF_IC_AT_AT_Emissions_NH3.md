---
layout: default
title: Industrial emissions (NH3)
parent: Manufacturing industries and construction (EF.IC)
nav_order: 2
---

# Industrial emissions (NH3)

<iframe src="../output_files/plots/EF_IC_AT_AT_Emissions_NH3.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.IC-AT.AT-Emissions-NH3** is ammonia from fuel combustion in industry, using the categories given in Table 12 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Data sources

- Emissions reported by Norway to the UN Convention on Long-range Transboundary Air Pollution (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The reported emissions are not measured but calculated in the national inventory, mainly as activity data (fuel consumption by fuel type and source category, from the national energy statistics) multiplied by emission factors, following the [EMEP/EEA Guidebook 2023](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023); for some large point sources, plant-specific reported emissions are used. The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).

#### Interpretations and comparisons

- NH3 emissions from fuel combustion in industry are very small (about 0.008 kt N/year), mainly from combustion of biomass and other fuels in 1A2d (pulp, paper and print) and 1A2gviii (other stationary combustion).
- NH3 is not a significant product of combustion except where biomass or catalytic NOx reduction is involved.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NH3, Mobile Combustion in manufacturing the IIR) (NFR 1A2gvii) | Inventory with published uncertainty | −50/+100 %, lognormal | 40% | 64% | 0.16 | 0.21 | none |
| NH3, Stationary combustion in manufacturing specify in the IIR) (NFR 1A2gviii) | Inventory with published uncertainty | ±24 %, normal | 47% | 24% | 0.54 | 0.39 | none |
| NH3, Stationary combustion in manufacturing Print (NFR 1A2d) | Inventory with published uncertainty | ±24 %, normal | 13% | 11% | 0.30 | 0.29 | none |

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
