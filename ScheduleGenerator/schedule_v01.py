import os
import pandas as pd
from ScheduleGenerator.src import schedule
import streamlit as st

def getCSV(uploaded_file):
    if not os.path.exists(uploaded_file):
        st.success("The file does not exist. Please check the path and try again.")
    else:
        try:
            schedules = pd.read_csv(uploaded_file)
            schedule.getScheduleINP(schedules)
        except Exception as e:
            st.success(f"An error occurred while reading the CSV file: {e}")
        
if __name__ == "__main__":
    # uploaded_file = st.file_uploader("Upload CSV or EXCEL file", type=["csv", "xlsx"])
    # main(uploaded_file)
    pass
