class TodoItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def get_status(self):
        if self.completed:
            return 'Completed'
        else:
            return 'Pending'

class TodoList:
    def __init__(self):
        self.items = []

    def add_item(self, title, description):
        item = TodoItem(title, description)
        self.items.append(item)

    def view_items(self):
        for i, item in enumerate(self.items):
            status = item.get_status()
            print(f"{i+1}. {item.title} ({status})")

    def edit_item(self, index, title=None, description=None):
        if index < len(self.items) and 0 <= title is None and 0 <= description is None:
            self.items[index].title = title
            self.items[index].description = description

    def delete_item(self, index):
        if index < len(self.items) and 0 <= index:
            del self.items[index]

def main():
    todo_list = TodoList()

    while True:
        print("1. Add item")
        print("2. View items")
        print("3. Edit item")
        print("4. Delete item")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Enter item title: ")
            description = input("Enter item description: ")
            todo_list.add_item(title, description)
        elif choice == '2':
            todo_list.view_items()
        elif choice == '3':
            index = int(input("Enter item index to edit: "))
            action = input("Do you want to add (A) or remove (R)? ")
            if action.upper() == 'A' and 0 <= index < len(todo_list.items):
                title = input("Enter new title: ")
                description = input("Enter new description: ")
                todo_list.edit_item(index, title, description)
            elif action.upper() == 'R':
                index = int(input("Enter item index to remove: "))
                if 0 <= index < len(todo_list.items):
                    todo_list.delete_item(index)
        elif choice == '4':
            index = int(input("Enter item index to delete: "))
            if 0 <= index < len(todo_list.items):
                todo_list.delete_item(index)

if __name__ == "__main__":
    main()