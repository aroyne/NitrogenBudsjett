---
layout: default
title: Excretia
parent: Aquaculture (HY.AC)
nav_order: 1
---

# Excretia

<iframe src="../output_files/plots/HY_AC_HY_CW_Excretia_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Found through mass balance by assuming N that does not become fish or waste feed is excreted, using the same time-varying biological retention as the other aquafeed-budget flows (see the [methodological note](subpool_aquaculture.html) on the Aquaculture (HY.AC) subpool page for details and sources). N in dead and discarded fish taken out of the sea is subtracted from excretion and counted in **HY.AC-MP.FP-Coastal fish and seafood-Nmix** instead.

Our combined losses from aquaculture to coastal waters (excretion plus waste feed) are 6-18 % higher than TEOTIL3 (Sample et al., 2024)<!--cite:sample_teotil3_2024--> for 2013-2023, and considerably higher than Miljødirektoratet's earlier estimates before 2005. The total feed N in our budget agrees with reported feed sales (Sjømat Norge, via Fiskeridirektoratet's key figures) to within 2 % for 2019-2023, so the difference lies in how much of the feed N is assumed retained in the fish. We use the whole-system apparent retention of 35.75 % from Aas et al. (2022)<!--cite:aas_utilization_2022-->, which counts all losses of feed ingredients, feed and fish as unretained, and a lower retention further back in time (Ytrestøyl et al., 2015)<!--cite:ytrestoyl_utilisation_2015-->. TEOTIL3 instead calculates losses as N in reported feed (5.84 % N) minus N in the biomass growth of the farmed fish (2.96 % N), including fish that are later lost, which implies a retention of about 44 %, close to the 45 % protein retention for 2012 reported by Torrissen et al. (2016)<!--cite:torrisen_naeringsutslipp_2016-->. Our estimate should therefore be seen as an upper bound for the losses to coastal water.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Aas, T. S., Åsgård, T., & Ytrestøyl, T. (2022). Utilization of feed resources in the production of Atlantic salmon (Salmo salar) in Norway: An update for 2020. *Aquaculture Reports, 26*, 101316. [https://doi.org/10.1016/j.aqrep.2022.101316](https://doi.org/10.1016/j.aqrep.2022.101316)
* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
* Torrissen, O., Hansen, P. K., Aure, J., Husa, V., Andersen, S., Strohmeier, T., & Olsen, R. E. (2016). *Næringsutslipp fra havbruk - nasjonale og regionale perspektiv*. [https://www.hi.no/resources/publikasjoner/rapport-fra-havforskningen/2016/21-2016_neringsutslipp_fra_havbruk_ot.pdf](https://www.hi.no/resources/publikasjoner/rapport-fra-havforskningen/2016/21-2016_neringsutslipp_fra_havbruk_ot.pdf)
* Ytrestøyl, T., Aas, T. S., & Åsgård, T. (2015). Utilisation of feed resources in production of Atlantic salmon (Salmo salar) in Norway. *Aquaculture, 448*, 365-374. [https://doi.org/10.1016/j.aquaculture.2015.06.023](https://doi.org/10.1016/j.aquaculture.2015.06.023)
