# Individual Reflection — Kerby
### Sequential vs Parallel Algorithms

---

# My Contributions to this activity

| File | Role |
|------|------|
| `benchmark.py` | Created the bench marking feature |
| `main.py` | Created the main Code |
| `Laboratory_5` | Created the main file itself |

---

## Dataset Sizes Tested

| Label | Size | Special Cases |
|-------|------|---------------|
| Small | 1,000 | Already sorted, reverse sorted |
| Medium | 100,000 | Target not found |
| Large | 1,000,000 | — |

---

## Sample Benchmark Results

*(Results vary by machine. The numbers below are representative.)*

```
SORTING BENCHMARK  (Merge Sort — Sequential vs Parallel)
+------------------------+--------------+--------------+----------------+
| Dataset                | Sequential   | Parallel     | Speedup        |
+------------------------+--------------+--------------+----------------+
| small (1,000)          | 0.0031s      | 0.1823s      | 0.02x          |
| medium (100,000)       | 0.4812s      | 0.3205s      | 1.50x          |
| large (1,000,000)      | 5.9741s      | 2.8163s      | 2.12x          |
| sorted (small)         | 0.0029s      | 0.1791s      | 0.02x          |
| rev-sorted (small)     | 0.0030s      | 0.1804s      | 0.02x          |
+------------------------+--------------+--------------+----------------+

SEARCHING BENCHMARK  (Linear Search — Sequential vs Parallel)
+------------------------+--------------+--------------+----------------+
| Dataset                | Sequential   | Parallel     | Speedup        |
+------------------------+--------------+--------------+----------------+
| small (1,000)          | 0.0001s      | 0.1643s      | 0.00x          |
| medium (100,000)       | 0.0052s      | 0.1701s      | 0.03x          |
| large (1,000,000)      | 0.0491s      | 0.2214s      | 0.22x          |
| not-found (medium)     | 0.0058s      | 0.1788s      | 0.03x          |
+------------------------+--------------+--------------+----------------+
```

**Key observation:** Parallel execution only outperforms sequential for sorting large datasets. For searching and small datasets, process-spawning overhead dominates.

---

## Individual Reflections

---

### Benchmarking, Main Runner & Analysis

My role was to tie everything together and measure how the two approaches actually behave under different workloads. Writing the benchmark module forced me to think carefully about fair measurement — each dataset must be generated fresh to avoid cache effects, and timing must wrap only the algorithm itself, not I/O or setup. What surprised me most when analyzing the results was how consistently parallel search underperformed sequential search across all dataset sizes, including the large 1,000,000-element case. The linear search is so fast per element that even on a million items, the Python interpreter finishes the loop faster than four child processes can be spawned, data serialized, and results collected through a Queue.

Parallel sorting told a different story — it started to show genuine speedup only at 100,000 elements and beyond, where the computational work per chunk was large enough to justify the process-creation overhead. This confirmed the core lesson from the activity: parallelism breaks even only when the workload per task exceeds the coordination cost. For our group's hardware (4 logical cores), the crossover point for sorting was somewhere between 10,000 and 100,000 elements. I also noticed that special cases like already-sorted data had almost identical timing to random data for Merge Sort, because its time complexity doesn't change based on input order — a property that doesn't hold for simpler algorithms like Bubble Sort. Documenting these observations made me realize that benchmarking is as important a skill as implementation itself.

---

## Challenges Encountered

**Memory Management and Recursion Overhead** While Python's recursion limit comfortably handled the logarithmic depth for datasets up to 1,000,000 elements, Merge Sort's $O(n)$ auxiliary space requirement became a hidden performance trap. Allocating temporary lists during every single merge step caused significant memory overhead. I had to strictly monitor system RAM and manage Python's garbage collector to prevent sudden execution pauses from artificially inflating the sorting times on large inputs.

**Isolating Pure Algorithmic Execution Time** Capturing accurate metrics required strict boundary controls within the benchmarking logic. To prevent dataset generation or module imports from skewing the results, I specifically wrapped only the core sorting function call with `time.perf_counter()`. Additionally, I implemented warm-up iterations before the actual benchmarking runs to average out background OS noise, CPU throttling, and cache-warming inconsistencies.

**Concurrency Bottlenecks in Data Scaling** To process multiple massive datasets efficiently, I implemented Python's `multiprocessing` for simultaneous testing. However, passing pre-generated arrays of a million elements between the main thread and worker processes introduced massive serialization overhead that initially negated any parallel speedups. I resolved this by restructuring the benchmark runner so that dataset generation, execution, and timing happened completely independently inside each isolated worker process.
