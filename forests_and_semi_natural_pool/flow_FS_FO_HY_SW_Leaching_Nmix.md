---
layout: default
title: Forest Leaching
parent: Forests (FS.FO)
nav_order: 4
---

# Forest Leaching

<iframe src="../output_files/plots/FS_FO_HY_SW_Leaching_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.FO-HY.SW-Leaching-Nmix** is N leached from forest to surface water.

#### Data sources

- From 2013, data supplied by NIVA, produced in the [TEOTIL3](https://github.com/NIVANorge/teotil3) model (Sample et al., 2024<!--cite:sample_teotil3_2024-->), using TEOTIL3's «wood» category.
- For 1990–2012, the natural diffuse loss from TEOTIL2 model results in NIVA's public repository (NIVANorge/teotil2 on GitHub, https://github.com/NIVANorge/teotil2, commit bf3c380), summed to national totals over the outlets of the main river basins 001–247 and 315 (inputs to the coast, after retention in lakes and rivers). This category covers forest, mountain, lakes and the background part of agricultural land, and is not split by land type.
- We do not use the published series for 1990–2012 (Miljødirektoratet's TEOTIL figures and NIVA's annual reports), because for 1990–1995 it contains results from an older TEOTIL version, with 40–50% higher background loading than the TEOTIL2 results used here, which gives an artificial drop in 1996. All years 1990–2012 used here come from the same TEOTIL2 model run.
- Results for 1990–1995 are less certain than for later years, because the input data for those years are incomplete (J. Sample, NIVA, pers. comm., September 2026); the gaps are mainly in point sources, which are not used here.

#### Assumptions

- The TEOTIL2 natural diffuse loss is bias-corrected to TEOTIL3 by multiplying with the ratio between the TEOTIL3 and TEOTIL2 means over the years both models cover (2013–2022). This is the method NIVA uses to extend TEOTIL3 back to 1990 in the annual reports Sample (2025)<!--cite:sample_kildefordelte_2025-->, but applied here to the categories the model uses, and without the published 1990–1995 values; here the TEOTIL2 natural diffuse loss is compared with TEOTIL3 wood + upland, which gives a factor of 1.02.
- Forest is assigned a fraction 0.59 of the scaled value, which is the share of wood in wood + upland in TEOTIL3 over 2013–2023 (0.56–0.60). The other land flow (**FS.OL-HY.SW-Leaching-Nmix**) gets the remaining 0.41.
- TEOTIL3 has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±15 %) applied to reflect that it is not a real, independently observed value.

#### Interpretations and comparisons

- The flow is about 27–42 kt N per year without a clear trend.
- TEOTIL calculates the diffuse loss from land as runoff times area-specific N concentrations, so the year-to-year variation mainly follows precipitation and runoff: low values in dry years (for example 2010) and high values in wet years (for example 2020).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Other flows affected |
|---|---|---|---|---|---|
| TEOTIL, leaching from forest and other land | Modelled statistics | ±30 %, normal | 50% | 96% | [Other Land Leaching](../forests_and_semi_natural_pool/flow_FS_OL_HY_SW_Leaching_Nmix.html) |
| Held constant or averaged (2023+) | Gap filling: held constant or averaged | ±15–15 %, lognormal, grows with distance to known year | – | 4% | none |
| Share of background leaching assigned to forest | Parameter | ±30 %, normal | 49% | – | none |

### References

* Sample, J. E. (2025). *Kildefordelte tilførsler av nitrogen og fosfor til norske kystområder i 2023 – tabeller, figurer og kart*.
* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
