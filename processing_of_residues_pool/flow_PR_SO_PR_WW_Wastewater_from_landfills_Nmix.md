---
layout: default
title: Wastewater from Landfills
parent: Solid Waste (PR.SO)
nav_order: 9
---

# Wastewater from Landfills

<iframe src="../output_files/plots/PR_SO_PR_WW_Wastewater_from_landfills_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**PR.SO-PR.WW-Wastewater from landfills-Nmix** is taken from Miljødirektoratet (2026)<!--cite:miljodirektoratet_norske_2026-->, emissions to water from landfills, where we have categorized landfills as being connected to municipal wastewater or not based on publicly available data. Where the categorization was not possible, the resulting emissions have been split evenly between the leaching and wastewater flows from landfills. Reported data only cover a single landfill in 2009-2010 and are not representative, so for years before 2011 we have extrapolated using the average value from 2011 onward. This probably underestimates the real value because landfilling was more prevalent in previous years.

**How the numbers are derived**

- Landfills with discharge permits report their annual emissions of total nitrogen to water to Miljødirektoratet, published in [Norske utslipp](https://www.norskeutslipp.no) (Utslipp_deponi.xlsx); the values are measured or calculated by the landfill operators.
- Each landfill is classified as connected or not connected to a municipal sewage network from publicly available information; where this was not possible, half of the emissions are assigned to each of PR.SO-HY.SW-Leaching-Nmix and PR.SO-PR.WW-Wastewater from landfills-Nmix.
- Reported data only cover a single landfill in 2009–2010, so 1990–2010 are the mean of 2011 onward scaled with methane from landfills in the national inventory (CRT Table 5, 5.A), which is calculated with a first-order decay model of the waste landfilled in earlier years and so follows the decomposition that also produces leachate. Methane from landfills fell from 82.5 kt in 1990 to 51.6 kt in 2010 and 28.6 kt in 2024.

**Interpretation**

- The flow is about 0.5–1.3 kt N per year since 2011.
- The extrapolated values fall from about 1.3 kt N in 1990 to 0.8 kt N in 2010, following the decline in landfill methane.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Miljødirektoratet (2026). *Norske Utslipp*. [norskeutslipp.no](norskeutslipp.no)
