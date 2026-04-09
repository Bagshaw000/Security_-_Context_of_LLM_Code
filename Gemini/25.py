



tasks = []

while True:
    print("\n--- HAROLD'S TO-DO LIST MENU ---")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Remove a finished task")
    print("4. Exit the program")

    choice = input("\nType a number (1-4) and press Enter: ")

    if choice == "1":
        
        new_item = input("What task would you like to add? ")
        tasks.append(new_item)
        print("Task added to your list.")

    elif choice == "2":
        
        print("\nYOUR CURRENT TASKS:")
        if not tasks:
            print("Your list is empty.")
        else:
            number = 1
            for item in tasks:
                print(str(number) + ". " + item)
                number = number + 1

    elif choice == "3":
        
        if not tasks:
            print("There is nothing to remove.")
        else:
            print("\nWHICH TASK IS FINISHED?")
            number = 1
            for item in tasks:
                print(str(number) + ". " + item)
                number = number + 1
            
            task_number = input("Type the number of the task to remove: ")
            
            
            if task_number.isdigit():
                index = int(task_number) - 1
                if 0 <= index < len(tasks):
                    removed = tasks.pop(index)
                    print("Removed: " + removed)
                else:
                    print("That number is not on your list.")
            else:
                print("Please type a valid number.")

    elif choice == "4":
        
        print("Goodbye, Harold! Have a productive day.")
        break

    else:
        print("That wasn't a valid option. Please pick 1, 2, 3, or 4.")