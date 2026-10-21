---
layout: default
title: Manure Emissions (N2O)
parent: Manure Management (AG.MM)
nav_order: 2
---

# Manure Emissions (N2O)

<iframe src="../output_files/plots/AG_MM_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.MM-AT.AT-Emissions-N2O** is direct N2O from manure in housing and storage plus indirect N2O from N that volatilises or leaches from the storage.

#### Data sources

- N2O from "3.B. Manure management" in the UNFCCC Common Reporting Tables (CRT), Table 3, of the national greenhouse gas inventory.
- It is calculated in the inventory from the N in managed manure with the manure model described under AG.MM-AG.SM-Manure application-Nmix and IPCC emission factors for each storage system ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)).

#### Interpretations and comparisons

- The flow is about 0.4 kt N per year with little change since 1990.
- The uncertainty is large, since the emission factors for N2O are uncertain by a factor of about two.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N2O from manure management (Norway's GHG inventory, CRT 3.B) | Inventory with published uncertainty | −50/+100 %, lognormal | 100% | 100% | 1.00 | 1.00 | none |
