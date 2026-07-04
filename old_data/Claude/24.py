import tkinter as tk

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.task_list = []
        self.completed_tasks = []

        self.task_entry = tk.Entry(master)
        self.task_entry.pack()

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.list_box = tk.Listbox(master, width=50)
        self.list_box.pack()

        self.complete_button = tk.Button(master, text="Complete Task", command=self.complete_task)
        self.complete_button.pack()

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.task_list.append(task)
            self.list_box.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def complete_task(self):
        selected_tasks = self.list_box.curselection()
        for index in reversed(selected_tasks):
            task = self.task_list.pop(index)
            self.completed_tasks.append(task)
            self.list_box.delete(index)

    def delete_task(self):
        selected_tasks = self.list_box.curselection()
        for index in reversed(selected_tasks):
            self.task_list.pop(index)
            self.list_box.delete(index)

root = tk.Tk()
app = TodoApp(root)
root.mainloop()