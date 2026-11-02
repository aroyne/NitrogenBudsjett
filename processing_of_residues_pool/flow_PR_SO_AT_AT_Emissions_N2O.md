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

- **PR.SO-AT.AT-Emissions-N2O** is N<sub>2</sub>O from biological treatment of waste (composting and biogas production) and waste incineration, with and without energy recovery; landfills report no N<sub>2</sub>O.

#### Data sources

- N<sub>2</sub>O from "5.B. Biological treatment of solid waste" and "5.C. Incineration and open burning of waste" in the UNFCCC Common Reporting Tables (CRT), Table 5, of the national greenhouse gas inventory ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)), calculated from the amounts of waste composted, digested and incinerated and emission factors.
- N<sub>2</sub>O from waste incinerated with energy recovery, which the inventory reports under 1.A.1.a (the “other fossil fuels” row in CRT Table 1.A(a), which includes the biogenic part of waste), as recommended in chapter 1.4.1.2 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Interpretations and comparisons

- The flow is small, about 0.01 kt N in 1990 and 0.03–0.056 kt N per year since 2000. Waste incineration with energy recovery accounts for 0.006–0.02 kt N per year; the rest is mainly biological treatment.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-10-22). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N<sub>2</sub>O from waste incineration and biological treatment (Norway's GHG inventory, CRT 5) | Inventory with published uncertainty | −66.7/+200 %, lognormal | 100% | 100% | 1.00 | 1.00 | none |
