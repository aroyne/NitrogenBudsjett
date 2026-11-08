---
layout: default
title: Ammonia for Straw Treatment
parent: Other Producing Industry (MP.OP)
nav_order: 14
---

# Ammonia for Straw Treatment

<iframe src="../output_files/plots/MP_OP_AG_MM_Ammonia_for_straw_treatment_NH3.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-AG.MM-Ammonia for straw treatment-NH3** is ammonia used to treat straw so that it can be used as feed. This flow is not in the flow tables of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- About half of the ammonia is emitted after the treatment and is part of AG.MM-AT.AT-Emissions-NH3 (NFR 3I); the rest is bound in the straw and eaten by the animals.

#### Data sources

- NH<sub>3</sub> emissions from straw treatment (NFR 3I) reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->).
- The inventory calculates these emissions as the amount of ammonia used for straw treatment (from Budsjettnemnda for jordbruket's Totalkalkylen) times the share that is not bound in the straw, 54% (European Environment Agency, 2023)<!--cite:eea_guidebook_2023-->, as described in section 5.7.2 of Norway's Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.

#### Assumptions

- The ammonia used is the emission divided by the emitted share, 0.54 (range 0.40–0.70, triangular; the range is our assumption).

#### Interpretations

- The flow is 1.8–3.2 kt N per year<!--range:MP.OP-AG.MM-Ammonia for straw treatment-NH3:1990-1997--> in 1990–1997, falls to 0.3–1.2 kt N from 2000, and has a peak of 2.6 kt N<!--val:MP.OP-AG.MM-Ammonia for straw treatment-NH3:2018--> in 2018, when more straw was treated to make up for the poor grass harvest in the drought summer.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NH<sub>3</sub>, Agriculture other (please specify in the IIR) (NFR 3I) | Inventory with published uncertainty | −50/+100 %, lognormal | 89% | 89% | 1.00 | 1.00 | [Manure Emissions (NH<sub>3</sub>)](../agriculture_pool/flow_AG_MM_AT_AT_Emissions_NH3.html) |
| Share of straw-treatment ammonia emitted | Parameter | 0.4–0.7, triangular | 11% | 11% | −0.91 | −0.91 | none |

### References

* European Environment Agency (2023). *EMEP/EEA air pollutant emission inventory guidebook 2023* (EMEP/EEA joint report 06/2023). [eea.europa.eu](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023)
* EMEP (2025). *Officially reported emission data*. [ceip.at](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
