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
- Domestic fertilizer N production is FAOSTAT's reported production up to 2001. From 2002 it is derived from the fertilizer balance of the MP.OP sub-pool: export + agricultural use − import + non-agricultural use (MP.OP-HS.HS-Mineral fertilizer-Nmix, 2% of total use), so that all mineral fertilizer leaving MP.OP is accounted for by domestic production.
- The combined value is smoothed with a centred 3-year moving average, since actual ammonia production is a continuous industrial process and presumably much steadier than the underlying trade statistics suggest on their own – annual trade figures are sensitive to shipment timing around year-end and to inventory/stock effects, which can otherwise dominate the apparent year-to-year change.
- The result is floored at zero, since a negative N2-fixation flow has no physical meaning.

#### Interpretations and comparisons

- The flow is about 220–370 kt N per year, by far the largest input of reactive N to Norway; it falls to about 220–240 kt N in the late 1990s and early 2000s and has been 320–370 kt N since 2010.
- The fixed N leaves Norway mainly as exported mineral fertilizer (MP.OP-RW.RW-Mineral fertilizer export-Nmix, 430–790 kt N per year), which also contains N from imported ammonia.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
