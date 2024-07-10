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
    else:
        st.error("Error: No input for simulation P file.")
        return
    
    if input_simb_path is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(input_simb_path.getbuffer())
            temp_file_path = temp_file.name
        sim_b_path = temp_file_path
    else:
        st.error("Error: No input for simulation B file.")
        return
        
    sim_p_path = sim_p_path.replace('\n', '\r\n')
    sim_b_path = sim_b_path.replace('\n', '\r\n')

    prop_data = psf.get_PSF_report_Prop(sim_p_path)
    base_data = psf.get_PSF_report_Base(sim_b_path)

    if prop_data is None or base_data is None:
        st.error("Error: Failed to retrieve simulation data.")
        return

    # ISSUES IN DATASETS #
    # Useful Condition if 3rd last column in LIGHTS is not TOTAL then insert a row
    if prop_data['LIGHTS'].iloc[-3] != 'TOTAL':
        new_row = pd.DataFrame({'LIGHTS': ['TOTAL'], 'OTHER_COLUMN': [None]})
        prop_data = pd.concat([prop_data.iloc[:-2], new_row, prop_data.iloc[-2:]]).reset_index(drop=True)
    
    if base_data['LIGHTS'].iloc[-3] != 'TOTAL':
        new_row = pd.DataFrame({'LIGHTS': ['TOTAL'], 'OTHER_COLUMN': [None]})
        base_data = pd.concat([base_data.iloc[:-2], new_row, base_data.iloc[-2:]]).reset_index(drop=True)
    
    prop_data['MISC_EQUIP'] = prop_data['MISC_EQUIP'].astype(str)
    base_data['MISC_EQUIP'] = base_data['MISC_EQUIP'].astype(str)

    def correct_multiple_dots(entry):
        parts = entry.split('.')
        if len(parts) > 2:
            return '.'.join(parts[1:])
        return entry

    prop_data['MISC_EQUIP'] = prop_data['MISC_EQUIP'].apply(correct_multiple_dots)
    base_data['MISC_EQUIP'] = base_data['MISC_EQUIP'].apply(correct_multiple_dots)

    for index, metering_name in prop_data.iloc[:, 0].items():
        if str(metering_name).strip() not in ['KWH', 'KW', 'NaN', 'nan', '', 'MAX KW', 'MAX KWH']:
            st.markdown(f"""<h6 style="color:red;">🟢 {metering_name}</h6>""", unsafe_allow_html=True)
            st.markdown("""<h7 style="color:green;"><b>Output PS-F</b></h7>""", unsafe_allow_html=True)

            elfh_propKWH, elfh_propKW = None, None
            elfh_baseKWH, elfh_baseKW = None, None
            equip_propKW, equip_propKWH = None, None
            equip_baseKW, equip_baseKWH = None, None

            for sub_index in range(index, len(prop_data)):
                if prop_data['LIGHTS'].iloc[sub_index] == "TOTAL":
                    elfh_propKWH = prop_data['LIGHTS'].iloc[sub_index + 1]
                    elfh_propKW = prop_data['LIGHTS'].iloc[sub_index + 2]
                    elfh_baseKWH = base_data['LIGHTS'].iloc[sub_index + 1]
                    elfh_baseKW = base_data['LIGHTS'].iloc[sub_index + 2] if base_data is not None else None

                    equip_propKW = prop_data['MISC_EQUIP'].iloc[sub_index + 2]
                    equip_propKWH = prop_data['MISC_EQUIP'].iloc[sub_index + 1]
                    equip_baseKW = base_data['MISC_EQUIP'].iloc[sub_index + 2]
                    equip_baseKWH = base_data['MISC_EQUIP'].iloc[sub_index + 1] if base_data is not None else None

                    if elfh_propKWH in ['NaN', 'nan', '', 'KWH']:
                        elfh_propKWH = prop_data['TASK_LIGHTS'].iloc[sub_index + 1]
                        equip_propKWH = prop_data['MISC_EQUIP'].iloc[sub_index + 1]

                    if elfh_baseKWH in ['NaN', 'nan', '', 'KWH']:
                        elfh_baseKWH = base_data['TASK_LIGHTS'].iloc[sub_index + 1] if base_data is not None else None
                        equip_baseKWH = base_data['MISC_EQUIP'].iloc[sub_index + 1] if base_data is not None else None

                    elfh_propKW = pd.to_numeric(elfh_propKW, errors='coerce')
                    elfh_propKWH = pd.to_numeric(elfh_propKWH, errors='coerce')
                    elfh_baseKW = pd.to_numeric(elfh_baseKW, errors='coerce')
                    elfh_baseKWH = pd.to_numeric(elfh_baseKWH, errors='coerce')
                    equip_propKW = pd.to_numeric(equip_propKW, errors='coerce')
                    equip_propKWH = pd.to_numeric(equip_propKWH, errors='coerce')
                    equip_baseKW = pd.to_numeric(equip_baseKW, errors='coerce')
                    equip_baseKWH = pd.to_numeric(equip_baseKWH, errors='coerce')

                    if elfh_propKWH == elfh_propKW and elfh_propKW != 0:
                        elfh_prop = 1
                    elif elfh_propKWH == elfh_propKW and elfh_propKW == 0:
                        elfh_prop = 0
                    else:
                        elfh_prop = round((elfh_propKWH / elfh_propKW), 1)

                    if elfh_baseKWH == elfh_baseKW and elfh_baseKW != 0:
                        elfh_base = 1
                    elif elfh_baseKWH == elfh_baseKW and elfh_baseKW == 0:
                        elfh_base = 0
                    else:
                        elfh_base = round((elfh_baseKWH / elfh_baseKW), 1)

                    ratio1 = 0 if elfh_baseKWH == elfh_propKWH and elfh_baseKWH == 0 else round((elfh_propKWH / elfh_baseKWH), 1)
                    ratio2 = 0 if elfh_baseKW == elfh_propKW  and elfh_baseKW == 0 else round((elfh_propKW / elfh_baseKW), 1)
                    ratio3 = 0 if equip_baseKWH == equip_propKWH and equip_baseKWH == 0  else round((equip_propKWH / equip_baseKWH), 1)

                    data_ps_f = {
                        'Item': ['Light', 'Light', 'Equipment'],
                        'Unit': ['kWh', 'kW', '-'],
                        'Baseline': [round(elfh_baseKWH, 1), round(elfh_baseKW, 1), round(equip_baseKWH, 1)],
                        'Proposed': [round(elfh_propKWH, 1), round(elfh_propKW, 1), round(equip_propKWH, 1)],
                        '% savings(1-(P/B))': [(1 - ratio1), (1 - ratio2), (1 - ratio3)]
                    }

                    data_elfh = {
                        'Item': ['Light'],
                        'Baseline(kWh/kW)': [elfh_base],
                        'Proposed(kWh/kW)': [elfh_prop]
                    }

                    df_ps_f = pd.DataFrame(data_ps_f)
                    st.table(df_ps_f)

                    st.markdown("""<h7 style="color:green;"><b>ELFH table</b></h7>""", unsafe_allow_html=True)
                    df_elfh = pd.DataFrame(data_elfh)
                    st.table(df_elfh)
                    break
    
    return 0

if __name__ == "__main__":
    # You can add code here to accept input from the command line if desired
    pass
