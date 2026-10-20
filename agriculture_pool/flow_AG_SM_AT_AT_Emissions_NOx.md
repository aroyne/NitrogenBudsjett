---
layout: default
title: NOx emissions from soil management
parent: Soil Management (AG.SM)
nav_order: 5
---

# NOx emissions from soil management

<iframe src="../output_files/plots/AG_SM_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AG.SM-AT.AT-Emissions-NOx** is NOx from agricultural soils: the soil categories 3Da1–3Df in Table 30 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> and field burning of agricultural residues (3F).

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions, EMEP 2025<!--cite:emep_officially_2025-->), as advised by Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.
- The emissions are calculated in the national inventory with the same manure model as the greenhouse gas inventory: N in manure, mineral fertilizer and other N sources multiplied by NH3 and NOx emission factors for each animal category, storage system, spreading method and fertilizer type. The methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).
- The LULUCF codes 4B1, 4B2, 4C1 and 4C2 in Table 30 are not reported in the CLRTAP inventory.
- The inventory counts all manure deposited by grazing animals as input to managed soils, including the share deposited on utmark (unmanaged land), which this model does not count as input to AG.SM (see AG.MM-AG.SM-Manure application-Nmix).

#### Assumptions

- The utmark share (26–33% of grazing manure, see AG.MM-AG.SM-Manure application-Nmix) of the emissions from grazing animals (3Da3) is therefore removed from this flow; it is counted in FS.OL-AT.AT-Emissions-NOx.

#### Interpretations and comparisons

- The flow is about 2.0–2.5 kt N per year.
- Field burning contributed 0.3 kt N in 1990 and less than 0.05 kt N in 2024.
- Mineral fertilizer (1.1 kt N in 2024) and manure spreading (0.65 kt N) are the main sources.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NOx, Inorganic N-fertilizers (includes also urea application) (NFR 3Da1) | Inventory with published uncertainty | −64.3/+180.1 %, lognormal | 92% | 89% | 0.57 | 0.56 | none |
| NOx, Animal manure applied to soils (NFR 3Da2a) | Inventory with published uncertainty | −50.4/+101.8 %, lognormal | 7% | 10% | 0.25 | 0.32 | none |

### References

* EMEP (2025). *Officially reported emission data*. [https://www.ceip.at/webdab-emission-database/reported-emissiondata](https://www.ceip.at/webdab-emission-database/reported-emissiondata)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
