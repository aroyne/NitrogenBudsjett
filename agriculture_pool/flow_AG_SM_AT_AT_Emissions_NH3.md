---
layout: default
title: NH3 emissions
parent: Soil Management (AG.SM)
nav_order: 4
---

# NH3 emissions

<iframe src="../output_files/plots/AG_SM_AT_AT_Emissions_NH3.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.SM-AT.AT-Emissions-NH3** is ammonia from agricultural soils: the soil categories 3Da1–3Df in Table 30 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> (mineral fertilizer, manure spreading, sewage sludge, other organic fertilizers, grazing animals and crop residues), and field burning of agricultural residues (3F), which the guidance names as an NH<sub>3</sub> source in its text but does not list in Table 30.

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The emissions are calculated in the national inventory with the same manure model as the greenhouse gas inventory: N in manure, mineral fertilizer and other N sources multiplied by NH<sub>3</sub> and NO<sub>x</sub> emission factors for each animal category, storage system, spreading method and fertilizer type. The methods are documented in the Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.
- The LULUCF codes 4B1, 4B2, 4C1 and 4C2 in Table 30 are not reported in the CLRTAP inventory, and 3Dd (off-farm storage and transport) is reported as zero.

#### Assumptions

- The inventory counts all manure deposited by grazing animals as input to managed soils, including the share deposited on unmanaged land (utmark), which this model does not count as input to AG.SM (see AG.MM-AG.SM-Manure application-Nmix). The unmanaged-land share (26–30% of grazing manure, see AG.MM-AG.SM-Manure application-Nmix) of the emissions from grazing animals (3Da3) is therefore removed from this flow; it is counted in FS.OL-AT.AT-Emissions-NH3.

#### Interpretations

- The flow is 13–15 kt N per year<!--range:AG.SM-AT.AT-Emissions-NH3:1990-2024-->, falling slowly from about 15.2 kt N<!--val:AG.SM-AT.AT-Emissions-NH3:1990--> in 1990 to 12.8 kt N<!--val:AG.SM-AT.AT-Emissions-NH3:2024--> in 2024.
- Field burning contributed 0.8 kt N in 1990 and less than 0.1 kt N in 2024.
- Manure spreading (3Da2a) is the largest source (10 kt N in 2024), followed by grazing animals on agricultural land (1.0 kt N) and mineral fertilizer (1.4 kt N, down from 2.1 kt N in 1990).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NH<sub>3</sub>, Animal manure applied to soils (NFR 3Da2a) | Inventory with published uncertainty | ±36 %, normal | 88% | 89% | 0.73 | 0.76 | none |
| NH<sub>3</sub>, Urine and dung deposited by grazing animals (NFR 3Da3) | Inventory with published uncertainty | −58/+138 %, lognormal | 6% | 7% | 0.07 | 0.08 | [Other Land Emissions (NH<sub>3</sub>)](../forests_and_semi_natural_pool/flow_FS_OL_AT_AT_Emissions_NH3.html) |
| NH<sub>3</sub>, Inorganic N-fertilizers (includes also urea application) (NFR 3Da1) | Inventory with published uncertainty | −33.3/+50 %, lognormal | 5% | 3% | 0.15 | 0.13 | none |

### References

* EMEP (2025). *Officially reported emission data*. [ceip.at](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
