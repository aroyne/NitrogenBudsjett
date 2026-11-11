---
layout: default
title: Manure Emissions (NH3)
parent: Manure Management (AG.MM)
nav_order: 3
---

# Manure Emissions (NH3)

<iframe src="../output_files/plots/AG_MM_AT_AT_Emissions_NH3.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.MM-AT.AT-Emissions-NH3** is ammonia from manure management (housing and storage), the categories 3B1a–3B4h in Table 29 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, and category 3I (other agriculture), which in Norway is NH<sub>3</sub> from ammonia treatment of straw used for feed.
- NH<sub>3</sub> from spreading manure and from grazing is counted in AG.SM-AT.AT-Emissions-NH3.

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The emissions are calculated in the national inventory with the same manure model as the greenhouse gas inventory: N in manure, mineral fertilizer and other N sources multiplied by NH<sub>3</sub> and NO<sub>x</sub> emission factors for each animal category, storage system, spreading method and fertilizer type. The methods are documented in the Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.

#### Assumptions

- The ammonia used for straw treatment is counted as an input to AG.MM in MP.OP-AG.MM-Ammonia for straw treatment-NH3: the 3I emission divided by the share of the ammonia that is emitted (54%; Miljødirektoratet, 2026, section 5.7.2)<!--cite:miljodirektoratet_iir_2026-->.

#### Interpretations

- The flow is about 9.4–11.8 kt N per year<!--range:AG.MM-AT.AT-Emissions-NH3:1990-2024-->: 10.3 kt N<!--val:AG.MM-AT.AT-Emissions-NH3:1990--> in 1990 and 9.9 kt N<!--val:AG.MM-AT.AT-Emissions-NH3:2024--> in 2024.
- Straw treatment (3I) contributed 1.2 kt N<!--val:nfr/3I/NH3:1990--> in 1990 but only 0.3 kt N<!--val:nfr/3I/NH3:2024--> in 2024, while manure management rose from about 9<!--val:nfr/3B1a+3B1b+3B2+3B3+3B4a+3B4d+3B4e+3B4f+3B4gi+3B4gii+3B4giii+3B4giv+3B4h/NH3:1990--> to 9.6 kt N<!--val:nfr/3B1a+3B1b+3B2+3B3+3B4a+3B4d+3B4e+3B4f+3B4gi+3B4gii+3B4giii+3B4giv+3B4h/NH3:2024-->.
- The peak in 2018 (11.8 kt N<!--val:AG.MM-AT.AT-Emissions-NH3:2018-->) comes from straw treatment, which rose to about 1.4 kt N<!--val:nfr/3I/NH3:2018--> in the drought year.
- Cattle account for about 70% (dairy cattle 3.0 kt N<!--val:nfr/3B1a/NH3:2024--> and other cattle 3.7 kt N<!--val:nfr/3B1b/NH3:2024--> in 2024).
- Emissions from other cattle, horses and poultry have increased, while emissions from dairy cattle, sheep and pigs have decreased.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NH<sub>3</sub>, manure management, all animal categories (NFR 3B) | Inventory with published uncertainty | ±25 %, normal | 82% | 99% | 0.86 | 0.97 | none |
| NH<sub>3</sub>, Agriculture other (please specify in the IIR) (NFR 3I) | Inventory with published uncertainty | −50/+100 %, lognormal | 18% | 1% | 0.14 | 0.03 | [Ammonia for Straw Treatment](../materials_and_products_pool/flow_MP_OP_AG_MM_Ammonia_for_straw_treatment_NH3.html) |

### References

* <span id="ref-emep_officially_2025" data-cite="EMEP" data-year="2025"></span>EMEP (2025). *Officially reported emission data*. [ceip.at](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* <span id="ref-miljodirektoratet_iir_2026" data-cite="Miljødirektoratet" data-year="2026"></span>Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
