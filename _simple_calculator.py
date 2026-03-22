# ============================================================
# Level 1 - Task 1: Simple Calculator
# Codveda Python Development Internship
# ============================================================

def add(a, b):
    """Return the sum of a and b."""
    return a + b

def subtract(a, b):
    """Return the difference of a and b."""
    return a - b

def multiply(a, b):
    """Return the product of a and b."""
    return a * b

def divide(a, b):
    """Return the quotient of a divided by b. Handles division by zero."""
    if b == 0:
        raise ValueError("Error: Division by zero is not allowed.")
    return a / b

def get_number(prompt):
    """Prompt the user for a valid float input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def calculator():
    print("=" * 40)
    print("       Simple Calculator")
    print("=" * 40)

    operations = {
        "1": ("Addition (+)",       add),
        "2": ("Subtraction (-)",    subtract),
        "3": ("Multiplication (*)", multiply),
        "4": ("Division (/)",       divide),
    }

    while True:
        print("\nSelect an operation:")
        for key, (label, _) in operations.items():
            print(f"  {key}. {label}")
        print("  5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "5":
            print("Goodbye!")
            break

        if choice not in operations:
            print("Invalid choice. Please select 1-5.")
            continue

        num1 = get_number("Enter the first number:  ")
        num2 = get_number("Enter the second number: ")

        label, func = operations[choice]
        try:
            result = func(num1, num2)
            print(f"\nResult: {num1} {label.split()[1]} {num2} = {result}")
        except ValueError as e:
            print(f"\n{e}")

if __name__ == "__main__":
    calculator()
