---
layout: default
title: Sewage Sludge to Landfill
parent: Wastewater (PR.WW)
nav_order: 6
---

# Sewage Sludge to Landfill

<iframe src="../output_files/plots/PR_WW_PR_SO_Sewage_sludge_landfill_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **PR.WW-PR.SO-Sewage sludge landfill-Nmix** is the N in sewage sludge that is landfilled or used as top cover on landfills (Schäppi et al., 2025<!--cite:schappi_annexes_2025-->).

#### Data sources

- SSB's statistics on sewage sludge ([table 05279](https://www.ssb.no/statbank/table/05279) “Avløpsslam, etter slamdisponering, statistikkvariabel, år og region”) give the amount of sludge (tonnes dry matter) from municipal wastewater treatment plants by disposal, based on the plants' reporting through KOSTRA. For 1993–2001 the amounts and shares by disposal are taken from SSB's Naturressurser og miljø series.
- [NIBIO](https://www.nibio.no/tema/jord/organisk-avfall-som-gjodsel/avlopsslam) gives 20–40 kg total N per tonne dry matter for Norwegian sewage sludge. There are no public Norwegian data on N in sludge from different treatment processes (Frøseth et al., 2025)<!--cite:froseth_nitrogenkilder_2025-->.

#### Assumptions

- 1990–1992 are the mean of 1993–1995.
- The dry matter is multiplied by an N content of 3% (range 2–4%), the middle of the NIBIO range.

#### Interpretations

- The flow is about 0.2–0.7 kt N per year.
- For comparison, Tables 54 and 55 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025--> give 2.6–3.7% N in dry matter for dewatered, digested and composted sludge in the JRC models (Huygens et al., 2022) and a median of 4.9% in German analyses (Sichler et al., 2022).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-05). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of sewage sludge | N content of waste | 0.02–0.04, normal | 29% | 84% | 1.00 | 1.00 | [Sewage Sludge Fertilizer to Ag](../processing_of_residues_pool/flow_PR_WW_AG_SM_Sewage_sludge_fertilizer_Nmix.html), [Sewage Sludge Fertilizer to HS](../processing_of_residues_pool/flow_PR_WW_HS_HS_Sewage_sludge_fertilizer_Nmix.html) |
| Sewage sludge disposal (SSB 05279) | Survey or self-reported data | ±15 %, normal, drawn per year | – | 16% | – | 1.00 | [Sewage Sludge Fertilizer to Ag](../processing_of_residues_pool/flow_PR_WW_AG_SM_Sewage_sludge_fertilizer_Nmix.html), [Sewage Sludge Fertilizer to HS](../processing_of_residues_pool/flow_PR_WW_HS_HS_Sewage_sludge_fertilizer_Nmix.html) |
| Sewage sludge disposal before 1993 (SSB) | Assumption | ±50 %, triangular | 66% | – | 1.00 | – | none |
| Held constant or averaged (sewage sludge:1993-1995) | Gap filling: held constant or averaged | ±15–25 %, lognormal, grows with distance to known year | 5% | – | 1.00 | – | [Sewage Sludge Fertilizer to Ag](../processing_of_residues_pool/flow_PR_WW_AG_SM_Sewage_sludge_fertilizer_Nmix.html), [Sewage Sludge Fertilizer to HS](../processing_of_residues_pool/flow_PR_WW_HS_HS_Sewage_sludge_fertilizer_Nmix.html) |

### References

* Frøseth, R. B., Kristoffersen, A. Ø., Bechmann, M., & Brod, E. (2025). *Nitrogenkilder og -strømmer i jordbruket* (NIBIO Rapport 11(124)). NIBIO. [landbruksdirektoratet.no](https://www.landbruksdirektoratet.no/nb/filarkiv/prosjektresultater/NIBIO-delrapport%201%20-%20Nitrogenkilder%20-%20og%20str%C3%B8mmer%20i%20jordbruket.pdf/_/attachment/inline/5986a77d-5097-4b6c-838f-27bc6ebad941:917ae8899116a72498026f7ab9a6ca50f03acc7c/NIBIO-delrapport%201%20-%20Nitrogenkilder%20-%20og%20str%C3%B8mmer%20i%20jordbruket.pdf)
* Schäppi, B., Reutimann, J., Bogler, S., Ehrler, A., & Fehrenbach, H. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets”* (TEXTE 05/2025). Umweltbundesamt. [https://doi.org/10.60810/openumwelt-7845](https://doi.org/10.60810/openumwelt-7845)
