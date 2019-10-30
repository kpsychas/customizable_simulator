#!/usr/bin/env python
import numpy as np

from simulator.simulation_base import SimulationBase


def exp_dis(mean):
    return -mean * np.log(np.random.rand(*mean.shape))


class Event:
    ARRIVAL = 'arrival'
    SERVICE = 'service'


class Simulation(SimulationBase):
    def __init__(self, n_servers, reserve, lambda1, lambda2):
        self.n_servers = n_servers
        self.lambdas = np.array([lambda1, lambda2])

        self._reserve = reserve

        self._used_spots = np.array([0, 0])
        self._jobs_arrived = np.array([0, 0])
        self._jobs_admitted = np.array([0, 0])

        self._time = 0

    @property
    def metric1(self):
        return self._used_spots[0]

    @property
    def metric2(self):
        jarr = self._jobs_arrived
        jadm = self._jobs_admitted
        return jadm[0]/jarr[0] if (jarr[0] > 0) else 0

    @property
    def cur_time(self):
        return self._time

    def get_next_event(self):
        arrival_intervals = 1 / (self.lambdas + 1e-10)
        service_intervals = []
        total_used_spots = self._used_spots
        for spots in total_used_spots:
            service_intervals.append(1 / np.ones(spots))

        arrival_times = exp_dis(arrival_intervals)
        service_times = np.zeros_like(total_used_spots, dtype='float')
        for i, interval in enumerate(service_intervals):
            service_times[i] = exp_dis(interval).min() \
                if total_used_spots[i] > 0 else np.inf

        # (x1, y1) < (x2, y2) if (x1 < x2) or (x1 = x2 and y1 < y2)
        event_time, event_type = min([(arrival_times.min(), Event.ARRIVAL),
                                      (service_times.min(), Event.SERVICE)])

        if event_type == Event.ARRIVAL:
            jobid = arrival_times.argmin()
        elif event_type == Event.SERVICE:
            jobid = service_times.argmin()
        else:
            raise ValueError(event_type)

        return event_time, event_type, jobid

    def print_state(self, verbose):
        print("Servers in use by job type 1: {}".format(self._used_spots[0]))
        print("Servers in use by job type 2: {}".format(self._used_spots[1]))
        empty = self.n_servers - self._used_spots[0] - self._used_spots[1]
        print("Empty servers: {}".format(empty))

    def step(self):
        event_time, event_type, jobid = self.get_next_event()
        self._time += event_time

        if event_type == Event.ARRIVAL:
            self._jobs_arrived[jobid] += 1

            c1 = self._used_spots[0]
            c2 = self._used_spots[1]
            ctot = self.n_servers
            if jobid == 0 and ctot - c1 - c2 > 0:
                self._used_spots[0] += 1
                self._jobs_admitted[0] += 1
            elif jobid == 1 and ctot - c1 - c2 > self._reserve:
                self._used_spots[1] += 1
                self._jobs_admitted[1] += 1

        elif event_type == Event.SERVICE:
            self._used_spots[jobid] -= 1

