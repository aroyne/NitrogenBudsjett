---
layout: default
title: Transport Fuel Import
parent: Rest of the world (RW)
nav_order: 7
---

# Transport Fuel Import

<iframe src="../output_files/plots/RW_RW_EF_TR_Import_of_transport_fuel_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-EF.TR-Import of transport fuel-Nmix** is the N in imported fuels for transport.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per fuel type from Table 15 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: motor and aviation gasoline 0% and jet fuel 0.1%.
- Only the commodity codes for transport fuels are included.

#### Interpretations

- The flow is small, below 0.5 kt N per year, since transport fuels contain little N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: jet fuel | N content of traded goods | ±50 %, triangular | 99% | 99% | 1.00 | 1.00 | [Export of transport fuels](../energy_and_fuels_pool/flow_EF_TR_RW_RW_Export_of_transport_fuels_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
