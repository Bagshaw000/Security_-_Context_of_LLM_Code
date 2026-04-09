import tkinter as tk

def calculate():
    try:
        value1 = float(entry1.get())
        value2 = float(entry2.get())
        operator = var.get()
        if operator == "+":
            result = value1 + value2
        elif operator == "-":
            result = value1 - value2
        elif operator == "*":
            result = value1 * value2
        elif operator == "/":
            result = value1 / value2
        else:
            result = "Invalid operator"
        output.delete(0, tk.END)
        output.insert(0, str(result))
    except ValueError:
        output.delete(0, tk.END)
        output.insert(0, "Invalid input")

root = tk.Tk()
root.title("Calculator")

var = tk.StringVar()
var.set("+")

label1 = tk.Label(root, text="Value 1:")
label1.grid(row=0, column=0)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1)

label2 = tk.Label(root, text="Value 2:")
label2.grid(row=1, column=0)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1)

operators = ["+", "-", "*", "/"]
for i, op in enumerate(operators):
    tk.Radiobutton(root, text=op, variable=var, value=op).grid(row=2, column=i)

button = tk.Button(root, text="Calculate", command=calculate)
button.grid(row=3, column=0, columnspan=2)

output = tk.Entry(root)
output.grid(row=4, column=0, columnspan=2)

root.mainloop()