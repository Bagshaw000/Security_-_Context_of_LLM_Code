import tkinter as tk

class TodoList:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.task_list = []
        self.task_entries = []

        self.label = tk.Label(master, text="Todo List")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.entry = tk.Entry(master)
        self.entry.grid(row=1, column=0, padx=10, pady=10)

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=1, padx=10, pady=10)

        self.task_frame = tk.Frame(master)
        self.task_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def add_task(self):
        task = self.entry.get()
        if task:
            self.task_list.append(task)
            self.entry.delete(0, tk.END)
            self.display_tasks()

    def display_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for i, task in enumerate(self.task_list):
            task_entry = tk.Entry(self.task_frame)
            task_entry.insert(0, task)
            task_entry.grid(row=i, column=0, padx=5, pady=5)
            self.task_entries.append(task_entry)

            delete_button = tk.Button(self.task_frame, text="Delete", command=lambda i=i: self.delete_task(i))
            delete_button.grid(row=i, column=1, padx=5, pady=5)

    def delete_task(self, index):
        self.task_list.pop(index)
        self.task_entries.pop(index)
        self.display_tasks()

root = tk.Tk()
todo_list = TodoList(root)
root.mainloop()