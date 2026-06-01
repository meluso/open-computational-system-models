# Project Brief: A Catalog of Computational System Models

You are building a catalog of **computational system models** that lives in this Git repository and renders to both a static website and narrative prose documents from a single underlying dataset. Work autonomously through this brief to completion. Do not stop to ask me for approval at each stage. Instead, make reasoned decisions, write down your reasoning, test your own work against criteria you define, and leave me a clear account of what you did and what you could not verify.

Commit to Git frequently with descriptive messages, and push to GitHub. Maintain a running `PROGRESS.md` log throughout so I can read your account when I return.

---

## 1. The working definition (the one inclusion test)

A **computational system model** is a representation of an engineered system with many interacting elements (more than twenty-five, which may be grouped into subsystems) that a person can actually run, such that changing inputs or parameters produces observably different outcomes of interest, such as performance characteristics.

This holds for **any user**, not only students. Access can be anything from permissively open source to commercially licensed, including tools people reach through an employer or university license such as MATLAB and Simulink. **Access type is an attribute to record, never a filter.**

Apply one inclusion test: **executability**. An entry qualifies only if a user can vary inputs or parameters and observe changed outputs. Exclude purely descriptive or static artifacts that capture relationships without computing consequences (for example, a Quality Function Deployment house of quality, a static requirements traceability matrix, or a static design structure matrix with no analysis). A structural-only model fails the test. An executable model with analysis or constraint definitions passes (for example, a SysML v2 model with delta-V and power-margin calculations passes, but a plain structural SysML model does not).

---

## 2. The audience (your north star for every quality decision)

The end website must be useful to **practicing professionals, engineers, and data scientists** — not only students, and not a toy. When you face a judgment call about depth, accuracy, presentation, or what counts as "good enough," resolve it in favor of what a skeptical senior engineer or data scientist evaluating these models for real work would need. Hold that standard throughout.

---

## 3. What to do, in order, running to completion

### Stage A — Define the schema and your own acceptance criteria

First, design the data schema for a single catalog entry, expressed as YAML. Include at least these fields:

- `name`
- `gloss` — one-line plain-language description
- `domain` — sector or domain
- `system_represented` — what engineered system it models
- `inputs_you_can_change` — specifically what a user can vary
- `outputs_you_can_observe` — what outcomes of interest respond
- `runtime_required` — tool, language, or runtime needed to run it
- `access_type` — **mandatory**; e.g. permissive-open, copyleft-open, free-closed, freemium, commercial, campus-or-employer-licensed
- `license` — license name where applicable
- `scale` — approximate element count and how it groups into subsystems
- `maintenance_status` — with latest version or date
- `access_link` — canonical URL
- `suitability` — who it suits, e.g. newcomer versus expert
- `last_verified` — **mandatory**; ISO date you confirmed the volatile facts
- `source_per_field` — where each volatile fact came from
- `verification_confidence` — your honest confidence, and an explicit flag for anything unverified

For any field whose value sources commonly leave unstated (element counts especially, but also license and maintenance status), the schema must allow an explicit "unstated — needs direct verification" value rather than a guess.

Then **write your own acceptance criteria** for the catalog in a file called `ACCEPTANCE.md`. Define what "reasonable and useful to professionals, engineers, and data scientists" means in concrete, checkable terms — for example: minimum number of entries per domain, required fields that may never be empty, accuracy expectations for volatile facts, how broken links are handled, what the website must let a visitor do (search, filter by domain, filter by access type, sort by maintenance recency), and readability expectations for the prose output. Justify each criterion by reference to the audience. You will test against these criteria at the end, so make them specific.

### Stage B — Scaffold the repository

Decide and justify a structure. At minimum:

- a `data/` directory holding entries (choose and justify one-file-per-entry versus one-file-per-domain)
- a `validate` step that checks every entry against the schema and **fails loudly** on any missing mandatory field or malformed entry
- a `build` step that renders (1) a static website and (2) the narrative prose documents (Parts 1, 2, and 3 described below) from the same data
- the website must serve the professional/engineer/data-scientist audience: searchable, filterable by domain and access type, sortable by maintenance recency, with each entry rendered as a structured card carrying the schema fields

Choose a tech stack you can build and test headlessly in this environment, and justify the choice briefly in the repo README.

### Stage C — Populate the catalog by researching the domains

Research the domain clusters below and create a schema-valid entry for every qualifying model you find. Treat named examples as **seeds, not limits** — find more. Verify volatile facts (element count, license, maintenance status) against more than one source where you can, and record the source per field. Judge currency by whether the model or tool is usable and maintained **now**, not only by origination date; a long-lived but actively maintained tool counts as current. Flag anything dormant or abandoned rather than dropping it silently.

1. **Executable MBSE** — SysML v2 models with analysis and constraint definitions; executable Capella models. (Seeds: Airbus Apollo 11 SysML v2; Open-MBEE TMT model.)
2. **MathWorks model-based design** — Simulink, Simscape, Stateflow reference applications and whole-system examples (hybrid/electric powertrains, motor control, ADAS, flight control); substantial File Exchange system models. Record campus-or-employer-licensed access explicitly.
3. **Multidisciplinary design optimization (MDO)** — OpenMDAO, Dymos, NASA Aviary, pyCycle, SUAVE, RCAIDE.
4. **Equation-based physical modeling** — Modelica/OpenModelica and libraries; commercial peers (Dymola, MapleSim, Simcenter Amesim, GT-SUITE); the FMI/FMU co-simulation standard.
5. **Controls and dynamics in Python** — python-control, CasADi, do-mpc.
6. **Discrete-event and agent-based simulation** — SimPy, JaamSim, AnyLogic, NetLogo, Mesa, MATSim, Eclipse SUMO (traffic).
7. **Power and energy systems** — pandapower, OpenDSS, PyPSA and PyPSA-Eur, GridLAB-D, PowerModels.jl, OSeMOSYS, Calliope; building energy with EnergyPlus and OpenStudio.
8. **Infrastructure networks** — EPANET (water distribution), SWMM (stormwater).
9. **Robotics and multibody** — ROS/URDF robot descriptions, Gazebo, Drake, MuJoCo, PyBullet, Webots.
10. **Aerospace and space mission** — NASA GMAT, Basilisk, JSBSim, Orekit, OpenVSP.
11. **Wind and marine energy** — NREL OpenFAST, FLORIS, WEC-Sim.
12. **Process and chemical engineering** — DWSIM, ChemSep, the Tennessee Eastman process benchmark.
13. **Circuits and electronics** — ngspice, Sandia Xyce.
14. **Architecture description languages with analysis** — AADL with OSATE and its analysis plugins; EAST-ADL.
15. **Parametric spreadsheet models** — openly shared Excel or Google Sheets engineering models where inputs drive recomputed outputs (satellite link budgets, CubeSat mass/power budgets, rocket sizing tools, vehicle fuel-economy models), including those from NASA, universities, or standards bodies.
16. **Computing design structure matrix (DSM) models** — change-propagation or clustering models that compute, as distinct from static matrices.
17. **Heterogeneous and digital-twin platforms** — Ptolemy II; FMI-based co-simulation setups.

Treat these as adjacent and include only where framable as a runnable multi-element engineered system: systems-biology SBML models (BioModels); continuum solvers such as OpenFOAM.

### Stage D — Generate the narrative prose documents

From the same data, render three prose documents written for **text-to-speech** (e.g. ElevenReader). This means: flowing prose in short declarative sentences; introduce every example with lead-in language; put glosses in parentheses right where a listener needs them (a brief plain-language definition, like this); spell out acronyms on first use; minimal headers; no bullet inventories, no tables, no bold-label run-ins. Keep the underlying facts parallel across entries so they remain harvestable.

- **Part 1** — the inventory of computational system models, organized by domain, in this narrative style.
- **Part 2** — how generative AI is and isn't being used across these modeling traditions (not only MBSE: include code generation for Python and MATLAB, AI features in Simulink and in spreadsheets, and the MBSE/SysML picture). Where it shows most and least promise, and why.
- **Part 3** — the intersection: how the availability or scarcity of open, runnable system models relates to the use of generative AI across these traditions, with opportunities and gaps.

### Stage E — Test what you built, then report

Run your own validation and build. Then **test against your `ACCEPTANCE.md` criteria** and write the results into a `TEST_REPORT.md`: which criteria passed, which failed, and what you did about failures. Check that the website builds and that its search/filter/sort actually work (test headlessly). Verify links resolve. Produce a `GAPS.md` listing every fact you could not verify — especially element counts, licenses, and maintenance statuses — so I can do targeted manual checks.

Finally, summarize in `PROGRESS.md`: what you built, the key decisions and their justifications, total entries by domain, what you tested and the outcomes, and the open questions you want my input on.

---

## 4. Operating principles

- Prefer doing over asking. Where you must choose, choose for the professional/engineer/data-scientist audience and record why.
- Never invent a volatile fact. An explicit "unstated — needs verification" is always better than a confident guess.
- Commit and push frequently. Keep `PROGRESS.md` current as you go, not only at the end.
- If a research domain yields little, say so plainly in the log rather than padding it.
- The schema is the keystone. Keep every entry parallel so the website and the prose are both clean renders of the same data.
