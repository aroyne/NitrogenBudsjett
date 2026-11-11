---
layout: default
title: Industrial emissions (NOx)
parent: Manufacturing industries and construction (EF.IC)
nav_order: 3
---

# Industrial emissions (NOx)

<iframe src="../output_files/plots/EF_IC_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.IC-AT.AT-Emissions-NOx** is NO<sub>x</sub> from fuel combustion in industry, using the categories given in Table 12 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Data sources

- Emissions reported by Norway to the UN Convention on Long-range Transboundary Air Pollution (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The reported emissions are not measured but calculated in the national inventory, mainly as activity data (fuel consumption by fuel type and source category, from the national energy statistics) multiplied by emission factors, following the EMEP/EEA Guidebook (European Environment Agency, 2023)<!--cite:eea_guidebook_2023-->; for some large point sources, plant-specific reported emissions are used. The methods are documented in the Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.

#### Interpretations

- NO<sub>x</sub> emissions from industry and construction fell from about 5.5–6.4 kt N/year<!--range:EF.IC-AT.AT-Emissions-NOx:1990-1999--> in the 1990s to about 2.4 kt N<!--val:EF.IC-AT.AT-Emissions-NOx:2024--> in 2024.
- The largest source is mobile machinery in construction and industry (1A2gvii, 2.5–3.7 kt N/year<!--range:nfr/1A2gvii/NOx:1990-1999--> in the 1990s, 1.2 kt N<!--val:nfr/1A2gvii/NOx:2024--> in 2024), where the decline follows the gradual replacement of machinery under the EU emission standards for non-road mobile machinery.
- Emissions from non-metallic minerals (1A2f, e.g. cement kilns) and pulp and paper (1A2d) have also fallen substantially, while emissions from iron and steel (1A2a) increased after 2010.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, Mobile Combustion in manufacturing the IIR) (NFR 1A2gvii) | Inventory with published uncertainty | −36.3/+57.1 %, lognormal | 97% | 97% | 0.50 | 0.48 | none |

### References

* <span id="ref-eea_guidebook_2023" data-cite="European Environment Agency" data-year="2023"></span>European Environment Agency (2023). *EMEP/EEA air pollutant emission inventory guidebook 2023* (EMEP/EEA joint report 06/2023). [eea.europa.eu](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023)
* <span id="ref-emep_officially_2025" data-cite="EMEP" data-year="2025"></span>EMEP (2025). *Officially reported emission data*. [ceip.at](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* <span id="ref-miljodirektoratet_iir_2026" data-cite="Miljødirektoratet" data-year="2026"></span>Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
