---
layout: default
title: Manure Management (AG.MM)
parent: 3. Agriculture (AG)
nav_order: 1
has_children: true
---

# Subpool: Manure management, storage and animal husbandry (AG.MM)


---

## Interactive Mass Balance Overview (1990-2024)

Hover over the chart to inspect specific flows, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_AG_MM.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

<!-- MANUAL:POOL_TEXT:START -->
### Flows that are zero or neglected:

* **AG.MM-RW.RW-Manure export-Nmix** is neglected. The export of animal and vegetable fertilizers (HS 3101, which also includes processed and plant-based products; SSB table 08801) is 0.01–0.16 kt N per year up to 2019 and 0.22–0.35 kt N per year in 2020–2024, assuming 3 % N (2–4 % in dried manure products). This is small enough to be left out, and HS 3101 is not included in any other flow (the same applies to imports, see RW.RW-AG.SM-Manure import-Nmix on the [Rest of the World](../rest_of_the_world_pool/pool_rest_of_the_world.html) page).


* **AG.MM-PR.SO-Manure for biofuel production-Nmix** is neglected because the Eurostat data used to calculate manure application to soil includes manure that has been processed for biogas. SSB table 12359 gives the amount of manure processed for biogas or through composting. Composting values are negligible compared with biogas.  The nitrogen content of manure for biogas production is found to rise from zero before 2012 to around 0.5 kt/year in 2023 (data from Landbruksdirektoratet (2025)<!--cite:landbruksdirektoratet_biogass_2025-->, a value which is still negligible compared with the total amount of manure application. We therefore do not introduce a correction for the amount of nitrogen lost through biogas processing.  

### Flows added or changed compared with Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->:

* **AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix** is not in the guidelines. It has been added because a large part of the grazing in Norway takes place on unmanaged land (utmark), which belongs to FS.OL and not to agricultural soils (AG.SM). See the page for [Other land (FS.OL)](../forests_and_semi_natural_pool/subpool_other_land.html).
* **AG.MM-HY.SW-Leaching-Nmix** goes to groundwater (HY.GW) in Schäppi et al. (2025). We do not include the groundwater subpool (see the [hydrosphere pool page](../hydrosphere_pool/pool_hydrosphere.html)), so the flow goes to surface water (HY.SW).

### Break in the fodder statistics in 2021:

* The surplus in the AG.MM balance increases from 2021 because SSB changed the method for the grass harvest (eng til slått) that year; the fodder crops flow rises by about 27% from 2020 to 2021 while the feed the animals must have eaten does not change. The balance before and after 2021 should therefore not be compared directly. See [Fodder crops](../agriculture_pool/flow_AG_SM_AG_MM_Fodder_crops_Nmix.html).

<!-- MANUAL:POOL_TEXT:END -->

### References

* <span id="ref-landbruksdirektoratet_biogass_2025" data-cite="Landbruksdirektoratet" data-year="2025"></span>Landbruksdirektoratet (2025). *Biogass*. [landbruksdirektoratet.no](https://www.landbruksdirektoratet.no/nb/statistikk-og-utviklingstrekk/statistikk-over-miljotilskudd-i-jordbruket/biogass)
* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
