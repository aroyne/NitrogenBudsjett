---
layout: default
title: Biologically treated organic waste to HS
parent: Solid Waste (PR.SO)
nav_order: 6
---

# Biologically treated organic waste to HS

<iframe src="../output_files/plots/PR_SO_HS_HS_Biologically_treated_organic_waste_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**PR.SO-HS.HS-Biologically treated organic waste-Nmix** is the N in compost and digestate from biological treatment of organic waste (composting and biogas production) used on green areas or delivered to soil producers. Sewage sludge that is treated biologically is counted in the PR.WW sludge flows and left out here.

**How the numbers are derived**

- N in: SSB's waste accounts ([table 10513](https://www.ssb.no/statbank/table/10513)) give the wet organic waste, park and garden waste and wood waste delivered to biogas production and to composting, multiplied by an N content per waste type (wet organic 0.9%, park and garden and wood 0.25%; Table 50 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)).
- N out: part of the N is lost as NH3, N2O and N2 during treatment; we assume a loss of 10% in biogas production (digestate_loss_fraction) and 30% in composting (compost_N_loss).
- Use: SSB's statistics on biological treatment ([table 12818](https://www.ssb.no/statbank/table/12818)) give how much compost and digestate is delivered to each use from 2018; this flow gets the share delivered to green areas and soil producers. Before 2018 the 2018 shares are used.
- The N is calculated from the N delivered to treatment, not from the mass of the products, since most of the mass lost during treatment is water and carbon (in 2018, 515 kt of waste was delivered and 286 kt of products were disposed of).
- Table 10513 starts in 2012; 1990–2011 are held at the 2012 value, although biological treatment was smaller in the 1990s.

**Interpretation**

- The flow is about 0.6–1.2 kt N per year; about a third of the compost and digestate goes to green areas and soil producers.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
