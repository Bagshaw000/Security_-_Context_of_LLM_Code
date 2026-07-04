
import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, master):
        self.master = master
        self.entry = tk.Entry(master, width=35, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4)

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            if button == '=':
                tk.Button(self.master, text=button, width=10, command=self.calculate).grid(row=row_val, column=col_val)
            else:
                tk.Button(self.master, text=button, width=10, command=lambda button=button: self.append_to_entry(button)).grid(row=row_val, column=col_val)

            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        tk.Button(self.master, text="Clear", width=21, command=self.clear_entry).grid(row=row_val, column=0, columnspan=2)
        tk.Button(self.master, text="Delete", width=21, command=self.delete_char).grid(row=row_val, column=2, columnspan=2)

    def append_to_entry(self, value):
        current_value = self.entry.get()
        new_value = current_value + value
        self.entry.delete(0, tk.END)
        self.entry.insert(0, new_value)

    def calculate(self):
        try:
            result = str(eval(self.entry.get()))
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except Exception as e:
            messagebox.showerror("Error", "Invalid input")

    def clear_entry(self):
        self.entry.delete(0, tk.END)

    def delete_char(self):
        current_value = self.entry.get()
        self.entry.delete(0, tk.END)
        for char in current_value:
            if char != ' ':
                self.entry.insert(0, char)
                break

root = tk.Tk()
root.title("Calculator")
calc = Calculator(root)
root.mainloop()
