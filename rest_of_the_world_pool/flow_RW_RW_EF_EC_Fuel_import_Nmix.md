---
layout: default
title: Fuel Import
parent: Rest of the world (RW)
nav_order: 6
---

# Fuel Import

<iframe src="../output_files/plots/RW_RW_EF_EC_Fuel_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Is taken from trade data, SSB table 08801 for all fuel items except those for transport. Unlike the export side of this flow, coal products (coking coal, bituminous coal, anthracite) dominate here rather than crude oil, since Norway imports comparatively little crude oil but relies on imported coal for coking and industrial use; the total flow is on the order of 19-28 ktN/year (2010-2024).

**How the numbers are derived**

- Import quantities (kg) by commodity code are taken from SSB's external trade statistics ([table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations, and multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.
- All fuel commodity codes except transport fuels are included.

**Interpretation**

- The flow is about 19–32 kt N per year, highest around 1999 and lowest around 2010, mainly following the import of coal and coke for industry.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
