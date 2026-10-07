---
layout: default
title: Food Products to Consumers
parent: Food and Feed Processing (MP.FP)
nav_order: 3
---

# Food Products to Consumers

<iframe src="../output_files/plots/MP_FP_HS_HS_Food_products_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**MP.FP-HS.HS-Food products-Nmix** is food products consumed by private households and pets. Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> advises using FAO statistics on food availability for human food consumption, but this only gives data back to 2009. The values in this statistic gives a bit more than 40 ktN per year. We have chosen to use data on food sales to consumers from SSB (table 13695: Næringsinnhald per dag frå selde mat- og drikkevarer 2018 – 2023, table 10249: Forbrukte mengder av mat- og drikkevarer per person per år, etter varegruppe (kg/liter) (avslutta serie) 1999 – 2012 and table 06376: Forbrukte mengder av mat- og drikkevarer per person per år, etter varegruppe (kg/liter) (avslutta serie) 1958-1959 - 1996-1998). The latter series gives values for 3 year averages, and we have assigned the averages to each individual year.

From 2018 the statistics are given in terms of protein content. Previous to this, the amounts of various food categories are given, and we have used protein contents found in Matvaretabellen (Mattilsynet, 2006)<!--cite:mattilsynet_matvaretabellen_2006--> as this reflects common foods found in Norwegian retail. Population data are taken from SSB and we have used the Jones factor of 6.25 for nitrogen content in protein.

For pet food, we have assumed (based on available statistics) that cats and dogs consume > 90 % of pet food. Horses are accounted for under the agriculture pool. The nitrogen intake per animal per year is taken from Table 19 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> and the number of cats and dogs between 1985 and 2025 is assumed using a trendline based on available statistics from a variety of sources.

The food statistics above count food bought by households, so food that leaves MP.FP but is wasted before it is bought is not in them, while food wasted in households after it is bought is already included. We therefore add food waste in wholesale, retail, food service, catering and education/care institutions, using per-sector 2021 tonnage and the 2015-to-2021 change per capita reported by Stensgård et al. (2023)<!--cite:stensgard_kartleggingsrapport_2023--> (Norway's food waste reduction agreement, "Bransjeavtalen", uses 2015 as its baseline year), linearly interpolated between the two years and held constant outside that range. Household food waste reported by Stensgård et al. (2023) is not added. The waste is converted to N using the mean N content of Norway's total food supply basket across 2010-2023 (FAOSTAT Food Balance Sheets "Food" quantity by item, weighted by N content per Table 21 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->). Food waste occurring upstream of MP.FP (agriculture, seafood landing) or internally within the food industry is excluded, since both are already covered by other flows. Food eaten outside the home (restaurants, canteens, institutions) and cross-border shopping are not covered by the food statistics and are therefore missing from this flow, except for the waste from food service, catering and institutions.

**How the numbers are derived**

- From 2018 the flow builds on SSB's diet statistics ([Kosthald](https://www.ssb.no/kosthald), [table 13695](https://www.ssb.no/statbank/table/13695)), which are based on the edible amount of food and drink sold in a sample of Norwegian grocery stores, weighted up to all grocery stores.
- According to SSB, the statistics do not include food bought at kiosks, petrol stations, cafés, restaurants, canteens or institutions or through cross-border shopping, and food wasted after it is sold is not deducted.
- Protein per person per day is multiplied by 365, by the population on 1 January ([table 06913](https://www.ssb.no/statbank/table/06913)) and divided by 6.25.
- In April 2026 SSB republished 2018–2023 with adjusted weights, which lowered the series by about 7–8%.
- For 1984–2012 the source is the household budget survey ([Forbruksundersøkelsen](https://www.ssb.no/inntekt-og-forbruk/forbruk/statistikk/forbruksundersokelsen); tables [10249](https://www.ssb.no/statbank/table/10249) and [06376](https://www.ssb.no/statbank/table/06376)), which records the quantities of food bought by households; for 1997–2009 SSB pooled three survey years and labels each period with its last year, so each value is placed in the middle year of its period.
- Years without survey data (1986–1988, 1992–1995, 2009–2011 and 2013–2017) are filled with the mean of the neighbouring survey periods or with a linear trend.
- The pet food term uses trend lines for the number of dogs (about 0.58 million in 2024) and cats (about 0.76 million in 2024) and 4.73 and 3.04 kg N per animal per year.

**Interpretation**

- The flow rises from about 26 kt N in 1990 to 29–31 kt N in 2019–2024.
- In 2024 it consists of about 24 kt N in food bought by households, 5 kt N in pet food and 1.2 kt N in food wasted in wholesale, retail, food service, catering and institutions.
- The increase is driven by population growth (4.2 million in 1990, 5.6 million in 2024) and the growing number of pets.
- N in food per person decreases from about 5.1 to 4.3 kg N per year (about 73 g protein per person per day in 2024), but part of this change may come from the change of data source in 2018.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Mattilsynet (2006). *Matvaretabellen*. [https://www.matvaretabellen.no](https://www.matvaretabellen.no)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
* Stensgård, A., Berntsen, I. C., Hohle, S. M., & Callewaert, P. (2023). *Kartleggingsrapport for matbransjen og forbrukerleddet*.
