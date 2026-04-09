here is the Python code for a calculator:

import tkinter as tk

def calculate():
    try:
        value = eval(entry.get())
        result.set(value)
    except:
        result.set("Error")

root = tk.Tk()
root.title("Calculator")

entry = tk.Entry(root, font=("Arial", 20))
entry.pack(pady=10)

button = tk.Button(root, text="Calculate", command=calculate, font=("Arial", 16))
button.pack(pady=10)

result = tk.StringVar()
result_label = tk.Label(root, textvariable=result, font=("Arial", 20))
result_label.pack(pady=10)

root.mainloop()