import os
import streamlit as st
from SIM2PDF.src_pdf import readSim

def main(input_sim_files, reports):
    try:
        st.success(f"The provided path '{input_sim_files.name}' exists and is a directory.")
        result_message = readSim.extractReport(input_sim_files.name, reports)
        st.success(result_message)
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
