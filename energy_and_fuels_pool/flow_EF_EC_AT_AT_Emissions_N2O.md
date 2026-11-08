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

- **EF.EC-AT.AT-Emissions-N2O** is N<sub>2</sub>O from energy industries (1.A.1) and from fugitive emissions in the oil and gas sector (1.B.2), using the categories given in Table 11 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- N<sub>2</sub>O from waste incinerated in heat and power plants (the “other fossil fuels” row of 1.A.1.a in CRT Table 1.A(a)) is included, since the incinerated waste is delivered to EF.EC (PR.SO-EF.EC-Waste to energy-Nmix). Schäppi et al. (2025, chapter 1.4.1.2) count it under PR.SO.

#### Data sources

- N<sub>2</sub>O from the UNFCCC Common Reporting Tables (CRT), Table 1, of the national greenhouse gas inventory.
- Like other combustion emissions in the inventory, N<sub>2</sub>O from energy industries is calculated as fuel consumption (TJ) multiplied by an emission factor (kg N<sub>2</sub>O per TJ), following the IPCC 2006 Guidelines for stationary combustion (Gómez et al., 2006)<!--cite:gomez_stationary_2006-->; Norway uses a mix of IPCC default and country-specific emission factors (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_nid_2026-->. Activity data and implied emission factors are reported in CRT Table 1.A(a).
- N<sub>2</sub>O from flaring (1.B.2.c, included via the 1.B.2 total) is calculated in the same way from the volume of gas flared (Picard et al., 2006)<!--cite:picard_fugitive_2006-->.

#### Interpretations

- The emission factors differ strongly between fuels: in the 2024 CRT, the implied N<sub>2</sub>O factors for 1.A.1 are about 0.1 kg/TJ for natural gas, about 2 kg/TJ for waste (“other fossil fuels”, which in the CRT includes the biogenic part of waste) and about 3.7 kg/TJ for wood fuel (“biomass”). The time series therefore reflects the use of waste and biomass as energy sources more than total energy use.
- Emissions from energy industries (1.A.1) increased from 0.037 kt N/year in 1990 to about 0.07 kt N in 2024, and almost all of the growth after 2008 comes from public electricity and heat production (1.A.1.a), mainly heat plants, where emissions rose from 0.017 kt N/year in 2008 to 0.050 kt N in 2023 as waste incineration and biomass-fired district heating expanded. Waste incineration accounts for 0.006–0.02 kt N per year of the flow.
- Emissions from oil and gas extraction (1.A.1.c), which use mainly natural gas in turbines, contribute less N<sub>2</sub>O (0.015 kt N/year in 2023), and emissions from petroleum refining (1.A.1.b) have been small since 2000.
- N<sub>2</sub>O from fugitive emissions in the oil and gas sector (1.B.2, in practice only 1.B.2.c Venting and flaring) was 0.011 kt N/year in 1990 (about 30% of the flow), varied mostly around 0.006–0.013 kt N with a short peak of 0.014 kt N in 2007–2008, and has since declined to 0.003 kt N in 2024 (about 4% of the flow); the other 1.B.2 subcategories are reported as not applicable, not occurring or included elsewhere.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N<sub>2</sub>O from stationary combustion (Norway's GHG inventory, CRT 1.A) | Inventory with published uncertainty | −66.7/+200 %, lognormal | 100% | 100% | 1.00 | 1.00 | [Industrial emissions (N<sub>2</sub>O)](../energy_and_fuels_pool/flow_EF_IC_AT_AT_Emissions_N2O.html), [Other energy emissions (N<sub>2</sub>O)](../energy_and_fuels_pool/flow_EF_OE_AT_AT_Emissions_N2O.html) |

### References

* Gómez, D. R., Watterson, J. D., Americano, B. B., Ha, C., Marland, G., Matsika, E., Namayanga, L. N., Osman-Elasha, B., Kalenga Saka, J. D., & Treanton, K. (2006). Chapter 2. Stationary Combustion. *2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 2: Energy*. [ipcc-nggip.iges.or.jp](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf)
* Miljødirektoratet (2026). *Greenhouse gas emissions 1990–2024, National Inventory Document* (M-3138). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)
* Picard, D., Ahmed, A. F. M., Gjerald, E., Nordrum, S., & Yesserkepova, I. (2006). Chapter 4. Fugitive Emissions. *2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 2: Energy*. [ipcc-nggip.iges.or.jp](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_4_Ch4_Fugitive_Emissions.pdf)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
