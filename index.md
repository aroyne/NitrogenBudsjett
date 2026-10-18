---
layout: default
title: Home
nav_order: 1
---

# Nitrogen Budget for Norway

**Last Updated:** October 18, 2026

{: .label .label-red }
Work in Progress

> **CRITICAL WARNING:** This project, including all underlying code, data parameterizations, and simulation results, is currently **under active development**. It is not yet validated or finalized. Using, copying, or relying on any part of this code or these results for research, decision-making, or any other application is **strongly discouraged** at this stage.

---

### Project Overview
Welcome to the interactive data and documentation portal for the Norwegian national nitrogen budget. This platform visualizes and centralizes the outputs from our Monte Carlo uncertainty analysis simulations.

Use the navigation menu on the left side to explore the individual nitrogen pools (e.g., Forests and Semi-natural Vegetation, Agriculture, Atmosphere, Hydrosphere, Rest of the World) and access detailed statistical time-series graphs, methodological explanations, and parameterizations for each specific flow.

<!-- MANUAL:INDEX_TEXT:START -->
### Central values and uncertainty intervals
- **Central value.** Every flow is first computed once with all parameters and data sets at their stated values. This deterministic run gives the central value (best estimate): the line in the time-series plots, the values in the balance plots and Sankey diagrams, and the value exported to the reporting template.
- **Uncertainty interval.** The uncertainty is estimated with a Monte Carlo analysis of 999 further runs. In each run, every uncertain parameter (N contents, conversion factors, shares) and an uncertainty factor for every data set are drawn once, from a fixed seed, and used for all years and all flows that use them. The shaded band is the 2.5–97.5 percentile range of these runs.
- **Distributions.** The bounds given for each parameter and data set are read as a 95 % interval. Symmetric bounds up to ±40 % use a normal distribution, wider or asymmetric bounds and minimum–maximum ranges from the literature use a triangular distribution, and uncertainty factors (for example −50/+100 % from the emission inventories) use a lognormal distribution.
- **Central value and band.** With skewed distributions the central value is not in the middle of the band. For a few flows whose best estimate lies at a bound (for example an N content of zero for petrol), the central value can lie at or just outside the edge of the band.
- **Balances.** Pool balances and their intervals are computed within each run, so flows that share parameters or are derived from each other keep their correlation.
- **Residual flows.** Flows computed as a difference of other flows (ammonia synthesis, inflow to coastal waters, consumer goods, recycling) are set to zero in the runs where the difference is negative; how often this happens is recorded.
- **Trends.** Since each data set's uncertainty factor is the same for all years within a run, most of the data uncertainty cancels out in trends over time.
<!-- MANUAL:INDEX_TEXT:END -->

### Interactive National Nitrogen Flow Map
The diagram below shows the nitrogen flows between the pools of the Norwegian nitrogen budget. Use the **slider** or press **Play** to step through the years; the scale is the same for every year, so the widths can be compared over time. Hover a flow to see the individual flows it contains, with their 95 % uncertainty intervals. The budget is dominated by fertilizer production and trade and by crude oil export; use **Hide fertilizer, ammonia & crude-oil trade** to see the smaller internal flows more clearly.

<iframe id="nnb-sankey" src="output_files/plots/global_nitrogen_sankey.html" width="100%" height="1000" style="border:0;" scrolling="no"></iframe>
<script>window.addEventListener("message", function (e) { if (e.data && e.data.sankeyHeight) { document.getElementById("nnb-sankey").style.height = e.data.sankeyHeight + "px"; } });</script>

---

For flows connected to the hydrosphere, and for land-relateds emissions and nitrogen deposition, we only consider the Norwegian mainland. For emissions to air reported through the UNFCCC framework we also include emissions from Norwegian economic activity on Svalbard (these are minor and mainly related to coal extraction, which has now been discontinued). We also include emissions and N flows that originate in petroleum extraction on the Norwegian continental shelf.
This NNB is built using the guidelines from (Winiwarter et al., 2025)<!--cite:winiwarter_inms_2025-->. Where flows are omitted or added to better fit the Norwegian nitrogen system, this is commented.

### References

* Winiwarter, W., Hayashi, K., Geupel, M., Gu, B., Zhang, X., Sutton, M. A., Schlegel, M., Baron, J., & van Grinsven, H. J. (2025). INMS Guidance Document on National Nitrogen Budgets. *UK Centre for Ecology & Hydrology*. [https://doi.org/10.5281/zenodo.15632929](https://doi.org/10.5281/zenodo.15632929)
