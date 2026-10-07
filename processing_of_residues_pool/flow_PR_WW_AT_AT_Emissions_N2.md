---
layout: default
title: N2 Emissions (Wastewater)
parent: Wastewater (PR.WW)
nav_order: 2
---

# N2 Emissions (Wastewater)

<iframe src="../output_files/plots/PR_WW_AT_AT_Emissions_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Found by using data on N emissions and removal rates from the six wastewater treatment plants that were equipped with nitrogen removal through 2024, joined by a seventh (Hokksund) from 2025. Where specific data on nitrogen removal fraction were missing we assumed a default 70 %, and we extrapolated or interpolated between existing data where reported emission data were missing. The amount of N released as N2 was calculated as N_released*removal_rate/(1-removal_rate). 

**How the numbers are derived**

- Only treatment plants with biological nitrogen removal release significant amounts of N2. The flow covers the plants with nitrogen removal: Lillehammer (from 1995), VEAS and Nordre Follo (from 1997), Gardermoen (from 1998), Bekkelaget (from 2002), NRVA (from 2003) and Hokksund (from 2025).
- For each plant, the N discharged (reported in Norske utslipp or by the plant) is converted to N removed with the plant's reported removal rate r as N discharged × r/(1 − r); where no rate is reported, a default of 70% is used.

**Interpretation**

- The flow rises from 0.1 kt N in 1995 to 1.5–1.6 kt N around 2000 and 3.4–4.9 kt N since 2012, as more plants have introduced nitrogen removal.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
