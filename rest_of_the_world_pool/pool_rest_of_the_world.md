---
layout: default
title: Rest of the world (RW)
nav_order: 10
has_children: true
---

# Pool: Rest of the world (RW)

This section contains all documented nitrogen inflows and transfers originating from the Rest of the world (RW) pool. Click on the individual sub-flows in the left-hand menu to view graphs and methodological explanations.


---

## Interactive Flow Diagram

Nitrogen flows into and out of RW. Use the slider or press **Play** to step through the years; the scale is the same for every year. Hover a flow to see the individual flows it contains, with their 95 % uncertainty intervals.

<iframe id="nnb-sankey" src="../output_files/plots/sankey_RW.html" width="100%" height="800" style="border:0;" scrolling="no"></iframe>
<script>window.addEventListener("message", function (e) { if (e.data && e.data.sankeyHeight) { document.getElementById("nnb-sankey").style.height = e.data.sankeyHeight + "px"; } });</script>

---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific flows, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_RW.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
### Flows that are zero or neglected:

* **RW.RW-MP.FP-Sea fish (landings)-Nmix** is set to zero because all wild fish catch is accounted for as a flow from coastal water (HY.CW-MP.FP-Fish (wild catch)-Nmix). HY.CW is treated as a boundary node like RW; see the page for [Coastal Water (HY.CW)](../hydrosphere_pool/subpool_coastal_water.html).
* **RW.RW-AG.SM-Manure import-Nmix** is neglected. Manure is bulky and is normally used close to where it is produced. The only trade in it is animal or vegetable fertilizer (HS 3101, mostly processed products such as pelleted manure) in [SSB table 08801](https://www.ssb.no/statbank/table/08801): 3–5 kt of product imported per year (14 kt in 2000) and up to 12 kt exported, about 0.1–0.4 kt N with 2–4% N.
* **RW.RW-HY.SW-Import of surface water-Nmix** are assumed negligible due to Norwegian topography.

<!-- MANUAL:POOL_TEXT:END -->
