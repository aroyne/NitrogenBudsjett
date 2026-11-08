---
layout: default
title: Transport emissions (NOx)
parent: Transportation (EF.TR)
nav_order: 3
---

# Transport emissions (NOx)

<iframe src="../output_files/plots/EF_TR_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.TR-AT.AT-Emissions-NOx** is NO<sub>x</sub> from fuel combustion in domestic transport, using the categories given in Table 13 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, with the addition of domestic aviation cruise (1A3aii(ii)), which is a memo item in the CLRTAP reporting but a domestic emission, and is included so that the NO<sub>x</sub> flow covers the same activities as the EF.TR fuel input and N<sub>2</sub>O flows (about 1.1 kt N/year<!--val:nfr/1A3aii(ii)/NOx:2024--> in 2024).

#### Data sources

- Emissions reported by Norway to the UN Convention on Long-range Transboundary Air Pollution (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The reported emissions are not measured but calculated in the national inventory, mainly as activity data (fuel consumption by fuel type and source category, from the national energy statistics) multiplied by emission factors, following the EMEP/EEA Guidebook (European Environment Agency, 2023)<!--cite:eea_guidebook_2023-->; for some large point sources, plant-specific reported emissions are used. The methods are documented in the Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.
- The inventory's NO<sub>x</sub> emission factors for ships are based on detailed calculations for selected years (1993, 1998, 2004 and 2007) with linear interpolation in between (SSB, 2010)<!--cite:ssb_noxfaktorer_2010-->.

#### Interpretations

- Total NO<sub>x</sub> from transport stays roughly flat at 27–33 kt N/year<!--range:EF.TR-AT.AT-Emissions-NOx:1990-2013--> until 2013 and then declines steadily to 12.5 kt N<!--val:EF.TR-AT.AT-Emissions-NOx:2024--> in 2024.
- The late decline does not reflect a delayed effect of catalytic converters, but the sum of four sources with different trajectories:
    - *Passenger cars (1A3bi)*: emissions more than halved from 10.0 kt N/year<!--val:nfr/1A3bi/NOx:1990--> in 1990 to 4.6 kt N<!--val:nfr/1A3bi/NOx:2004--> in 2004 as the petrol car fleet was replaced by cars with three-way catalytic converters, which became mandatory on new passenger cars in Norway from 1989 ([Store norske leksikon: Katalysator – bil](https://snl.no/katalysator_-_bil)). Emissions then increased again to 6.4 kt N/year<!--val:nfr/1A3bi/NOx:2013--> in 2013 as new car sales shifted to diesel, particularly after the CO<sub>2</sub>-based registration tax in 2007 (NHH, 2017)<!--cite:nhh_engangsavgiften_2017-->. Diesel cars cannot use three-way catalysts, and Euro 5 and Euro 6 diesel cars emitted on average about four times their type-approval NO<sub>x</sub> limit in real-world driving ([ICCT](https://theicct.org/test-results-confirm-only-10-of-euro-6-cars-meet-emission-limit-in-real-world-driving-conditions/)). The decline after 2013 coincides with Euro 6 (all new cars from September 2015), real-driving emission (RDE) testing from 2017 ([DieselNet: EU light-duty standards](https://dieselnet.com/standards/eu/ld.php)), and the rapid replacement of new petrol and diesel cars by battery electric vehicles ([SSB: Bilparken](https://www.ssb.no/transport-og-reiseliv/landtransport/statistikk/bilparken)). Light commercial vehicles (1A3bii) follow the same pattern, rising from 1.8 kt N/year<!--val:nfr/1A3bii/NOx:1990--> in 1990 to 2.7 kt N<!--val:nfr/1A3bii/NOx:2012--> in 2012 and falling to 1.4 kt N<!--val:nfr/1A3bii/NOx:2024--> in 2024.
    - *Heavy-duty vehicles (1A3biii)*: emissions were stable at 7.6–8.8 kt N/year<!--range:nfr/1A3biii/NOx:1990-2008--> until 2008 and have since fallen to 1.5 kt N<!--val:nfr/1A3biii/NOx:2024-->, following Euro V (all new registrations from 2009) and in particular Euro VI (all new registrations from January 2014) ([DieselNet: EU heavy-duty standards](https://dieselnet.com/standards/eu/hd.php)).
    - *Domestic navigation (1A3dii)*: shipping accounts for 30–50% of transport NO<sub>x</sub> and is unaffected by catalytic converter requirements for cars. Emissions increased from 9.1 kt N/year<!--val:nfr/1A3dii/NOx:1990--> in 1990 to 15.5 kt N<!--val:nfr/1A3dii/NOx:1999--> in 1999 and remained around 12 kt N<!--mean:nfr/1A3dii/NOx:2000-2013--> until 2013, before falling to 5.8 kt N<!--val:nfr/1A3dii/NOx:2024--> in 2024. The NO<sub>x</sub> tax introduced on 1 January 2007 and the NO<sub>x</sub> Fund established in 2008 have financed measures such as catalytic cleaning, engine improvements and low-emission ferries ([Teknisk Ukeblad](https://www.tu.no/artikler/nytt-fond-erstatter-nox-avgift/322638); [Næringslivets NO<sub>x</sub>-fond](https://www.nox-fondet.no/)). Part of the decline after 2000 reflects a smaller share of fuel use by shuttle tankers with high emission factors and newer engines (SSB, 2010)<!--cite:ssb_noxfaktorer_2010-->.
- From around 2014, all three major sources – cars, heavy-duty vehicles and shipping – decline simultaneously, which explains why the total does not fall until then.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, National navigation (shipping) (NFR 1A3dii) | Inventory with published uncertainty | ±25 %, normal | 36% | 68% | 0.31 | 0.44 | none |
| NO<sub>x</sub>, road transport exhaust (NFR 1A3bi–iv) | Inventory with published uncertainty | ±15.8 %, normal | 64% | 30% | 0.64 | 0.45 | none |

### References

* European Environment Agency (2023). *EMEP/EEA air pollutant emission inventory guidebook 2023* (EMEP/EEA joint report 06/2023). [eea.europa.eu](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023)
* EMEP (2025). *Officially reported emission data*. [ceip.at](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* NHH (2017). Engangsavgiften gir renere bilpark. *NHH Bulletin*. [nhh.no](https://nhh.no/nhh-bulletin/artikkelarkiv/2017/februar/engangsavgiften-gir-renere-bilpark/)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
* SSB (2010). *Nye NO<sub>x</sub>-faktorer gir lavere utslipp fra skip*. [ssb.no](https://www.ssb.no/natur-og-miljo/artikler-og-publikasjoner/nye-no-x-faktorer-gir-lavere-utslipp-fra-skip)
