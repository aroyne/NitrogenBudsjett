---
layout: default
title: Other Land (FS.OL)
parent: 4. Forests and semi-natural vegetation (FS)
nav_order: 2
has_children: true
---

# Subpool: Other land (FS.OL)


---

## Interactive Mass Balance Overview (1990-2023)

Hover over the chart to inspect specific streams, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_FS_OL.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

### Flows that are zero or neglected:

* **FS.OL-AT.AT-Emissions-NOx** is neglected because no values are reported in the CRLTAP/WebDab categories 4F1 and 4F2 (wetlands / other land NOx).
* Following Swedish NBB (Jutterström et al., 2020), we also consider denitrification in the OL pool to be negligible and therefore neglect **FS.OL-AT.AT-Emissions-N2** and **FS.OL-AT.AT-Emissions-N2O**.
* **Manure deposited directly by grazing animals on unmanaged land (utmark)** is not included as a flow into FS.OL. Norway's national inventory (UNFCCC CRT, Table 3.D, "Urine and dung deposited by grazing animals") reports total manure-N deposited during grazing (all land types combined) at approximately 25 ktN/year, calculated from livestock population, animal-specific excretion factors, and animal-specific fractions of time spent grazing (Norwegian Environment Agency, 2020). This total is not split between managed agricultural grazing land (innmark, which belongs to AG.SM's manure input, see AG.MM-AG.SM-Manure application-Nmix) and unmanaged land (utmark, which would belong here) in any source we have found. Apportioning it by species using typical Norwegian grazing practice (e.g. dairy cattle graze almost exclusively on innmark for milking logistics, while sheep spend a large share of the grazing season on utmark) gives a rough estimate of 9.5-13.8 ktN/year on utmark specifically - a similar order of magnitude to several flows this study does track explicitly. We have not included it because that species-level apportionment is our own estimate rather than a reported figure, and we are not aware of a data source that reports it directly.

### References

* Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation*.
* Norwegian Environment Agency (2020). *Calculation of atmospheric nitrogen emissions from manure in Norwegian agriculture: Technical description of the revised model*. [https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf](https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf)
