
tasks = []

print("Welcome to your To-Do List Manager, Harold!")

while True:
    print("\n--- MENU ---")
    print("1. Add a new task")
    print("2. View your tasks")
    print("3. Delete a task")
    print("4. Exit the program")

    
    choice = input("\nType a number (1-4) and press Enter: ")

    if choice == "1":
        
        new_task = input("What task would you like to add? ")
        tasks.append(new_task)
        print("Task added to your list.")

    elif choice == "2":
        
        print("\n--- YOUR CURRENT TO-DO LIST ---")
        if not tasks:
            print("Your list is currently empty.")
        else:
            
            for number, task in enumerate(tasks, start=1):
                print(str(number) + ". " + task)

    elif choice == "3":
        
        if not tasks:
            print("There are no tasks to delete.")
        else:
            for number, task in enumerate(tasks, start=1):
                print(str(number) + ". " + task)
            
            try:
                task_to_remove = int(input("Type the number of the task you want to delete: "))
                
                removed = tasks.pop(task_to_remove - 1)
                print("Successfully removed: " + removed)
            except:
                print("That is not a valid task number.")

    elif choice == "4":
        
        print("Closing the program. Have a great day, Harold!")
        break

    else:
        print("Please choose a valid option (1, 2, 3, or 4).")