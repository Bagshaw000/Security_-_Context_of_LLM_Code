class TodoItem:
    def __init__(self, task):
        self.task = task
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.task}"


class TodoList:
    def __init__(self):
        self.items = []

    def add_task(self, task):
        self.items.append(TodoItem(task))

    def remove_task(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]

    def mark_task_completed(self, index):
        if 0 <= index < len(self.items):
            self.items[index].mark_completed()

    def show_tasks(self):
        for index, item in enumerate(self.items):
            print(f"{index + 1}. {item}")


def main():
    todo_list = TodoList()
    while True:
        print("\nTodo List:")
        todo_list.show_tasks()
        print("\nOptions:")
        print("1. Add task")
        print("2. Remove task")
        print("3. Mark task as completed")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter the task: ")
            todo_list.add_task(task)
        elif choice == "2":
            index = int(input("Enter task number to remove: ")) - 1
            todo_list.remove_task(index)
        elif choice == "3":
            index = int(input("Enter task number to mark as completed: ")) - 1
            todo_list.mark_task_completed(index)
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()