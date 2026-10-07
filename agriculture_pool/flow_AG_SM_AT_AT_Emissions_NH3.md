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

- **AG.SM-AT.AT-Emissions-NH3** is ammonia from agricultural soils: the soil categories 3Da1–3Df in Table 30 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> (mineral fertilizer, manure spreading, sewage sludge, other organic fertilizers, grazing animals and crop residues), and field burning of agricultural residues (3F), which the guidance names as an NH3 source in its text but does not list in Table 30.

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The emissions are calculated in the national inventory with the same manure model as the greenhouse gas inventory: N in manure, mineral fertilizer and other N sources multiplied by NH3 and NOx emission factors for each animal category, storage system, spreading method and fertilizer type. The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).
- The LULUCF codes 4B1, 4B2, 4C1 and 4C2 in Table 30 are not reported in the CLRTAP inventory, and 3Dd (off-farm storage and transport) is reported as zero.
- The inventory counts all manure deposited by grazing animals as input to managed soils, including the share deposited on utmark (unmanaged land), which this model does not count as input to AG.SM (see AG.MM-AG.SM-Manure application-Nmix).

#### Assumptions

- The utmark share (35–39% of grazing manure, see AG.MM-AG.SM-Manure application-Nmix) of the emissions from grazing animals (3Da3) is therefore removed from this flow; it is counted in FS.OL-AT.AT-Emissions-NH3.

#### Interpretations and comparisons

- The flow is 13–15 kt N per year, falling slowly from about 15.2 kt N in 1990 to 12.8 kt N in 2024.
- Field burning contributed 0.8 kt N in 1990 and less than 0.1 kt N in 2024.
- Manure spreading (3Da2a) is the largest source (10 kt N in 2024), followed by grazing animals on innmark (0.9 kt N) and mineral fertilizer (1.4 kt N, down from 2.1 kt N in 1990).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
