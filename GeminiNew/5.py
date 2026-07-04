import os
import re


FILE_NAME = "my_todo_list.txt"

def clean_text(user_input):
    
    
    safe_text = re.sub(r'[^a-zA-Z0-9\s.,!?\-]', '', user_input)
    
    return safe_text.strip()

def show_tasks():
    
    if not os.path.exists(FILE_NAME):
        print("\nYour list is currently empty.")
        return
    
    print("\n--- YOUR CURRENT TO-DO LIST ---")
    try:
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()
            if not lines:
                print("Your list is currently empty.")
            else:
                for index, line in enumerate(lines, start=1):
                    
                    print(f"{index}. {line.strip()}")
    except Exception:
        print("Could not read the file. It may be in use by another program.")
    print("------------------------------")

def add_task():
    
    raw_task = input("Type the task you want to add: ")
    safe_task = clean_text(raw_task)
    
    if safe_task:
        try:
            with open(FILE_NAME, "a") as file:
                
                file.write(f"[ ] {safe_task}\n")
            print("Success: Task added to your list.")
        except Exception:
            print("Error: Could not save the task.")
    else:
        print("Safety Warning: The task contained invalid characters and was blocked.")

def mark_finished():
    
    show_tasks()
    if not os.path.exists(FILE_NAME):
        return
        
    choice = input("Enter the number of the task you have finished: ")
    
    clean_choice = re.sub(r'\D', '', choice)
    
    if not clean_choice:
        print("Invalid input. Please enter a number.")
        return

    try:
        task_num = int(clean_choice)
        with open(FILE_NAME, "r") as file:
            lines = file.readlines()
        
        if 1 <= task_num <= len(lines):
            
            if "[ ]" in lines[task_num - 1]:
                lines[task_num - 1] = lines[task_num - 1].replace("[ ]", "[X]", 1)
                with open(FILE_NAME, "w") as file:
                    file.writelines(lines)
                print(f"Task {task_num} is now marked as finished!")
            else:
                print("That task is already marked as finished.")
        else:
            print("That number is not on your list.")
    except (ValueError, IndexError, IOError):
        print("There was an error updating the list. Please try again.")

def main():
    
    print("Welcome to your Digital To-Do List.")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. View my list")
        print("2. Add a new task")
        print("3. Mark a task as finished")
        print("4. Close the program")
        
        user_choice = input("\nEnter a number (1-4): ").strip()
        
        if user_choice == "1":
            show_tasks()
        elif user_choice == "2":
            add_task()
        elif user_choice == "3":
            mark_finished()
        elif user_choice == "4":
            print("Saving changes and closing. Goodbye, Harold!")
            break
        else:
            print("Please choose a valid option by typing 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()