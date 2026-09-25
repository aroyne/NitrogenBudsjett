---
layout: default
title: Inflow to coastal waters
parent: Surface Water (HY.SW)
nav_order: 3
---

# Inflow to coastal waters

<iframe src="../output_files/plots/HY_SW_HY_CW_Inflow_to_coastal_waters_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
From 2013 onward, found from data supplied by NIVA, produced in the TEOTIL3 model Sample et al. (2024)<!--cite:sample_teotil3_2024-->. TEOTIL3's total N-to-coast figure includes both aquaculture and treated wastewater discharge, so to avoid double counting with the dedicated aquaculture and wastewater flows, we subtract TEOTIL3's aquaculture component and the flow *PR.WW-HY.CW-Treated wastewater discharge-Nmix* (which already assigns all treated wastewater discharge to CW).

For 1990–2012, we use TEOTIL2 model results from NIVA's public repository (NIVANorge/teotil2 on GitHub, https://github.com/NIVANorge/teotil2, commit bf3c380), summed to national totals over the outlets of the main river basins 001–247 and 315 (inputs to the coast, after retention in lakes and rivers). Four categories are used: natural diffuse loss (background), agriculture, urban areas and industry; aquaculture and wastewater are left out, as they have their own flows. Each category is bias-corrected to TEOTIL3 by multiplying with the ratio between the TEOTIL3 and TEOTIL2 means over the years both models cover (2013–2022). This is the method NIVA uses to extend TEOTIL3 back to 1990 in the annual reports Sample (2025)<!--cite:sample_kildefordelte_2025-->, but applied here to the categories the model uses, and without the published 1990–1995 values. The factors are 1.17 for background (compared with TEOTIL3 forest, mountain, lake and agricultural background), 1.83 for agriculture, 19.4 for urban areas (TEOTIL2 has a much lower and constant urban loading) and 0.89 for industry. Since the TEOTIL3 source data are inputs to surface water before retention, the sum of the four scaled categories is multiplied by 0.88, the share of these inputs that reaches the coast in TEOTIL3 over the same years. The factors are calculated from the data each time the model runs.

We do not use the published series for 1990–2012 (Miljødirektoratet's TEOTIL figures and NIVA's annual reports), because for 1990–1995 it contains results from an older TEOTIL version, with 40–50 % higher background loading than the TEOTIL2 results used here, which gives an artificial drop in 1996. All years 1990–2012 used here come from the same TEOTIL2 model run. Results for 1990–1995 are less certain than for later years, because the input data for those years are incomplete (J. Sample, NIVA, pers. comm., September 2026); the gaps are mainly in point sources, which are not used here. TEOTIL2 assumes a fixed long-term mean runoff for agricultural land, so the agricultural part does not vary with runoff between years before 2013, unlike the TEOTIL3 data used from 2013. The step in TEOTIL2's agricultural loading in 2001 comes from the model's input data and is kept.

TEOTIL3 has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Sample, J. E. (2025). *Kildefordelte tilførsler av nitrogen og fosfor til norske kystområder i 2023 – tabeller, figurer og kart*.
* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
