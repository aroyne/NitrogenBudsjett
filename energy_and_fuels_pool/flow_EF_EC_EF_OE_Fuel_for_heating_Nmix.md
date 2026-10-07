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

- Fuel consumption (TJ) for 1.A.4 Other sectors and 1.A.5 Other from the UNFCCC Common Reporting Tables (CRT), Table 1.A(a) sheet 4, as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->. The fuel consumption in the CRT tables comes from the national energy balance compiled by Statistics Norway ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)).
- Net calorific values (TJ per kt fuel) from [IPCC 2006, Vol. 2, Ch. 1, Table 1.2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf) (Garg et al., 2006<!--cite:garg_chapter_2006-->), and nitrogen contents (mass fraction) from Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.
- The mix of oil products used in the sector from [SSB table 11561](https://www.ssb.no/statbank/table/11561) ("Andre forbruksgrupper", which covers 1.A.4 and 1.A.5).

#### Assumptions

- The fuel consumption (TJ) is divided by the net calorific value and multiplied by the nitrogen content, by fuel class.
- Liquid fuels: NCV 44 TJ/kt; N content weighted by year from the mix of oil products in SSB table 11561, with Table 15 values (gas/diesel oil and light fuel oil 0.0133%, heavy fuel oil 0.45%, kerosene 0.1%, heavy distillates 0.0375%, LPG and gasoline 0). The weighted N content falls from 0.035% in 1990 to 0.016% in 2024.
- Solid fuels: 25.8 TJ/kt (IPCC 2006 Table 1.2, other bituminous coal) and 1.5% N (Schäppi et al. 2025, Table 15, bituminous coal), the same values as for coal used as feedstock.
- Other fossil fuels, i.e. waste fuels such as waste oil, tyres and plastics: assumed 25 TJ/kt and 0.4% N, between the values for waste oil, tyres and mixed waste (uncertain).
- In the Monte Carlo simulation the NCVs vary within the IPCC 2006 Table 1.2 ranges (liquid fuels 41.4–44.8 TJ/kt, from gas/diesel oil to gasoline; coal 19.9–30.5 TJ/kt; other fossil fuels 10–40 TJ/kt, an assumption between municipal waste and waste oil), and the N contents within the Table 15 ranges where given (heavy fuel oil 0.1–0.8%, coal 0.5–2.5%); N contents for which Table 15 gives only an average (kerosene, gas/diesel oil, heavy distillates, and the assumed 0.4% for other fossil fuels) vary by ±50%.
- Biomass is not included: firewood burned in households enters EF.OE via FS.FO-EF.OE-Fuel wood for households (SSB table 09702), which matches the biomass reported in the CRT, so including it here as well would count it twice. Gaseous fuels are not included.

#### Interpretations and comparisons

- Since biomass enters via the fuel wood flow, this flow only covers fossil fuels and is small: about 0.7 kt N in 1990 and 0.2 kt N in 2024, mainly from liquid fuels.
- Biomass used in the commercial/institutional sector (1.A.4.a, about 3,600 TJ in 2024, roughly 0.9 kt N) is not covered by the fuel wood flow and is therefore not included in the budget.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Garg, A., Kazunari, K., & Pulles, T. (2006). Chapter 1. Introduction. *IPCC Guidelines for National Greenhouse Gas Inventories*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
