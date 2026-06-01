# Part Three: The Intersection of Open Runnable Models and Generative AI

The first part inventoried the models. The second asked where generative
artificial intelligence, shortened to A I, helps. This third part joins them,
because the two questions turn out to be two aspects of the same question.
The usefulness of A I across these engineering traditions tracks, almost line for
line, the availability of open, runnable system models. Where open models are
abundant, the A I is genuinely useful. Where they are scarce or proprietary, the A
I has little to draw on.

The reason is mechanical, not mysterious. A language model learns from text it can
see. An open, runnable model contributes far more than a closed one, because it
brings its source code, its documentation, its issue threads, its tutorials, and
the many public projects built on top of it. A commercial tool reached only
through a license leaves little public material by comparison. So the very openness
that lets a human run a model for free is the same openness that taught the A I how
that model works. Of the 89 models in this catalog, 70 are open source, and
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
supply of open, executable SysML and Capella models is small, and much of what
exists is held only inside vendor tools. The arrival of the textual SysML version two
notation may change this, because a clean text format encourages public examples, and
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
That single act serves two purposes. It lets a practicing engineer run and learn the
model for free, and it adds to the public corpus that makes the A I helpful for that
very tool. A catalog like this one is one contribution toward that, because it
gathers the runnable models in one place, records how to reach each one, and says
honestly which facts it could not confirm.

There is a quieter opportunity too, in the opposite direction. A I can help reduce the
scarcity it depends on. It is already reasonable to use a model to translate a model
between formalisms, to generate the textual SysML version two for an analysis, to
write the script that drives a simulator, or to convert an undocumented spreadsheet into
documented code. Used this way, generative A I does not only consume open models.
It can help produce more of them.

The risk to watch is trust. As it becomes easy to generate
system models, it becomes easy to generate models that look right and are wrong.
The traditions in this catalog that have strong validation practices, the ones that
check a simulation against measured data and against conservation laws, are the
ones best positioned to adopt A I help safely. The discipline that made these models
trustworthy in the first place is exactly the discipline that A I makes more
necessary, not less. The runnable, checkable, openly licensed model is both the
input the A I depends on and the standard it must meet.
