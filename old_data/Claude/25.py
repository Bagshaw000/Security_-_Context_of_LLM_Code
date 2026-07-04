import tkinter as tk
from datetime import datetime


root = tk.Tk()
root.title("Todo List App")


tasks = []


def add_task():
    task = entry.get()
    if task:
        tasks.append({"task": task, "completed": False, "timestamp": datetime.now()})
        entry.delete(0, tk.END)
        update_listbox()


def complete_task(index):
    tasks[index]["completed"] = not tasks[index]["completed"]
    update_listbox()


def update_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        status = "[X]" if task["completed"] else "[ ]"
        listbox.insert(tk.END, f"{status} {task['task']}")


entry = tk.Entry(root)
entry.pack(pady=10)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=10)


listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

scrollbar = tk.Scrollbar(root, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)


listbox.bind("<<ListboxSelect>>", lambda event: complete_task(listbox.curselection()[0]))


root.mainloop()