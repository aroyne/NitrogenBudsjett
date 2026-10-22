---
layout: default
title: Consumer Goods (Mass Balance)
parent: Other Producing Industry (MP.OP)
nav_order: 7
---

# Consumer Goods (Mass Balance)

<iframe src="../output_files/plots/MP_OP_HS_HS_Consumer_goods_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.OP-HS.HS-Consumer goods-Nmix** is the N in domestic consumer goods, calculated by mass balance, assuming that all incoming flows to OP that are not accounted for in outgoing flows end up in domestic consumer goods.
- The fertilizer industry is kept out of the balance: we have excluded N2 fixation for ammonia synthesis, ammonia import and export, mineral fertilizer flows, and the wastewater from fertilizer plants (Yara Porsgrunn, Yara Glomfjord, Herøya industrial park and Hydro Rjukan). We also exclude emissions to air from the balance because they result mainly from fertilizer production.

#### Data sources

- The flow is not measured but calculated as the residual of the inflows and outflows listed under Assumptions, each documented on its own page.

#### Assumptions

- Incoming flows:
    - AG.SM-MP.OP-Crop products for industrial use-Nmix
    - AG.MM-MP.OP-Non-edible animal products-Nmix
    - PR.SO-MP.OP-Recycling-Nmix
    - EF.EC-MP.OP-Fuel used as feedstock-Nmix
    - FS.FO-MP.OP-Industrial round wood-Nmix
    - RW.RW-MP.OP-Other goods import -Nmix (excluding nitric acid and dicyandiamide – RW.RW-MP.OP-Other goods import -Nmix itself still reports the full total including them)
- Outgoing flows:
    - MP.OP-PR.SO-Other industry waste-Nmix
    - MP.OP-PR.WW-Other industry wastewater-Nmix
    - MP.OP-HY.SW-Untreated wastewater-Nmix (excluding the fertilizer plants listed above)
    - MP.OP-RW.RW-Other goods export-Nmix (excluding nitric acid, dicyandiamide and ammonia, for the same reason as the import flow above – MP.OP-RW.RW-Other goods export-Nmix itself still reports the full total including them)
    - MP.OP-EF.IC-Industrial waste fuels-Nmix
- The trade-based inflow and outflow (Other goods import/export) are adjusted to exclude nitric acid and dicyandiamide specifically: both are fertilizer-production intermediates (ammonium/calcium ammonium nitrate feedstock and a nitrification inhibitor, respectively) reported within the broader 'kjemikalier' (chemicals) trade category alongside genuine consumer-good inputs such as pharmaceuticals, polyamide and resin, which are kept. This distinction is about the fertilizer industry specifically, not industry in general: explosives, though also ammonium-nitrate-based, serve mining and civil engineering rather than fertilizer production and are deliberately left in the balance. A sharp rise in Norwegian nitric acid exports from 2018 onward, most plausibly linked to increased commercial nitric acid trade by domestic fertilizer producers, had been distorting the Consumer goods trend before this adjustment.

#### Interpretations and comparisons

- All errors in the inflows and outflows end up in this flow: a 10% error in Other goods import alone corresponds to about 2.4 kt N, or about 25% of the flow.
- The flow rises from about 4–6 kt N per year in 1990–1994 to about 9 kt N around 2000, 10–13.5 kt N in 2004–2011 (7.4 kt N in 2009) and 13–16.5 kt N in 2012–2022, and falls to 9–10 kt N in 2023–2024 (about 1.8 kg N per person).
- The low level in the early 1990s is mainly due to lower imports of other goods (13.5–20 kt N against 18–28 kt N from 1995).
- The drop in 2023–2024 comes mainly from lower recycling and higher imports of nitric acid, which are excluded from the balance.
- The 95% interval is wide (3–14 kt N in 2024, 0–7 kt N in 1990), since the flow is the difference between much larger flows. A negative difference is set to zero; this happens in about 27% of the Monte Carlo iterations in 1990, about 5% in 1991–1994 and 3% in 1997, and rarely in other years.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of conifer roundwood | Parameter | 0.0007–0.0017, triangular | 19% | 22% | 0.90 | 0.50 | [Industrial Round Wood](../forests_and_semi_natural_pool/flow_FS_FO_MP_OP_Industrial_round_wood_Nmix.html) |
| N content of hazardous waste | N content of waste | 0.0005–0.006 (min–max), triangular | 5% | 16% | −0.08 | −0.07 | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
| N content of traded goods: roundwood conifer | N content of traded goods | 0.0007–0.0017, triangular | <1% | 12% | 0.09 | −0.37 | [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html), [Other Goods Import](../rest_of_the_world_pool/flow_RW_RW_MP_OP_Other_goods_import__Nmix.html) |
| Waste accounts from 2012, industry (SSB 10514) | Modelled statistics | ±30 %, normal | – | 8% | – | −0.44 | [Food Industry Waste](../materials_and_products_pool/flow_MP_FP_PR_SO_Food_industry_waste_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html) |
| Waste treatment from 2012 (SSB 10513) (recycling) | Survey or self-reported data | ±20 %, normal, drawn per year | – | 8% | – | 0.63 | [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
| N content of wood waste fuels in industry | Parameter | 0.0019–0.0055, triangular | 13% | 5% | −0.67 | −0.21 | [Industrial Waste Fuels](../materials_and_products_pool/flow_MP_OP_EF_IC_Industrial_waste_fuels_Nmix.html) |
| Wood density of industrial roundwood | Parameter | 0.32–0.48, triangular | 4% | 5% | 0.94 | 0.52 | [Industrial Round Wood](../forests_and_semi_natural_pool/flow_FS_FO_MP_OP_Industrial_round_wood_Nmix.html) |
| N content of oil products used as feedstock | Parameter | 0–0.0025, lognormal | 1% | 4% | 0.03 | 0.02 | [Fuel used as feedstock](../energy_and_fuels_pool/flow_EF_EC_MP_OP_Fuel_used_as_feedstock_Nmix.html) |
| N content of traded goods: detergent | N content of traded goods | ±40 %, normal | 1% | 3% | 0.18 | 0.20 | [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html), [Other Goods Import](../rest_of_the_world_pool/flow_RW_RW_MP_OP_Other_goods_import__Nmix.html) |
| N content of other waste materials | N content of waste | ±50 %, lognormal | 1% | 3% | −0.16 | 0.19 | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
| N content of traded goods: wood products | N content of traded goods | 0.001–0.0049, triangular | 12% | 3% | −0.30 | 0.06 | [Other Goods Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Other_goods_export_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html), [Other Goods Import](../rest_of_the_world_pool/flow_RW_RW_MP_OP_Other_goods_import__Nmix.html) |
| N content of coal | Parameter | 0.005–0.025, triangular | 3% | 2% | 0.20 | 0.09 | [Fuel for industry](../energy_and_fuels_pool/flow_EF_EC_EF_IC_Fuel_for_industry_Nmix.html), [Fuel for heating](../energy_and_fuels_pool/flow_EF_EC_EF_OE_Fuel_for_heating_Nmix.html), [Fuel used as feedstock](../energy_and_fuels_pool/flow_EF_EC_MP_OP_Fuel_used_as_feedstock_Nmix.html) |
| Net calorific value of wood fuels | Parameter | 12.3–20.9, triangular | 4% | 1% | 0.61 | 0.19 | [Industrial Waste Fuels](../materials_and_products_pool/flow_MP_OP_EF_IC_Industrial_waste_fuels_Nmix.html) |
| N content of wood waste | N content of waste | 0.001–0.0049, triangular | 7% | <1% | −0.27 | 0.03 | [Household and Settlement Waste](../humans_and_settlements_pool/flow_HS_HS_PR_SO_Household_waste_Nmix.html), [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Biologically treated organic waste to Ag](../processing_of_residues_pool/flow_PR_SO_AG_SM_Biologically_treated_organic_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html) and 2 more |
| Waste accounts 1995–2011, industry (SSB 05282) | Modelled statistics | ±30 %, normal | 14% | – | −1.04 | – | [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
| Extrapolation (other industry waste:1995) | Gap filling: extrapolation | ±15–35 %, lognormal, grows with distance to known year | 6% | – | −0.97 | – | [Other Industry Waste](../materials_and_products_pool/flow_MP_OP_PR_SO_Other_industry_waste_Nmix.html), [Waste to energy (Incineration)](../processing_of_residues_pool/flow_PR_SO_EF_EC_Waste_to_energy_Nmix.html), [Material Recycling](../processing_of_residues_pool/flow_PR_SO_MP_OP_Recycling_Nmix.html) |
