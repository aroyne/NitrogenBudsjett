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

- **AT.AT-FS.OL-N2 fixation-N2** is biological N<sub>2</sub> fixation on other land, which in our model includes what Moldan et al. (2025)<!--cite:moldan_where_2025--> treat as a separate wetland (WL) compartment.

#### Data sources

- N<sub>2</sub> fixation rates from Table 62 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> (Reddy and DeLaune, 2008): 11 (0–22) kg N/ha for peat bogs, 29 (0–58) kg N/ha for freshwater marshes and 4 (0–7) kg N/ha for mud flats.
- Land type areas from the CORINE land cover inventory (European Environment Agency, 2019<!--cite:european_environment_agency_corine_2019-->): 2.10 million ha peat bogs, 296 ha inland marshes and 18 272 ha intertidal flats.

#### Assumptions

- The mud-flat rate is used for CORINE intertidal flats.

#### Interpretations

- The flow is constant at about 23 kt N per year<!--mean:AT.AT-FS.OL-N2 fixation-N2:1984-2025-->; almost all comes from peat bogs, while intertidal flats and freshwater marshes contribute less than 0.1 kt N.
- In the Swedish NNB (Moldan et al., 2025)<!--cite:moldan_where_2025-->, N<sub>2</sub> fixation in the OL compartment was considered negligible. Our total is therefore not directly comparable to that estimate, but corresponds closely to their separate WL estimate of about 30 kt N (Jutterström et al., 2020)<!--cite:jutterstrom_swedish_2020-->.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N fixation rate in peat bogs | Parameter | 0–22 (min–max), triangular | 94% | 94% | 1.00 | 1.00 | none |
| Peat bog area | Parameter | ±20 %, normal | 6% | 6% | 1.00 | 1.00 | none |

### References

* European Environment Agency (2019). *CORINE Land cover inventory*. [eea.europa.eu](https://www.eea.europa.eu/en/datahub/datahubitem-view/a5144888-ee2a-4e5d-a7b0-2bbf21656348)
* Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation* (C 549). IVL Swedish Environmental Research Institute.
* Moldan, F., Stadmark, J., Jutterström, S., & Ljunggren, J. (2025). Where does Sweden’s nitrogen go? Building a comprehensive national nitrogen budget. *Environmental Research Letters, 20*(12), 124068. [https://doi.org/10.1088/1748-9326/ae2697](https://doi.org/10.1088/1748-9326/ae2697)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
