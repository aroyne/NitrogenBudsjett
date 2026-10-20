---
layout: default
title: Industrial Emissions (NOx)
parent: Other Producing Industry (MP.OP)
nav_order: 4
---

# Industrial Emissions (NOx)

<iframe src="../output_files/plots/MP_OP_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-AT.AT-Emissions-NOx** is NOx from industrial processes. The flow sums the NFR categories in Table 20 of Schäppi et al. (2025): 2A Mineral industry, 2B Chemical industry, 2C Metal production, 2D Non-energy products from fuels and solvent use, 2G Other product use and 2H Other, which Norway reports at sub-category level (e.g. 2B2, 2C2).
- Emissions from fuel combustion in industry are not included here but in EF.IC-AT.AT-Emissions-NOx.

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- For industrial processes the inventory emissions are largely based on emissions reported by the individual plants to Miljødirektoratet, supplemented by production data multiplied by emission factors from the [EMEP/EEA Guidebook 2023](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023). The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).

#### Interpretations and comparisons

- The flow falls from about 4.2 kt N in 1990 to 2.5 kt N in 2024.
- Ferroalloy production (2C2) is the largest source (2.8–3.0 kt N until 2005, 1.9 kt N in 2024), followed by aluminium production (2C3, about 0.3 kt N).
- NOx from nitric acid production (2B2) fell from 0.7 kt N in 1990 to 0.1 kt N in 2024, and from pulp and paper (2H1) from 0.24 to 0.09 kt N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NOx, Ferroalloys production (NFR 2C2) | Inventory with published uncertainty | ±20 %, normal | 69% | 73% | 0.71 | 0.76 | none |
| NOx, Aluminium production (NFR 2C3) | Inventory with published uncertainty | −50/+100 %, lognormal | 5% | 21% | 0.05 | 0.11 | none |
| NOx, Nitric acid production (NFR 2B2) | Inventory with published uncertainty | −42.9/+75 %, lognormal | 18% | 4% | 0.12 | 0.06 | none |
| NOx, Pulp and paper industry (NFR 2H1) | Inventory with published uncertainty | −50/+100 %, lognormal | 8% | 2% | 0.06 | 0.03 | none |

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
