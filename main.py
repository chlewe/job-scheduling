from annealing import SimulatedAnnealing
from math import log
from scheduling import SchedulingTask
from time import time
import re
import sys
import argparse


def exp_series(time):
    global temperature0
    global last_time
    global exp_decay

    temperature0 = temperature0 * exp_decay ** (time - last_time)
    last_time = time
    return temperature0


#def fast_series(time):
#    global temperature0
#    return temperature0 / time
#
#
#def boltz_series(time):
#    global temperature0
#    return temperature0 / log(time + 1)
#
#
#def root_boltz_series(time):
#    global temperature0
#    return temperature0 / (log(time + 1) ** 0.5)
#
#
#def linear_series(time):
#    global temperature0
#    return max(temperature0 - 0.25 * time, 5)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_file',
                        help='path to the scheduling task')
    parser.add_argument('-t', dest='timeout', type=int, default=5,
                        help='timeout')
    parser.add_argument('-o', dest='output_file',
                        help='output file')

    args = parser.parse_args()

    path_to_file = args.path_to_file
    timeout = args.timeout

    if re.search(r"\.split$", path_to_file):
        split_format = True
    elif re.search(r"\.merged$", path_to_file):
        split_format = False
    else:
        print("The given file must end with either '.split' or '.merged'!")
        sys.exit(1)

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

    temperature0 = 225
    exp_decay = (0.1/temperature0) ** (1 / (sa.time * 5))
    print("Expected number of annealing steps:", sa.time * 5)
    print("Set exponential decay factor to", exp_decay)
    last_time = 0

    sa = SimulatedAnnealing(exp_series,
                            scheduling_task.random_schedule,
                            SchedulingTask.get_random_neighbour_arbitrary,
                            SchedulingTask.get_schedule_time)

    print("Start temperature: {}".format(temperature0))
    print("Created first random schedule with time", sa.evaluation_function(sa.state))
    beginning = time()
    while True:
        sa.do_annealing_step()
        if time() - beginning >= timeout:
            break
    print("Final temperature: {}\nTotal time steps: {}".format(sa.get_temperature(), sa.time))

    print("\nTime of final schedule:", sa.evaluation_function(sa.state))
    print("The schedule found is " + ("" if scheduling_task.schedule_validity(sa.state) else "in") + "valid.")

    if args.output_file:
        try:
            SchedulingTask.output_schedule(sa.state, args.output_file)
            print("Saved schedule in " + args.output_file)
        except Exception:
            print("Couldn't write output file.")
