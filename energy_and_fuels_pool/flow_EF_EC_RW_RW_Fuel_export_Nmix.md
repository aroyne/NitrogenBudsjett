---
layout: default
title: Fuel export
parent: Energy conversion (EF.EC)
nav_order: 7
---

# Fuel export

<iframe src="../output_files/plots/EF_EC_RW_RW_Fuel_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.EC-RW.RW-Fuel export-Nmix** is the nitrogen in exported fuels: all petroleum products and other fuels except those assumed to be used in the transport sector.
- Natural gas exports (HS code 2711) are not captured here: they are a comparably large export by mass and energy content, but natural gas itself has negligible nitrogen content and is therefore not expected to materially affect the national N budget.

#### Data sources

- Export quantities (kg) by HS commodity code from [SSB table 08801](https://www.ssb.no/statbank/table/08801). Export quantities in the trade statistics are registered by customs and are therefore observed rather than modelled.
- N contents per fuel type from Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- N contents: crude oil (HS 2709) 0.10% (lognormal with this median and 0.05% and 0.20% as the lower and upper end of the 95% interval, from Equinor's assays of 21 Norwegian crudes: 0.01–0.20% total nitrogen, about 0.12% weighted by production in 2020–2024 and 0.08% in the 1990s), residual fuel oil 0.45%, gas/diesel oil 0.0133%, kerosene 0.1%, other oils 0.0375%, bitumen 0.7%, coal and coke 1.0–1.85% and peat 0.2%; gasoline, naphtha and natural gas condensate are included with zero N (Table 15: gasoline 0, naphtha and NGL not specified).

#### Interpretations

- Crude oil dominates the flow, accounting for over 99% of its N content. The flow is 70–85 kt N per year in 2012–2024, after a peak of about 145 kt N around 2000 when crude oil exports were highest.
- The uncertainty of the flow lies mainly in the N content of crude oil, which varies between fields.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-04). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: crude oil | N content of traded goods | 0.0005–0.002, lognormal | 99% | 99% | 0.94 | 0.96 | [Fuel Import](../rest_of_the_world_pool/flow_RW_RW_EF_EC_Fuel_import_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
