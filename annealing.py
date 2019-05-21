from math import e, log
from random import random


class SimulatedAnnealing:

    def __init__(self, temperature_modifier, init_function, neighbouring_function, evaluation_function):
        self.temperature_modifier = temperature_modifier
        self.state = init_function()
        self.neighbouring_function = neighbouring_function
        self.evaluation_function = evaluation_function
        self.time = 1

    def get_temperature(self):
        return self.temperature_modifier/log(self.time+1)

    def random_transition(self, difference):
        return e**(-difference/self.get_temperature()) >= random()

    def do_annealing_step(self):
        neighbour = self.neighbouring_function(self.state)
        current_value = self.evaluation_function(self.state)
        neighbour_value = self.evaluation_function(neighbour)
        if neighbour_value < current_value or self.random_transition(neighbour_value-current_value):
            self.state = neighbour
        self.time += 1
