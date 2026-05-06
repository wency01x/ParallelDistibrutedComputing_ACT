# Distributed Order Processing Challenge

## Reflection Questions

**1. How did you distribute orders among worker processes?**
We established a master-worker architecture using `mpi4py`. The master process (Rank 0) generated a list of 6 customer orders and distributed them to the available worker processes using `comm.send()`. We used a modulo operator `(i % active_workers) + 1` to route the tasks evenly.

**2. What happens if there are more orders than workers?**
Because of our routing loop, the master process simply cycles back to the first worker process and continues distributing the remaining orders. The workers pull tasks from their message queues sequentially.
