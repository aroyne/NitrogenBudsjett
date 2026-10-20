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

- The flow is about 19–32 kt N per year, highest around 1999 and lowest around 2010, and about 19–28 kt N per year in 2010–2024.
- Unlike the export side, coal products (coking coal, bituminous coal, anthracite) dominate here rather than crude oil, since Norway imports comparatively little crude oil but relies on imported coal for coking and industrial use.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| N content of traded goods: crude oil | N content of traded goods | 0.0002–0.015, lognormal | 76% | 76% | [Fuel export](../energy_and_fuels_pool/flow_EF_EC_RW_RW_Fuel_export_Nmix.html) |
| N content of traded goods: bitomenous coal | N content of traded goods | 0.005–0.025, triangular | 1% | 13% | none |
| N content of traded goods: residual fuel oil | N content of traded goods | 0.001–0.008 (min–max), triangular | 3% | 7% | [Fuel export](../energy_and_fuels_pool/flow_EF_EC_RW_RW_Fuel_export_Nmix.html) |
| N content of traded goods: coking coal | N content of traded goods | 0.0057–0.0168, triangular | 6% | 3% | none |
| N content of traded goods: lignite | N content of traded goods | 0.004–0.025 (min–max), triangular | 12% | <1% | none |
