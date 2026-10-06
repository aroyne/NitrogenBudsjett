---
layout: default
title: Fuel for heating
parent: Energy conversion (EF.EC)
nav_order: 4
---

# Fuel for heating

<iframe src="../output_files/plots/EF_EC_EF_OE_Fuel_for_heating_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**EF.EC-EF.OE-Fuel for heating-Nmix**: As advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, we have found this in the UNFCCC Common reporting tables (Table 1) which gives amount of energy consumed in TJ, together with net caloric values from Table 1.2 in Garg et al. (2006)<!--cite:garg_chapter_2006--> and nitrogen contents from Table 15 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

**How the numbers are derived.** The flow is calculated from the fuel consumption (TJ) reported in CRT Table 1.A(a) sheet 4 for 1.A.4 Other sectors and 1.A.5 Other (mainly military, mobile), so that the fuel input matches the OE emission flows, divided by a net calorific value (TJ per kt fuel; [IPCC 2006, Vol. 2, Ch. 1, Table 1.2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)) and multiplied by a nitrogen content (mass fraction, Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)). The fuel consumption in the CRT tables comes from the national energy balance compiled by Statistics Norway ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)). Fuels are read by fuel class, with these assumptions: liquid fuels (NCV 44 TJ/kt; N content weighted by year from the mix of oil products used in the sector according to [SSB table 11561](https://www.ssb.no/statbank/table/11561) ("Andre forbruksgrupper", which covers 1.A.4 and 1.A.5), with Table 15 values: gas/diesel oil and light fuel oil 0.0133%, heavy fuel oil 0.45%, kerosene 0.1%, heavy distillates 0.0375%, LPG and gasoline 0; the weighted N content falls from 0.035% in 1990 to 0.016% in 2024), solid fuels (25 TJ/kt, 1.4% N), other fossil fuels, i.e. waste fuels such as waste oil, tyres and plastics (assumed 25 TJ/kt and 0.4% N, between the values for waste oil, tyres and mixed waste; uncertain). Biomass is not included in this flow: firewood burned in households enters EF.OE via FS.FO-EF.OE-Fuel wood for households (SSB table 09702), which matches the biomass reported in the CRT, so including it here as well would count it twice; gaseous fuels are not included.

**Interpretation.** Category 1.A.4 covers commercial/institutional and residential heating, but also mobile combustion in agriculture, forestry and fishing (tractors, off-road machinery and fishing vessels), and 1.A.5 mainly military mobile use, so the flow is broader than "heating". Since biomass enters via the fuel wood flow, this flow only covers fossil fuels and is small: about 0.7 kt N in 1990 and 0.2 kt N in 2024, mainly from liquid fuels. Biomass used in the commercial/institutional sector (1.A.4.a, about 3,600 TJ in 2024, roughly 0.9 kt N) is not covered by the fuel wood flow and is therefore not included in the budget.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Garg, A., Kazunari, K., & Pulles, T. (2006). Chapter 1. Introduction. *IPCC Guidelines for National Greenhouse Gas Inventories*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
