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
#### Flow description

- **MP.FP-HS.HS-Food products-Nmix** is food products consumed by private households and pets.
- The food statistics count food bought by households, so food that leaves MP.FP but is wasted before it is bought is not in them, while food wasted in households after it is bought is already included. We therefore add food waste in wholesale, retail, food service, catering and education/care institutions; household food waste is not added.
- Food waste occurring upstream of MP.FP (agriculture, seafood landing) or internally within the food industry is excluded, since both are already covered by other flows.
- Food eaten outside the home (restaurants, canteens, institutions) and cross-border shopping are not covered by the food statistics and are therefore missing from this flow, except for the waste from food service, catering and institutions.
- Horses are accounted for under the agriculture pool.

#### Data sources

- From 2018, SSB's diet statistics ([Kosthald](https://www.ssb.no/kosthald), [table 13695](https://www.ssb.no/statbank/table/13695): Næringsinnhald per dag frå selde mat- og drikkevarer), which are based on the edible amount of food and drink sold in a sample of Norwegian grocery stores, weighted up to all grocery stores, and given in terms of protein content. According to SSB, the statistics do not include food bought at kiosks, petrol stations, cafés, restaurants, canteens or institutions or through cross-border shopping, and food wasted after it is sold is not deducted. In April 2026 SSB republished 2018–2023 with adjusted weights, which lowered the series by about 7–8%.
- For 1984–2012, the household budget survey ([Forbruksundersøkelsen](https://www.ssb.no/inntekt-og-forbruk/forbruk/statistikk/forbruksundersokelsen); tables [10249](https://www.ssb.no/statbank/table/10249) “Forbrukte mengder av mat- og drikkevarer per person per år, etter varegruppe (kg/liter)” 1999–2012 and [06376](https://www.ssb.no/statbank/table/06376), the same for 1958–1959 to 1996–1998), which records the quantities of food bought by households; for 1997–2009 SSB pooled three survey years and labels each period with its last year. The older series gives values for 3-year averages.
- Protein contents of food categories from Matvaretabellen (Mattilsynet, 2006)<!--cite:mattilsynet_matvaretabellen_2006-->, as this reflects common foods found in Norwegian retail.
- Population on 1 January from SSB ([table 06913](https://www.ssb.no/statbank/table/06913)).
- Nitrogen intake per cat and dog per year from Table 19 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, and the number of cats and dogs from available statistics from a variety of sources.
- Food waste per sector: 2021 tonnage and the 2015-to-2021 change per capita reported by Stensgård et al. (2023)<!--cite:stensgard_kartleggingsrapport_2023--> (Norway's food waste reduction agreement, "Bransjeavtalen", uses 2015 as its baseline year).
- Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> advises using FAO statistics on food availability for human food consumption, but this only gives data back to 2009. The values in this statistic give a bit more than 40 kt N per year.

#### Assumptions

- Protein per person per day is multiplied by 365 and by the population, and divided by the Jones factor 6.25. Before 2018 the amounts of the food categories are multiplied by their protein contents.
- The 3-year averages of the older series are assigned to each individual year, and each value is placed in the middle year of its period.
- Years without survey data (1986–1988, 1992–1995, 2009–2011 and 2013–2017) are filled with the mean of the neighbouring survey periods or with a linear trend.
- For pet food, we have assumed (based on available statistics) that cats and dogs consume >90% of pet food. The number of cats and dogs between 1985 and 2025 is taken from trend lines (about 0.58 million dogs and 0.76 million cats in 2024), with 4.73 and 3.04 kg N per animal per year.
- Food waste in wholesale, retail, food service, catering and institutions is linearly interpolated between 2015 and 2021 and held constant outside that range. The waste is converted to N using the mean N content of Norway's total food supply basket across 2010–2023 (FAOSTAT Food Balance Sheets "Food" quantity by item, weighted by N content per Table 21 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->).

#### Interpretations and comparisons

- The flow rises from about 26 kt N in 1990 to 29–31 kt N in 2019–2024.
- In 2024 it consists of about 24 kt N in food bought by households, 5 kt N in pet food and 1.2 kt N in food wasted in wholesale, retail, food service, catering and institutions.
- The increase is driven by population growth (4.2 million in 1990, 5.6 million in 2024) and the growing number of pets.
- N in food per person decreases from about 5.1 to 4.3 kg N per year (about 73 g protein per person per day in 2024), but part of this change may come from the change of data source in 2018.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Mattilsynet (2006). *Matvaretabellen*. [https://www.matvaretabellen.no](https://www.matvaretabellen.no)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
* Stensgård, A., Berntsen, I. C., Hohle, S. M., & Callewaert, P. (2023). *Kartleggingsrapport for matbransjen og forbrukerleddet*.
