import csv



my_workout_records = []

def add_workout_manually():
    
    print("\n--- Enter Workout Details ---")
    date = input("Enter the date (e.g., 2023-10-25): ")
    exercise = input("Enter the exercise name (e.g., Bench Press): ")
    sets = input("How many sets did you do? ")
    reps = input("How many repetitions per set? ")
    weight = input("How much weight did you use (lbs/kg)? ")

    
    workout_entry = {
        "Date": date,
        "Exercise": exercise,
        "Sets": sets,
        "Reps": reps,
        "Weight": weight
    }

    
    my_workout_records.append(workout_entry)
    print("Workout saved successfully!")

def import_from_other_app():
    
    
    print("\n--- Import Data from CSV ---")
    file_name = input("Enter the exact name of the file (e.g., my_data.csv): ")

    try:
        
        with open(file_name, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                
                my_workout_records.append(row)
        print("Data imported successfully from " + file_name)
    except FileNotFoundError:
        print("Error: I couldn't find a file with that name. Please check the spelling.")

def view_all_workouts():
    
    if not my_workout_records:
        print("\nYour workout log is currently empty.")
        return

    print("\n--- YOUR WORKOUT LOG ---")
    
    for entry in my_workout_records:
        print(f"Date: {entry.get('Date')} | Exercise: {entry.get('Exercise')} | "
              f"Sets: {entry.get('Sets')} | Reps: {entry.get('Reps')} | Weight: {entry.get('Weight')}")
    print("------------------------")

def main_menu():
    
    
    while True:
        print("\nWORKOUT TRACKER MENU")
        print("1. Add a workout manually")
        print("2. Import workouts from another app (CSV file)")
        print("3. View all workouts")
        print("4. Exit program")
        
        choice = input("Please type 1, 2, 3, or 4: ")

        if choice == '1':
            add_workout_manually()
        elif choice == '2':
            import_from_other_app()
        elif choice == '3':
            view_all_workouts()
        elif choice == '4':
            print("Closing the app. Have a great day, Harold!")
            break
        else:
            print("Invalid choice. Please pick a number from the menu.")


if __name__ == "__main__":
    main_menu()