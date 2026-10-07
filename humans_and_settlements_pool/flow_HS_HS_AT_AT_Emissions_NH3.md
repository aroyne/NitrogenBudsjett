---
layout: default
title: Ammonia Body Emissions
parent: 6. Humans and settlements (HS)
nav_order: 1
---

# Ammonia Body Emissions

<iframe src="../output_files/plots/HS_HS_AT_AT_Emissions_NH3.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HS.HS-AT.AT-Emissions-NH3** is ammonia emitted from the human body, including additional emissions from infants and young children (nappies), and from smoking.

#### Data sources

- Population by age from SSB ([table 07459](https://www.ssb.no/statbank/table/07459)).
- Shares of daily and occasional smokers from SSB's statistics on smoking habits ([table 05307](https://www.ssb.no/statbank/table/05307)), based on a survey of the population aged 16–79.
- Cigarettes per daily smoker from [FHI](https://www.fhi.no/le/royking/tobakkinorge/bruk-av-tobakk/nikotinmarkedets-sammensetning-og-endring/): 12 per day for men and 10 for women.

#### Assumptions

- Emissions are calculated with Equation 46 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025--> (after Sutton et al., 2000): 17 g N per person per year for the total population, with additional factors of 11.7 g N for infants under 1 year and 14.6 g N for children aged 1–3, plus 3.4 mg N per cigarette.
- Daily smokers are assumed to smoke 4015 cigarettes per year (11 per day), and occasional smokers 100 per year.

#### Interpretations and comparisons

- The flow is about 0.1 kt N per year.
- Smoking contributes about 0.016 kt N in 1990 and 0.005 kt N in 2024; the decline in smoking offsets most of the increase from population growth.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
