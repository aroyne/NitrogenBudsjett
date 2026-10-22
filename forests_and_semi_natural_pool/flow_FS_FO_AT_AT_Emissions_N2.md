---
layout: default
title: Forest Emissions (N2)
parent: Forests (FS.FO)
nav_order: 1
---

# Forest Emissions (N2)

<iframe src="../output_files/plots/FS_FO_AT_AT_Emissions_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.FO-AT.AT-Emissions-N2** is N2 from denitrification in forest soils. N2 from forest soils is not measured or reported.

#### Data sources

- N2O from forest land in CRT Table 4 (see FS.FO-AT.AT-Emissions-N2O).
- N2:N2O ratio of 19.5 ± 26.8 (range 0–46.3), calculated by Butterbach-Bahl et al. (2013) from six studies of temperate beech and spruce forests in Germany, as given by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 157.
- Schäppi et al. (2025) also give an alternative: an average N2 loss of 1.1 kg N per ha per year from Andreae et al. (2016), used by Sweden and Germany.

#### Assumptions

- The flow is the N2O from forest land multiplied by the mean N2:N2O ratio of 19.5.

#### Interpretations and comparisons

- The flow is about 7.1–7.7 kt N per year and follows the N2O flow.
- Since both the N2O emissions and the ratio are very uncertain, the 95% interval is wide.
- With the alternative of 1.1 kg N per ha and about 12 million ha of forest, the flow would be about 13 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N2O from land use (Norway's GHG inventory, CRT 4) | Inventory with published uncertainty | ±201 %, lognormal | 68% | 68% | 1.00 | 1.00 | [Forest Emissions (N2O)](../forests_and_semi_natural_pool/flow_FS_FO_AT_AT_Emissions_N2O.html), [LUC Emissions (N2O)](../humans_and_settlements_pool/flow_HS_HS_AT_AT_LUC_emissions_N2O.html) |
| N2:N2O ratio for forest soils | Parameter | 0–46.3 (min–max), triangular | 32% | 32% | 1.00 | 1.00 | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
