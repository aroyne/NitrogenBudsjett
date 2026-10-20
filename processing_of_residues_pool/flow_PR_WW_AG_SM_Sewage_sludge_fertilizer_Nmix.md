---
layout: default
title: Sewage Sludge Fertilizer to Ag
parent: Wastewater (PR.WW)
nav_order: 1
---

# Sewage Sludge Fertilizer to Ag

<iframe src="../output_files/plots/PR_WW_AG_SM_Sewage_sludge_fertilizer_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.WW-AG.SM-Sewage sludge fertilizer-Nmix** is the N in sewage sludge used on agricultural land.

#### Data sources

- SSB's statistics on sewage sludge ([table 05279](https://www.ssb.no/statbank/table/05279) “Avløpsslam, etter slamdisponering, statistikkvariabel, år og region”) give the amount of sludge (tonnes dry matter) from municipal wastewater treatment plants by disposal, based on the plants' reporting through KOSTRA. For 1993–2001 the amounts and shares by disposal are taken from SSB's Naturressurser og miljø series.
- [NIBIO](https://www.nibio.no/tema/jord/organisk-avfall-som-gjodsel/avlopsslam) gives 20–40 kg total N per tonne dry matter for Norwegian sewage sludge. There are no public Norwegian data on N in sludge from different treatment processes (Frøseth et al., 2025, NIBIO Rapport 11(124)).

#### Assumptions

- 1990–1992 are the mean of 1993–1995.
- The dry matter is multiplied by an N content of 3% (range 2–4%), the middle of the NIBIO range.

#### Interpretations and comparisons

- The flow is about 1.0–2.5 kt N per year; about 40–60% of the sewage sludge in Norway is used on agricultural land.
- For comparison, Tables 54 and 55 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> give 2.6–3.7% N in dry matter for dewatered, digested and composted sludge in the JRC models (Huygens et al., 2022) and a median of 4.9% in German analyses (Sichler et al., 2022).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of sewage sludge | N content of waste | 0.02–0.04, normal | 29% | 84% | 1.00 | 1.00 | [Sewage Sludge Fertilizer to HS](../processing_of_residues_pool/flow_PR_WW_HS_HS_Sewage_sludge_fertilizer_Nmix.html), [Sewage Sludge to Landfill](../processing_of_residues_pool/flow_PR_WW_PR_SO_Sewage_sludge_landfill_Nmix.html) |
| Sewage sludge disposal (SSB 05279) | Survey or self-reported data | ±15 %, normal, drawn per year | – | 16% | – | 1.00 | [Sewage Sludge Fertilizer to HS](../processing_of_residues_pool/flow_PR_WW_HS_HS_Sewage_sludge_fertilizer_Nmix.html), [Sewage Sludge to Landfill](../processing_of_residues_pool/flow_PR_WW_PR_SO_Sewage_sludge_landfill_Nmix.html) |
| Waste statistics 1985–1995 (SSB) | Assumption | ±50 %, triangular | 66% | – | 1.00 | – | [Consumer Goods (Mass Balance)](../materials_and_products_pool/flow_MP_OP_HS_HS_Consumer_goods_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html), [Sewage Sludge Fertilizer to HS](../processing_of_residues_pool/flow_PR_WW_HS_HS_Sewage_sludge_fertilizer_Nmix.html) |
| Held constant or averaged (sewage sludge:1993-1995) | Gap filling: held constant or averaged | ±15–25 %, lognormal, grows with distance to known year | 5% | – | 1.00 | – | [Sewage Sludge Fertilizer to HS](../processing_of_residues_pool/flow_PR_WW_HS_HS_Sewage_sludge_fertilizer_Nmix.html), [Sewage Sludge to Landfill](../processing_of_residues_pool/flow_PR_WW_PR_SO_Sewage_sludge_landfill_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
