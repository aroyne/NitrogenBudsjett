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

#### Interpretations

- The flow is stable at 1.1–1.3 kt N per year<!--range:MP.FP-AG.SM-Seeds and planting material -Nmix:1984-2025-->.
- Cereal seed (about 54,000 t in 2024) accounts for over 90% of the N, and grass seed for most of the rest.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Totalkalkylen for agriculture (NIBIO) (seeds) | Modelled statistics | ±30 %, normal | 84% | 84% | 1.00 | 1.00 | none |
| Protein content of cereal seed | Parameter | ±10 %, normal | 9% | 9% | 0.95 | 0.93 | none |
| Protein-to-N factor for cereal seed | Parameter | ±10 %, normal | 7% | 7% | −0.86 | −0.84 | none |

### References

* Budsjettnemnda for jordbruket (2025). *Totalkalkylen for jordbruket - statistikk*. [nibio.no](https://www.nibio.no/tjenester/totalkalkylen-statistikk)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
