from jobs import *
from annealing import *


if __name__ == "__main__":
    scheduling_task = SchedulingTask()
    scheduling_task.add_from_file("instance_abz5.txt")
    sa = SimulatedAnnealing(10,
                            scheduling_task.random_schedule,
                            SchedulingTask.get_random_neighbour_arbitrary,
                            SchedulingTask.get_schedule_time)
    for i in range(500000):
        sa.do_annealing_step()
        if sa.time % 10000 == 0:
            print(str(sa.time/5000) + "%")
    print(sa.state)
    print(sa.evaluation_function(sa.state))
