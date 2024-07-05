import pandas as pd
import streamlit as st
from ScheduleGenerator.src import schedule

def get_file_extension(uploaded_file):
    return uploaded_file.name.split('.')[-1]

def get_schedule(uploaded_file):
    try:
        if uploaded_file is not None:
            file_extension = get_file_extension(uploaded_file)
            if file_extension == 'csv':
                schedules = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            elif file_extension == 'xlsx':
                schedules = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a CSV or XLSX file.")
                return

            schedule.getScheduleINP(schedules)
        else:
            st.info("No file uploaded. Please upload a file and try again.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        
def analytics(uploaded_file):
    try:
        if uploaded_file is not None:
            file_extension = get_file_extension(uploaded_file)
            if file_extension == 'csv':
                data = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                st.title("Visualization between Schedules of 24 hours")
                data = data.drop([0, 6])
                first_col_name = data.columns[0]
                index_to_drop_from = data[data[first_col_name] == "Rows can be added to add more weekly schedule"].index[0]
                data = data[:index_to_drop_from]
                st.write(data)
            elif file_extension == 'xlsx':
                st.title("Visualization between Schedules of 24 hours")
                data = pd.read_excel(uploaded_file)
                data = data.drop([0, 6])
                first_col_name = data.columns[0]
                index_to_drop_from = data[data[first_col_name] == "Rows can be added to add more weekly schedule"].index[0]
                data = data[:index_to_drop_from]
                st.write(data)
        else:
            st.info("No file uploaded. Please upload a file and try again.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    uploaded_file = st.file_uploader("Upload CSV or EXCEL file", type=["csv", "xlsx"])
    get_schedule(uploaded_file)
