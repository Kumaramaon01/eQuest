# import os
# import streamlit as st
# import shutil
# from fpdf import FPDF
# from SIM2PDF.src_pdf import readSim
# import PyPDF2

# def main(input_sim_files, reports):
#         if os.path.isdir(input_sim_files):
#             readSim.extractReport(input_sim_files, reports)
#             st.success("PDFs Generated Successfully!")
#         else:
#             st.error("Invalid directory path.")

import os
import shutil
from fpdf import FPDF
import PyPDF2

def main(input_sim_files, reports):
    try:
        print("Received directory path:", input_sim_files)  # Debugging output
        input_sim_files = os.path.normpath(input_sim_files)  # Normalize the path
        if os.path.isdir(input_sim_files):
            readSim.extractReport(input_sim_files, reports)
            print("PDFs Generated Successfully!")
        else:
            print("Directory does not exist or is not a directory.")
    except Exception as e:
        print("Error:", e)
