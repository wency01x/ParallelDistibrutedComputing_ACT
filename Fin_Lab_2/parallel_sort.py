from multiprocessing import Pool
from sequential_sort import merge

def _sort_chunk(chunk: list[int]) -> list[int]:
    from sequential_sort import merge_sort
    return merge_sort(chunk)
