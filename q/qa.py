import os
import re
import streamlit as st
import tempfile
import pandas as pd
from q.src import psf

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

    prop_data = psf.get_PSF_report_Prop(sim_p_path)
    base_data = psf.get_PSF_report_Base(sim_b_path)
    
    # elfh baseline and proposed
    elfh_propKW = prop_data['LIGHTS'].iloc[-1]
    elfh_propKWH = prop_data['LIGHTS'].iloc[-2]
    elfh_baseKW = base_data['LIGHTS'].iloc[-1]
    elfh_baseKWH = base_data['LIGHTS'].iloc[-2]
    
    # equipment baseline and proposed
    equip_propKW = prop_data['MISC_EQUIP'].iloc[-1]
    equip_propKWH = prop_data['MISC_EQUIP'].iloc[-2]
    equip_baseKW = base_data['MISC_EQUIP'].iloc[-1]
    equip_baseKWH = base_data['MISC_EQUIP'].iloc[-2]

    # converting to numeric so that we can do math later
    elfh_propKW = pd.to_numeric(elfh_propKW, errors='coerce')
    elfh_propKWH = pd.to_numeric(elfh_propKWH, errors='coerce')
    elfh_baseKW = pd.to_numeric(elfh_baseKW, errors='coerce')
    elfh_baseKWH = pd.to_numeric(elfh_baseKWH, errors='coerce')
    equip_propKW = pd.to_numeric(equip_propKW, errors='coerce')
    equip_propKWH = pd.to_numeric(equip_propKWH, errors='coerce')
    equip_baseKW = pd.to_numeric(equip_baseKW, errors='coerce')
    equip_baseKWH = pd.to_numeric(equip_baseKWH, errors='coerce')
    
    elfh_prop = round((elfh_propKWH / elfh_propKW),2)
    elfh_base = round((elfh_baseKWH / elfh_baseKW),2)

    # Data for Output PS-F table
    data_ps_f = {
        'Item': ['Light', 'Light', 'Equipment'],
        'Unit': ['kWh', 'kW', '-'],
        'Baseline': [elfh_baseKWH, elfh_baseKW, 'Data 9'],
        'Proposed': [elfh_propKWH, elfh_propKW, 'Data 12'],
        '% savings(1-(P/B))': [(1 - (elfh_propKWH / elfh_baseKWH)), (1 - (elfh_propKW / elfh_baseKW)), (1 - (equip_propKWH / equip_baseKWH))]
    }

    # Data for ELFH table
    data_elfh = {
        'Item': ['Light'],
        'Baseline(kWh/kW)': [elfh_prop],
        'Proposed(kWh/kW)': [elfh_base]
    }

    # Display Output PS-F table
    st.markdown("""
    <h4 style="color:red;">Output PS-F</h4>""", unsafe_allow_html=True)
    df_ps_f = pd.DataFrame(data_ps_f)
    st.table(df_ps_f)

    # Display ELFH table
    st.markdown("""
    <h4 style="color:red;">ELFH table</h4>""", unsafe_allow_html=True)
    df_elfh = pd.DataFrame(data_elfh)
    st.table(df_elfh)
    
    return 0

if __name__ == "__main__":
    # You can add code here to accept input from the command line if desired
    pass
