---
layout: default
title: Export of transport fuels
parent: Transportation (EF.TR)
nav_order: 4
---

# Export of transport fuels

<iframe src="../output_files/plots/EF_TR_RW_RW_Export_of_transport_fuels_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
EF.TR-RW.RW-Export of transport fuels-Nmix is export of fuels for transport. We use trade data in SSB table 08801 to account for all petroleum products assumed to be used in the transport sector..

**How the numbers are derived**

- Export quantities (kg) by HS commodity code are taken from [SSB table 08801](https://www.ssb.no/statbank/table/08801) and multiplied by an N content from Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf).
- The flow covers motor and aviation gasoline (0% N) and jet fuel (jet gasoline and jet kerosene, 0.1% N); the HS codes are defined in the trade mapping sheet of N_parameters.xlsx.
- Naphtha, which is mainly a petrochemical feedstock, is counted in EF.EC-RW.RW-Fuel export.
- Export quantities are registered by customs and are observed rather than modelled.
- Since gasoline has no fuel-bound nitrogen, the flow is small (below 0.5 kt N per year) and consists of jet fuel exports.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
