---
layout: default
title: Other Land Emissions (N2O)
parent: Other Land (FS.OL)
nav_order: 5
---

# Other Land Emissions (N2O)

<iframe src="../output_files/plots/FS_OL_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.OL-AT.AT-Emissions-N2O** is N<sub>2</sub>O from manure deposited by grazing animals on unmanaged land (AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix).
- Following the Swedish NNB (Jutterström et al., 2020)<!--cite:jutterstrom_swedish_2020-->, denitrification in the soils of other land is considered negligible.

#### Data sources

- N<sub>2</sub>O from grazing manure in the UNFCCC Common Reporting Tables (CRT), Table 3.D, of the national greenhouse gas inventory ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)): direct N<sub>2</sub>O from urine and dung deposited by grazing animals (3.D.1.c), and the fractions and implied emission factors for indirect N<sub>2</sub>O from volatilisation (FracGASPRP, 3.D.2.a) and leaching (FracLEACH, 3.D.2.b). The inventory calculates these with IPCC emission factors and reports them for all grazing land combined.

#### Assumptions

- The flow is the unmanaged-land share of the direct N<sub>2</sub>O from grazing manure plus the indirect N<sub>2</sub>O from the volatilisation and leaching of the manure deposited on unmanaged land. The unmanaged-land share (26–30% of the grazing manure) is calculated per animal category as described under [AG.MM-AG.SM-Manure application-Nmix](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html).
- The same amount is removed from AG.SM-AT.AT-Emissions-N2O.

#### Interpretations

- The flow is small, about 0.07 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N<sub>2</sub>O from agricultural soils (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | −66.7/+200 %, lognormal | 99% | 96% | 1.00 | 1.00 | [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html) |

### References

* Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation*.
