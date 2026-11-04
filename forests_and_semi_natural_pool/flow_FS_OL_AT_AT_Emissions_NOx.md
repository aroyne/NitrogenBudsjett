---
layout: default
title: Other Land Emissions (NOx)
parent: Other Land (FS.OL)
nav_order: 4
---

# Other Land Emissions (NOx)

<iframe src="../output_files/plots/FS_OL_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.OL-AT.AT-Emissions-NOx** is NO<sub>x</sub> from manure deposited by grazing animals on unmanaged land (AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix).
- NO<sub>x</sub> from the soils of other land is neglected because no values are reported in the CRLTAP categories 4F1 and 4F2 (wetlands / other land).

#### Data sources

- Emissions from grazing animals (NFR 3Da3) reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), calculated in the national inventory with the manure model: N deposited during grazing multiplied by emission factors ([Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)).
- The inventory reports the emissions from grazing for all land types combined; it does not split agricultural land and unmanaged land.

#### Assumptions

- The flow is the unmanaged-land share of the NO<sub>x</sub> from grazing animals (3Da3). The unmanaged-land share is the grazing manure per animal category (CRT Table 3.B(b)) weighted with the share of each category's grazing time spent on unmanaged land in 2018 (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79): sheep 51%, goats 54% and horses 16% (each ±20%), reindeer 100% and farmed deer 0%. For cattle the survey shares (dairy cows 16%, suckler cows 30%, other cattle 32%) would give more manure on unmanaged land than the feed taken up on unmanaged land (FS.OL-AG.MM-Grazing-Nmix) allows. The cattle manure on unmanaged land is therefore the number of cattle on unmanaged land (SSB table 12660, which counts animals with at least 5 weeks on unmanaged land; the 1995 level before 1995) times the average N excretion of cattle other than dairy cows (CRT Table 3.B(b); most cattle on unmanaged land are beef cows and young stock) times 8 weeks on unmanaged land (range 5–12, PERT) out of 52, at most the grazing manure of cattle. This is 8–17% of the cattle grazing manure. In total this gives 26–30% of the grazing manure. The shares are held at the 2018 survey values for all years; before 2009 the subsidy rules required a longer grazing period on unmanaged land (eight instead of five weeks), so the share may have been somewhat higher.
- The same amount is removed from AG.SM-AT.AT-Emissions-NOx.

#### Interpretations

- The flow is small, about 0.1 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-04). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, Urine and dung deposited by grazing animals (NFR 3Da3) | Inventory with published uncertainty | −50.6/+102.4 %, lognormal | 96% | 88% | 1.00 | 1.00 | [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) |
| Protein per feed unit of grazing | Parameter | ±20 %, normal | – | 4% | – | 0.85 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html) and 6 more |
| Manure N applied to soils and on pasture (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | ±20 %, normal | <1% | 4% | −0.22 | −0.77 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html) and 5 more |
| Share of sheep grazing manure deposited on unmanaged land | Parameter | ±20 %, normal | 2% | – | 0.56 | – | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html) and 4 more |

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
