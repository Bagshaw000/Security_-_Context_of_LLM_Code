import tkinter as tk
from tkinter import ttk

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.task_list = []

        self.input_label = ttk.Label(master, text="Enter a new task:")
        self.input_label.pack(pady=10)

        self.input_entry = ttk.Entry(master)
        self.input_entry.pack(pady=10)

        self.add_button = ttk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

        self.task_listbox = tk.Listbox(master, width=50)
        self.task_listbox.pack(pady=10)

        self.delete_button = ttk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=10)

    def add_task(self):
        task = self.input_entry.get().strip()
        if task:
            self.task_list.append(task)
            self.task_listbox.insert(tk.END, task)
            self.input_entry.delete(0, tk.END)

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task = self.task_list.pop(selected[0])
            self.task_listbox.delete(selected[0])

root = tk.Tk()
app = TodoApp(root)
root.mainloop()