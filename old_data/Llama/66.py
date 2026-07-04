
import operator as op

def calculate(expression):
    try:
        
        operations = {
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
        }

        
        result = eval(expression)

        return result

    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")

    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    while True:
        
        expression = input("Enter a mathematical expression (or 'q' to quit): ")

        if expression.lower() == 'q':
            break

        try:
            
            result = calculate(expression)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
