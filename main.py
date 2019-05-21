from jobs import *

if __name__ == "__main__":
    scheduling_task = SchedulingTask()
    scheduling_task.add_from_file("instance_abz5.txt")
    print(scheduling_task)
    s = scheduling_task.random_schedule()
    for o, jid in s:
        print("Job " + str(jid) + " does operation on machine " + str(o.machine) + " for time " + str(o.time))
    print("Schedule is " + "valid" if scheduling_task.schedule_validity(s) else "not valid")
    length = SchedulingTask.get_schedule_time(s)
    print("Schedule takes " + str(length) + " time")
