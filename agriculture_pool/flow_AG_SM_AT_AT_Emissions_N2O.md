---
layout: default
title: N2O emissions from denitrification
parent: Soil Management (AG.SM)
nav_order: 3
---

# N2O emissions from denitrification

<iframe src="../output_files/plots/AG_SM_AT_AT_Emissions_N2O.html" width="100%" height="400px" frameborder="0" scrolling="no"></iframe>

### Flow Description
<!-- MANUAL:FLOW_DESCRIPTION:START -->
N2O emissions are taken from UNFCCC Common reporting tables, Table 3.

**How the numbers are derived.** The flow is the N2O from "3.D. Agricultural soils" in CRT Table 3 of the national greenhouse gas inventory: direct N2O from mineral fertilizer, manure, sewage sludge, grazing animals, crop residues, mineralisation and cultivated organic soils, and indirect N2O from N that volatilises or leaches. It is calculated as the N applied by each source multiplied by IPCC emission factors ([Miljødirektoratet, NID 2026](https://www.miljodirektoratet.no/publikasjoner/2026/mars-2026/greenhouse-gas-emissions-1990-2024-national-inventory-document/)). N2O is converted to N with the factor 28/44. The inventory counts all manure deposited by grazing animals as input to managed soils, including the share deposited on utmark (unmanaged land), which this model does not count as input to AG.SM (see AG.MM-AG.SM-Manure application-Nmix). The utmark share (47%, range 38–56%) of the losses from grazing manure is therefore removed from this flow; these losses are part of the runoff from upland areas measured by TEOTIL3 (FS.OL). The removed N2O is the utmark share of the direct N2O from grazing manure (3.D.1.c) plus the indirect N2O from its volatilisation and leaching, calculated with the fractions and implied emission factors in CRT Table 3.D (about 0.1 kt N per year).

**Interpretation.** The flow is about 4.0–4.6 kt N per year, with a slight decrease since 1990. The uncertainty is large (CV about 40%), mainly from the emission factors.
<!-- MANUAL:FLOW_DESCRIPTION:END -->
