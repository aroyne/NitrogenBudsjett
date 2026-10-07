---
layout: default
title: Excretia
parent: Aquaculture (HY.AC)
nav_order: 1
---

# Excretia

<iframe src="../output_files/plots/HY_AC_HY_CW_Excretia_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HY.AC-HY.CW-Excretia-Nmix** is the N excreted by farmed fish to coastal water: the eaten feed N that is not retained in the fish.
- N in dead and discarded fish taken out of the sea is subtracted from excretion and counted in **HY.AC-MP.FP-Coastal fish and seafood-Nmix** instead.

#### Data sources

- Sold farmed salmon and trout by year from Fiskeridirektoratet (2025)<!--cite:fiskeridirektoratet_06002_2025--> (table A.06.002, 1994 onward; historical compilation for 1984–1993).

#### Assumptions

- Harvested fish are multiplied by 2.8% N (Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, p. 254).
- Feed N is the harvested N divided by an apparent whole-system retention that rises linearly from 26% in 1990 (Ytrestøyl et al., 2015<!--cite:ytrestoyl_utilisation_2015-->) to 35.75% in 2010 (Aas et al., 2022<!--cite:aas_utilization_2022-->) and is constant after. The rise is attributed to less feed waste, so the biological retention of eaten feed is held constant and the feed waste falls from about 29% of the feed in 1990 to the measured 3% (Wang et al., 2013<!--cite:wang_chemical_2013-->) in 2010; see the [methodological note](subpool_aquaculture.html) on the Aquaculture (HY.AC) subpool page.
- Found through mass balance by assuming N that does not become fish or waste feed is excreted, using the same time-varying biological retention as the other aquafeed-budget flows (see the [methodological note](subpool_aquaculture.html) for details and sources).

#### Interpretations and comparisons

- The flow rises from about 1.5 kt N in 1984 to 77 kt N in 2024, following production, and is the largest N input to Norwegian coastal waters from a single source after the inflow from land.
- Our combined losses from aquaculture to coastal waters (excretion plus waste feed) are 6–18% higher than TEOTIL3 (Sample et al., 2024)<!--cite:sample_teotil3_2024--> for 2013–2023, and considerably higher than Miljødirektoratet's earlier estimates before 2005.
- The total feed N in our budget agrees with reported feed sales (Sjømat Norge, via Fiskeridirektoratet's key figures) to within 2% for 2019–2023, so the difference lies in how much of the feed N is assumed retained in the fish. We use the whole-system apparent retention of 35.75% from Aas et al. (2022)<!--cite:aas_utilization_2022-->, which counts all losses of feed ingredients, feed and fish as unretained, and a lower retention further back in time (Ytrestøyl et al., 2015)<!--cite:ytrestoyl_utilisation_2015-->. TEOTIL3 instead calculates losses as N in reported feed (5.84% N) minus N in the biomass growth of the farmed fish (2.96% N), including fish that are later lost, which implies a retention of about 44%, close to the 45% protein retention for 2012 reported by Torrissen et al. (2016)<!--cite:torrisen_naeringsutslipp_2016-->.
- Our estimate should therefore be seen as an upper bound for the losses to coastal water.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Aas, T. S., Åsgård, T., & Ytrestøyl, T. (2022). Utilization of feed resources in the production of Atlantic salmon (Salmo salar) in Norway: An update for 2020. *Aquaculture Reports, 26*, 101316. [https://doi.org/10.1016/j.aqrep.2022.101316](https://doi.org/10.1016/j.aqrep.2022.101316)
* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
* Torrissen, O., Hansen, P. K., Aure, J., Husa, V., Andersen, S., Strohmeier, T., & Olsen, R. E. (2016). *Næringsutslipp fra havbruk - nasjonale og regionale perspektiv*. [https://www.hi.no/resources/publikasjoner/rapport-fra-havforskningen/2016/21-2016_neringsutslipp_fra_havbruk_ot.pdf](https://www.hi.no/resources/publikasjoner/rapport-fra-havforskningen/2016/21-2016_neringsutslipp_fra_havbruk_ot.pdf)
* Ytrestøyl, T., Aas, T. S., & Åsgård, T. (2015). Utilisation of feed resources in production of Atlantic salmon (Salmo salar) in Norway. *Aquaculture, 448*, 365-374. [https://doi.org/10.1016/j.aquaculture.2015.06.023](https://doi.org/10.1016/j.aquaculture.2015.06.023)
