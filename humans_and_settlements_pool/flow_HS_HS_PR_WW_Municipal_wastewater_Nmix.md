---
layout: default
title: Municipal Wastewater
parent: 6. Humans and settlements (HS)
nav_order: 5
---

# Municipal Wastewater

<iframe src="../output_files/plots/HS_HS_PR_WW_Municipal_wastewater_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HS.HS-PR.WW-Municipal wastewater-Nmix** is the N in municipal wastewater from the whole population, also households with private sewage systems (septic tanks and small plants).

#### Data sources

- Population on 1 January from SSB ([table 06913](https://www.ssb.no/statbank/table/06913)).

#### Assumptions

- The population is multiplied by 4.56 kg N per person per year (range ±10%), the default value for municipal wastewater in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->. This corresponds to 12.5 g N per person per day.
- The discharges from private sewage systems are part of SSB's statistics on discharges from the wastewater sector used for PR.WW-HY.CW-Treated wastewater discharge-Nmix, so they are included here as input to PR.WW.

#### Interpretations

- The flow rises from about 19 kt N<!--val:HS.HS-PR.WW-Municipal wastewater-Nmix:1990--> in 1990 to 25 kt N<!--val:HS.HS-PR.WW-Municipal wastewater-Nmix:2024--> in 2024, in proportion to the population.
- It is about 95% of the N entering PR.WW. The outputs from PR.WW (discharges, N<sub>2</sub> removal, N<sub>2</sub>O and sewage sludge) are within ±6% of the inputs up to 2012 and 4–15% larger since, with the largest difference in 2014–2017 when N<sub>2</sub> removal at the treatment plants was highest.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N load to wastewater per person | Parameter | ±10 %, normal | 96% | 96% | 1.00 | 1.00 | none |
| Population (SSB 06913) | Registered data | ±2 %, normal, drawn per year | 4% | 4% | 1.00 | 1.00 | [Food Products to Consumers](../materials_and_products_pool/flow_MP_FP_HS_HS_Food_products_Nmix.html) |

### References

* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
