---
layout: default
title: Solid Waste (PR.SO)
parent: Processing of residues (PR)
nav_order: 1
has_children: true
---

# Subpool: Solid Waste (PR.SO)


---

## Mass Balance Overview (1990-2023)

The chart below illustrates the integrated nitrogen mass balance for **PR.SO**. It includes total system inflows (positive stack), total outflows (negative stack), and the net balance line with estimated uncertainty bounds (±1σ).

![Mass Balance PR.SO](../output_files/plots/balance_PR_SO.png)
We have added the flow *PR.SO-EF.EC-Waste to energy-Nmix* to better account for the Norwegian waste management system and statistics. This accounts for all waste incineration. Although the SSB data does separate between incineration with and without energy recovery for use, the fraction for energy reuse has consistently been around or above 80% since 1995, and we therefore for simplicity assign the entire waste incineration process to the EF.EC sector.

 It is expected that there should be a surplus for all years because landfilled waste stays in the PR sector and thus does not represent an outflow. The fraction of waste to landfill has been decreasing. 
### Flows that are zero or neglected:

* **PR.SO-EF.IC-Biofuels-Nmix**, **PR.SO-EF.TR-Biofuels-Nmix** and **PR.SO-EF.OE-Biofuels-Nmix** are neglected because diesel and biogas contain very little nitrogen. We assume the N in waste to be processed is lost as emissions or retained in digestates from the biofuel production process. 
* The guidelines recommends assigning separate flows for compost and biofuel digestate used on the AG and HS pools. However, the SSB statistics for treatment and use of organic waste does not separate between different treatment methods when it comes to end use. We have therefore decided to combine these flows to one called “biologically treated waste” to agriculture, and one to HS. 