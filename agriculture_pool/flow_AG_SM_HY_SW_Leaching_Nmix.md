---
layout: default
title: Leaching from soil management
parent: Soil Management (AG.SM)
nav_order: 6
---

# Leaching from soil management

<iframe src="../output_files/plots/AG_SM_HY_SW_Leaching_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.SM-HY.SW-Leaching-Nmix** is N leached and lost in runoff from agricultural soils.

#### Data sources

- "3.D.2.b. Nitrogen leaching and run-off" in the UNFCCC Common Reporting Tables (CRT), Table 3.D, of the national greenhouse gas inventory ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)): the N applied to agricultural soils (mineral fertilizer, manure, sewage sludge, grazing animals, crop residues and mineralisation) multiplied by the fraction lost through leaching and runoff (FracLEACH).
- Norway uses a country-specific FracLEACH of 22%, derived by Bioforsk in 2011 from the agricultural catchments in the national monitoring programme JOVA; the fraction ranged from 16% on grassland to 44% in intensive vegetable, potato and cereal production ([Bioforsk, 2011](https://partner.sciencenorway.no/agriculture-agriculture--fisheries-bioforsk/updated-estimate-for-nitrogen-losses-in-agriculture/1377328)).
- The inventory counts all manure deposited by grazing animals as input to managed soils, including the share deposited on utmark (unmanaged land), which this model does not count as input to AG.SM (see AG.MM-AG.SM-Manure application-Nmix).

#### Assumptions

- The utmark share (47%, range 38–56%) of the losses from grazing manure is therefore removed from this flow; these losses are part of the runoff from upland areas measured by TEOTIL3 (FS.OL).
- The removed leaching is FracLEACH (from CRT Table 3.D) times the utmark share of the grazing manure, about 2.5 kt N per year.

#### Interpretations and comparisons

- The flow is 37–44 kt N per year and follows the N applied to soils, falling slowly from about 44 kt N in 1990 to 39 kt N in 2024.
- The flow is the N leaving the root zone, not the N reaching the sea; TEOTIL3 gives 43–51 kt N from agriculture including the agricultural background in 2013–2023, before retention in lakes and rivers. The data agree within the error range with what is reported in TEOTIL3 (Sample, 2024<!--cite:sample_kildefordelte_2024-->).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Sample, J. E. (2024). *Kildefordelte tilførsler av nitrogen og fosfor til norske kystområder i 2022 – tabeller, figurer og kart*.
