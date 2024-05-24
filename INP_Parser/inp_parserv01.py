import os
import pandas as pd
import streamlit as st
from INP_Parser.src_inp import hvac_system

def get_report_and_save(report_function, inp_path, file_suffix):
    report = report_function(inp_path)
    # Get the parent directory of the INP file
    parent_directory = os.path.dirname(inp_path)
    file_name = os.path.splitext(os.path.basename(inp_path))[0]
    file_path = os.path.join(parent_directory, f'{file_name}_{file_suffix}.csv')
    if os.path.isfile(file_path):
        os.remove(file_path)
    report.to_csv(file_path, index=False)
    st.success(f"{file_suffix} Report Generated!")

def main(uploaded_file):
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        inp_path = os.path.join(os.path.expanduser("~"), "Downloads", uploaded_file.name)
        with open(inp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Generate reports
        get_report_and_save(hvac_system.get_HVAC_System_report, inp_path, 'Sys_INP')
        get_report_and_save(hvac_system.get_HVAC_Zone_report, inp_path, 'Zone_INP')
        st.success("INP Parsed Successfully!!")

        # Optionally, clean up the temp file after processing
        os.remove(inp_path)