---
layout: default
title: Fuel for heating
parent: Energy conversion (EF.EC)
nav_order: 4
---

# Fuel for heating

<iframe src="../output_files/plots/EF_EC_EF_OE_Fuel_for_heating_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.EC-EF.OE-Fuel for heating-Nmix** is the N in fossil fuels used in other sectors (1.A.4) and other (1.A.5, mainly military, mobile), so that the fuel input matches the OE emission flows.
- Category 1.A.4 covers commercial/institutional and residential heating, but also mobile combustion in agriculture, forestry and fishing (tractors, off-road machinery and fishing vessels), and 1.A.5 mainly military mobile use, so the flow is broader than "heating".

#### Data sources

- Fuel consumption (TJ) for 1.A.4 Other sectors and 1.A.5 Other from the UNFCCC Common Reporting Tables (CRT), Table 1.A(a) sheet 4, as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->. The fuel consumption in the CRT tables comes from the national energy balance compiled by Statistics Norway (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_nid_2026-->.
- Net calorific values (TJ per kt fuel) from Table 1.2 in Garg et al. (2006)<!--cite:garg_chapter_2006-->, and nitrogen contents (mass fraction) from Table 15 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The mix of oil products used in the sector from [SSB table 11561](https://www.ssb.no/statbank/table/11561) ("Andre forbruksgrupper", which covers 1.A.4 and 1.A.5).

#### Assumptions

- The fuel consumption (TJ) is divided by the net calorific value and multiplied by the nitrogen content, by fuel class.
- Liquid fuels: NCV 44 TJ/kt; N content weighted by year from the mix of oil products in SSB table 11561, with Table 15 values (gas/diesel oil and light fuel oil 0.0133%, heavy fuel oil 0.45%, kerosene 0.1%, heavy distillates 0.0375%, LPG and gasoline 0). The weighted N content falls from 0.035% in 1990 to 0.016% in 2024.
- Solid fuels: 25.8 TJ/kt (IPCC 2006 Table 1.2, other bituminous coal) and 1.5% N (Schäppi et al. 2025, Table 15, bituminous coal), the same values as for coal used as feedstock.
- Other fossil fuels, i.e. waste fuels such as waste oil, tyres and plastics: assumed 25 TJ/kt and 0.4% N, between the values for waste oil, tyres and mixed waste (uncertain).
- The uncertainty ranges are from IPCC 2006 Table 1.2 for the NCVs and from Table 15 for the N contents where Table 15 gives a range. The range for the NCV of other fossil fuels (between municipal waste and waste oil) and the ranges for N contents for which Table 15 gives only an average (kerosene, gas/diesel oil, heavy distillates and other fossil fuels) are our assumptions.
- Biomass is not included: firewood burned in households (SSB table 09702, which matches the residential biomass in the CRT) and wood pellets and chips burned in other sectors (CRT 1.A.4.a and 1.A.4.c) enter EF.OE via FS.FO-EF.OE-Fuel wood for households, so including them here as well would count them twice. Gaseous fuels are not included.

#### Interpretations

- Since biomass enters via the fuel wood flow, this flow only covers fossil fuels and is small: about 0.7 kt N in 1990 and 0.2 kt N in 2024, mainly from liquid fuels.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of gas/diesel oil | Parameter | ±50 %, triangular | 11% | 41% | 0.21 | 0.47 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for transport](../energy_and_fuels_pool/flow_EF_EC_EF_TR_Fuel_for_transport_Nmix.html) |
| Net calorific value of other fossil fuels | Parameter | 10–40, triangular | <1% | 29% | −0.01 | −0.33 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html) |
| N content of other fossil fuels | Parameter | ±50 %, triangular | <1% | 24% | 0.01 | 0.36 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html) |
| N content of jet kerosene | Parameter | ±50 %, triangular | 46% | 4% | 0.42 | 0.15 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for transport](../energy_and_fuels_pool/flow_EF_EC_EF_TR_Fuel_for_transport_Nmix.html) |
| Fuel consumption (Norway's GHG inventory, CRT 1.A) | Registered data | ±5 %, normal, drawn per year | 2% | 2% | 1.00 | 1.00 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for transport](../energy_and_fuels_pool/flow_EF_EC_EF_TR_Fuel_for_transport_Nmix.html), [Fuel Wood for Heat Plants](../forests_and_semi_natural_pool/flow_FS_FO_EF_EC_Fuel_wood_for_co_fired_power_plants_Nmix.html), [Fuel Wood for Households](../forests_and_semi_natural_pool/flow_FS_FO_EF_OE_Fuel_wood_for_households_Nmix.html) |
| N content of coal | Parameter | 0.005–0.025, triangular | 35% | <1% | 0.28 | 0.01 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel used as feedstock](../energy_and_fuels_pool/flow_EF_EC_MP_OP_Fuel_used_as_feedstock_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Net calorific value of coal | Parameter | 19.9–30.5, triangular | 3% | <1% | −0.25 | −0.01 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel used as feedstock](../energy_and_fuels_pool/flow_EF_EC_MP_OP_Fuel_used_as_feedstock_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |

### References

* Garg, A., Kainou, K., & Pulles, T. (2006). Chapter 1. Introduction. *2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 2: Energy*. [ipcc-nggip.iges.or.jp](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)
* Miljødirektoratet (2026). *Greenhouse gas emissions 1990–2024, National Inventory Document* (M-3138). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
