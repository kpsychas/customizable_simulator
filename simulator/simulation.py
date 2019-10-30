#!/usr/bin/env python
import simulator.simulation_type1 as st1
import simulator.simulation_type1 as st2

SIM1 = "sim1"
SIM2 = "sim2"


class SimulationFactory(object):
    @staticmethod
    def factory(sim_type, **kwargs):
        """
        Factory method that returns a Simulation class
        
        * there is a chance that interface of Simulation class cannot 
        be consistent in all methods
        
        :param sim_type:
        :param kwargs: 
        :return: 
        """
        if sim_type == SIM1:
            n_servers = kwargs.pop('n_servers', 10)
            reserve = kwargs.pop('reserve', 1)
            lambdas = kwargs.pop('lambdas', [n_servers*0.5, n_servers*0.5])
            return st1.Simulation(n_servers=n_servers, reserve=reserve,
                                  lambda1=lambdas[0], lambda2=lambdas[1])
        elif sim_type == SIM2:
            n_servers = kwargs.pop('n_servers', 10)
            reserve = kwargs.pop('reserve', 1)
            lambdas = kwargs.pop('lambdas', [n_servers*0.5, n_servers*0.5])
            return st2.Simulation(n_servers=n_servers, reserve=reserve,
                                  lambda1=lambdas[0], lambda2=lambdas[1])
        else:
            raise ValueError("Simulation Type: '{}' is not valid."
                             .format(sim_type))


def main():
    for sim_type in [SIM1, SIM2]:

        sim = SimulationFactory.factory(sim_type)
        for _ in range(1000):
            sim.step()

        print('-----------------------------------------')
        print("Method {}, metric 1 after 1000 simulation steps:{}"
              .format(sim_type, sim.metric1))
        print("State at end of simulation:")
        sim.print_state(verbose=False)
        print('-----------------------------------------')


if __name__ == '__main__':
    main()
