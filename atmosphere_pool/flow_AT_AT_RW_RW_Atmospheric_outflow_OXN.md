---
layout: default
title: Atmospheric Outflow (Oxidized N)
parent: 7. Atmosphere (AT)
nav_order: 16
---

# Atmospheric Outflow (Oxidized N)

<iframe src="../output_files/plots/AT_AT_RW_RW_Atmospheric_outflow_OXN.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AT.AT-RW.RW-Atmospheric outflow-OXN** is the nitrogen emitted in Norway and deposited elsewhere in the EMEP domain.

#### Data sources

- The [EMEP source-receptor tables](https://emep.int/mscw/mscw_srdata.html) (EMEP, 2024<!--cite:emep_sr_2024-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: deposition in the EMEP domain from Norwegian emissions of nitrogen oxides, minus the part deposited in Norway, which is included in the national deposition flows (AT.AT-*-Deposition-OXN).
- 1997–2006 are from EMEP's recalculation of these years with one model version (2009); from 2007 each year is from the annual EMEP Status Report, calculated with the model version and meteorology of that year. The tables for 2019, 2020 and 2022–2024 are taken from Appendix C of the Status Reports, and the table files are compiled by data_files/emep_sr_norway.py.

#### Assumptions

- 2015 has no tables and is the mean of 2014 and 2016; 1984–1996 are the mean of 1997–2001.
- The change of EMEP model domain and version in 2007 gives a break in the deposition in Norway from foreign emitters (see RW.RW-AT.AT-Atmospheric inflow), but not in the deposition of Norwegian emissions abroad, so this flow is not corrected.

#### Interpretations and comparisons

- The flow is about 35–42 kt N per year up to 2021 and falls to 25 kt N in 2024, following lower Norwegian NOx emissions.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Transboundary deposition (EMEP source-receptor tables) | M2; calibration points | ±50 %, triangular | 75% | 100% | 1.00 | 1.00 | [Atmospheric Outflow (Reduced N)](../atmosphere_pool/flow_AT_AT_RW_RW_Atmospheric_outflow_RDN.html), [Atmospheric Inflow (Oxidized N)](../rest_of_the_world_pool/flow_RW_RW_AT_AT_Atmospheric_inflow_OXN.html), [Atmospheric Inflow (Reduced N)](../rest_of_the_world_pool/flow_RW_RW_AT_AT_Atmospheric_inflow_RDN.html) |
| Held constant or averaged (None-1997) | Gap filling: held constant or averaged | ±25–45 %, lognormal, grows with distance to known year | 25% | – | 1.00 | – | none |

### References

* EMEP (2024). *SR country tables*. [https://www.emep.int/mscw/mscw_srdata.html](https://www.emep.int/mscw/mscw_srdata.html)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
