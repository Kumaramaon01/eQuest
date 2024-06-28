import pandas as pd
import streamlit as st
from ScheduleGenerator.src import schedule

def getCSV(uploaded_file):
    try:
        # Check if the uploaded file is not None
        if uploaded_file is not None:
            schedules = pd.read_csv(uploaded_file)
            schedule.getScheduleINP(schedules)
        else:
            st.success("No file uploaded. Please upload a file and try again.")
    except Exception as e:
        st.success(f"An error occurred while reading the CSV file: {e}")
        
if __name__ == "__main__":
    uploaded_file = st.file_uploader("Upload CSV or EXCEL file", type=["csv", "xlsx"])
    getCSV(uploaded_file)
