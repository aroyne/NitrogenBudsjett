---
layout: default
title: Biologically treated organic waste to HS
parent: Solid Waste (PR.SO)
nav_order: 6
---

# Biologically treated organic waste to HS

<iframe src="../output_files/plots/PR_SO_HS_HS_Biologically_treated_organic_waste_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.SO-HS.HS-Biologically treated organic waste-Nmix** is the N in compost and digestate from biological treatment of organic waste (composting and biogas production) used on green areas or delivered to soil producers.
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
- This flow gets the share delivered to green areas and soil producers.

#### Interpretations and comparisons

- The flow is about 0.6–1.2 kt N per year; about a third of the compost and digestate goes to green areas and soil producers.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of wet organic waste | N content of waste | 0.004–0.0165, triangular | 32% | 82% | 0.85 | 0.92 | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Food Industry Waste](../materials_and_products_pool/flow_MP_FP_PR_SO_Food_industry_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html) and 3 more |
| Waste treatment from 2012 (SSB 10513) (biological treatment) | Survey or self-reported data | ±20 %, normal, drawn per year | 4% | 8% | 1.00 | 1.00 | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |
| Use of digestate and compost (SSB 12818) | Survey or self-reported data | ±20 %, normal, drawn per year | 4% | 6% | −1.10 | −0.85 | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |
| N loss in biogas treatment | Parameter | 0.06–0.3, triangular | <1% | 2% | −0.02 | −0.09 | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |
| N loss in composting | N content of waste | 0.1–0.7, triangular | 11% | 2% | −0.34 | −0.09 | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |
| Held constant or averaged (biologically treated waste:2012) | Gap filling: held constant or averaged | ±100–120 %, lognormal, grows with distance to known year | 48% | – | 1.00 | – | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
