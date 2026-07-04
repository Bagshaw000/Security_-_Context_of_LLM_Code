
from tkinter import *


root = Tk()
root.title("Calculator")


expression = ""


def press(num):
    global expression
    expression += str(num)
    equation.set(expression)


def clear():
    global expression
    expression = ""
    equation.set("")


def equalpress():
    try:
        global expression
        total = str(eval(expression))
        equation.set(total)
        expression = total
    except Exception as e:
        equation.set("Error")
        expression = ""


equation = StringVar()
entry_field = Entry(root, textvariable=equation, width=20)
entry_field.grid(row=0, column=0, columnspan=4)


button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: press(7))
button_7.grid(row=1, column=0)

button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: press(8))
button_8.grid(row=1, column=1)

button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: press(9))
button_9.grid(row=1, column=2)

button_divide = Button(root, text="/", padx=39, pady=20, command=lambda: press("/"))
button_divide.grid(row=1, column=3)


button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: press(4))
button_4.grid(row=2, column=0)

button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: press(5))
button_5.grid(row=2, column=1)

button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: press(6))
button_6.grid(row=2, column=2)

button_multiply = Button(root, text="*", padx=39, pady=20, command=lambda: press("*"))
button_multiply.grid(row=2, column=3)


button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: press(1))
button_1.grid(row=3, column=0)

button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: press(2))
button_2.grid(row=3, column=1)

button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: press(3))
button_3.grid(row=3, column=2)

button_subtract = Button(root, text="-", padx=39, pady=20, command=lambda: press("-"))
button_subtract.grid(row=3, column=3)


button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: press(0))
button_0.grid(row=4, column=1)

button_equal = Button(root, text="=", padx=38, pady=20, command=equalpress)
button_equal.grid(row=4, column=2)

button_add = Button(root, text="+", padx=39, pady=20, command=lambda: press("+"))
button_add.grid(row=4, column=3)


button_clear = Button(root, text="C", padx=21, pady=20, command=clear)
button_clear.grid(row=5, column=0, columnspan=2)

root.mainloop()
