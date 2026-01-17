# Member 1: Wency Casino
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def main():
    while True:
        print("\n--- Simple Calculator ---")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply (Coming Soon)")
        print("4. Divide (Coming Soon)")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ")
        
        if choice == '5':
            print("Exiting...")
            break
            
        if choice in ('1', '2', '3', '4'):
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == '1':
                print(f"Result: {add(num1, num2)}")
            elif choice == '2':
                print(f"Result: {subtract(num1, num2)}")
            else:
                print("Member 2 needs to implement this!")
        else:
            print("Invalid Input")

if __name__ == "__main__":
    main()