---
layout: default
title: Fuel for industry
parent: Energy conversion (EF.EC)
nav_order: 3
---

# Fuel for industry

<iframe src="../output_files/plots/EF_EC_EF_IC_Fuel_for_industry_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**EF.EC-EF.IC-Fuel for industry-Nmix**: As advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, we have found this in the UNFCCC Common reporting tables (Table 1) which gives amount of energy consumed in TJ, together with net caloric values from Table 1.2 in Garg et al. (2006)<!--cite:garg_chapter_2006--> and nitrogen contents from Table 15 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

**How the numbers are derived**

- The flow is calculated from the fuel consumption (TJ) reported in CRT Table 1.A(a) sheet 2 for 1.A.2 Manufacturing industries and construction, divided by a net calorific value (TJ per kt fuel; [IPCC 2006, Vol. 2, Ch. 1, Table 1.2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)) and multiplied by a nitrogen content (mass fraction, Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)).
- The fuel consumption in the CRT tables comes from the national energy balance compiled by Statistics Norway ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)).
- Fuels are read by fuel class, with these assumptions: liquid fuels (NCV 44 TJ/kt; N content weighted by year from the mix of oil products used in the sector according to [SSB table 11561](https://www.ssb.no/statbank/table/11561) ("Industri og bergverk"), with Table 15 values: gas/diesel oil and light fuel oil 0.0133%, heavy fuel oil 0.45%, kerosene 0.1%, heavy distillates 0.0375%, LPG and gasoline 0; the weighted N content falls from 0.17% in 1990 to 0.010% in 2024 as heavy fuel oil has been phased out; fuel gas from the chemical industry, which SSB reports as "oil products not elsewhere specified", is not part of CRT 1.A.2 liquid fuels and is left out), solid fuels (25 TJ/kt, 1.4% N), other fossil fuels, i.e. waste fuels such as waste oil, tyres and plastics (assumed 25 TJ/kt and 0.4% N, between the values for waste oil, tyres and mixed waste; uncertain).
- Biomass is not included in this flow: biomass burned in industry (mainly black liquor, bark and wood waste) enters EF.IC via MP.OP-EF.IC-Industrial waste fuels (own-produced bioenergy, SSB table 08205), which matches the biomass reported in the CRT, so including it here as well would count it twice.
- Gaseous fuels are not included, since natural gas contains no fuel-bound reactive nitrogen.

**Interpretation**

- The flow declines from about 4.4 kt N in 1990 to about 1.8 kt N in 2024.
- In 2024, solid fuels (coal and coke) contribute about 1.1 kt, waste fuels about 0.7 kt and liquid fuels about 0.05 kt; in 1990, liquid fuels (mainly heavy fuel oil) contributed about 1.4 kt.
- Purchased biomass in industry not covered by the own-produced bioenergy statistics (about 1,000 TJ in 2024, roughly 0.3 kt N) is not included.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Garg, A., Kazunari, K., & Pulles, T. (2006). Chapter 1. Introduction. *IPCC Guidelines for National Greenhouse Gas Inventories*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
