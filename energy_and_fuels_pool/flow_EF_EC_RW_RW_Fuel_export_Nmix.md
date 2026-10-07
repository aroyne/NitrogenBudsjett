---
layout: default
title: Fuel export
parent: Energy conversion (EF.EC)
nav_order: 7
---

# Fuel export

<iframe src="../output_files/plots/EF_EC_RW_RW_Fuel_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **EF.EC-RW.RW-Fuel export-Nmix** is the nitrogen in exported fuels: all petroleum products and other fuels except those assumed to be used in the transport sector.
- Natural gas exports (HS code 2711) are not captured here: they are a comparably large export by mass and energy content, but natural gas itself has negligible nitrogen content and is therefore not expected to materially affect the national N budget.

#### Data sources

- Export quantities (kg) by HS commodity code from [SSB table 08801](https://www.ssb.no/statbank/table/08801). Export quantities in the trade statistics are registered by customs and are therefore observed rather than modelled.
- N contents per fuel type from Table 15 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- N contents: crude oil (HS 2709) 0.25% (lognormal with this median and 1.5% as the upper end of the 95% interval), residual fuel oil 0.45%, gas/diesel oil 0.0133%, kerosene 0.1%, other oils 0.0375%, bitumen 0.7%, coal and coke 1.0–1.85% and peat 0.2%; gasoline, naphtha and natural gas condensate are included with zero N (Table 15: gasoline 0, naphtha and NGL not specified).
- The selection of HS codes and fuel types is defined in the trade mapping sheet of N_parameters.xlsx.

#### Interpretations and comparisons

- Crude oil dominates the flow, accounting for over 99% of its N content, giving a total on the order of 160–220 kt N per year (2013–2023).
- The uncertainty of the flow lies mainly in the N content of crude oil, which varies between fields (0.02–1.5%).
- The flow is broadly consistent with the Norway-specific crude oil N content and export estimate of Hohmann-Marriott (2025)<!--cite:hohmann-marriott_nitrogen_2025-->.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Hohmann-Marriott, M. F. (2025). A Nitrogen budget for Norway analysis of Nitrogen flows from societal and natural sources (1961–2020). *PLOS ONE, 20*(2), e0313598. [https://doi.org/10.1371/journal.pone.0313598](https://doi.org/10.1371/journal.pone.0313598)
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
