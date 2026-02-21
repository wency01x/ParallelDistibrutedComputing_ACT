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