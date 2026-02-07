def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

def parse_number(value):
    return float(value) if '.' in value else int(value)

print("Select operation:")
print("1. Add")
print("2. Subtract")
print("3. Multiply")
print("4. Divide")

while True:
    choice = input("Enter choice(1/2/3/4): ")

    if choice == '1':
        num1 = parse_number(input("Enter first number: "))
        num2 = parse_number(input("Enter second number: "))

        result = add(num1, num2)
        print(num1, "+", num2, "=", result)

    elif choice == '2':
        num1 = parse_number(input("Enter first number: "))
        num2 = parse_number(input("Enter second number: "))
        result = subtract(num1, num2)
        print(num1, "-", num2, "=", result)

    elif choice == '3':
        num1 = parse_number(input("Enter first number: "))
        num2 = parse_number(input("Enter second number: "))
        result = multiply(num1, num2)
        print(num1, "*", num2, "=", result)

    elif choice == '4':
        num1 = parse_number(input("Enter first number: "))
        num2 = parse_number(input("Enter second number: "))
        result = divide(num1, num2)
        print(num1, "/", num2, "=", result)

        next_calculation = input("Let's do next calculation? (y/n): ")
        if next_calculation.lower() == 'y':
            continue
        else:
            print("Exiting the calculator. Goodbye!")
            break

    

