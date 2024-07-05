import os
import re
import streamlit as st
import tempfile
# from BaselineAutomation.src import update_MLC, insertConst, insertGlass, wwr, updateHVAC, HVAC_sys, perging, CLM_delete, update_lpd, updateFreshAir, aa, freshAir

def getTwoSimFiles(input_simp_path, input_simb_path):
    if input_simp_path is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(input_simp_path.getbuffer())
            temp_file_path = temp_file.name
        sim_p_path = temp_file_path

    if input_simb_path is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(input_simb_path.getbuffer())
            temp_file_path = temp_file.name
        sim_b_path = temp_file_path
        
    sim_p_path = sim_p_path.replace('\n', '\r\n')
    sim_b_path = sim_b_path.replace('\n', '\r\n')
    st.info("Hey, This page is under development!!")

     # Data for Output PS-F table
    data_ps_f = {
        'Column 1': ['Data 1', 'Data 2', 'Data 3'],
        'Column 2': ['Data 4', 'Data 5', 'Data 6'],
        'Column 3': ['Data 7', 'Data 8', 'Data 9'],
        'Column 4': ['Data 10', 'Data 11', 'Data 12'],
        'Column 5': ['Data 13', 'Data 14', 'Data 15']
    }

    # Data for ELFH table
    data_elfh = {
        'Column A': ['Value A1', 'Value A2'],
        'Column B': ['Value B1', 'Value B2'],
        'Column C': ['Value C1', 'Value C2']
    }

    # Display Output PS-F table
    st.header('Output PS-F')
    df_ps_f = pd.DataFrame(data_ps_f)
    st.table(df_ps_f)

    # Display ELFH table
    st.header('ELFH table')
    df_elfh = pd.DataFrame(data_elfh)
    st.table(df_elfh)
    
    return 0

if __name__ == "__main__":
    # You can add code here to accept input from the command line if desired
    pass
