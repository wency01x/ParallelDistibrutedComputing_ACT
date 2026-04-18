# benchmark.py
# Author: Kerby
# Responsibility: Measure and compare execution times across all implementations
#                 and dataset sizes, then print a formatted results table.

import time
import random
from dataset_generator import (
    generate_random,
    generate_sorted,
    generate_reverse_sorted,
    DATASET_SIZES,
)
from sequential_sort   import merge_sort
from sequential_search import linear_search
from parallel_sort     import parallel_sort
from parallel_search   import parallel_search


# ── Timing helper ─────────────────────────────────────────────────────────────

def timed(func, *args, **kwargs):
    """Run func(*args, **kwargs) and return (result, elapsed_seconds)."""
    start  = time.time()
    result = func(*args, **kwargs)
    return result, time.time() - start


# ── Table printer ─────────────────────────────────────────────────────────────

def print_table(title: str, rows: list[tuple]) -> None:
    """Pretty-print a results table to stdout."""
    col_widths = [22, 12, 12, 14]
    headers    = ["Dataset", "Sequential", "Parallel", "Speedup"]
    sep        = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(sep)
    header_row = "| " + " | ".join(
        h.ljust(col_widths[i]) for i, h in enumerate(headers)
    ) + " |"
    print(header_row)
    print(sep)
    for row in rows:
        label, seq_t, par_t, speedup = row
        print(
            f"| {str(label).ljust(col_widths[0])} "
            f"| {f'{seq_t:.4f}s'.ljust(col_widths[1])} "
            f"| {f'{par_t:.4f}s'.ljust(col_widths[2])} "
            f"| {speedup.ljust(col_widths[3])} |"
        )
    print(sep)


# ── Sorting benchmark ─────────────────────────────────────────────────────────

def benchmark_sorting() -> None:
    rows = []

    for label, size in DATASET_SIZES.items():
        data = generate_random(size)

        _, seq_t = timed(merge_sort,    data)
        _, par_t = timed(parallel_sort, data, num_processes=4)

        speedup = f"{seq_t / par_t:.2f}x" if par_t > 0 else "N/A"
        rows.append((f"{label} ({size:,})", seq_t, par_t, speedup))

    # Special cases
    for variant_label, generator in [
        ("sorted (small)",    lambda: generate_sorted(DATASET_SIZES["small"])),
        ("rev-sorted (small)", lambda: generate_reverse_sorted(DATASET_SIZES["small"])),
    ]:
        data        = generator()
        _, seq_t    = timed(merge_sort,    data)
        _, par_t    = timed(parallel_sort, data, num_processes=4)
        speedup     = f"{seq_t / par_t:.2f}x" if par_t > 0 else "N/A"
        rows.append((variant_label, seq_t, par_t, speedup))

    print_table("SORTING BENCHMARK  (Merge Sort — Sequential vs Parallel)", rows)


# ── Searching benchmark ───────────────────────────────────────────────────────

def benchmark_searching() -> None:
    rows = []

    for label, size in DATASET_SIZES.items():
        data   = generate_random(size)
        target = data[random.randint(0, size - 1)]   # guaranteed hit

        _, seq_t = timed(linear_search,   data, target)
        _, par_t = timed(parallel_search, data, target, num_processes=4)

        speedup = f"{seq_t / par_t:.2f}x" if par_t > 0 else "N/A"
        rows.append((f"{label} ({size:,})", seq_t, par_t, speedup))

    # Special case — target NOT in list
    data        = generate_random(DATASET_SIZES["medium"])
    _, seq_t    = timed(linear_search,   data, -1)
    _, par_t    = timed(parallel_search, data, -1, num_processes=4)
    speedup     = f"{seq_t / par_t:.2f}x" if par_t > 0 else "N/A"
    rows.append(("not-found (medium)", seq_t, par_t, speedup))

    print_table("SEARCHING BENCHMARK  (Linear Search — Sequential vs Parallel)", rows)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  Sequential vs Parallel Algorithm Benchmark")
    print("  Authors: Wency · Harvie · Kerby")
    print("=" * 60)

    print("\n[1/2] Running sorting benchmarks …  (large may take a moment)")
    benchmark_sorting()

    print("\n[2/2] Running searching benchmarks …")
    benchmark_searching()

    print("\n✓ Benchmark complete.\n")
