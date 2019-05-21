from typing import List, Tuple
import random


class Operation:

    def __init__(self, time, machine):
        self.time = time
        self.machine = machine

    def __str__(self):
        return "Operation with time " + str(self.time) + " on machine " + str(self.machine)


class Job:

    def __init__(self, operations: List[Operation] = None):
        if operations is None:
            operations = []
        self.operations = operations

    def add_operation(self, op):
        self.operations.append(op)

    def add_operations(self, ops):
        for op in ops:
            self.operations.append(op)

    def __str__(self):
        operations = "Operation"
        times = "Time     "
        machines = "Machine  "
        for i, operation in enumerate(self.operations):
            operations += " " * (7 - len(str(i))) + str(i)
            times += " "*(7-len(str(operation.time))) + str(operation.time)
            machines += " " * (7 - len(str(operation.machine))) + str(operation.machine)
        return operations + "\n" + times + "\n" + machines


class SchedulingTask:

    # Structural stuff
    def __init__(self, jobs: List[Job] = None):
        self.next_id = 0
        self.jobs = []
        if jobs is None:
            jobs = []
        for job in jobs:
            self.jobs.append(tuple((job, self.next_id)))
            self.next_id += 1

    def add_job(self, job):
        self.jobs.append(tuple((job, self.next_id)))
        self.next_id += 1

    def add_jobs(self, jobs):
        for job in jobs:
            self.jobs.append(tuple((job, self.next_id)))
            self.next_id += 1

    def get_job_by_id(self, job_id):
        for job, j_id in self.jobs:
            if job_id == j_id:
                return job
        return None

    def add_from_file(self, path_to_file, replace_jobs=False):
        """
        Add all jobs from the given file to the scheduling instance.
        Expected format is jobs separated by \n and operations given by machine time separated by blanks, e.g.
        1 14 2 6 3 17
        2 5 3 21 1 10

        Keyword arguments:
        path_to_file -- relative path to the text file to be parsed
        replace_jobs -- boolean value whether to overwrite all existing jobs
        """
        with open(path_to_file) as f:
            job_list = []
            for line in f:
                j = Job()
                line = line[:-1]
                while line[0] == " ":
                    line = line[1:]
                while line[-1] == " ":
                    line = line[:-1]
                while "  " in line:
                    line = line.replace("  ", " ")
                line = line.split(" ")
                if len(line) % 2 != 0:
                    print("Couldn't read file " + path_to_file + " as a job contained an odd number of values.")
                    return
                for (machine, time) in zip(line[::2], line[1::2]):
                    op = Operation(int(time), int(machine))
                    j.add_operation(op)
                job_list.append(j)
        if replace_jobs:
            self.jobs = []
        self.add_jobs(job_list)

    def __str__(self):
        out = ""
        for job, job_id in self.jobs:
            out += "Job " + str(job_id) + "\n" + str(job) + "\n\n"
        return out

    # Solving related stuff
    def random_schedule(self):
        """Return a random schedule, represented by a list of tuples each containing the operation and its job"""
        to_be_scheduled = [[tuple((op, job_id)) for op in job.operations] for job, job_id in self.jobs]
        schedule = []
        while to_be_scheduled:
            next_job = random.choice(to_be_scheduled)
            next_operation = next_job[0]
            schedule.append(next_operation)
            next_job.pop(0)
            if [] in to_be_scheduled:
                to_be_scheduled.remove([])
        return schedule

    def schedule_validity(self, schedule: List[Tuple[Operation, int]]):
        # Check whether operations belong to given job
        for op, job_id in schedule:
            job = self.get_job_by_id(job_id)
            if op not in job.operations:
                return False
        # Check whether operation order withing jobs is preserved
        for job, job_id in self.jobs:
            job_schedule = [op for op, j_id in schedule if j_id == job_id]
            if job.operations != job_schedule:
                return False
        return True

    @staticmethod
    def get_schedule_time(schedule: List[Tuple[Operation, int]]):
        """ For a given schedule, compute how much time passes for all operations to finish """
        # TODO: make this return a schedule, not just time
        # for each job, save how long scheduling an operation of this job
        # is blocked by the execution of a previous operation of that job
        job_blocking = {}
        # for each machine, save how long it is blocked by an operation
        machine_blocking = {}

        for op, job_id in schedule:
            earliest_scheduling_time = 0
            if job_id in job_blocking:
                earliest_scheduling_time = job_blocking.get(job_id)
            if op.machine in machine_blocking:
                earliest_scheduling_time = max(earliest_scheduling_time, machine_blocking[op.machine])
            end_time = earliest_scheduling_time + op.time
            job_blocking[job_id] = end_time
            machine_blocking[op.machine] = end_time
        return max(job_blocking.values())


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
