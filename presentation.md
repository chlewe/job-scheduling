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
    - exponential function: `T0 * d^t`
    - short dry run to estimate total number of steps
    - start temperature `T0` = 225 (~80% chance of random walk)
    - compute base / decay `d` such that final temperature ~3 (~1% chance of random walk)
    - for each problem size / timeout: same time spent per temperature

## Evaluation
- short timeout (5s)
    - from random solution to optimum:
        - ~60% on `tai_15_15`
        - ~17% on `tai_100_20`
    - acceptable for short computation time
    - good solution for smaller examples
- medium timeout (30-60s)
    - 30s: ~35-80%
    - 60s: ~50-85%
    - all examples benefit from more time
- long timeout (>60s)
    - 300s:
        - ~80% on `tai_50_20`
        - ~70% on `tai_100_20`
    - small examples do not benefit significantly, but large ones do

### Experiment
- `tai_15_15_1` (1118)
    -  5s: 2329 -> 1551 (64.24%)
    - 30s: 3138 -> 1464 (82.87%)
    - 60s: 2557 -> 1329 (85.34%)
- `tai_30_20_1` (1957)
    -  5s: 5088 -> 3859 (39.25%)
    - 30s: 4784 -> 3051 (61.30%)
    - 60s: 4558 -> 2851 (65.63%)
- `tai_50_20_1` (2868)
    -   5s: 6672 -> 5207 (38.51%)
    -  30s: 6823 -> 4805 (51.02%)
    -  60s: 5927 -> 4034 (61.88%)
    - 300s: 7182 -> 3586 (83.36%)
- `tai_100_20_1` (5464)
    -   5s: 10279 -> 9440 (17.42%)
    -  30s: 10173 -> 8444 (36.72%)
    -  60s: 10601 -> 7972 (51.18%)
    - 300s: 10719 -> 6841 (73.80%)
