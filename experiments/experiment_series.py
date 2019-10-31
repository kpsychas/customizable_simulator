#!/usr/bin/env python
import os

import numpy as np
from experiments.utils import NameGen, Timer

from simulator.sim_helper import SimulatorSeries
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
    reserve = 1
    sim_types = [msim.SIM1, msim.SIM2]
    n_server_v = np.array([10, 20, 50, 100])

    simulator.init_series(reps=1, values=n_server_v, labels=sim_types)

    for simid, sim_type in enumerate(sim_types):
        print("Simulation Type", sim_type)

        for vi, n_servers in enumerate(n_server_v):
            lams = np.array([0.5, 0.5]) * n_servers
            sim = msim.SimulationFactory.factory(
                sim_type, n_servers=n_servers, reserve=reserve, lam=lams)
            label = sim_type
            simulator.run(0, vi, sim, max_steps=STEPS, label=label,
                          plot_stride=PLOT_STRIDE)

    simulator.plot_save_all_series(plot_1=False, plot_h=False)


def main_example2(simulator):
    n_servers = 100
    reserve = 1
    sim_types = [msim.SIM1, msim.SIM2]
    arr_scale_v = np.array([0.9, 1.0, 1.1, 1.2])

    simulator.init_series(reps=1, values=arr_scale_v, labels=sim_types)

    for simid, sim_type in enumerate(sim_types):
        print("Simulation Type", sim_type)

        for vi, arr_scale in enumerate(arr_scale_v):
            lams = arr_scale * n_servers * np.array([0.5, 0.5])
            sim = msim.SimulationFactory.factory(
                sim_type, n_servers=n_servers, reserve=reserve, lam=lams)
            label = sim_type
            simulator.run(0, vi, sim, STEPS, label=label,
                          plot_stride=PLOT_STRIDE)

    simulator.plot_save_all_series(plot_1=False, plot_h=False)


def main_plot1(simulator):
    sim_types = [msim.SIM1, msim.SIM2]
    n_server_v = np.array([10, 20, 50, 100])
    simulator.init_series(reps=1, values=n_server_v, labels=sim_types)

    for label in sim_types:
        simulator.load(label=label, new_label=label, plot_1=False, plot_h=False)


def main_plot2(simulator):
    sim_types = [msim.SIM1, msim.SIM2]
    arr_scale_v = np.array([0.9, 1.0, 1.1, 1.2])
    simulator.init_series(reps=1, values=arr_scale_v, labels=sim_types)

    for label in sim_types:
        simulator.load(label=label, new_label=label, plot_1=False, plot_h=False)


def main():
    mynamegen = NameGen(FILETAG, OUTPUTFOLDER)
    mysimulator = SimulatorSeries(mynamegen, RUNTAG, SAVE)

    xlabel = ""
    if PROGRAM == Program.EXAMPLE1:
        main_example1(mysimulator)
        xlabel = "Number of Servers"
    elif PROGRAM == Program.EXAMPLE2:
        main_example2(mysimulator)
        xlabel = "Arrival Rate"
    elif PROGRAM == Program.PLOT1:
        main_plot1(mysimulator)
        xlabel = "Number of Servers"
    elif PROGRAM == Program.PLOT2:
        main_plot2(mysimulator)
        xlabel = "Arrival Rate"

    mysimulator.finalize_plot(xlabel=xlabel, ylabel="Acceptance Rate")


if __name__ == '__main__':
    with Timer('Experiment'):
        main()
