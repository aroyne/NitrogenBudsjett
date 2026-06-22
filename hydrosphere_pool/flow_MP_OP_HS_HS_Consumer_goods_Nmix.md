---
layout: default
title: Consumer Goods (Mass Balance)
parent: Other Producing Industry (MP.OP)
nav_order: 7
---

# Consumer Goods (Mass Balance)

![MP.OP-HS.HS-Consumer goods-Nmix](../output_files/plots/MP_OP_HS_HS_Consumer_goods_Nmix.png)

### Flow Description
**MP.OP-HS.HS-Consumer goods-Nmix** is calculated by mass balance, assuming that all incoming flows to OP that are not accounted for in outgoing flows end up in domestic consumer goods. We have excluded N2 fixation for ammonia synthesis, and mineral fertilizer flows. We also exclude emissions to air from the balance because they result mainly from fertilizer production.
\n**Incoming flows:**\n* AG.SM-MP.OP-Crop products for industrial use-Nmix
* AG.MM-MP.OP-Non-edible animal products-Nmix
* PR.SO-MP.OP-Recycling-Nmix
* EF.EC-MP.OP-Fuel used as feedstock-Nmix
* FS.FO-MP.OP-Industrial round wood-Nmix
* RW.RW-MP.OP-Other goods import -Nmix

**Outgoing flows:**
* MP.OP-PR.SO-Other industry waste-Nmix
* MP.OP-PR.WW-Other industry wastewater-Nmix
* MP.OP-HY.SW-Untreated wastewater-Nmix
* MP.OP-RW.RW-Other goods export-Nmix
* MP.OP-EF.IC-Industrial waste fuels-Nmix

For comparison, Moldan et al. (2025) found flows from MP to HS of 15.9 ktN in the form of wood products (produced – export – waste) and 52.2 ktN in the form of chemical products, also found by mass balance, and identified as “plastics, deicing agents, glue, paint, tensides, etc.”, giving a total of 68.1 ktN which, given that the Swedish population is larger than that of Norway, agrees well with our findings.

### References

* Moldan, F., Stadmark, J., Jutterström, S., & Ljunggren, J. (2025). Where does Sweden’s nitrogen go? Building a comprehensive national nitrogen budget. *Environmental Research Letters, 20*(12), 124068. [https://doi.org/10.1088/1748-9326/ae2697](https://doi.org/10.1088/1748-9326/ae2697)
