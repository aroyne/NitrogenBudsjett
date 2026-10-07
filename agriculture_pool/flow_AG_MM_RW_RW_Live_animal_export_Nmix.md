---
layout: default
title: Live Animal Export
parent: Manure Management (AG.MM)
nav_order: 8
---

# Live Animal Export

<iframe src="../output_files/plots/AG_MM_RW_RW_Live_animal_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Taken from FAOSTAT Crop and livestock products, assuming typical weights of animals from various sources, average 16 % protein in whole animal based on typical values in Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> and Jones factor 6.25 for nitrogen to protein (standard).

**How the numbers are derived**

- FAOSTAT's trade statistics for live animals ([TCL](https://www.fao.org/faostat/en/#data/TCL)) give the number of animals exported per year and animal category.
- FAOSTAT reports poultry in thousands of animals, which is converted to animals.
- The number is multiplied by an average live weight per category from the IPCC 2006 Guidelines (Vol. 4, Ch. 10, Annex 10A: e.g. other cattle 420 kg, breeding pigs 198 kg, sheep 48.5 kg, goats 38.5 kg, horses 377 kg, laying hens 1.8 kg; animal_weights in N_parameters.xlsx), a protein content of 16% and 1/6.25 to get N.

**Interpretation**

- The flow is very small, below 0.03 kt N per year.
- Pigs and horses make up most of the exported animals.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
