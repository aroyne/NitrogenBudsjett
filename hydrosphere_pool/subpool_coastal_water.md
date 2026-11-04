---
layout: default
title: Coastal Water (HY.CW)
parent: 8. Hydrosphere (HY)
nav_order: 2
has_children: true
---

# Subpool: Coastal water (HY.CW)


---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific flows, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_HY_CW.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
HY.CW is treated as an open boundary node, in practice as a category of the rest of the world (RW). We lack a clear definition of the boundary between coastal water and the open sea, and we have no data on deposition to, denitrification in or exchange across the boundary of such an area that could be used here. The subpool can therefore not be balanced, and its balance should not be interpreted. The node is kept separate from RW to distinguish N that goes to or comes from the sea (runoff, wastewater, aquaculture, wild catch) from trade with other countries.

The wild catch comes from large sea areas, not only from Norwegian coastal waters. The official catch statistics cover all catch by Norwegian vessels, landed in Norway or abroad ([Fiskeridirektoratet, Om dataene – fangst](https://www.fiskeridir.no/statistikk-tall-og-analyse/data-og-statistikk-om-yrkesfiske/fangst/om-dataene--fangst-offisiell-statistikk)). In 2018–2024, 58–74% of this catch was taken in the Norwegian economic zone; the rest came from the EU, UK, Icelandic and Faroese zones, the Svalbard fisheries protection zone, international waters in the North-East Atlantic and, at 8–14%, Antarctic krill from the Southern Ocean (Fiskeridirektoratet statistics bank, table F.06.003b). Of the catch, 12–20% is landed abroad, including all the krill (landed in Uruguay; table F.06.002). The largest species groups are herring, blue whiting, mackerel, cod and saithe (see [Fish (wild catch)](flow_HY_CW_MP_FP_Fish_(wild_catch)_Nmix.html) and [Shellfish](flow_HY_CW_MP_FP_Shellfish_Nmix.html)).

### Flows that are zero or neglected:

* **HY.CW-AT.AT-Emissions-N2** is neglected as we do not use mass balance on this subpool.
* **HY.CW-AT.AT-Emissions-N2O** and **HY.CW-AT.AT-Emissions-NOx** are neglected as we lack a clearly defined area for coastal waters.
* **HY.CW-PR.SO-Biomass for energy production-Nmix** is neglected because organic material from the processing of caught or farmed fish is assigned to the MP.FS subpool...
* **Recreational fishing** is not included in the official guidelines, and we have also chosen to neglect it here...

### Flows added or changed compared with Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->:

* **HY.CW-MP.FP-Fish (wild catch)-Nmix**: In the guidelines, wild catch (HY.SW-MP.FP) is fish from freshwater fishery, and landings from marine fishery are a flow from the rest of the world, **RW.RW-MP.FP-Sea fish (landings)-Nmix** (note to Table 65 in Schäppi et al., 2025). We assign the marine catch to HY.CW instead, since HY.CW is treated as a boundary node (see above). This does not change the balance of the economy as a whole, since both HY.CW and RW are boundary nodes, but it keeps catch from the sea separate from imported food.
* **HY.CW-MP.FP-Shellfish-Nmix** is shellfish from aquaculture in the guidelines. Our flow contains wild-caught crustaceans (including Antarctic krill) and harvested seaweed.

<!-- MANUAL:POOL_TEXT:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
