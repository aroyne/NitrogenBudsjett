---
layout: default
title: Fuel for transport
parent: Energy conversion (EF.EC)
nav_order: 5
---

# Fuel for transport

<iframe src="../output_files/plots/EF_EC_EF_TR_Fuel_for_transport_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**EF.EC-EF.TR-Fuel for transport-Nmix**: As advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, we have found this in the UNFCCC Common reporting tables (Table 1) which gives amount of energy consumed in TJ, together with net caloric values from Table 1.2 in Garg et al. (2006)<!--cite:garg_chapter_2006--> and nitrogen contents from Table 15 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

**How the numbers are derived**

- The flow is calculated from the fuel consumption (TJ) reported in CRT Table 1.A(a) sheet 3 for 1.A.3 Transport, divided by a net calorific value (TJ per kt fuel; [IPCC 2006, Vol. 2, Ch. 1, Table 1.2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)) and multiplied by a nitrogen content (mass fraction, Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)).
- The fuel consumption in the CRT tables comes from the national energy balance compiled by Statistics Norway ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)).
- Fuels are read by fuel class, with these assumptions: domestic aviation (all fuels, 44.1 TJ/kt, 0.1% N as for jet kerosene), road transport diesel oil (43 TJ/kt, 0.0133% N) and biomass, i.e. biofuels (27 TJ/kt and 0.0133% N, the Table 15 value for gas/diesel oil used as a proxy: the Table 15 value for liquid biomass, 1%, refers to sewage sludge, while biodiesel (FAME) is made from refined vegetable oils, HVO is hydrotreated, which removes nitrogen compounds, and bioethanol is practically free of nitrogen; the fuel standards EN 14214 and EN 15940 set no limit for N), railway liquid fuels (44 TJ/kt, 0.0133% N, as railways use only diesel according to SSB table 11561) and solid fuels (25 TJ/kt, 1.4% N), and domestic navigation residual fuel oil (40.4 TJ/kt, 0.45% N) and gas/diesel oil (43 TJ/kt, 0.0133% N).
- Gasoline is not included since its N content is 0 in Table 15, and natural gas (LNG in ferries) is not included either.

**Interpretation**

- The flow is about 0.5–0.8 kt N per year.
- Domestic aviation (jet kerosene, 0.1% N) and diesel in road transport and navigation are the largest contributions; biofuels contribute about 0.09 kt N in 2024.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Garg, A., Kazunari, K., & Pulles, T. (2006). Chapter 1. Introduction. *IPCC Guidelines for National Greenhouse Gas Inventories*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
