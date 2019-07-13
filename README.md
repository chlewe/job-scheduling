# job-scheduling
Practical assignment for Problem Solving and Search in AI

# Usage

```py main.py <instance-file> [-t timeout] [-o output-file]```

Arguments:

* ```<instance-file>```: The file defining jobs and their operations (see below for their structure)
* ```-t timeout``` (optional): Give the time for which the annealing algorithm shall run in seconds. default: 5 seconds.
* ```-o output-file``` (optional): Give a file to which the best found schedule shall be written. If omitted the time of the found schedule will be displayed but the schedule itself will be lost.

# Instance file format

All input files have to be of the ```.split``` or ```.merged``` format. Their file name has to end in either of those two.

## .split files

Instance given as follows:

```
Times
[time of job1 op1] [time of job1 op2] ...
[time of job2 op1] ...
...
Machines
[machine of job1 op1] [machine of job1 op2] ...
[machine of job2 op1] ...
```

Used by Taillard examples.

## .merged files

Instance given as follows:

```
[machine of job1 op1] [time of job1 op1] [machine of job1 op2] [time of job1 op2] ...
[machine of job2 op1] [time of job2 op1] ...
```

Used by the Brunel jobshop examples.
