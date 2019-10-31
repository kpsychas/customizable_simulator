Customizable Simulator
==

This project automates the task of simulating and comparing 
different models. Classes were kept generic but have to be 
customized to be useful

Features
--

* A minimal interface that should be implemented from
all simulation classes is defined in simulation_base.py
* Factory method of simulation.py automates initialization of 
simulation classes which can have any number of custom named
fields.
* Two helper classes automate the generation of 
time based plots and plots with respect to a custom parameter.
* Another class automates the storage of simulation data such
that their plots can be generated at a later time without
running the simulation again.

Use case
--
The functionality of simulator is demonstrated through the
implementation of two trivial cluster scheduling models
whose details are not in scope of this work.
They are in `simulator.simulation_type1.py` and
`simulator.simulation_type2.py`.

We will simply mention that both models serve two job types
and metric 1 corresponds to the number of jobs of type 1
in the system, while
metric 2 corresponds to the fraction of jobs of type 1
that were not rejected.
To test them we implemented two experiments in
the `experiments` folder. The `experiment_simple.py` 
plots metric 1 with respect to time. 
The `experiment_series.py` plots metric 2 at the end
of simulation with respect to model parameters like
the number of servers and how frequently jobs 
arrive.

Running Examples
--
Invoke `python` from root directory to run any of the scripts
e.g.

    > python experiments/experiment_simple.py

Parameter `PROGRAM` chooses whether to plot or run one of
the two examples. Parameter `SAVE` saves outputs after 
running simulations (ignored if we choose to plot).
Parameter `RUNTAG` is supposed to be a unique identifier
of a run. It has to change in every run, if parameters are 
different.

Extensions and Discussion
--
The design allows the addition of multiple simulation 
classes as long as they all have the same interface.
This simplifies the comparison but not the implementation
of individual classes. Also documenting each class and
documenting experiments (e.g. which parameters or example
was run for a specific runtag) are necessary and unavoidable.