class TodoApp:
    def __init__(self):
        self.todos = []

    def add_task(self, task):
        self.todos.append(task)
        print(f'Task "{task}" added.')

    def remove_task(self, task):
        if task in self.todos:
            self.todos.remove(task)
            print(f'Task "{task}" removed.')
        else:
            print(f'Task "{task}" not found.')

    def view_tasks(self):
        if not self.todos:
            print("No tasks in the list.")
        else:
            print("Todo List:")
            for idx, task in enumerate(self.todos, start=1):
                print(f"{idx}. {task}")

    def run(self):
        while True:
            command = input("Enter a command (add, remove, view, exit): ").strip().lower()
            if command == "add":
                task = input("Enter the task: ")
                self.add_task(task)
            elif command == "remove":
                task = input("Enter the task to remove: ")
                self.remove_task(task)
            elif command == "view":
                self.view_tasks()
            elif command == "exit":
                print("Exiting the app.")
                break
            else:
                print("Invalid command. Please try again.")

if __name__ == "__main__":
    app = TodoApp()
    app.run()