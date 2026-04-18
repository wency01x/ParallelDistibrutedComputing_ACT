from multiprocessing import Process, Queue

def worker(sub_data: list[int], target: int, q: Queue, offset: int) -> None:
    for local_index, value in enumerate(sub_data):
        if value == target:
            global_index = offset + local_index
            q.put(global_index)  
            return

    q.put(-1) 
