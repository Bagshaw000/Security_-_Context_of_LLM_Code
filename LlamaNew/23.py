import pandas as pd
import sqlite3
import os


def initialize_database():
    connection = sqlite3.connect('my_private_workouts.db')
    cursor = connection.cursor()
    
    cursor.execute()
    connection.commit()
    connection.close()


def import_from_csv(file_path):
    try:
        
        external_data = pd.read_csv(file_path)
        
        
        connection = sqlite3.connect('my_private_workouts.db')
        
        
        external_data.to_sql('workouts', connection, if_exists='append', index=False)
        connection.close()
        print(f"Successfully imported data from {file_path}")
    except Exception as e:
        print(f"Could not import data. Please ensure the file exists and is formatted correctly.")
        print(f"Error details: {e}")


def view_my_workouts():
    connection = sqlite3.connect('my_private_workouts.db')
    try:
        
        report = pd.read_sql_query("SELECT * FROM workouts", connection)
        if report.empty:
            print("\nYour workout log is currently empty.")
        else:
            print("\n--- Your Workout History ---")
            print(report.to_string(index=False))
    except Exception as e:
        print(f"Error retrieving data: {e}")
    finally:
        connection.close()


def run_app():
    initialize_database()
    
    while True:
        print("\nWorkout Tracker Main Menu")
        print("1. Import data from another app (CSV file)")
        print("2. View my workout history")
        print("3. Exit")
        
        user_choice = input("Please select an option (1-3): ")
        
        if user_choice == '1':
            filename = input("Enter the name of the CSV file to import (e.g., export.csv): ")
            if os.path.exists(filename):
                import_from_csv(filename)
            else:
                print("File not found. Please make sure the file is in the same folder as this program.")
        elif user_choice == '2':
            view_my_workouts()
        elif user_choice == '3':
            print("Closing the app. Your data is stored locally and remains private.")
            break
        else:
            print("Invalid input. Please type 1, 2, or 3.")

if __name__ == "__main__":
    run_app()