---
layout: default
title: Transport emissions (NH3)
parent: Transportation (EF.TR)
nav_order: 2
---

# Transport emissions (NH3)

<iframe src="../output_files/plots/EF_TR_AT_AT_Emissions_NH3.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
EF.TR-AT.AT-Emissions-NH3 denotes ammonia emissions from fuel combustion. We have used data from CLRTAP Inventory Submissions EMEP (2025)<!--cite:emep_officially_2025--> as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, using the categories given in Table 13, with the addition of domestic aviation cruise (1A3aii(ii)), included for consistency with the EF.TR fuel input and N2O flows. 

**Interpretation**

- Passenger cars (NFR 1A3bi) account for 90–95% of the flow and determine its shape: emissions rise steadily from 0.18 Gg NH3 in 1990 to a peak of 2.0 Gg in 2002, and then decline steadily to 0.31 Gg in 2024.
- Ammonia from road transport is formed almost exclusively in three-way catalytic converters on petrol cars, where NO is over-reduced to NH3 under slightly fuel-rich operating conditions ([EMEP/EEA Guidebook 2023, ch.
- 1.A.3.b.i–iv](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023/part-b-sectoral-guidance-chapters/1-energy/1-a-combustion/1-a-3-b-i)).
- Catalytic converters became mandatory on all new passenger cars in Norway from 1989 ([Store norske leksikon: Katalysator – bil](https://snl.no/katalysator_-_bil)), so the rise during the 1990s reflects the gradual turnover of the car fleet towards catalyst-equipped vehicles.
- The subsequent decline has several overlapping causes: (i) newer catalyst generations (Euro 3 and later) with more precise air–fuel control emit considerably less NH3 per km than the early catalyst cars, which were scrapped during the 2000s; (ii) new car sales shifted from petrol to diesel, particularly after the CO2-based registration tax was introduced in 2007 (the diesel share of new cars rose from 48% in 2006 to 76% in 2011; [NHH, 2017](https://nhh.no/nhh-bulletin/artikkelarkiv/2017/februar/engangsavgiften-gir-renere-bilpark/); [Dokument 8:138 S (2012–2013)](https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Representantforslag/2012-2013/dok8-201213-138/)), and diesel cars without SCR emit very little NH3; and (iii) from around 2012, battery electric vehicles replaced a rapidly growing share of new petrol cars ([SSB: Bilparken](https://www.ssb.no/transport-og-reiseliv/landtransport/statistikk/bilparken)).
- The smoothness of the curve reflects that road transport emissions in the inventory are modelled from vehicle-km by vehicle and emission class multiplied by emission factors, rather than measured, so they follow the gradual fleet turnover ([Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)).

In contrast, emissions from light commercial vehicles (1A3bii) have increased again since 2015, and emissions from heavy-duty vehicles (1A3biii) have grown from 0.007 Gg in 2002 to 0.038 Gg in 2024. This is most likely ammonia slip from urea-based selective catalytic reduction (SCR) used to meet Euro VI and Euro 6 NOx limits ([EMEP/EEA Guidebook 2023, ch. 1.A.3.b.i–iv](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023/part-b-sectoral-guidance-chapters/1-energy/1-a-combustion/1-a-3-b-i)). Although still small, light commercial and heavy-duty vehicles together now emit about 0.07 Gg NH3, close to half of the passenger-car level in 1990.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
