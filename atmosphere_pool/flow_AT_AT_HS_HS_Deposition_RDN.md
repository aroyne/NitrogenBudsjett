---
layout: default
title: Reduced N Deposition (Settlements)
parent: 7. Atmosphere (AT)
nav_order: 11
---

# Reduced N Deposition (Settlements)

<iframe src="../output_files/plots/AT_AT_HS_HS_Deposition_RDN.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AT.AT-HS.HS-Deposition-RDN** is deposition of reduced N to settlements, one of five land-class deposition flows derived from the same NILU/AR5 dataset; see the [Atmospheric Nitrogen Deposition Overview](pool_atmosphere.html) on the 7. Atmosphere (AT) pool page for the shared methodology, period structure and national totals.

#### Data sources

- NILU's gridded deposition for each five-year period from 1983–1987 to 2012–2016 (Blake et al., 2023<!--cite:blake_deposition_2023-->), distributed on land-cover classes with the NIBIO AR5 map.

#### Assumptions

- Each year gets the value of its five-year period, so the series changes in steps.
- 2017–2021 is the 2012–2016 value scaled by the national change since 2015 in observed (kriging) deposition in Blake et al. (2023)<!--cite:blake_deposition_2023-->, −10% for oxidised and −17% for reduced N, and later years are held at the 2017–2021 value.

#### Interpretations and comparisons

- The flow falls from about 2.5 kt N in 1984–1987 to 1.3–1.4 kt N from 2017.
- The steps follow the five-year periods of the NILU data; the decline reflects lower emissions in Europe, more for oxidised than for reduced N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Blake, L. R., Aas, W., Denby, B., Hjellbrekke, A., Mu, Q., Simpson, D., & Fagerli, H. (2023). *Deposition of sulfur and nitrogen in Norway 2017-2021*.
