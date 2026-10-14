---
layout: default
title: Household and Settlement Waste
parent: 6. Humans and settlements (HS)
nav_order: 4
---

# Household and Settlement Waste

<iframe src="../output_files/plots/HS_HS_PR_SO_Household_waste_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HS.HS-PR.SO-Household waste-Nmix** includes all types of solid waste from settlements which are processed in the sub-pool “solid waste” through incineration, landfilling, biofuel production or composting.
- We include households, services (tjenesteytende næringer) and construction (Bygge- og anleggsvirksomhet). Power and water supply and the waste management sector are not included, since much of the waste from waste management is residues from treating waste that has already been counted.

#### Data sources

- SSB's waste accounts ([Avfallsregnskapet](https://www.ssb.no/natur-og-miljo/avfall/statistikk/avfallsregnskapet)): table [05282](https://www.ssb.no/statbank/table/05282) “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og kilde” (1995–2011) and table [10514](https://www.ssb.no/statbank/table/10514) «Avfallsregnskap for Norge, etter kilde og materialtype (1 000 tonn)» (2012 onward) give the generated amount of waste by material and source sector.
- Household waste is reported by the municipalities through KOSTRA; for services and construction SSB combines reports from waste treatment plants, surveys and estimates based on turnover or employees.
- SSB revised the waste accounts from 2012 (table 10514). For private households the total amount is about the same in 2011 and 2012, but most residual waste is now reported as mixed waste instead of being split into materials. For services and construction, table 10514 reports much more waste than table 05282, most likely because the new method builds on the waste received by treatment plants rather than on estimates per employee.
- For services, SSB has surveys only for 1999 and 2006 (pilot); from 2008 the numbers are based on customer registers from a sample of waste collectors (the sample was expanded for 2008–2010), scaled up with a model where the number of employees is the explanatory variable ([SSB, about the statistics](https://www.ssb.no/natur-og-miljo/statistikker/avfhandel/aar/2013-12-11?fane=om)). In table 05282 the services materials grow in nearly fixed proportions from 1995 to 2008, so these years appear to be projected rather than measured. For construction, 2000–2004 appear to be linearly interpolated (e.g. plastic rises by exactly 5 kt per year).
- Detailed data are not available prior to 1995, but trends in municipal and other waste are described by SSB (1997)<!--cite:ssb_naturressurser_1997-->: household waste per inhabitant increased from about 200 kg/person to 289 kg/person in 1995 (Figure 4.1 in SSB, 1997<!--cite:ssb_naturressurser_1997-->).

#### Assumptions

- The tonnes of each material are multiplied by an N content, mainly from Table 50 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025--> (for example wet organic 0.9%, plastic 2.1%, paper 0.28%, mixed waste 0.9%); typical, assumed values are chosen if none are given.
- The change to mixed waste for private households in 2012 changes the N only slightly and is not adjusted.
- The 1995–2011 values for services and construction are scaled by the ratio of their N in 2012 to that in 2011 (about 1.66).
- 1990–1994: we assume a linear increase in waste per inhabitant between about 200 kg/person and 289 kg/person in 1995, and a constant N content per unit mass, and extrapolate from the 1995 value back to 1990.

#### Interpretations and comparisons

- The flow rises from about 10 kt N in 1990 to 28–32 kt N in 2005–2019, with a dip in 2009, and falls to about 26 kt N in 2024.
- Private households account for 40–45% of the N; the rest comes from services and construction, which have grown more than households over the period.
- The flow rises faster than the population up to 2008. For private households the growth is real: waste per inhabitant rose from about 290 kg in 1995 to about 470 kg in 2011, following higher consumption. The services and construction values follow employment and building activity, and because they are scaled by about 1.66 they make up about two thirds of the flow before 2012 and determine its shape.
- The dip from 2008 to 2009 (about −4.6 kt N) comes mainly from services (about −3.6 kt N). SSB reported a 19% decrease in waste from services from 2008 to 2009 and wrote that the cause is not known ([SSB 2011](https://www.ssb.no/natur-og-miljo/statistikker/avfhandel/aar/2011-12-12)). The composition also changes abruptly (paper 519 → 338 kt, other materials 59 → 103 kt), which points to a break in the data rather than a real change: the expanded sample of waste collectors, and the full change to the SN2007 industry classification from 2009 (which moved e.g. publishing from manufacturing to services). Construction accounts for about −0.8 kt N, probably a real effect of the financial crisis (SSB reported a further 10% decrease for construction from 2009 to 2010; [SSB 2011](https://www.ssb.no/natur-og-miljo/statistikker/avfregno/aar/2011-12-14)), and private households for about −0.3 kt N.
- The services values before 2009 are therefore probably too high. Because the scaling to table 10514 is based on 2011, after the break, the higher pre-2009 level is carried into the scaled series. This is not corrected.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
* SSB (1997). *Naturressurser og miljø 1997*.
