---
layout: default
title: Transport emissions (NOx)
parent: Transportation (EF.TR)
nav_order: 3
---

# Transport emissions (NOx)

<iframe src="../output_files/plots/EF_TR_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
EF.TR-AT.AT-Emissions-NOx denotes NOx emissions from fuel combustion. We have used data from CLRTAP Inventory Submissions EMEP (2025)<!--cite:emep_officially_2025--> as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, using the categories given in Table 13, with the addition of domestic aviation cruise (1A3aii(ii)), which is a memo item in the CLRTAP reporting but a domestic emission, and is included so that the NOx flow covers the same activities as the EF.TR fuel input and N2O flows (about 3.6 Gg NOx in 2024). 

**Interpretation of the time series.** Total NOx from transport stays roughly flat at 90–110 Gg NOx until 2013 and then declines steadily to 41 Gg in 2024. The late decline does not reflect a delayed effect of catalytic converters, but the sum of four sources with different trajectories:

* *Passenger cars (1A3bi)*: emissions more than halved from 33 Gg in 1990 to 15 Gg in 2004 as the petrol car fleet was replaced by cars with three-way catalytic converters, which became mandatory on new passenger cars in Norway from 1989 ([Store norske leksikon: Katalysator – bil](https://snl.no/katalysator_-_bil)). Emissions then increased again to 21 Gg in 2013 as new car sales shifted to diesel, particularly after the CO2-based registration tax in 2007 ([NHH, 2017](https://nhh.no/nhh-bulletin/artikkelarkiv/2017/februar/engangsavgiften-gir-renere-bilpark/)). Diesel cars cannot use three-way catalysts, and Euro 5 and Euro 6 diesel cars emitted on average about four times their type-approval NOx limit in real-world driving ([ICCT](https://theicct.org/test-results-confirm-only-10-of-euro-6-cars-meet-emission-limit-in-real-world-driving-conditions/)). The decline after 2013 coincides with Euro 6 (all new cars from September 2015), real-driving emission (RDE) testing from 2017 ([DieselNet: EU light-duty standards](https://dieselnet.com/standards/eu/ld.php)), and the rapid replacement of new petrol and diesel cars by battery electric vehicles ([SSB: Bilparken](https://www.ssb.no/transport-og-reiseliv/landtransport/statistikk/bilparken)). Light commercial vehicles (1A3bii) follow the same pattern, rising from 6 Gg in 1990 to 9 Gg in 2012 and falling to 4.5 Gg in 2024.
* *Heavy-duty vehicles (1A3biii)*: emissions were stable at 25–29 Gg until 2008 and have since fallen to 5 Gg, following Euro V (all new registrations from 2009) and in particular Euro VI (all new registrations from January 2014) ([DieselNet: EU heavy-duty standards](https://dieselnet.com/standards/eu/hd.php)).
* *Domestic navigation (1A3dii)*: shipping accounts for 30–50% of transport NOx and is unaffected by catalytic converter requirements for cars. Emissions increased from 30 Gg in 1990 to 51 Gg in 1999 and remained around 40 Gg until 2013, before falling to 19 Gg in 2024. The NOx tax introduced on 1 January 2007 and the NOx Fund established in 2008 have financed measures such as catalytic cleaning, engine improvements and low-emission ferries ([Teknisk Ukeblad](https://www.tu.no/artikler/nytt-fond-erstatter-nox-avgift/322638); [Næringslivets NOx-fond](https://www.nox-fondet.no/)). Note that the inventory's NOx emission factors for ships are based on detailed calculations for selected years (1993, 1998, 2004 and 2007) with linear interpolation in between, and that part of the decline after 2000 reflects a smaller share of fuel use by shuttle tankers with high emission factors and newer engines ([SSB, 2010](https://www.ssb.no/natur-og-miljo/artikler-og-publikasjoner/nye-no-x-faktorer-gir-lavere-utslipp-fra-skip)).

From around 2014, all three major sources – cars, heavy-duty vehicles and shipping – decline simultaneously, which explains why the total does not fall until then.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
