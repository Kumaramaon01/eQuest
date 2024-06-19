import os
import streamlit as st
import shutil
from fpdf import FPDF
from SIM2PDF.src_pdf import readSim
import PyPDF2
import tempfile

def main(reports, input_sim_files):
    st.success("Inside sim_print.py")
    st.success(input_sim_files)
    if input_sim_files is not None:
        try:
            with tempfile.NamedTemporaryFile() as temp_dir:
                # Save the uploaded file temporarily
                sim_path = os.path.join(temp_dir, input_sim_files.name)
                with open(sim_path, "wb") as f:
                    f.write(input_sim_files.getbuffer())
                sim_path = sim_path.replace('\n', '\r\n')
        
                if os.path.isdir(sim_path):
                    st.success(sim_path)
                    readSim.extractReport(sim_path, reports)
                    st.success("PDFs Generated Successfully!")
                else:
                    st.error("Invalid directory path.")
            
        except Exception as e:
            st.error(f"An error occurred while updating SIM file: {e}")
            return None, None
