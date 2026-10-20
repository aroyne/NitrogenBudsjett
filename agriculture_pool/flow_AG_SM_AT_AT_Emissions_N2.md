---
layout: default
title: N2 emissions from denitrification
parent: Soil Management (AG.SM)
nav_order: 2
---

# N2 emissions from denitrification

<iframe src="../output_files/plots/AG_SM_AT_AT_Emissions_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.SM-AT.AT-Emissions-N2** is N2 from denitrification in agricultural soils. The flow is not based on measurements.

#### Data sources

- A default loss rate of 14 kg N per ha per year (range 7–21 kg N per ha), which Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> recommends if no other data are available.
- The agricultural area in use each year from SSB's agricultural statistics ([table 05982](https://www.ssb.no/statbank/table/05982), "Jordbruksareal i drift"), about 0.98–1.04 million ha.

#### Assumptions

- The loss rate is multiplied by the agricultural area.
- The table has no values for 1990–1998, which are interpolated between 1989 and 1999.

#### Interpretations and comparisons

- The flow is about 14–15 kt N per year and follows the agricultural area, which rose to about 1.04 million ha around 2000 and has since fallen to 0.98 million ha.
- It does not reflect changes in fertilization or soil conditions.
- Schäppi et al. (2025) note that the loss rate can vary from below 10 kg N per ha in well-drained soils to above 150 kg N per ha in waterlogged peat soils, so the uncertainty is large.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N2 loss from agricultural soils per hectare | Parameter | 7–21, triangular | 96% | 100% | 1.00 | 1.00 | none |
| Interpolation (1989-1999) | Gap filling: interpolation | ±7–15 %, lognormal, grows with distance to known year | 4% | – | 1.00 | – | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
