



print("--- English Department Calculator ---")



first_number = float(input("Enter your first number: "))


operation = input("Enter the operation (+, -, *, /): ")


second_number = float(input("Enter your second number: "))



if operation == "+":
    result = first_number + second_number
elif operation == "-":
    result = first_number - second_number
elif operation == "*":
    result = first_number * second_number
elif operation == "/":
    
    if second_number == 0:
        result = "Error: Cannot divide by zero."
    else:
        result = first_number / second_number
else:
    result = "Error: Invalid operation symbol used."


print("Calculation Result:", result)

