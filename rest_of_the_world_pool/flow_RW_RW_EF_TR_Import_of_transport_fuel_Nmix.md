---
layout: default
title: Transport Fuel Import
parent: Rest of the world (RW)
nav_order: 7
---

# Transport Fuel Import

<iframe src="../output_files/plots/RW_RW_EF_TR_Import_of_transport_fuel_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-EF.TR-Import of transport fuel-Nmix** is the N in imported fuels for transport.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.
- Only the commodity codes for transport fuels are included.

#### Interpretations and comparisons

- The flow is small, below 0.5 kt N per year, since transport fuels contain little N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| N content of traded goods: jet fuel | N content of traded goods | ±20 %, normal | 94% | 94% | [Export of transport fuels](../energy_and_fuels_pool/flow_EF_TR_RW_RW_Export_of_transport_fuels_Nmix.html) |
| Traded quantities (SSB 08801) (transport_fuel) | Registered data | ±5 %, normal, drawn per year | 6% | 6% | [Export of transport fuels](../energy_and_fuels_pool/flow_EF_TR_RW_RW_Export_of_transport_fuels_Nmix.html) |
