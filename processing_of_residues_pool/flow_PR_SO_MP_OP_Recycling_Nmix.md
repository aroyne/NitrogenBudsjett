---
layout: default
title: Material Recycling
parent: Solid Waste (PR.SO)
nav_order: 8
---

# Material Recycling

<iframe src="../output_files/plots/PR_SO_MP_OP_Recycling_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.SO-MP.OP-Recycling-Nmix** is the N in waste delivered to material recycling.
- We have not included the categories sludge, garden waste and wet organic material reported as being assigned to material recycling, because this use is rather for soil production or fertilizer and does not belong in the MP.OP subpool.

#### Data sources

- SSB's waste accounts ([Avfallsregnskapet](https://www.ssb.no/natur-og-miljo/avfall/statistikk/avfallsregnskapet)): table [05281](https://www.ssb.no/statbank/table/05281) “Avfallsregnskap for Norge (1 000 tonn), etter statistikkvariabel, behandlingsmåte, materialtype og år” (1995–2011) and table [10513](https://www.ssb.no/statbank/table/10513) “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og behandlingsmåte” (2012 onward) give the amount of waste by material and treatment method.
- SSB combines municipal reporting of household waste (KOSTRA), surveys of manufacturing companies, the companies' own reporting to Miljødirektoratet, figures from the recycling industry and, where data are missing, estimates based on turnover or number of employees.
- N contents per material, mainly from Table 50 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- The waste delivered to material recycling by material is multiplied by an N content per material.

#### Interpretations and comparisons

- The flow rises from about 0.8 kt N in 1990 to 2.6 kt N in 2011, jumps to 4.2 kt N in 2012 with the change of table, and is 3.4–7.7 kt N since.
- Table 10513 introduces a new, large "mixed waste" (blandet avfall) reporting category from 2012 with no equivalent in the earlier table 05281, which shows up as the jump from 2011 to 2012.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| Waste treatment from 2012 (SSB 10513) (recycling) | Survey or self-reported data | ±20 %, normal, drawn per year | – | 42% | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of other waste materials | N content of waste | ±50 %, lognormal | <1% | 22% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html) |
| N content of mixed waste | N content of waste | 0.001–0.012 (min–max), triangular | <1% | 17% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html) |
| N content of hazardous waste | N content of waste | 0.0005–0.006 (min–max), triangular | 1% | 6% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html) |
| N content of wood waste | N content of waste | 0.001–0.0049, triangular | 16% | 5% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html) and 2 more |
| N content of plastic waste | N content of waste | 0.002–0.008, lognormal | <1% | 3% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html) |
| N content of paper waste | N content of waste | ±20 %, normal | 2% | 2% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html) |
| Waste treatment 1995–2011 (SSB 05281) (recycling) | Survey or self-reported data | ±30 %, normal, drawn per year | 20% | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| Waste statistics 1985–1995 (SSB) | Assumption | ±50 %, triangular | 54% | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Sewage Sludge Fertilizer to Ag](../processing_of_residues_pool/flow_PR_WW_AG_SM_Sewage_sludge_fertilizer_Nmix.html), [Sewage Sludge Fertilizer to HS](../processing_of_residues_pool/flow_PR_WW_HS_HS_Sewage_sludge_fertilizer_Nmix.html) |
| Extrapolation (household waste:1995) | Gap filling: extrapolation | ±15–35 %, lognormal, grows with distance to known year | 5% | – | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
