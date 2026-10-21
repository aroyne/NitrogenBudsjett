---
layout: default
title: Seeds and Planting Material
parent: Food and Feed Processing (MP.FP)
nav_order: 2
---

# Seeds and Planting Material

<iframe src="../output_files/plots/MP_FP_AG_SM_Seeds_and_planting_material__Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-AG.SM-Seeds and planting material-Nmix** is purchased seed and planting material (cereals, oilseeds, peas, grass seed and root and vegetable seed). Seed saved on the farm is not purchased and is therefore not part of this flow.

#### Data sources

- Totalkalkylen for jordbruket (Budsjettnemnda for jordbruket, 2025)<!--cite:bfj_totalkalkylen_2025-->, compiled by NIBIO, gives the quantities of seed purchased by Norwegian farms (tonnes per year).
- Protein contents and crop-specific protein-to-N factors from Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- The quantities are multiplied by a protein content (cereals 12%, oilseeds 19.6%, peas 22.5%, grass and root/vegetable seed assumed 12%) and divided by a protein-to-N factor (5.83 for cereals, 6.25 for the others).

#### Interpretations and comparisons

- The flow is stable at 1.1–1.3 kt N per year.
- Cereal seed (about 54,000 t in 2024) accounts for over 90% of the N, and grass seed for most of the rest.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Totalkalkylen for agriculture (NIBIO) (seeds) | Modelled statistics | ±30 %, normal | 84% | 84% | 1.00 | 1.00 | none |
| Protein content of cereal seed | Parameter | ±10 %, normal | 9% | 9% | 0.95 | 0.93 | none |
| Protein-to-N factor for cereal seed | Parameter | ±10 %, normal | 7% | 7% | −0.86 | −0.84 | none |

### References

* Budsjettnemnda for jordbruket (2025). *Totalkalkylen for jordbruket - statistikk*. [https://www.nibio.no/tjenester/totalkalkylen-statistikk](https://www.nibio.no/tjenester/totalkalkylen-statistikk)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
