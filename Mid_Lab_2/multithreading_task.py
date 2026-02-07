import threading
import time


def compute_gwa(student_name, grades):
    # Simulating a slight delay to visualize threading
    time.sleep(0.5)
    gwa = sum(grades) / len(grades)
    print(f" [Thread] {student_name}: GWA = {gwa:.2f}")


def main():
    print("--- Multithreading Grade Calculator (By Harvie) ---")
    try:
        num_students = int(input("How many students? "))
        student_data = []

        # Collecting input
        for _ in range(num_students):
            name = input("Enter student name: ")
            grades_str = input(f"Enter grades for {name} (separated by space): ")
            grades = [float(g) for g in grades_str.split()]
            student_data.append((name, grades))

        print("\nStarting Threaded Calculation...")
        start_time = time.time()
        threads = []

        # Creating threads
        for name, grades in student_data:
            t = threading.Thread(target=compute_gwa, args=(name, grades))
            threads.append(t)
            t.start()

        # Waiting for threads to finish
        for t in threads:
            t.join()

        end_time = time.time()
        print(f"\nTotal Execution Time: {end_time - start_time:.4f} seconds")

    except ValueError:
        print("Invalid input. Please enter numbers correctly.")


if __name__ == "__main__":
    main()