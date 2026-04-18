from multiprocessing import Pool
from sequential_sort import merge

def _sort_chunk(chunk: list[int]) -> list[int]:
    """
    Worker function: receives a chunk of data and returns it sorted.
    This runs inside a separate process spawned by the Pool.

    We reuse our own sequential merge_sort logic on each sub-chunk so that
    every process does real divide-and-conquer work independently.
    """
    from sequential_sort import merge_sort
    return merge_sort(chunk)

def merge_sorted_halves(sorted_lists: list[list[int]]) -> list[int]:
    """
    Iteratively merge a collection of individually sorted lists into one
    globally sorted list using the same merge() helper from sequential_sort.

    Strategy: tournament-style pairwise merge until one list remains.
    This keeps the merge step at O(n log k) where k is the number of chunks.
    """
    while len(sorted_lists) > 1:
        merged = []
        # Pair up adjacent sorted lists and merge each pair
        for i in range(0, len(sorted_lists), 2):
            if i + 1 < len(sorted_lists):
                merged.append(merge(sorted_lists[i], sorted_lists[i + 1]))
            else:
                # Odd one out — carry it forward unchanged
                merged.append(sorted_lists[i])
        sorted_lists = merged
    return sorted_lists[0]

def parallel_sort(data: list[int], num_processes: int = 4) -> list[int]:
    """
    Parallel Merge Sort using Python's multiprocessing.Pool.

    Steps:
      1. Partition data into `num_processes` roughly equal chunks.
      2. Dispatch each chunk to a worker process via Pool.map().
      3. Collect the sorted chunks from all workers.
      4. Merge all sorted chunks into one globally sorted result.

    Note: Pool.map() blocks until ALL worker processes finish, then
    returns results in the same order as the input iterable.
    """
    if len(data) == 0:
        return []
