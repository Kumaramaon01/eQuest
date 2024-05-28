import os
import streamlit as st
from SIM2PDF.src_pdf import readSim

def main(input_sim_files, reports):
    # Check if the path exists and is a directory
    input_sim_files = input_sim_files.strip()
    
    if os.path.isdir(input_sim_files):
        st.success(f"The provided path '{input_sim_files}' exists and is a directory.")
        result_message = readSim.extractReport(input_sim_files, reports)
        st.success(result_message)
    else:
        st.error(f"The provided path '{input_sim_files}' does not exist or is not a directory.")
