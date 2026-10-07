---
layout: default
title: Waste to energy (Incineration)
parent: Solid Waste (PR.SO)
nav_order: 5
---

# Waste to energy (Incineration)

<iframe src="../output_files/plots/PR_SO_EF_EC_Waste_to_energy_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**PR.SO-EF.EC-Waste to energy-Nmix** is found from SSB tables 05281 “Avfallsregnskap for Norge (1 000 tonn), etter statistikkvariabel, behandlingsmåte, materialtype og år “ (1995-2011) and 10513 “Avfallsregnskap for Norge (1 000 tonn), etter materialtype, statistikkvariabel, år og behandlingsmåte” (2012-2023), using N content values from Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->.

For years prior to 1995, we use the overall fraction of waste to incineration given in historical records and assume that the overall N content of the waste is equal to the 1995 value. For years with missing data, we interpolate.

**How the numbers are derived**

- SSB's waste accounts ([Avfallsregnskapet](https://www.ssb.no/natur-og-miljo/avfall/statistikk/avfallsregnskapet); tables [05281](https://www.ssb.no/statbank/table/05281) for 1995–2011 and [10513](https://www.ssb.no/statbank/table/10513) from 2012) give the amount of waste by material and treatment method.
- SSB combines municipal reporting of household waste (KOSTRA), surveys of manufacturing companies, the companies' own reporting to Miljødirektoratet, figures from the recycling industry and, where data are missing, estimates based on turnover or number of employees.
- The flow is the waste incinerated (with and without energy recovery) by material, multiplied by an N content per material, mainly from Table 50 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf).
- Sludge incinerated is mainly industrial sludge (sewage sludge delivered to incineration is about 1 kt dry matter per year, SSB table 05279), so the N content of industrial effluent sludges (1.4%, Table 50) is used.
- Table 10513 reports most incinerated residual waste as mixed waste (0.9% N), while table 05281 split the same waste into materials with lower N contents; from 2011 to 2012 the incinerated tonnage rises about 12% but the N per tonne about 30%. The 1995–2011 values are therefore scaled by the ratio of the N per tonne in 2012 to that in 2011, so the series is continuous in N content.
- Before 1995 the flow is the total waste (household and industry) multiplied by the share incinerated in historical SSB records, calibrated so that the same calculation gives the 1995 value.

**Interpretation**

- The flow rises from about 5 kt N in 1990 to 24 kt N in 2011 and 26 kt N in 2012, is 22–25 kt N in 2013–2018 and 19–22 kt N in 2019–2024.
- The rise until 2011 follows the expansion of waste incineration, which became the main treatment for residual waste after the ban on landfilling of biodegradable waste in 2009.
- After the scaling, the change from 2011 to 2012 follows the incinerated tonnage.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
