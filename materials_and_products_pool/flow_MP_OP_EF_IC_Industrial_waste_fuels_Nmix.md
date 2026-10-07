---
layout: default
title: Industrial Waste Fuels
parent: Other Producing Industry (MP.OP)
nav_order: 5
---

# Industrial Waste Fuels

<iframe src="../output_files/plots/MP_OP_EF_IC_Industrial_waste_fuels_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-EF.IC-Industrial waste fuels-Nmix** is wood waste used as biofuel in the industries where the waste originates, reported as "egentilvirket bioenergi" (self-produced bioenergy) in SSB's statistics. “Egentilvirket bioenergi” encompasses “black liquor” as well as wood waste. Producers of wood and paper products obtain a significant fraction of their energy through this source.

#### Data sources

- SSB's statistics on energy use in manufacturing and mining ([Energibruk i industrien](https://www.ssb.no/energi-og-industri/energi/statistikk/energibruk-i-industrien), [table 08205](https://www.ssb.no/statbank/table/08205)), which start in 2003, are based on a survey of about 2,300 establishments, including the largest establishments in each industry, which together cover about 95% of the energy use; energy use in the remaining establishments is estimated from their energy costs.
- For 1990–2002, solid biofuels used in industry and mining from the energy balance ([SSB table 11561](https://www.ssb.no/statbank/table/11561), "12.1 Industri og bergverk").
- Net calorific value from Table 1.2 in Garg et al. (2006)<!--cite:garg_chapter_2006-->.

#### Assumptions

- For lack of better compositional details we have assumed values for the entire flow corresponding to wood, although this brings significant uncertainty.
- The values are converted to TJ, divided by a net calorific value of 15.6 TJ/kt and multiplied by a mean N content of 4.0 kg/t (0.4% N), the average of the whole-tree values in Table 45 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> (3.4 g/kg for conifers and 4.3 g/kg for broadleaves), since industrial waste wood (bark, sawdust, black liquor) is closer in composition to whole-tree biomass than to clean stem wood.
- The energy balance values for 1990–2002 are scaled to the level of table 08205 by the ratio of the two series over 2003–2007 (about 1.06), since the energy balance also includes purchased biofuels.

#### Interpretations and comparisons

- The flow is about 3.4–4.1 kt N per year until 2011, falls to about 1.7 kt N in 2014–2015 and has been 2.3–2.7 kt N since.
- The decline coincides with the closure of several pulp and paper mills, among them Norske Skog Follum (2012) and Södra Cell Tofte (2013).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Garg, A., Kazunari, K., & Pulles, T. (2006). Chapter 1. Introduction. *IPCC Guidelines for National Greenhouse Gas Inventories*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
