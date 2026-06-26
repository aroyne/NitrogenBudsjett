---
layout: default
title: Home
nav_order: 1
---

# Nitrogen Budget for Norway

**Last Updated:** June 25, 2026

{: .label .label-red }
Work in Progress

> **CRITICAL WARNING:** This project, including all underlying code, data parameterizations, and simulation results, is currently **under active development**. It is not yet validated or finalized. Using, copying, or relying on any part of this code or these results for research, decision-making, or any other application is **strongly discouraged** at this stage.

---

### Project Overview
Welcome to the interactive data and documentation portal for the Norwegian national nitrogen budget. This platform visualizes and centralizes the outputs from our Monte Carlo uncertainty analysis simulations.

Use the navigation menu on the left side to explore the individual nitrogen pools (e.g., Forests and Semi-natural Vegetation, Agriculture, Atmosphere, Hydrosphere, Rest of the World) and access detailed statistical time-series graphs, methodological explanations, and parameterizations for each specific flow.

### Interactive National Nitrogen Flow Map
The diagram below illustrates the integrated nitrogen economy of Norway. Use the **slider at the bottom** or press **Play** to explore how the flow magnitudes have evolved over time. Flows are color-coded by chemical/functional type (e.g., gray for inert N₂, red for NOx, orange for NH₃/RDN, green for Nmix).

> 💡 **Tip:** The national budget is highly dominated by fertilizer production and trade. If you want to study the smaller, internal environmental and agricultural cycles more closely, you can view the **[Sankey Map with Fertilizer Trade Hidden](output_files/plots/global_nitrogen_sankey_no_fertilizer.html)**.

<iframe src="output_files/plots/global_nitrogen_sankey.html" width="100%" height="800px" frameborder="0" scrolling="no"></iframe>

---

For flows connected to the hydrosphere, and for land-relateds emissions and nitrogen deposition, we only consider the Norwegian mainland. For emissions to air reported through the UNFCCC framework we also include emissions from Norwegian economic activity on Svalbard (these are minor and mainly related to coal extraction, which has now been discontinued). We also include emissions and N flows that originate in petroleum extraction on the Norwegian continental shelf.
This NNB is built using the guidelines from (Winiwarter et al., 2025). Where flows are omitted or added to better fit the Norwegian nitrogen system, this is commented.

### References

* Winiwarter, W., Hayashi, K., Geupel, M., Gu, B., Zhang, X., Sutton, M. A., Schlegel, M., Baron, J., & van Grinsven, H. J. (2025). INMS Guidance Document on National Nitrogen Budgets. *UK Centre for Ecology & Hydrology*. [https://doi.org/10.5281/zenodo.15632929](https://doi.org/10.5281/zenodo.15632929)
