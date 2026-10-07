---
layout: default
title: Surface water N2O emissions
parent: Surface Water (HY.SW)
nav_order: 2
---

# Surface water N2O emissions

<iframe src="../output_files/plots/HY_SW_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
Uses data on N retention in surface waters supplied by NIVA, produced in the TEOTIL3 model Sample et al. (2024)<!--cite:sample_teotil3_2024-->, and assuming that all N retained in SW is lost to denitrification, with an assumed fraction 1 % as N2O and the rest as N2. For years prior to 2013, retention is calculated from **HY.SW-HY.CW-Inflow to coastal waters-Nmix** with the TEOTIL3 ratio between retention and diffuse inputs to the coast, as for the N2 flow, with the N2O fraction taken from the resulting denitrification amount. For those years the inflow is based on bias-corrected TEOTIL2 results (see that flow). TEOTIL3 has not been updated for 2024 at the time of writing; the 2024 value is a flat carry-forward of 2023, with additional uncertainty (±50%) applied to reflect that it is not a real, independently observed value.

**How the numbers are derived**

- 1% (lognormal, 95% interval 0.05–20%) of the N retained in lakes and rivers, calculated as for HY.SW-AT.AT-Emissions-N2.
- 2024 is a flat carry-forward of 2023 until TEOTIL3 is updated.

**Interpretation**

- The flow is about 0.13–0.16 kt N per year, with a large uncertainty from the N2O share of denitrification.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Sample, J. E., Jackson-Blake, L., Vogelsang, C., & Kaste, Ø. (2024). *TEOTIL3: En modell for beregning av kildebaserte tilførsler via elver og direktetilførsler til kyst*.
