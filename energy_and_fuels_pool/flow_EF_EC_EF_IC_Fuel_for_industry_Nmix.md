---
layout: default
title: Fuel for industry
parent: Energy conversion (EF.EC)
nav_order: 3
---

# Fuel for industry

<iframe src="../output_files/plots/EF_EC_EF_IC_Fuel_for_industry_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.EC-EF.IC-Fuel for industry-Nmix** is the N in fossil fuels used in manufacturing industries and construction (1.A.2).

#### Data sources

- Fuel consumption (TJ) for 1.A.2 Manufacturing industries and construction from the UNFCCC Common Reporting Tables (CRT), Table 1.A(a) sheet 2, as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->. The fuel consumption in the CRT tables comes from the national energy balance compiled by Statistics Norway ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)).
- Net calorific values (TJ per kt fuel) from [IPCC 2006, Vol. 2, Ch. 1, Table 1.2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf) (Garg et al., 2006<!--cite:garg_chapter_2006-->), and nitrogen contents (mass fraction) from Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.
- The mix of oil products used in the sector from [SSB table 11561](https://www.ssb.no/statbank/table/11561) ("Industri og bergverk").

#### Assumptions

- The fuel consumption (TJ) is divided by the net calorific value and multiplied by the nitrogen content, by fuel class.
- Liquid fuels: NCV 44 TJ/kt; N content weighted by year from the mix of oil products in SSB table 11561, with Table 15 values (gas/diesel oil and light fuel oil 0.0133%, heavy fuel oil 0.45%, kerosene 0.1%, heavy distillates 0.0375%, LPG and gasoline 0). The weighted N content falls from 0.17% in 1990 to 0.010% in 2024 as heavy fuel oil has been phased out. Fuel gas from the chemical industry, which SSB reports as "oil products not elsewhere specified", is not part of CRT 1.A.2 liquid fuels and is left out.
- Solid fuels: 25.8 TJ/kt (IPCC 2006 Table 1.2, other bituminous coal) and 1.5% N (Schäppi et al. 2025, Table 15, bituminous coal), the same values as for coal used as feedstock.
- Other fossil fuels, i.e. waste fuels such as waste oil, tyres and plastics: assumed 25 TJ/kt and 0.4% N, between the values for waste oil, tyres and mixed waste (uncertain).
- In the Monte Carlo simulation the NCVs vary within the IPCC 2006 Table 1.2 ranges (liquid fuels 41.4–44.8 TJ/kt, from gas/diesel oil to gasoline; coal 19.9–30.5 TJ/kt; other fossil fuels 10–40 TJ/kt, an assumption between municipal waste and waste oil), and the N contents within the Table 15 ranges where given (heavy fuel oil 0.1–0.8%, coal 0.5–2.5%); N contents for which Table 15 gives only an average (kerosene, gas/diesel oil, heavy distillates, and the assumed 0.4% for other fossil fuels) vary by ±50%.
- Biomass is not included: biomass burned in industry (mainly black liquor, bark and wood waste) enters EF.IC via MP.OP-EF.IC-Industrial waste fuels (own-produced bioenergy, SSB table 08205), which matches the biomass reported in the CRT, so including it here as well would count it twice.
- Gaseous fuels are not included, since natural gas contains no fuel-bound reactive nitrogen.

#### Interpretations and comparisons

- The flow declines from about 4.5 kt N in 1990 to about 1.8 kt N in 2024.
- In 2024, solid fuels (coal and coke) contribute about 1.1 kt, waste fuels about 0.7 kt and liquid fuels about 0.05 kt; in 1990, liquid fuels (mainly heavy fuel oil) contributed about 1.4 kt.
- Purchased biomass in industry not covered by the own-produced bioenergy statistics (about 1,000 TJ in 2024, roughly 0.3 kt N) is not included.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Garg, A., Kazunari, K., & Pulles, T. (2006). Chapter 1. Introduction. *IPCC Guidelines for National Greenhouse Gas Inventories*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
