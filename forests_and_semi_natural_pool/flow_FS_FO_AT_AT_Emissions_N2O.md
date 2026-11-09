---
layout: default
title: Forest Emissions (N2O)
parent: Forests (FS.FO)
nav_order: 2
---

# Forest Emissions (N2O)

<iframe src="../output_files/plots/FS_FO_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.FO-AT.AT-Emissions-N2O** is N<sub>2</sub>O from forest land, as reported under land use, land-use change and forestry (category 4.A Forest land in the greenhouse gas inventory).

#### Data sources

- N<sub>2</sub>O from "4.A. Forest land" in the UNFCCC Common Reporting Tables (CRT), Table 4, of the national greenhouse gas inventory (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_nid_2026-->.
- The emissions are not measured but calculated in the inventory from activity data (areas, N inputs, burned area) and emission factors, following the IPCC guidelines. In 2024 the category consists of (CRT Tables 4(I)–4(IV)):
    - Drained organic forest soils (Table 4(II), 0.36 of 0.38 kt N/year<!--val:FS.FO-AT.AT-Emissions-N2O:2024-->): 128 kha drained organic soil in forest remaining forest with 2.8 kg N<sub>2</sub>O–N per ha, plus a small area of cropland converted to forest.
    - Fertilization of forest (Table 4(I), 0.009 kt N/year): 0.47 kt N of inorganic fertilizer, with direct emissions and indirect emissions from volatilised and leached N.
    - Mineralisation of soil organic matter after land-use change to forest (Table 4(III), 0.001 kt N/year).
    - Forest fires (Table 4(IV), 427 ha burned in 2024, 0.0007 kt N/year).
#### Assumptions

- The inventory values are used directly, converted from N<sub>2</sub>O to N.

#### Interpretations

- The flow is small and nearly constant, about 0.37–0.38 kt N per year<!--range:FS.FO-AT.AT-Emissions-N2O:1990-2024-->, since the area of drained organic forest soil changes little.
- The 0.47 kt N<!--val:MP.OP-FS.FO-Mineral fertilizer-Nmix:2024--> of fertilizer on forest in the inventory is the same as MP.OP-FS.FO-Mineral fertilizer-Nmix in this model in 2024.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N<sub>2</sub>O from land use (Norway's GHG inventory, CRT 4) | Inventory with published uncertainty | ±201 %, lognormal | 100% | 100% | 1.00 | 1.00 | [Forest Emissions (N<sub>2</sub>)](../forests_and_semi_natural_pool/flow_FS_FO_AT_AT_Emissions_N2.html), [LUC Emissions (N<sub>2</sub>O)](../humans_and_settlements_pool/flow_HS_HS_AT_AT_LUC_emissions_N2O.html) |

### References

* Miljødirektoratet (2026). *Greenhouse gas emissions 1990–2024, National Inventory Document* (M-3138). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)
