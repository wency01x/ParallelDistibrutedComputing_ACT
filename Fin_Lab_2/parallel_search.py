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
