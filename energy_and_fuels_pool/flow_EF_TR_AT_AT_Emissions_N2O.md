---
layout: default
title: Transport emissions (N2O)
parent: Transportation (EF.TR)
nav_order: 1
---

# Transport emissions (N2O)

<iframe src="../output_files/plots/EF_TR_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.TR-AT.AT-Emissions-N2O** is N2O from domestic transport (1.A.3), using the categories given in Table 13 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

#### Data sources

- N2O from the UNFCCC Common Reporting Tables (CRT), Table 1, of the national greenhouse gas inventory.
- N2O from fuel combustion is not measured but calculated in the inventory as fuel consumption (TJ, by fuel type and source category, from the national energy statistics) multiplied by emission factors (kg N2O per TJ), following the IPCC 2006 Guidelines ([IPCC 2006, Vol. 2, Ch. 3](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_3_Ch3_Mobile_Combustion.pdf)); Norway uses a mix of IPCC default and country-specific emission factors, documented in the National Inventory Document ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)). Activity data and implied emission factors are reported in CRT Table 1.A(a).
- For road transport, the emission factors depend on vehicle type, fuel and emission control technology (Euro class), and are combined with vehicle-km in the road traffic model used for the inventory.

#### Interpretations and comparisons

- Road transport (1.A.3.b) accounts for 66–79% of the flow throughout the period.
- N2O from road transport increased from 0.12 kt N/year in 1990 to about 0.18 kt N in 1999–2004, mainly from petrol cars, because early three-way catalytic converters produce N2O as a by-product ([EMEP/EEA Guidebook 2023, ch. 1.A.3.b.i–iv](https://www.eea.europa.eu/en/analysis/publications/emep-eea-guidebook-2023/part-b-sectoral-guidance-chapters/1-energy/1-a-combustion/1-a-3-b-i)).
- In 2005 road transport N2O fell in one step to 0.13 kt N/year. The step comes from the implied N2O emission factor for petrol cars in the CRT, which falls from 3.3 to 2.0 kg N2O/TJ between 2004 and 2005, while petrol use falls by only 4%; the CRT tables do not give the reason.
- After 2005 the flow has been driven by diesel: the implied emission factor for diesel in road transport rose from 0.9 kg N2O/TJ in 2000 to 1.5 in 2010 and 3.1 in 2024, likely due to oxidation catalysts and urea-based selective catalytic reduction (SCR) on newer diesel vehicles (EMEP/EEA Guidebook 2023). Road transport N2O rose from 0.14 kt N/year in 2010 to about 0.20 kt N in 2018–2024, of which diesel accounted for 0.16 kt N and biofuels 0.03 kt N in 2024, while petrol cars contribute almost nothing.
- Railways contributed 0.024–0.033 kt N/year in 1990–1995 (13–16% of the flow), fell to about 0.016 kt N in 1996 and have been 0.009–0.014 kt N since 2010 (4–5%).
- Domestic navigation increased from 0.020 kt N/year in 1990 to about 0.03 kt N and has been fairly stable since 2003 (11–16% of the flow).
- Domestic aviation increased from 0.014 kt N/year in 1990 to 0.019–0.024 kt N in 1996–2019, with a dip to 0.016 kt N in 2020–2021 during the COVID-19 pandemic.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N2O from road transport (Norway's GHG inventory, CRT 1.A.3.b) | Inventory with published uncertainty | ±65 %, triangular | 100% | 100% | 1.00 | 1.00 | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
