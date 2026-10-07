---
layout: default
title: Export of transport fuels
parent: Transportation (EF.TR)
nav_order: 4
---

# Export of transport fuels

<iframe src="../output_files/plots/EF_TR_RW_RW_Export_of_transport_fuels_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.TR-RW.RW-Export of transport fuels-Nmix** is the export of fuels assumed to be used in the transport sector: motor and aviation gasoline and jet fuel (jet gasoline and jet kerosene).
- Naphtha, which is mainly a petrochemical feedstock, is counted in EF.EC-RW.RW-Fuel export.

#### Data sources

- Export quantities (kg) by HS commodity code from [SSB table 08801](https://www.ssb.no/statbank/table/08801), registered by customs and therefore observed rather than modelled.
- N contents from Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- Motor and aviation gasoline 0% N, jet fuel 0.1% N; the HS codes are defined in the trade mapping sheet of N_parameters.xlsx.

#### Interpretations and comparisons

- Since gasoline has no fuel-bound nitrogen, the flow is small (below 0.5 kt N per year) and consists of jet fuel exports.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
