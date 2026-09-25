---
layout: default
title: N2 emissions from denitrification in surface waters
parent: Surface Water (HY.SW)
nav_order: 1
---

# N2 emissions from denitrification in surface waters

<iframe src="../output_files/plots/HY_SW_AT_AT_Emissions_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
N2 is taken from data on N retention in surface waters supplied by NIVA, produced in the TEOTIL3 model Sample et al. (2024)<!--cite:sample_teotil3_2024-->, by assuming that all N retained in SW is lost to denitrification, with an assumed fraction 1 % as N2O and the rest as N2. For years prior to 2013, we have used a retention rate of 7 % which is the typical value from the NIVA data and calculated the denitrification amount as 0.07/(1-0.07)* **HY.SW-HY.CW-Inflow to coastal waters-Nmix**, which for those years is based on bias-corrected TEOTIL2 results (see that flow). TEOTIL3 has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
