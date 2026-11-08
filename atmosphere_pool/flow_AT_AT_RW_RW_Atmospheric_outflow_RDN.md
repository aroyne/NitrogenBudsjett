---
layout: default
title: Atmospheric Outflow (Reduced N)
parent: 7. Atmosphere (AT)
nav_order: 17
---

# Atmospheric Outflow (Reduced N)

<iframe src="../output_files/plots/AT_AT_RW_RW_Atmospheric_outflow_RDN.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AT.AT-RW.RW-Atmospheric outflow-RDN** is the nitrogen emitted in Norway and deposited elsewhere in the EMEP domain.

#### Data sources

- The [EMEP source-receptor tables](https://emep.int/mscw/mscw_srdata.html) (EMEP, 2024<!--cite:emep_sr_2024-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: deposition in the EMEP domain from Norwegian emissions of ammonia, minus the part deposited in Norway, which is included in the national deposition flows (AT.AT-*-Deposition-RDN).
- 1997–2006 are from EMEP's recalculation of these years with one model version (2009); from 2007 each year is from the annual EMEP Status Report, calculated with the model version and meteorology of that year. The tables for 2019, 2020 and 2022–2024 are taken from Appendix C of the Status Reports, and the table files are compiled by data_files/emep_sr_norway.py.

#### Assumptions

- 2015 has no tables and is the mean of 2014 and 2016; 1984–1996 are the mean of 1997–2001.
- The change of EMEP model domain and version in 2007 gives a break in the deposition in Norway from foreign emitters (see RW.RW-AT.AT-Atmospheric inflow), but not in the deposition of Norwegian emissions abroad, so this flow is not corrected.

#### Interpretations

- The flow is about 10–12 kt N per year up to 2016 and 13–14 kt N since, much less than for oxidised N since ammonia is mainly deposited close to the source.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Transboundary deposition (EMEP source-receptor tables) | M2; calibration points | ±50 %, triangular | 75% | 100% | 1.00 | 1.00 | [Atmospheric Outflow (Oxidized N)](../atmosphere_pool/flow_AT_AT_RW_RW_Atmospheric_outflow_OXN.html), [Atmospheric Inflow (Oxidized N)](../rest_of_the_world_pool/flow_RW_RW_AT_AT_Atmospheric_inflow_OXN.html), [Atmospheric Inflow (Reduced N)](../rest_of_the_world_pool/flow_RW_RW_AT_AT_Atmospheric_inflow_RDN.html) |
| Held constant or averaged (before 1997) | Gap filling: held constant or averaged | ±25–45 %, lognormal, grows with distance to known year | 25% | – | 1.00 | – | none |

### References

* EMEP (2024). *SR country tables*. [emep.int](https://www.emep.int/mscw/mscw_srdata.html)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
