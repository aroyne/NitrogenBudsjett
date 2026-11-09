---
layout: default
title: Fuel Wood for Households
parent: Forests (FS.FO)
nav_order: 3
---

# Fuel Wood for Households

<iframe src="../output_files/plots/FS_FO_EF_OE_Fuel_wood_for_households_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.FO-EF.OE-Fuel wood for households-Nmix** is the N in wood burned in dwellings and holiday homes, and in wood pellets and chips burned in commercial and institutional buildings and in agriculture, forestry and fishing.
- Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> (chapter 4.4.4) suggest a single flow to EF.OE when households dominate, so the other sectors are included here although the flow name refers to households.

#### Data sources

- SSB's energy balance gives the wood burned in dwellings and holiday homes ([table 09702](https://www.ssb.no/statbank/table/09702), 'Energibalansen. Vedforbruk i boliger og fritidsboliger 1990 – 2024'). From 2005 the figures are based on SSB's survey of households' wood consumption; earlier years build on SSB's energy statistics and household surveys.
- Biomass consumption (TJ) in 1.A.4.a Commercial/institutional and 1.A.4.c Agriculture/forestry/fishing from the UNFCCC Common Reporting Tables (CRT), Table 1.A(a) sheet 4. Residential biomass (1.A.4.b) is not read from the CRT, since it is the same firewood as in table 09702.
- N content of broadleaf stems with bark from Table 45 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- For 2005 the holiday-home figure is the 2006 value.
- Biomass in the other sectors is divided by a net calorific value of 15.6 TJ/kt (IPCC 2006 Table 1.2, wood) and multiplied by the same N content as wood fuel in heat plants, 0.3 % (range 0.14–0.4 %), since it is mainly pellets and chips (see FS.FO-EF.EC-Fuel wood for co-fired power plants-Nmix).
- Fuel wood is mainly stem wood with bark, much of it birch, so the N content of broadleaf stems is used: 1.4 g/kg, with a range from 0.7 g/kg (stems minus one standard deviation) to 4.3 g/kg (whole broadleaf trees including branches and foliage).

#### Interpretations

- The flow is about 1.5–2.7 kt N per year<!--range:FS.FO-EF.OE-Fuel wood for households-Nmix:1990-2024-->. It rises from about 1.7 kt N<!--val:FS.FO-EF.OE-Fuel wood for households-Nmix:1990--> in 1990 to a peak of 2.7 kt N<!--val:FS.FO-EF.OE-Fuel wood for households-Nmix:2010--> in 2010, a cold winter, falls to about 1.8–2.0 kt N<!--range:FS.FO-EF.OE-Fuel wood for households-Nmix:2014-2020--> in 2014–2020 and rises again to 2.2 kt N<!--val:FS.FO-EF.OE-Fuel wood for households-Nmix:2022--> in 2022, when electricity prices were high, and 2.5 kt N<!--range:FS.FO-EF.OE-Fuel wood for households-Nmix:2023-2024--> in 2023–2024.
- The other sectors add little before 2000 and about 0.2–0.3 kt N per year in 2010–2022. In 2023–2024 they add about 0.6–0.7 kt N, as biomass in commercial buildings doubled and biomass in agriculture, forestry and fishing, almost none before 2023, rose to about 1,100 TJ in 2024.
- The stem value is close to the 1.1 g/kg for stem with bark of conifers used by Hellsten et al. (2008), cited in the Swedish nitrogen budget (Jutterström et al., 2020)<!--cite:jutterstrom_swedish_2020-->; the Swedish budget uses the whole-tree value for fuel wood, as the guidance suggests when no other data are available.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of fuel wood burned in households | Parameter | 0.0007–0.0043, triangular | 98% | 97% | 0.99 | 0.83 | none |

### References

* Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation* (C 549). IVL Swedish Environmental Research Institute.
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
