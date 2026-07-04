import tkinter as tk
from datetime import date

class TodoList:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.tasks = []
        self.task_entries = []

        self.task_label = tk.Label(master, text="Task:")
        self.task_label.pack()

        self.task_entry = tk.Entry(master)
        self.task_entry.pack()

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.list_box = tk.Listbox(master, width=50)
        self.list_box.pack()

        self.remove_button = tk.Button(master, text="Remove Task", command=self.remove_task)
        self.remove_button.pack()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.list_box.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def remove_task(self):
        selected = self.list_box.curselection()
        if selected:
            self.tasks.pop(selected[0])
            self.list_box.delete(selected[0])

root = tk.Tk()
todo_list = TodoList(root)
root.mainloop()