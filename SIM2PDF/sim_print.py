import os
import streamlit as st
from SIM2PDF.src_pdf import readSim

def main(input_sim_files, reports):
    # Validate path
    st.success(input_sim_files)
    st.success(reports)
    
    if not os.path.isabs(input_sim_files):
        input_sim_files = os.path.abspath(input_sim_files)
    
    # Check if the path exists and is a directory
    if os.path.exists(input_sim_files):
        if os.path.isdir(input_sim_files):
            result_message = readSim.extractReport(input_sim_files, reports)
            st.success(result_message)
        else:
            st.error("The path exists but is not a directory.")
            print("Error: The path exists but is not a directory.")
    else:
        st.error("Invalid directory path.")
        print("Error: Invalid directory path.")
