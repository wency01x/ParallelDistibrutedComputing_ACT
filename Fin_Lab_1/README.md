# Distributed Order Processing Challenge

## Reflection Questions

**1. How did you distribute orders among worker processes?**
We established a master-worker architecture using `mpi4py`. The master process (Rank 0) generated a list of 6 customer orders and distributed them to the available worker processes using `comm.send()`. We used a modulo operator `(i % active_workers) + 1` to route the tasks evenly.

**2. What happens if there are more orders than workers?**
Because of our routing loop, the master process simply cycles back to the first worker process and continues distributing the remaining orders. The workers pull tasks from their message queues sequentially.

**3. How did processing delays affect the order completion?**
By using `time.sleep()` to simulate processing time, the order of task completion became asynchronous. A task assigned later could finish before an earlier task if it was given a shorter randomized sleep delay.

**4. How did you implement shared memory, and where was it initialized?**
We implemented shared memory using `Manager().list()` from the `multiprocessing` library. It was initialized at the beginning of the `main()` function before the processes diverge, creating a shared structure accessible to the workers.

**5. What issues occurred when multiple workers wrote to shared memory simultaneously?**
Without synchronization, multiple worker processes attempted to append to the shared list at the exact same time. This caused race conditions, leading to missing data and inconsistent final outputs.

**6. How did you ensure consistent results when using multiple processes?**
We used `Lock()` from the `multiprocessing` library. By wrapping the append action inside a `with lock:` critical section, we ensured that only one worker process could write to the shared memory list at a time.
