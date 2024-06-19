import os
import streamlit as st
import shutil
from fpdf import FPDF
from SIM2PDF.src_pdf import readSim
import PyPDF2
import tempfile

# Function to process and convert SIM files to PDF
def main(reports, input_sim_files):
    st.success("Inside sim_print.py")
    st.success([file.name for file in input_sim_files])

    if input_sim_files is not None and isinstance(input_sim_files, list):
        for input_sim_file in input_sim_files:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Save the uploaded file temporarily
                    sim_path = os.path.join(temp_dir, input_sim_file.name)
                    with open(sim_path, "wb") as f:
                        f.write(input_sim_file.getbuffer())
                    
                    # Process the SIM file
                    readSim.extractReport(sim_path, reports)
                    st.success(f"PDF Generated Successfully for {input_sim_file.name}!")
            
            except Exception as e:
                st.error(f"An error occurred while processing SIM file {input_sim_file.name}: {e}")
    else:
        st.error("No files uploaded or invalid input.")
