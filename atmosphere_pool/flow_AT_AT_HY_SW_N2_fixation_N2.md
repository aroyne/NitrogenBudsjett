---
layout: default
title: Biological N2 Fixation (Surface Water)
parent: 7. Atmosphere (AT)
nav_order: 14
---

# Biological N2 Fixation (Surface Water)

<iframe src="../output_files/plots/AT_AT_HY_SW_N2_fixation_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AT.AT-HY.SW-N2 fixation-N2** is biological N2 fixation in lakes and rivers.

#### Data sources

- Surface water area of 20 457 km² from NIBIO ([Arealbarometer](https://arealbarometer.nibio.no/nb/norge/); NIBIO, 2026<!--cite:nibio_arealbarometer_2026-->).
- Table 62 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025--> (after Reddy and DeLaune, 2008) gives biological fixation rates of 0–18 (mean 9) kg N/ha in oligotrophic lakes, 0–1 (mean 1) kg N/ha in mesotrophic lakes and 2–91 (mean 47) kg N/ha in eutrophic lakes.

#### Assumptions

- Most Norwegian lakes are oligotrophic, but N fixation in nutrient-poor boreal lakes is generally low, and we use 0.1 t N/km² (1 kg N/ha, the mesotrophic mean) as the median of a lognormal distribution with 2 t N/km² as the upper end of the 95% interval (95% interval 0.005–2 t N/km²).

#### Interpretations and comparisons

- The flow is constant at about 2 kt N per year, with a large uncertainty (95% interval about 0.1–37 kt N).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N fixation rate in surface water | Parameter | 0–2, lognormal | 100% | 100% | 1.00 | 1.00 | none |

### References

* NIBIO (2026). Arealbarometer for Norge. *nibio.no*. [https://arealbarometer.nibio.no/nb/norge/](https://arealbarometer.nibio.no/nb/norge/)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
