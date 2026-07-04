



import os


DATA_FILE = "my_todo_list.txt"

def load_tasks():
    
    tasks = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            
            tasks = [line.strip() for line in file.readlines()]
    return tasks

def save_tasks(tasks):
    
    with open(DATA_FILE, "w") as file:
        for task in tasks:
            file.write(task + "\n")

def main():
    
    tasks = load_tasks()

    while True:
        
        print("\n" + "="*30)
        print("      HAROLD'S TO-DO LIST")
        print("="*30)

        if not tasks:
            print("Your list is empty.")
        else:
            
            for index, item in enumerate(tasks, start=1):
                print(f"{index}. {item}")

        print("-" * 30)
        print("OPTIONS:")
        print("1. Add a new task")
        print("2. Remove a finished task (by number)")
        print("3. Save and Exit")

        choice = input("\nWhat would you like to do? (Type 1, 2, or 3): ")

        if choice == "1":
            
            new_item = input("Type your task here: ")
            tasks.append(new_item)
            print("Task added!")

        elif choice == "2":
            
            if not tasks:
                print("Nothing to remove.")
                continue
            
            try:
                task_number = int(input("Type the number of the task to remove: "))
                if 1 <= task_number <= len(tasks):
                    
                    removed = tasks.pop(task_number - 1)
                    print(f"Successfully removed: {removed}")
                else:
                    print("That number is not on your list.")
            except ValueError:
                print("Please type a valid number.")

        elif choice == "3":
            
            save_tasks(tasks)
            print("List saved to " + DATA_FILE + ". Goodbye!")
            break
        
        else:
            print("Invalid choice. Please type 1, 2, or 3.")


if __name__ == "__main__":
    main()