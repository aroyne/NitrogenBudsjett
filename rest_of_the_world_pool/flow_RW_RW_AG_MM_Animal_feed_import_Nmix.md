---
layout: default
title: Animal Feed Import
parent: Rest of the world (RW)
nav_order: 1
---

# Animal Feed Import

<iframe src="../output_files/plots/RW_RW_AG_MM_Animal_feed_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Data on imported animal feed is taken from Landbruksdirektoratet and we have used the detailed composition of animal feed together with protein contents from FAO and specific Jones factors to get nitrogen contents.

 N content is applied separately by raw-material type: 0.0197 kgN/kg for carbohydrate raw materials and 0.0648 kgN/kg for protein raw materials. NIBIO Totalkalkylen gives statistics for total amount of feed to Norwegian farm animals between 1959 and 2026. Table 6.10 in (Bruholt & Longva, 1994)<!--cite:bruholt_jordbruksstatistikk_1994--> gives the domestically produced fraction of farm animal feed between 1985 and 1994. We combine these data to find values before 2000, using an average import fraction for 1995-1999.

Soy meal produced in Norway from imported soybeans is listed as a domestic raw material in Landbruksdirektoratet's statistics, but is counted here as imported feed, since the soybeans are imported (6–10 ktN/year). Before 2000, domestic soy meal is taken as 9.3 % (range 7.5–10.2 %, PERT) of total concentrate feed, its share in 2000–2004. The same amount is subtracted from MP.FP-AG.MM-Farm animal feed-Nmix.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Bruholt, L. & Longva, S. (1994). *Jordbruksstatistikk 1994*.
