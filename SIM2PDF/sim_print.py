import os
import streamlit as st
from fpdf import FPDF
from SIM2PDF.src_pdf import readSim
import tempfile

def main(reports, uploaded_file):
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Save the uploaded file to a temporary directory
        temp_sim_path = os.path.join(tmpdirname, uploaded_file.name)
        with open(temp_sim_path, 'wb') as temp_file:
            temp_file.write(uploaded_file.read())
        
        st.success("File uploaded and saved to temporary directory.")
        
        # Extract reports and generate PDFs
        readSim.extractReport(temp_sim_path, reports)
        
        st.success("PDFs Generated Successfully!")
