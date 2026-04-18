from multiprocessing import Process, Queue

def worker(sub_data: list[int], target: int, q: Queue, offset: int) -> None:
    for local_index, value in enumerate(sub_data):
        if value == target:
            global_index = offset + local_index
            q.put(global_index)  
            return

    q.put(-1) 
def parallel_search(data: list[int], target: int, num_processes: int = 4) -> int:
    if len(data) == 0:
        return -1

    chunk_size = len(data) // num_processes
    chunks: list[tuple[list[int], int]] = []

    for i in range(0, len(data), chunk_size):
        chunk  = data[i : i + chunk_size]
        offset = i
        chunks.append((chunk, offset))

    q         = Queue()
    processes = []

    for chunk, offset in chunks:
        p = Process(target=worker, args=(chunk, target, q, offset))
        processes.append(p)
        p.start()

    results = []
    for _ in processes:
        results.append(q.get())  

    for p in processes:
        p.join()

    valid_indices = [r for r in results if r != -1]
    if not valid_indices:
        return -1                      
    return min(valid_indices)           
