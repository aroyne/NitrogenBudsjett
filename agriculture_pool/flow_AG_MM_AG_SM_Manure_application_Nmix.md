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

- **AG.MM-AG.SM-Manure application-Nmix** is the manure N applied to agricultural soils: managed manure N net of losses during animal housing and manure storage (tracked separately as AG.MM's own NH<sub>3</sub>/N<sub>2</sub>O/NO<sub>x</sub> emission flows), plus the share of manure deposited directly by grazing animals that lands on agricultural grazing land (innmark) rather than unmanaged land (utmark).
- The unmanaged-land share goes to FS.OL as AG.MM-FS.OL-Manure from grazing on unmanaged land-Nmix.

#### Data sources

- The UNFCCC Common Reporting Tables (CRT), Table 3.D: the row "Animal manure applied to soils" – the IPCC 2006 Guidelines' FAM term, managed animal manure N applied to soils (Volume 4, Chapter 11, Equation 11.4; De Klein et al. (2006)<!--cite:deklein_chapter11_2006-->) – and the row "Urine and dung deposited by grazing animals" (PRP, the IPCC term for N deposited by grazing animals on pasture, range and paddock).
- Norway's inventory calculates the N excreted per animal category from animal numbers and national N excretion rates, distributes the manure between grazing and the different housing and storage systems using SSB's surveys of manure use in agriculture, and deducts the N lost as NH<sub>3</sub>, N<sub>2</sub>O, NO<sub>x</sub> and N<sub>2</sub> during housing and storage. The method is documented in Norwegian Environment Agency (2020)<!--cite:miljodirektoratet_manure_2020--> and in the [Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/).

#### Assumptions

- The flow is the sum of FAM and the agricultural-land share of PRP. The unmanaged-land share is the PRP per animal category (CRT Table 3.B(b)) weighted with the share of each category's grazing time spent on unmanaged land in 2018 (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79): sheep 51%, goats 54% and horses 16% (each ±20%), reindeer 100% and farmed deer 0%. For cattle the survey shares (dairy cows 16%, suckler cows 30%, other cattle 32%) would give more manure on unmanaged land than the feed taken up on unmanaged land (FS.OL-AG.MM-Grazing-Nmix) allows. The cattle manure on unmanaged land is therefore the number of cattle on unmanaged land (SSB table 12660, which counts animals with at least 5 weeks on unmanaged land; the 1995 level before 1995) times the average N excretion of cattle other than dairy cows (CRT Table 3.B(b); most cattle on unmanaged land are beef cows and young stock) times 8 weeks on unmanaged land (range 5–12, PERT) out of 52, at most the grazing manure of cattle. This is 8–17% of the cattle grazing manure. The manure on unmanaged land is at most the N taken up by grazing there (FS.OL-AG.MM-Grazing-Nmix) minus the share retained in growth, milk and wool, 10% (range 5–15%, triangular; IPCC 2006 Vol. 4 Table 10.20 gives 0.10 for sheep and goats and 0.07 for other cattle and horses, with an uncertainty of ±50%). This cap applies from 2000; the rest of the grazing manure is then applied to AG.SM, so the total equals the inventory's PRP. In total this gives an unmanaged-land share of 26–30% of PRP, so 70–74% is applied to AG.SM. The shares are held at the 2018 survey values for all years; before 2009 the subsidy rules required a longer grazing period on unmanaged land (eight instead of five weeks), so the unmanaged-land share may have been somewhat higher.
- N lost when manure is used for biogas and spread as digestate is not deducted. Manure to biogas plants rose from zero before 2012 to about 0.5 kt N in 2023 (Landbruksdirektoratet, 2025)<!--cite:landbruksdirektoratet_biogass_2025-->; with the loss fraction used for digestate elsewhere in the model (10%, range 6–30%), the loss is about 0.05 kt N per year (at most 0.15 kt N).

#### Interpretations

- The flow is 65–70 kt N per year in the 1990s, rises to about 75 kt N in 2016–2018 and is about 70 kt N in 2024.
- In 2024 managed manure accounts for about 54 kt N and manure deposited on agricultural land during grazing for about 16 kt N.
- The changes follow the livestock numbers, with fewer dairy cows and more beef cattle, pigs and poultry over the period.
- Manure deposited on unmanaged land (about 7 kt N per year) goes to FS.OL, and the losses from it are removed from the AG.SM emission and leaching flows.
- EUROSTAT's Gross Nutrient Balance reports a substantially larger figure for manure N (roughly 40–65% higher across the time series): its documentation states manure excretion coefficients are gross, with "no reductions... made for volatilisation from the moment of excretion till the application to the soil" (Eurostat (2025)<!--cite:eurostat_gnb_glossary_2025-->) – i.e. it measures total excretion rather than what actually reaches the field.
- EUROSTAT's Norwegian series also has a reporting-methodology discontinuity around 2017–2020 (Norway supplied EUROSTAT with pre-calculated results up to 2017; EUROSTAT has calculated results itself from raw activity data since 2020, per personal correspondence with EUROSTAT), producing an artificial ~23% step between 2016 and 2020 that does not appear in the CRT-based series used here.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-04). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Manure N applied to soils and on pasture (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | ±20 %, normal | 99% | 99% | 1.02 | 1.08 | [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [N<sub>2</sub>O emissions from denitrification](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_N2O.html), [NH<sub>3</sub> emissions](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NH3.html), [NO<sub>x</sub> emissions from soil management](../agriculture_pool/flow_AG_SM_AT_AT_Emissions_NOx.html) and 5 more |

### References

* De Klein, C., Novoa, R. S. A., Ogle, S., Smith, K. A., Rochette, P., Wirth, T. C., McConkey, B. G., Mosier, A., & Rypdal, K. (2006). Chapter 11. N<sub>2</sub>O Emissions from Managed Soils, and CO<sub>2</sub> Emissions from Lime and Urea Application. *2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 4: Agriculture, Forestry and Other Land Use*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf)
* Eurostat (2025). *Glossary: Gross nitrogen balance*. [https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Gross_nitrogen_balance](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Gross_nitrogen_balance)
* Landbruksdirektoratet (2025). *Biogass*. [https://www.landbruksdirektoratet.no/nb/statistikk-og-utviklingstrekk/statistikk-over-miljotilskudd-i-jordbruket/biogass](https://www.landbruksdirektoratet.no/nb/statistikk-og-utviklingstrekk/statistikk-over-miljotilskudd-i-jordbruket/biogass)
* Norwegian Environment Agency (2020). *Calculation of atmospheric nitrogen emissions from manure in Norwegian agriculture: Technical description of the revised model*. [https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf](https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf)
