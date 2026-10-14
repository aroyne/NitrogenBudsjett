---
layout: default
title: 8. Hydrosphere (HY)
nav_order: 9
has_children: true
---

# Pool: 8. Hydrosphere (HY)

The hydrosphere ecosystem is split into three operational modules. Explore them below:

* [Surface Water (HY.SW)](subpool_surface_water.html)
* [Coastal Water (HY.CW)](subpool_coastal_water.html)
* [Aquaculture (HY.AC)](subpool_aquaculture.html)

---

## Interactive Flow Diagram

Nitrogen flows into and out of HY and between its subpools. Use the slider or press **Play** to step through the years; the scale is the same for every year. Hover a flow to see the individual flows it contains, with their 95 % uncertainty intervals.

<iframe id="nnb-sankey" src="../output_files/plots/sankey_HY.html" width="100%" height="800" style="border:0;" scrolling="no"></iframe>
<script>window.addEventListener("message", function (e) { if (e.data && e.data.sankeyHeight) { document.getElementById("nnb-sankey").style.height = e.data.sankeyHeight + "px"; } });</script>

---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific streams, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_HY.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
We have chosen to not include the pool groundwater (GW) because N concentrations and dynamics in Norway are largely unknown (Kværnø et al., 2024)<!--cite:kvaerno_agritil_2024-->.

<!-- MANUAL:POOL_TEXT:END -->

### References

* Kværnø, S. H., Fischer, F., & Bechmann, M. (2024). *AGRITIL - Nutrient loss model for agriculture Modelling soil, organic carbon, nitrogen and phosphorus losses from Norwegian agricultural areas to surface water*.
