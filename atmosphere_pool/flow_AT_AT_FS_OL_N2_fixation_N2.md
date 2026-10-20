---
layout: default
title: Biological N2 Fixation (Other Land)
parent: 7. Atmosphere (AT)
nav_order: 9
---

# Biological N2 Fixation (Other Land)

<iframe src="../output_files/plots/AT_AT_FS_OL_N2_fixation_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **AT.AT-FS.OL-N2 fixation-N2** is biological N2 fixation on other land, which in our model includes what Moldan et al. (2025)<!--cite:moldan_where_2025--> treat as a separate wetland (WL) compartment.

#### Data sources

- N2 fixation rates from Table 62 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025--> (Reddy and DeLaune, 2008): 11 (0–22) kg N/ha for peat bogs, 29 (0–58) kg N/ha for freshwater marshes and 4 (0–7) kg N/ha for mud flats.
- Land type areas from the CORINE land cover inventory (European Environment Agency, 2019<!--cite:european_environment_agency_corine_2019-->): 2.10 million ha peat bogs, 296 ha inland marshes and 18 272 ha intertidal flats.

#### Assumptions

- The mud-flat rate is used for CORINE intertidal flats.

#### Interpretations and comparisons

- The flow is constant at about 23 kt N per year; almost all comes from peat bogs, while intertidal flats and freshwater marshes contribute less than 0.1 kt N.
- In the Swedish NNB (Moldan et al., 2025)<!--cite:moldan_where_2025-->, N2 fixation in the OL compartment was considered negligible. Our total is therefore not directly comparable to that estimate, but corresponds closely to their separate WL estimate of about 30 kt N (Jutterström et al., 2020)<!--cite:jutterstrom_swedish_2020-->.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources with at least 2% of the variance of this flow in one of the periods, from a first-order sensitivity analysis around the central run: each source is raised by 10 % on its own, and the change in the flow is scaled with the source's uncertainty in the Monte Carlo. Shares are averages over the years of the period. They are indicative where the flow is a residual close to zero or a source has a strongly skewed distribution. Elasticity: relative change in the flow per relative change in the source; a negative value means the flow decreases when the source increases. Computed 2026-10-20.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N fixation rate in peat bogs | Parameter | 0–22 (min–max), triangular | 94% | 94% | 1.00 | 1.00 | none |
| Peat bog area | Parameter | ±20 %, normal | 6% | 6% | 1.00 | 1.00 | none |

### References

* European Environment Agency (2019). *CORINE Land cover inventory*. [https://www.eea.europa.eu/en/datahub/datahubitem-view/a5144888-ee2a-4e5d-a7b0-2bbf21656348](https://www.eea.europa.eu/en/datahub/datahubitem-view/a5144888-ee2a-4e5d-a7b0-2bbf21656348)
* Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation*.
* Moldan, F., Stadmark, J., Jutterström, S., & Ljunggren, J. (2025). Where does Sweden’s nitrogen go? Building a comprehensive national nitrogen budget. *Environmental Research Letters, 20*(12), 124068. [https://doi.org/10.1088/1748-9326/ae2697](https://doi.org/10.1088/1748-9326/ae2697)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
