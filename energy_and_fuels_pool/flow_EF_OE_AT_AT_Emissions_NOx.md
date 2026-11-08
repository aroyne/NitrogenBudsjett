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

- **EF.OE-AT.AT-Emissions-NOx** is NO<sub>x</sub> from fuel combustion in residential, commercial and other sectors that are not already covered, using the categories given in Table 14 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Data sources

- Emissions reported by Norway to the UN Convention on Long-range Transboundary Air Pollution (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The reported emissions are not measured but calculated in the national inventory, mainly as activity data (fuel consumption by fuel type and source category, from the national energy statistics) multiplied by emission factors, following the EMEP/EEA Guidebook (European Environment Agency, 2023)<!--cite:eea_guidebook_2023-->; for some large point sources, plant-specific reported emissions are used. The methods are documented in the Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.

#### Interpretations

- NO<sub>x</sub> emissions declined from about 9.1 kt N/year<!--mean:EF.OE-AT.AT-Emissions-NOx:1990-1999--> in the 1990s to about 5.5 kt N<!--val:EF.OE-AT.AT-Emissions-NOx:2024--> in 2024.
- The largest source is national fishing (1A4ciii), with 3.7–5.2 kt N/year<!--range:nfr/1A4ciii/NOx:1990-2000--> until 2000 and 1.7 kt N<!--val:nfr/1A4ciii/NOx:2024--> in 2024, reflecting a smaller and more modern fishing fleet and NO<sub>x</sub>-reducing measures.
- Other important sources are commercial and household mobile machinery (1A4aii, 1A4bii), agricultural and forestry machinery (1A4cii) and other mobile sources including military and recreational boats (1A5b).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, Agriculture/Forestry/Fishing: National fishing (NFR 1A4ciii) | Inventory with published uncertainty | −32.8/+48.7 %, lognormal | 72% | 64% | 0.42 | 0.37 | none |
| NO<sub>x</sub>, Commercial/institutional: Mobile (NFR 1A4aii) | Inventory with published uncertainty | −30.9/+44.7 %, lognormal | 17% | 17% | 0.22 | 0.20 | none |
| NO<sub>x</sub>, Residential: Household and gardening (mobile) (NFR 1A4bii) | Inventory with published uncertainty | −29.1/+41.1 %, lognormal | 1% | 7% | 0.07 | 0.14 | none |
| NO<sub>x</sub>, Other, Mobile (including military, land based and recreational boats) (NFR 1A5b) | Inventory with published uncertainty | ±30.4 %, normal | 3% | 5% | 0.12 | 0.13 | none |
| NO<sub>x</sub>, Residential: Stationary (NFR 1A4bi) | Inventory with published uncertainty | −43.8/+77.9 %, lognormal | 3% | 4% | 0.06 | 0.06 | none |
| NO<sub>x</sub>, Agriculture/Forestry/Fishing: Off-road vehicles and other machinery (NFR 1A4cii) | Inventory with published uncertainty | −29.2/+41.2 %, lognormal | 3% | 2% | 0.10 | 0.08 | none |

### References

* European Environment Agency (2023). *EMEP/EEA air pollutant emission inventory guidebook 2023* (EMEP/EEA joint report 06/2023). [eea.europa.eu](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023)
* EMEP (2025). *Officially reported emission data*. [ceip.at](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
