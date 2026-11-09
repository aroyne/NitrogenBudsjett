---
layout: default
title: N2O emissions from denitrification
parent: Soil Management (AG.SM)
nav_order: 3
---

# N2O emissions from denitrification

<iframe src="../output_files/plots/AG_SM_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.SM-AT.AT-Emissions-N2O** is direct N<sub>2</sub>O from mineral fertilizer, manure, sewage sludge, grazing animals, crop residues, mineralisation and cultivated organic soils, and indirect N<sub>2</sub>O from N that volatilises or leaches.

#### Data sources

- N<sub>2</sub>O from "3.D. Agricultural soils" in the UNFCCC Common Reporting Tables (CRT), Table 3, of the national greenhouse gas inventory, calculated as the N applied by each source multiplied by IPCC emission factors (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_nid_2026-->.

#### Assumptions

- The inventory counts all manure deposited by grazing animals as input to managed soils, including the share deposited on unmanaged land (utmark), which this model does not count as input to AG.SM (see AG.MM-AG.SM-Manure application-Nmix). The unmanaged-land share (26–30% of grazing manure, see AG.MM-AG.SM-Manure application-Nmix) of the losses from grazing manure is therefore removed from this flow; it is counted in FS.OL-AT.AT-Emissions-N2O.
- The removed N<sub>2</sub>O is the unmanaged-land share of the direct N<sub>2</sub>O from grazing manure (3.D.1.c) plus the indirect N<sub>2</sub>O from its volatilisation and leaching, calculated with the fractions and implied emission factors in CRT Table 3.D (about 0.06 kt N per year).

#### Interpretations

- The flow is about 3.4–3.9 kt N per year<!--range:AG.SM-AT.AT-Emissions-N2O:1990-2024-->, with a slight decrease since 1990.
- The uncertainty is large, mainly from the emission factors (a factor of 3 in Norway's greenhouse gas inventory).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N<sub>2</sub>O from agricultural soils (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | −66.7/+200 %, lognormal | 100% | 100% | 1.00 | 1.00 | [Other Land Emissions (N<sub>2</sub>O)](../forests_and_semi_natural_pool/flow_FS_OL_AT_AT_Emissions_N2O.html) |

### References

* Miljødirektoratet (2026). *Greenhouse gas emissions 1990–2024, National Inventory Document* (M-3138). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)
