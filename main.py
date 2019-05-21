from typing import List


class Operation:

    def __init__(self, time, machine):
        self.time = time
        self.machine = machine


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
                    op = Operation(time, machine)
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
