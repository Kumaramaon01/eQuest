import os
import streamlit as st
from SIM2PDF.src_pdf import readSim

def main(input_sim_files, reports):
   input_sim = input_sim_files
    if os.path.isdir(input_sim):
        st.success(f"The provided path '{input_sim}' exists and is a directory.")
        result_message = readSim.extractReport(input_sim, reports)
        st.success(result_message)
    else:
        st.error(f"The provided path '{input_sim}' does not exist or is not a directory.")
