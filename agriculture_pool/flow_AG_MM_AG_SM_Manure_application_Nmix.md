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

- The flow is the sum of FAM and the innmark share of PRP. The utmark share is the PRP per animal category (CRT Table 3.B(b)) weighted with the share of each category's grazing time spent on utmark in 2018 (SSB Rapporter 2020/9 (Bruk av gjødselressurser i jordbruket 2018), Table A79): sheep 51%, goats 54% and horses 16% (each ±20%), reindeer 100% and farmed deer 0%. For cattle the survey shares (dairy cows 16%, suckler cows 30%, other cattle 32%) would give more manure on utmark than the feed taken up on utmark (FS.OL-AG.MM-Grazing-Nmix) allows. The cattle manure on utmark is therefore the number of cattle on utmark (SSB table 12660, which counts animals with at least 5 weeks on utmark; the 1995 level before 1995) times the average N excretion of cattle other than dairy cows (CRT Table 3.B(b); most cattle on utmark are beef cows and young stock) times 8 weeks on utmark (range 5–12, PERT) out of 52, at most the grazing manure of cattle. This is 8–17% of the cattle grazing manure. In total this gives a utmark share of 26–33% of PRP, so 67–74% is applied to AG.SM. The shares are held at the 2018 survey values for all years; before 2009 the subsidy rules required a longer grazing period on utmark (eight instead of five weeks), so the utmark share may have been somewhat higher.

#### Interpretations and comparisons

- The flow is 65–70 kt N per year in the 1990s, rises to about 74 kt N in 2016–2018 and is about 69 kt N in 2024.
- In 2024 managed manure accounts for about 54 kt N and manure deposited on innmark during grazing for about 14 kt N.
- The changes follow the livestock numbers, with fewer dairy cows and more beef cattle, pigs and poultry over the period.
- Manure deposited on utmark (about 7–8 kt N per year) goes to FS.OL, and the losses from it are removed from the AG.SM emission and leaching flows.
- EUROSTAT's Gross Nutrient Balance reports a substantially larger figure for manure N (roughly 40–65% higher across the time series): its documentation states manure excretion coefficients are gross, with "no reductions... made for volatilisation from the moment of excretion till the application to the soil" (Eurostat (2025)<!--cite:eurostat_gnb_glossary_2025-->) – i.e. it measures total excretion rather than what actually reaches the field.
- EUROSTAT's Norwegian series also has a reporting-methodology discontinuity around 2017–2020 (Norway supplied EUROSTAT with pre-calculated results up to 2017; EUROSTAT has calculated results itself from raw activity data since 2020, per personal correspondence with EUROSTAT), producing an artificial ~23% step between 2016 and 2020 that does not appear in the CRT-based series used here.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Manure N applied to soils and on pasture (Norway's GHG inventory, CRT 3.D) | Inventory with published uncertainty | ±20 %, normal | 99% | 99% | 1.00 | 1.00 | [Manure from Grazing on Unmanaged Land](../agriculture_pool/flow_AG_MM_FS_OL_Manure_from_grazing_on_unmanaged_land_Nmix.html), [Grazing on Unmanaged Land](../forests_and_semi_natural_pool/flow_FS_OL_AG_MM_Grazing_Nmix.html) |

### References

* De Klein, C., Novoa, R. S. A., Ogle, S., Smith, K. A., Rochette, P., Wirth, T. C., McConkey, B. G., Mosier, A., & Rypdal, K. (2006). Chapter 11. N2O Emissions from Managed Soils, and CO2 Emissions from Lime and Urea Application. *2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 4: Agriculture, Forestry and Other Land Use*. [https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf)
* Eurostat (2025). *Glossary: Gross nitrogen balance*. [https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Gross_nitrogen_balance](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Gross_nitrogen_balance)
* Norwegian Environment Agency (2020). *Calculation of atmospheric nitrogen emissions from manure in Norwegian agriculture: Technical description of the revised model*. [https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf](https://www.miljodirektoratet.no/globalassets/publikasjoner/m1848/m1848.pdf)
