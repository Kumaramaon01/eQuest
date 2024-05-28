import os
import streamlit as st
from SIM2PDF.src_pdf import readSim

def main(input_sim_files, reports):
    
    # Check if the path exists and is a directory
    if os.path.exists(input_sim_files):
        st.success(input_sim_files)
        if os.path.isdir(input_sim_files):
            result_message = readSim.extractReport(input_sim_files, reports)
            st.success(result_message)
