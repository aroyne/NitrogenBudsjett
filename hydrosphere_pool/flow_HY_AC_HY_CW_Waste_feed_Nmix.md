---
layout: default
title: Waste feed
parent: Aquaculture (HY.AC)
nav_order: 2
---

# Waste feed

<iframe src="../output_files/plots/HY_AC_HY_CW_Waste_feed_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HY.AC-HY.CW-Waste feed-Nmix** is the N in feed that is not eaten by the farmed fish and is lost to coastal water.

#### Data sources

- Sold farmed salmon and trout by year from Fiskeridirektoratet (2025)<!--cite:fiskeridirektoratet_06002_2025--> (table A.06.002, 1994 onward; historical compilation for 1984–1993).

#### Assumptions

- Harvested fish are multiplied by 2.8% N (Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 254).
- Feed N is the harvested N divided by an apparent whole-system retention that rises linearly from 26% in 1990 (Ytrestøyl et al., 2015<!--cite:ytrestoyl_utilisation_2015-->) to 35.75% in 2010 (Aas et al., 2022<!--cite:aas_utilization_2022-->) and is constant after. The rise is attributed to less feed waste, so the biological retention of eaten feed is held constant and the feed waste falls from about 29% of the feed in 1990 to the measured 3% (Wang et al., 2013<!--cite:wang_chemical_2013-->) in 2010; see the [methodological note](subpool_aquaculture.html) on the Aquaculture (HY.AC) subpool page.
- This flow is the feed N times the feed-waste fraction (see the [methodological note](subpool_aquaculture.html) for how the fraction is derived from the apparent whole-fish retention trend).

#### Interpretations and comparisons

- The flow rises to about 7.4 kt N around 2000, falls to 2.5 kt N in 2010 as the feed waste fraction falls, and then rises with production to about 4 kt N in 2024.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Aas, T. S., Åsgård, T., & Ytrestøyl, T. (2022). Utilization of feed resources in the production of Atlantic salmon (Salmo salar) in Norway: An update for 2020. *Aquaculture Reports, 26*, 101316. [https://doi.org/10.1016/j.aqrep.2022.101316](https://doi.org/10.1016/j.aqrep.2022.101316)
* Fiskeridirektoratet (2025). *A.06.002 Matfisk. Salg av laks, regnbueørret og ørret, etter art (Fylke) (1994-2024)*. [https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__A%20Akvakultur__A.06%20Salg/A06002.px/](https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__A%20Akvakultur__A.06%20Salg/A06002.px/)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
* Wang, X., Andresen, K., Handå, A., Jensen, B., Reitan, K., & Olsen, Y. (2013). Chemical composition and release rate of waste discharge from an Atlantic salmon farm with an evaluation of IMTA feasibility. *Aquaculture Environment Interactions, 4*(2), 147-162. [https://doi.org/10.3354/aei00079](https://doi.org/10.3354/aei00079)
* Ytrestøyl, T., Aas, T. S., & Åsgård, T. (2015). Utilisation of feed resources in production of Atlantic salmon (Salmo salar) in Norway. *Aquaculture, 448*, 365-374. [https://doi.org/10.1016/j.aquaculture.2015.06.023](https://doi.org/10.1016/j.aquaculture.2015.06.023)
