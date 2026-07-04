



tasks = []


while True:
    print("\n--- TO-DO LIST MENU ---")
    print("1. Add a new task")
    print("2. View your tasks")
    print("3. Remove a task")
    print("4. Close the program")

    
    choice = input("\nType 1, 2, 3, or 4 and press Enter: ")

    if choice == "1":
        
        new_item = input("What do you need to do? ")
        tasks.append(new_item)
        print("Task added to your list!")

    elif choice == "2":
        
        print("\nYOUR CURRENT TASKS:")
        if len(tasks) == 0:
            print("Your list is currently empty.")
        else:
            
            for index, item in enumerate(tasks, start=1):
                print(str(index) + ". " + item)

    elif choice == "3":
        
        if len(tasks) == 0:
            print("There are no tasks to remove.")
        else:
            
            for index, item in enumerate(tasks, start=1):
                print(str(index) + ". " + item)
            
            try:
                task_num = int(input("Type the number of the task you want to delete: "))
                
                removed_item = tasks.pop(task_num - 1)
                print("Successfully removed: " + removed_item)
            except:
                print("Error: Please type a valid number from the list above.")

    elif choice == "4":
        
        print("Closing the app. Have a productive day, Harold!")
        break

    else:
        
        print("I didn't understand that choice. Please type 1, 2, 3, or 4.")