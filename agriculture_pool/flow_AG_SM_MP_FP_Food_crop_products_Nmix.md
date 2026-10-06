---
layout: default
title: Food crop products
parent: Soil Management (AG.SM)
nav_order: 7
---

# Food crop products

<iframe src="../output_files/plots/AG_SM_MP_FP_Food_crop_products_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Food crop products are taken from EUROSTAT Gross nutrient balance as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: «Nutrient removal by harvest of crops» minus «Industrial crops». «Ornamenal crops», which should also be removed, are negligible in Norway. Eurostat GNB has no values for 2017–2019 and has not yet published 2024. For these years we use SSB's cereal harvest ([table 07479](https://www.ssb.no/statbank/table/07479)), since cereals carry most of the N: the cereal N is the harvest times the N per tonne of cereal harvest in the balance (interpolated between 2016 and 2020, or the 2023 value for 2024), and the other crops are interpolated between 2016 and 2020 or held at the 2023 value. 

**How the numbers are derived.** Eurostat's Gross Nutrient Balance ([aei_pr_gnb](https://ec.europa.eu/eurostat/databrowser/view/aei_pr_gnb/default/table)) calculates nutrient removal by harvest as crop production multiplied by an N content per crop, based on Norwegian crop statistics. The flow is "Nutrient removal by harvest of crops" minus "industrial crops"; fodder crops and grazing are reported separately in the balance and are not included.

**Interpretation.** The flow is 19–32 kt N per year and follows the size of the cereal harvest, since cereals make up about 88% of the N. Most of the cereal is used for animal feed and returns to AG.MM via MP.FP-AG.MM-Farm animal feed-Nmix. The low values in 2018 (16 kt N) and 2023 (19 kt N) are the drought years with poor cereal harvests, and the high value in 1990 (32 kt N) a good harvest.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
