---
layout: default
title: Atmospheric Inflow (Oxidized N)
parent: Rest of the world (RW)
nav_order: 4
---

# Atmospheric Inflow (Oxidized N)

<iframe src="../output_files/plots/RW_RW_AT_AT_Atmospheric_inflow_OXN.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-AT.AT-Atmospheric inflow-OXN** is the oxidised nitrogen emitted outside Norway and deposited in Norway.

#### Data sources

- The [EMEP source-receptor tables](https://emep.int/mscw/mscw_srdata.html), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: deposition of oxidised nitrogen in Norway from all emitters, including ships and natural sources, minus the deposition from Norwegian emissions.
- 1997–2006 are from EMEP's recalculation of these years with one model version (2009); from 2007 each year is from the annual EMEP Status Report, calculated with the model version and meteorology of that year. The tables for 2019, 2020 and 2022–2024 are taken from Appendix C of the Status Reports, and the table files are compiled by data_files/emep_sr_norway.py.
- From 2007 EMEP uses an extended model domain and a newer model version. In the tables, deposition in Norway from foreign emitters roughly halves from 2006 to 2007, with a 40–70% drop for each of the main emitter countries, while Norway's own deposition and the deposition of Norwegian emissions abroad are almost unchanged.

#### Assumptions

- The values for 1997–2006 (and hence 1984–1996) are scaled to the level of the later tables by the ratio of the means for 2007–2009 and 2004–2006, which is 0.59. Without this correction the flow would be about twice as high before 2007.
- 2015 has no tables and is the mean of 2014 and 2016; 1984–1996 are the mean of 1997–2001.

#### Interpretations and comparisons

- The flow is about 28–39 kt N per year with large year-to-year variation from the meteorology, and a weak decline after 2016.
- Inflow plus the deposition of Norwegian emissions in Norway is 52–72% of the oxidised N deposition in the NILU data used for the deposition flows, which are based on measurements (see the [Atmospheric Nitrogen Deposition Overview](../atmosphere_pool/pool_atmosphere.html)); Blake et al. (2023)<!--cite:blake_deposition_2023--> also find EMEP model deposition well below the kriging estimates.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Blake, L. R., Aas, W., Denby, B., Hjellbrekke, A., Mu, Q., Simpson, D., & Fagerli, H. (2023). *Deposition of sulfur and nitrogen in Norway 2017-2021*.
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
