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

- **AG.SM-AT.AT-Emissions-N2** is N<sub>2</sub> from denitrification in agricultural soils. The flow is not based on measurements.

#### Data sources

- A default loss rate of 14 kg N per ha per year (range 7–21 kg N per ha), which Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> recommends if no other data are available.
- The agricultural area in use each year from SSB's agricultural statistics ([table 05982](https://www.ssb.no/statbank/table/05982), "Jordbruksareal i drift"), about 0.98–1.04 million ha.

#### Assumptions

- The loss rate is multiplied by the agricultural area.
- The table has no values for 1990–1998, which are interpolated between 1989 and 1999.

#### Interpretations

- The flow is about 14–15 kt N per year and follows the agricultural area, which rose to about 1.04 million ha around 2000 and has since fallen to 0.98 million ha.
- It does not reflect changes in fertilization or soil conditions.
- Schäppi et al. (2025) note that the loss rate can vary from below 10 kg N per ha in well-drained soils to above 150 kg N per ha in waterlogged peat soils, so the uncertainty is large.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N<sub>2</sub> loss from agricultural soils per hectare | Parameter | 7–21, triangular | 96% | 100% | 1.00 | 1.00 | none |
| Interpolation (1989-1999) | Gap filling: interpolation | ±7–15 %, lognormal, grows with distance to known year | 4% | – | 1.00 | – | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
