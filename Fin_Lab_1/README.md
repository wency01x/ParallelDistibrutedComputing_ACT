# Laboratory 5: Distributed Data Ingestion Pipeline

## Reflection Questions

**1. How did you distribute orders among worker processes?**
We implemented an API Gateway architecture using `mpi4py`. The Gateway (Master Process / Rank 0) generates structured JSON payloads and distributes them to active Microservice Nodes (Worker Processes / Rank > 0) using `comm.send()`. We utilized a modulo-based partitioning logic `(i % active_nodes) + 1` to route the traffic evenly across the available worker nodes.

**2. What happens if there are more orders than workers?**
Our routing loop ensures that if the payload count exceeds the number of available nodes, the API Gateway cycles back to the first node and continues dispatching. The worker nodes utilize a `while True:` loop to continuously process their respective MPI message queues until a termination signal (`None`) is received.

**3. How did processing delays affect the order completion?**
We used `time.sleep()` to simulate real-world, I/O-bound database latency. Because each node received randomized sleep durations, tasks completed asynchronously. A payload dispatched later in the queue often finished processing before an earlier payload if it encountered a shorter simulated database delay.

**4. How did you implement shared memory, and where was it initialized?**
We initialized a centralized Data Lake using `multiprocessing.Manager().list()`. This was declared at the root level of our `main()` function prior to the rank-based process divergence, allowing all downstream parallel processes to access a unified proxy structure.
