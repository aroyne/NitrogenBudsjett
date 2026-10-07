---
layout: default
title: Farm Animal Feed
parent: Food and Feed Processing (MP.FP)
nav_order: 1
---

# Farm Animal Feed

<iframe src="../output_files/plots/MP_FP_AG_MM_Farm_animal_feed_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-AG.MM-Farm animal feed-Nmix** is domestically produced concentrate feed to farm animals.
- Soy meal produced in Norway from imported soybeans is not included; it is counted as imported feed in RW.RW-AG.MM-Animal feed import-Nmix (see that flow).

#### Data sources

- Landbruksdirektoratet's concentrate feed statistics (Landbruksdirektoratet, 2025)<!--cite:landbruksdirektoratet_kraftforstatistikk_2025-->, which give the annual use of raw materials in compound feed from Norwegian feed mills, as reported by the feed producers, split into Norwegian and imported raw materials and by raw material group.
- The detailed composition of animal feed in Eidem & Ruud (2022)<!--cite:eidem_for-_2022-->, protein contents from FAO (2021)<!--cite:fao_annex_2021--> and specific Jones factors from FAO (2023)<!--cite:fao_chapter_2023-->.
- Total purchased concentrate feed for 1959–2026 from Totalkalkylen for jordbruket (Budsjettnemnda for jordbruket, 2025)<!--cite:bfj_totalkalkylen_2025-->, the sector account for Norwegian agriculture compiled by NIBIO.
- Table 6.10 in Bruholt & Longva (1994)<!--cite:bruholt_jordbruksstatistikk_1994--> gives the domestically produced fraction of farm animal feed between 1985 and 1994.

#### Assumptions

- N content is applied separately by raw-material type, derived from the feed composition, protein content and Jones factor sources above: 1.97% (0.0197 kg N/kg) for carbohydrate raw materials (mainly cereals) and 6.48% (0.0648 kg N/kg) for protein raw materials; fat and mineral raw materials are not included.
- From 2000 the Norwegian raw materials in Landbruksdirektoratet's statistics are used. In these statistics, soy meal crushed in Norway from imported soybeans is already listed among the imported raw materials.
- For 1985–1999 the total amount of purchased concentrate feed from Totalkalkylen is multiplied by the domestically produced share (Bruholt & Longva (1994) for 1985–1994, the average of 69.4% for 1995–1999) and by the average N content per tonne of Norwegian raw materials in 2004–2024.
- Soy meal crushed in Norway is counted as imported in both sources: in Landbruksdirektoratet's statistics from 2000, and in Table 6.10 in Bruholt & Longva (1994), which lists all soybean meal as imported (42 600 t in 1994).
- The domestic shares in Table 6.10 include concentrate feed for fish farming (92 900 t in 1985, 331 200 t in 1994, 17% of the total in 1994), which cannot be separated out. Fish feed was largely herring meal, mostly domestic, so the domestic share for farm animals alone was probably somewhat lower than the share used.

#### Interpretations and comparisons

- The flow varies between 19 and 26 kt N without a clear trend.
- Much of the year-to-year variation is consistent with the size of the Norwegian cereal harvest, which determines how much of the carbohydrate raw material can be sourced domestically: the flow is low in 2019 (18.6 kt N), after the drought in 2018, and in 2024 (20.4 kt N), after the poor harvest in 2023, and high in 2023 (23.8 kt N).
- In 2024 the total N in concentrate feed (this flow plus RW.RW-AG.MM-Animal feed import-Nmix) is about 54 kt N, of which almost 40% is domestic.
- Hohmann-Marriott (2025)<!--cite:hohmann-marriott_nitrogen_2025--> found the domestic supply of animal feed in 2010 to be around 35 kt N, based on FAO statistics of production, export and import of seed cake, which is a dominant ingredient in farm animal feed. This is less than we found when combining domestic and imported animal feed. *(Note: This estimate might be too low, as it leads to a surplus here and a deficit in the AG.MM pool).*
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Budsjettnemnda for jordbruket (2025). *Totalkalkylen for jordbruket - statistikk*. [https://www.nibio.no/tjenester/totalkalkylen-statistikk](https://www.nibio.no/tjenester/totalkalkylen-statistikk)
* Bruholt, L. & Longva, S. (1994). *Jordbruksstatistikk 1994*.
* Eidem, B. & Ruud, T. (2022). *Fôr- og husdyrbaserte verdikjeder i norsk matproduksjon – nåsituasjon og begreper*.
* FAO (2021). Annex 1. Food composition tables. *FOOD BALANCE SHEETS. A handbook*. [https://www.fao.org/4/x9892e/X9892e05.htm](https://www.fao.org/4/x9892e/X9892e05.htm)
* FAO (2023). CHAPTER 2: METHODS OF FOOD ANALYSIS. *Food energy - methods of analysis and conversion factors*. [https://www.fao.org/4/y5022e/y5022e03.htm](https://www.fao.org/4/y5022e/y5022e03.htm)
* Hohmann-Marriott, M. F. (2025). A Nitrogen budget for Norway analysis of Nitrogen flows from societal and natural sources (1961–2020). *PLOS ONE, 20*(2), e0313598. [https://doi.org/10.1371/journal.pone.0313598](https://doi.org/10.1371/journal.pone.0313598)
* Landbruksdirektoratet (2025). *Kraftforstatistikk - årlig råvareforbruk*. [https://www.landbruksdirektoratet.no/nb/statistikk-og-utviklingstrekk/utvikling-i-jordbruket/kraftforstatistikk](https://www.landbruksdirektoratet.no/nb/statistikk-og-utviklingstrekk/utvikling-i-jordbruket/kraftforstatistikk)
