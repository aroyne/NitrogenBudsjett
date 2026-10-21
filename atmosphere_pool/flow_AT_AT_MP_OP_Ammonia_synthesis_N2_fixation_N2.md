---
layout: default
title: Ammonia Synthesis N2 Fixation
parent: 7. Atmosphere (AT)
nav_order: 15
---

# Ammonia Synthesis N2 Fixation

<iframe src="../output_files/plots/AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2** is N2 fixed from the air in industrial ammonia synthesis (Haber–Bosch) in Norway.

#### Data sources

- FAOSTAT Fertilizers by Nutrient: production, export, import and agricultural use of fertilizer N. FAOSTAT reports domestic production directly up to 2001; from 2002 onward FAOSTAT's production figure is imputed, and it is not consistent with FAOSTAT's own (revised) export figures for 2002–2020.
- Trade in ammonia from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)).

#### Assumptions

- The flow is found through mass balance: domestic fertilizer N production, minus imported ammonia (not domestically fixed), plus exported ammonia (domestically fixed before leaving the country).
- Domestic fertilizer N production is derived from the fertilizer balance of the MP.OP sub-pool in every year: export + agricultural use − import + non-agricultural use (MP.OP-HS.HS-Mineral fertilizer-Nmix, 2% of total use), so that all mineral fertilizer leaving MP.OP is accounted for by domestic production. Up to 2001 this matches FAOSTAT's reported production within 1%, except 1992 (13% lower than reported) and 1993 (9% lower).
- The combined value is smoothed with a centred 3-year moving average, since actual ammonia production is a continuous industrial process and presumably much steadier than the underlying trade statistics suggest on their own – annual trade figures are sensitive to shipment timing around year-end and to inventory/stock effects, which can otherwise dominate the apparent year-to-year change.
- The result is floored at zero, since a negative N2-fixation flow has no physical meaning. The central run is never negative; in the Monte Carlo simulation at most 2.5% of the iterations (in 1998) are set to zero.

#### Interpretations and comparisons

- The flow is about 130–410 kt N per year, by far the largest input of reactive N to Norway; it dips to 130–220 kt N in 1997–1999 and 230–280 kt N in 2005–2007, and has been 310–390 kt N since 2008.
- The fixed N leaves Norway mainly as exported mineral fertilizer (MP.OP-RW.RW-Mineral fertilizer export-Nmix, 430–790 kt N per year), which also contains N from imported ammonia.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-21.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| FAOSTAT fertilizers by nutrient (export) | Modelled statistics | ±30 %, normal | 92% | 97% | 1.37 | 2.09 | [Mineral Fertilizer Export](../materials_and_products_pool/flow_MP_OP_RW_RW_Mineral_fertilizer_export_Nmix.html) |
| FAOSTAT fertilizers by nutrient (use) | Modelled statistics | ±30 %, normal | 7% | 2% | 0.38 | 0.31 | [Mineral Fertilizer for Agriculture](../materials_and_products_pool/flow_MP_OP_AG_SM_Mineral_fertilizer_Nmix.html), [Mineral Fertilizer for HS](../materials_and_products_pool/flow_MP_OP_HS_HS_Mineral_fertilizer_Nmix.html) |
