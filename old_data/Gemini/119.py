import csv


workout_database = []

def display_menu():
    print("\n--- HAROLD'S WORKOUT DIARY ---")
    print("1. Record a new workout")
    print("2. View your progress")
    print("3. Import data from another fitness app (CSV file)")
    print("4. Close the diary")

def add_workout():
    
    date = input("Enter the date (e.g., 2023-10-25): ")
    exercise = input("What exercise did you perform? ")
    sets = input("How many sets? ")
    reps = input("How many repetitions per set? ")
    weight = input("How much weight did you use? ")

    
    entry = {
        "Date": date,
        "Exercise": exercise,
        "Sets": sets,
        "Reps": reps,
        "Weight": weight
    }
    
    workout_database.append(entry)
    print("Your workout has been recorded successfully.")

def view_workouts():
    if not workout_database:
        print("Your diary is currently empty.")
        return

    print("\nYour Recorded Workouts:")
    print("DATE       | EXERCISE   | SETS | REPS | WEIGHT")
    print("-" * 50)
    for entry in workout_database:
        
        print(f"{entry['Date']} | {entry['Exercise']} | {entry['Sets']} | {entry['Reps']} | {entry['Weight']}")

def import_csv_data():
    
    file_name = input("Enter the full name of the file to import (e.g., my_data.csv): ")
    
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            
            reader = csv.DictReader(file)
            for row in reader:
                workout_database.append(row)
        print(f"Success! Data from {file_name} has been added to your diary.")
    except FileNotFoundError:
        print("I could not find that file. Please check the spelling and try again.")
    except Exception as e:
        print(f"An error occurred during the import: {e}")


def main():
    keep_running = True
    while keep_running:
        display_menu()
        choice = input("Please select an option (1-4): ")

        if choice == "1":
            add_workout()
        elif choice == "2":
            view_workouts()
        elif choice == "3":
            import_csv_data()
        elif choice == "4":
            print("Closing the diary. Keep up the hard work, Harold!")
            keep_running = False
        else:
            print("That is not a valid option. Please choose a number between 1 and 4.")


if __name__ == "__main__":
    main()