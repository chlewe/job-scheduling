# Presentation notes (2019-07-08)

## General
- simulated annealing
- temperature function
    - high: random walk
    - low: local search
- neighbourhood function
    - many jobs, each job has many operations, each operation has a machine
    - space of schedules

## Problems and solutions
- good neighbourhood function
    - goal: small, but impactful
    - sequence of operations
    - shift each operation "leftwards" until there is another operation using the same machine
    - neighbours: swap two operations (preserve order within job)
    - optimisation: only swap operations of different machines (and jobs)
- good temperature function
    - goal: random walk at beginning, local search at end
    - goal: scales with problem size and timeout
    - exponential function: `T0 + d^t`
    - short dry run to estimate total number of steps
    - start temperature `T0` = 1000 (~100% chance of random walk)
    - compute base / decay `d` such that final temperature ~3 (~1% chance of random walk)
    - for each problem size / timeout: same time spent per temperature

## Evaluation
- TODO: verify these numbers in little experiment over Taillard instances and various timeouts
- short timeout (5s)
    - ~25% from random solution to optimum
    - acceptable for short computation time
- medium timeout (30 - 60s)
    - ~50% from random solution to optimum
    - more time gives better solutions
- long timeout (>60s)
    - ~75% from random solution to optimum
    - approach does not benefit significantly from long computation times
