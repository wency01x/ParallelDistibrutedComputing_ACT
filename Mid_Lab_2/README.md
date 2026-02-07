# Lab 2: Exploring Multithreading and Multiprocessing

## Group Members
* **Harvie Lorenz C. Babuyo:** Implemented `multithreading_task.py`
* **Kerby B. Fabria:** Implemented `multiprocessing_task.py`
* **Wency G. Casiño:** Repository Management & Documentation

## Performance Analysis
| Method | Execution Order | GWA Output | Execution Time |
| :--- | :--- | :--- | :--- |
| Multithreading | Mixed/Concurrent | Calculated Correctly | 0.5441 s |
| Multiprocessing | Parallel | Calculated Correctly | 0.8521 s |

## Answers to Guide Questions

**1. Which approach demonstrates true parallelism in Python? Explain.**
Multiprocessing demonstrates true parallelism. Because Python creates a separate memory space and interpreter for each process, they can run on different CPU cores at the exact same time, bypassing the Global Interpreter Lock (GIL).

**2. Compare execution times between multithreading and multiprocessing.**
For this specific small task, Multithreading is likely faster because creating threads is "cheaper" (uses less memory/setup time) than creating full processes. However, for heavy calculations, Multiprocessing would be faster.

**3. Can Python handle true parallelism using threads? Why or why not?**
No. Python threads are bound by the **Global Interpreter Lock (GIL)**, which ensures only one thread executes Python bytecode at a time. This means threads are concurrent (taking turns very fast), but not truly parallel.

**4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster?**
If we had to calculate 1000 GWAs:
* **Multiprocessing** would be faster if the calculation is very complex (CPU-bound).
* **Multithreading** is faster if the task involves waiting for data (I/O-bound) or if the calculation is simple, due to lower overhead.

**5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?**
* **CPU-Bound (Heavy Math):** Multiprocessing.
* **I/O-Bound (Downloading, User Input):** Multithreading.

**6. How did your group apply creative coding or algorithmic solutions in this lab?**
We designed a dynamic input system that accepts any number of students and grades. We also used formatted strings (f-strings) to ensure the output is readable and the GWA is rounded to two decimal places.

