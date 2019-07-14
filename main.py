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

    # Dry run to determine the expected number of steps before the timeout.
    sa = SimulatedAnnealing(lambda x: 100,
                            scheduling_task.random_schedule,
                            SchedulingTask.get_random_neighbour_arbitrary,
                            SchedulingTask.get_schedule_time)

    beginning = time()
    while True:
        sa.do_annealing_step()
        if time() - beginning >= timeout / 5:
            break

    # Temperature at the start of the annealing
    temperature0 = 225
    # Temperature that should be reached at the end of the annealing
    final_temperature = 0.1
    # Exponential decay is computed so that we reach `final_temperature` after the expected number of steps
    exp_decay = (final_temperature / temperature0) ** (1 / (sa.time * 5))
    last_time = 0

    print("Expected step count:      {}".format(sa.time * 5))
    print("Exponential decay factor: {}".format(exp_decay))

    # Reset annealing for actual run
    sa = SimulatedAnnealing(exp_series,
                            scheduling_task.random_schedule,
                            SchedulingTask.get_random_neighbour_arbitrary,
                            SchedulingTask.get_schedule_time)

    print("\nCreated random schedule.")
    print("Start temperature:        {}".format(temperature0))
    print("Time of random schedule:  {}".format(sa.evaluation_function(sa.state)))

    # Actual annealing
    beginning = time()
    while True:
        sa.do_annealing_step()
        if time() - beginning >= timeout:
            break

    print("\nFinal temperature:        {}".format(sa.get_temperature()))
    print("Time of final schedule:   {}".format(sa.evaluation_function(sa.state)))
    print("The final schedule is {}".format("valid." if scheduling_task.schedule_validity(sa.state) else "INVALID!"))
    print("\nTotal step count:         {}".format(sa.time))

    if args.output_file:
        try:
            SchedulingTask.output_schedule(sa.state, args.output_file)
            print("\nWrote final schedule to \'{}\'.".format(args.output_file))
        except Exception:
            print("\nFailed to write to output file!")
