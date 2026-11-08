---
layout: default
title: Solid Waste (PR.SO)
parent: 5. Processing of residues (PR)
nav_order: 1
has_children: true
---

# Subpool: Solid Waste (PR.SO)


---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific flows, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_PR_SO.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
It is expected that there should be a surplus for all years because landfilled waste stays in the PR sector and thus does not represent an outflow. The fraction of waste to landfill has been decreasing. Up to 2008 about 2 million tonnes of waste were landfilled each year (SSB table 05281), and the outflows were about 50–65% of the inflows. From 1 July 2009 landfilling of biodegradable waste was banned ([Avfallsforskriften § 9-4](https://lovdata.no/dokument/SF/forskrift/2004-06-01-930/%C2%A79-4), amended by regulation of 27 June 2008 no. 741). Landfilled waste fell to 0.8 million tonnes in 2011 (SSB table 05281; see also SSB, 2011b<!--cite:ssb_avfallsregnskap_2011-->), more waste went to incineration, and from 2012 the outflows are about 90–100% of the inflows.

### Flows that are zero or neglected:

* **PR.SO-EF.IC-Biofuels-Nmix**, **PR.SO-EF.TR-Biofuels-Nmix** and **PR.SO-EF.OE-Biofuels-Nmix** are neglected because diesel and biogas contain very little nitrogen. We assume the N in waste to be processed is lost as emissions or retained in digestates from the biofuel production process. 
* The guidelines recommends assigning separate flows for compost and biofuel digestate used on the AG and HS pools. However, the SSB statistics for treatment and use of organic waste does not separate between different treatment methods when it comes to end use. We have therefore decided to combine these flows to one called “biologically treated waste” to agriculture, and one to HS. 

### Flows added or changed compared with Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->:

* **PR.SO-EF.EC-Waste to energy-Nmix** is not in the guidelines, where waste incineration belongs to PR.SO (see above).
* **PR.SO-MP.OP-Recycling-Nmix** is a flow from HS (HS.HS-MP.OP) in the guidelines. We let all waste to recycling go from PR.SO, since the SSB waste statistics report recycling for waste of all origins together.
* **PR.SO-RW.RW-Export for recycling-Nmix** and **PR.SO-RW.RW-Export for reuse-Nmix** are not in the guidelines, which only have **PR.SO-RW.RW-Solid waste export-Nmix**. We keep waste exported for recycling and used textiles exported for reuse as separate flows.
* **PR.SO-HY.SW-Leaching-Nmix** goes to groundwater (HY.GW) in Schäppi et al. (2025). We do not include the groundwater subpool (see the [hydrosphere pool page](../hydrosphere_pool/pool_hydrosphere.html)), so the flow goes to surface water (HY.SW).

<!-- MANUAL:POOL_TEXT:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
* SSB (2011b). *Avfallsregnskapet: Store endringer i deponert avfall*. [ssb.no](https://www.ssb.no/natur-og-miljo/statistikker/avfregno/aar/2011-12-14)
