---
layout: default
title: Urban Overland Flow
parent: 6. Humans and settlements (HS)
nav_order: 3
---

# Urban Overland Flow

<iframe src="../output_files/plots/HS_HS_HY_SW_Overland_flow_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **HS.HS-HY.SW-Overland flow-Nmix** is runoff of N from urban (built-up) areas to surface water. The flow has been added to account for urban runoff.
- Some of this may actually end up directly in coastal water (CW), but we have not been able to separate the two.

#### Data sources

- From 2013, the 'urban' component of the TEOTIL3 model outputs from NIVA (Sample et al., 2024)<!--cite:sample_teotil3_2024-->. TEOTIL3 calculates the N load from urban areas as the area of built-up land in each catchment (from land-cover maps) times an export coefficient per area, so the year-to-year variation mainly follows changes in area and runoff.
- For 1990–2012, the urban loading from TEOTIL2 model results in NIVA's public repository (NIVANorge/teotil2 on GitHub, https://github.com/NIVANorge/teotil2, commit bf3c380), summed to national totals over the outlets of the main river basins 001–247 and 315 (inputs to the coast, after retention in lakes and rivers). TEOTIL2 uses the same urban value in every year.

#### Assumptions

- The TEOTIL2 values are bias-corrected to TEOTIL3 by multiplying with the ratio between the TEOTIL3 and TEOTIL2 means over the years both models cover (2013–2022). This is the method NIVA uses to extend TEOTIL3 back to 1990 in the annual reports Sample (2025)<!--cite:sample_kildefordelte_2025-->, but applied here to the categories the model uses, and without the published 1990–1995 values. The factor for urban areas is 19.4, because TEOTIL2 estimates much lower urban loading than TEOTIL3.
- Since TEOTIL2's urban value is constant, the resulting series for 1990–2012 is constant at the TEOTIL3 average level and carries no information about the trend before 2013. An additional uncertainty (±50%) is applied to these years to reflect this.
- TEOTIL3's urban loading is the input to surface water before retention, and is used directly; the retention in lakes and rivers is counted in HY.SW-AT.AT-Emissions-N2 and -N2O.
- TEOTIL3 has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.

#### Interpretations and comparisons

- The flow is about 6–8.5 kt N per year since 2013, with the highest value in 2020, a wet year.
- The values for 1990–2012 are constant and do not show the growth of urban areas over the period.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Sample, J. E. (2025). *Kildefordelte tilførsler av nitrogen og fosfor til norske kystområder i 2023 – tabeller, figurer og kart*.
* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
