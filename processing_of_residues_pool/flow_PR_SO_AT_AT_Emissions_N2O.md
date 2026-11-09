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

- **PR.SO-AT.AT-Emissions-N2O** is N<sub>2</sub>O from biological treatment of waste (composting and biogas production) and waste incineration without energy recovery; landfills report no N<sub>2</sub>O. N<sub>2</sub>O from waste incinerated with energy recovery (1.A.1.a) is counted in EF.EC-AT.AT-Emissions-N2O, since the waste is delivered to EF.EC.

#### Data sources

- N<sub>2</sub>O from "5.B. Biological treatment of solid waste" and "5.C. Incineration and open burning of waste" in the UNFCCC Common Reporting Tables (CRT), Table 5, of the national greenhouse gas inventory (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_nid_2026-->, calculated from the amounts of waste composted, digested and incinerated and emission factors.

#### Interpretations

- The flow is small, about 0.003 kt N<!--val:PR.SO-AT.AT-Emissions-N2O:1990--> in 1990 and 0.02–0.04 kt N per year<!--range:PR.SO-AT.AT-Emissions-N2O:2000-2024--> since 2000, mainly from biological treatment.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N<sub>2</sub>O from waste incineration and biological treatment (Norway's GHG inventory, CRT 5) | Inventory with published uncertainty | −66.7/+200 %, lognormal | 100% | 100% | 1.00 | 1.00 | none |

### References

* Miljødirektoratet (2026). *Greenhouse gas emissions 1990–2024, National Inventory Document* (M-3138). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)
