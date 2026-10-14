---
layout: default
title: 1. Energy and fuels (EF)
nav_order: 2
has_children: true
---

# Pool: 1. Energy and fuels (EF)

This pool is divided into four operational sub-pools. Explore them using the side menu or links below:

* [Energy conversion (EF.EC)](subpool_energy_conversion.html)
* [Manufacturing industries and construction (EF.IC)](subpool_industry.html)
* [Transportation (EF.TR)](subpool_transport.html)
* [Other energy and fuels (EF.OE)](subpool_other_energy.html)


---

## Interactive Flow Diagram

Nitrogen flows into and out of EF and between its subpools. Use the slider or press **Play** to step through the years; the scale is the same for every year. Hover a flow to see the individual flows it contains, with their 95 % uncertainty intervals.

<iframe id="nnb-sankey" src="../output_files/plots/sankey_EF.html" width="100%" height="800" style="border:0;" scrolling="no"></iframe>
<script>window.addEventListener("message", function (e) { if (e.data && e.data.sankeyHeight) { document.getElementById("nnb-sankey").style.height = e.data.sankeyHeight + "px"; } });</script>

---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific streams, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_EF.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
In the guidelines, there are N2 flows assigned to and from EF sectors associated with nitrogen conversions in the combustion process. We have chosen to ignore these here because they can only be found by mass balance but by doing so, they may hide other imbalances that could be significant. They also do not make any significant contributions to the flows of reactive N. Note on subpools: it is not always clear where flows end up. For example, industrial waste fuels from MP.OP is assigned to manufacturing industries EC.IC, meaning that waste for fuel is kept within the industrial sector. This is not necessarily the case.

<!-- MANUAL:POOL_TEXT:END -->
