
import tkinter as tk

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.entry = tk.Entry(self.window, width=40, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=4)

        
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
                tk.Button(self.window, text=button, width=10, command=self.calculate).grid(row=row_val, column=col_val)
            else:
                tk.Button(self.window, text=button, width=10, command=lambda button=button: self.append_to_entry(button)).grid(row=row_val, column=col_val)

            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        
        tk.Button(self.window, text="Clear", width=21, command=self.clear).grid(row=row_val, column=0, columnspan=2)

        
        tk.Button(self.window, text="Backspace", width=10, command=self.remove_last_char).grid(row=row_val, column=2, columnspan=2)

    def append_to_entry(self, value):
        self.entry.insert(tk.END, value)

    def remove_last_char(self):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current[:-1])

    def calculate(self):
        try:
            result = str(eval(self.entry.get()))
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    def clear(self):
        self.entry.delete(0, tk.END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()
