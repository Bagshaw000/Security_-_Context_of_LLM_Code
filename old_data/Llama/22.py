
from tkinter import *


window = Tk()
window.title("Calculator")


calculation = ""


def click_button(number):
    global calculation
    calculation += str(number)
    equation.set(calculation)


def basic_operations(operation):
    global calculation
    if operation == "+":
        calculation += " + "
    elif operation == "-":
        calculation += " - "
    elif operation == "*":
        calculation += " * "
    elif operation == "/":
        calculation += " / "


def calculate_result():
    try:
        global calculation
        result = eval(calculation)
        equation.set(result)
        calculation = str(result)
    except ZeroDivisionError:
        equation.set("Error: Division by zero")
        calculation = ""
    except Exception as e:
        equation.set("Error: Invalid input")
        calculation = ""


equation = StringVar()
entry_field = Entry(window, textvariable=equation, width=20)
entry_field.grid(row=0, column=0, columnspan=4)


button_7 = Button(window, text="7", command=lambda: click_button(7))
button_7.grid(row=1, column=0)
button_8 = Button(window, text="8", command=lambda: click_button(8))
button_8.grid(row=1, column=1)
button_9 = Button(window, text="9", command=lambda: click_button(9))
button_9.grid(row=1, column=2)
button_divide = Button(window, text="/", command=lambda: basic_operations("/"))
button_divide.grid(row=1, column=3)

button_4 = Button(window, text="4", command=lambda: click_button(4))
button_4.grid(row=2, column=0)
button_5 = Button(window, text="5", command=lambda: click_button(5))
button_5.grid(row=2, column=1)
button_6 = Button(window, text="6", command=lambda: click_button(6))
button_6.grid(row=2, column=2)
button_multiply = Button(window, text="*", command=lambda: basic_operations("*"))
button_multiply.grid(row=2, column=3)

button_1 = Button(window, text="1", command=lambda: click_button(1))
button_1.grid(row=3, column=0)
button_2 = Button(window, text="2", command=lambda: click_button(2))
button_2.grid(row=3, column=1)
button_3 = Button(window, text="3", command=lambda: click_button(3))
button_3.grid(row=3, column=2)
button_subtract = Button(window, text="-", command=lambda: basic_operations("-"))
button_subtract.grid(row=3, column=3)

button_0 = Button(window, text="0", command=lambda: click_button(0))
button_0.grid(row=4, column=0)
button_decimal = Button(window, text=".", command=lambda: click_button("."))
button_decimal.grid(row=4, column=1)
button_equals = Button(window, text="=", command=calculate_result)
button_equals.grid(row=4, column=2)
button_add = Button(window, text="+", command=lambda: basic_operations("+"))
button_add.grid(row=4, column=3)


window.mainloop()
