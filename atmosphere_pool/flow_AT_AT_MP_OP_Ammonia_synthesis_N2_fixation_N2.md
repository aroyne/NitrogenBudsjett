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
**AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2**

is found through mass balance where we use domestic fertilizer N production, adjusted for trade in ammonia using SSB trade data (table 08801): imported ammonia is subtracted (not domestically fixed) and exported ammonia is added back (domestically fixed before leaving the country). Domestic fertilizer N production is taken from FAOSTAT Fertilizer by nutrient for the years where FAOSTAT reports it directly (up to 2001). From 2002 onward FAOSTAT's production figure is imputed, and it is not consistent with FAOSTAT's own (revised) export figures for 2002-2020. For these years we instead derive production from the fertilizer balance of the MP.OP sub-pool: export + agricultural use − import + non-agricultural use (**MP.OP-HS.HS-Mineral fertilizer-Nmix**), all taken from FAOSTAT Fertilizer by nutrient, so that all mineral fertilizer leaving MP.OP is accounted for by domestic production. This combined value is smoothed with a centered 3-year moving average, since actual ammonia production is a continuous industrial process and presumably much steadier than the underlying trade statistics suggest on their own - annual trade figures are sensitive to shipment timing around year-end and to inventory/stock effects, which can otherwise dominate the apparent year-to-year change. The result is floored at zero, since a negative N2-fixation flow has no physical meaning.

**How the numbers are derived**

- Up to 2001 the domestic production of N fertilizer is taken from FAOSTAT Fertilizers by Nutrient; from 2002 FAOSTAT's production is imputed, and production is instead export + agricultural use − import + non-agricultural use (2% of total use).
- Imported ammonia is subtracted and exported ammonia added, from SSB's external trade statistics ([table 08801](https://www.ssb.no/statbank/table/08801)).
- The result is smoothed with a centred 3-year moving average and floored at zero.

**Interpretation**

- The flow is about 220–370 kt N per year, by far the largest input of reactive N to Norway; it falls to about 220–240 kt N in the late 1990s and early 2000s and has been 320–370 kt N since 2010.
- The fixed N leaves Norway mainly as exported mineral fertilizer (MP.OP-RW.RW-Mineral fertilizer export-Nmix, 430–790 kt N per year), which also contains N from imported ammonia.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
