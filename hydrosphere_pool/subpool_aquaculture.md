---
layout: default
title: Aquaculture (HY.AC)
parent: Hydrosphere (HY)
nav_order: 3
has_children: true
---

# Subpool: Aquaculture (HY.AC)


---

## Interactive Mass Balance Overview (1990-2023)

Hover over the chart to inspect specific streams, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_HY_AC.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

**Methodological note:** The conversion from feed N to fish production N (and the resulting waste feed and excretion, `HY.AC-HY.SW-Waste feed-Nmix` and `HY.AC-HY.SW-Excretia-Nmix`) is based on the apparent, whole-industry N retention reported for Norwegian salmon farming: about 26% in 1990 (Ytrestøyl et al., 2015), rising linearly (no intermediate data points are available) to the ~35.75% plateau measured from 2010 onward (Aas et al., 2022), and held constant at each end of that range outside 1990-2010. Aas et al. (2022) state explicitly that this figure is a mass balance for the whole production system, "including all losses of feed ingredients, feed and fish", and contrast it with controlled nutritional studies that isolate the fish's own metabolic efficiency on feed actually eaten, which is higher. We attribute the historical rise in apparent retention entirely to improved feed technology reducing feed waste, not to a change in the fish's own metabolic efficiency: the biological retention of feed actually eaten is held constant over time, derived from the two 2010-onward parameters where both apparent retention and feed waste are independently known (apparent retention = biological retention x (1 - feed waste), so biological retention = 35.75% / (1 - 3%) = 36.9%). The feed-waste fraction for any other year then follows directly from how far that year's apparent retention falls below this constant biological retention, without needing its own separate historical trend data - implying a feed-waste fraction of about 29% in 1990, falling to the measured 3% (Wang et al., 2013) by 2010. The same decomposition is used consistently for `MP.FP-HY.AC-Feed to coastal aquaculture-Nmix` and `RW.RW-HY.AC-Aquaculture feed import-Nmix`, which derive the same underlying feed budget from the other direction.

**Methodological note (feed import share):** `MP.FP-HY.AC-Feed to coastal aquaculture-Nmix` (the domestically supplied share of feed) and `RW.RW-HY.AC-Aquaculture feed import-Nmix` (the imported share) split the total feed budget above using an import fraction that varies by year rather than the constant 92% reported for 2020 (Aas et al., 2022). This is composed from two separately-trending components: the marine share of feed (fish meal and fish oil), which fell roughly linearly from 89.4% in 1990 to 22.4% in 2020 (Aas et al., 2022), and the import dependence of that marine share specifically, which rose from negligible in the mid-1980s (Norway was a net fishmeal exporter, (Deutsch et al., 2007)) to about two-thirds of consumption by 2000, held flat from there (back-solving from the measured 92% total import fraction and 22.4% marine share for 2020 gives an implied ~64% marine import dependence today, close enough to the 2000 level to treat as a plateau absent further data points). The remaining, non-marine (plant-based) share of feed is assumed 100% imported throughout, since Norway has no domestic capacity for protein-rich feed crops - so the overall import fraction keeps rising after 2000 even though the marine-specific import dependence has plateaued, simply because the always-imported non-marine share keeps growing. This gives an import fraction of about 11% in 1984-1985 (already nonzero purely from the small non-marine share importable at the time), rising to 76% by 2000 and 92% by 2020.

### Flows that are zero or neglected:

* **HY.AC-MP.FP-Freshwater fish and seafood-Nmix**, **HY.AC-HY.SW-Waste feed-Nmix** and **HY.AC-HY.SW-Excretia-Nmix** are set to zero...
* **HY.AC-AT.AT-Emissions-NH3** is set to zero assuming negligible ammonia emissions from these coastal marine cages.

### References

* Aas, T. S., Åsgård, T., & Ytrestøyl, T. (2022). Utilization of feed resources in the production of Atlantic salmon (Salmo salar) in Norway: An update for 2020. *Aquaculture Reports, 26*, 101316. [https://doi.org/10.1016/j.aqrep.2022.101316](https://doi.org/10.1016/j.aqrep.2022.101316)
* Deutsch, L., Gräslund, S., Folke, C., Troell, M., Huitric, M., Kautsky, N., & Lebel, L. (2007). Feeding aquaculture growth through globalization: Exploitation of marine ecosystems for fishmeal. *Global Environmental Change, 17*(2), 238-249. [https://doi.org/10.1016/j.gloenvcha.2006.08.004](https://doi.org/10.1016/j.gloenvcha.2006.08.004)
* Wang, X., Andresen, K., Handå, A., Jensen, B., Reitan, K., & Olsen, Y. (2013). Chemical composition and release rate of waste discharge from an Atlantic salmon farm with an evaluation of IMTA feasibility. *Aquaculture Environment Interactions, 4*(2), 147-162. [https://doi.org/10.3354/aei00079](https://doi.org/10.3354/aei00079)
* Ytrestøyl, T., Aas, T. S., & Åsgård, T. (2015). Utilisation of feed resources in production of Atlantic salmon (Salmo salar) in Norway. *Aquaculture, 448*, 365-374. [https://doi.org/10.1016/j.aquaculture.2015.06.023](https://doi.org/10.1016/j.aquaculture.2015.06.023)
