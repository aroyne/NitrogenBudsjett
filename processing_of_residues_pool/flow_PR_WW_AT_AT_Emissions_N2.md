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

- **PR.WW-AT.AT-Emissions-N2** is N<sub>2</sub> released by biological nitrogen removal in wastewater treatment plants. Only treatment plants with nitrogen removal release significant amounts of N<sub>2</sub>.

#### Data sources

- N discharged from the plants with nitrogen removal, reported in Norske utslipp or by the plant, and the plants' reported removal rates: Lillehammer (from 1995), VEAS and Nordre Follo (from 1997), Gardermoen (from 1998), Bekkelaget (from 2002), NRVA (from 2003) – six plants with nitrogen removal through 2024 – and Hokksund (from 2025).

#### Assumptions

- For each plant, the N discharged is converted to N removed with the plant's removal rate r as N discharged × r/(1 − r).
- The plants' own reported removal rates are used where they exist: VEAS from 2009, Bekkelaget from 2002 and NRVA from 2017. Where specific data on the nitrogen removal fraction were missing, we assumed a default of 70%, and we extrapolated or interpolated between existing data where reported emission data were missing.

#### Interpretations

- The flow rises from 0.1 kt N<!--val:PR.WW-AT.AT-Emissions-N2:1995--> in 1995 to 1.6 kt N<!--range:PR.WW-AT.AT-Emissions-N2:1998-2001--> in 1998–2001, 3.3–3.6 kt N<!--range:PR.WW-AT.AT-Emissions-N2:2009-2018--> in 2009–2018 and 3.9–4.6 kt N<!--range:PR.WW-AT.AT-Emissions-N2:2019-2024--> since 2019, as more plants have introduced nitrogen removal and the removal rates have improved.
- VEAS discharged more N in 2014–2017 (1.2–1.4 kt N against about 0.9 kt N before) because its removal rate fell to 54–60%, while the N entering the plant was about the same. With the reported removal rate this gives less N removed, not more.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N removal at wastewater treatment plants (plant reports) | Survey or self-reported data | ±20 %, normal, drawn per year | – | 80% | – | 1.00 | none |
| N removal rate at wastewater treatment plants with N removal | Parameter | 0.5–0.8, triangular | – | 20% | – | 0.45 | none |
