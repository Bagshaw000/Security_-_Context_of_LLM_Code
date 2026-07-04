class TodoItem:
    def __init__(self, task, due_date):
        self.task = task
        self.due_date = due_date
        self.is_completed = False

class TodoList:
    def __init__(self):
        self.items = []

    def add_item(self, task, due_date):
        item = TodoItem(task, due_date)
        self.items.append(item)

    def mark_complete(self, index):
        self.items[index].is_completed = True

    def print_list(self):
        for i, item in enumerate(self.items):
            status = "[X]" if item.is_completed else "[ ]"
            print(f"{i+1}. {status} {item.task} - {item.due_date}")

def main():
    todo_list = TodoList()

    while True:
        print("Welcome to the Todo List app!")
        print("1. Add a new item")
        print("2. Mark an item as complete")
        print("3. View the todo list")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            task = input("Enter the task: ")
            due_date = input("Enter the due date: ")
            todo_list.add_item(task, due_date)
            print("Item added to the list.")
        elif choice == "2":
            todo_list.print_list()
            index = int(input("Enter the index of the item to mark as complete: "))
            todo_list.mark_complete(index - 1)
            print("Item marked as complete.")
        elif choice == "3":
            todo_list.print_list()
        elif choice == "4":
            print("Exiting the Todo List app.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()