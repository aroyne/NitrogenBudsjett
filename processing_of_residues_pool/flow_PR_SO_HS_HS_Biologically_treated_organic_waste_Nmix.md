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
- For 1995–2011, the waste delivered to composting in SSB's earlier waste accounts ([table 05281](https://www.ssb.no/statbank/table/05281)), where other biological treatment (biogas) is included in composting.
- SSB's statistics on biological treatment ([table 12818](https://www.ssb.no/statbank/table/12818)) give how much compost and digestate is delivered to each use from 2018.
- N contents per waste type from Table 50 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: wet organic 0.9%, park and garden and wood 0.25%.

#### Assumptions

- N in the waste delivered to biogas production and composting multiplied by the N content per waste type.
- N out: part of the N is lost as NH<sub>3</sub>, N<sub>2</sub>O and N<sub>2</sub> during treatment; we assume a loss of 10% in biogas production (digestate_loss_fraction) and 30% in composting (compost_N_loss).
- The N is calculated from the N delivered to treatment, not from the mass of the products, since most of the mass lost during treatment is water and carbon (in 2018, 515 kt of waste was delivered and 286 kt of products were disposed of).
- Before 2018 the 2018 shares by use are used.
- 1995–2011: the wet organic and wood waste delivered to composting in table 05281 (park and garden waste is probably included in wood waste there) times the N out per tonne in 2012. The amounts in the two tables agree well at the break (400 kt in 2011 and 438 kt in 2012).
- 1990–1994 are held at the 1995 value, which is small (57 kt of waste delivered).
- This flow gets the share delivered to green areas and soil producers.

#### Interpretations

- The flow rises from about 0.07 kt N per year<!--mean:PR.SO-HS.HS-Biologically treated organic waste-Nmix:1990-1995--> in 1990–1995 to 0.6 kt N<!--val:PR.SO-HS.HS-Biologically treated organic waste-Nmix:2010--> in 2010 and 0.5–1.5 kt N per year<!--range:PR.SO-HS.HS-Biologically treated organic waste-Nmix:2012-2024--> since 2012; about a third of the compost and digestate goes to green areas and soil producers.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of wet organic waste | N content of waste | 0.004–0.0165, triangular | 52% | 82% | 0.85 | 0.92 | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Food Industry Waste](../materials_and_products_pool/flow_MP_FP_PR_SO_Food_industry_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html) and 3 more |
| Waste treatment from 2012 (SSB 10513) (biological treatment) | Survey or self-reported data | ±20 %, normal, drawn per year | – | 8% | – | 1.00 | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |
| Use of digestate and compost (SSB 12818) | Survey or self-reported data | ±20 %, normal, drawn per year | 7% | 6% | −1.10 | −0.85 | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |
| N loss in biogas treatment | Parameter | 0.06–0.3, triangular | <1% | 2% | −0.02 | −0.09 | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |
| N loss in composting | N content of waste | 0.1–0.7, triangular | 19% | 2% | −0.34 | −0.09 | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |
| Waste treatment 1995–2011 (SSB 05281) (biological treatment) | Survey or self-reported data | ±30 %, normal, drawn per year | 14% | – | 1.00 | – | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |
| Held constant or averaged (biologically treated waste:1995) | Gap filling: held constant or averaged | ±15–35 %, lognormal, grows with distance to known year | 7% | – | 1.00 | – | [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
