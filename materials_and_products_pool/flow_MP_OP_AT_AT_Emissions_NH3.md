---
layout: default
title: Industrial Emissions (NH3)
parent: Other Producing Industry (MP.OP)
nav_order: 3
---

# Industrial Emissions (NH3)

<iframe src="../output_files/plots/MP_OP_AT_AT_Emissions_NH3.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-AT.AT-Emissions-NH3** is ammonia from industrial processes. The flow sums the NFR categories in Table 20 of Schäppi et al. (2025): 2A Mineral industry, 2B Chemical industry, 2C Metal production, 2D Non-energy products from fuels and solvent use, 2G Other product use and 2H Other, which Norway reports at sub-category level (e.g. 2B2, 2C2).

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- For industrial processes the inventory emissions are largely based on emissions reported by the individual plants to Miljødirektoratet, supplemented by production data multiplied by emission factors from the [EMEP/EEA Guidebook 2023](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023). The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).

#### Interpretations and comparisons

- The flow is about 0.4–0.6 kt N per year without a clear trend.
- Nitric acid production (2B2) accounts for about 0.4 kt N, and the rest comes mainly from glass production (2A3) and other mineral products (2A6).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NH3, Glass production (NFR 2A3) | Inventory with published uncertainty | −69.9/+232 %, lognormal | 26% | 60% | 0.07 | 0.13 | none |
| NH3, Other mineral products (please specify in the IIR) (NFR 2A6) | Inventory with published uncertainty | −68.2/+214 %, lognormal | 60% | 32% | 0.11 | 0.10 | none |
| NH3, Nitric acid production (NFR 2B2) | Inventory with published uncertainty | ±10 %, normal | 12% | 8% | 0.72 | 0.74 | none |

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
