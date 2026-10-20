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

- Due to lack of available data, 1990–1996 are held at the 1997 value.

#### Interpretations and comparisons

- The flow is about 16–20 kt N per year, falling from about 18.5 kt N in 1990–1997 to 16 kt N in 2002–2005 and rising again to about 20 kt N in 2024 with population growth.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| N discharges from wastewater treatment plants (SSB 05280) | Survey or self-reported data | ±20 %, normal, drawn per year | – | 100% | [Inflow to coastal waters](../hydrosphere_pool/flow_HY_SW_HY_CW_Inflow_to_coastal_waters_Nmix.html) |
| Wastewater discharges 1997–2001 (SSB) | Survey or self-reported data | ±30 %, normal, drawn per year | 52% | – | none |
| Held constant or averaged (treated wastewater:1997) | Gap filling: held constant or averaged | ±25–45 %, lognormal, grows with distance to known year | 48% | – | none |
