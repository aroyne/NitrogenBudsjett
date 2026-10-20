---
layout: default
title: Fuel Import
parent: Rest of the world (RW)
nav_order: 6
---

# Fuel Import

<iframe src="../output_files/plots/RW_RW_EF_EC_Fuel_import_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **RW.RW-EF.EC-Fuel import-Nmix** is the N in imported fuels, all fuel items except those for transport.

#### Data sources

- Import quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from customs declarations.

#### Assumptions

- The quantities are multiplied by an N content per commodity type from the trade mapping sheet of N_parameters.xlsx.
- All fuel commodity codes except transport fuels are included.

#### Interpretations and comparisons

- The flow is about 13–28 kt N per year, highest around 1996–2000 and lowest in 2010–2013 (13–15 kt N), and about 14–20 kt N per year since 2014.
- Unlike the export side, coal products (coking coal, bituminous coal, anthracite) dominate here rather than crude oil, since Norway imports comparatively little crude oil but relies on imported coal for coking and industrial use.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: bitomenous coal | N content of traded goods | 0.005–0.025, triangular | 4% | 49% | 0.08 | 0.33 | none |
| N content of traded goods: residual fuel oil | N content of traded goods | 0.001–0.008 (min–max), triangular | 12% | 24% | 0.15 | 0.26 | [Fuel export](../energy_and_fuels_pool/flow_EF_EC_RW_RW_Fuel_export_Nmix.html) |
| N content of traded goods: coking coal | N content of traded goods | 0.0057–0.0168, triangular | 24% | 11% | 0.26 | 0.20 | none |
| N content of traded goods: crude oil | N content of traded goods | 0.0005–0.002, lognormal | 3% | 7% | 0.07 | 0.10 | [Fuel export](../energy_and_fuels_pool/flow_EF_EC_RW_RW_Fuel_export_Nmix.html) |
| N content of traded goods: anthracite | N content of traded goods | 0.002–0.035 (min–max), triangular | 5% | 5% | 0.09 | 0.09 | none |
| Traded quantities (SSB 08801) (fuel) | Registered data | ±5 %, normal, drawn per year | 3% | 2% | 1.00 | 1.00 | [Fuel export](../energy_and_fuels_pool/flow_EF_EC_RW_RW_Fuel_export_Nmix.html) |
| N content of traded goods: lignite | N content of traded goods | 0.004–0.025 (min–max), triangular | 49% | <1% | 0.34 | 0.00 | none |
