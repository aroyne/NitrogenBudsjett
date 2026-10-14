---
layout: default
title: 6. Humans and settlements (HS)
nav_order: 7
has_children: true
---

# Pool: 6. Humans and settlements (HS)


---

## Interactive Flow Diagram

Nitrogen flows into and out of HS. Use the slider or press **Play** to step through the years; the scale is the same for every year. Hover a flow to see the individual flows it contains, with their 95 % uncertainty intervals.

<iframe id="nnb-sankey" src="../output_files/plots/sankey_HS.html" width="100%" height="800" style="border:0;" scrolling="no"></iframe>
<script>window.addEventListener("message", function (e) { if (e.data && e.data.sankeyHeight) { document.getElementById("nnb-sankey").style.height = e.data.sankeyHeight + "px"; } });</script>

---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific streams, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_HS.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
### Flows that are zero or neglected:

* **HS.HS-AT.AT-LUC emissions-NH3** is assumed negligible as no NH3 emissions are given in the CLRTAP inventory submissions.
* **HS.HS-AT.AT-LUC emissions-NOx** is set to zero because none is reported in UNFCCC Common reporting tables, Table 4.
* **HS.HS-HY.SW-Untreated wastewater-Nmix** and **HS.HS-HY.CW-Untreated wastewater-Nmix** are set to zero because wastewater treatment is mandated by law.
* **HS.HS-PR.SO-Organic waste biofuel substrate-Nmix** and **HS.HS-PR.SO-Organic waste for composting-Nmix** are not given as separate flows; instead they are included in the flow **HS.HS-PR.SO-Household waste-Nmix** because official statistics do not clearly indicate what origin waste flows end up in different end uses.
* **HS.HS-MP.OP-Recycling-Nmix** is not reported here because the flow of wastes from all origins to recycling is assigned to the PR.SO subpool to better reflect the Norwegian waste management and statistics structure.

<!-- MANUAL:POOL_TEXT:END -->
