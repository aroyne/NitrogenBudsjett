---
layout: default
title: Manure Application
parent: Manure Management (AG.MM)
nav_order: 1
---

# Manure Application

<iframe src="../output_files/plots/AG_MM_AG_SM_Manure_application_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.MM-AG.SM-Manure application-Nmix** is the manure N applied to agricultural soils: managed manure N net of losses during animal housing and manure storage (tracked separately as AG.MM's own NH3/N2O/NOx emission flows), plus the share of manure deposited directly by grazing animals that lands on agricultural grazing land (innmark) rather than unmanaged land (utmark).
- The utmark share goes to FS.OL as AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix.

#### Data sources

- The UNFCCC Common Reporting Tables (CRT), Table 3.D: the row "Animal manure applied to soils" – the IPCC 2006 Guidelines' FAM term (Volume 4, Chapter 11, Equation 11.4; De Klein et al. (2006)<!--cite:deklein_chapter11_2006-->) – and the row "Urine and dung deposited by grazing animals" (PRP).
- Norway's inventory calculates the N excreted per animal category from animal numbers and national N excretion rates, distributes the manure between grazing and the different housing and storage systems using SSB's surveys of manure use in agriculture, and deducts the N lost as NH3, N2O, NOx and N2 during housing and storage. The method is documented in Norwegian Environment Agency (2020)<!--cite:miljodirektoratet_manure_2020--> and in the [Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/).

#### Assumptions

- The flow is the sum of FAM and the innmark share of PRP. The utmark share is the PRP per animal category (CRT Table 3.B(b)) weighted with the share of each category's grazing time spent on utmark in 2018 (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79): dairy cows 16%, suckler cows 30%, other cattle 32%, sheep 51%, goats 54% and horses 16% (each ±20%), reindeer 100% and farmed deer 0%. This gives a utmark share of 35–39% of PRP, so 61–65% is applied to AG.SM. The shares are held at the 2018 survey values for all years; before 2009 the subsidy rules required a longer grazing period on utmark (eight instead of five weeks), so the utmark share may have been somewhat higher.

#### Interpretations and comparisons

- The flow is 64–67 kt N per year in the 1990s, rises to about 72 kt N in 2015–2018 and is about 68 kt N in 2024.
- In 2024 managed manure accounts for about 54 kt N and manure deposited on innmark during grazing for about 14 kt N.
- The changes follow the livestock numbers, with fewer dairy cows and more beef cattle, pigs and poultry over the period.
- Manure deposited on utmark (about 9 kt N per year) goes to FS.OL, and the losses from it are removed from the AG.SM emission and leaching flows.
- EUROSTAT's Gross Nutrient Balance reports a substantially larger figure for manure N (roughly 40–65% higher across the time series): its documentation states manure excretion coefficients are gross, with "no reductions... made for volatilisation from the moment of excretion till the application to the soil" (Eurostat (2025)<!--cite:eurostat_gnb_glossary_2025-->) – i.e. it measures total excretion rather than what actually reaches the field.
- EUROSTAT's Norwegian series also has a reporting-methodology discontinuity around 2017–2020 (Norway supplied EUROSTAT with pre-calculated results up to 2017; EUROSTAT has calculated results itself from raw activity data since 2020, per personal correspondence with EUROSTAT), producing an artificial ~23% step between 2016 and 2020 that does not appear in the CRT-based series used here.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* De Klein, C., Novoa, R. S. A., Ogle, S., Smith, K. A., Rochette, P., Wirth, T. C., McConkey, B. G., Mosier, A., & Rypdal, K. (2006). Chapter 11. N2O Emissions from Managed Soils, and CO2 Emissions from Lime and Urea Application. *2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 4: Agriculture, Forestry and Other Land Use*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf)
* Eurostat (2025). *Glossary: Gross nitrogen balance*. [https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Gross_nitrogen_balance](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Gross_nitrogen_balance)
* Norwegian Environment Agency (2020). *Calculation of atmospheric nitrogen emissions from manure in Norwegian agriculture: Technical description of the revised model*. [https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf](https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf)
