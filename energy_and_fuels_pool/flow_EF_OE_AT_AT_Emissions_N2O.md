---
layout: default
title: Other energy emissions (N2O)
parent: Other energy and fuels (EF.OE)
nav_order: 1
---

# Other energy emissions (N2O)

<iframe src="../output_files/plots/EF_OE_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.OE-AT.AT-Emissions-N2O** is N2O from fuel combustion in other sectors (1.A.4 and 1.A.5), using the categories given in Table 14 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Data sources

- N2O from the UNFCCC Common Reporting Tables (CRT), Table 1, of the national greenhouse gas inventory.
- N2O from fuel combustion is not measured but calculated in the inventory as fuel consumption (TJ, by fuel type and source category, from the national energy statistics) multiplied by emission factors (kg N2O per TJ), following the IPCC 2006 Guidelines ([IPCC 2006, Vol. 2, Ch. 2](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf), [IPCC 2006, Vol. 2, Ch. 3](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_3_Ch3_Mobile_Combustion.pdf)); Norway uses a mix of IPCC default and country-specific emission factors, documented in the National Inventory Document ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)). Activity data and implied emission factors are reported in CRT Table 1.A(a).

#### Interpretations and comparisons

- Emissions from other sectors (1.A.4 and 1.A.5) are stable at 0.064–0.083 kt N/year.
- In 2024 they come in roughly equal parts from commercial/institutional (1.A.4.a), residential (1.A.4.b, mainly wood stoves) and agriculture, forestry and fishing (1.A.4.c, including fishing vessels and tractors).
- The decline in residential emissions after 2010 reflects reduced use of heating oil and firewood, while commercial emissions increased.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N2O from stationary combustion (Norway's GHG inventory, CRT 1.A) | Inventory with published uncertainty | −66.7/+200 %, lognormal | 100% | 100% | 1.00 | 1.00 | [Energy conversion emissions (N2O)](../energy_and_fuels_pool/flow_EF_EC_AT_AT_Emissions_N2O.html), [Industrial emissions (N2O)](../energy_and_fuels_pool/flow_EF_IC_AT_AT_Emissions_N2O.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
