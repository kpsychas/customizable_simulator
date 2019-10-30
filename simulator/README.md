Prototype of Generic Simulator
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
time based plots and plots of a custom metric
respectively.
* Another class automates the storage of simulation data such
that their plots can be generated at a later time without
running the simulation again

Use case
--
TODO


