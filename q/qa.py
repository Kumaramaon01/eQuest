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

# ISSUES IN DATASETS #
###### Useful Condition if 3rd last colmn in LIGHTS is not TOTAL then insert a row #############################
    # Check if the 3rd last value in the LIGHTS column is 'TOTAL'
    if prop_data['LIGHTS'].iloc[-3] != 'TOTAL':
        # Create a new DataFrame with the new row
        new_row = pd.DataFrame({'LIGHTS': ['TOTAL'], 'OTHER_COLUMN': [None]})
        # Insert the new row at the 3rd last position
        prop_data = pd.concat([prop_data.iloc[:-2], new_row, prop_data.iloc[-2:]]).reset_index(drop=True)
    
    if base_data['LIGHTS'].iloc[-3] != 'TOTAL':
        # Create a new DataFrame with the new row
        new_row = pd.DataFrame({'LIGHTS': ['TOTAL'], 'OTHER_COLUMN': [None]})
        # Insert the new row at the 3rd last position
        base_data = pd.concat([base_data.iloc[:-2], new_row, base_data.iloc[-2:]]).reset_index(drop=True)
    
    prop_data['MISC_EQUIP'] = prop_data['MISC_EQUIP'].astype(str)
    base_data['MISC_EQUIP'] = base_data['MISC_EQUIP'].astype(str)
    # Function to correct entries with multiple dots
    def correct_multiple_dots(entry):
        parts = entry.split('.')
        if len(parts) > 2:
            return '.'.join(parts[1:])  # Keep only the first two parts
        return entry

    prop_data['MISC_EQUIP'] = prop_data['MISC_EQUIP'].apply(correct_multiple_dots)
    base_data['MISC_EQUIP'] = base_data['MISC_EQUIP'].apply(correct_multiple_dots)

#############################################################################################################

    # Iterate through the first column to find valid metering names
    for index, metering_name in prop_data.iloc[:, 0].items():
        if str(metering_name).strip() not in ['KWH', 'KW', 'NaN', 'nan', '', 'MAX KW', 'MAX KWH']:
            st.markdown(f"""<h6 style="color:red;">🟢 {metering_name}</h6>""", unsafe_allow_html=True)
            st.markdown("""<h7 style="color:green;"><b>Output PS-F</b></h7>""", unsafe_allow_html=True)
            
            # Check for "TOTAL" in "LIGHTS" column and display the next two rows
            for sub_index in range(index, len(prop_data)):
                if prop_data['LIGHTS'].iloc[sub_index] == "TOTAL":
                    elfh_propKWH = prop_data['LIGHTS'].iloc[sub_index + 1]
                    elfh_propKW = prop_data['LIGHTS'].iloc[sub_index + 2]
                    elfh_baseKWH = base_data['LIGHTS'].iloc[sub_index + 1]
                    elfh_baseKW = base_data['LIGHTS'].iloc[sub_index + 2]

                    equip_propKW = prop_data['MISC_EQUIP'].iloc[sub_index + 2]
                    equip_propKWH = prop_data['MISC_EQUIP'].iloc[sub_index + 1]
                    equip_baseKW = base_data['MISC_EQUIP'].iloc[sub_index + 2]
                    equip_baseKWH = base_data['MISC_EQUIP'].iloc[sub_index + 1]

                    # isssue with the data, so we need to check if the value is NaN or not
                    if elfh_propKWH == 'NaN' or elfh_propKWH == 'nan' or elfh_propKWH == '' or elfh_propKWH == 'KWH':
                        elfh_propKWH = prop_data['TASK_LIGHTS'].iloc[sub_index + 1]
                        equip_propKWH = prop_data['MISC_EQUIP'].iloc[sub_index + 1]
                    if elfh_baseKWH == 'NaN' or elfh_baseKWH == 'nan' or elfh_baseKWH == '' or elfh_baseKWH == 'KWH':
                        elfh_baseKWH = base_data['TASK_LIGHTS'].iloc[sub_index + 1]
                        equip_baseKWH = base_data['MISC_EQUIP'].iloc[sub_index + 1]

                    # converting to numeric so that we can do math later
                    elfh_propKW = pd.to_numeric(elfh_propKW, errors='coerce')
                    elfh_propKWH = pd.to_numeric(elfh_propKWH, errors='coerce')
                    elfh_baseKW = pd.to_numeric(elfh_baseKW, errors='coerce')
                    elfh_baseKWH = pd.to_numeric(elfh_baseKWH, errors='coerce')
                    equip_propKW = pd.to_numeric(equip_propKW, errors='coerce')
                    equip_propKWH = pd.to_numeric(equip_propKWH, errors='coerce')
                    equip_baseKW = pd.to_numeric(equip_baseKW, errors='coerce')
                    equip_baseKWH = pd.to_numeric(equip_baseKWH, errors='coerce')
                    
                    if elfh_propKWH == elfh_propKW:
                        elfh_prop = 1
                    if elfh_baseKWH == elfh_baseKW:
                        elfh_base = 1
                    else:
                        elfh_prop = round((elfh_propKWH / elfh_propKW),2)
                        elfh_base = round((elfh_baseKWH / elfh_baseKW),2)

                    # st.info(f"Next two values after TOTAL in LIGHTS: {elfh_propKWH}, {elfh_propKW}")
                    if elfh_baseKWH == elfh_propKWH:
                        ratio1 = 1
                    if elfh_baseKW == elfh_propKW:
                        ratio2 = 1
                    if equip_baseKWH == equip_propKWH:
                        ratio3 = 1
                    if elfh_baseKWH != elfh_propKWH:
                        ratio1 = (elfh_propKWH / elfh_baseKWH)
                    if elfh_baseKW != elfh_propKW:
                        ratio2 = (elfh_propKW / elfh_baseKW)
                    if equip_baseKWH != equip_propKWH:
                        ratio3 = (equip_propKWH / equip_baseKWH)

                    # Data for Output PS-F table
                    data_ps_f = {
                        'Item': ['Light', 'Light', 'Equipment'],
                        'Unit': ['kWh', 'kW', '-'],
                        'Baseline': [elfh_baseKWH, elfh_baseKW, equip_baseKWH],
                        'Proposed': [elfh_propKWH, elfh_propKW, equip_propKWH],
                        '% savings(1-(P/B))': [(1 - ratio1), (1 - ratio2), (1 - ratio3)]
                    }

                    # Data for ELFH table
                    data_elfh = {
                        'Item': ['Light'],
                        'Baseline(kWh/kW)': [elfh_prop],
                        'Proposed(kWh/kW)': [elfh_base]
                    }
    
                    df_ps_f = pd.DataFrame(data_ps_f)
                    st.table(df_ps_f)

                    # Display ELFH table
                    st.markdown("""<h7 style="color:green;"><b>ELFH table</b></h7>""", unsafe_allow_html=True)
                    df_elfh = pd.DataFrame(data_elfh)
                    st.table(df_elfh)
                    break
    
    return 0

if __name__ == "__main__":
    # You can add code here to accept input from the command line if desired
    pass
