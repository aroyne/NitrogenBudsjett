---
layout: default
title: Transport Fuel Import
parent: Rest of the world (RW)
nav_order: 7
---

# Transport Fuel Import

<iframe src="../output_files/plots/RW_RW_EF_TR_Import_of_transport_fuel_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Is taken from trade data, SSB table 08801 for all fuel items for transport.

**How the numbers are derived**

- Import quantities (kg) by commodity code are taken from SSB's external trade statistics ([table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations, and multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.
- Only the commodity codes for transport fuels are included.

**Interpretation**

- The flow is small, below 0.5 kt N per year, since transport fuels contain little N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
