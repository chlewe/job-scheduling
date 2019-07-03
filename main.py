from annealing import SimulatedAnnealing
from math import log
from scheduling import SchedulingTask
from time import time
import re
import sys

def exp_series(time):
    global temperature0
    return temperature0 * (0.95 ** time)
def fast_series(time):
    global temperature0
    return temperature0 / time
def boltz_series(time):
    global temperature0
    if time <= 1:
        return 1000000
    else:
        return temperature0 / log(time)

def safe_log_series(time):
    global temperature0
    return temperature0 / log(time + 1)
def squared_boltz_series(time):
    global temperature0
    if time <= 1:
        return 1000000
    else:
        return temperature0 / (log(time) ** 2)
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

    temperature0 = timeout * 2
    scheduling_task = SchedulingTask()
    scheduling_task.add_from_file(path_to_file, split_format=split_format)
    sa = SimulatedAnnealing(safe_log_series,
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
    print("Total time steps: {}".format(sa.time))

    #for i in range(200000):
    #    if sa.time % 10000 == 1:
    #        print(str((sa.time - 1)/2000) + "%")
    #        print(sa.evaluation_function(sa.state))
    #    sa.do_annealing_step()
    #print(sa.state)
    #print(sa.evaluation_function(sa.state))
