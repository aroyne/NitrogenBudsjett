---
layout: default
title: Manure from Grazing on Unmanaged Land
parent: Manure Management (AG.MM)
nav_order: 9
---

# Manure from Grazing on Unmanaged Land

<iframe src="../output_files/plots/AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix** is the manure N deposited directly by grazing animals on unmanaged land (unmanaged land: mountain, heath and forest grazing), the part of the grazing manure that is not applied to agricultural land (AG.MM-AG.SM-Manure application-Nmix).

#### Data sources

- "Urine and dung deposited by grazing animals" (PRP, the IPCC term for N deposited by grazing animals on pasture, range and paddock) in the UNFCCC Common Reporting Tables (CRT), Table 3.D, and the PRP per animal category in Table 3.B(b), of the national greenhouse gas inventory. The inventory calculates the N excreted per animal category from animal numbers and national N excretion rates and the fraction of time spent grazing (Miljødirektoratet, 2020<!--cite:miljodirektoratet_manure_2020-->). It does not split the grazing manure between agricultural land and unmanaged land.
- Weeks on agricultural land, unmanaged land and in exercise yards per animal category in 2018 from SSB's survey of manure use (Kolle & Oguz-Alper, 2020, Table A79)<!--cite:ssb_gjodselressurser_2020-->.

#### Assumptions

- The unmanaged-land share of the grazing manure (26–30%) is calculated per animal category, from SSB's survey of grazing time and, for cattle, the number of cattle on unmanaged land, as described under [AG.MM-AG.SM-Manure application-Nmix](flow_AG_MM_AG_SM_Manure_application_Nmix.html).

#### Interpretations

- The flow is about 6.8–7.4 kt N per year<!--range:AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix:1990-2024-->.
- Sheep account for 52–62%, cattle for 19–29% and reindeer, which graze only on unmanaged land, for 14–18%.
- Without a cap, the manure on unmanaged land would rise from 86% of the feed taken up there (FS.OL-AG.MM-Grazing-Nmix, 7.5–8.6 kt N including reindeer) in 1990 to 99% after 2015, which leaves almost nothing retained in growth, milk and wool. From 2000 the manure is therefore capped at 90% of the uptake (see AG.MM-AG.SM-Manure application-Nmix). Both flows are uncertain: the feed uptake builds on a single estimate for 1996 (Hegrenes & Asheim, 2006)<!--cite:hegrenes_verdi_2006-->, and the manure on the survey of grazing time in 2018.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Protein per feed unit of grazing | Parameter | ±20 %, normal | – | 52% | – | 0.85 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html) and 6 more |
| Feed units of sheep on unmanaged land, 1996 | Parameter | ±20 %, normal | – | 22% | – | 0.55 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 5 more |
| Protein-to-N conversion factor (Jones factor) | Parameter | ±10 %, normal | 1% | 11% | −0.22 | −0.77 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html), [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html) and 10 more |
| N retained by grazing animals on unmanaged land | Parameter | 0.05–0.15, triangular | – | 6% | – | −0.11 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 4 more |
| Feed units of cattle on unmanaged land, 1996 | Parameter | ±20 %, normal | – | 5% | – | 0.28 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 5 more |
| Livestock on unmanaged land (SSB 12660) | Registered data | ±5 %, normal, drawn per year | – | 3% | – | 0.85 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 5 more |
| Manure N applied to soils and on pasture (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | ±20 %, normal | 54% | 2% | 0.80 | 0.15 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 5 more |
| Held constant or averaged (cattle on unmanaged land) | Gap filling: held constant or averaged | ±15–35 %, lognormal, grows with distance to known year | 4% | – | 0.19 | – | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 5 more |
| Share of sheep grazing manure deposited on unmanaged land | Parameter | ±20 %, normal | 26% | – | 0.56 | – | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 4 more |
| Weeks on unmanaged land per head of cattle | Parameter | 5–12, lognormal | 14% | – | 0.19 | – | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 4 more |

### References

* Hegrenes, A., & Asheim, L. J. (2006). *Verdi av fôr frå utmarksbeite og sysselsetting i beitebaserte næringar*. NILF.
* Miljødirektoratet (2020). *Calculation of atmospheric nitrogen emissions from manure in Norwegian agriculture: Technical description of the revised model* (M-1848). [miljodirektoratet.no](https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf)
* Kolle, S. O., & Oguz-Alper, M. (2020). *Bruk av gjødselressurser i jordbruket 2018. Metodebeskrivelse og resultater fra en utvalgsbasert undersøkelse* (Rapporter 2020/9). Statistisk sentralbyrå.
