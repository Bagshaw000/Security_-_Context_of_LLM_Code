import csv



workout_database = []

def manual_entry():
    
    print("\n--- Enter New Workout Details ---")
    date = input("Enter Date (e.g., 2023-10-27): ")
    activity = input("Enter Exercise Name (e.g., Bench Press): ")
    sets = input("Enter Number of Sets: ")
    reps = input("Enter Number of Reps: ")
    weight = input("Enter Weight Used (e.g., 100lbs): ")

    
    record = {
        "Date": date,
        "Exercise": activity,
        "Sets": sets,
        "Reps": reps,
        "Weight": weight
    }

    
    workout_database.append(record)
    print("Workout added to your log successfully.")

def import_from_other_app():
    
    
    
    
    filename = input("\nEnter the exact name of the CSV file (e.g., 'my_data.csv'): ")
    
    try:
        
        with open(filename, mode='r', encoding='utf-8') as file:
            
            
            reader = csv.DictReader(file)
            for row in reader:
                workout_database.append(row)
        print("Data imported successfully!")
    except FileNotFoundError:
        print("Error: I couldn't find a file with that name. Please check the spelling.")

def display_log():
    
    print("\n--- YOUR CURRENT WORKOUT LOG ---")
    if len(workout_database) == 0:
        print("The log is currently empty.")
    else:
        
        for item in workout_database:
            
            d = item.get('Date', 'N/A')
            e = item.get('Exercise', 'N/A')
            s = item.get('Sets', '0')
            r = item.get('Reps', '0')
            w = item.get('Weight', '0')
            print(f"Date: {d} | Exercise: {e} | Sets: {s} | Reps: {r} | Weight: {w}")
    print("--------------------------------\n")

def run_app():
    
    running = True
    while running:
        print("HAROLD'S WORKOUT TRACKER")
        print("1. Type in a new workout")
        print("2. Import data from another app (CSV file)")
        print("3. View all workout history")
        print("4. Close the program")
        
        choice = input("What would you like to do? (Type 1, 2, 3, or 4): ")

        if choice == "1":
            manual_entry()
        elif choice == "2":
            import_from_other_app()
        elif choice == "3":
            display_log()
        elif choice == "4":
            print("Closing the app. Keep up the hard work, Harold!")
            running = False
        else:
            print("That wasn't a valid option. Please try typing 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_app()