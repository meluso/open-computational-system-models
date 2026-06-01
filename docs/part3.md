# Part Three: The Intersection of Open Runnable Models and Generative AI

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
that model works. Of the 1 models in this catalog, 1 are open source, and
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
