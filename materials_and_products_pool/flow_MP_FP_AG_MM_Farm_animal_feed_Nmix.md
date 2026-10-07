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
**MP.FP-AG.MM-Farm animal feed-Nmix** is feed to farm animals. We have used data on domestic feed supply from Landbruksdirektoratet (Landbruksdirektoratet, 2025)<!--cite:landbruksdirektoratet_kraftforstatistikk_2025--> and used the detailed composition of animal feed given in Eidem & Ruud (2022)<!--cite:eidem_for-_2022--> together with protein contents from FAO (2021)<!--cite:fao_annex_2021--> and specific Jones factors from FAO (2023)<!--cite:fao_chapter_2023--> to get nitrogen contents.

N content is applied separately by raw-material type, derived from the feed composition, protein content and Jones factor sources above: 0.0197 kgN/kg for carbohydrate raw materials and 0.0648 kgN/kg for protein raw materials. NIBIO Totalkalkylen gives statistics for total amount of feed to Norwegian farm animals between 1959 and 2026. Table 6.10 in Bruholt & Longva (1994)<!--cite:bruholt_jordbruksstatistikk_1994--> gives the domestically produced fraction of farm animal feed between 1985 and 1994. We combine these data to find values before 2000, using an average import fraction for 1995-1999. The 2000-2003 gap between the two source series is bridged with a linear interpolation. Soy meal produced in Norway from imported soybeans is listed as a domestic raw material in the statistics, but is counted as imported feed in RW.RW-AG.MM-Animal feed import-Nmix and subtracted here (see that flow).

Hohmann-Marriott (2025)<!--cite:hohmann-marriott_nitrogen_2025--> found the domestic supply of animal feed in 2010 to be around 35 ktN, based on FAO statistics of production, export and import of seed cake, which is a dominant ingredient in farm animal feed. This is less than we found when combining domestic and imported animal feed. *(Note: This estimate might be too low, as it leads to a surplus here and a deficit in the AG.MM pool).*

**How the numbers are derived**

- From 2004 the flow is based on Landbruksdirektoratet's concentrate feed statistics (Landbruksdirektoratet, 2025)<!--cite:landbruksdirektoratet_kraftforstatistikk_2025-->, which give the annual use of raw materials in compound feed from Norwegian feed mills, as reported by the feed producers, split into Norwegian and imported raw materials and by raw material group.
- The Norwegian carbohydrate raw materials (mainly cereals) are multiplied by 1.97% N and the Norwegian protein raw materials by 6.48% N; fat and mineral raw materials are not included.
- For 1985–1999 the total amount of purchased concentrate feed is taken from Totalkalkylen for jordbruket (Budsjettnemnda for jordbruket, 2025)<!--cite:bfj_totalkalkylen_2025-->, the sector account for Norwegian agriculture compiled by NIBIO, and multiplied by the domestically produced share (Bruholt & Longva (1994)<!--cite:bruholt_jordbruksstatistikk_1994--> for 1985–1994, 69.4% for 1995–1999) and by the average N content per tonne of Norwegian raw materials in 2004–2024.
- Norwegian-crushed soy meal is subtracted in all years: from the statistics from 2004, and as 9.3% of the concentrate feed before 2000.

**Interpretation**

- The flow varies between 9 and 18 kt N without a clear trend.
- Much of the year-to-year variation is consistent with the size of the Norwegian cereal harvest, which determines how much of the carbohydrate raw material can be sourced domestically: the flow is low in 2019 (10.4 kt N), after the drought in 2018, and in 2024 (13.7 kt N), after the poor harvest in 2023, and high in 2023 (17.6 kt N).
- In 2024 the total N in concentrate feed (this flow plus RW.RW-AG.MM-Animal feed import-Nmix) is about 54 kt N, of which about a quarter is domestic.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Budsjettnemnda for jordbruket (2025). *Totalkalkylen for jordbruket - statistikk*. [https://www.nibio.no/tjenester/totalkalkylen-statistikk](https://www.nibio.no/tjenester/totalkalkylen-statistikk)
* Bruholt, L. & Longva, S. (1994). *Jordbruksstatistikk 1994*.
* Eidem, B. & Ruud, T. (2022). *Fôr- og husdyrbaserte verdikjeder i norsk matproduksjon – nåsituasjon og begreper*.
* FAO (2021). Annex 1. Food composition tables. *FOOD BALANCE SHEETS. A handbook*. [https://www.fao.org/4/x9892e/X9892e05.htm](https://www.fao.org/4/x9892e/X9892e05.htm)
* FAO (2023). CHAPTER 2: METHODS OF FOOD ANALYSIS. *Food energy - methods of analysis and conversion factors*. [https://www.fao.org/4/y5022e/y5022e03.htm](https://www.fao.org/4/y5022e/y5022e03.htm)
* Hohmann-Marriott, M. F. (2025). A Nitrogen budget for Norway analysis of Nitrogen flows from societal and natural sources (1961–2020). *PLOS ONE, 20*(2), e0313598. [https://doi.org/10.1371/journal.pone.0313598](https://doi.org/10.1371/journal.pone.0313598)
* Landbruksdirektoratet (2025). *Kraftforstatistikk - årlig råvareforbruk*. [https://www.landbruksdirektoratet.no/nb/statistikk-og-utviklingstrekk/utvikling-i-jordbruket/kraftforstatistikk](https://www.landbruksdirektoratet.no/nb/statistikk-og-utviklingstrekk/utvikling-i-jordbruket/kraftforstatistikk)
