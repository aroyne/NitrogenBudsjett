---
layout: default
title: Other Land (FS.OL)
parent: 4. Forests and semi-natural vegetation (FS)
nav_order: 2
has_children: true
---

# Subpool: Other land (FS.OL)


---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific streams, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_FS_OL.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
### Flows that are zero or neglected:

* **FS.OL-AT.AT-Emissions-NOx** from the soils themselves is neglected because no values are reported in the CRLTAP/WebDab categories 4F1 and 4F2 (wetlands / other land NOx). The NOx from manure deposited by grazing animals on utmark is included in this flow (see below).
* Following Swedish NBB (Jutterström et al., 2020)<!--cite:jutterstrom_swedish_2020-->, we also consider denitrification in the OL pool to be negligible and therefore neglect **FS.OL-AT.AT-Emissions-N2**. **FS.OL-AT.AT-Emissions-N2O** only includes N2O from manure deposited by grazing animals on utmark.

### Manure from grazing on unmanaged land

* Norway's national inventory (UNFCCC CRT, Table 3.D, "Urine and dung deposited by grazing animals") reports total manure N deposited during grazing (all land types combined) at about 23–27 kt N per year, calculated from livestock population, animal-specific excretion factors and animal-specific fractions of time spent grazing (Norwegian Environment Agency, 2020)<!--cite:miljodirektoratet_manure_2020-->. The inventory does not split this between managed agricultural grazing land (innmark) and unmanaged land (utmark), and the NH3 and N2O from grazing are also reported for all land types combined.
* We split it with the share of each animal category's grazing time spent on utmark in SSB's survey of manure use in 2018 (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79), weighted with the grazing manure per category in CRT Table 3.B(b); reindeer are counted fully on utmark. This gives 35–39% on utmark, about 9 kt N per year, in **AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix**.
* The NH3, NOx and N2O from this manure are the utmark share of the inventory's emissions from grazing, and are counted as FS.OL-AT.AT emissions instead of AG.SM-AT.AT. The leaching from it is part of the runoff from upland areas in TEOTIL3 (FS.OL-HY.SW-Leaching-Nmix).
* The manure deposited on utmark (about 9 kt N) is larger than the feed taken up on utmark (FS.OL-AG.MM-Grazing-Nmix, about 6.5 kt N), which it cannot be in reality; at least one of the two is uncertain. The feed uptake builds on a single estimate for 1996 (Hegrenes & Asheim, 2006), while the manure builds on the inventory's excretion and the survey of grazing time.
<!-- MANUAL:POOL_TEXT:END -->

### References

* Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation*.
* Norwegian Environment Agency (2020). *Calculation of atmospheric nitrogen emissions from manure in Norwegian agriculture: Technical description of the revised model*. [https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf](https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf)
