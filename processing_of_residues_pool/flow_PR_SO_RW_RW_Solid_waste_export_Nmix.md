---
layout: default
title: Solid Waste Export
parent: Solid Waste (PR.SO)
nav_order: 12
---

# Solid Waste Export

<iframe src="../output_files/plots/PR_SO_RW_RW_Solid_waste_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Taken from trade data, SSB table 08801 with N contents taken from Table 50 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> for municipal waste, sewage sludge, hazardous and other waste. No export in these categories is reported before 2002, so we set all previous years to zero. The increase seen from 2022 to 2023 is in the category municipal waste.

**How the numbers are derived**

- Export quantities (kg) by commodity code are taken from SSB's external trade statistics ([table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations, and multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.

**Interpretation**

- The flow is below 1 kt N per year, with the highest value in 2012 (0.9 kt N).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
