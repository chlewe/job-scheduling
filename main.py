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
    if len(sys.argv) < 2:
        print("Usage: <file.split|file.merged> [timeout in seconds]")
        sys.exit(1)

    path_to_file = sys.argv[1]

    if re.search(r"\.split$", path_to_file):
        split_format = True
    elif re.search(r"\.merged$", path_to_file):
        split_format = False
    else:
        print("The given file must end with either '.split' or '.merged'!")
        sys.exit(1)

    if len(sys.argv) >= 3:
        timeout = int(sys.argv[2])
    else:
        timeout = 5

    scheduling_task = SchedulingTask()
    scheduling_task.add_from_file(path_to_file, split_format=split_format)
    sa = SimulatedAnnealing(temperature_series,
                            scheduling_task.random_schedule,
                            SchedulingTask.get_random_neighbour_arbitrary,
                            SchedulingTask.get_schedule_time)

    print(sa.evaluation_function(sa.state))
    beginning = time()
    while True:
        sa.do_annealing_step()
        if time() - beginning >= timeout:
            break
    print(sa.evaluation_function(sa.state))

    #for i in range(200000):
    #    if sa.time % 10000 == 1:
    #        print(str((sa.time - 1)/2000) + "%")
    #        print(sa.evaluation_function(sa.state))
    #    sa.do_annealing_step()
    #print(sa.state)
    #print(sa.evaluation_function(sa.state))
