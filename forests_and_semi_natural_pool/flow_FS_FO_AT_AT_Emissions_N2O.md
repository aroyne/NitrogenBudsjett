---
layout: default
title: Forest Emissions (N2O)
parent: Forests (FS.FO)
nav_order: 2
---

# Forest Emissions (N2O)

<iframe src="../output_files/plots/FS_FO_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.FO-AT.AT-Emissions-N2O** is N2O from forest land, as reported under land use, land-use change and forestry (category 4.A Forest land in the greenhouse gas inventory).

#### Data sources

- N2O from "4.A. Forest land" in the UNFCCC Common Reporting Tables (CRT), Table 4, of the national greenhouse gas inventory ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)).
- The emissions are not measured but calculated in the inventory from activity data (areas, N inputs, burned area) and emission factors, following the IPCC guidelines. In 2024 the category consists of (CRT Tables 4(I)–4(IV)):
    - Drained organic forest soils (Table 4(II), 0.36 of 0.38 kt N/year): 128 kha drained organic soil in forest remaining forest with 2.8 kg N2O–N per ha, plus a small area of cropland converted to forest.
    - Fertilization of forest (Table 4(I), 0.009 kt N/year): 0.47 kt N of inorganic fertilizer, with direct emissions and indirect emissions from volatilised and leached N.
    - Mineralisation of soil organic matter after land-use change to forest (Table 4(III), 0.001 kt N/year).
    - Forest fires (Table 4(IV), 427 ha burned in 2024, 0.0006 kt N/year).
- The inventory gives an uncertainty of 201% (95% interval).

#### Assumptions

- The uncertainty is modelled as a lognormal distribution with the reported value as median.

#### Interpretations and comparisons

- The flow is small and nearly constant, about 0.37–0.38 kt N per year, since the area of drained organic forest soil changes little.
- The 0.47 kt N of fertilizer on forest in the inventory is the same as MP.OP-FS.FO-Mineral fertilizer-Nmix in this model in 2024.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| N2O from land use (Norway's GHG inventory, CRT 4) | Inventory with published uncertainty | ±201 %, lognormal | 100% | 100% | [Forest Emissions (N2)](../forests_and_semi_natural_pool/flow_FS_FO_AT_AT_Emissions_N2.html), [LUC Emissions (N2O)](../humans_and_settlements_pool/flow_HS_HS_AT_AT_LUC_emissions_N2O.html) |
