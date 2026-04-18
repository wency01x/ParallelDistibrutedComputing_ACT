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

    # ── Step 1: Partition with offsets ────────────────────────────────────
    chunk_size = len(data) // num_processes
    chunks: list[tuple[list[int], int]] = []

    for i in range(0, len(data), chunk_size):
        chunk  = data[i : i + chunk_size]
        offset = i
        chunks.append((chunk, offset))

    # ── Step 2: Spawn worker processes ────────────────────────────────────
    q         = Queue()
    processes = []

    for chunk, offset in chunks:
        p = Process(target=worker, args=(chunk, target, q, offset))
        processes.append(p)
        p.start()

    # ── Step 3: Collect results ───────────────────────────────────────────
    results = []
    for _ in processes:
        results.append(q.get())   # blocks until each worker puts a result

    # Wait for all processes to fully terminate
    for p in processes:
        p.join()

    # ── Step 4: Resolve final answer ──────────────────────────────────────
    valid_indices = [r for r in results if r != -1]
    if not valid_indices:
        return -1                          # not found in any chunk
    return min(valid_indices)             # earliest occurrence in original list


if __name__ == "__main__":
    import random
    import time

    data   = [random.randint(1, 1_000_000) for _ in range(100_000)]
    target = data[random.randint(0, len(data) - 1)]  # guaranteed hit

    start   = time.time()
    result  = parallel_search(data, target, num_processes=4)
    elapsed = time.time() - start

    print(f"Parallel Linear Search — 100,000 elements | 4 processes")
    print(f"  Target: {target}")
    print(f"  Found at global index: {result}")
    print(f"  Elapsed time:          {elapsed:.6f}s")
    print(f"  Correct index:         {data.index(target)}")

    # Test a miss
    miss = parallel_search(data, -1, num_processes=4)
    print(f"  Search for -1 (not in list): index = {miss}")
