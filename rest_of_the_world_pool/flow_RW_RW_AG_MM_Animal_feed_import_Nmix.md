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
- Soy meal produced in Norway from imported soybeans is counted here as imported feed, since the soybeans are imported. Landbruksdirektoratet's statistics (from 2000) list it among the imported raw materials, and so does Table 6.10 in Bruholt & Longva (1994) (all soybean meal imported, 42 600 t in 1994).

#### Data sources

- From 2000, imported raw materials for concentrate feed from Landbruksdirektoratet's statistics (Årlig råvareforbruk), with the detailed composition of the feed.
- NIBIO Totalkalkylen gives the total amount of purchased concentrate feed to Norwegian farm animals between 1959 and 2026.
- Table 6.10 in Bruholt & Longva (1994)<!--cite:bruholt_jordbruksstatistikk_1994--> gives the domestically produced fraction of farm animal feed between 1985 and 1994.

#### Assumptions

- N contents are calculated from the composition of the feed, protein contents from FAO and specific Jones factors, and applied separately by raw-material type: 0.0197 kg N/kg for carbohydrate raw materials and 0.0648 kg N/kg for protein raw materials (including soy meal).
- For 1985–1999, total purchased concentrate feed (NIBIO Totalkalkylen) is multiplied by the imported share (1 − the domestic share in Table 6.10 for 1985–1994, and the 1985–1994 mean for 1995–1999) and by the mean N content of the imported raw materials from 2000 onward.
- The domestic shares in Table 6.10 include concentrate feed for fish farming (92 900 t in 1985, 331 200 t in 1994, 17% of the total in 1994), which cannot be separated out. Fish feed was largely herring meal, mostly domestic, so the domestic share for farm animals alone was probably somewhat lower, and the imported share somewhat higher, than the share used.

#### Interpretations and comparisons

- The flow is about 16–25 kt N per year in 1990–1999 and rises from 14 kt N in 2000 to 33–37 kt N since 2012, as more of the concentrate feed is based on imported protein raw materials.
- 2000 is a low year in the concentrate feed statistics (24% imported raw materials, compared with 25–40% in the following years), not a break between the two sources.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of protein feed ingredients | Parameter | ±10 %, normal | 6% | 64% | 0.77 | 0.75 | [Farm Animal Feed](../materials_and_products_pool/flow_MP_FP_AG_MM_Farm_animal_feed_Nmix.html) |
| Concentrate feed sales (Norwegian Agriculture Agency) | Registered data | ±5 %, normal, drawn per year | – | 29% | – | 1.00 | [Farm Animal Feed](../materials_and_products_pool/flow_MP_FP_AG_MM_Farm_animal_feed_Nmix.html) |
| N content of carbohydrate feed ingredients | Parameter | ±10 %, normal | 1% | 7% | 0.23 | 0.25 | [Farm Animal Feed](../materials_and_products_pool/flow_MP_FP_AG_MM_Farm_animal_feed_Nmix.html) |
| Totalkalkylen for agriculture (NIBIO) (concentrate) | Modelled statistics | ±30 %, normal | 93% | – | 1.00 | – | [Farm Animal Feed](../materials_and_products_pool/flow_MP_FP_AG_MM_Farm_animal_feed_Nmix.html) |

### References

* Bruholt, L. & Longva, S. (1994). *Jordbruksstatistikk 1994*.
