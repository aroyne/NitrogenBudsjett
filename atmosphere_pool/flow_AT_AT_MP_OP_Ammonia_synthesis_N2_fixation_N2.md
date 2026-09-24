---
layout: default
title: Ammonia Synthesis N2 Fixation
parent: 7. Atmosphere (AT)
nav_order: 15
---

# Ammonia Synthesis N2 Fixation

<iframe src="../output_files/plots/AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2**

is found through mass balance where we use domestic fertilizer N production, adjusted for trade in ammonia using SSB trade data (table 08801): imported ammonia is subtracted (not domestically fixed) and exported ammonia is added back (domestically fixed before leaving the country). Domestic fertilizer N production is taken from FAOSTAT Fertilizer by nutrient for the years where FAOSTAT reports it directly (up to 2001). From 2002 onward FAOSTAT's production figure is imputed, and it is not consistent with FAOSTAT's own (revised) export figures for 2002-2020. For these years we instead derive production from the fertilizer balance of the MP.OP sub-pool: export + agricultural use − import + non-agricultural use (**MP.OP-HS.HS-Mineral fertilizer-Nmix**), all taken from FAOSTAT Fertilizer by nutrient, so that all mineral fertilizer leaving MP.OP is accounted for by domestic production. This combined value is smoothed with a centered 3-year moving average, since actual ammonia production is a continuous industrial process and presumably much steadier than the underlying trade statistics suggest on their own - annual trade figures are sensitive to shipment timing around year-end and to inventory/stock effects, which can otherwise dominate the apparent year-to-year change. The result is floored at zero, since a negative N2-fixation flow has no physical meaning.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
