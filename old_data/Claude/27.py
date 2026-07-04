import tkinter as tk

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.task_entry = tk.Entry(master)
        self.task_entry.pack()

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_list = tk.Listbox(master)
        self.task_list.pack()

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

    def add_task(self):
        task = self.task_entry.get()
        if task.strip():
            self.task_list.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        selected = self.task_list.curselection()
        if selected:
            self.task_list.delete(selected)

root = tk.Tk()
app = TodoApp(root)
root.mainloop()