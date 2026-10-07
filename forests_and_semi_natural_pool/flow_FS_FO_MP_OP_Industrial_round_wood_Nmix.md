---
layout: default
title: Industrial Round Wood
parent: Forests (FS.FO)
nav_order: 5
---

# Industrial Round Wood

<iframe src="../output_files/plots/FS_FO_MP_OP_Industrial_round_wood_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **FS.FO-MP.OP-Industrial round wood-Nmix** is the N in industrial roundwood removed from forests.

#### Data sources

- FAOSTAT's forestry statistics ([Forestry production and trade](https://www.fao.org/faostat/en/#data/FO)) give the removals of industrial roundwood (1000 m³ under bark) for coniferous and non-coniferous trees. They are collected from the countries through the joint FAO/UNECE/Eurostat forest sector questionnaire.
- The values are very close to those reported in SSB table 08979 “Avvirkning for salg (1 000 m³) 1996 – 2024”. We have also compared with data in Eurostat, which gives the total amount of roundwood removed (over or under bark) including use for firewood in households and industry.
- Stem-wood N contents from Table 45 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025-->.

#### Assumptions

- Following the Swedish NBB (Jutterström et al., 2020)<!--cite:jutterstrom_swedish_2020-->, we use an average wood density of 0.45 t/m³ (range 0.32–0.48) for all wood categories.
- Stem-only N contents of 1.2 g/kg for coniferous and 1.4 g/kg for non-coniferous trees (ranges 0.7–1.7 and 0.9–1.9 g/kg), since roundwood removals consist mainly of stem wood, not foliage, branches and roots. Fuel wood also uses the stem value for broadleaves (see FS.FO-EF.OE-Fuel wood for households-Nmix).

#### Interpretations and comparisons

- The flow is about 3.4–6.3 kt N per year. It falls from 5.7 kt N in 1990 to about 3.5–4.5 kt N around 1995–2010 and rises to 6.3 kt N in 2024, following the volume of timber harvested.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Jutterström, S., Stadmark, J., & Moldan, F. (2020). *Swedish National Nitrogen Budget – Forest and semi-natural vegetation*.
* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
