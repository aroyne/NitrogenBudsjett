---
layout: default
title: Grazing on Unmanaged Land
parent: Other Land (FS.OL)
nav_order: 1
---

# Grazing on Unmanaged Land

<iframe src="../output_files/plots/FS_OL_AG_MM_Grazing_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.OL-AG.MM-Grazing-Nmix** is the N in feed taken up by livestock and semi-domesticated reindeer grazing on utmark (outfield pasture).

#### Data sources

- SSB gives the number of livestock on utmark grazing ([table 12660](https://www.ssb.no/statbank/table/12660)), based on the applications for the production subsidy for animals on utmark: animals with at least 8 weeks on utmark up to 2008 and at least 5 weeks from 2009. The table covers all animals on utmark, not only those in grazing associations, and is available from 1995; sheep include lambs, and goats and horses are reported together.
- Hegrenes & Asheim (2006)<!--cite:hegrenes_verdi_2006-->, Table 1.2, after Garmo & Skurdal (1998), estimate that livestock took up 303 mill. FEm on utmark in 1996: 70% by sheep, 27% by cattle, 2% by goats and 1% by horses.
- The number of winter-fed sheep from SSB ([table 03710](https://www.ssb.no/statbank/table/03710)).
- For reindeer, the N in urine and dung deposited by reindeer on pasture (category 3.B.4.h.ii) in the UNFCCC Common Reporting Tables (CRT), Table 3.B(b), of the national greenhouse gas inventory.
- The statistics on organised grazing (Organisert beitebruk) are not used, since they grew in the early 1990s as more farmers joined grazing associations and so do not show the number of animals on utmark.

#### Assumptions

- Dividing each group's share of the 1996 feed uptake by the number of animals in 1996 gives about 95 FEm per sheep or lamb, 336 FEm per head of cattle and 105 FEm per goat or horse per grazing season; these are applied to all years.
- The FEm are converted to N with 150 g protein per FEm (as for innmark grazing in AG.SM-AG.MM-Fodder crops-Nmix) and the standard Jones factor (1/6.25).
- Reindeer graze only on utmark and are rarely given supplementary feed, so their feed uptake is set equal to the N they deposit as urine and dung (0.9–1.4 kt N per year); the N retained in growth is neglected.
- For 1990–1994, sheep are extrapolated back from 1995 with the change in the number of winter-fed sheep, and cattle, goats and horses are held at the 1995 level.

#### Interpretations and comparisons

- The flow is about 8.2–8.6 kt N in 1990–1996 and falls slowly to about 7.5 kt N in 2024, following the number of sheep on utmark (2.2 million in 1996, 1.8 million in 2024); the number of cattle on utmark has increased since 2017. Reindeer account for 0.9–1.4 kt N.
- The values for 1990–1994 follow the number of sheep and are less certain than later years.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| Protein per feed unit of grazing | Parameter | ±20 %, normal | 40% | 55% | [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html) |
| Feed units of sheep on unmanaged land, 1996 | Parameter | ±20 %, normal | 18% | 23% | none |
| Protein-to-N conversion factor (Jones factor) | Parameter | ±10 %, normal | 8% | 11% | [Live Animal Export](../agriculture_pool/flow_AG_MM_RW_RW_Live_animal_export_Nmix.html), [Fodder Crops Production](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html), [Seeds and Planting Material](../materials_and_products_pool/flow_MP_FP_AG_SM_Seeds_and_planting_material__Nmix.html), [Food Products to Consumers](../materials_and_products_pool/flow_MP_FP_HS_HS_Food_products_Nmix.html) and 1 more |
| Feed units of cattle on unmanaged land, 1996 | Parameter | ±20 %, normal | 3% | 6% | none |
| Livestock on unmanaged land (SSB 12660) | Registered data | ±5 %, normal, drawn per year | 3% | 3% | none |
| Held constant or averaged (utmark cattle) | Gap filling: held constant or averaged | ±15–35 %, lognormal, grows with distance to known year | 4% | – | [Manure Application](../agriculture_pool/flow_AG_MM_AG_SM_Manure_application_Nmix.html), [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [N2O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH3 emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html) and 5 more |
| Extrapolation (utmark sheep) | Gap filling: extrapolation | ±15–35 %, lognormal, grows with distance to known year | 22% | – | none |

### References

* Hegrenes, A. & Asheim, L. J. (2006). *Verdi av fôr frå utmarksbeite og sysselsetting i beitebaserte næringar*.
