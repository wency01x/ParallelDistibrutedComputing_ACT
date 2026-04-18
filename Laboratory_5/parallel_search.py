from multiprocessing import Process, Queue

def worker(sub_data: list[int], target: int, q: Queue, offset: int) -> None:
    """
    Worker process: searches sub_data for target and puts results into the queue.

    Parameters
    ----------
    sub_data : list[int]
        The chunk of the original dataset assigned to this process.
    target   : int
        The value to search for.
    q        : Queue
        Shared queue used to communicate results back to the main process.
    offset   : int
        The starting index of sub_data within the full dataset.
        Used to convert a local index into a global index.
    """
    for local_index, value in enumerate(sub_data):
        if value == target:
            global_index = offset + local_index
            q.put(global_index)   # Report the global index and stop early
            return

    q.put(-1)  # Signal "not found in this chunk"

def parallel_search(data: list[int], target: int, num_processes: int = 4) -> int:
    """
    Parallel Linear Search using multiprocessing.Process and Queue.

    Steps:
      1. Divide data into `num_processes` chunks, tracking each chunk's offset.
      2. Spawn one Process per chunk; each worker searches its chunk independently.
      3. Collect results from the shared Queue as workers finish.
      4. Return the smallest valid global index found, or -1 if not found anywhere.

    Why Queue?
    ----------
    Queue is a thread/process-safe FIFO. Each worker puts() its result (a global
    index or -1) into the queue. The main process get()s one result per worker
    and decides the final answer.

    Note on correctness:
    --------------------
    Because workers run concurrently, results may arrive out of order. We collect
    ALL results and then pick the minimum valid index to guarantee we return the
    FIRST occurrence in the original list.
    """
    if len(data) == 0:
        return -1
