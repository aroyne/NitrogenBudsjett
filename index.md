---
layout: default
title: Home
nav_order: 1
---

# Nitrogen Budget for Norway

**Last Updated:** November 09, 2026

{: .label .label-red }
Work in Progress

> **CRITICAL WARNING:** This project, including all underlying code, data parameterizations, and simulation results, is currently **under active development**. It is not yet validated or finalized. Using, copying, or relying on any part of this code or these results for research, decision-making, or any other application is **strongly discouraged** at this stage.

---

### Project Overview
Welcome to the interactive data and documentation portal for the Norwegian national nitrogen budget. This NNB follows the methodology described in the NNB guidelines of the International Nitrogen Management System (INMS) (Winiwarter et al., 2025)<!--cite:winiwarter_inms_2025--> and their detailed annexes (Schäppi et al., 2025)<!--cite:schappi_annexes_2025-->, including the division into pools and sub-pools and the naming of flows. Where flows are omitted or added to better fit the Norwegian nitrogen system, this is commented. The data come mainly from official statistics (Statistics Norway and other national agencies), Norway's emission inventories to the UNFCCC and CLRTAP and international databases such as FAOSTAT, combined with N contents and other parameters from the literature. This platform visualizes the results and associated uncertainties for each individual flow in the NNB, as well as the balances for each pool and sub-pool.

Use the navigation menu on the left side to explore the individual nitrogen pools and sub-pools and access detailed statistical time-series graphs, methodological explanations, and parameterizations for each specific flow.

<!-- MANUAL:INDEX_TEXT:START -->
### Data and uncertainties
All parameters used are assigned a most probable value, as well as an uncertainty distribution with an associated interval taken from literature where possible. The bounds are read as a 95 % interval, except minimum–maximum ranges from the literature (marked "min–max" in the uncertainty tables on the flow pages), which are read as the limits of a triangular distribution. Symmetric bounds up to ±40 % use a normal distribution, wider or asymmetric bounds a triangular distribution, and uncertainty factors (for example −50/+100 % from the emission inventories) a lognormal distribution.

Central value estimates for each flow and year are calculated using all parameters and data sets at their most probable value. These are the values shown as dark blue solid lines in the flow diagrams and as the values in the Sankey diagrams.

The uncertainty is estimated with a Monte Carlo analysis of 999 further runs from a fixed seed, where each uncertain parameter (N contents, conversion factors, etc.) is drawn once per run and used for all years and all flows that use it. Each data set gets an uncertainty factor that is drawn once per run (inventories, modelled statistics and assumptions) or anew for each year (registered data and surveys). The shaded band shown for each flow is the 2.5–97.5 percentile range of these runs.

Flows computed as a difference of other flows (ammonia synthesis, inflow to coastal waters, consumer goods, recycling) are set to zero in the runs where the difference is negative; how often this happens is recorded.

Each flow page lists the sources (parameters, data sets and gap filling) that account for at least 2 % of the uncertainty of the flow, measured as its variance, in 1990–1994 or 2020–2024. A source matters if it is itself uncertain and if the flow is sensitive to it. For a flow F and a source x<sub>i</sub>, the sensitivity is given as the elasticity e<sub>i</sub>, and the share of the variance as s<sub>i</sub>:

<p style="text-align:center">e<sub>i</sub> = (ΔF / F) / (Δx<sub>i</sub> / x<sub>i</sub>), &nbsp;&nbsp;&nbsp; s<sub>i</sub> = e<sub>i</sub><sup>2</sup> σ<sub>i</sub><sup>2</sup> / Σ<sub>j</sub> e<sub>j</sub><sup>2</sup> σ<sub>j</sub><sup>2</sup></p>

Here ΔF / F is the relative change in the flow when the source is increased by Δx<sub>i</sub> / x<sub>i</sub> = 10 %, σ<sub>i</sub> is the relative standard deviation of the source, and the sum is over all sources of the flow. The elasticity is negative if the flow decreases when the source increases. The share is computed for each year and averaged over the years of the period. This is a linear approximation, computed by changing one source at a time around the central run, and is less reliable when the flow is a small difference between larger flows (for example Consumer goods) or when a source has a very skewed distribution.
<!-- MANUAL:INDEX_TEXT:END -->

### Interactive National Nitrogen Flow Map
The diagram below shows the nitrogen flows between the pools of the Norwegian nitrogen budget. Use the **slider** or press **Play** to step through the years; the scale is the same for every year, so the widths can be compared over time. Hover a flow to see the individual flows it contains, with their 95 % uncertainty intervals. The budget is dominated by fertilizer production and trade and by crude oil export; use **Hide fertilizer, ammonia & crude-oil trade** to see the smaller internal flows more clearly.

<iframe id="nnb-sankey" src="output_files/plots/global_nitrogen_sankey.html" width="100%" height="1000" style="border:0;" scrolling="no"></iframe>
<script>window.addEventListener("message", function (e) { if (e.data && e.data.sankeyHeight) { document.getElementById("nnb-sankey").style.height = e.data.sankeyHeight + "px"; } });</script>

---

For land-related emissions and nitrogen deposition, we only consider the Norwegian mainland. For emissions to air reported through the UNFCCC framework we also include emissions from Norwegian economic activity on Svalbard (these are minor and mainly related to coal extraction, which has now been discontinued). We also include emissions and N flows that originate in petroleum extraction on the Norwegian continental shelf. For the hydrosphere pool, wild catch is an exception: the catch statistics cover all catch by Norwegian vessels, wherever it is taken. In 2018–2024, 58–74 % was taken in the Norwegian economic zone; the rest came from the zones of other countries, international waters in the North-East Atlantic and, at 8–14 %, Antarctic krill from the Southern Ocean. Coastal water (HY.CW) is therefore treated as a boundary node, like the rest of the world (RW) (see [Coastal Water (HY.CW)](hydrosphere_pool/subpool_coastal_water.html)).

### References

* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
* <span id="ref-winiwarter_inms_2025" data-cite="Winiwarter et al." data-year="2025"></span>Winiwarter, W., Hayashi, K., Geupel, M., Gu, B., Zhang, X., Sutton, M. A., Schlegel, M., Baron, J., & van Grinsven, H. J. (2025). *INMS Guidance Document on National Nitrogen Budgets*. UK Centre for Ecology & Hydrology. [https://doi.org/10.5281/zenodo.15632929](https://doi.org/10.5281/zenodo.15632929)
