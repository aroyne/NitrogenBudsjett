---
layout: default
title: Ammonia Synthesis N2 Fixation
parent: 7. Atmosphere (AT)
nav_order: 15
---

# Ammonia Synthesis N2 Fixation

<iframe src="../output_files/plots/AT_AT_MP_OP_Ammonia_synthesis_N2_fixation_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
**AT.AT-MP.OP-Ammonia synthesis N2 fixation-N2**

is found through mass balance where we use data from FAOSTAT Fertilizer by nutrient, domestic fertilizer production, and adjusted for trade in ammonia using SSB trade data (table 08801): imported ammonia is subtracted (not domestically fixed) and exported ammonia is added back (domestically fixed before leaving the country). This combined value is smoothed with a centered 3-year moving average, since actual ammonia production is a continuous industrial process and presumably much steadier than the underlying trade statistics suggest on their own - annual trade figures are sensitive to shipment timing around year-end and to inventory/stock effects, which can otherwise dominate the apparent year-to-year change. The result is floored at zero, since a negative N2-fixation flow has no physical meaning. FAOSTAT Fertilizer by nutrient has not yet published a 2024 figure at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.