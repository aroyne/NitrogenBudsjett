---
layout: default
title: Oxidized N Deposition (Forest)
parent: 7. Atmosphere (AT)
nav_order: 4
---

# Oxidized N Deposition (Forest)

<iframe src="../output_files/plots/AT_AT_FS_FO_Deposition_OXN.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AT.AT-FS.FO-Deposition-OXN** is deposition of oxidised N to forest, one of five land-class deposition flows derived from the same NILU/AR5 dataset; see the [Atmospheric Nitrogen Deposition Overview](pool_atmosphere.html) on the 7. Atmosphere (AT) pool page for the shared methodology, period structure and national totals.

#### Data sources

- NILU's gridded deposition for each five-year period from 1983–1987 to 2012–2016 (Blake et al., 2023<!--cite:blake_deposition_2023-->), distributed on land-cover classes with the NIBIO AR5 map.

#### Assumptions

- Each year gets the value of its five-year period, so the series changes in steps.
- 2017–2021 is the 2012–2016 value scaled by the national change since 2015 in observed (kriging) deposition in Blake et al. (2023)<!--cite:blake_deposition_2023-->, −10% for oxidised and −17% for reduced N, and later years are held at the 2017–2021 value.

#### Interpretations and comparisons

- The flow falls from about 39 kt N in 1984–1987 to 28 kt N around 2000 and 22–23 kt N from 2017.
- The steps follow the five-year periods of the NILU data; the decline reflects lower emissions in Europe, more for oxidised than for reduced N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
