---
layout: default
title: Other energy emissions (NOx)
parent: Other energy and fuels (EF.OE)
nav_order: 3
---

# Other energy emissions (NOx)

<iframe src="../output_files/plots/EF_OE_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.OE-AT.AT-Emissions-NOx** is NOx from fuel combustion in residential, commercial and other sectors that are not already covered, using the categories given in Table 14 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Data sources

- Emissions reported by Norway to the UN Convention on Long-range Transboundary Air Pollution (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The reported emissions are not measured but calculated in the national inventory, mainly as activity data (fuel consumption by fuel type and source category, from the national energy statistics) multiplied by emission factors, following the [EMEP/EEA Guidebook 2023](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023); for some large point sources, plant-specific reported emissions are used. The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).

#### Interpretations and comparisons

- NOx emissions declined from about 9.1 kt N/year in the 1990s to about 5.5 kt N in 2024.
- The largest source is national fishing (1A4ciii), with 3.7–5.2 kt N/year until 2000 and 1.7 kt N in 2024, reflecting a smaller and more modern fishing fleet and NOx-reducing measures.
- Other important sources are commercial and household mobile machinery (1A4aii, 1A4bii), agricultural and forestry machinery (1A4cii) and other mobile sources including military and recreational boats (1A5b).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NOx, Agriculture/Forestry/Fishing: National fishing (NFR 1A4ciii) | Inventory with published uncertainty | −32.8/+48.7 %, lognormal | 72% | 64% | 0.42 | 0.37 | none |
| NOx, Commercial/institutional: Mobile (NFR 1A4aii) | Inventory with published uncertainty | −30.9/+44.7 %, lognormal | 17% | 17% | 0.22 | 0.20 | none |
| NOx, Residential: Household and gardening (mobile) (NFR 1A4bii) | Inventory with published uncertainty | −29.1/+41.1 %, lognormal | 1% | 7% | 0.07 | 0.14 | none |
| NOx, Other, Mobile (including military, land based and recreational boats) (NFR 1A5b) | Inventory with published uncertainty | ±30.4 %, normal | 3% | 5% | 0.12 | 0.13 | none |
| NOx, Residential: Stationary (NFR 1A4bi) | Inventory with published uncertainty | −43.8/+77.9 %, lognormal | 3% | 4% | 0.06 | 0.06 | none |
| NOx, Agriculture/Forestry/Fishing: Off-road vehicles and other machinery (NFR 1A4cii) | Inventory with published uncertainty | −29.2/+41.2 %, lognormal | 3% | 2% | 0.10 | 0.08 | none |

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
