---
layout: default
title: Other Industry Waste
parent: Other Producing Industry (MP.OP)
nav_order: 10
---

# Other Industry Waste

<iframe src="../output_files/plots/MP_OP_PR_SO_Other_industry_waste_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-PR.SO-Other industry waste-Nmix** is waste from mining, manufacturing (except wet organic waste, which is assigned to the food industry) and other or unspecified industries (annen eller uspesifisert næring).
- The category “contaminated waste” is very irregularly reported (placed in different sectors in different years) and has therefore been excluded.

#### Data sources

- SSB's waste accounts ([Avfallsregnskapet](https://www.ssb.no/natur-og-miljo/avfall/statistikk/avfallsregnskapet)): table [05282](https://www.ssb.no/statbank/table/05282) “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og kilde” (1995–2011) and table [10514](https://www.ssb.no/statbank/table/10514) «Avfallsregnskap for Norge, etter kilde og materialtype (1 000 tonn)» (2012 onward) give the generated amount of waste by material type and source sector. The statistic does not separate between food and other industry waste.
- SSB combines several sources: a periodic survey of about 1,600 manufacturing companies, the companies' own reporting to Miljødirektoratet in the years between, statistics on hazardous waste and waste from construction, figures from the recycling industry, and, where data are missing, estimates based on turnover or number of employees.
- SSB (1997)<!--cite:ssb_naturressurser_1997--> reports the change in industry waste between 1992 and 1995.

#### Assumptions

- We make the assumption that everything in the category “wet organic waste” is from the food industry, and all other waste is assigned to other producing industry.
- This flow uses the materials paper, plastics, wood, textiles, other materials, hazardous waste and (from 2012) mixed waste from the source sectors "Bergverk og utvinning", "Industri" and "Annen eller uspesifisert næring", plus wet organic waste from "Bergverk og utvinning".
- N contents are mainly from Table 50 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->: paper 0.28%, wood 0.25%, textiles 1%, hazardous waste 0.1%; mixed waste (0.9%) and other materials (0.2%) are assumed values, and typical, assumed values are chosen if none are given.
- Plastic is set to 0.4% N (95% interval 0.2–0.8%) instead of the 2.1% in Table 50: the N-bearing polymers (polyurethane, polyamide, cellulose nitrate, acrylic) make up 0.40–0.44% N of the plastics imported to Norway (HS 39, 1990–2024), domestic polymer production (PE, PP, PVC) contains no N, and amino resins are left out because they are used as glue in wood panels and end up as wood waste. Plastic waste cannot contain more N than the plastic that enters use; the upper bound allows for food residues and other contamination.
- There is a change in categorization between the two tables, where the main difference is in the category “other waste” and “mixed waste”. To ensure continuity between the data series we chose a lower value for “other waste” than for “mixed waste”.
- Values between 1990 and 1994 are extrapolated from 1995 given the change in industry waste reported between 1992 and 1995.

#### Interpretations and comparisons

- The flow is about 6–7 kt N per year in the mid-1990s, 5–6 kt N after 2000 (4.7–4.9 kt N in 2012–2015) and about 6 kt N in 2024.
- In 2024 mixed waste accounts for about 70% of the N, hazardous waste for about 17% and plastics for about 3%.
- Since the N contents of mixed waste and other materials are assumed, the level is uncertain.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| N content of hazardous waste | N content of waste | 0.0005–0.006 (min–max), triangular | 14% | 53% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
| N content of mixed waste | N content of waste | 0.001–0.012 (min–max), triangular | – | 25% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
| Waste accounts from 2012, industry (SSB 10514) | Modelled statistics | ±30 %, normal | – | 21% | [Food Industry Waste](../materials_and_products_pool/flow_MP_FP_PR_SO_Food_industry_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html) |
| N content of wood waste | N content of waste | 0.001–0.0049, triangular | 27% | <1% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html) and 2 more |
| N content of plastic waste | N content of waste | 0.002–0.008, lognormal | 3% | <1% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
| N content of textile waste | N content of waste | 0.0017–0.029 (min–max), triangular | 3% | <1% | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
| Waste accounts 1995–2011, industry (SSB 05282) | Modelled statistics | ±30 %, normal | 33% | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
| Extrapolation (other industry waste:1995) | Gap filling: extrapolation | ±15–35 %, lognormal, grows with distance to known year | 18% | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
* SSB (1997). *Naturressurser og miljø 1997*.
