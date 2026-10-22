---
layout: default
title: Surface water N2O emissions
parent: Surface Water (HY.SW)
nav_order: 2
---

# Surface water N2O emissions

<iframe src="../output_files/plots/HY_SW_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HY.SW-AT.AT-Emissions-N2O** is N2O from denitrification in lakes and rivers.

#### Data sources

- N retention in surface waters from data supplied by NIVA, produced in the [TEOTIL3](https://github.com/NIVANorge/teotil3) model (Sample et al., 2024<!--cite:sample_teotil3_2024-->), from 2013.

#### Assumptions

- All N retained in surface water is assumed lost to denitrification, with 1% as N2O (lognormal, 95% interval 0.05–20%) and the rest as N2.
- For years prior to 2013, retention is calculated from **HY.SW-HY.CW-Inflow to coastal waters-Nmix** with the TEOTIL3 ratio between retention and diffuse inputs to the coast, as for the N2 flow; for those years the inflow is based on bias-corrected TEOTIL2 results (see that flow).
- TEOTIL3 has not been updated for 2024 at the time of writing; the 2024 value is held at the 2023 value.

#### Interpretations and comparisons

- The flow is about 0.13–0.16 kt N per year, with a large uncertainty from the N2O share of denitrification.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-22.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| Share of retained N in surface water emitted as N2O | Parameter | 0.005–0.2, lognormal | 100% | 100% | 1.00 | 1.00 | [N2 emissions from denitrification in surface waters](../hydrosphere_pool/flow_HY_SW_AT_AT_Emissions_N2.html) |

### References

* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
