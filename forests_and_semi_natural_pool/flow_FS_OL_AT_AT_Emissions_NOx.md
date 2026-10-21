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

- **FS.OL-AT.AT-Emissions-NOx** is NOx from manure deposited by grazing animals on utmark (AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix).
- NOx from the soils of other land is neglected because no values are reported in the CRLTAP categories 4F1 and 4F2 (wetlands / other land).

#### Data sources

- Emissions from grazing animals (NFR 3Da3) reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), calculated in the national inventory with the manure model: N deposited during grazing multiplied by emission factors ([Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)).
- The inventory reports the emissions from grazing for all land types combined; it does not split innmark and utmark.

#### Assumptions

- The flow is the utmark share of the NOx from grazing animals (3Da3). The utmark share is the grazing manure per animal category (CRT Table 3.B(b)) weighted with the share of each category's grazing time spent on utmark in 2018 (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79): sheep 51%, goats 54% and horses 16% (each ±20%), reindeer 100% and farmed deer 0%. For cattle the survey shares (dairy cows 16%, suckler cows 30%, other cattle 32%) would give more manure on utmark than the feed taken up on utmark (FS.OL-AG.MM-Grazing-Nmix) allows. The cattle manure on utmark is therefore the number of cattle on utmark (SSB table 12660, which counts animals with at least 5 weeks on utmark; the 1995 level before 1995) times the average N excretion of cattle other than dairy cows (CRT Table 3.B(b); most cattle on utmark are beef cows and young stock) times 8 weeks on utmark (range 5–12, PERT) out of 52, at most the grazing manure of cattle. This is 8–17% of the cattle grazing manure. In total this gives 26–33% of the grazing manure. The shares are held at the 2018 survey values for all years; before 2009 the subsidy rules required a longer grazing period on utmark (eight instead of five weeks), so the share may have been somewhat higher.
- The same amount is removed from AG.SM-AT.AT-Emissions-NOx.

#### Interpretations and comparisons

- The flow is small, about 0.1 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NOx, Urine and dung deposited by grazing animals (NFR 3Da3) | Inventory with published uncertainty | −50.6/+102.4 %, lognormal | 96% | 96% | 1.00 | 1.00 | [NOx emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) |
| Weeks on unmanaged land per head of cattle | Parameter | 5–12, lognormal | 1% | 2% | 0.19 | 0.28 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [N2O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH3 emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html) and 4 more |
| Share of sheep grazing manure deposited on unmanaged land | Parameter | ±20 %, normal | 2% | 2% | 0.58 | 0.52 | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [N2O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH3 emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html) and 4 more |

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
