---
layout: default
title: NOx emissions from soil management
parent: Soil Management (AG.SM)
nav_order: 5
---

# NOx emissions from soil management

<iframe src="../output_files/plots/AG_SM_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.SM-AT.AT-Emissions-NOx** is NO<sub>x</sub> from agricultural soils: the soil categories 3Da1–3Df in Table 30 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> and field burning of agricultural residues (3F).

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The emissions are calculated in the national inventory with the same manure model as the greenhouse gas inventory: N in manure, mineral fertilizer and other N sources multiplied by NH<sub>3</sub> and NO<sub>x</sub> emission factors for each animal category, storage system, spreading method and fertilizer type. The methods are documented in the Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.
- The LULUCF codes 4B1, 4B2, 4C1 and 4C2 in Table 30 are not reported in the CLRTAP inventory.

#### Assumptions

- The inventory counts all manure deposited by grazing animals as input to managed soils, including the share deposited on unmanaged land (utmark), which this model does not count as input to AG.SM (see AG.MM-AG.SM-Manure application-Nmix). The unmanaged-land share (26–30% of grazing manure, see AG.MM-AG.SM-Manure application-Nmix) of the emissions from grazing animals (3Da3) is therefore removed from this flow; it is counted in FS.OL-AT.AT-Emissions-NOx.

#### Interpretations

- The flow is about 2.0–2.5 kt N per year<!--range:AG.SM-AT.AT-Emissions-NOx:1990-2024-->.
- Field burning contributed 0.3 kt N<!--val:nfr/3F/NOx:1990--> in 1990 and less than 0.05 kt N in 2024.
- Mineral fertilizer (1.1 kt N<!--val:nfr/3Da1/NOx:2024--> in 2024) and manure spreading (0.65 kt N<!--val:nfr/3Da2a/NOx:2024-->) are the main sources.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, Inorganic N-fertilizers (includes also urea application) (NFR 3Da1) | Inventory with published uncertainty | −64.3/+180.1 %, lognormal | 92% | 89% | 0.57 | 0.56 | none |
| NO<sub>x</sub>, Animal manure applied to soils (NFR 3Da2a) | Inventory with published uncertainty | −50.4/+101.8 %, lognormal | 7% | 10% | 0.25 | 0.31 | none |

### References

* <span id="ref-emep_officially_2025" data-cite="EMEP" data-year="2025"></span>EMEP (2025). *Officially reported emission data*. [ceip.at](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* <span id="ref-miljodirektoratet_iir_2026" data-cite="Miljødirektoratet" data-year="2026"></span>Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
