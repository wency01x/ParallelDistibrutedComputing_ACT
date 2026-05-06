# Laboratory 5: Distributed Data Ingestion Pipeline

## Reflection Questions

**1. How did you distribute orders among worker processes?**
We implemented an API Gateway architecture using `mpi4py`. The Gateway (Master Process / Rank 0) generates structured JSON payloads and distributes them to active Microservice Nodes (Worker Processes / Rank > 0) using `comm.send()`. We utilized a modulo-based partitioning logic `(i % active_nodes) + 1` to route the traffic evenly across the available worker nodes.

**2. What happens if there are more orders than workers?**
Our routing loop ensures that if the payload count exceeds the number of available nodes, the API Gateway cycles back to the first node and continues dispatching. The worker nodes utilize a `while True:` loop to continuously process their respective MPI message queues until a termination signal (`None`) is received.
