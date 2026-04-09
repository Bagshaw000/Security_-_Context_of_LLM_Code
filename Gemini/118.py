


import csv
import os



DATABASE_FILE = "my_workout_log.csv"

def initialize_app():
    
    
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Exercise", "Sets", "Reps", "Weight"])

def add_new_workout():
    
    print("\n--- Enter Workout Details ---")
    date = input("Enter the date (e.g., 2023-12-01): ")
    exercise = input("What is the name of the exercise? ")
    sets = input("How many sets did you do? ")
    reps = input("How many repetitions per set? ")
    weight = input("How much weight did you use? ")

    with open(DATABASE_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, exercise, sets, reps, weight])
    print("Saved! Your workout has been added to the list.")

def show_history():
    
    print("\n--- Your Progress History ---")
    if not os.path.exists(DATABASE_FILE):
        print("No records found yet.")
        return

    try:
        with open(DATABASE_FILE, mode='r') as file:
            reader = csv.reader(file)
            
            next(reader, None) 
            for row in reader:
                if row: 
                    print(f"Date: {row[0]} | Exercise: {row[1]} | Sets: {row[2]} | Reps: {row[3]} | Weight: {row[4]}")
    except FileNotFoundError:
        print("The record file hasn't been created yet.")

def import_external_data():
    
    
    print("\n--- Import from Another App ---")
    print("Make sure the other file is in the same folder as this program.")
    other_filename = input("Enter the exact name of the other file (e.g., export_data.csv): ")

    try:
        with open(other_filename, mode='r') as source_file:
            reader = csv.reader(source_file)
            
            next(reader, None)
            
            with open(DATABASE_FILE, mode='a', newline='') as master_file:
                writer = csv.writer(master_file)
                added_count = 0
                for row in reader:
                    if row:
                        writer.writerow(row)
                        added_count += 1
        print(f"Success! {added_count} rows were imported from {other_filename}.")
    except FileNotFoundError:
        print("Error: I couldn't find a file with that name. Please check the spelling.")

def run_app():
    
    initialize_app()
    
    while True:
        print("\n===============================")
        print("HAROLD'S WORKOUT TRACKER")
        print("===============================")
        print("1. Record a new workout")
        print("2. View all past workouts")
        print("3. Import data from another app")
        print("4. Exit program")
        
        choice = input("\nWhat would you like to do? (Type 1, 2, 3, or 4): ")
        
        if choice == '1':
            add_new_workout()
        elif choice == '2':
            show_history()
        elif choice == '3':
            import_external_data()
        elif choice == '4':
            print("Closing the tracker. Great job today, Harold!")
            break
        else:
            print("That wasn't a valid option. Please type a number from 1 to 4.")


if __name__ == "__main__":
    run_app()