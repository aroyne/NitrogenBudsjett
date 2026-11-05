---
layout: default
title: Other Land Emissions (NH3)
parent: Other Land (FS.OL)
nav_order: 3
---

# Other Land Emissions (NH3)

<iframe src="../output_files/plots/FS_OL_AT_AT_Emissions_NH3.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.OL-AT.AT-Emissions-NH3** is ammonia from manure deposited by grazing animals on unmanaged land (AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix). Other NH<sub>3</sub> emissions from other land are not included.

#### Data sources

- Emissions from grazing animals (NFR 3Da3) reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), calculated in the national inventory with the manure model: N deposited during grazing multiplied by emission factors ([Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)).
- The inventory reports the emissions from grazing for all land types combined; it does not split agricultural land and unmanaged land.

#### Assumptions

- The flow is the unmanaged-land share of the NH<sub>3</sub> from grazing animals (3Da3). The unmanaged-land share (26–30% of the grazing manure) is calculated per animal category as described under [AG.MM-AG.SM-Manure application-Nmix](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html).
- The same amount is removed from AG.SM-AT.AT-Emissions-NH3.

#### Interpretations

- The flow is about 0.4–0.5 kt N per year, about 6% of the manure deposited on unmanaged land.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NH<sub>3</sub>, Urine and dung deposited by grazing animals (NFR 3Da3) | Inventory with published uncertainty | −58/+138 %, lognormal | 98% | 93% | 1.00 | 1.00 | [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html) |
| Protein per feed unit of grazing | Parameter | ±20 %, normal | – | 3% | – | 0.85 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html) and 6 more |
| Manure N applied to soils and on pasture (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | ±20 %, normal | <1% | 2% | −0.22 | −0.77 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html) and 5 more |

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
