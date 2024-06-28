import os
import pandas as pd
import streamlit as st
import io

def getScheduleINP(data):
    data.columns = data.columns.str.replace(' ', '_')
    desired_column_name = data.columns[1]
    file_name = f"{desired_column_name}_Scheduled.inp"
    
    # Use StringIO to create an in-memory text stream
    output = io.StringIO()

    # Write to the in-memory file
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

    output.write("INPUT ..\n\n")
    output.write("$ ---------------------------------------------------------\n")
    output.write("$              Abort, Diagnostics\n")
    output.write("$ ---------------------------------------------------------\n")

    # Creating a new section called Day schedules
    output.write("\n$ ---------------------------------------------------------\n")
    output.write("$              Day Schedules\n")
    output.write("$ ---------------------------------------------------------\n\n")

    # Extracting the 'Hour' row values from 2nd to 25th column
    hour_values = data.loc[data.iloc[:, 0] == 'Hour'].iloc[0, 1:25].tolist()
    formatted_hour_values = ', '.join(map(str, hour_values))
    type_value = data.iloc[0, 1].upper()

    # Iterate through the rows of the data
    for index, row in data.iterrows():
        if row[0] == 'Week Schedule' or row[0] == 'Rows can be added to add more weekly schedule':
            break
        if index > idx1:
            schedule_name = row[0]
            # Extract values from 2nd to 25th column for the current row
            row_values = row[1:25].tolist()
            formatted_values = ', '.join(map(str, row_values))
            
            # Write to the file
            output.write(f'"{schedule_name}" = DAY-SCHEDULE-PD\n')
            output.write(f"   TYPE             = {type_value}\n")
            output.write(f"   VALUES           = ( {formatted_values} )\n")
            output.write("   ..\n")
            output.write("")

    # Creating a new section called week schedules after completion of Day Schedule
    output.write("\n$ ---------------------------------------------------------\n")
    output.write("$              Week Schedules\n")
    output.write("$ ---------------------------------------------------------\n\n")

    # Extracting the 'Hour' row values from 2nd to 25th column
    day_values = data.loc[data.iloc[:, 0] == 'Day'].iloc[0, 1:11].tolist()
    formatted_day_values = ', '.join(map(str, day_values))
    
    for index, row in data.iterrows():
        if row[0] == 'Annual Schedule' or row[0] == 'Rows can be added to add more weekly schedule': # need to ask this
            break
        if index > idx2:
            schedule_name = row[0]
            # Extract values from 2nd to 11th column for the current row
            row_values = row[1:11].tolist()
            formatted_day = ', '.join(f'"{value}"' for value in row_values)

            output.write(f'"{schedule_name}" = WEEK-SCHEDULE-PD\n')
            output.write(f"   TYPE             = {type_value}\n")
            output.write(f"   DAY-SCHEDULES    = ( {formatted_day} )\n")
            output.write("   ..\n")
            output.write("")

    # Creating a new section called Annual schedules after completion of Week Schedule
    output.write("\n$ ---------------------------------------------------------\n")
    output.write("$              Annual Schedules\n")
    output.write("$ ---------------------------------------------------------\n\n")

    # Extracting the 'Hour' row values from 2nd to 25th column
    month_values = data.loc[data.iloc[:, 0] == 'Month'].iloc[0, 1:13].tolist()
    day_values = data.loc[data.iloc[:, 0] == 'Month'].iloc[0, 1:13].tolist()
    formatted_values1 = ', '.join(map(str, month_values))
    formatted_values2 = ', '.join(map(str, day_values))
    
    for index, row in data.iterrows():
        if row[0] == 'nan' or row[0] == 'NaN' or row[0] == 'NAN' or row[0] == 'Rows can be added to add more weekly schedule': # need to ask this
            break
        if index > idx3:
            schedule_name = row[0]
            # Extract values from 2nd to 13th column for the current row
            row_values = row[1:13].tolist()
            formatted_days = ', '.join(f'"{value}"' for value in row_values)

            output.write(f'"{schedule_name}" = SCHEDULE-PD\n')
            output.write(f"   TYPE             = {type_value}\n")
            output.write(f"   MONTH            = ( {formatted_values1} )\n")
            output.write(f"   DAY              = ( {formatted_values2} )\n")
            output.write(f"   WEEK-SCHEDULES   = ( {formatted_days} )\n")
            output.write("   ..\n")
            output.write("")
    
    output.write("\n\n")
    output.write("$ ---------------------------------------------------------\n")
    output.write("$              THE END\n")
    output.write("$ ---------------------------------------------------------\n\n")
    output.write("END ..\n")
    output.write("COMPUTE ..\n")
    output.write("STOP ..\n")

    # Get the content of the in-memory text stream
    inp_content = output.getvalue()
    
    # Close the StringIO object
    output.close()

    st.success("INP Generated Successfully!")
    st.download_button(
        label="Download INP File",
        data=inp_content,
        file_name=file_name,
        mime="text/plain"
    )
