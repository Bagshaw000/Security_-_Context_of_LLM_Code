import datetime

class TodoItem:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False

class TodoList:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def complete_item(self, index):
        self.items[index].completed = True

    def display_items(self):
        for i, item in enumerate(self.items):
            status = "[X]" if item.completed else "[ ]"
            print(f"{i+1}. {status} {item.title} - {item.due_date}")

def main():
    todo_list = TodoList()

    while True:
        print("1. Add a new item")
        print("2. Mark an item as complete")
        print("3. Display todo list")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            title = input("Enter the title: ")
            description = input("Enter the description: ")
            due_date_str = input("Enter the due date (YYYY-MM-DD): ")
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            item = TodoItem(title, description, due_date)
            todo_list.add_item(item)
            print("Item added to the todo list.")

        elif choice == "2":
            todo_list.display_items()
            index = int(input("Enter the index of the item to mark as complete: "))
            todo_list.complete_item(index - 1)
            print("Item marked as complete.")

        elif choice == "3":
            todo_list.display_items()

        elif choice == "4":
            print("Exiting the todo list app...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()