---
layout: default
title: Food Export
parent: Food and Feed Processing (MP.FP)
nav_order: 9
---

# Food Export

<iframe src="../output_files/plots/MP_FP_RW_RW_Food_export_Nmix.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Flow description

- **MP.FP-RW.RW-Food export-Nmix** is exported food: cereals and plants, meat, fish, dairy products and eggs, and other food.

#### Data sources

- Export quantities (kg) by commodity code from SSB's external trade statistics ([SSB table 08801](https://www.ssb.no/statbank/table/08801)), which are compiled from the customs declarations for goods crossing the border ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)).
- Fish caught by Norwegian vessels outside the Norwegian customs area and landed directly abroad is also included as export, with data from Fiskeridirektoratet from July 2010 to 2023 and from customs declarations from 2024 ([Utenrikshandel med varer](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer)).
- Catch landed directly abroad by Norwegian vessels, by landing country, from Fiskeridirektoratet table F.06.002 (catch by Norwegian vessels by landing nation, species and gear, 2000 onward; [statistics bank](https://statistikkbanken.fiskeridir.no/PxWeb/pxweb/no/Fiskeridirektoratet/Fiskeridirektoratet__F_Fiskeri__F_06_Fangst/)).

#### Assumptions

- Each commodity code is assigned an N content, mostly from Table 21 in [Schäppi et al. 2025, Annexes](https://www.clrtap-tfrn.org/sites/default/files/2025-05/Annexes%20to%20the%20Guidance%20Document%20on%20NNB.pdf)<!--cite:schappi_annexes_2025--> (N contents of food products), and quantities are multiplied by it.
- Catch landed directly abroad that is not in the export statistics is added to the flow, with the N content of fish (2.8%), since it is counted in the catch flows into MP.FP but leaves the country directly:
  - Antarctic krill, all years: it is landed in Uruguay and does not appear as export.
  - Other fish 2000–2009: all landings abroad, which are missing from the exports before 2010.
  - Other fish 2010–2023: nothing; the landings abroad are in the exports.
  - Other fish 2024: per landing country, the landings minus the exports of whole fresh and frozen fish (HS 0302/0303) and industrial fish not fit for human consumption (HS 0511.9111) to that country, after subtracting the exports to that country in 2023 that were not landings (assumed unchanged from 2023). From 2024 the direct landings are recorded as industrial fish, and almost all of them are in the exports (Iceland: 65.2 kt landed, 24.7 + 40.5 kt exported).
  - Other fish 1990–1999 (no data by landing country): the 2000–2009 ratio between landings abroad and the total wild fish catch, times the catch, with extra uncertainty for the extrapolation.
- Klippfisk (salted and dried fish) and tørrfisk (dried fish) have their own N contents, 10.3% and 12.6%, from the protein content in the Norwegian food composition table ([Matvaretabellen](https://www.matvaretabellen.no/klippfisk-saltet-og-torket/): 64.3 and 78.5 g protein per 100 g; N = protein/6.25). Other fish products, including salted but not dried fish, use 2.8% N.

#### Interpretations

- Fish and fish products (fresh, frozen and processed, including farmed salmon) make up about 98% of the flow, 82 of 84 kt N in 2024 (73 kt N in the export statistics and 9 kt N added landings abroad, almost all krill), of which klippfisk is 8.2 kt N and tørrfisk 0.4 kt N.
- The flow rises from 30 kt N in 1990 to 75–92 kt N from 2010 and has been roughly stable since. The increase from about 60 kt N in 2006 to 80 kt N in 2009 comes from exports of fresh fish (mainly farmed salmon, HS 0302, +170 kt from 2006 to 2009) and frozen fish (HS 0303, +440 kt). After 2010 the growth in farmed fish has been offset by lower wild catches (see HY.AC-MP.FP-Coastal fish and seafood-Nmix and HY.CW-MP.FP-Fish (wild catch)-Nmix).
- Exports of meat and of cheese are each below 0.5 kt N.
- The added landings abroad are 4.5–8.5 kt N per year in 1990–1999, 6–12 kt N in 2000–2009 and 2.6–9 kt N (almost only krill) in 2010–2024. Without them, this N would stay in MP.FP and add to its surplus.
- The 6 kt of fish and crustacean meal exported to Uruguay in 2024 (about 0.6 kt N, in MP.FP-RW.RW-Feed export-Nmix) is probably krill meal, so up to 0.6 kt N of krill may be counted twice that year.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

### Uncertainty

Sources that contribute at least 2% of the variance of this flow in one of the periods (computed 2026-11-04). How the table is computed is explained under [Data and uncertainties](../index.html#data-and-uncertainties) on the front page.

| Source | Type | Uncertainty (95 %) | Share of variance 1990–1994 | Share of variance 2020–2024 | Elasticity 1990–1994 | Elasticity 2020–2024 | Other flows affected |
|---|---|---|---|---|---|---|---|
| N content of traded goods: fish fresh frozen | N content of traded goods | ±20 %, normal | 67% | 90% | 0.60 | 0.78 | [Feed Export](../materials_and_products_pool/flow_MP_FP_RW_RW_Feed_export_Nmix.html), [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| Traded quantities (SSB 08801) (kjøtt/fisk/meieri/egg) | Registered data | ±5 %, normal, drawn per year | 8% | 8% | 0.82 | 0.90 | [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| N content of traded goods: dried salted fish | N content of traded goods | ±20 %, normal | 4% | 1% | 0.14 | 0.10 | [Food Import](../rest_of_the_world_pool/flow_RW_RW_MP_FP_Food_import_Nmix.html) |
| Extrapolation (direct landings <2000) | Gap filling: extrapolation | ±40–50 %, lognormal, grows with distance to known year | 19% | – | 0.16 | – | none |
