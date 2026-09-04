---
layout: default
title: 7. Atmosphere (AT)
nav_order: 8
has_children: true
---

# Pool: 7. Atmosphere (AT)

This section contains all documented nitrogen flows leaving the Atmosphere pool.

---

## Interactive Mass Balance Overview (1990-2023)

Hover over the chart to inspect specific streams, or click legend items to toggle visibility.

<iframe src="../output_files/plots/balance_AT.html" width="100%" height="600px" frameborder="0" scrolling="no"></iframe>

### Atmospheric Nitrogen Deposition Overview

Atmospheric deposition to the Norwegian mainland is distributed across five land-cover categories - agricultural soils (AG.SM), forest (FS.FO), other land (FS.OL), settlements (HS.HS) and surface waters (HY.SW) - each documented as its own flow below.

Deposition data comes from NILU (described in Blake et al. (2023)), which gives gridded deposition data for both oxidized and reduced N as averages for the periods 1983-1987, 1988-1992, 1997-2001, 2002-2006, 2007-2011 and 2012-2016. Deposition is allocated to each land class by intersecting this deposition grid with the NIBIO AR5 land-cover map (NIBIO, 2016) (FKB-AR5, downloaded from geonorge.no): each AR5 polygon is assigned to one of the five classes above (settlements: AR5 types 11-12; agriculture: 21-23; forest: 30; surface water: 81; other: 50/60/70/99), and each grid cell's deposition is distributed across classes in proportion to the area of each class within that cell. The resulting land-class areas agree well with NIBIO's own Arealbarometer, aside from a modest discrepancy in the 'other' category from differences in how unclassified area is handled.

Summed across the five land classes, this gives a total of about 68 ktN oxidized N (OXN) and 73 ktN reduced N (RDN) for the 2012-2016 period. No new NILU period map exists yet for 2017 onward, so the 2012-2016 land-class distribution is kept and scaled by the national trend reported for that period. NILU's own guidance for trend assessment (personal correspondence, 2026) is to use their measurement-kriging method specifically, since it is the only method applied consistently across all periods - their two most recent periods instead assimilate measurements with the EMEP chemical transport model, with the fusion methodology itself changing somewhat between periods. Applying the kriging-method trend reported in Blake et al. (2023) (a 10% decrease in oxidized N and 17% in reduced N since 2015) gives about 61 ktN OXN and 61 ktN RDN from 2017 onward - a step change rather than a gradual trend, extrapolated flat for years after 2021.


### Flows that are zero or neglected:

* **AT.AT-EF.EC-Combustion N2 fixation-N2**, **AT.AT-EF.IC-Combustion N2 fixation-N2** and **AT.AT-EF.OE-Combustion N2 fixation-N2** are neglected because we have chosen to ignore nitrogen fixation in combustion processes. In fuel combustion, some bound N is converted to NOx, and some atmospheric N2 is also converted to N2. The amount of resulting NOx depends on the combustion conditions and on the use of catalytic converters. It is possible to estimate an N2 fixation rate based on mass balance, but we have chosen not to do so because it does not add useful understanding of the flows of reactive N in the NNB.
* **AT.AT-HY.CW-Deposition-OXN**, **AT.AT-HY.CW-Deposition-RDN** and **AT.AT-HY.CW-N2 fixation-N2** are neglected because we lack an accurate area for coastal waters and do not attempt to make a mass balance for CW.

### References

* Blake, L. R., Aas, W., Denby, B., Hjellbrekke, A., Mu, Q., Simpson, D., & Fagerli, H. (2023). *Deposition of sulfur and nitrogen in Norway 2017-2021*.
* NIBIO (2016). *AR5*. [https://www.nibio.no/tema/jord/arealressurser/arealressurskart-ar5?locationfilter=true](https://www.nibio.no/tema/jord/arealressurser/arealressurskart-ar5?locationfilter=true)
