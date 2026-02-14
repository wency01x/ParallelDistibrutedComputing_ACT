import concurrent.futures
import time
import threading

# Deduction Rates based on Lab PDF
SSS_RATE = 0.045
PHILHEALTH_RATE = 0.025
PAGIBIG_RATE = 0.02
TAX_RATE = 0.10

def calculate_sss(salary):
    # [cite_start]Optional enhancement: Displaying thread name [cite: 85]
    print(f"[{threading.current_thread().name}] Computing SSS...")
    time.sleep(0.1) # Simulate processing time
    return salary * SSS_RATE

def calculate_philhealth(salary):
    print(f"[{threading.current_thread().name}] Computing PhilHealth...")
    time.sleep(0.1)
    return salary * PHILHEALTH_RATE

def calculate_pagibig(salary):
    print(f"[{threading.current_thread().name}] Computing Pag-IBIG...")
    time.sleep(0.1)
    return salary * PAGIBIG_RATE

def calculate_tax(salary):
    print(f"[{threading.current_thread().name}] Computing Tax...")
    time.sleep(0.1)
    return salary * TAX_RATE

def main():
    print("--- Task Parallelism: Payroll for Single Employee (Harvie) ---")
    
    # [cite_start]Target Employee: Alice [cite: 29]
    employee_name = "Alice"
    salary = 25000.00
    
    print(f"Processing Payroll for: {employee_name} (Gross: {salary})")
    
    # [cite_start]Using ThreadPoolExecutor for independent tasks sharing memory [cite: 74]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_sss = executor.submit(calculate_sss, salary)
        future_philhealth = executor.submit(calculate_philhealth, salary)
        future_pagibig = executor.submit(calculate_pagibig, salary)
        future_tax = executor.submit(calculate_tax, salary)
        
        # [cite_start]Retrieving results [cite: 81]
        sss = future_sss.result()
        philhealth = future_philhealth.result()
        pagibig = future_pagibig.result()
        tax = future_tax.result()

    total_deduction = sss + philhealth + pagibig + tax
    net_salary = salary - total_deduction

    print("\n--- Deduction Breakdown ---")
    print(f"SSS (4.5%):        {sss:.2f}")
    print(f"PhilHealth (2.5%): {philhealth:.2f}")
    print(f"Pag-IBIG (2%):     {pagibig:.2f}")
    print(f"Tax (10%):         {tax:.2f}")
    print("---------------------------")
    print(f"Total Deductions:  {total_deduction:.2f}")
    print(f"Net Salary:        {net_salary:.2f}")

if __name__ == "__main__":
    main()