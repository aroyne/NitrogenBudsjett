---
layout: default
title: Farm Animal Feed
parent: Food and Feed Processing (MP.FP)
nav_order: 1
---

# Farm Animal Feed

![MP.FP-AG.MM-Farm animal feed-Nmix](../output_files/plots/MP_FP_AG_MM_Farm_animal_feed_Nmix.png)

### Flow Description
**MP.FP-AG.MM-Farm animal feed-Nmix** is feed to farm animals. We have used data on domestic feed supply from Landbruksdirektoratet (Landbruksdirektoratet, 2025b) and used the detailed composition of animal feed given in (Eidem & Ruud, 2022) together with protein contents from (FAO, 2021) and specific Jones factors from (FAO, 2023) to get nitrogen contents.

Based on the Landbruksdirektoratet data, the N content of the total amount of feed is 0.02 kgN/kg feed. NIBIO Totalkalkylen gives statistics for total amount of feed to Norwegian farm animals between 1959 and 2026. Table 6.10 in (Bruholt & Longva, 1994) gives the domestically produced fraction of farm animal feed between 1985 and 1994. We combine these data to find values before 2000, using an average import fraction for 1995-1999.

(Hohmann-Marriott, 2025) found the domestic supply of animal feed in 2010 to be around 35 ktN, based on FAO statistics of production, export and import of seed cake, which is a dominant ingredient in farm animal feed. This is less than we found when combining domestic and imported animal feed. *(Note: This estimate might be too low, as it leads to a surplus here and a deficit in the AG.MM pool).*


### References

{% bibliography --cited %}
