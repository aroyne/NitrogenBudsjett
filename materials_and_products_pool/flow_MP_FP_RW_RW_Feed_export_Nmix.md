---
layout: default
title: Feed Export
parent: Food and Feed Processing (MP.FP)
nav_order: 8
---

# Feed Export

<iframe src="../output_files/plots/MP_FP_RW_RW_Feed_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Using trade data from SSB, table 08801.

**How the numbers are derived**

- Export quantities (kg) by commodity code are taken from SSB's external trade statistics ([table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from the customs declarations for goods crossing the border ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)).
- Each commodity code is assigned a commodity type and an N content in the trade mapping sheet of N_parameters.xlsx, and quantities are multiplied by the N content.
- This flow includes the commodity types feed, fish feed and pet food, and fish waste and by-products not fit for human consumption (HS 0511), whether or not they are declared for feed.

**Interpretation**

- The flow rises from about 7 kt N in 1990 to about 20 kt N in 2024.
- In 2024 it consists mainly of oilseed cake and meal (about 7 kt N), pet food (about 6 kt N, up from 0.2 kt N in 1990) and fish products and by-products (about 6 kt N).
- The peak in 2002–2005 (15–17 kt N) comes from exports of fish waste and by-products not for feed, which reached about 8 kt N in 2003.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
