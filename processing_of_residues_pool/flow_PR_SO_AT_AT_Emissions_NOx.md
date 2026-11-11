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

- **PR.SO-AT.AT-Emissions-NOx** is NO<sub>x</sub> from waste treatment, using the categories given in Tables 48 and 31 of Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->: 5A (solid waste disposal), 5B1 composting, 5B2 anaerobic digestion, 5C (incineration) and 5E (other waste).
- Table 48 also lists 1A1a (public electricity and heat production) for waste incineration with energy recovery. Since the incinerated waste is delivered to EF.EC (PR.SO-EF.EC-Waste to energy-Nmix), all of 1A1a is counted in EF.EC-AT.AT.

#### Data sources

- Emissions reported by Norway to CLRTAP (CLRTAP inventory submissions). The emissions are calculated in the national inventory from the amounts of waste treated and emission factors, or from emissions reported by the plants; the methods are documented in the Informative Inventory Report (Miljødirektoratet, 2026)<!--cite:miljodirektoratet_iir_2026-->.

#### Interpretations

- The flow is very small, about 0.005 kt N per year<!--mean:PR.SO-AT.AT-Emissions-NOx:1990-2024-->, since NO<sub>x</sub> from waste incineration with energy recovery is counted in EF.EC-AT.AT-Emissions-NOx (0.06–0.32 kt N per year).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-09). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| NO<sub>x</sub>, Cremation (NFR 5C1bv) | Inventory with published uncertainty | ±20.1 %, normal | 26% | 78% | 0.66 | 0.88 | none |
| NO<sub>x</sub>, Municipal waste incineration (NFR 5C1a) | Inventory with published uncertainty | −53.9/+117 %, lognormal | 71% | 20% | 0.26 | 0.09 | none |
| NO<sub>x</sub>, Other waste (please specify in IIR) (NFR 5E) | Inventory with published uncertainty | −60.5/+153 %, lognormal | 3% | 2% | 0.04 | 0.02 | none |

### References

* <span id="ref-miljodirektoratet_iir_2026" data-cite="Miljødirektoratet" data-year="2026"></span>Miljødirektoratet (2026). *Informative Inventory Report (IIR) 2026. Norway. Air pollutant emissions 1990–2024* (M-3140). [miljodirektoratet.no](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/informative-inventory-report-iir-2026-norway-air-pollutant-emissions-1990-2024/)
* <span id="ref-schappi_annexes_2025" data-cite="Schäppi et al." data-year="2025"></span>Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
