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

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.
- Only the commodity codes for transport fuels are included.

#### Interpretations and comparisons

- The flow is small, below 0.5 kt N per year, since transport fuels contain little N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
