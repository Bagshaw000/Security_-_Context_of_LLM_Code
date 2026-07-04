import tkinter as tk


root = tk.Tk()
root.title("Todo List App")


tasks = []


def add_task():
    task = entry.get()
    if task:
        tasks.append(task)
        entry.delete(0, tk.END)
        update_listbox()


def remove_task():
    selected = listbox.curselection()
    if selected:
        tasks.pop(selected[0])
        update_listbox()


def update_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        listbox.insert(tk.END, task)


label = tk.Label(root, text="Todo List")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=5)

remove_button = tk.Button(root, text="Remove Task", command=remove_task)
remove_button.pack(pady=5)

listbox = tk.Listbox(root, width=30)
listbox.pack(pady=10)


root.mainloop()