class TodoListApp:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name, due_date=None):
        new_task = {
            'task': task_name,
            'due_date': due_date
        }
        self.tasks.append(new_task)

    def view_tasks(self):
        for i, task in enumerate(self.tasks, start=1):
            status = "Due" if 'due_date' in task else "Not Due"
            print(f"{i}. {task['task']} ({status}) - {task.get('due_date', 'No due date')}")
            print("")

    def delete_task(self, task_number):
        try:
            del self.tasks[task_number - 1]
            print("Task deleted successfully.")
        except IndexError:
            print("Invalid task number.")

    def update_task(self, task_number, new_task_name=None, new_due_date=None):
        if task_number < 1 or task_number > len(self.tasks):
            print("Invalid task number.")
            return
        task = self.tasks[task_number - 1]
        if new_task_name:
            task['task'] = new_task_name
        if new_due_date:
            task['due_date'] = new_due_date
        print("Task updated successfully.")

def main():
    todo_app = TodoListApp()

    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Update Task")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice == '1':
            task_name = input("Enter task name: ")
            due_date = input("Enter due date (YYYY-MM-DD) or press Enter for no due date: ")
            if due_date:
                todo_app.add_task(task_name, due_date)
            else:
                todo_app.add_task(task_name)

        elif choice == '2':
            todo_app.view_tasks()

        elif choice == '3':
            task_number = int(input("Enter the number of the task to delete: "))
            todo_app.delete_task(task_number)

        elif choice == '4':
            task_number = int(input("Enter the number of the task to update: "))
            new_task_name = input("Enter new task name (press Enter for no change): ")
            if new_task_name:
                new_task_name = new_task_name
            else:
                new_task_name = None

            new_due_date = input("Enter new due date (YYYY-MM-DD) or press Enter for no due date: ")
            if new_due_date:
                todo_app.update_task(task_number, new_task_name=new_task_name, new_due_date=new_due_date)
            else:
                todo_app.update_task(task_number)

        elif choice == '5':
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()