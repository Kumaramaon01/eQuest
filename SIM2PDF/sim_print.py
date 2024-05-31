import os
import tempfile
import streamlit as st
from SIM2PDF.src_pdf import readSim

def main(reports, uploaded_files):
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            if not isinstance(uploaded_files, list):
                uploaded_files = [uploaded_files]
            
            # Save uploaded files to temporary directory
            temp_sim_paths = []
            for uploaded_file in uploaded_files:
                temp_sim_path = os.path.join(tmpdirname, uploaded_file.name)
                with open(temp_sim_path, 'wb') as temp_file:
                    temp_file.write(uploaded_file.read())
                temp_sim_paths.append(temp_sim_path)

            st.success(f"Files uploaded and saved to temporary directory: {tmpdirname}")
            
            # Extract reports and generate PDFs
            for sim_path in temp_sim_paths:
                readSim.extractReport(sim_path, reports)
            
            st.success("PDFs Generated Successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
