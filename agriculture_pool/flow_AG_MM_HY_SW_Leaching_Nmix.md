---
layout: default
title: Manure Leaching
parent: Manure Management (AG.MM)
nav_order: 5
---

# Manure Leaching

<iframe src="../output_files/plots/AG_MM_HY_SW_Leaching_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.MM-HY.SW-Leaching-Nmix** is N lost through leaching and runoff from manure management.

#### Data sources

- The N lost through leaching and runoff from manure management in the UNFCCC Common Reporting Tables (CRT), Table 3.B(b), reported as the basis for indirect N2O emissions (3.B.5).
- It is calculated in the inventory as a fraction of the N in managed manure, using the manure model described under AG.MM-AG.SM-Manure application-Nmix ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)).

#### Interpretations and comparisons

- The flow is about 3 kt N per year with little change since 1990.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N leaching and run-off from agricultural soils (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | −41/+70 %, lognormal | 100% | 100% | 1.00 | 1.00 | [Leaching from soil management](../agriculture_pool/flow_AG_SM_HY_SW_Leaching_Nmix.html) |
