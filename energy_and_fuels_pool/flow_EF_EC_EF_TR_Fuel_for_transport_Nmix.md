---
layout: default
title: Fuel for transport
parent: Energy conversion (EF.EC)
nav_order: 5
---

# Fuel for transport

<iframe src="../output_files/plots/EF_EC_EF_TR_Fuel_for_transport_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.EC-EF.TR-Fuel for transport-Nmix** is the N in fuels used for domestic transport (1.A.3).

#### Data sources

- Fuel consumption (TJ) for 1.A.3 Transport from the UNFCCC Common Reporting Tables (CRT), Table 1.A(a) sheet 3, as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->. The fuel consumption in the CRT tables comes from the national energy balance compiled by Statistics Norway (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_nid_2026-->.
- Net calorific values (TJ per kt fuel) from Table 1.2 in Garg et al. (2006)<!--cite:garg_chapter_2006-->, and nitrogen contents (mass fraction) from Table 15 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- The fuel consumption (TJ) is divided by the net calorific value and multiplied by the nitrogen content, by fuel class.
- Domestic aviation: all fuels, 44.1 TJ/kt, 0.1% N as for jet kerosene.
- Road transport: diesel oil 43 TJ/kt, 0.0133% N; biofuels 27 TJ/kt and 0.0133% N, the Table 15 value for gas/diesel oil used as a proxy. The Table 15 value for liquid biomass, 1%, refers to sewage sludge, while biodiesel (FAME) is made from refined vegetable oils, HVO is hydrotreated, which removes nitrogen compounds, and bioethanol is practically free of nitrogen; the fuel standards EN 14214 and EN 15940 set no limit for N.
- Railways: liquid fuels 44 TJ/kt, 0.0133% N, as railways use only diesel according to SSB table 11561; solid fuels 25.8 TJ/kt, 1.5% N (as for solid fuels in EF.EC-EF.IC-Fuel for industry-Nmix).
- Domestic navigation: residual fuel oil 40.4 TJ/kt, 0.45% N; gas/diesel oil 43 TJ/kt, 0.0133% N.
- The uncertainty ranges are from IPCC 2006 Table 1.2 for the NCVs and from Table 15 for the N contents where Table 15 gives a range. The ranges for N contents for which Table 15 gives only an average (jet kerosene and gas/diesel oil) are our assumption.
- Gasoline is not included since its N content is 0 in Table 15, and natural gas (LNG in ferries) is not included either.

#### Interpretations

- The flow is about 0.4–1.0 kt N per year<!--range:EF.EC-EF.TR-Fuel for transport-Nmix:1990-2024-->, rising from 0.4 kt N<!--val:EF.EC-EF.TR-Fuel for transport-Nmix:1990--> in 1990 to a peak of about 1.0 kt N<!--mean:EF.EC-EF.TR-Fuel for transport-Nmix:2007-2008--> in 2007–2008 and about 0.8 kt N<!--val:EF.EC-EF.TR-Fuel for transport-Nmix:2024--> in 2024.
- Domestic aviation (jet kerosene, 0.1% N) and diesel in road transport and navigation are the largest contributions; biofuels contribute about 0.09 kt N in 2024.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of gas/diesel oil | Parameter | ±50 %, triangular | 32% | 67% | 0.37 | 0.61 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for heating](../energy_and_fuels_pool/flow_EF_EC_EF_OE_Fuel_for_heating_Nmix.html) |
| N content of jet kerosene | Parameter | ±50 %, triangular | 62% | 27% | 0.52 | 0.39 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for heating](../energy_and_fuels_pool/flow_EF_EC_EF_OE_Fuel_for_heating_Nmix.html) |
| Net calorific value of liquid biofuels | Parameter | 13.6–54, lognormal | – | 4% | – | −0.10 | none |
| Fuel consumption (Norway's GHG inventory, CRT 1.A) | Registered data | ±5 %, normal, drawn per year | 2% | 2% | 1.00 | 1.00 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for heating](../energy_and_fuels_pool/flow_EF_EC_EF_OE_Fuel_for_heating_Nmix.html), [Fuel Wood for Heat Plants](../forests_and_semi_natural_pool/flow_FS_FO_EF_EC_Fuel_wood_for_co_fired_power_plants_Nmix.html), [Fuel Wood for Households](../forests_and_semi_natural_pool/flow_FS_FO_EF_OE_Fuel_wood_for_households_Nmix.html) |
| N content of residual fuel oil | Parameter | 0.001–0.008 (min–max), triangular | 4% | – | 0.11 | – | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for heating](../energy_and_fuels_pool/flow_EF_EC_EF_OE_Fuel_for_heating_Nmix.html) |

### References

* <span id="ref-garg_chapter_2006" data-cite="Garg et al." data-year="2006"></span>Garg, A., Kainou, K., & Pulles, T. (2006). Chapter 1. Introduction. *2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 2: Energy*. [ipcc-nggip.iges.or.jp](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)
* <span id="ref-miljodirektoratet_nid_2026" data-cite="Miljødirektoratet" data-year="2026"></span>Miljødirektoratet (2026). *Greenhouse gas emissions 1990–2024, National Inventory Document* (M-3138). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)
* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
