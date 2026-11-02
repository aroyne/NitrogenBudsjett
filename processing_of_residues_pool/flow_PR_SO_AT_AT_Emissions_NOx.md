---
layout: default
title: NOx Emissions (Solid Waste)
parent: Solid Waste (PR.SO)
nav_order: 4
---

# NOx Emissions (Solid Waste)

<iframe src="../output_files/plots/PR_SO_AT_AT_Emissions_NOx.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.SO-AT.AT-Emissions-NOx** is NO<sub>x</sub> from waste treatment, using the categories given in Tables 48 and 31 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: the waste incineration part of 1A1a (public electricity and heat production), 5A (solid waste disposal), 5B1 composting, 5B2 anaerobic digestion, 5C (incineration) and 5E (other waste).
- 1A1a is split between waste incineration (counted here) and other heat and power plants (counted in EF.EC-AT.AT) by the waste share of the 1.A.1.a fuel use in the CRT (17–50 %, about 50 % in 2024), as recommended in chapter 1.4.1.2 of Schäppi et al. (2025). The inventory does not split 1A1a by fuel, so the split assumes the same emissions per TJ for waste and other fuels.

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions). The emissions are calculated in the national inventory from the amounts of waste treated and emission factors, or from emissions reported by the plants; the methods are documented in the [Informative Inventory Report 2026, Norway](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/).

#### Interpretations and comparisons

- The flow is about 0.1–0.35 kt N per year and has increased with waste incineration, from about 0.17 kt N in 1990 to 0.34 kt N in 2023–2024. The low value in 2010 (0.10 kt N) comes from the low waste share of 1.A.1.a that year, when the use of other fuels in heat and power plants was high.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-10-22). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, Public electricity and heat production (NFR 1A1a) | Inventory with published uncertainty | ±36.2 %, normal | 100% | 100% | 0.99 | 0.99 | none |

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
