---
layout: default
title: Other Land Leaching
parent: Other Land (FS.OL)
nav_order: 2
---

# Other Land Leaching

<iframe src="../output_files/plots/FS_OL_HY_SW_Leaching_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
From 2013 onward, found in data supplied by NIVA, produced in the TEOTIL3 model (Sample et al., 2024)<!--cite:sample_teotil3_2024-->, using TEOTIL3's «upland» category (mountain, heath and wetland areas, i.e. other land including WL).

For 1990–2012, we use the natural diffuse loss from TEOTIL2 model results from NIVA's public repository (NIVANorge/teotil2 on GitHub, https://github.com/NIVANorge/teotil2, commit bf3c380), summed to national totals over the outlets of the main river basins 001–247 and 315 (inputs to the coast, after retention in lakes and rivers). This category covers forest, mountain, lakes and the background part of agricultural land, and is not split by land type. It is bias-corrected to TEOTIL3 by multiplying with the ratio between the TEOTIL3 and TEOTIL2 means over the years both models cover (2013–2022). This is the method NIVA uses to extend TEOTIL3 back to 1990 in the annual reports Sample (2025)<!--cite:sample_kildefordelte_2025-->, but applied here to the categories the model uses, and without the published 1990–1995 values; here the TEOTIL2 natural diffuse loss is compared with TEOTIL3 wood + upland, which gives a factor of 1.02. Other land is assigned a fraction 0.41 of the scaled value, which is the share of upland in wood + upland in TEOTIL3 over 2013–2023 (0.40–0.44). The forest flow (**FS.FO-HY.SW-Leaching-Nmix**) gets the remaining 0.59.

We do not use the published series for 1990–2012 (Miljødirektoratet's TEOTIL figures and NIVA's annual reports), because for 1990–1995 it contains results from an older TEOTIL version, with 40–50 % higher background loading than the TEOTIL2 results used here, which gives an artificial drop in 1996. All years 1990–2012 used here come from the same TEOTIL2 model run. Results for 1990–1995 are less certain than for later years, because the input data for those years are incomplete (J. Sample, NIVA, pers. comm., September 2026); the gaps are mainly in point sources, which are not used here.

TEOTIL3 has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Sample, J. E. (2025). *Kildefordelte tilførsler av nitrogen og fosfor til norske kystområder i 2023 – tabeller, figurer og kart*.
* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
