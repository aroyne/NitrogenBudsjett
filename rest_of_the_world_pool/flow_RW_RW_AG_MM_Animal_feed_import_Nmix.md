---
layout: default
title: Animal Feed Import
parent: Rest of the world (RW)
nav_order: 1
---

# Animal Feed Import

<iframe src="../output_files/plots/RW_RW_AG_MM_Animal_feed_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-AG.MM-Animal feed import-Nmix** is the N in imported raw materials for concentrate feed for farm animals.
- Soy meal produced in Norway from imported soybeans is listed as a domestic raw material in Landbruksdirektoratet's statistics, but is counted here as imported feed, since the soybeans are imported (6–10 kt N/year). The same amount is subtracted from MP.FP-AG.MM-Farm animal feed-Nmix.

#### Data sources

- From 2000, imported raw materials for concentrate feed from Landbruksdirektoratet's statistics (Årlig råvareforbruk), with the detailed composition of the feed.
- NIBIO Totalkalkylen gives the total amount of purchased concentrate feed to Norwegian farm animals between 1959 and 2026.
- Table 6.10 in Bruholt & Longva (1994)<!--cite:bruholt_jordbruksstatistikk_1994--> gives the domestically produced fraction of farm animal feed between 1985 and 1994.

#### Assumptions

- N contents are calculated from the composition of the feed, protein contents from FAO and specific Jones factors, and applied separately by raw-material type: 0.0197 kg N/kg for carbohydrate raw materials and 0.0648 kg N/kg for protein raw materials (including soy meal).
- For 1985–1999, total purchased concentrate feed (NIBIO Totalkalkylen) is multiplied by the imported share (1 − the domestic share in Table 6.10 for 1985–1994, and the 1985–1994 mean for 1995–1999) and by the mean N content of the imported raw materials from 2000 onward.
- Before 2000, domestic soy meal is taken as 9.3% (range 7.5–10.2%, PERT) of total concentrate feed, its share in 2000–2004.

#### Interpretations and comparisons

- The flow is about 30–34 kt N per year in 1990–1999 and rises from 22 kt N in 2000 to about 40 kt N since 2010, as more of the concentrate feed is based on imported protein raw materials.
- 2000 is a low year in the concentrate feed statistics (24% imported raw materials, compared with 25–40% in the following years), not a break between the two sources.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Bruholt, L. & Longva, S. (1994). *Jordbruksstatistikk 1994*.
