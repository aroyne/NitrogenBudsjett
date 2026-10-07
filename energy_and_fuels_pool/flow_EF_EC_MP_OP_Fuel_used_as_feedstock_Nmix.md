---
layout: default
title: Fuel used as feedstock
parent: Energy conversion (EF.EC)
nav_order: 6
---

# Fuel used as feedstock

<iframe src="../output_files/plots/EF_EC_MP_OP_Fuel_used_as_feedstock_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.EC-MP.OP-Fuel used as feedstock-Nmix** covers coal and oil products consumed as chemical feedstock rather than combusted for energy.
- Other minor feedstock categories listed in the guidelines are neglected as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- Natural gas used as feedstock (e.g. for ammonia and methanol production) is not included, since natural gas contains no fuel-bound reactive nitrogen; the nitrogen in ammonia produced from natural gas comes from the air and is accounted for in the materials and products pool.

#### Data sources

- Feedstock use (GWh) of coal and coal products and of oil and oil products (excluding bio) from the section "11 Netto innenlands forbruk som råstoff" (net domestic consumption as feedstock) in [SSB table 11561](https://www.ssb.no/statbank/table/11561) (Energibalansen), including the product split for section 11.
- Net calorific values from [IPCC 2006, Vol. 2, Ch. 1, Table 1.2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf) and nitrogen contents for coal and oil feedstock from Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- Feedstock use is converted to TJ (1 TJ = 0.278 GWh) and divided by a net calorific value from IPCC 2006 Table 1.2: 25.8 TJ/kt (range 19.9–30.5) for coal, the value for other bituminous coal, since the coal used as feedstock is "Kull og brunkull" used in "11.2 I annen produksjon" (mainly as a reducing agent in industry), and 44.5 TJ/kt (range 41.8–46.5) for oil products, the value for naphtha.
- N content 1.5% (range 0.5–2.5%, PERT) for coal, the Table 15 value for bituminous coal and the same as for solid fuels burned for energy (EF.EC-EF.IC-Fuel for industry-Nmix), and 0.0375% for oil products (the Table 15 value for "other oil"), applied to the oil feedstock excluding LPG and ethane.
- LPG and ethane make up 50–65% of the oil feedstock and are given zero N (Table 15: ethane 0, LPG not specified).

#### Interpretations and comparisons

- In 2024 the flow is about 1.1 kt N, of which about 0.8 kt comes from coal.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
