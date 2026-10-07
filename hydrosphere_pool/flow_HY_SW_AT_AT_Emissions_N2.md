---
layout: default
title: N2 emissions from denitrification in surface waters
parent: Surface Water (HY.SW)
nav_order: 1
---

# N2 emissions from denitrification in surface waters

<iframe src="../output_files/plots/HY_SW_AT_AT_Emissions_N2.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
N2 is taken from data on N retention in surface waters supplied by NIVA, produced in the TEOTIL3 model Sample et al. (2024)<!--cite:sample_teotil3_2024-->, by assuming that all N retained in SW is lost to denitrification, with an assumed fraction 1 % as N2O and the rest as N2. For years prior to 2013, retention is calculated as **HY.SW-HY.CW-Inflow to coastal waters-Nmix** (based on bias-corrected TEOTIL2 results for those years, see that flow) multiplied by the ratio between retention and the diffuse inputs to the coast in TEOTIL3 (0.12 on average for 2013–2023, calculated from the data each time the model runs). The diffuse inputs are TEOTIL3's total to the coast minus aquaculture and wastewater, which are discharged directly to the sea and hardly pass lakes and rivers; retention in TEOTIL3 is about 6.5 % of all inputs including these sources, but 12 % of the diffuse inputs that reach the coast. TEOTIL3 has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.

**How the numbers are derived**

- From 2013, the N retained in lakes and rivers in [TEOTIL3](https://github.com/NIVANorge/teotil3) is assumed to be denitrified, 99% to N2 and 1% to N2O (lognormal, 95% interval 0.05–20%).
- For 1990–2012, retention is HY.SW-HY.CW-Inflow to coastal waters-Nmix times TEOTIL3's mean ratio between retention and the diffuse inputs to the coast (0.12).
- 2024 is a flat carry-forward of 2023 until TEOTIL3 is updated.

**Interpretation**

- The flow is about 12–15 kt N per year, following the inflow to coastal waters before 2013 and TEOTIL3's retention from 2013.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
