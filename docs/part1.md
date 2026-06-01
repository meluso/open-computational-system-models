# Part One: An Inventory of Computational System Models

What follows is an inventory of computational system models, organized by domain and written to be read aloud. A computational system model, for our purposes, is a representation of an engineered system with many interacting parts that a person can actually run, so that changing inputs or parameters produces observably different outcomes. Every model named here meets that one test. You can vary something and watch a result change.

The inventory holds 1 model across 1 domain. We take the domains in turn.

Now consider multidisciplinary design optimization, shortened to M D O (the practice of coupling several engineering disciplines and letting an optimizer trade them off against one another). These frameworks turn a whole vehicle into something you can optimize.

In this domain the inventory records one model.

Consider OpenMDAO (an open-source framework for gradient-based multidisciplinary design optimization of coupled engineering systems). It represents coupled multidisciplinary engineering systems — for example an aircraft whose aerodynamics, structures, and propulsion are optimized together — assembled from interconnected analysis components. A user can change design variables (e.g. geometry, sizing, operating conditions), constraints and objective function, component connections and model topology, solver and optimizer settings, and analytic vs. finite-difference derivative options. In response, the model reports optimized design variable values, objective and constraint values at the optimum, coupled multidisciplinary analysis results, total derivatives / design sensitivities, and optimizer iteration history. To run it you need Python 3 (with NumPy/SciPy; optional pyOptSparse for advanced optimizers). It is permissively open source, released under the Apache-2.0 license. As of the last check it was actively maintained. The latest version on record is 3.43.0, from 2026-03-11. Suits engineers and researchers comfortable with Python who need rigorous, derivative-based optimization of coupled systems; steeper learning curve than a point tool, so less suited to a casual newcomer.

That completes the inventory. The facts above are kept deliberately parallel from one model to the next, so the same questions are answered for each. What does it represent. What can you change. What can you observe. What does it cost to reach. How well is it maintained. Where a fact could not be confirmed, the catalog says so plainly rather than guessing.
