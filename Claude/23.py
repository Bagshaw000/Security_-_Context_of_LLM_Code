import tkinter as tk
from datetime import datetime

class TodoList:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.tasks = []
        self.task_entries = []

        self.label = tk.Label(master, text="Todo List")
        self.label.pack()

        self.task_entry = tk.Entry(master)
        self.task_entry.pack()

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.list_box = tk.Listbox(master)
        self.list_box.pack()

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.save_button = tk.Button(master, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.list_box.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        selected = self.list_box.curselection()
        if selected:
            self.tasks.pop(selected[0])
            self.list_box.delete(selected[0])

    def save_tasks(self):
        with open("todo_list.txt", "w") as f:
            for task in self.tasks:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {task}\n")

root = tk.Tk()
todo_list = TodoList(root)
root.mainloop()