---
layout: default
title: Other Goods Export
parent: Other Producing Industry (MP.OP)
nav_order: 13
---

# Other Goods Export

<iframe src="../output_files/plots/MP_OP_RW_RW_Other_goods_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
**MP.OP-RW.RW-Other goods export-Nmix** is taken from SSB trade data (table 08801) on goods that can be characterized as flowers, chemicals, soap, industrial protein, leather, wood, textiles, and ammonia. Within the plastics and synthetic-textile trade categories, N content is assigned by base polymer rather than a single blended factor: nitrogen-containing polymers (polyamide/nylon, polyurethane, melamine and urea formaldehyde resins, polyacrylonitrile) use the N contents given in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, Table 23, while ordinary commodity plastics and fibres with no nitrogen in their polymer backbone (polyethylene, polypropylene, PVC, polystyrene, polyester, viscose/rayon, cotton) are assigned ~0. The same principle applies to clothing, footwear and other finished textile articles: items explicitly of wool use the protein-fibre N content from Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->, Table 24 (as for silk), items with a leather component use the same N content as hides and skins, and items of cotton or unspecified synthetic/artificial fibre (predominantly polyester, which - like cotton - has no nitrogen in its polymer backbone) default to ~0. Roundwood, fuel wood, chips, sawdust and wood residues (HS 4401 and 4403) are given the N content of stem wood (1.2 g/kg for conifers and 1.4 g/kg for broadleaves, Table 45 in Schäppi et al. (2025)<!--cite:schappi_annexes_2025-->), the same as domestic industrial round wood, while processed wood products use 0.2% (Table 22). Fish waste and by-products (HS 0511) are counted in MP.FP-RW.RW-Feed export-Nmix.

The significant increase from 2018 is due to export of nitric acid, which started that year. Nitric acid is an intermediary in fertilizer production but not counted as fertilizer, so it shows up in this flow.  

**How the numbers are derived**

- Export quantities (kg) by commodity code are taken from SSB's external trade statistics ([table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from the customs declarations for goods crossing the border ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)).
- Each commodity code is assigned a commodity type and an N content in the trade mapping sheet of N_parameters.xlsx, and quantities are multiplied by the N content.

**Interpretation**

- The flow is about 7–10 kt N per year until 2013, 11–12 kt N in 2014–2017 and 20–33 kt N from 2018.
- The step in 2018–2019 comes from exports of nitric acid, and the rise from 2013 from roundwood exports, which grew from about 0.5 to 3–4 million tonnes per year after several Norwegian pulp and paper mills closed.
- In 2024 roundwood, chips and wood residues (6.4 kt N) and nitric acid (7.7 kt N) are the largest items, followed by processed wood products (2.7 kt N), hides and leather (1.0 kt N), wool (0.8 kt N) and detergents (0.75 kt N).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### References

* Schäppi, B., Reutimann, J., Bogler, S., & Ehrler, A. (2025). *Detailed Annexes to ECE/EB.AIR/119 – “Guidance document on national nitrogen budgets*. [https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)
