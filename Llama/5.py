class TodoItem:
    def __init__(self, task, done=False):
        self.task = task
        self.done = done

    def mark_as_done(self):
        self.done = True

    def mark_as_not_done(self):
        self.done = False

class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        new_task = TodoItem(task)
        self.tasks.append(new_task)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
        else:
            print("Invalid index")

    def mark_task_as_done(self, index):
        try:
            self.tasks[index].mark_as_done()
        except IndexError:
            print("Invalid index")

    def mark_task_as_not_done(self, index):
        try:
            self.tasks[index].mark_as_not_done()
        except IndexError:
            print("Invalid index")

    def display_tasks(self):
        for i, task in enumerate(self.tasks):
            status = "Done" if task.done else "Not Done"
            print(f"{i+1}. {task.task} - {status}")

def main():
    todo_list = TodoList()
    
    while True:
        print("\nTodo List Menu:")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Mark Task as Done")
        print("4. Mark Task as Not Done")
        print("5. Display Tasks")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            task = input("Enter a new task: ")
            todo_list.add_task(task)
        elif choice == "2":
            index = int(input("Enter the number of the task to delete: "))
            todo_list.delete_task(index-1)
        elif choice == "3":
            index = int(input("Enter the number of the task to mark as done: "))
            todo_list.mark_task_as_done(index-1)
        elif choice == "4":
            index = int(input("Enter the number of the task to mark as not done: "))
            todo_list.mark_task_as_not_done(index-1)
        elif choice == "5":
            todo_list.display_tasks()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()