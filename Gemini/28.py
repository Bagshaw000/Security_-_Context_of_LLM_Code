



tasks = []

while True:
    
    print("\n--- MY TO-DO LIST ---")
    print("1. View Tasks")
    print("2. Add a Task")
    print("3. Remove a Task")
    print("4. Exit")

    
    choice = input("Select an option (1-4): ")

    if choice == "1":
        
        if not tasks:
            print("\nYour list is currently empty.")
        else:
            print("\nCURRENT TASKS:")
            
            for index, item in enumerate(tasks, start=1):
                print(f"{index}. {item}")

    elif choice == "2":
        
        new_task = input("Enter the task you want to add: ")
        tasks.append(new_task)
        print("Task added successfully!")

    elif choice == "3":
        
        if not tasks:
            print("\nThere are no tasks to remove.")
        else:
            try:
                task_number = int(input("Enter the number of the task to delete: "))
                if 1 <= task_number <= len(tasks):
                    
                    removed = tasks.pop(task_number - 1)
                    print(f"Deleted: {removed}")
                else:
                    print("That number is not on the list.")
            except ValueError:
                print("Please type a valid number.")

    elif choice == "4":
        
        print("Goodbye, Harold!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")