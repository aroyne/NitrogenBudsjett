---
layout: default
title: LUC Emissions (N2O)
parent: 6. Humans and settlements (HS)
nav_order: 2
---

# LUC Emissions (N2O)

<iframe src="../output_files/plots/HS_HS_AT_AT_LUC_emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HS.HS-AT.AT-LUC emissions-N2O** is N2O from soils in settlements, as reported under land use, land-use change and forestry (category 4.E Settlements in the greenhouse gas inventory).

#### Data sources

- N2O from "4.E. Settlements" in the UNFCCC Common Reporting Tables (CRT), Table 4, of the national greenhouse gas inventory ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)).
- The emissions are not measured but calculated in the inventory from activity data (N inputs, areas, losses of soil carbon) and emission factors, following the IPCC guidelines. In 2024 the category consists of three parts (CRT Tables 4(I)–4(III)):
- N inputs to soils in settlements (Table 4(I), 0.022 kt N/year): 1.9 kt N of organic fertilizers (such as sewage sludge and compost) applied to settlement areas, with direct emissions at an implied emission factor of 0.006 kg N2O–N per kg N, plus indirect emissions from the part of the N that volatilises (0.39 kt N) or is lost by leaching and run-off (0.44 kt N). Inorganic fertilizer used in settlements is reported under another category (notation key IE).
- Drained organic soils (Table 4(II), 0.046 kt N/year): area-based emission factors of about 1.5–1.6 kg N2O–N per hectare for forest and wetland converted to settlements (4.0 and 1.6 kha), and emissions from drained organic soils in settlements remaining settlements.
- Mineralisation of soil organic matter on land converted to settlements (Table 4(III), 0.032 kt N/year): the N released when soil carbon is lost (0.47 kt N on 73 kha in 2024, mainly forest and grassland converted to settlements) gives direct emissions and indirect emissions from leaching (0.011 kg N2O–N per kg N). Mineral soils in settlements remaining settlements are assumed to be in steady state and give no emissions.
#### Assumptions

- The inventory values are used directly, converted from N2O to N.

#### Interpretations and comparisons

- The flow rose from about 0.06 kt N in 1990 to 0.1 kt N around 2010 with the expansion of settlement areas, and has been about 0.1 kt N per year since.
- Inorganic fertilizer used in settlements (MP.OP-HS.HS-Mineral fertilizer-Nmix, about 2 kt N) is reported under another category in the inventory (IE), most likely agricultural soils (3.D). Its N2O, below 0.05 kt N per year, may therefore be counted in AG.SM-AT.AT-Emissions-N2O instead of here.
- The 1.9 kt N of organic fertilizer on settlement areas in the inventory is of the same size as the sewage sludge and biologically treated waste delivered to green areas and soil producers in this model (PR.WW-HS.HS-Sewage sludge fertilizer-Nmix and PR.SO-HS.HS-Biologically treated organic waste-Nmix, together about 2.3 kt N in 2024).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N2O from land use (Norway's GHG inventory, CRT 4) | Inventory with published uncertainty | ±201 %, lognormal | 100% | 100% | 1.00 | 1.00 | [Forest Emissions (N2)](../forests_and_semi_natural_pool/flow_FS_FO_AT_AT_Emissions_N2.html), [Forest Emissions (N2O)](../forests_and_semi_natural_pool/flow_FS_FO_AT_AT_Emissions_N2O.html) |
