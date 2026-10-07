---
layout: default
title: Atmospheric Outflow (Oxidized N)
parent: 7. Atmosphere (AT)
nav_order: 16
---

# Atmospheric Outflow (Oxidized N)

<iframe src="../output_files/plots/AT_AT_RW_RW_Atmospheric_outflow_OXN.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**AT.AT-RW.RW-Atmospheric outflow-OXN**

is the nitrogen emitted in Norway and deposited elsewhere in the EMEP domain, found using source-receptor data from (EMEP, 2024)<!--cite:emep_sr_2024-->, as advised by (Schäppi et al., 2025)<!--cite:schappi_annexes_2025-->.

**How the numbers are derived**

- From the [EMEP source-receptor tables](https://emep.int/mscw/mscw_srdata.html): deposition in the EMEP domain from Norwegian emissions of nitrogen oxides, minus the part deposited in Norway, which is included in the national deposition flows (AT.AT-*-Deposition-OXN).
- 1997–2006 are from EMEP's recalculation of these years with one model version (2009); from 2007 each year is from the annual EMEP Status Report, calculated with the model version and meteorology of that year. The tables for 2019, 2020 and 2022–2024 are taken from Appendix C of the Status Reports, and the table files are compiled by data_files/emep_sr_norway.py.
- 2015 has no tables and is the mean of 2014 and 2016; 1984–1996 are the mean of 1997–2001.
- The change of EMEP model domain and version in 2007 gives a break in the deposition in Norway from foreign emitters (see RW.RW-AT.AT-Atmospheric inflow), but not in the deposition of Norwegian emissions abroad, so this flow is not corrected.

**Interpretation**

- The flow is about 35–42 kt N per year up to 2021 and falls to 25 kt N in 2024, following lower Norwegian NOx emissions.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* EMEP (2024). *SR country tables*. [https://www.emep.int/mscw/mscw_srdata.html](https://www.emep.int/mscw/mscw_srdata.html)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
