
from tkinter import *
import math


root = Tk()
root.title("Calculator Application")


def update_display(num):
    current_value = entry.get()
    new_value = current_value + str(num)
    entry.delete(0, END)
    entry.insert(0, new_value)


def calculate():
    try:
        value = eval(entry.get())
        entry.delete(0, END)
        entry.insert(0, value)
    except Exception as e:
        entry.delete(0, END)
        entry.insert(0, "Error")


def clear():
    entry.delete(0, END)


expression = ""


entry = Entry(root, width=35, borderwidth=5)
entry.grid(row=0, column=0, columnspan=4)


button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: update_display(1))
button_1.grid(row=3, column=0)

button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: update_display(2))
button_2.grid(row=3, column=1)

button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: update_display(3))
button_3.grid(row=3, column=2)

button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: update_display(4))
button_4.grid(row=2, column=0)

button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: update_display(5))
button_5.grid(row=2, column=1)

button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: update_display(6))
button_6.grid(row=2, column=2)

button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: update_display(7))
button_7.grid(row=1, column=0)

button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: update_display(8))
button_8.grid(row=1, column=1)

button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: update_display(9))
button_9.grid(row=1, column=2)

button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: update_display(0))
button_0.grid(row=4, column=0)


button_add = Button(root, text="+", padx=39, pady=20, command=lambda: update_display("+"))
button_add.grid(row=1, column=3)

button_subtract = Button(root, text="-", padx=40, pady=20, command=lambda: update_display("-"))
button_subtract.grid(row=2, column=3)

button_multiply = Button(root, text="*", padx=41, pady=20, command=lambda: update_display("*"))
button_multiply.grid(row=3, column=3)

button_divide = Button(root, text="/", padx=40, pady=20, command=lambda: update_display("/"))
button_divide.grid(row=4, column=3)

button_equal = Button(root, text="=", padx=39, pady=20, command=calculate)
button_equal.grid(row=4, column=2)

button_clear = Button(root, text="Clear", padx=29, pady=20, command=clear)
button_clear.grid(row=4, column=1)


root.mainloop()
