---
layout: default
title: Industrial Emissions (N2O)
parent: Other Producing Industry (MP.OP)
nav_order: 2
---

# Industrial Emissions (N2O)

<iframe src="../output_files/plots/MP_OP_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-AT.AT-Emissions-N2O** is N2O from industrial processes, as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: the sum of 2.B Chemical industry, 2.C Metal industry, 2.G Other product manufacture and use and 2.H Other (2.A Mineral industry and 2.D Non-energy products from fuels report no N2O). The main source is nitric acid production.

#### Data sources

- N2O from industrial processes in the UNFCCC Common Reporting Tables (CRT), Table 2(I), of the national greenhouse gas inventory. N2O from nitric acid production is reported by the plants; the methods are documented in the [National Inventory Document (Miljødirektoratet, NID 2026)](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/).

#### Interpretations and comparisons

- Chemical industry (2.B, nitric acid production) accounts for over 90% of the flow. Emissions are substantial, at least before 2009.
- Emissions were about 4.4 kt N/year in 1990, fell from 4.3 kt N in 2005 to about 1.1 kt N in 2010 after N2O-reducing catalysts were installed in the nitric acid plants, and have been 0.5–0.8 kt N since.
- Category 2.G (mainly N2O used as anaesthetic and propellant) contributes about 0.06 kt N/year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N2O from industrial processes (Norway's GHG inventory, CRT 2) | Inventory with published uncertainty | ±7 %, lognormal | 100% | 100% | 1.00 | 1.00 | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
