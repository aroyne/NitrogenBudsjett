---
layout: default
title: Aquaculture (HY.AC)
parent: Hydrosphere (HY)
nav_order: 3
has_children: true
---

# Subpool: Aquaculture (HY.AC)


---

## Interactive Mass Balance Overview (1990-2023)

Hover over the chart to inspect specific streams, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_HY_AC.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

**Methodological note:** The conversion from feed N to fish production N (and the resulting waste feed and excretion, `HY.AC-HY.SW-Waste feed-Nmix` and `HY.AC-HY.SW-Excretia-Nmix`) uses a single, constant N-retention factor applied uniformly across the entire 1990–2023 period, rather than a value that varies by year. This does not capture the well-documented improvement in feed conversion efficiency in Norwegian aquaculture over this period, and may therefore misrepresent the feed input (and associated waste/excretion) implied by production figures in earlier vs. later years. This is a possible methodological weakness that should be followed up, e.g. by introducing a time-varying retention factor if suitable historical data can be found.

### Flows that are zero or neglected:

* **HY.AC-MP.FP-Freshwater fish and seafood-Nmix**, **HY.AC-HY.SW-Waste feed-Nmix** and **HY.AC-HY.SW-Excretia-Nmix** are set to zero...
* **HY.AC-AT.AT-Emissions-NH3** is set to zero assuming negligible ammonia emissions from these coastal marine cages.
