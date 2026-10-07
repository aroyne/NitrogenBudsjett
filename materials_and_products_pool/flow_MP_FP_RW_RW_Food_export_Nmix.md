---
layout: default
title: Food Export
parent: Food and Feed Processing (MP.FP)
nav_order: 9
---

# Food Export

<iframe src="../output_files/plots/MP_FP_RW_RW_Food_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Using trade data from SSB, table 08801.

**How the numbers are derived**

- Export quantities (kg) by commodity code are taken from SSB's external trade statistics ([table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from the customs declarations for goods crossing the border ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)).
- Each commodity code is assigned a commodity type and an N content in the trade mapping sheet of N_parameters.xlsx, and quantities are multiplied by the N content.
- This flow includes the commodity types cereals and plants, meat, fish, dairy products and eggs, and other food.

**Interpretation**

- Fish and fish products (fresh, frozen and processed, including farmed salmon) make up over 95% of the flow, 66 of 69 kt N in 2024.
- The flow rises from 22 kt N in 1990 to about 70 kt N by 2010 and has been roughly stable since, as the growth in farmed fish has been offset by lower wild catches (see HY.AC-MP.FP-Coastal fish and seafood-Nmix and HY.CW-MP.FP-Fish (wild catch)-Nmix).
- Exports of meat and of cheese are each below 0.5 kt N.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
