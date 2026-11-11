---
layout: default
title: 1. Energy and fuels (EF)
nav_order: 2
has_children: true
---

# Pool: 1. Energy and fuels (EF)

This pool is divided into four sub-pools. Explore them using the side menu or links below:

* [Energy conversion (EF.EC)](subpool_energy_conversion.html)
* [Manufacturing industries and construction (EF.IC)](subpool_industry.html)
* [Transportation (EF.TR)](subpool_transport.html)
* [Other energy and fuels (EF.OE)](subpool_other_energy.html)


---

## Interactive Flow Diagram

Nitrogen flows into and out of EF and between its sub-pools. Use the slider or press **Play** to step through the years; the scale is the same for every year. Hover a flow to see the individual flows it contains, with their 95 % uncertainty intervals.

<iframe id="nnb-sankey" src="../output_files/plots/sankey_EF.html" width="100%" height="800" style="border:0;" scrolling="no"></iframe>
<script>window.addEventListener("message", function (e) { if (e.data && e.data.sankeyHeight) { document.getElementById("nnb-sankey").style.height = e.data.sankeyHeight + "px"; } });</script>

---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific flows, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_EF.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
In the guidelines, there are N<sub>2</sub> flows assigned to and from the EF sectors associated with nitrogen conversions in combustion processes. We have chosen to ignore these here because they can only be found by mass balance, and by doing so, they may hide other imbalances that could be significant.

<!-- MANUAL:POOL_TEXT:END -->
