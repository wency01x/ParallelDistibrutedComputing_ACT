# Laboratory 4: The "Analog-to-Digital" Parallel Challenge

*Course:* Parallel and Distributed Computing  
*Activity:* The "Analog-to-Digital" Parallel Challenge

---

## 👥 Group Members

- Harvie Babuyo
- Kerby Fabria
- Wency Casiño

---

## 📝 Project Overview

This repository contains our group's implementation for the Analog-to-Digital Parallel Challenge. The goal of this activity is to identify a real-world sequential bottleneck, translate it into a computational model, and implement a parallelized solution to measure performance improvements.

### Our Chosen Scenario: Pageant Tabulation System

We chose a *Local Pageant Scoring and Tabulation System*.

- *The Sequential Bottleneck:* A single chief tabulator manually gathering paper scorecards, calculating the average for one candidate, recording it, and then moving to the next.
- *The Parallel Solution:* Using *Data Parallelism*, we distributed the workload across multiple "assistant tabulators" (worker threads). Since the mathematical operation (averaging scores) is identical for all candidates, we partitioned the data (the candidates) so that multiple threads can process different candidates simultaneously.

---

## 🛠️ Technologies Used

- *Language:* Python 3.x
- *Concurrency Library:* concurrent.futures.ThreadPoolExecutor (Standard Python Library)

---

## 🚀 How to Run the Code

1. Clone the repository to your local machine:

git clone https://github.com/wency01x/ParallelDistibrutedComputing_ACT.git

2. Navigate into the directory:

cd ParallelDistibrutedComputing_ACT

3. Run the main Python script:

python main.py

---

## 📊 Expected Output & Benchmarks

The script simulates processing *50 candidates*, each with *5 judge scores*. It applies an artificial delay (time.sleep(0.1)) to simulate the physical time it takes to read a paper scorecard.

When you run the script, you should expect an output similar to this:

Running Sequential Tabulation (please wait ~5 seconds)...
Running Parallel Tabulation (please wait ~1 second)...

--- BENCHMARK REPORT ---
Sequential Time: 5.06 seconds
Parallel Time:   1.02 seconds
Speedup Ratio:   4.96

**Note:** Exact execution times and speedup ratios will vary slightly depending on the CPU load and hardware of the machine running the script.


---

## 📌 Contribution Breakdown

To meet the individual contribution requirements, the code was divided into three main implementation phases:

| # | Member | Contribution |
|---|--------|-------------|
| 1 | *Wency* | Implemented data setup and sequential processing logic — setup of candidate data and the run_sequential function |
| 2 | *Kerby* | Created thread pool for parallel data execution — implementation of the run_parallel function using ThreadPoolExecutor |
| 3 | *Harvie* | Added benchmarking logic and speedup calculation — execution block, timing, and formatting the console report |
