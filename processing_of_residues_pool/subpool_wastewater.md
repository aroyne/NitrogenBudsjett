---
layout: default
title: Wastewater (PR.WW)
parent: 5. Processing of residues (PR)
nav_order: 2
has_children: true
---

# Subpool: Wastewater (PR.WW)


---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific flows, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_PR_WW.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
We considered added a flow *PR.WW-PR.SO-Sewage sludge to biogas-Nmix* to account for sewage sludge used in biogas production. However, the digestate from these biogas plants is counted together with other sewage sludge when SSB reports end uses. In order to avoid double counting we have neglected this flow.

### Flows that are zero or neglected:

* **PR.WW-HY.SW-Treated wastewater discharge-Nmix** is neglected because we lack information on what wastewater treatment plants discharge their wastewater to SW or CW, and have therefore assigned the entire flow to CW. 
* **PR.WW-AT.AT-Emissions-NH3** and **PR.WW-AT.AT-Emissions-NOx** are reported as zero in the CLRTAP Inventory Submissions EMEP (2025)<!--cite:emep_officially_2025-->.
* **PR.WW-PR.SO-Sewage sludge incineration-Nmix** is sporadically reported in SSB table 05279, ranging between zero and a maximum of 4.5 % of the total amount of sewage sludge. Because the reporting is so sporadic and numbers are small we have chosen to ignore this flow. 
Note on sewage sludge: SSB table 05279 reports part of the sewage sludge as “other use” (Annen disponering) or “unknown use” (Ukjent disponering): 18–28% of the sludge in 2002–2006 (18–29 kt dry matter, about 0.6–0.9 kt N with 3% N) and 0–10% from 2007 (at most about 0.4 kt N). This sludge is not assigned to any flow. The PR.WW balance has more outflow than inflow in most years since 2012, so assigning it would increase this imbalance. 

### Flows added or changed compared with Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->:

* **PR.WW-HS.HS-Sewage sludge fertilizer-Nmix** is not in the guidelines, where sewage sludge goes only to agriculture (AG.SM) and to incineration (PR.SO). It has been added because SSB table 05279 reports sludge used on green areas and delivered to soil producers.
* **PR.WW-PR.SO-Sewage sludge landfill-Nmix** replaces **PR.WW-PR.SO-Sewage sludge incineration-Nmix** in the guidelines. In Norway, sewage sludge to PR.SO is landfilled or used as top cover on landfills; incineration is neglected (see above).

<!-- MANUAL:POOL_TEXT:END -->

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
