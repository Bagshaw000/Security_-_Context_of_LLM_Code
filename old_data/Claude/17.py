import tkinter as tk
from tkinter import ttk

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.task_list = []

        self.task_input = ttk.Entry(master)
        self.task_input.pack(pady=10)

        self.add_button = ttk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(master, width=30, height=10)
        self.task_listbox.pack(pady=10)

        self.delete_button = ttk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

    def add_task(self):
        task = self.task_input.get().strip()
        if task:
            self.task_list.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_input.delete(0, tk.END)

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.task_list.pop(selected[0])
            self.task_listbox.delete(selected[0])

root = tk.Tk()
app = TodoApp(root)
root.mainloop()