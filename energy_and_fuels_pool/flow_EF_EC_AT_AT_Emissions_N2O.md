---
layout: default
title: Energy conversion emissions (N2O)
parent: Energy conversion (EF.EC)
nav_order: 1
---

# Energy conversion emissions (N2O)

<iframe src="../output_files/plots/EF_EC_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.EC-AT.AT-Emissions-N2O** is N2O from energy industries (1.A.1) and from fugitive emissions in the oil and gas sector (1.B.2), using the categories given in Table 11 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Data sources

- N2O from the UNFCCC Common Reporting Tables (CRT), Table 1, of the national greenhouse gas inventory.
- Like other combustion emissions in the inventory, N2O from energy industries is calculated as fuel consumption (TJ) multiplied by an emission factor (kg N2O per TJ), following the IPCC 2006 Guidelines for stationary combustion ([IPCC 2006, Vol. 2, Ch. 2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf)); Norway uses a mix of IPCC default and country-specific emission factors ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)). Activity data and implied emission factors are reported in CRT Table 1.A(a).
- N2O from flaring (1.B.2.c, included via the 1.B.2 total) is calculated in the same way from the volume of gas flared ([IPCC 2006, Vol. 2, Ch. 4](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_4_Ch4_Fugitive_Emissions.pdf)).

#### Interpretations and comparisons

- The emission factors differ strongly between fuels: in the 2024 CRT, the implied N2O factors for 1.A.1 are about 0.1 kg/TJ for natural gas, about 2 kg/TJ for the fossil part of waste (“other fossil fuels”) and about 3.7 kg/TJ for biomass (including the biogenic part of waste). The time series therefore follows the use of waste and biomass more than total energy use.
- Emissions from energy industries (1.A.1) increased from 0.025 kt N/year in 1990 to about 0.064 kt N in 2024, and almost all of the growth after 2008 comes from public electricity and heat production (1.A.1.a), mainly heat plants, where emissions rose from 0.017 kt N/year in 2008 to 0.050 kt N in 2023 as waste incineration and biomass-fired district heating expanded.
- Emissions from oil and gas extraction (1.A.1.c), which use mainly natural gas in turbines, are larger in CO2 terms but contribute less N2O (0.015 kt N/year in 2023), and emissions from petroleum refining (1.A.1.b) have been small since 2000.
- N2O from fugitive emissions in the oil and gas sector (1.B.2, in practice only 1.B.2.c Venting and flaring) was 0.011 kt N/year in 1990 (about 30% of the flow), varied mostly around 0.006–0.013 kt N with a short peak of 0.014 kt N in 2007–2008, and has since declined to 0.003 kt N in 2024 (about 4% of the flow); the other 1.B.2 subcategories are reported as not applicable, not occurring or included elsewhere.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N2O from stationary combustion (Norway's GHG inventory, CRT 1.A) | Inventory with published uncertainty | −66.7/+200 %, lognormal | 100% | 100% | 1.00 | 1.00 | [Industrial emissions (N2O)](../energy_and_fuels_pool/flow_EF_IC_AT_AT_Emissions_N2O.html), [Other energy emissions (N2O)](../energy_and_fuels_pool/flow_EF_OE_AT_AT_Emissions_N2O.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
