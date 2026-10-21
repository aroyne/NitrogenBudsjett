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

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Atmospheric deposition (NILU, Blake et al. 2023) | Inventory with published uncertainty | −70/+30 % (min–max), triangular | 100% | 67% | 1.00 | 1.00 | [Oxidized N Deposition (Agricultural Soils)](../atmosphere_pool/flow_AT_AT_AG_SM_Deposition_OXN.html), [Reduced N Deposition (Agricultural Soils)](../atmosphere_pool/flow_AT_AT_AG_SM_Deposition_RDN.html), [Oxidized N Deposition (Forest)](../atmosphere_pool/flow_AT_AT_FS_FO_Deposition_OXN.html), [Reduced N Deposition (Forest)](../atmosphere_pool/flow_AT_AT_FS_FO_Deposition_RDN.html) and 5 more |
| Extrapolation (2016+) | Gap filling: extrapolation | ±30–35 %, lognormal, grows with distance to known year | – | 25% | – | 1.00 | none |
| Held constant or averaged (2021+) | Gap filling: held constant or averaged | ±15–25 %, lognormal, grows with distance to known year | – | 8% | – | 1.00 | none |

### References

* Blake, L. R., Aas, W., Denby, B., Hjellbrekke, A., Mu, Q., Simpson, D., & Fagerli, H. (2023). *Deposition of sulfur and nitrogen in Norway 2017-2021*.
