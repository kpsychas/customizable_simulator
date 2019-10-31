#!/usr/bin/env python
import os

import numpy as np
from experiments.utils import NameGen, Timer

from simulator.sim_helper import SimulatorSimple
import simulator.simulation as msim


class Program:
    EXAMPLE1 = 1
    EXAMPLE2 = 2
    PLOT1 = 3
    PLOT2 = 4


PROGRAM = Program.EXAMPLE1
SAVE = True
RUNTAG = "runA"

FILETAG = os.path.basename(__file__)[:-3]
OUTPUTFOLDER = "outputs"
STEPS = int(1e5)
LOG_STEPS = STEPS//20
PLOT_STRIDE = 100


def main_example1(simulator):
    n_servers = 100
    reserve = 0
    lam = np.array([0.5, 0.5]) * n_servers

    for simid, sim_type in enumerate([msim.SIM1, msim.SIM2]):
        sim = msim.SimulationFactory.factory(
            sim_type, n_servers=n_servers, reserve=reserve, lam=lam)
        label = sim_type
        simulator.run(sim, STEPS, label=label, plot_stride=PLOT_STRIDE)


def main_example2(simulator):
    n_servers = 100
    reserve = 2
    lam = np.array([0.5, 0.5]) * n_servers
    lam_factors = [0.9, 1.0, 1.1]

    for simid, sim_type in enumerate([msim.SIM1, msim.SIM2]):
        for lam_factor in lam_factors:
            sim = msim.SimulationFactory.factory(
                sim_type, n_servers=n_servers, reserve=reserve,
                lam=lam*lam_factor)

            label = sim_type + '_' + str(lam_factor)
            simulator.run(sim, STEPS, label=label, plot_stride=PLOT_STRIDE)


def main_plot1(simulator):
    for label in [msim.SIM1, msim.SIM2]:
        simulator.load(label=label, new_label=label)


def main_plot2(simulator):
    lam_factors = [0.9, 1.0, 1.1]

    for sim_type in [msim.SIM1, msim.SIM2]:
        for lam_factor in lam_factors:
            label = sim_type + '_' + str(lam_factor)
            simulator.load(label=label, new_label=label)


def main():
    mynamegen = NameGen(FILETAG, OUTPUTFOLDER)
    mysimulator = SimulatorSimple(mynamegen, RUNTAG, SAVE)

    if PROGRAM == Program.EXAMPLE1:
        main_example1(mysimulator)
    elif PROGRAM == Program.EXAMPLE2:
        main_example2(mysimulator)
    elif PROGRAM == Program.PLOT1:
        main_plot1(mysimulator)
    elif PROGRAM == Program.PLOT2:
        main_plot1(mysimulator)

    mysimulator.finalize_plot(ylabel="Jobs in System", )


if __name__ == '__main__':
    with Timer('Experiment'):
        main()
