---
layout: default
title: Urban Overland Flow
parent: 6. Humans and settlements (HS)
nav_order: 3
---

# Urban Overland Flow

<iframe src="../output_files/plots/HS_HS_HY_SW_Overland_flow_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**HS.HS-HY.SW-Overland flow-Nmix** is a flow that has been added to account for runoff from urban (built-up) areas. Some of this may actually end up directly in CW, but we have not been able to separate the two. From 2013 onward, we use the 'urban' component of the TEOTIL3 model outputs from NIVA (Sample et al., 2024)<!--cite:sample_teotil3_2024-->.

For 1990–2012, we use the urban loading from TEOTIL2 model results from NIVA's public repository (NIVANorge/teotil2 on GitHub, https://github.com/NIVANorge/teotil2, commit bf3c380), summed to national totals over the outlets of the main river basins 001–247 and 315 (inputs to the coast, after retention in lakes and rivers). It is bias-corrected to TEOTIL3 by multiplying with the ratio between the TEOTIL3 and TEOTIL2 means over the years both models cover (2013–2022). This is the method NIVA uses to extend TEOTIL3 back to 1990 in the annual reports Sample (2025)<!--cite:sample_kildefordelte_2025-->, but applied here to the categories the model uses, and without the published 1990–1995 values; the factor for urban areas is 19.4, because TEOTIL2 estimates much lower urban loading than TEOTIL3. TEOTIL2 uses the same urban value in every year, so the resulting series is constant at the TEOTIL3 average level and carries no information about the trend before 2013. An additional uncertainty (±50%) is applied to these years to reflect this.

In both periods, a retention fraction is applied to account for N retained before reaching surface water (5% most likely, ranging 0-20%, following TEOTIL3). TEOTIL3 has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Sample, J. E. (2025). *Kildefordelte tilførsler av nitrogen og fosfor til norske kystområder i 2023 – tabeller, figurer og kart*.
* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
