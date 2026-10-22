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

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NH3 emission factor per person | Parameter | ±20 %, normal | 75% | 97% | 0.75 | 0.91 | none |
| Cigarettes per daily smoker per year | Parameter | 3300–5800, triangular | 16% | 1% | 0.21 | 0.06 | none |
| NH3 emission factor per cigarette | Parameter | ±20 %, normal | 6% | <1% | 0.21 | 0.06 | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
