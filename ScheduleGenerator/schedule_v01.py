import os
import pandas as pd
# from src import schedule

input_csv_path = input("Enter the path of the CSV file to update: ")

if not os.path.exists(input_csv_path):
    print("The file does not exist. Please check the path and try again.")
else:
    try:
        schedules = pd.read_csv(input_csv_path)
        schedule.getScheduleINP(schedules)
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
