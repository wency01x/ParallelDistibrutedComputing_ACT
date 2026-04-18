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
