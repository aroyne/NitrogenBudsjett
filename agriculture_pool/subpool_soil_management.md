---
layout: default
title: Soil Management (AG.SM)
parent: Agriculture (AG)
nav_order: 2
has_children: true
---

# Subpool: Soil management (AG.SM)


---

## Interactive Mass Balance Overview (1990-2023)

Hover over the chart to inspect specific streams, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_AG_SM.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

### Flows that are zero or neglected:

* **AG.SM-HY.SW-Overland flow-Nmix**, **AG.SM-FS.OL-Overland flow-Nmix** and **AG.SM-FS.WL-Overland flow-Nmix** are neglected as suggested by Schäppi et al. (2025): «In a first approximation it can be assumed that N losses to hydrosphere or forests and semi-natural vegetation occur mainly via leaching. If no country specific data is available on fractions for overland flow of N, the overland flows can be neglected for simplification purposes». is not included because all runoff and leaching is included in Leaching.
* **AG.SM-PR.SO-Farm crops substrate-Nmix** is farm crops substrate for biofuels production and composting. According to data in SSB table 12359 «Biologisk behandling av avfall, etter materialtype (1 000 tonn) 2017 – 2023» for category «Landbruksavfall, etande”, these values are small enough to be neglected. Since we only have values given for a few years, we have chosen to neglect this flow.
* **AG.SM-HY.SW-Overland flow-Nmix** is not included because all runoff and leaching is included in  **AG.SM-HY.SW-Leaching-Nmix**.

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
