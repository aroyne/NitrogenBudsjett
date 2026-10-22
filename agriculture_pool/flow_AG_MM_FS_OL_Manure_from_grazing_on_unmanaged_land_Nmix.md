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

- **AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix** is the manure N deposited directly by grazing animals on utmark (unmanaged land: mountain, heath and forest grazing), the part of the grazing manure that is not applied to agricultural land (AG.MM-AG.SM-Manure application-Nmix).

#### Data sources

- "Urine and dung deposited by grazing animals" (PRP) in the UNFCCC Common Reporting Tables (CRT), Table 3.D, and the PRP per animal category in Table 3.B(b), of the national greenhouse gas inventory. The inventory calculates the N excreted per animal category from animal numbers and national N excretion rates and the fraction of time spent grazing (Norwegian Environment Agency, 2020<!--cite:miljodirektoratet_manure_2020-->). It does not split the grazing manure between innmark and utmark.
- Weeks on innmark, utmark and in exercise yards per animal category in 2018 from SSB's survey of manure use (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79).

#### Assumptions

- The utmark share is the grazing manure per animal category (CRT Table 3.B(b)) weighted with the share of each category's grazing time spent on utmark in 2018 (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79): sheep 51%, goats 54% and horses 16% (each ±20%), reindeer 100% and farmed deer 0%. For cattle the survey shares (dairy cows 16%, suckler cows 30%, other cattle 32%) would give more manure on utmark than the feed taken up on utmark (FS.OL-AG.MM-Grazing-Nmix) allows. The cattle manure on utmark is therefore the number of cattle on utmark (SSB table 12660, which counts animals with at least 5 weeks on utmark; the 1995 level before 1995) times the average N excretion of cattle other than dairy cows (CRT Table 3.B(b); most cattle on utmark are beef cows and young stock) times 8 weeks on utmark (range 5–12, PERT) out of 52, at most the grazing manure of cattle. This is 8–17% of the cattle grazing manure. In total this gives 26–33% of the grazing manure. The shares are held at the 2018 survey values for all years; before 2009 the subsidy rules required a longer grazing period on utmark (eight instead of five weeks), so the share may have been somewhat higher.

#### Interpretations and comparisons

- The flow is about 7–8 kt N per year, slightly higher after 2005 as more cattle (mainly beef cattle) graze on utmark.
- Sheep account for 52–62%, cattle for 19–29% and reindeer, which graze only on utmark, for 14–18%.
- The manure deposited on utmark is slightly smaller than the feed taken up on utmark (FS.OL-AG.MM-Grazing-Nmix, 7.5–8.6 kt N including reindeer), as it should be since part of the N in the feed is retained in growth, milk and wool. The difference is small, and both flows are uncertain: the feed uptake builds on a single estimate for 1996 (Hegrenes & Asheim, 2006), and the manure on the survey of grazing time in 2018.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Manure N applied to soils and on pasture (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | ±20 %, normal | 64% | 62% | 1.00 | 1.00 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Grazing on Unmanaged Land](../forests_and_semi_natural_pool/flow_FS_OL_AG_MM_Grazing_Nmix.html) |
| Weeks on unmanaged land per head of cattle | Parameter | 5–12, lognormal | 11% | 22% | 0.19 | 0.28 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N2O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH3 emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NOx emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 4 more |
| Share of sheep grazing manure deposited on unmanaged land | Parameter | ±20 %, normal | 22% | 17% | 0.58 | 0.52 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N2O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH3 emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NOx emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 4 more |
| Held constant or averaged (utmark cattle) | Gap filling: held constant or averaged | ±15–35 %, lognormal, grows with distance to known year | 3% | – | 0.19 | – | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [N2O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH3 emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NOx emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 5 more |

### References

* Norwegian Environment Agency (2020). *Calculation of atmospheric nitrogen emissions from manure in Norwegian agriculture: Technical description of the revised model*. [https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf](https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf)
