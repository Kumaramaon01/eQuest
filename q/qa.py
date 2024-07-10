import streamlit as st
import tempfile
import pandas as pd
from q.src import psf

def getTwoSimFiles(input_simp_path, input_simb_path):
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

    prop_data = psf.get_PSF_report_Prop(sim_p_path)
    base_data = psf.get_PSF_report_Base(sim_b_path)

    if prop_data is None or base_data is None:
        st.error("Error: Failed to retrieve simulation data.")
        return

    # Handle trailing columns in LIGHTS and MISC_EQUIP
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
            fans_propKW, fans_propKWH = None, None
            fans_baseKW, fans_baseKWH = None, None

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

                    fans_propKW = prop_data['VENT FANS'].iloc[sub_index + 2]
                    fans_propKWH = prop_data['VENT FANS'].iloc[sub_index + 1]
                    fans_baseKW = base_data['VENT FANS'].iloc[sub_index + 2]
                    fans_baseKWH = base_data['VENT FANS'].iloc[sub_index + 1] if base_data is not None else None

                    if elfh_propKWH in ['NaN', 'nan', '', 'KWH']:
                        elfh_propKWH = prop_data['TASK_LIGHTS'].iloc[sub_index + 1]
                        equip_propKWH = prop_data['MISC_EQUIP'].iloc[sub_index + 1]
                        fans_propKWH = prop_data['VENT FANS'].iloc[sub_index + 1]

                    if elfh_baseKWH in ['NaN', 'nan', '', 'KWH']:
                        elfh_baseKWH = base_data['TASK_LIGHTS'].iloc[sub_index + 1] if base_data is not None else None
                        equip_baseKWH = base_data['MISC_EQUIP'].iloc[sub_index + 1] if base_data is not None else None
                        fans_baseKWH = base_data['VENT FANS'].iloc[sub_index + 1] if base_data is not None else None

                    # Convert to numeric and round to 1 decimal place
                    elfh_propKW = pd.to_numeric(elfh_propKW, errors='coerce').round(1)
                    elfh_propKWH = pd.to_numeric(elfh_propKWH, errors='coerce').round(1)
                    elfh_baseKW = pd.to_numeric(elfh_baseKW, errors='coerce').round(1)
                    elfh_baseKWH = pd.to_numeric(elfh_baseKWH, errors='coerce').round(1)
                    equip_propKW = pd.to_numeric(equip_propKW, errors='coerce').round(1)
                    equip_propKWH = pd.to_numeric(equip_propKWH, errors='coerce').round(1)
                    equip_baseKW = pd.to_numeric(equip_baseKW, errors='coerce').round(1)
                    equip_baseKWH = pd.to_numeric(equip_baseKWH, errors='coerce').round(1)
                    fans_propKW = pd.to_numeric(fans_propKW, errors='coerce').round(1)
                    fans_propKWH = pd.to_numeric(fans_propKWH, errors='coerce').round(1)
                    fans_baseKW = pd.to_numeric(fans_baseKW, errors='coerce').round(1)
                    fans_baseKWH = pd.to_numeric(fans_baseKWH, errors='coerce').round(1)

                    # LIGHTS
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
                    
                    # EQUIPMENT
                    if equip_propKWH == equip_propKW and equip_propKW != 0:
                        equip_prop = 1
                    elif equip_propKWH == equip_propKW and equip_propKW == 0:
                        equip_prop = 0
                    else:
                        equip_prop = round((equip_propKWH / equip_propKW), 1)

                    if equip_baseKWH == equip_baseKW and equip_baseKW != 0:
                        equip_base = 1
                    elif equip_baseKWH == equip_baseKW and equip_baseKW == 0:
                        equip_base = 0
                    else:
                        equip_base = round((equip_baseKWH / equip_baseKW), 1)

                    # FANS
                    if fans_propKWH == fans_propKW and fans_propKW != 0:
                        fans_prop = 1
                    elif fans_propKWH == fans_propKW and fans_propKW == 0:
                        fans_prop = 0
                    else:
                        fans_prop = round((fans_propKWH / fans_propKW), 1)
                    
                    if fans_baseKWH == fans_baseKW and fans_baseKW != 0:
                        fans_base = 1
                    elif fans_baseKWH == fans_baseKW and fans_baseKW == 0:
                        fans_base = 0
                    else:
                        fans_base = round((fans_baseKWH / fans_baseKW), 1)

                    ratio1 = 0 if elfh_baseKWH == elfh_propKWH and elfh_baseKWH == 0 else round((elfh_propKWH / elfh_baseKWH), 1)
                    ratio2 = 0 if elfh_baseKW == elfh_propKW  and elfh_baseKW == 0 else round((elfh_propKW / elfh_baseKW), 1)
                    ratio3 = 0 if equip_baseKWH == equip_propKWH and equip_baseKWH == 0  else round((equip_propKWH / equip_baseKWH), 1)
                    ratio4 = 0 if equip_baseKW == equip_propKW and equip_baseKW == 0  else round((equip_propKW / equip_baseKW), 1)
                    ratio5 = 0 if fans_baseKWH == fans_propKWH and fans_baseKWH == 0  else round((fans_propKWH / fans_baseKWH), 1)
                    ratio6 = 0 if fans_baseKW == fans_propKW and fans_baseKW == 0  else round((fans_propKW / fans_baseKW), 1)

                    data_ps_f = {
                        'Item': ['Light', 'Light', 'Equipment', 'Equipment', 'Vent Fans', 'Vent Fans'],
                        'Unit': ['kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW'],
                        'Baseline': [elfh_baseKWH, elfh_baseKW, equip_baseKWH, equip_baseKW, fans_baseKWH, fans_baseKW],
                        'Proposed': [elfh_propKWH, elfh_propKW, equip_propKWH, equip_propKW, fans_propKWH, fans_propKW],
                        '% savings(1-(P/B))': [(1 - ratio1), (1 - ratio2), (1 - ratio3), (1 - ratio4), (1 - ratio5), (1 - ratio6)]
                    }

                    data_elfh = {
                        'Item': ['Light', 'Equipment', 'Vent Fans'],
                        'Baseline(kWh/kW)': [elfh_base, equip_base, fans_base],
                        'Proposed(kWh/kW)': [elfh_prop, equip_prop, fans_prop],
                    }

                    # Create DataFrames
                    df_ps_f = pd.DataFrame(data_ps_f)
                    df_elfh = pd.DataFrame(data_elfh)

                    # Display tables with 1 decimal place using st.write
                    # st.write("**Output PS-F**")
                    st.table(df_ps_f.style.format({
                        'Baseline': '{:.1f}',
                        'Proposed': '{:.1f}',
                        '% savings(1-(P/B))': '{:.1%}'
                    }))

                    st.markdown("""<h7 style="color:green;"><b>ELFH table</b></h7>""", unsafe_allow_html=True)
                    st.table(df_elfh.style.format({
                        'Baseline(kWh/kW)': '{:.1f}',
                        'Proposed(kWh/kW)': '{:.1f}'
                    }))
                    break
    
    return 0

if __name__ == "__main__":
    # You can add code here to accept input from the command line if desired
    pass
