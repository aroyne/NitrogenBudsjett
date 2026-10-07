---
layout: default
title: Fuel export
parent: Energy conversion (EF.EC)
nav_order: 7
---

# Fuel export

<iframe src="../output_files/plots/EF_EC_RW_RW_Fuel_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
EF.EC-RW.RW-Fuel export-Nmix is the nitrogen content in exported fuels. We use trade data in SSB table 08801 to account for all petroleum products excluding those assumed to be used in the transport sector. Crude oil (HS code 2709) dominates this flow, accounting for over 99% of its N content: it is assigned an average N content of 0.25% (range 0.02-1.5%) from Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, giving a total flow on the order of 150-210 ktN/year (2013-2023) - broadly consistent with the Norway-specific crude oil N content and export estimate of Hohmann-Marriott (2025)<!--cite:hohmann-marriott_nitrogen_2025-->. Natural gas exports (HS code 2711) are not captured here: they are a comparably large export by mass and energy content, but natural gas itself has negligible nitrogen content and is therefore not expected to materially affect the national N budget.

**How the numbers are derived**

- Export quantities (kg) by HS commodity code are taken from [SSB table 08801](https://www.ssb.no/statbank/table/08801) and multiplied by an N content per fuel type (Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)): crude oil (HS 2709) 0.25%, residual fuel oil 0.45%, gas/diesel oil 0.0133%, kerosene 0.1%, other oils 0.0375%, bitumen 0.7%, coal and coke 1.0–1.85% and peat 0.2%; gasoline, naphtha and natural gas condensate are included with zero N (Table 15: gasoline 0, naphtha and NGL not specified).
- The selection of HS codes and fuel types is defined in the trade mapping sheet of N_parameters.xlsx.
- Export quantities in the trade statistics are registered by customs and are therefore observed rather than modelled; the uncertainty of the flow lies mainly in the N content of crude oil, which varies between fields (0.02–1.5%).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Hohmann-Marriott, M. F. (2025). A Nitrogen budget for Norway analysis of Nitrogen flows from societal and natural sources (1961–2020). *PLOS ONE, 20*(2), e0313598. [https://doi.org/10.1371/journal.pone.0313598](https://doi.org/10.1371/journal.pone.0313598)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
