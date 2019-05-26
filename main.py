from annealing import SimulatedAnnealing
from math import log
from scheduling import SchedulingTask
from time import time
import re
import sys


def temperature_series(time):
    temperature = 20 / log(time + 1)
    return temperature

if __name__ == "__main__":
    scheduling_task = SchedulingTask()
    scheduling_task.add_from_file(path_to_file, split_format=split_format)
    sa = SimulatedAnnealing(temperature_series,
                            scheduling_task.random_schedule,
                            SchedulingTask.get_random_neighbour_arbitrary,
                            SchedulingTask.get_schedule_time)
    for i in range(200000):
        if sa.time % 10000 == 1:
            print(str((sa.time-1)/2000) + "%")
            print(sa.evaluation_function(sa.state))
        sa.do_annealing_step()
    print(sa.state)
    print(sa.evaluation_function(sa.state))
