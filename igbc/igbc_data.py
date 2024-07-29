import os
import pandas as pd
from igbc.src import igbc_parser
import streamlit as st
import tempfile
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def getINPSimFiles(input_simp_path, input_simb_path):
    if input_simp_path is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(input_simp_path.getbuffer())
            sim_p_path = temp_file.name
    else:
        st.error("Error: No input for simulation P file.")
        return
    
    if input_simb_path is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(input_simb_path.getbuffer())
            sim_b_path = temp_file.name
    else:
        st.error("Error: No input for simulation B file.")
        return
    
    sim_p_path = sim_p_path.replace('\n', '\r\n')
    sim_b_path = sim_b_path.replace('\n', '\r\n')

    get_report1, get_report2 = igbc_parser.get_HVAC_Zone_report(sim_p_path, sim_b_path)

    if get_report1 is not None:
        st.write(get_report1)
        # Download CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Output",
            data=csv,
            file_name='report.csv',
            mime='text/csv'
        )
    if get_report2 is not None:
        st.write(get_report2)
        # Download CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Output",
            data=csv,
            file_name='report.csv',
            mime='text/csv'
        )
    elif get_report1 is None:
        st.info("Data Not found!")
    elif get_report2 is None:
        st.info("Data Not found!")
