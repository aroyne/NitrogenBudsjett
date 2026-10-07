---
layout: default
title: Household and Settlement Waste
parent: 6. Humans and settlements (HS)
nav_order: 4
---

# Household and Settlement Waste

<iframe src="../output_files/plots/HS_HS_PR_SO_Household_waste_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**HS.HS-PR.SO-Household waste-Nmix** includes all types of solid waste from settlements which are processed in the sub-pool “solid waste” through incineration, landfilling, biofuel production or composting. We use data from SSB table 05282 “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og kilde” (1995-2011) and 10514 «Avfallsregnskap for Norge, etter kilde og materialtype (1 000 tonn) 2012 – 2023» with N contents taken from Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> and typical, assumed values are chosen if none are given. We include households, services (tjenesteytende næringer) and construction (Bygge- og anleggsvirksomhet). Power and water supply and the waste management sector are not included, since much of the waste from waste management is residues from treating waste that has already been counted.

Detailed data are not available prior to 1995, but trends in municipal and other waste are described by SSB (1997)<!--cite:ssb_naturressurser_1997-->. Household waste per inhabitant increased from about 200 kg/person to 289 kg/person in 1995 Figure 4.1 in (SSB, 1997)<!--cite:ssb_naturressurser_1997-->, with an assumed linear increase in the years between. Based on this we assume a constant N content per unit mass and extrapolate from 1995 values back to 1990. SSB revised the waste accounts from 2012 (table 10514). For private households the total amount is about the same in 2011 and 2012, but most residual waste is now reported as mixed waste instead of being split into materials; this changes the N only slightly and is not adjusted. For services and construction, table 10514 reports much more waste than table 05282, most likely because the new method builds on the waste received by treatment plants rather than on estimates per employee; the 1995–2011 values for these two sectors are therefore scaled by the ratio of their N in 2012 to that in 2011 (about 1.66).

**How the numbers are derived**

- SSB's waste accounts ([Avfallsregnskapet](https://www.ssb.no/natur-og-miljo/avfall/statistikk/avfallsregnskapet); tables [05282](https://www.ssb.no/statbank/table/05282) and [10514](https://www.ssb.no/statbank/table/10514)) give the generated amount of waste by material and source sector. Household waste is reported by the municipalities through KOSTRA; for services and construction SSB combines reports from waste treatment plants, surveys and estimates based on turnover or employees.
- The tonnes of each material are multiplied by an N content, mainly from Table 50 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf) (for example wet organic 0.9%, plastic 2.1%, paper 0.28%, mixed waste 0.9%).

**Interpretation**

- The flow rises from about 10 kt N in 1990 to 28–32 kt N in 2005–2019, with a dip in 2009, and falls to about 26 kt N in 2024.
- Private households account for 40–45% of the N; the rest comes from services and construction, which have grown more than households over the period.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
* SSB (1997). *Naturressurser og miljø 1997*.
