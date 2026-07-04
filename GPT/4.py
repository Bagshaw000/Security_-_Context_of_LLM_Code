class TodoItem:
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title}: {self.description}"


class TodoList:
    def __init__(self):
        self.items = []

    def add_item(self, title, description=""):
        item = TodoItem(title, description)
        self.items.append(item)

    def remove_item(self, title):
        self.items = [item for item in self.items if item.title != title]

    def mark_item_completed(self, title):
        for item in self.items:
            if item.title == title:
                item.mark_completed()
                break

    def show_list(self):
        for item in self.items:
            print(item)


def main():
    todo_list = TodoList()
    
    while True:
        print("\nTodo List App")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Mark Item Completed")
        print("4. Show List")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            title = input("Enter the title of the todo item: ")
            description = input("Enter a description (optional): ")
            todo_list.add_item(title, description)
        elif choice == "2":
            title = input("Enter the title of the item to remove: ")
            todo_list.remove_item(title)
        elif choice == "3":
            title = input("Enter the title of the item to mark as completed: ")
            todo_list.mark_item_completed(title)
        elif choice == "4":
            todo_list.show_list()
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()