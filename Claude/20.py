import tkinter as tk
from datetime import datetime

class TodoList:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.tasks = []
        self.task_entries = []

        self.task_entry = tk.Entry(master)
        self.task_entry.pack()

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(master, width=50)
        self.task_listbox.pack()

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.tasks.append((task, timestamp))
            self.task_listbox.insert(tk.END, f"{task} - {timestamp}")
            self.task_entries.append(self.task_entry)
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.task_listbox.delete(selected)
            del self.tasks[selected[0]]
            self.task_entries[selected[0]].delete(0, tk.END)
            del self.task_entries[selected[0]]

root = tk.Tk()
todo_list = TodoList(root)
root.mainloop()