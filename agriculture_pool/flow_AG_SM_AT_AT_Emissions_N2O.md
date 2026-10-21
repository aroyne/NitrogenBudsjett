---
layout: default
title: N2O emissions from denitrification
parent: Soil Management (AG.SM)
nav_order: 3
---

# N2O emissions from denitrification

<iframe src="../output_files/plots/AG_SM_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.SM-AT.AT-Emissions-N2O** is direct N2O from mineral fertilizer, manure, sewage sludge, grazing animals, crop residues, mineralisation and cultivated organic soils, and indirect N2O from N that volatilises or leaches.

#### Data sources

- N2O from "3.D. Agricultural soils" in the UNFCCC Common Reporting Tables (CRT), Table 3, of the national greenhouse gas inventory, calculated as the N applied by each source multiplied by IPCC emission factors ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)).
- The inventory counts all manure deposited by grazing animals as input to managed soils, including the share deposited on utmark (unmanaged land), which this model does not count as input to AG.SM (see AG.MM-AG.SM-Manure application-Nmix).

#### Assumptions

- The utmark share (26–33% of grazing manure, see AG.MM-AG.SM-Manure application-Nmix) of the losses from grazing manure is therefore removed from this flow; it is counted in FS.OL-AT.AT-Emissions-N2O.
- The removed N2O is the utmark share of the direct N2O from grazing manure (3.D.1.c) plus the indirect N2O from its volatilisation and leaching, calculated with the fractions and implied emission factors in CRT Table 3.D (about 0.1 kt N per year).

#### Interpretations and comparisons

- The flow is about 3.4–3.9 kt N per year, with a slight decrease since 1990.
- The uncertainty is large, mainly from the emission factors (a factor of 3 in Norway's greenhouse gas inventory).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N2O from agricultural soils (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | −66.7/+200 %, lognormal | 100% | 100% | 1.00 | 1.00 | [Other Land Emissions (N2O)](../forests_and_semi_natural_pool/flow_FS_OL_AT_AT_Emissions_N2O.html) |
