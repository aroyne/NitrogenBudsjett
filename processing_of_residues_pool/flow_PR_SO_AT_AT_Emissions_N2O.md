---
layout: default
title: N2O Emissions (Solid Waste)
parent: Solid Waste (PR.SO)
nav_order: 2
---

# N2O Emissions (Solid Waste)

<iframe src="../output_files/plots/PR_SO_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.SO-AT.AT-Emissions-N2O** is N2O from biological treatment of waste (composting and biogas production) and waste incineration; landfills report no N2O.

#### Data sources

- N2O from "5.B. Biological treatment of solid waste" and "5.C. Incineration and open burning of waste" in the UNFCCC Common Reporting Tables (CRT), Table 5, of the national greenhouse gas inventory ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)), calculated from the amounts of waste composted, digested and incinerated and emission factors.

#### Interpretations and comparisons

- The flow is small, below 0.005 kt N in 1990 and 0.02–0.04 kt N per year since 2000; biological treatment accounts for most of it.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| N2O from waste incineration and biological treatment (Norway's GHG inventory, CRT 5) | Inventory with published uncertainty | −66.7/+200 %, lognormal | 100% | 100% | none |
