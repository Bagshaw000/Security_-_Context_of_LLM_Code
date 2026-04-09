import tkinter as tk

class TodoList:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.task_list = []
        self.task_entry = tk.Entry(master)
        self.task_entry.pack()

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(master)
        self.task_listbox.pack()

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.task_list.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.task_list.pop(selected[0])
            self.task_listbox.delete(selected[0])

root = tk.Tk()
todo_list = TodoList(root)
root.mainloop()