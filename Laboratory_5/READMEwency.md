# Individual Reflection — Wency
### Sequential vs Parallel Algorithms | Group Activity

---

## My Contributions

| File | Role |
|------|------|
| `dataset_generator.py` | Designed and implemented all dataset generation utilities |
| `sequential_sort.py` | Built the sequential Merge Sort from scratch |
| `sequential_search.py` | Built the sequential Linear Search from scratch |

---

## Reflection

Working on the dataset generation and sequential algorithms gave me a strong foundation before our group even touched parallelism. My first task was building `dataset_generator.py`, which handled generating random, already-sorted, and reverse-sorted lists across three sizes — 1,000, 100,000, and 1,000,000 elements. It seems simple on the surface, but deciding how to structure the generator cleanly so that Kerby's benchmark module could import it without issues required thinking about the project as a whole, not just my individual part.

Implementing Merge Sort sequentially in `sequential_sort.py` was where I spent the most time. I had to build both the `merge()` helper and the recursive `merge_sort()` function entirely from scratch without relying on Python's built-in sort. The core logic — splitting the list at the midpoint, recursively sorting each half, then merging them back together — is straightforward in concept but easy to get wrong in the details, especially in the merge step where you have to carefully track two pointers moving through the left and right sublists simultaneously. Once I had it working correctly on small inputs, I tested it against `sorted()` as a ground truth and confirmed it produced identical results across all dataset sizes.

What surprised me most was how well the sequential version performed even on the large 1,000,000-element dataset. Because Merge Sort is O(n log n) in all cases — best, average, and worst — it did not slow down disproportionately as the data grew. Comparing this to what Harvie measured with the parallel version, the sequential sort was actually faster on small and medium datasets. The overhead of spawning processes, serializing data, and collecting results through `Pool.map()` cost more time than the parallelism saved. This was only overcome at the large dataset size, where the computational work per chunk finally outweighed the coordination cost.

The sequential linear search in `sequential_search.py` reinforced this lesson even more clearly. The operation per element is so lightweight — just one comparison — that the sequential version ran in microseconds on small datasets. No amount of parallel coordination can compete with that. I also added a `linear_search_all()` variant that returns every index where the target appears, which I thought was a practical addition since our random datasets can contain duplicate values.

The biggest insight I took from my part of this activity is that sequential algorithms are not inferior to parallel ones — they are simply designed for a different context. When the problem is small, or when the work per element is trivial, simplicity wins. Parallelism only becomes worthwhile when the dataset is large enough that dividing and coordinating the work costs less than the time saved by doing it simultaneously. Understanding where that crossover point lies is what I now see as the real skill in systems programming.

---

## Observed Performance (Sorting)

| Dataset | Sequential Time | Parallel Time | Speedup |
|---------|----------------|---------------|---------|
| Small (1,000) | ~0.0011s | ~0.1601s | 0.01x (seq faster) |
| Medium (100,000) | ~0.2155s | ~0.3496s | 0.62x (seq faster) |
| Large (1,000,000) | ~5.97s | ~2.82s | ~2.12x (par faster) |
| Already sorted (1,000) | ~0.0029s | ~0.1791s | 0.02x (seq faster) |
| Reverse sorted (1,000) | ~0.0030s | ~0.1804s | 0.02x (seq faster) |

> Parallel sorting only outperformed sequential at the **large dataset size**. For small and medium sizes, process-spawning overhead dominated.

---

## Challenges I Encountered

**Recursive depth on large inputs.** Python's default recursion limit is 1,000. For 1,000,000 elements, the recursion depth of Merge Sort reaches log₂(1,000,000) ≈ 20, which is well within the limit — but I had to verify this carefully before being confident it would not crash on the large dataset.

**Making the generator reusable.** I had to structure `dataset_generator.py` so that both the `main.py` and `benchmark.py` modules could import `DATASET_SIZES` and the generator functions cleanly. This meant thinking about module-level constants and avoiding any side effects at import time.

**Validating correctness before speed.** It was tempting to jump straight to timing, but I made sure to confirm that `merge_sort()` produced the exact same output as Python's built-in `sorted()` on every dataset size before handing it off to Harvie and Kerby to use in their modules.

---

## Key Takeaways

- Sequential algorithms have **predictable, low-overhead behavior** that is hard to beat for small or simple workloads.
- Merge Sort's **O(n log n) complexity in all cases** makes it an ideal base for parallelization — each chunk gets the same algorithm applied independently.
- Establishing a **correct sequential baseline** first is essential. If the foundation is wrong, parallel versions will just propagate the bug across multiple processes in harder-to-debug ways.
- The crossover point where parallelism becomes beneficial depends heavily on **hardware, dataset size, and per-element work cost** — it cannot be assumed in advance.
