import tkinter as tk

class TodoList:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.tasks = []
        self.task_entries = []

        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=10)

        self.task_entry = tk.Entry(self.input_frame, width=30)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.input_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.list_frame = tk.Frame(master)
        self.list_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.list_frame, width=40)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_bar = tk.Scrollbar(self.list_frame)
        self.scroll_bar.pack(side=tk.LEFT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.task_listbox.yview)

        self.delete_button = tk.Button(self.list_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.tasks.pop(selected[0])
            self.task_listbox.delete(selected)

root = tk.Tk()
todo_list = TodoList(root)
root.mainloop()