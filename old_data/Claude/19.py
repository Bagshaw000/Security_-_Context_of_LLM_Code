import tkinter as tk

class TodoList:
    def __init__(self, master):
        self.master = master
        master.title("Todo List")

        self.todo_items = []

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.add_button = tk.Button(master, text="Add", command=self.add_todo)
        self.add_button.pack()

        self.listbox = tk.Listbox(master, width=50)
        self.listbox.pack()

        self.delete_button = tk.Button(master, text="Delete", command=self.delete_todo)
        self.delete_button.pack()

    def add_todo(self):
        todo = self.entry.get()
        if todo:
            self.todo_items.append(todo)
            self.listbox.insert(tk.END, todo)
            self.entry.delete(0, tk.END)

    def delete_todo(self):
        selected = self.listbox.curselection()
        if selected:
            self.todo_items.pop(selected[0])
            self.listbox.delete(selected[0])

root = tk.Tk()
app = TodoList(root)
root.mainloop()