import csv



my_workout_log = []

def add_workout():
    
    print("\n--- RECORD A NEW WORKOUT ---")
    date = input("Enter the date (e.g., 2023-10-27): ")
    exercise = input("What exercise did you do? ")
    sets = input("How many sets? ")
    reps = input("How many repetitions per set? ")
    weight = input("How much weight did you use (lbs/kg)? ")

    
    workout_entry = {
        "Date": date,
        "Exercise": exercise,
        "Sets": sets,
        "Reps": reps,
        "Weight": weight
    }

    
    my_workout_log.append(workout_entry)
    print("Workout saved successfully!")

def show_all_workouts():
    
    print("\n--- YOUR WORKOUT HISTORY ---")
    if not my_workout_log:
        print("Your notebook is currently empty.")
        return

    
    print("Date       | Exercise   | Sets | Reps | Weight")
    print("-" * 55)
    
    for entry in my_workout_log:
        
        print(f"{entry['Date']:10} | {entry['Exercise']:10} | {entry['Sets']:4} | {entry['Reps']:4} | {entry['Weight']}")

def import_from_csv():
    
    print("\n--- IMPORT DATA FROM ANOTHER APP ---")
    print("Instructions: Place your file in the same folder as this program.")
    filename = input("Enter the exact name of the file (e.g., my_data.csv): ")
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            
            reader = csv.DictReader(file)
            for row in reader:
                my_workout_log.append(row)
        print(f"Successfully imported data from {filename}!")
    except FileNotFoundError:
        print(f"Error: Could not find a file named '{filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main_menu():
    
    while True:
        print("\n==============================")
        print("   HAROLD'S WORKOUT TRACKER")
        print("==============================")
        print("1. Add a new workout")
        print("2. View your history")
        print("3. Import data from a file (CSV)")
        print("4. Exit program")

        choice = input("\nWhat would you like to do? (Type 1, 2, 3, or 4): ")

        if choice == '1':
            add_workout()
        elif choice == '2':
            show_all_workouts()
        elif choice == '3':
            import_from_csv()
        elif choice == '4':
            print("Closing the tracker. Great job today!")
            break
        else:
            print("I didn't understand that choice. Please type a number from 1 to 4.")


if __name__ == "__main__":
    main_menu()