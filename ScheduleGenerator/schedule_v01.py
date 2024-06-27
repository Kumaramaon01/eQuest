import os
import pandas as pd
from src import schedule

def main(uploaded_file)
    if not os.path.exists(uploaded_file):
        print("The file does not exist. Please check the path and try again.")
    else:
        try:
            schedules = pd.read_csv(uploaded_file)
            schedule.getScheduleINP(schedules)
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
        
if __name__ == "__main__":
    uploaded_file = st.file_uploader("Upload your INP file", type=["inp"])
    main(uploaded_file)
