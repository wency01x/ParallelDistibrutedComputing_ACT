# Laboratory 3: Applying Task and Data Parallelism

## Group Members
* **Harvie Lorenz C. Babuyo:** Implemented `task_parallelism.py` (Task Parallelism)
* **Kerby B. Fabria:** Implemented `data_parallelism.py` (Data Parallelism)
* **Wency G. Casiño:** Analysis, Documentation, and Repository Management

---

## Analysis Questions

**1. Differentiate Task and Data Parallelism. Identify which part of the lab demonstrates each.**
* **Task Parallelism** focuses on distributing different *functions* or tasks across threads or processes. In our lab, **Part A** demonstrates this by calculating SSS, PhilHealth, Pag-IBIG, and Tax as separate tasks running concurrently for a single employee.
* **Data Parallelism** focuses on distributing different *subsets of data* across multiple cores. **Part B** demonstrates this by applying the same payroll function to a list of 5 different employees simultaneously.

**2. Explain how concurrent.futures managed execution, including submit(), map(), and Future objects.**
* `submit()`: Used in Part A, it schedules a callable (function) to be executed and returns a `Future` object representing the execution.
* `map()`: Used in Part B, it applies a function to every item in an iterable (list of employees) concurrently, returning the results in the order they were started.
* `Future objects`: These act as placeholders for results that haven't been computed yet. In Part A, we used `.result()` to retrieve the value from the Future once the thread completed its task.

**3. Analyze ThreadPoolExecutor execution in relation to the GIL and CPU cores.**
`ThreadPoolExecutor` uses threads, which run within a single process and share the same memory space. Due to Python's **Global Interpreter Lock (GIL)**, only one thread can execute Python bytecode at a time. Therefore, true parallelism (simultaneous CPU execution) did not occur; instead, the threads switched context very quickly (concurrency), which is efficient for I/O-bound tasks but not for heavy CPU calculations.

**4. Explain why ProcessPoolExecutor enables true parallelism.**
`ProcessPoolExecutor` bypasses the GIL by creating separate Python processes. Each process has its own instance of the Python interpreter and its own memory space. This allows them to run on different CPU cores at the exact same time, achieving true parallelism.

**5. Evaluate scalability if the system increases from 5 to 10,000 employees.**
* **Data Parallelism (ProcessPoolExecutor)** scales much better. With 10,000 employees, the workload can be split across all available CPU cores, significantly reducing processing time.
* Task Parallelism would be inefficient because creating thousands of threads or managing distinct tasks for every single employee would introduce massive overhead and memory consumption.

**6. Real-world payroll system example.**
* **Data Parallelism Scenario:** Calculating the final net pay for 5,000 factory workers at the end of the month. I would use `ProcessPoolExecutor` to distribute the list of employees across cores to finish the batch job quickly.
* **Task Parallelism Scenario:** Generating a real-time pay slip view for a user. When they click "View Payslip," the system uses `ThreadPoolExecutor` to simultaneously fetch their attendance records, query the tax database, and retrieve their loan balance from different servers.


