---
layout: default
title: Export of transport fuels
parent: Transportation (EF.TR)
nav_order: 4
---

# Export of transport fuels

<iframe src="../output_files/plots/EF_TR_RW_RW_Export_of_transport_fuels_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.TR-RW.RW-Export of transport fuels-Nmix** is the export of fuels assumed to be used in the transport sector: motor and aviation gasoline and jet fuel (jet gasoline and jet kerosene).
- Naphtha, which is mainly a petrochemical feedstock, is counted in EF.EC-RW.RW-Fuel export.

#### Data sources

- Export quantities (kg) by HS commodity code from [SSB table 08801](https://www.ssb.no/statbank/table/08801), registered by customs and therefore observed rather than modelled.
- N contents from Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- Motor and aviation gasoline 0% N, jet fuel 0.1% N; the HS codes are defined in the trade mapping sheet of N_parameters.xlsx.

#### Interpretations and comparisons

- Since gasoline has no fuel-bound nitrogen, the flow is small (below 0.5 kt N per year) and consists of jet fuel exports.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: jet fuel | N content of traded goods | ±20 %, normal | 94% | 94% | 1.00 | 1.00 | [Transport Fuel Import](../rest_of_the_world_pool/flow_RW_RW_EF_TR_Import_of_transport_fuel_Nmix.html) |
| Traded quantities (SSB 08801) (transport_fuel) | Registered data | ±5 %, normal, drawn per year | 6% | 6% | 1.00 | 1.00 | [Transport Fuel Import](../rest_of_the_world_pool/flow_RW_RW_EF_TR_Import_of_transport_fuel_Nmix.html) |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
