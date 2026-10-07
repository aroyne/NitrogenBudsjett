---
layout: default
title: Biologically treated organic waste to Ag
parent: Solid Waste (PR.SO)
nav_order: 1
---

# Biologically treated organic waste to Ag

<iframe src="../output_files/plots/PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.SO-AG.SM-Biologically treated organic waste-Nmix** is the N in compost and digestate from biological treatment of organic waste (composting and biogas production) used on agricultural land.
- Sewage sludge that is treated biologically is counted in the PR.WW sludge flows and left out here.

#### Data sources

- SSB's waste accounts ([table 10513](https://www.ssb.no/statbank/table/10513)) give the wet organic waste, park and garden waste and wood waste delivered to biogas production and to composting; the table starts in 2012.
- SSB's statistics on biological treatment ([table 12818](https://www.ssb.no/statbank/table/12818)) give how much compost and digestate is delivered to each use from 2018.
- N contents per waste type from Table 50 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->: wet organic 0.9%, park and garden and wood 0.25%.

#### Assumptions

- N in: the waste delivered to biogas production and composting multiplied by the N content per waste type.
- N out: part of the N is lost as NH3, N2O and N2 during treatment; we assume a loss of 10% in biogas production (digestate_loss_fraction) and 30% in composting (compost_N_loss).
- The N is calculated from the N delivered to treatment, not from the mass of the products, since most of the mass lost during treatment is water and carbon (in 2018, 515 kt of waste was delivered and 286 kt of products were disposed of).
- Before 2018 the 2018 shares by use are used.
- 1990–2011 are held at the 2012 value, although biological treatment was smaller in the 1990s.
- This flow gets the share delivered to agricultural land.

#### Interpretations and comparisons

- The flow is about 0.7–1.3 kt N per year; about a third of the compost and digestate goes to agricultural land.
- It rises from 2012 with more biogas production, and digestate from biogas plants is mostly used in agriculture.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
