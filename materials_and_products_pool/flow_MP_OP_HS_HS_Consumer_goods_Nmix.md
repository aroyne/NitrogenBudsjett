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
- Negative residuals in individual MC iterations are set to zero.

#### Interpretations and comparisons

- All errors in the inflows and outflows end up in this flow: a 10% error in Other goods import alone corresponds to about 3 kt N, or about 20% of the flow.
- The flow rises from about 4–5 kt N per year in 1990–1994 to 8–11 kt N around 2000, 13–16 kt N in 2004–2011 and 17–20 kt N in 2012–2022, and falls to about 14 kt N in 2023–2024 (about 2.6 kg N per person).
- The low level in the early 1990s is mainly due to lower imports of other goods (15–22 kt N against 24–28 kt N from 1995).
- The drop in 2023–2024 comes mainly from lower recycling and higher imports of nitric acid, which are excluded from the balance.
- The 95% interval is wide (8–21 kt N in 2024), since the flow is the difference between much larger flows.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
