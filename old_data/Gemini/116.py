import csv
import os





def setup_storage():
    
    filename = 'workout_log.csv'
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow(['Date', 'Exercise', 'Sets', 'Reps', 'Weight'])

def add_workout():
    
    print("\n--- Enter New Workout Details ---")
    date = input("Enter the date (e.g., 2023-10-27): ")
    exercise = input("What exercise did you do? ")
    sets = input("How many sets? ")
    reps = input("How many repetitions? ")
    weight = input("How much weight did you use (in lbs)? ")

    with open('workout_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, exercise, sets, reps, weight])
    print("Workout saved successfully!")

def view_history():
    
    print("\n--- Your Workout History ---")
    try:
        with open('workout_log.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                
                print("{:<12} {:<15} {:<6} {:<6} {:<6}".format(*row))
    except FileNotFoundError:
        print("No records found. Start by adding a workout!")

def import_external_data():
    
    
    print("\n--- Import Data from Other Apps ---")
    print("Note: The file you are importing must have the columns: Date, Exercise, Sets, Reps, Weight.")
    external_file = input("Enter the name of the file to import (e.g., my_old_data.csv): ")

    if os.path.exists(external_file):
        with open(external_file, mode='r') as source:
            reader = csv.reader(source)
            next(reader)  
            
            with open('workout_log.csv', mode='a', newline='') as destination:
                writer = csv.writer(destination)
                count = 0
                for row in reader:
                    writer.writerow(row)
                    count += 1
        print(f"Success! Imported {count} rows of data.")
    else:
        print("Error: Could not find a file with that name. Please check the spelling.")

def main():
    
    setup_storage()
    
    while True:
        print("\n--- HAROLD'S WORKOUT TRACKER ---")
        print("1. Log a new workout")
        print("2. View workout history")
        print("3. Import data from another app")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            add_workout()
        elif choice == '2':
            view_history()
        elif choice == '3':
            import_external_data()
        elif choice == '4':
            print("Closing the app. Have a great day, Harold!")
            break
        else:
            print("That wasn't a valid choice. Please type 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()