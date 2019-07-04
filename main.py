from annealing import SimulatedAnnealing
from math import log
from scheduling import SchedulingTask
from time import time
import re
import sys

def exp_series(time):
    global temperature0
    global last_time
    global exp_decay

    temperature0 = temperature0 * exp_decay ** (time - last_time)
    last_time = time
    return temperature0
def fast_series(time):
    global temperature0
    return temperature0 / time
def boltz_series(time):
    global temperature0
    return temperature0 / log(time + 1)

def root_boltz_series(time):
    global temperature0
    return temperature0 / (log(time + 1) ** 0.5)
def linear_series(time):
    global temperature0
    return max(temperature0 - 0.25 * time, 5)

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

    sa = SimulatedAnnealing(lambda x: 100,
                            scheduling_task.random_schedule,
                            SchedulingTask.get_random_neighbour_arbitrary,
                            SchedulingTask.get_schedule_time)

    beginning = time()
    while True:
        sa.do_annealing_step()
        if time() - beginning >= timeout / 5:
            break

    temperature0 = 1000
    exp_decay = 0.003 ** (1 / (sa.time * 5))
    print(exp_decay, sa.time * 5)
    last_time = 0

    sa = SimulatedAnnealing(exp_series,
                            scheduling_task.random_schedule,
                            SchedulingTask.get_random_neighbour_arbitrary,
                            SchedulingTask.get_schedule_time)

    print("Start temperature: {}".format(temperature0))
    print(sa.evaluation_function(sa.state))
    beginning = time()
    while True:
        sa.do_annealing_step()
        if time() - beginning >= timeout:
            break
    print(sa.evaluation_function(sa.state))
    print("Final temperature: {}\nTotal time steps: {}".format(sa.get_temperature(), sa.time))
