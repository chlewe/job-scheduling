from math import e
from random import random


class SimulatedAnnealing:

    def __init__(self, temperature_series, init_function, neighbouring_function, evaluation_function):
        self.temperature_series = temperature_series
        self.state = init_function()
        self.neighbouring_function = neighbouring_function
        self.evaluation_function = evaluation_function
        self.time = 1

    def get_temperature(self):
        return self.temperature_series(self.time)

    def random_transition(self, difference):
        return e**(-difference / self.get_temperature()) >= random()

    def do_annealing_step(self):
        neighbour = self.neighbouring_function(self.state)
        current_badness = self.evaluation_function(self.state)
        neighbour_badness = self.evaluation_function(neighbour)

        if neighbour_badness <= current_badness or self.random_transition(neighbour_badness - current_badness):
            self.state = neighbour
        self.time += 1
