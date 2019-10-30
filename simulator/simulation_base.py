#!/usr/bin/env python
from abc import ABCMeta, abstractmethod


class SimulationBase(metaclass=ABCMeta):

    @property
    @abstractmethod
    def metric1(self):
        pass

    @property
    @abstractmethod
    def metric2(self):
        pass

    @property
    @abstractmethod
    def cur_time(self):
        pass

    @abstractmethod
    def print_state(self, verbose):
        pass

    @abstractmethod
    def step(self):
        pass
