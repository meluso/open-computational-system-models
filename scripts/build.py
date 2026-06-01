#!/usr/bin/env python3
"""Build the static website and the three narrative prose documents from the
single catalog dataset under data/.

Refuses to build if validation fails (build on a clean dataset only).

Outputs:
    site/                 static website (index.html, css, mjs, generated data)
    docs/part1.md         inventory, by domain, in text-to-speech prose
    docs/part2.md         generative AI across these modeling traditions
    docs/part3.md         the intersection of open runnable models and AI

Usage:
    python scripts/build.py
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import pathlib
import shutil
import sys
from collections import Counter

from common import (
    REPO_ROOT,
    is_unstated,
    load_domains,
    load_entries,
)
import validate as _validate

WEB_DIR = REPO_ROOT / "web"
SITE_DIR = REPO_ROOT / "site"
DOCS_DIR = REPO_ROOT / "docs"

ACCESS_PHRASE = {
    "permissive-open": "permissively open source",
    "weak-copyleft-open": "open source under a weak-copyleft license",
    "copyleft-open": "open source under a copyleft license",
    "free-closed": "free to use but closed source",
    "freemium": "free in a limited tier with paid upgrades",
    "commercial": "commercially licensed",
    "campus-or-employer-licensed": "reached through a campus or employer license",
}

ACCESS_LABEL = {
    "permissive-open": "Permissive open source",
    "weak-copyleft-open": "Weak-copyleft open source",
    "copyleft-open": "Copyleft open source",
    "free-closed": "Free, closed source",
    "freemium": "Freemium",
    "commercial": "Commercial",
    "campus-or-employer-licensed": "Campus / employer licensed",
}

STATUS_PHRASE = {
    "active": "actively maintained",
    "maintained": "maintained, though at a slower pace",
    "dormant": "dormant but still usable",
    "abandoned": "effectively abandoned",
    "unknown": "of uncertain maintenance status",
}

# Authored, text-to-speech-friendly lead-ins per domain. Acronyms are spelled
# out on first use here so the generated inventory reads cleanly aloud.
DOMAIN_INTRO = {
    "executable-mbse": (
        "We begin with executable Model-Based Systems Engineering, often shortened "
        "to M B S E (the practice of capturing a system as a connected model rather "
        "than as scattered documents). The models that interest us here do more than "
        "describe. They compute. They carry analysis and constraint definitions, so "
        "changing a parameter changes a calculated result."
    ),
    "mathworks-mbd": (
        "Next we turn to model-based design in the MathWorks tools, chiefly Simulink "
        "(a block-diagram environment for simulating dynamic systems). Access here is "
        "usually through a campus or employer license, which we record plainly rather "
        "than treat as a reason to exclude."
    ),
    "mdo": (
        "Now consider multidisciplinary design optimization, shortened to M D O (the "
        "practice of coupling several engineering disciplines and letting an optimizer "
        "trade them off against one another). These frameworks turn a whole vehicle "
        "into something you can optimize."
    ),
    "equation-based-physical": (
        "We move to equation-based physical modeling. The idea is to write the physics "
        "as equations and let a solver sort out cause and effect, rather than fixing "
        "the direction of computation in advance. Modelica is the open language at the "
        "center of this tradition."
    ),
    "controls-dynamics-python": (
        "Here are the controls and dynamics libraries written for Python. They let an "
        "engineer design, simulate, and optimize control systems in a familiar "
        "scripting language."
    ),
    "des-abm": (
        "Now we reach discrete-event and agent-based simulation. In discrete-event "
        "simulation, a system jumps from one event to the next, such as a part arriving "
        "at a machine. In agent-based simulation, many individual agents follow simple "
        "rules and the system behavior emerges from their interaction."
    ),
    "power-energy": (
        "We turn to power and energy systems. These models represent electrical grids "
        "and energy systems, from the flow of power through a distribution feeder to the "
        "expansion of a national energy system over decades."
    ),
    "infrastructure-networks": (
        "Next are infrastructure networks for water. These models route flow and "
        "pressure through pipes, junctions, and pumps, and they are the public standard "
        "for utilities and consultants alike."
    ),
    "robotics-multibody": (
        "Now consider robotics and multibody simulation. These tools describe a robot "
        "as a tree of links and joints and then simulate the physics, so you can test "
        "control and motion before touching hardware."
    ),
    "aerospace-space": (
        "We move to aerospace and space mission modeling. These tools cover flight "
        "dynamics in the atmosphere, spacecraft attitude and orbit in space, and the "
        "geometry of an aircraft before it is built."
    ),
    "wind-marine-energy": (
        "Here is wind and marine energy. These models capture the aeroelastic behavior "
        "of a wind turbine, the wakes that turbines cast on one another across a farm, "
        "and the response of a wave energy converter in the sea."
    ),
    "process-chemical": (
        "Now we reach process and chemical engineering. These simulators assemble a "
        "chemical plant from unit operations such as columns, reactors, and heat "
        "exchangers, and then solve for the streams that flow between them."
    ),
    "circuits-electronics": (
        "We turn to circuits and electronics. These are simulators in the S P I C E "
        "tradition, where S P I C E stands for the Simulation Program with Integrated "
        "Circuit Emphasis. You give them a netlist of components and they solve for the "
        "voltages and currents."
    ),
    "architecture-description-langs": (
        "Next are architecture description languages with analysis. These languages let "
        "you model the architecture of a system and then run analyses on it, such as "
        "whether a set of tasks can be scheduled or whether a safety property holds."
    ),
    "parametric-spreadsheets": (
        "Now consider parametric spreadsheet models. A spreadsheet may be humble, but "
        "when its inputs drive a chain of recomputed outputs across dozens of linked "
        "cells, it is a runnable system model in every sense that matters here."
    ),
    "computing-dsm": (
        "We turn to computing models built on the design structure matrix, shortened to "
        "D S M (a square matrix that records which elements of a system depend on which "
        "others). The models that qualify here compute something from that matrix, such "
        "as how a change propagates, rather than merely displaying it."
    ),
    "heterogeneous-digital-twin": (
        "Finally among the core clusters we reach heterogeneous and digital-twin "
        "platforms. These frameworks let different kinds of model run together, or couple "
        "separate simulators into a single co-simulation that can stand in for a real "
        "system."
    ),
    "systems-biology-sbml": (
        "We include a brief, adjacent note on systems biology. The Systems Biology "
        "Markup Language, shortened to S B M L, lets researchers share runnable models "
        "of biochemical networks. We include only those that read as a runnable system "
        "of many interacting parts."
    ),
    "continuum-cfd": (
        "We close with another adjacent note, on continuum solvers such as computational "
        "fluid dynamics, shortened to C F D. We include these only where a setup reads as "
        "a runnable, multi-element engineered system rather than a single physics demo."
    ),
}


def prose_join(items: list[str]) -> str:
    """Join a list into spoken-prose form with an Oxford comma."""
    items = [str(i).strip().rstrip(".") for i in items if str(i).strip()]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + ", and " + items[-1]


def soften(text: str) -> str:
    """Lowercase the first character of a gloss and strip a trailing period so it
    sits naturally inside a parenthetical."""
    t = str(text).strip().rstrip(".")
    if not t:
        return t
    # Keep acronyms / proper nouns that are all-caps for the first word.
    first_word = t.split()[0]
    if first_word.isupper() or (len(first_word) > 1 and first_word[1:].islower() is False and first_word[0].isupper() and any(c.isupper() for c in first_word[1:])):
        return t
    return t[0].lower() + t[1:]


def entry_paragraph(e: dict) -> str:
    name = e["name"]
    gloss = soften(e["gloss"])
    sys_rep = soften(str(e["system_represented"]).strip().rstrip("."))
    inputs = prose_join(e["inputs_you_can_change"])
    outputs = prose_join(e["outputs_you_can_observe"])
    runtime = str(e["runtime_required"]).strip().rstrip(".")

    s = []
    s.append(f"Consider {name} ({gloss}).")
    s.append(f"It represents {sys_rep}.")
    s.append(f"A user can change {inputs}.")
    s.append(f"In response, the model reports {outputs}.")
    s.append(f"To run it you need {runtime}.")

    access = ACCESS_PHRASE.get(e["access_type"], e["access_type"])
    lic = e.get("license")
    if is_unstated(lic):
        s.append(
            f"It is {access}, though the exact license is unstated and needs direct "
            f"verification."
        )
    else:
        s.append(f"It is {access}, released under the {lic} license.")

    ms = e.get("maintenance_status", {})
    status = STATUS_PHRASE.get(ms.get("status"), "of uncertain maintenance status")
    ver = ms.get("latest_version")
    date = ms.get("latest_release_date")
    tail = ""
    if ver and not is_unstated(ver):
        tail += f" The latest version on record is {ver}"
        if date and not is_unstated(date):
            tail += f", from {date}"
        tail += "."
    elif date and not is_unstated(date):
        tail += f" The latest activity on record is from {date}."
    s.append(f"As of the last check it was {status}.{tail}")

    s.append(str(e["suitability"]).strip().rstrip(".") + ".")
    return " ".join(s)


def build_part1(entries: list[dict], domains: list[dict]) -> str:
    by_domain: dict[str, list[dict]] = {}
    for e in entries:
        by_domain.setdefault(e["domain"], []).append(e)

    lines = []
    lines.append("# Part One: An Inventory of Computational System Models")
    lines.append("")
    lines.append(
        "What follows is an inventory of computational system models, organized by "
        "domain and written to be read aloud. A computational system model, for our "
        "purposes, is a representation of an engineered system with many interacting "
        "parts that a person can actually run, so that changing inputs or parameters "
        "produces observably different outcomes. Every model named here meets that one "
        "test. You can vary something and watch a result change."
    )
    lines.append("")
    total = len(entries)
    present_domains = [d for d in domains if by_domain.get(d["slug"])]
    model_word = "model" if total == 1 else "models"
    domain_word = "domain" if len(present_domains) == 1 else "domains"
    lines.append(
        f"The inventory holds {total} {model_word} across {len(present_domains)} "
        f"{domain_word}. We take the domains in turn."
    )
    lines.append("")

    for d in present_domains:
        items = sorted(by_domain[d["slug"]], key=lambda e: e["name"].lower())
        intro = DOMAIN_INTRO.get(d["slug"], "")
        lines.append(intro)
        lines.append("")
        n = len(items)
        count_word = "one model" if n == 1 else f"{n} models"
        lines.append(f"In this domain the inventory records {count_word}.")
        lines.append("")
        for e in items:
            lines.append(entry_paragraph(e))
            lines.append("")

    lines.append(
        "That completes the inventory. The facts above are kept deliberately parallel "
        "from one model to the next, so the same questions are answered for each. What "
        "does it represent. What can you change. What can you observe. What does it cost "
        "to reach. How well is it maintained. Where a fact could not be confirmed, the "
        "catalog says so plainly rather than guessing."
    )
    lines.append("")
    return "\n".join(lines)


def build_part2(entries: list[dict], domains: list[dict]) -> str:
    n = len(entries)
    open_types = {"permissive-open", "weak-copyleft-open", "copyleft-open"}
    n_open = sum(1 for e in entries if e["access_type"] in open_types)
    n_licensed = sum(
        1
        for e in entries
        if e["access_type"] in {"commercial", "campus-or-employer-licensed", "freemium"}
    )
    # Authored essay; the few figures are pulled from the live catalog so the
    # prose stays consistent with the data.
    text = f"""# Part Two: Generative AI Across These Modeling Traditions

This part steps back from the inventory and asks a single question. Where is
generative artificial intelligence, shortened to A I, actually changing how these
system models get built and used, and where is it mostly noise. We will move
across the traditions in the catalog, from writing code, through the modeling
languages, into the spreadsheets, and on to systems engineering. The honest
answer differs sharply from one tradition to the next.

Start with the place the effect is largest, which is writing model code in
general-purpose languages. Many of the most capable tools in this catalog are
Python libraries. OpenMDAO for optimization, python-control and do-mpc for
control, SimPy and Mesa for simulation, pandapower and PyPSA for power systems,
Orekit and Basilisk for spacecraft. For all of these, a large language model is a
genuine accelerant. It can scaffold a model, wire up a component, recall an
unfamiliar interface, and explain an error message. The reason it works so well
here is that the languages are popular, the libraries are open, and decades of
example code sit in public repositories that the models were trained on. The same
holds, with a little more friction, for MATLAB and Simulink. The MATLAB language
is widely documented, so a model can write MATLAB scripts capably, and MathWorks
has added an A I assistant of its own. But Simulink itself is a visual,
block-diagram tool. A model can describe how to build a Simulink diagram, and can
generate the MATLAB that builds one programmatically, but it cannot yet drag the
blocks. The further a tradition sits from text, the weaker the help.

That single observation, that these tools help most where the artifact is text
and where training data is abundant, explains nearly everything that follows.

Consider the equation-based physical modeling tradition, built on Modelica. Here
the picture is mixed. Modelica is a text language, which helps, but it is far less
common than Python, so a model has seen far less of it and makes more mistakes,
especially around the acausal semantics that make Modelica distinctive. It can
write plausible Modelica that does not quite simulate. The verification burden
falls back on the engineer.

Now consider spreadsheets, the parametric budget models for satellites, launch
vehicles, and the like. These are a quiet success story for A I assistance.
Spreadsheet formulas are text, the patterns are common, and the major spreadsheet
vendors have shipped natural-language features that write formulas and explain
them. For an engineer assembling a link budget or a mass and power budget, this is
real help with low stakes, because the result is immediately checkable.

Then there is systems engineering and the modeling languages, M B S E and SysML.
This is where the marketing is loudest and the substance is thinnest. The vision
is appealing. Describe a system in plain language and have the model produce a
SysML model. In practice the results are brittle. SysML version one has a heavy,
tool-specific representation under the surface, so generated models often fail to
load or fail to mean what they appear to mean. SysML version two, which is newer,
has a clean textual notation and a published grammar, and this matters a great
deal. A textual, well-specified language is exactly what these models are good at.
So the most credible near-term A I help in systems engineering is not the grand
vision but the narrow one. Generate the textual SysML version two for a constraint
or an analysis, and let the engineer check it.

A pattern emerges across the catalog. Of the {n} models recorded here, {n_open}
are open source and {n_licensed} are reached through a commercial, freemium, or
institutional license. Generative A I helps most with the open, text-based,
widely-used tools, because those are the ones whose code filled the training data.
It helps least with the closed, visual, or niche tools, because those left little
public trace and cannot be driven through text.

Two cautions belong in any honest account. First, these models are confident when
they are wrong, and a simulation that runs is not a simulation that is correct. In
engineering, a plausible-looking but subtly wrong model is more dangerous than an
obvious error, because it passes the eye test. Second, the help is concentrated at
the start of the work, the scaffolding and the boilerplate, and thins out exactly
where engineering judgment matters most, in choosing assumptions, validating
against data, and deciding whether the answer can be trusted. The tools shorten the
typing. They do not shorten the thinking.
"""
    return text


def build_part3(entries: list[dict], domains: list[dict]) -> str:
    n = len(entries)
    open_types = {"permissive-open", "weak-copyleft-open", "copyleft-open"}
    n_open = sum(1 for e in entries if e["access_type"] in open_types)
    by_domain = Counter(e["domain"] for e in entries)
    # Domains that lean open vs. closed, for the argument.
    text = f"""# Part Three: The Intersection of Open Runnable Models and Generative AI

The first part inventoried the models. The second asked where generative
artificial intelligence, shortened to A I, helps. This third part joins them,
because the two questions turn out to be the same question seen from two sides.
The usefulness of A I across these engineering traditions tracks, almost line for
line, the availability of open, runnable system models. Where open models are
abundant, the A I is genuinely useful. Where they are scarce or locked away, the A
I has little to stand on.

The reason is mechanical, not mysterious. A language model learns from text it can
see. An open, runnable model contributes far more than a closed one, because it
brings its source code, its documentation, its issue threads, its tutorials, and
the many public projects built on top of it. A commercial tool reached only
through a license leaves a thin public trace by comparison. So the very openness
that lets a human run a model for free is the same openness that taught the A I how
that model works. Of the {n} models in this catalog, {n_open} are open source, and
it is no accident that those are the same traditions where A I assistance is
strongest.

Look at where the open models cluster. The Python ecosystems for control, for
optimization, for simulation, and for power systems are deep and open, and these
are exactly the places where an engineer gets the most from an A I assistant
today. The catalog reflects this. Domains such as controls and dynamics in Python,
multidisciplinary design optimization, and power and energy systems are well
populated with permissively licensed tools whose code is fully public.

Now look at where open, runnable models are scarce. Three gaps stand out. The
first is systems engineering. For all the talk of A I writing system models, the
supply of open, executable SysML and Capella models is thin, and much of what
exists lives inside vendor tools. The arrival of the textual SysML version two
notation may change this, because a clean text format invites public examples, and
public examples are what the A I needs. The second gap is the commercial physical
modeling and systems simulation tools, the high-end environments for
multi-physics, powertrain, and plant simulation. They are powerful and widely used
in industry, but their models are closed, so the A I cannot learn them well, and
the engineers who rely on them get the least help. The third gap is the visual and
block-diagram tools, where even an open tool resists A I assistance because the
artifact is not text.

From this reading, the opportunities follow directly. The highest-value move for
any of these traditions that wants to benefit from A I is to publish open, runnable
example models in a textual form, with documentation, under a permissive license.
That single act does double duty. It lets a practicing engineer run and learn the
model for free, and it feeds the public corpus that makes the A I helpful for that
very tool. A catalog like this one is a small step in that direction, because it
gathers the runnable models in one place, records how to reach each one, and says
honestly which facts it could not confirm.

There is a quieter opportunity too, pointing the other way. A I can help close the
gap it depends on. It is already reasonable to use a model to translate a model
between formalisms, to generate the textual SysML version two for an analysis, to
write the script that drives a simulator, or to convert a brittle spreadsheet into
documented code. Used this way, generative A I does not only consume open models.
It can help manufacture more of them.

The gap to watch, and to guard against, is trust. As it becomes easy to generate
system models, it becomes easy to generate models that look right and are wrong.
The traditions in this catalog that have strong validation cultures, the ones that
check a simulation against measured data and against conservation laws, are the
ones best placed to absorb A I help safely. The discipline that made these models
trustworthy in the first place is exactly the discipline that A I makes more
necessary, not less. The runnable, checkable, openly licensed model is both the
fuel for the A I and the test it must pass.
"""
    return text


def write_site(entries: list[dict], domains: list[dict], built_iso: str) -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    # Copy static source assets.
    for fn in ("index.html", "style.css", "app.mjs", "catalog-logic.mjs"):
        shutil.copyfile(WEB_DIR / fn, SITE_DIR / fn)

    # Strip private keys for publication.
    public = [{k: v for k, v in e.items() if not k.startswith("_")} for e in entries]
    meta = {"built": built_iso, "count": len(public)}

    # JSON for data consumers.
    with open(SITE_DIR / "catalog.json", "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "domains": domains, "entries": public}, fh, indent=2, ensure_ascii=False)

    # ES module so the app works from file:// with no fetch / CORS issues.
    with open(SITE_DIR / "catalog-data.mjs", "w", encoding="utf-8") as fh:
        fh.write("// GENERATED by scripts/build.py — do not edit by hand.\n")
        fh.write("export const CATALOG = ")
        json.dump(public, fh, indent=2, ensure_ascii=False)
        fh.write(";\n\nexport const DOMAINS = ")
        json.dump(domains, fh, indent=2, ensure_ascii=False)
        fh.write(";\n\nexport const META = ")
        json.dump(meta, fh, ensure_ascii=False)
        fh.write(";\n")


def main() -> int:
    # Build only on a valid dataset.
    rc = _validate.main(["--quiet"])
    if rc != 0:
        print("\nBuild aborted: validation failed. Fix the errors above.", file=sys.stderr)
        return rc

    entries = load_entries()
    domains = load_domains()
    # Stamp build date. Allow override for reproducible builds/tests.
    built_iso = os.environ.get("BUILD_DATE")
    if not built_iso:
        built_iso = _dt.date.today().isoformat()

    write_site(entries, domains, built_iso)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "part1.md").write_text(build_part1(entries, domains), encoding="utf-8")
    (DOCS_DIR / "part2.md").write_text(build_part2(entries, domains), encoding="utf-8")
    (DOCS_DIR / "part3.md").write_text(build_part3(entries, domains), encoding="utf-8")

    print(f"BUILD OK: {len(entries)} entries")
    print(f"  site/    -> index.html, catalog-data.mjs, catalog.json (+assets)")
    print(f"  docs/    -> part1.md, part2.md, part3.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
