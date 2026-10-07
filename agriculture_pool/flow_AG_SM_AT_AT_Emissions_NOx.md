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

- **AG.SM-AT.AT-Emissions-NOx** is NOx from agricultural soils: the soil categories 3Da1–3Df in Table 30 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> and field burning of agricultural residues (3F).

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The emissions are calculated in the national inventory with the same manure model as the greenhouse gas inventory: N in manure, mineral fertilizer and other N sources multiplied by NH3 and NOx emission factors for each animal category, storage system, spreading method and fertilizer type. The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).
- The LULUCF codes 4B1, 4B2, 4C1 and 4C2 in Table 30 are not reported in the CLRTAP inventory.
- The inventory counts all manure deposited by grazing animals as input to managed soils, including the share deposited on utmark (unmanaged land), which this model does not count as input to AG.SM (see AG.MM-AG.SM-Manure application-Nmix).

#### Assumptions

- The utmark share (26–33% of grazing manure, see AG.MM-AG.SM-Manure application-Nmix) of the emissions from grazing animals (3Da3) is therefore removed from this flow; it is counted in FS.OL-AT.AT-Emissions-NOx.

#### Interpretations and comparisons

- The flow is about 2.0–2.5 kt N per year.
- Field burning contributed 0.3 kt N in 1990 and less than 0.05 kt N in 2024.
- Mineral fertilizer (1.1 kt N in 2024) and manure spreading (0.65 kt N) are the main sources.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
