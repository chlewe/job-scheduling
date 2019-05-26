from scheduling import SchedulingTask
from annealing import *


if __name__ == "__main__":
    scheduling_task = SchedulingTask()
    scheduling_task.add_from_file("tai_15_15_1.txt")
    sa = SimulatedAnnealing(20,
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
