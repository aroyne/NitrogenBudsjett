---
layout: default
title: Fuel Import
parent: Rest of the world (RW)
nav_order: 6
---

# Fuel Import

<iframe src="../output_files/plots/RW_RW_EF_EC_Fuel_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-EF.EC-Fuel import-Nmix** is the N in imported fuels, all fuel items except those for transport.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.
- All fuel commodity codes except transport fuels are included.

#### Interpretations and comparisons

- The flow is about 19–32 kt N per year, highest around 1999 and lowest around 2010, and about 19–28 kt N per year in 2010–2024.
- Unlike the export side, coal products (coking coal, bituminous coal, anthracite) dominate here rather than crude oil, since Norway imports comparatively little crude oil but relies on imported coal for coking and industrial use.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
