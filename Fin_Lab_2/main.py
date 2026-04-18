# main.py
# Author: Kerby
# Responsibility: Top-level runner — demonstrates correctness of all four
#                 implementations then delegates to the full benchmark.

import random
from dataset_generator import generate_random
from sequential_sort   import merge_sort
from sequential_search import linear_search
from parallel_sort     import parallel_sort
from parallel_search   import parallel_search


DEMO_SIZE = 20   # small size so output is readable


def verify_sorting() -> None:
    """Quick correctness check: sequential and parallel sort must agree."""
    data      = generate_random(DEMO_SIZE)
    expected  = sorted(data)           # Python built-in as ground truth

    seq_out   = merge_sort(data)
    par_out   = parallel_sort(data, num_processes=4)

    print("── Sorting Verification ──────────────────────────────────")
    print(f"  Input    : {data}")
    print(f"  Expected : {expected}")
    print(f"  Seq sort : {seq_out}  ✓" if seq_out == expected else f"  Seq sort : FAILED ✗")
    print(f"  Par sort : {par_out}  ✓" if par_out == expected else f"  Par sort : FAILED ✗")


def verify_searching() -> None:
    """Quick correctness check: both search methods must return the same index."""
    data   = generate_random(DEMO_SIZE)
    target = data[random.randint(0, DEMO_SIZE - 1)]   # guaranteed present

    seq_idx = linear_search(data, target)
    par_idx = parallel_search(data, target, num_processes=4)

    print("\n── Searching Verification ────────────────────────────────")
    print(f"  Data     : {data}")
    print(f"  Target   : {target}")
    print(f"  Seq idx  : {seq_idx}  ({'✓' if seq_idx == par_idx else '✗'})")
    print(f"  Par idx  : {par_idx}  ({'✓' if seq_idx == par_idx else '✗'})")

    # Not-found case
    miss_seq = linear_search(data, -999)
    miss_par = parallel_search(data, -999, num_processes=4)
    print(f"  Not-found (-999) seq={miss_seq}, par={miss_par}  "
          f"({'✓' if miss_seq == miss_par == -1 else '✗'})")


def main() -> None:
    print("=" * 60)
    print("  Sequential vs Parallel Algorithms — Group Demo")
    print("  Wency · Harvie · Kerby")
    print("=" * 60)

    verify_sorting()
    verify_searching()

    print("\n── Full Benchmark ────────────────────────────────────────")
    print("  Running benchmark.py …\n")

    # Import and run the full benchmark suite
    from benchmark import benchmark_sorting, benchmark_searching
    benchmark_sorting()
    benchmark_searching()

    print("\n✓ All done.\n")


if __name__ == "__main__":
    main()
