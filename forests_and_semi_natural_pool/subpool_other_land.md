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

Hover over the chart to inspect specific flows, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_FS_OL.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
### Flows that are zero or neglected:

* NO<sub>x</sub> from the soils of other land is neglected because no values are reported in the CRLTAP/WebDab categories 4F1 and 4F2 (wetlands / other land).
* Following Swedish NBB (Jutterström et al., 2020)<!--cite:jutterstrom_swedish_2020-->, we also consider denitrification in the OL pool to be negligible and therefore neglect **FS.OL-AT.AT-Emissions-N2**.

### Manure from grazing on unmanaged land

* Norway's national inventory (UNFCCC CRT, Table 3.D, "Urine and dung deposited by grazing animals") reports total manure N deposited during grazing (all land types combined) at about 23–27 kt N per year, calculated from livestock population, animal-specific excretion factors and animal-specific fractions of time spent grazing (Miljødirektoratet, 2020)<!--cite:miljodirektoratet_manure_2020-->. The inventory does not split this between managed agricultural grazing land (innmark) and unmanaged land (utmark), and the NH<sub>3</sub> and N<sub>2</sub>O from grazing are also reported for all land types combined.
* We split it with the share of each animal category's grazing time spent on unmanaged land in SSB's survey of manure use in 2018 (Kolle & Oguz-Alper, 2020, Table A79)<!--cite:ssb_gjodselressurser_2020-->, weighted with the grazing manure per category in CRT Table 3.B(b); reindeer are counted fully on unmanaged land. For cattle, the manure on unmanaged land is calculated from the number of cattle on unmanaged land (SSB table 12660), their N excretion and the weeks spent on unmanaged land, since the survey shares would give more cattle manure on unmanaged land than the feed taken up there allows. This gives 26–30% on unmanaged land, about 7 kt N per year, in **AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix**.
* The NH<sub>3</sub>, NO<sub>x</sub> and N<sub>2</sub>O from this manure are the unmanaged-land share of the inventory's emissions from grazing, and are counted as FS.OL-AT.AT emissions instead of AG.SM-AT.AT. The leaching from it is part of the runoff from upland areas in TEOTIL3 (FS.OL-HY.SW-Leaching-Nmix).
* The manure deposited on unmanaged land is at most 90% of the feed taken up on unmanaged land (FS.OL-AG.MM-Grazing-Nmix, 7.5–8.6 kt N including reindeer), since part of the N in the feed is retained in growth, milk and wool (10%, range 5–15%); this cap applies from 2000. Both are uncertain: the feed uptake builds on a single estimate for 1996 (Hegrenes & Asheim, 2006)<!--cite:hegrenes_verdi_2006-->, and the manure on the inventory's excretion and the survey of grazing time.

### Flows added or changed compared with Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->:

* **FS.OL-HS.HS-Game meat-Nmix** (wild reindeer) is not in the guidelines. It has been added for consistency with the game meat from forests, although it is below 0.01 kt N per year.
* **FS.OL-AG.MM-Grazing-Nmix** is not in the guidelines. It has been added because livestock grazing on unmanaged land (utmark) takes up N from FS.OL. It is the counterpart of **AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix**, which is also not in the guidelines (see below).
* **FS.OL-AT.AT-Emissions-NH3**: the guidelines list only NO<sub>x</sub>, N<sub>2</sub>O and N<sub>2</sub> for emissions from FS.OL. NH<sub>3</sub> has been added for the emissions from manure deposited by grazing animals on unmanaged land (see below).
* **FS.OL-HY.SW-Leaching-Nmix** goes to groundwater (HY.GW) in Schäppi et al. (2025). We do not include the groundwater subpool (see the [hydrosphere pool page](../hydrosphere_pool/pool_hydrosphere.html)), so the flow goes to surface water (HY.SW).

<!-- MANUAL:POOL_TEXT:END -->

### References

* <span id="ref-hegrenes_verdi_2006" data-cite="Hegrenes &amp; Asheim" data-year="2006"></span>Hegrenes, A., & Asheim, L. J. (2006). *Verdi av fôr frå utmarksbeite og sysselsetting i beitebaserte næringar*. NILF.
* <span id="ref-jutterstrom_swedish_2020" data-cite="Jutterström et al." data-year="2020"></span>Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation* (C 549). IVL Swedish Environmental Research Institute.
* <span id="ref-miljodirektoratet_manure_2020" data-cite="Miljødirektoratet" data-year="2020"></span>Miljødirektoratet (2020). *Calculation of atmospheric nitrogen emissions from manure in Norwegian agriculture: Technical description of the revised model* (M-1848). [miljodirektoratet.no](https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf)
* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
* <span id="ref-ssb_gjodselressurser_2020" data-cite="Kolle &amp; Oguz-Alper" data-year="2020"></span>Kolle, S. O., & Oguz-Alper, M. (2020). *Bruk av gjødselressurser i jordbruket 2018. Metodebeskrivelse og resultater fra en utvalgsbasert undersøkelse* (Rapporter 2020/9). Statistisk sentralbyrå.
