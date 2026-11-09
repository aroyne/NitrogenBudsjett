---
layout: default
title: Manure Emissions (NOx)
parent: Manure Management (AG.MM)
nav_order: 4
---

# Manure Emissions (NOx)

<iframe src="../output_files/plots/AG_MM_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.MM-AT.AT-Emissions-NOx** is NO<sub>x</sub> from manure management (housing and storage), the categories 3B1a–3B4h in Table 29 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, and 3I (other agriculture, ammonia treatment of straw), which reports no NO<sub>x</sub>.

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The emissions are calculated in the national inventory with the same manure model as the greenhouse gas inventory: N in manure, mineral fertilizer and other N sources multiplied by NH<sub>3</sub> and NO<sub>x</sub> emission factors for each animal category, storage system, spreading method and fertilizer type. The methods are documented in the Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.

#### Interpretations

- The flow is very small, about 0.03–0.04 kt N per year<!--range:AG.MM-AT.AT-Emissions-NOx:1990-2024-->.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, manure management, all animal categories (NFR 3B) | Inventory with published uncertainty | −50/+100 %, lognormal | 100% | 100% | 1.00 | 1.00 | none |

### References

* EMEP (2025). *Officially reported emission data*. [ceip.at](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
