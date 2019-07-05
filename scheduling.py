from jobs import Job, Operation
from job_parser import read_jobs_from_file_merged, read_jobs_from_file_split
from typing import List, Tuple
import random


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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.jobs == other.jobs:
                return True
        return False

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

    def add_from_file(self, path_to_file, replace_jobs=False, split_format=False):
        """
        Add all jobs from the given file to the scheduling instance.

        Keyword arguments:
        path_to_file -- relative path to the text file to be parsed
        replace_jobs -- boolean value whether to overwrite all existing jobs
        split_format -- True: use split data format; False: use merged data format
        """

        if split_format:
            job_list = read_jobs_from_file_split(path_to_file)
        else:
            job_list = read_jobs_from_file_merged(path_to_file)

        if replace_jobs:
            self.jobs = []
        self.add_jobs(job_list)

    def __str__(self):
        out = ""
        for job, job_id in self.jobs:
            out += "Job " + str(job_id) + "\n" + str(job) + "\n\n"
        return out

    # Solving-related stuff
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
        # TODO: Clarify of above comment
        for op, job_id in schedule:
            job = self.get_job_by_id(job_id)
            if op not in job.operations:
                return False
        # Check whether operation order within jobs is preserved
        # TODO: Check that there are no overlapping operations
        for job, job_id in self.jobs:
            job_schedule = [op for op, j_id in schedule if j_id == job_id]
            if job.operations != job_schedule:
                print(job_id)
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

    @staticmethod
    def get_neighbours_arbitrary(schedule):
        """ For a schedule, return all valid swaps of arbitrarily-placed operations that produce a valid schedule """
        swaps = []
        for i, (op, job_id) in enumerate(schedule):
            forbidden_job_swaps = [job_id]
            k = 1
            while i+k < len(schedule):
                _, swap_job_id = schedule[i + k]
                if swap_job_id in forbidden_job_swaps:
                    break
                else:
                    swaps.append(tuple((i, i + k)))
                    forbidden_job_swaps.append(swap_job_id)
                k += 1
        return swaps

    @staticmethod
    def get_neighbours_local_arbitrary(schedule):
        """ For a schedule, return all valid swaps of arbitrarily-placed operations that produce a valid schedule """
        i, (op, job_id) = random.choice(list(enumerate(schedule)))

        swaps = []
        forbidden_job_swaps = [job_id]
        seen_machines = [op.machine]
        k = 1
        while i+k < len(schedule):
            neigh_op, neigh_swap_job_id = schedule[i + k]
            if neigh_swap_job_id in forbidden_job_swaps:
                break
            else:
                if op.machine in seen_machines or neigh_op.machine in seen_machines:
                    swaps.append((i, i + k))
                else:
                    seen_machines.append(op.machine)
                forbidden_job_swaps.append(neigh_swap_job_id)
            k += 1
        return swaps

    @staticmethod
    def get_random_neighbour_arbitrary(schedule):
        """ For a schedule, return a valid schedule that has two operations swapped """
        neighbours = []

        while not neighbours:
            neighbours = SchedulingTask.get_neighbours_local_arbitrary(schedule)
        i, j = random.choice(neighbours)
        new_schedule = schedule.copy()
        new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
        return new_schedule

    #@staticmethod
    #def get_neighbours_direct(schedule):
    #    """ For a schedule, return all valid swaps of adjacent operations that produce valid schedules """
    #    neighbour_swaps = []
    #    for i, (op, job_id) in enumerate(schedule):
    #        if i == len(schedule) - 1:
    #            break
    #        _, next_job_id = schedule[i + 1]
    #        if job_id != next_job_id:
    #            neighbour_swaps.append(tuple((i, i + 1)))
    #    return neighbour_swaps

    #@staticmethod
    #def get_random_neighbour_direct(schedule):
    #    """ For a schedule, return a valid schedule that has two adjacent operations swapped """
    #    neighbours = SchedulingTask.get_neighbours_direct(schedule)
    #    i, j = random.choice(neighbours)
    #    new_schedule = schedule.copy()
    #    new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
    #    return new_schedule
