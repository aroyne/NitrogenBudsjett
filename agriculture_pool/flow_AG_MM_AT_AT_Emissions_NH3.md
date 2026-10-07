---
layout: default
title: Manure Emissions (NH3)
parent: Manure Management (AG.MM)
nav_order: 3
---

# Manure Emissions (NH3)

<iframe src="../output_files/plots/AG_MM_AT_AT_Emissions_NH3.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
We have used data from CLRTAP Inventory Submissions (EMEP, 2025)<!--cite:emep_officially_2025--> as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, using the categories given in Table 29.

**How the numbers are derived**

- The emissions reported to CLRTAP are calculated in the national inventory with the same manure model as the greenhouse gas inventory: N in manure, mineral fertilizer and other N sources multiplied by NH3 and NOx emission factors for each animal category, storage system, spreading method and fertilizer type.
- The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).
- Emissions in Gg NH3 or Gg NOx (as NO2) are converted to N with the factors 14/17 and 14/46.
- The flow sums the manure management categories 3B1a–3B4h (Table 29 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->), which cover housing and storage, and category 3I (other agriculture), which in Norway is NH3 from ammonia treatment of straw used for feed.
- The ammonia used for straw treatment is an N input to agriculture, but we have not found data on the amounts used, so it is not included as an input.
- NH3 from spreading manure and from grazing is counted in AG.SM-AT.AT-Emissions-NH3.

**Interpretation**

- The flow is about 9.4–11.8 kt N per year: 10.3 kt N in 1990 and 9.9 kt N in 2024.
- Straw treatment (3I) contributed 1.2 kt N in 1990 but only 0.3 kt N in 2024, while manure management rose from about 9 to 9.6 kt N.
- The peak in 2018 (11.8 kt N) comes from straw treatment, which rose to about 1.4 kt N in the drought year.
- Cattle account for about 70% (dairy cattle 3.0 kt N and other cattle 3.7 kt N in 2024).
- Emissions from other cattle, horses and poultry have increased, while emissions from dairy cattle, sheep and pigs have decreased.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
