---
layout: default
title: NOx Emissions (Solid Waste)
parent: Solid Waste (PR.SO)
nav_order: 4
---

# NOx Emissions (Solid Waste)

<iframe src="../output_files/plots/PR_SO_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**PR.SO-AT.AT-Emissions-NOx**: We have used data from CLRTAP Inventory Submissions, using the categories given in Table 48 and 31 (emissions from category 1A1 Energy industries are all assigned to the EF pool). 

**How the numbers are derived**

- The emissions reported to CLRTAP are calculated in the national inventory from the amounts of waste treated and emission factors, or from emissions reported by the plants; the methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).
- The flow sums the categories in Tables 48 and 31 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: 1A1a (public electricity and heat production, in Norway mainly waste incineration and district heating), 5A (solid waste disposal), 5B1 composting, 5B2 anaerobic digestion, 5C (incineration) and 5E (other waste).
- Category 1A1a is counted here and not in EF.EC-AT.AT, as recommended in chapter 1.4.1.2 of Schäppi et al. (2025), to avoid double counting.
- Emissions in Gg NOx (as NO2) or Gg NH3 are converted to N with the factors 14/46 and 14/17.

**Interpretation**

- The flow is about 0.4–0.7 kt N per year and has increased with waste incineration.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
