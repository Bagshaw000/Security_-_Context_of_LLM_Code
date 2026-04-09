class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f'Task "{task}" added.')

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            print(f'Task "{task}" removed.')
        else:
            print(f'Task "{task}" not found.')

    def view_tasks(self):
        if not self.tasks:
            print("No tasks in the list.")
        else:
            print("Todo List:")
            for idx, task in enumerate(self.tasks, start=1):
                print(f"{idx}. {task}")

def main():
    todo_list = TodoList()
    while True:
        print("\nOptions: add, remove, view, exit")
        choice = input("Choose an option: ").strip().lower()
        
        if choice == "add":
            task = input("Enter the task: ")
            todo_list.add_task(task)
        elif choice == "remove":
            task = input("Enter the task to remove: ")
            todo_list.remove_task(task)
        elif choice == "view":
            todo_list.view_tasks()
        elif choice == "exit":
            print("Exiting the app.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()