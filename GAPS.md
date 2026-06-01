# Gaps — Facts to Verify Manually

This file lists every volatile fact the catalog could not ground in a source, plus every entry whose overall verification confidence is below `high`. It is generated from the entry data by `scripts/gaps.py`. Use it for targeted manual checks. Nothing here was guessed: a fact is either marked with the sentinel `unstated — needs direct verification` or flagged in an entry's `verification_confidence`.

## Summary

- Total entries: **89**
- Overall confidence: **62 high**, **27 medium**, **0 low**
- Fields carrying the explicit `unstated` sentinel: **41**

## Per-entry unverified facts

Only entries with at least one unverified/unstated fact, or non-high confidence, are listed.


### architecture-description-langs

- **Cheddar** (`cheddar-aadl-scheduling`) — confidence: medium
  - _note:_ Latest release on the official site is 3.3 (2023); no newer release observed, so judged maintained rather than highly active. Tool listed alongside AADL/OSATE as its primary ADL input.

### computing-dsm

- **DesignStructureMatrix.jl** (`designstructurematrix-jl`) — confidence: medium
  - _note:_ Latest release 0.3.0 (2022), judged dormant. Computes clustering and sequencing (not change propagation).
- **DSM Clustering Algorithm (Thebeau)** (`dsmclustering-thebeau`) — confidence: medium — unstated: maintenance_status.latest_version
  - _note:_ No tagged releases; latest commit 2023-01-16, judged dormant. Implements the well-known Thebeau (2001) MIT clustering algorithm.

### des-abm

- **AnyLogic** (`anylogic`) — confidence: medium — also flagged: latest_version, latest_release_date
  - _note:_ Version 8.9.8 (2026-02-26) reported via web search of AnyLogic pages; the downloads page returned HTTP 403 and was not directly fetched, so the exact current build should be confirmed on the vendor site.

### equation-based-physical

- **Dymola** (`dymola`) — confidence: medium — unstated: license, maintenance_status.latest_version, maintenance_status.latest_release_date
  - _note:_ Vendor page does not publish version numbers or license terms; marked unstated per rules.
- **GT-SUITE** (`gt-suite`) — confidence: medium — unstated: license, maintenance_status.latest_version, maintenance_status.latest_release_date
  - _note:_ Vendor page omits version/license; marked unstated.
- **MapleSim** (`maplesim`) — confidence: medium — unstated: license, maintenance_status.latest_version, maintenance_status.latest_release_date
  - _note:_ Vendor page omits version/license; marked unstated.
- **OpenModelica** (`openmodelica`) — confidence: high — also flagged: license
  - _note:_ License dual-scheme (OSMC-PL/GPL) stated on project pages but exact SPDX not directly fetched this session.
- **Simcenter Amesim** (`simcenter-amesim`) — confidence: medium — unstated: license, maintenance_status.latest_version, maintenance_status.latest_release_date
  - _note:_ Vendor page omits version/license; marked unstated.

### executable-mbse

- **Open-MBEE Thirty Meter Telescope SysML Model** (`openmbee-tmt-sysml-model`) — confidence: medium — unstated: maintenance_status.latest_version
  - _note:_ No tagged release version; latest activity is a 2023 Cameo migration, so judged dormant. Requires commercial modeling tool to execute.

### heterogeneous-digital-twin

- **FMI / FMU Standard** (`fmi-standard`) — confidence: high — unstated: maintenance_status.latest_release_date
  - _note:_ fmi-standard.org confirms current spec 3.0.2 but does not state the 3.0.2 release date on the fetched page.
- **Ptolemy II** (`ptolemy-ii`) — confidence: high — unstated: license
  - _note:_ License (BSD-style Ptolemy license) not directly fetched this session; latest release 11.0.1 (June 2018) confirmed, repo shows only maintenance commits in 2025 → dormant.

### infrastructure-networks

- **SWMM** (`swmm`) — confidence: medium — unstated: maintenance_status.latest_release_date — also flagged: latest_version
  - _note:_ EPA SWMM is documented at version 5.2.x (5.2.3 referenced); exact current build number and release date on the EPA/GitHub repo were not pinned this session.
- **WNTR** (`wntr`) — confidence: high — unstated: maintenance_status.latest_release_date
  - _note:_ PyPI JSON confirmed latest version 1.4.0 and Revised BSD license; the precise release date for 1.4.0 was not returned in the fetched metadata.

### mathworks-mbd

- **Highway Lane Following** (`adas-highway-lane-following`) — confidence: medium — unstated: scale.element_count
- **NASA HL-20 Lifting Body Airframe** (`aeroblks-hl20-airframe`) — confidence: medium — unstated: scale.element_count
- **Microgrid Design with Simscape (File Exchange)** (`fex-microgrid-design-simscape`) — confidence: medium — unstated: scale.element_count — also flagged: outputs_you_can_observe
  - _note:_ License text read directly from GitHub (master/License.md) — it is a BSD-form license with a MathWorks-products-only restriction, not unrestricted BSD-3-Clause. Some output signals generalized.
- **Vehicle Dynamics, 14 DOF Model in Simscape Multibody (File Exchange)** (`fex-vehicle-dynamics-14dof`) — confidence: medium — also flagged: scale.element_count
  - _note:_ License text read directly from GitHub (master/LICENSE.md) — BSD-form with MathWorks-products-only restriction, not unrestricted BSD-3-Clause.
- **Field-Oriented Control of PMSM Using Quadrature Encoder** (`mcb-pmsm-foc-qep`) — confidence: medium — unstated: scale.element_count
- **HEV P1 Reference Application (Powertrain Blockset)** (`powertrain-hev-p1`) — confidence: medium — unstated: scale.element_count
- **HEV P2 Reference Application (Powertrain Blockset)** (`powertrain-hev-p2`) — confidence: medium — unstated: scale.element_count
- **Use Model-Based Design to Build a Battery Management System** (`simscape-battery-mbd-bms`) — confidence: medium — unstated: scale.element_count — also flagged: inputs_you_can_change, outputs_you_can_observe
  - _note:_ Cell chemistry (27 Ah NMC) and product list verified on the example page; specific inputs/outputs generalized from Simscape Battery BMS documentation.
- **Model and Control a Manipulator Arm with Robotics and Simscape** (`sm-manipulator-arm-simscape`) — confidence: medium — unstated: scale.element_count
- **Three-Phase Grid-Connected Solar Photovoltaic System** (`sps-three-phase-grid-pv`) — confidence: medium — unstated: scale.element_count

### mdo

- **SUAVE** (`suave`) — confidence: medium
  - _note:_ Last release 2.5.2 (Mar 2022); last repository push Feb 2024 per GitHub API, so judged dormant. RCAIDE is the modernization path; no explicit deprecation notice on the repo.

### parametric-spreadsheets

- **AMSAT/IARU Satellite Link Budget Spreadsheet** (`amsat-iaru-link-budget`) — confidence: high — unstated: license
  - _note:_ URL confirmed to download a real 71 KB Excel (Composite Document) file authored by "jking" with create date 2003; the .xls embedded metadata gives Rev1/2003. Formal license terms ("free for non-commercial use") not in a machine-readable license file.
- **Artemis CubeSat Kit Power Budget Spreadsheet** (`artemis-cubesat-power-budget`) — confidence: medium — unstated: license, maintenance_status.latest_version, maintenance_status.latest_release_date
  - _note:_ The Google Sheets link is published in the open OER textbook chapter; it is view/copy shared (not directly fetched as a file by the verification tool). Version and license are not stated for the sheet itself.
- **GREET Model (Excel)** (`greet-model`) — confidence: medium — unstated: license, maintenance_status.latest_version, maintenance_status.latest_release_date
  - _note:_ greet.es.anl.gov returned HTTP 403 to the automated fetcher (likely a User-Agent block); page exists and is the canonical download. Annual Excel editions (2019-2022) confirmed on DOECode/OSTI; R&D GREET 2024 documented in Argonne publications. Exact current Excel version, release date, and formal license require registration/direct download.

### power-energy

- **OpenDSS (with OpenDSSDirect.py / DSS-Python)** (`opendss`) — confidence: medium — also flagged: latest_version, latest_release_date
  - _note:_ OpenDSS core standalone release version on SourceForge could not be pinned to a precise number; Python wrapper versions are verified via PyPI but the OpenDSSDirect.py wrapper is somewhat behind.
- **OSeMOSYS** (`osemosys`) — confidence: medium — unstated: maintenance_status.latest_release_date — also flagged: latest_version
  - _note:_ GitHub API returned 404 for /releases/latest, indicating no formal tagged release; project activity confirmed via search (repo updated 2025-10-22). License Apache-2.0 confirmed via project description.

### process-chemical

- **ChemSep** (`chemsep`) — confidence: medium — unstated: license, maintenance_status.latest_version, maintenance_status.latest_release_date
  - _note:_ chemsep.org intermittently refused connections during verification; LITE free-download status and 40-component/300-stage limit confirmed via search results and download/info pages, but exact current version and formal license text were not directly fetched.
- **Tennessee Eastman Process (tep2py)** (`tennessee-eastman-tep2py`) — confidence: high — unstated: maintenance_status.latest_version
  - _note:_ Repo has no tagged releases; latest_release_date taken from last push date. Variable counts (41 XMEAS, 12 XMV) cross-confirmed from multiple TE references. Last commit Sept 2021; the underlying TE Fortran model is a stable, long-standing benchmark.

### robotics-multibody

- **Project Chrono** (`project-chrono`) — confidence: high — also flagged: access_link
  - _note:_ GitHub release tag 10.0.0 published 2026-04-07; BSD-3-Clause confirmed via repo. The PyPI package named "pychrono" is an unrelated project; PyChrono module distributed via conda. access_link projectchrono.org not directly fetched.

### systems-biology-sbml

- **Kholodenko1999 EGFR Signaling (BIOMD0000000048)** (`biomodels-kholodenko1999-egfr`) — confidence: medium — unstated: maintenance_status.latest_version, maintenance_status.latest_release_date — also flagged: license, scale.element_count
  - _note:_ Entry confirmed curated and available in SBML L2V1 (with Matlab/Octave exports) via biomodels.org page fetch. Exact species/reaction counts (23/25) are from cited references, not directly read from the SBML; the live page preview showed at least 10 species and 10 reactions before truncation. BioModels curated models are generally CC0 but per-model license should be checked.

## Link resolution

From the most recent `scripts/check_links.py` run: guarded=12, ok=77.

These hosts answered but blocked the scripted request (HTTP 401/403/405/429 — typically vendor/government anti-bot). The pages load in a browser; confirm manually:

- 403 — `adas-highway-lane-following` — https://www.mathworks.com/help/driving/ug/highway-lane-following.html
- 403 — `aeroblks-hl20-airframe` — https://www.mathworks.com/help/aeroblks/nasa-hl-20-lifting-body-airframe.html
- 403 — `fex-microgrid-design-simscape` — https://www.mathworks.com/matlabcentral/fileexchange/123865-microgrid-design-with-simscape
- 403 — `fex-vehicle-dynamics-14dof` — https://www.mathworks.com/matlabcentral/fileexchange/110350-vehicle-dynamics-14-dof-model-in-simscape-multibody
- 403 — `greet-model` — https://greet.es.anl.gov/greet_excel_model
- 403 — `mcb-pmsm-foc-qep` — https://www.mathworks.com/help/mcb/gs/foc-pmsm-using-quadrature-encoder.html
- 403 — `powertrain-hev-p1` — https://www.mathworks.com/help/autoblks/ug/explore-the-hybrid-electric-vehicle-p1-reference-application.html
- 403 — `powertrain-hev-p2` — https://www.mathworks.com/help/autoblks/ug/explore-the-hybrid-electric-vehicle-p2-reference-application.html
- 403 — `simscape-battery-mbd-bms` — https://www.mathworks.com/help/simulink/ug/use-mbd-to-build-bms.html
- 403 — `sldemo-fuelsys` — https://www.mathworks.com/help/simulink/slref/modeling-a-fault-tolerant-fuel-control-system.html
- 403 — `sm-manipulator-arm-simscape` — https://www.mathworks.com/help/robotics/ug/model-and-control-a-manipulator-arm-with-simscape.html
- 403 — `sps-three-phase-grid-pv` — https://www.mathworks.com/help/sps/ug/three-phase-grid-connected-in-pv-system.html

No genuinely dead links were found.
