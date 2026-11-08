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

- **FS.FO-AT.AT-Emissions-N2** is N<sub>2</sub> from denitrification in forest soils. N<sub>2</sub> from forest soils is not measured or reported.

#### Data sources

- N<sub>2</sub>O from forest land in CRT Table 4 (see FS.FO-AT.AT-Emissions-N2O).
- N<sub>2</sub>:N<sub>2</sub>O ratio of 19.5 ± 26.8 (range 0–46.3), calculated by Butterbach-Bahl et al. (2013) from six studies of temperate beech and spruce forests in Germany, as given by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 157.
- Schäppi et al. (2025) also give an alternative: an average N<sub>2</sub> loss of 1.1 kg N per ha per year from Andreae et al. (2016), used by Sweden and Germany.

#### Assumptions

- The flow is the N<sub>2</sub>O from forest land multiplied by the mean N<sub>2</sub>:N<sub>2</sub>O ratio of 19.5.

#### Interpretations

- The flow is about 7.1–7.7 kt N per year<!--range:FS.FO-AT.AT-Emissions-N2:1990-2024--> and follows the N<sub>2</sub>O flow.
- Since both the N<sub>2</sub>O emissions and the ratio are very uncertain, the 95% interval is wide.
- With the alternative of 1.1 kg N per ha and about 12 million ha of forest, the flow would be about 13 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N<sub>2</sub>O from land use (Norway's GHG inventory, CRT 4) | Inventory with published uncertainty | ±201 %, lognormal | 68% | 68% | 1.00 | 1.00 | [Forest Emissions (N<sub>2</sub>O)](../forests_and_semi_natural_pool/flow_FS_FO_AT_AT_Emissions_N2O.html), [LUC Emissions (N<sub>2</sub>O)](../humans_and_settlements_pool/flow_HS_HS_AT_AT_LUC_emissions_N2O.html) |
| N<sub>2</sub>:N<sub>2</sub>O ratio for forest soils | Parameter | 0–46.3 (min–max), triangular | 32% | 32% | 1.00 | 1.00 | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
