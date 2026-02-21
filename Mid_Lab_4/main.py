import time
import random
from concurrent.futures import ThreadPoolExecutor

# Simulate 50 pageant candidates, each receiving scores from 5 judges
candidates_data = {f"Candidate_{i}": [random.randint(70, 100) for _ in range(5)] for i in range(1, 51)}

def calculate_score(candidate_name, scores):
    # Simulate heavy computation/delays in reading paper scores
    time.sleep(0.1) 
    average = sum(scores) / len(scores)
    return (candidate_name, average)

def run_sequential():
    start_time = time.time()
    results = []
    for name, scores in candidates_data.items():
        results.append(calculate_score(name, scores))
    return time.time() - start_time

def run_parallel():
    start_time = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Distributing the work units concurrently
        futures = [executor.submit(calculate_score, name, scores) for name, scores in candidates_data.items()]
        for future in futures:
            results.append(future.result())
    return time.time() - start_time

if __name__ == "__main__":
    print("Running Sequential Tabulation...")
    time_seq = run_sequential()
    
    print("Running Parallel Tabulation...")
    time_par = run_parallel()
    
    speedup = time_seq / time_par
    
    print("\n--- BENCHMARK REPORT ---")
    print(f"Sequential Time: {time_seq:.2f} seconds")
    print(f"Parallel Time:   {time_par:.2f} seconds")
    print(f"Speedup Ratio:   {speedup:.2f}")