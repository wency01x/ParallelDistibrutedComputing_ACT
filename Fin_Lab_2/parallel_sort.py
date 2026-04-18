from multiprocessing import Pool
from sequential_sort import merge

def _sort_chunk(chunk: list[int]) -> list[int]:
    from sequential_sort import merge_sort
    return merge_sort(chunk)

def merge_sorted_halves(sorted_lists: list[list[int]]) -> list[int]:
    while len(sorted_lists) > 1:
        merged = []
        for i in range(0, len(sorted_lists), 2):
            if i + 1 < len(sorted_lists):
                merged.append(merge(sorted_lists[i], sorted_lists[i + 1]))
            else:
                merged.append(sorted_lists[i])
        sorted_lists = merged
    return sorted_lists[0]

def parallel_sort(data: list[int], num_processes: int = 4) -> list[int]:
    if len(data) == 0:
        return []

    # ── Step 1: Partition ──────────────────────────────────────────────────
    chunk_size = len(data) // num_processes
    chunks = [
        data[i : i + chunk_size]
        for i in range(0, len(data), chunk_size)
    ]

    # ── Step 2 & 3: Sort chunks in parallel ───────────────────────────────
    with Pool(processes=num_processes) as pool:
        sorted_chunks = pool.map(_sort_chunk, chunks)

    # ── Step 4: Merge sorted chunks ───────────────────────────────────────
    return merge_sorted_halves(sorted_chunks)
    
if __name__ == "__main__":
    import random
    import time

    sample = [random.randint(1, 1_000_000) for _ in range(10_000)]
    start  = time.time()
    result = parallel_sort(sample, num_processes=4)
    elapsed = time.time() - start

    print(f"Parallel Merge Sort — 10,000 elements | 4 processes")
    print(f"  First 10 sorted: {result[:10]}")
    print(f"  Elapsed time:    {elapsed:.4f}s")
    print(f"  Correctly sorted: {result == sorted(sample)}")
