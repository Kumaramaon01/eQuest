import os
import pandas as pd

def getScheduleINP(data):
    try:
        new_file_path = os.path.join(os.path.dirname(__file__), 'new_file.inp')
        with open(new_file_path, 'w') as file:
            file.write("INPUT ..\n\n")
            file.write("$ ---------------------------------------------------------\n")
            file.write("$              Abort, Diagnostics\n")
            file.write("$ ---------------------------------------------------------\n")

            # Creating a new section called Day schedules
            file.write("\n$ ---------------------------------------------------------\n")
            file.write("$              Day Schedules\n")
            file.write("$ ---------------------------------------------------------\n\n")

            # Extracting the 'Hour' row values from 2nd to 25th column
            hour_values = data.loc[data.iloc[:, 0] == 'Hour'].iloc[0, 1:25].tolist()
            formatted_values = ', '.join(map(str, hour_values))
            
            for index, row in data.iterrows():
                if row[0] != 'Hour':
                    schedule_name = row[0]
                    file.write(f'"{schedule_name}" = DAY-SCHEDULE-PD\n')
                    file.write("   TYPE             = FRACTION\n")
                    file.write(f"   VALUES           = ( {formatted_values} )\n")
                    file.write("   ..\n")
                    file.write("")
            
                    
            # Creating a new section called week schedules after completion of Day Schedule
            file.write("\n$ ---------------------------------------------------------\n")
            file.write("$              Week Schedules\n")
            file.write("$ ---------------------------------------------------------\n\n")

            # Extracting the 'Hour' row values from 2nd to 25th column
            hour_values = data.loc[data.iloc[:, 0] == 'Day'].iloc[0, 1:10].tolist()
            formatted_values = ', '.join(map(str, hour_values))
            
            for index, row in data.iterrows():
                if row[0] != 'Hour':
                    schedule_name = row[0]
                    file.write(f'"{schedule_name}" = WEEK-SCHEDULE-PD\n')
                    file.write("   TYPE             = FRACTION\n")
                    file.write(f"   DAY-SCHEDULES    = ( {formatted_values} )\n")
                    file.write("   ..\n")
                    file.write("")

            # Creating a new section called Annual schedules after completion of Week Schedule
            file.write("\n$ ---------------------------------------------------------\n")
            file.write("$              Annual Schedules\n")
            file.write("$ ---------------------------------------------------------\n\n")

            # Extracting the 'Hour' row values from 2nd to 25th column
            hour_values = data.loc[data.iloc[:, 0] == 'Month'].iloc[0, 1:13].tolist()
            formatted_values = ', '.join(map(str, hour_values))
            
            for index, row in data.iterrows():
                if row[0] != 'Hour':
                    schedule_name = row[0]
                    file.write(f'"{schedule_name}" = SCHEDULE-PD\n')
                    file.write("   TYPE             = FRACTION\n")
                    file.write(f"   MONTH            = ( {formatted_values} )\n")
                    file.write(f"   DAY              = ( {formatted_values} )\n")
                    file.write(f"   WEEK-SCHEDULES   = ( {formatted_values} )\n")
                    file.write("   ..\n")
                    file.write("")
            
            file.write("\n\n")
            file.write("$ ---------------------------------------------------------\n")
            file.write("$              THE END\n")
            file.write("$ ---------------------------------------------------------\n\n")
            file.write("END ..\n")
            file.write("COMPUTE ..\n")
            file.write("STOP ..\n")
                
        print(f"New file created at: {new_file_path}")
    except Exception as e:
        print(f"An error occurred while creating the new file: {e}")