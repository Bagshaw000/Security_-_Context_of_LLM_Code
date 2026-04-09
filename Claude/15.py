import tkinter as tk
from datetime import datetime

class TodoListApp:
    def __init__(self, master):
        self.master = master
        master.title("Todo List App")

        self.todo_list = []
        self.completed_list = []

        self.task_entry = tk.Entry(master)
        self.task_entry.pack()

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.todo_listbox = tk.Listbox(master, width=50)
        self.todo_listbox.pack()

        self.complete_button = tk.Button(master, text="Complete Task", command=self.complete_task)
        self.complete_button.pack()

        self.completed_listbox = tk.Listbox(master, width=50)
        self.completed_listbox.pack()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.todo_list.append((task, datetime.now()))
            self.todo_listbox.insert(tk.END, f"{task} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.task_entry.delete(0, tk.END)

    def complete_task(self):
        selected = self.todo_listbox.curselection()
        if selected:
            task, timestamp = self.todo_list.pop(selected[0])
            self.completed_list.append((task, timestamp))
            self.completed_listbox.insert(tk.END, f"{task} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            self.todo_listbox.delete(selected)

root = tk.Tk()
app = TodoListApp(root)
root.mainloop()