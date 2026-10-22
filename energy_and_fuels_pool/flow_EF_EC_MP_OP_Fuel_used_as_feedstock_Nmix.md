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
- N content 1.5% (95% interval 0.5–2.5%, triangular distribution) for coal, the Table 15 value for bituminous coal and the same as for solid fuels burned for energy (EF.EC-EF.IC-Fuel for industry-Nmix), and 0.0375% for oil products (the Table 15 value for "other oil"), applied to the oil feedstock excluding LPG and ethane.
- LPG and ethane make up 50–65% of the oil feedstock and are given zero N (Table 15: ethane 0, LPG not specified).

#### Interpretations and comparisons

- In 2024 the flow is about 1.1 kt N, of which about 0.8 kt comes from coal.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of oil products used as feedstock | Parameter | 0–0.0025, lognormal | 31% | 65% | 0.11 | 0.21 | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of coal | Parameter | 0.005–0.025, triangular | 63% | 32% | 0.89 | 0.79 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for heating](../energy_and_fuels_pool/flow_EF_EC_EF_OE_Fuel_for_heating_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Net calorific value of coal | Parameter | 19.9–30.5, triangular | 5% | 3% | −0.80 | −0.72 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for heating](../energy_and_fuels_pool/flow_EF_EC_EF_OE_Fuel_for_heating_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
