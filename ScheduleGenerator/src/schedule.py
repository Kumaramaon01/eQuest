import os
import pandas as pd

def getScheduleINP(data):
    try:
        data.columns = data.columns.str.replace(' ', '_')
        desired_column_name = data.columns[1]
        file_name = f"{desired_column_name}_Scheduled.inp"
        new_file_path = os.path.join(os.path.dirname(__file__), file_name)

        with open(new_file_path, 'w') as file:
            # Store index or markers to capture range of values
            idx1 = 0
            idx2 = 0
            idx3 = 0
        
            idx1, idx2, idx3 = None, None, None
            for index, row in data.iterrows():
                if row[0] == 'Hour':
                    idx1 = index
                elif row[0] == 'Day' and idx1 is not None and idx2 is None:
                    idx2 = index
                elif row[0] == 'Month' and idx2 is not None and idx3 is None:
                    idx3 = index + 1  # Adjust index as needed
                
                if idx1 is not None and idx2 is not None and idx3 is not None:
                    break

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
            type_value = data.iloc[0, 1].upper()
            
            for index, row in data.iterrows():
                if row[0] == 'Week Schedule' or row[0] == 'Rows can be added to add more weekly schedule': # need to ask this
                    break
                if index > idx1:
                    schedule_name = row[0]
                    file.write(f'"{schedule_name}" = DAY-SCHEDULE-PD\n')
                    file.write(f"   TYPE             = {type_value}\n")
                    file.write(f"   VALUES           = ( {formatted_values} )\n")
                    file.write("   ..\n")
                    file.write("")
            
            # Creating a new section called week schedules after completion of Day Schedule
            file.write("\n$ ---------------------------------------------------------\n")
            file.write("$              Week Schedules\n")
            file.write("$ ---------------------------------------------------------\n\n")

            # Extracting the 'Hour' row values from 2nd to 25th column
            hour_values = data.loc[data.iloc[:, 0] == 'Day'].iloc[0, 1:11].tolist()
            formatted_values = ', '.join(map(str, hour_values))
            
            for index, row in data.iterrows():
                if row[0] == 'Annual Schedule' or row[0] == 'Rows can be added to add more weekly schedule': # need to ask this
                    break
                if index > idx2:
                    schedule_name = row[0]
                    file.write(f'"{schedule_name}" = WEEK-SCHEDULE-PD\n')
                    file.write(f"   TYPE             = {type_value}\n")
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
                if row[0] == 'nan' or row[0] == 'NaN' or row[0] == 'NAN' or row[0] == 'Rows can be added to add more weekly schedule': # need to ask this
                    break
                if index > idx3:
                    schedule_name = row[0]
                    file.write(f'"{schedule_name}" = SCHEDULE-PD\n')
                    file.write(f"   TYPE             = {type_value}\n")
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
