import os
import tempfile
import streamlit as st
from SIM2PDF.src_pdf import readSim

def main(reports, uploaded_file):
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Save the uploaded file to a temporary directory
            temp_sim_path = os.path.join(tmpdirname, uploaded_file.name)
            with open(temp_sim_path, 'wb') as temp_file:
                temp_file.write(uploaded_file.read())
            
            st.success(f"File uploaded and saved to temporary directory: {temp_sim_path}")
            
            # Extract reports and generate PDFs
            readSim.extractReport(temp_sim_path, reports)
            
            st.success("PDFs Generated Successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
