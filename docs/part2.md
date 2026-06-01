# Part Two: Generative AI Across These Modeling Traditions

This part steps back from the inventory and asks a single question. Where is
generative artificial intelligence, shortened to A I, actually changing how these
system models get built and used, and where does it add little. We will move
across the traditions in the catalog, from writing code, through the modeling
languages, into the spreadsheets, and on to systems engineering. The honest
answer differs sharply from one tradition to the next.

Start with the place the effect is largest, which is writing model code in
general-purpose languages. Many of the most capable tools in this catalog are
Python libraries. OpenMDAO for optimization, python-control and do-mpc for
control, SimPy and Mesa for simulation, pandapower and PyPSA for power systems,
Orekit and Basilisk for spacecraft. For all of these, a large language model is a
substantial help. It can scaffold a model, wire up a component, recall an
unfamiliar interface, and explain an error message. The reason it works so well
here is that the languages are popular, the libraries are open, and decades of
example code are available in public repositories that the models were trained on. The same
holds, with more difficulty, for MATLAB and Simulink. The MATLAB language
is widely documented, so a model can write MATLAB scripts capably, and MathWorks
has added an A I assistant of its own. But Simulink itself is a visual,
block-diagram tool. A model can describe how to build a Simulink diagram, and can
generate the MATLAB that builds one programmatically, but it cannot yet drag the
blocks. The less text-based a tradition is, the weaker the help.

That single observation, that these tools help most where the artifact is text
and where training data is abundant, explains nearly everything that follows.

Consider the equation-based physical modeling tradition, built on Modelica. Here
the picture is mixed. Modelica is a text language, which helps, but it is far less
common than Python, so a model has seen far less of it and makes more mistakes,
especially around the acausal semantics that make Modelica distinctive. It can
write plausible Modelica that does not quite simulate. The verification burden
falls back on the engineer.

Now consider spreadsheets, the parametric budget models for satellites, launch
vehicles, and the like. These are an underappreciated success for A I assistance.
Spreadsheet formulas are text, the patterns are common, and the major spreadsheet
vendors have shipped natural-language features that write formulas and explain
them. For an engineer assembling a link budget or a mass and power budget, this is
real help with low stakes, because the result is immediately checkable.

Then there is systems engineering and the modeling languages, M B S E and SysML.
This is where the claims are strongest and the demonstrated results are weakest. The
goal is appealing. Describe a system in plain language and have the model produce a
SysML model. In practice the results are unreliable. SysML version one has a complex,
tool-specific underlying representation, so generated models often fail to
load or fail to mean what they appear to mean. SysML version two, which is newer,
has a clean textual notation and a published grammar, and this matters a great
deal. A textual, well-specified language is exactly what these models are good at.
So the most credible near-term A I help in systems engineering is not the broad
goal but the narrow one. Generate the textual SysML version two for a constraint
or an analysis, and let the engineer check it.

A pattern emerges across the catalog. Of the 89 models recorded here, 70
are open source and 17 are reached through a commercial, freemium, or
institutional license. Generative A I helps most with the open, text-based,
widely-used tools, because those are the ones whose code is well represented in the
training data. It helps least with the closed, visual, or niche tools, because those
left little public material and cannot be driven through text.

Two cautions belong in any honest account. First, these models are confident when
they are wrong, and a simulation that runs is not a simulation that is correct. In
engineering, a plausible-looking but subtly wrong model is more dangerous than an
obvious error, because it looks correct on inspection. Second, the help is concentrated at
the start of the work, the scaffolding and the boilerplate, and diminishes exactly
where engineering judgment matters most, in choosing assumptions, validating
against data, and deciding whether the answer can be trusted. The tools shorten the
typing. They do not shorten the thinking.
