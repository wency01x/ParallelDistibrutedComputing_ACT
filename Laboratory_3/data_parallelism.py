import concurrent.futures
import time
import os

# [cite_start]Deduction Rates [cite: 19-23]
SSS_RATE = 0.045
PHILHEALTH_RATE = 0.025
PAGIBIG_RATE = 0.02
TAX_RATE = 0.10

# [cite_start]Employee Data [cite: 29-33]
employees = [
    ("Alice", 25000),
    ("Bob", 32000),
    ("Charlie", 28000),
    ("Diana", 40000),
    ("Edward", 35000)
]

def process_payroll(employee):
    name, salary = employee
    
    # Calculate deductions
    deduction = salary * (SSS_RATE + PHILHEALTH_RATE + PAGIBIG_RATE + TAX_RATE)
    net_salary = salary - deduction
    
    # Optional: Show process ID to prove parallelism
    pid = os.getpid()
    
    return f"PID: {pid} | {name:<10} | Gross: {salary:<8} | Deductions: {deduction:<8.2f} | Net: {net_salary:<8.2f}"

def main():
    print("--- Data Parallelism: Batch Payroll Processing (Kerby) ---")
    print(f"Processing {len(employees)} employees concurrently...\n")

    start_time = time.time()

    # [cite_start]Using ProcessPoolExecutor for data parallelism [cite: 87]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(process_payroll, employees)

    # Display Results
    print(f"{'Process ID':<10} | {'Name':<10} | {'Gross':<8} | {'Deductions':<8} | {'Net':<8}")
    print("-" * 75)
    
    for res in results:
        print(res)

    print(f"\nBatch processing complete in {time.time() - start_time:.4f} seconds.")

if __name__ == "__main__":
    main()


