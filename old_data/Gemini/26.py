



import os

def run_todo_app():
    
    filename = "my_tasks.txt"
    
    
    if os.path.exists(filename):
        with open(filename, "r") as file:
            tasks = [line.strip() for line in file.readlines()]
    else:
        
        tasks = []

    while True:
        
        print("\n--- YOUR CURRENT TODO LIST ---")
        if not tasks:
            print("(The list is currently empty)")
        else:
            
            for number, task in enumerate(tasks, 1):
                print(f"{number}. {task}")

        
        print("\nWhat would you like to do?")
        print("1. Add a new task")
        print("2. Remove a completed task")
        print("3. Exit the program")
        
        choice = input("Type 1, 2, or 3 and then press the Enter key: ")

        if choice == "1":
            
            new_item = input("What task would you like to add? ")
            tasks.append(new_item)
            
            
            with open(filename, "w") as file:
                for item in tasks:
                    file.write(item + "\n")
            print("Task successfully added to your list.")

        elif choice == "2":
            
            if not tasks:
                print("You have no tasks to remove.")
            else:
                try:
                    remove_num = int(input("Enter the number of the task you finished: "))
                    
                    if 1 <= remove_num <= len(tasks):
                        removed_task = tasks.pop(remove_num - 1)
                        
                        
                        with open(filename, "w") as file:
                            for item in tasks:
                                file.write(item + "\n")
                        print(f"Removed '{removed_task}' from your list.")
                    else:
                        print("That number is not on your list. Please try again.")
                except ValueError:
                    
                    print("Please enter a valid number (e.g., 1, 2, 3).")

        elif choice == "3":
            
            print("Goodbye, Harold! Your list has been saved.")
            break
        else:
            
            print("That was not a valid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    run_todo_app()