---
layout: default
title: N2 Emissions (Wastewater)
parent: Wastewater (PR.WW)
nav_order: 2
---

# N2 Emissions (Wastewater)

<iframe src="../output_files/plots/PR_WW_AT_AT_Emissions_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.WW-AT.AT-Emissions-N2** is N2 released by biological nitrogen removal in wastewater treatment plants. Only treatment plants with nitrogen removal release significant amounts of N2.

#### Data sources

- N discharged from the plants with nitrogen removal, reported in Norske utslipp or by the plant, and the plants' reported removal rates: Lillehammer (from 1995), VEAS and Nordre Follo (from 1997), Gardermoen (from 1998), Bekkelaget (from 2002), NRVA (from 2003) – six plants with nitrogen removal through 2024 – and Hokksund (from 2025).

#### Assumptions

- For each plant, the N discharged is converted to N removed with the plant's removal rate r as N discharged × r/(1 − r).
- Where specific data on the nitrogen removal fraction were missing we assumed a default of 70%, and we extrapolated or interpolated between existing data where reported emission data were missing.

#### Interpretations and comparisons

- The flow rises from 0.1 kt N in 1995 to 1.5–1.6 kt N around 2000 and 3.4–4.9 kt N since 2012, as more plants have introduced nitrogen removal.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N removal rate at wastewater treatment plants with N removal | Parameter | 0.5–0.8, triangular | – | 89% | – | 2.55 | none |
| N removal at wastewater treatment plants (plant reports) | Survey or self-reported data | ±20 %, normal, drawn per year | – | 11% | – | 1.00 | none |
