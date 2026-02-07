from multiprocessing import Process
import time

def compute_gwa_mp(student_name, grades):
    # Simulating work
    time.sleep(0.5)
    gwa = sum(grades) / len(grades)
    print(f" [Process] {student_name}: GWA = {gwa:.2f}")

def main():
    print("--- Multiprocessing Grade Calculator (By Kerby) ---")
    try:
        # Input must be gathered first in the main process
        num_students = int(input("How many students? "))
        student_data = []
        
        for _ in range(num_students):
            name = input("Enter student name: ")
            grades_str = input(f"Enter grades for {name} (separated by space): ")
            grades = [float(g) for g in grades_str.split()]
            student_data.append((name, grades))

        print("\nStarting Multi-Process Calculation...")
        start_time = time.time()
        processes = []

        # Creating and starting processes
        for name, grades in student_data:
            p = Process(target=compute_gwa_mp, args=(name, grades))
            processes.append(p)
            p.start()

        # Waiting for processes to finish
        for p in processes:
            p.join()

        end_time = time.time()
        print(f"\nTotal Execution Time: {end_time - start_time:.4f} seconds")

    except ValueError:
        print("Invalid input.")

if __name__ == "__main__":
    main()