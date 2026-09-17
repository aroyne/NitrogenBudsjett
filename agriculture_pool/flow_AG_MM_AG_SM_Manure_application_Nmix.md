---
layout: default
title: Manure Application
parent: Manure Management (AG.MM)
nav_order: 1
---

# Manure Application

<iframe src="../output_files/plots/AG_MM_AG_SM_Manure_application_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Taken from the UNFCCC Common Reporting Table (CRT), Table 3.D. The main component is row "Animal manure applied to soils" - the IPCC 2006 Guidelines' FAM term (Volume 4, Chapter 11, Equation 11.4; De Klein et al. (2006)<!--cite:deklein_chapter11_2006-->), i.e. managed manure N net of losses during animal housing and manure storage (tracked separately as AG.MM's own NH3/N2O/NOx emissions flows). We add to this the share of manure deposited directly by grazing animals (row "Urine and dung deposited by grazing animals", PRP) that we estimate lands on agricultural grazing land (innmark) rather than unmanaged land (utmark) - approximately 44-62 % of the national PRP total, apportioned by animal category using typical Norwegian grazing practice (e.g. dairy cattle graze almost exclusively on innmark, while sheep spend a large share of the season on utmark). The utmark share is not included in any flow in this study; see the Other Land (FS.OL) subpool page for that portion and why it is excluded. Norway's calculation methodology for both terms is documented in Norwegian Environment Agency (2020)<!--cite:miljodirektoratet_manure_2020-->. 

EUROSTAT's Gross Nutrient Balance reports a substantially larger figure for manure N (roughly 40-65 % higher across the time series): its documentation states manure excretion coefficients are gross, with "no reductions... made for volatilisation from the moment of excretion till the application to the soil" (Eurostat (2025)<!--cite:eurostat_gnb_glossary_2025-->) - i.e. it measures total excretion rather than what actually reaches the field. EUROSTAT's Norwegian series also has a reporting-methodology discontinuity around 2017-2020 (Norway supplied EUROSTAT with pre-calculated results up to 2017; EUROSTAT has calculated results itself from raw activity data since 2020, per personal correspondence with EUROSTAT), producing an artificial ~23 % step between 2016 and 2020 that does not appear in the CRT-based series used here.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* De Klein, C., Novoa, R. S. A., Ogle, S., Smith, K. A., Rochette, P., Wirth, T. C., McConkey, B. G., Mosier, A., & Rypdal, K. (2006). Chapter 11. N2O Emissions from Managed Soils, and CO2 Emissions from Lime and Urea Application. *2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 4: Agriculture, Forestry and Other Land Use*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf)
* Eurostat (2025). *Glossary: Gross nitrogen balance*. [https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Gross_nitrogen_balance](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Gross_nitrogen_balance)
* Norwegian Environment Agency (2020). *Calculation of atmospheric nitrogen emissions from manure in Norwegian agriculture: Technical description of the revised model*. [https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf](https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf)
