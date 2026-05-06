# Distributed Order Processing Challenge

## Reflection Questions

**1. How did you distribute orders among worker processes?**
We established a master-worker architecture using `mpi4py`. The master process (Rank 0) generated a list of 6 customer orders and distributed them to the available worker processes using `comm.send()`. We used a modulo operator `(i % active_workers) + 1` to route the tasks evenly.

**2. What happens if there are more orders than workers?**
Because of our routing loop, the master process simply cycles back to the first worker process and continues distributing the remaining orders. The workers pull tasks from their message queues sequentially.

**3. How did processing delays affect the order completion?**
By using `time.sleep()` to simulate processing time, the order of task completion became asynchronous. A task assigned later could finish before an earlier task if it was given a shorter randomized sleep delay.
