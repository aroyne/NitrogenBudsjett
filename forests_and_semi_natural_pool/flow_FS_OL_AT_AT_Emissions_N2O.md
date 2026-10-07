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

- **FS.OL-AT.AT-Emissions-N2O** is N2O from manure deposited by grazing animals on utmark (AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix).
- Following the Swedish NNB (Jutterström et al., 2020)<!--cite:jutterstrom_swedish_2020-->, denitrification in the soils of other land is considered negligible.

#### Data sources

- N2O from grazing manure in the UNFCCC Common Reporting Tables (CRT), Table 3.D, of the national greenhouse gas inventory ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)): direct N2O from urine and dung deposited by grazing animals (3.D.1.c), and the fractions and implied emission factors for indirect N2O from volatilisation (FracGASPRP, 3.D.2.a) and leaching (FracLEACH, 3.D.2.b). The inventory calculates these with IPCC emission factors and reports them for all grazing land combined.

#### Assumptions

- The flow is the utmark share of the direct N2O from grazing manure plus the indirect N2O from the volatilisation and leaching of the manure deposited on utmark. The utmark share is the grazing manure per animal category (CRT Table 3.B(b)) weighted with the share of each category's grazing time spent on utmark in 2018 (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79): sheep 51%, goats 54% and horses 16% (each ±20%), reindeer 100% and farmed deer 0%. For cattle the survey shares (dairy cows 16%, suckler cows 30%, other cattle 32%) would give more manure on utmark than the feed taken up on utmark (FS.OL-AG.MM-Grazing-Nmix) allows. The cattle manure on utmark is therefore the number of cattle on utmark (SSB table 12660, which counts animals with at least 5 weeks on utmark; the 1995 level before 1995) times the average N excretion of cattle other than dairy cows (CRT Table 3.B(b); most cattle on utmark are beef cows and young stock) times 8 weeks on utmark (range 5–12, PERT) out of 52, at most the grazing manure of cattle. This is 8–17% of the cattle grazing manure. In total this gives 26–33% of the grazing manure. The shares are held at the 2018 survey values for all years; before 2009 the subsidy rules required a longer grazing period on utmark (eight instead of five weeks), so the share may have been somewhat higher.
- The same amount is removed from AG.SM-AT.AT-Emissions-N2O.

#### Interpretations and comparisons

- The flow is small, about 0.07 kt N per year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation*.
