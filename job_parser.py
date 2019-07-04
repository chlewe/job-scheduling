from jobs import Job, Operation
import re
import sys

def read_jobs_from_file_merged(path_to_file):
    """
    Reads jobs from the given file.

    Expected format (prefix, infix or suffix whitespaces are allowed):
    1 14 2 6 3 17
    2 5 3 21 1 10

    Format semantics:
    <machine job1/op1> <time job1/op1> <machine job1/op1> <time job1/op2> ...
    <machine job2/op1> <time job2/op1> ...

    Keyword arguments:
    path_to_file -- relative path to the text file to be parsed

    Returns:
    list of jobs, read from the file
    """
    with open(path_to_file, "r") as f:
        jobs = list()

        for line in f:
            normalised_line = re.sub(r"(^\s*)|(\s*$)", "", line)
            split_line = re.split(r"\s+", normalised_line)

            if len(split_line) % 2 != 0:
                print("Failed to parse \"" + path_to_file + "\" as a job contains an odd number of values!")
                sys.exit(1)

            job = Job()
            for (machine, time) in zip(split_line[::2], split_line[1::2]):
                op = Operation(int(time), int(machine))
                job.add_operation(op)

            jobs.append(job)

    return jobs

def read_jobs_from_file_split(path_to_file):
    """
    Reads jobs from the given file.

    Expected format (prefix, infix or suffix whitespaces are allowed):
    Times
    14 6 17
    5 21 10
    Machines
    1 2 3
    2 3 1

    Format semantics:
    Times
    <time job1/op1> <time job1/op2> ...
    <time job2/op1> ...
    Machines
    <machine job1/op1> <machine job1/op2> ...
    <machine job2/op1> ...

    Keyword arguments:
    path_to_file -- relative path to the text file to be parsed

    Returns:
    list of jobs, read from the file
    """
    with open(path_to_file, "r") as f:
        times = list()
        machines = list()
        times_and_not_machines = True

        for line in f:
            normalised_line = re.sub(r"(^\s*)|(\s*$)", "", line)

            if normalised_line == "Times":
                times_and_not_machines = True
                continue
            elif normalised_line == "Machines":
                times_and_not_machines = False
                continue

            split_line = re.split(r"\s+", normalised_line)

            if times_and_not_machines:
                times.append(split_line)
            else:
                machines.append(split_line)

        if len(times) != len(machines):
            print("Failed to parse \"" + path_to_file + "\" as the number of jobs is inconsistent!")
            sys.exit(1)

        jobs = list()
        for i in range(0, len(times)):
            if len(times[i]) != len(machines[i]):
                print("Failed to parse \"" + path_to_file + "\" as a job contains an inconsistent number of times and machines!")
                sys.exit(1)

            job = Job()
            for (time, machine) in zip(times[i], machines[i]):
                op = Operation(int(time), int(machine))
                job.add_operation(op)

            jobs.append(job)

    return jobs
