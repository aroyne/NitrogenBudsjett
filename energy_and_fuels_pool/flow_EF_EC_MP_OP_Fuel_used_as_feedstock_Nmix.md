---
layout: default
title: Fuel used as feedstock
parent: Energy conversion (EF.EC)
nav_order: 6
---

# Fuel used as feedstock

<iframe src="../output_files/plots/EF_EC_MP_OP_Fuel_used_as_feedstock_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**EF.EC-MP.OP-Fuel used as feedstock-Nmix** covers coal and oil products consumed as chemical feedstock rather than combusted for energy. We use SSB table 11561 "Energibalansen"'s "Netto innenlands forbruk som råstoff" (net domestic consumption as feedstock) section for consumption volumes by energy product, net caloric values from IPCC (2006), and nitrogen contents for coal and oil feedstock from Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->. Other minor feedstock categories listed in the guidelines are neglected as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

**How the numbers are derived.** Feedstock use (GWh) of coal and coal products and of oil and oil products (excluding bio) is read from the section "11 Netto innenlands forbruk som råstoff" in [SSB table 11561](https://www.ssb.no/statbank/table/11561), converted to TJ (1 TJ = 0.278 GWh), divided by a net calorific value (coal 20 TJ/kt, oil products 44 TJ/kt; [IPCC 2006, Vol. 2, Ch. 1, Table 1.2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)) and multiplied by an N content: 1% for coal and 0.0375% for oil products (the Table 15 value for "other oil" in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)), applied to the oil feedstock excluding LPG and ethane. LPG and ethane make up 50–65% of the oil feedstock (SSB table 11561, product split for section 11) and are given zero N (Table 15: ethane 0, LPG not specified). Natural gas used as feedstock (e.g. for ammonia and methanol production) is not included, since natural gas contains no fuel-bound reactive nitrogen; the nitrogen in ammonia produced from natural gas comes from the air and is accounted for in the materials and products pool. In 2024 the flow is about 0.9 kt N, of which about 0.7 kt comes from coal.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
