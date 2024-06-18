import os
import streamlit as st
import shutil
from fpdf import FPDF
from SIM2PDF.src_pdf import readSim
import PyPDF2
import tempfile

def main(input_sim_files, reports):
    if input_sim_files is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(input_sim_files.getbuffer())
            temp_file_path = temp_file.name
        sim_path = temp_file_path
        
    if os.path.isdir(sim_path):
        st.success(sim_path)
        readSim.extractReport(sim_path, reports)
        st.success("PDFs Generated Successfully!")
    else:
        st.error("Invalid directory path.")
