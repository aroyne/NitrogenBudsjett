---
layout: default
title: Fuel Wood for Heat Plants
parent: Forests (FS.FO)
nav_order: 4
---

# Fuel Wood for Heat Plants

<iframe src="../output_files/plots/FS_FO_EF_EC_Fuel_wood_for_co_fired_power_plants_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.FO-EF.EC-Fuel wood for co-fired power plants-Nmix** is the N in wood fuel (energy wood, bark, branches and tops, wood chips and pellets) burned in heat and power plants, mainly district heating.
- The flow code follows Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, whose text defines the flow as wood fuel used in wood-fired heating plants (chapter 4.4.4), not only co-firing.

#### Data sources

- Biomass consumption (TJ) in 1.A.1.a Public electricity and heat production from the UNFCCC Common Reporting Tables (CRT), Table 1.A(a) sheet 1.
- From 2014 this matches "Bark, flis og tre" in [SSB table 04730](https://www.ssb.no/statbank/table/04730) (fuel used for district heating) within 1–5 %. All waste incinerated, including its biogenic part, is reported as "Other fossil fuels" in the CRT and equals "Avfall" in table 04730; it enters EF via PR.SO-EF.EC-Waste to energy.
- Net calorific value of wood, 15.6 TJ/kt, from [IPCC 2006, Vol. 2, Ch. 1, Table 1.2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf) (Garg et al., 2006<!--cite:garg_chapter_2006-->), and N contents of stems and whole trees from Table 45 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- The consumption in TJ is divided by the net calorific value and multiplied by an N content of 0.3 % (range 0.14–0.4 %), between the stem value for broadleaves and about the whole-tree average, since the fuel is a mix of stem wood, bark and branches and tops.
- Recycled wood (returtre) is assumed to be reported as waste ("Avfall") in the district heating statistics and is therefore part of PR.SO-EF.EC, not this flow. SSB's documentation does not say which category it belongs to.
- The whole flow is counted from FS.FO. Energy wood ("rundvirke til flis", 524 000 m³ in 2025, [SSB table 14641](https://www.ssb.no/statbank/table/14641)) and bark are not part of the industrial roundwood under bark in FS.FO-MP.OP, so they are not counted twice. Of the sawmill by-products from stem wood, sawdust goes to board production and animal bedding and pulp chips to paper; only dry by-products (planer shavings, about 4 % of the sawlog volume) go partly to energy ([Belbo et al., 2022, NIBIO Rapport 8(170), Table 1](https://nibio.brage.unit.no/nibio-xmlui/handle/11250/3050195)). This small part is counted both here and in FS.FO-MP.OP.
- Imported wood fuel (about 200 000 m³ of energy wood in 2021, about 0.4 TWh, Belbo et al., 2022) enters MP.OP via Other goods import (HS 4401). The part burned in heat plants is therefore counted both as import and in this flow.

#### Interpretations and comparisons

- The flow rises from about 0.2 kt N in 1990 to 1.3–1.7 kt N in 2010–2020 and about 2.2 kt N in 2021–2024, following the expansion of wood-fired district heating.
- Before 2010 the CRT biomass in 1.A.1.a is larger than "Bark, flis og tre" in table 04730 (1990: 1 060 against 103 TJ), probably plants outside the district heating statistics.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
