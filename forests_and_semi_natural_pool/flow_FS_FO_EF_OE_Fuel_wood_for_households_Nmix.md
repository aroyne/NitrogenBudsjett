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

- **FS.FO-EF.OE-Fuel wood for households-Nmix** is the N in wood burned in dwellings and holiday homes.

#### Data sources

- SSB's energy balance gives the wood burned in dwellings and holiday homes ([table 09702](https://www.ssb.no/statbank/table/09702), 'Energibalansen. Vedforbruk i boliger og fritidsboliger 1990 – 2024'). From 2005 the figures are based on SSB's survey of households' wood consumption; earlier years build on SSB's energy statistics and household surveys.
- N content of broadleaf stems with bark from Table 45 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- For 2005 the holiday-home figure is the 2006 value.
- Fuel wood is mainly stem wood with bark, much of it birch, so the N content of broadleaf stems is used: 1.4 g/kg, with a range from 0.7 g/kg (stems minus one standard deviation) to 4.3 g/kg (whole broadleaf trees including branches and foliage).

#### Interpretations and comparisons

- The flow is about 1.7–2.8 kt N per year. It rises from about 2.0 kt N in 1990 to a peak of 2.8 kt N in 2010, a cold winter, falls to about 1.9 kt N in 2015–2020 and rises again to 2.3 kt N in 2022, when electricity prices were high.
- The stem value is close to the 1.1 g/kg for stem with bark of conifers used by Hellsten et al. (2008), cited in the Swedish nitrogen budget (Jutterström et al., 2020)<!--cite:jutterstrom_swedish_2020-->; the Swedish budget uses the whole-tree value for fuel wood, as the guidance suggests when no other data are available.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of fuel wood burned in households | Parameter | 0.0007–0.0043, triangular | 98% | 98% | 1.00 | 1.00 | none |

### References

* Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation*.
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
