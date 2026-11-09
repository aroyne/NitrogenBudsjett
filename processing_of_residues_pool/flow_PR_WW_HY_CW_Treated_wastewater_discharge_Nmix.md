---
layout: default
title: Treated Wastewater Discharge to CW
parent: Wastewater (PR.WW)
nav_order: 5
---

# Treated Wastewater Discharge to CW

<iframe src="../output_files/plots/PR_WW_HY_CW_Treated_wastewater_discharge_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.WW-HY.CW-Treated wastewater discharge-Nmix** is the N discharged from the municipal wastewater sector. All treated wastewater discharge is assigned to coastal water.

#### Data sources

- SSB's statistics on discharges from the wastewater sector ([table 05280](https://www.ssb.no/statbank/table/05280) *Totale utslipp av fosfor og nitrogen fra avløpssektoren*) give the total nitrogen discharged, based on the municipalities' reporting through KOSTRA.
- Data back to 1997 are found in the series SSB Naturressurser og miljø.

#### Assumptions

- Due to lack of available data, 1990–1996 are the 1997 value scaled with the population (SSB table 06913). Nitrogen removal in treatment plants was small in this period (PR.WW-AT.AT-Emissions-N2 is below 0.1 kt N until 1996), so the discharge is assumed to follow the population.

#### Interpretations

- The flow is about 16–20 kt N per year<!--range:PR.WW-HY.CW-Treated wastewater discharge-Nmix:1990-2024-->, rising from about 17.6 kt N<!--val:PR.WW-HY.CW-Treated wastewater discharge-Nmix:1990--> in 1990 to 18.5 kt N<!--val:PR.WW-HY.CW-Treated wastewater discharge-Nmix:1997--> in 1997, falling to 16 kt N<!--mean:PR.WW-HY.CW-Treated wastewater discharge-Nmix:2002-2005--> in 2002–2005 and rising again to about 20 kt N<!--val:PR.WW-HY.CW-Treated wastewater discharge-Nmix:2024--> in 2024 with population growth.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N discharges from wastewater treatment plants (SSB 05280) | Survey or self-reported data | ±20 %, normal, drawn per year | – | 100% | – | 1.00 | [Inflow to coastal waters](../hydrosphere_pool/flow_HY_SW_HY_CW_Inflow_to_coastal_waters_Nmix.html) |
| Wastewater discharges 1997–2001 (SSB) | Survey or self-reported data | ±30 %, normal, drawn per year | 52% | – | 1.00 | – | none |
| Extrapolation (treated wastewater:1997) | Gap filling: extrapolation | ±25–45 %, lognormal, grows with distance to known year | 48% | – | 1.00 | – | none |
