---
layout: default
title: Biological N2 Fixation (Forest)
parent: 7. Atmosphere (AT)
nav_order: 6
---

# Biological N2 Fixation (Forest)

<iframe src="../output_files/plots/AT_AT_FS_FO_N2_fixation_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AT.AT-FS.FO-N2 fixation-N2** is biological N2 fixation in forests.

#### Data sources

- Forested area of 12.0 million ha from SSB ([table 14368](https://www.ssb.no/statbank/table/14368), 2019–2023).
- N-fixation rate of 1.5 kg N/ha per year from the Swedish NNB (Moldan et al., 2025)<!--cite:moldan_where_2025-->.

#### Assumptions

- 1.5 kg N/ha per year (range ±50%) times the forested area, assumed constant for the entire time period.

#### Interpretations and comparisons

- The flow is constant at about 18 kt N per year; for comparison, the value for Sweden in 2015 was 39.5 kt N (Moldan et al., 2025)<!--cite:moldan_where_2025-->.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Biological N fixation in forest, per hectare | Parameter | ±50 %, triangular | 96% | 96% | 1.00 | 1.00 | none |
| Forest area | Parameter | ±10 %, normal | 4% | 4% | 1.00 | 1.00 | none |

### References

* Moldan, F., Stadmark, J., Jutterström, S., & Ljunggren, J. (2025). Where does Sweden’s nitrogen go? Building a comprehensive national nitrogen budget. *Environmental Research Letters, 20*(12), 124068. [https://doi.org/10.1088/1748-9326/ae2697](https://doi.org/10.1088/1748-9326/ae2697)
