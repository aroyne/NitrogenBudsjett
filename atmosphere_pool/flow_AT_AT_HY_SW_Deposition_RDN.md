---
layout: default
title: Reduced N Deposition (Surface Water)
parent: 7. Atmosphere (AT)
nav_order: 13
---

# Reduced N Deposition (Surface Water)

<iframe src="../output_files/plots/AT_AT_HY_SW_Deposition_RDN.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**AT.AT-HY.SW-Deposition-RDN**

Deposition of N to surface waters is one of five land-class deposition flows derived from the same NILU/AR5 dataset; see the [Atmospheric Nitrogen Deposition Overview](pool_atmosphere.html) on the 7. Atmosphere (AT) pool page for the shared methodology, period structure and national totals.

For comparison, the data used in the TEOTIL model gives 3.5 ktN in 2013 and 3.0 ktN in 2023 - a similar declining trend to our combined OXN+RDN values (about 9.4 and 8.1 ktN for the same years), but substantially lower in magnitude, likely reflecting different datasets and different data treatment. 

**How the numbers are derived**

- NILU's gridded deposition for each five-year period from 1983–1987 to 2012–2016 (Blake et al., 2023) is distributed on land-cover classes with the AR5 map; see the [Atmospheric Nitrogen Deposition Overview](pool_atmosphere.html).
- Each year gets the value of its five-year period, so the series changes in steps. 2017–2021 is the 2012–2016 value scaled by the national change since 2015 in observed (kriging) deposition in Blake et al. (2023), −10% for oxidised and −17% for reduced N, and later years are held at the 2017–2021 value.

**Interpretation**

- The flow falls from about 5.8 kt N in 1984–1987 to 3.7–3.8 kt N from 2017.
- The steps follow the five-year periods of the NILU data; the decline reflects lower emissions in Europe, more for oxidised than for reduced N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
