---
layout: default
title: Food Import
parent: Rest of the world (RW)
nav_order: 9
---

# Food Import

<iframe src="../output_files/plots/RW_RW_MP_FP_Food_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-MP.FP-Food import-Nmix** is the N in imported food commodities, including fish waste and by-products not fit for human consumption (HS 0511), which are processed in the food and feed industry.
- Soybeans and soybean meal (HS 1201 and 1208.10) are not included. Soybeans are imported mainly for feed and crushed in Norway (Eidem & Ruud, 2022)<!--cite:eidem_for-_2022-->. The soy meal used in feed for farm animals is counted in RW.RW-AG.MM-Animal feed import-Nmix, and the soy used in fish feed is part of RW.RW-HY.AC-Aquaculture feed import-Nmix, where all plant-based ingredients are counted as imported. Imported soybeans amount to 18–25 kt N/year.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.
- Vegetables are assigned N content by product form. Fresh, chilled, frozen and preserved vegetables, potatoes and tomatoes use the fresh-weight N contents in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, Table 21 (0.2–0.3 %). Dried peas and beans use the N content of pulses (3.6 %, Table 21), tomato paste 0.7 % (USDA FoodData Central), and other dried vegetables and potato flakes an estimated 1.6 %.

#### Interpretations and comparisons

- The flow rises from about 16 kt N in 1990 to 25–32 kt N per year since 2010.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Eidem, B. & Ruud, T. (2022). *Fôr- og husdyrbaserte verdikjeder i norsk matproduksjon – nåsituasjon og begreper*.
