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
            cool_propKW, cool_propKWH = None, None
            cool_baseKW, cool_baseKWH = None, None
            heat_propKW, heat_propKWH = None, None
            heat_baseKW, heat_baseKWH = None, None
            ext_propKW, ext_propKWH = None, None
            ext_baseKW, ext_baseKWH = None, None
            domest_propKW, domest_propKWH = None, None
            domest_baseKW, domest_baseKWH = None, None
            pumps_propKW, pumps_propKWH = None, None
            pumps_baseKW, pumps_baseKWH = None, None
            refringe_propKW, refringe_propKWH = None, None
            refringe_baseKW, refringe_baseKWH = None, None
            ht_pump_propKW, ht_pump_propKWH = None, None
            ht_pump_baseKW, ht_pump_baseKWH = None, None
            total_propKW, total_propKWH = None, None
            total_baseKW, total_baseKWH = None, None

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

                    cool_propKW = prop_data['SPACE_COOLING'].iloc[sub_index + 2]
                    cool_propKWH = prop_data['SPACE_COOLING'].iloc[sub_index + 1]
                    cool_baseKW = base_data['SPACE_COOLING'].iloc[sub_index + 2]
                    cool_baseKWH = base_data['SPACE_COOLING'].iloc[sub_index + 1] if base_data is not None else None

                    heat_propKW = prop_data['HEAT_REJECT'].iloc[sub_index + 2]
                    heat_propKWH = prop_data['HEAT_REJECT'].iloc[sub_index + 1]
                    heat_baseKW = base_data['HEAT_REJECT'].iloc[sub_index + 2]
                    heat_baseKWH = base_data['HEAT_REJECT'].iloc[sub_index + 1] if base_data is not None else None

                    ext_propKW = prop_data['EXT USAGE'].iloc[sub_index + 2]
                    ext_propKWH = prop_data['EXT USAGE'].iloc[sub_index + 1]
                    ext_baseKW = base_data['EXT USAGE'].iloc[sub_index + 2]
                    ext_baseKWH = base_data['EXT USAGE'].iloc[sub_index + 1] if base_data is not None else None

                    domest_propKW = prop_data['DOMEST HOT WTR'].iloc[sub_index + 2]
                    domest_propKWH = prop_data['DOMEST HOT WTR'].iloc[sub_index + 1]
                    domest_baseKW = base_data['DOMEST HOT WTR'].iloc[sub_index + 2]
                    domest_baseKWH = base_data['DOMEST HOT WTR'].iloc[sub_index + 1] if base_data is not None else None

                    pumps_propKW = prop_data['PUMPS & AUX'].iloc[sub_index + 2]
                    pumps_propKWH = prop_data['PUMPS & AUX'].iloc[sub_index + 1]
                    pumps_baseKW = base_data['PUMPS & AUX'].iloc[sub_index + 2]
                    pumps_baseKWH = base_data['PUMPS & AUX'].iloc[sub_index + 1] if base_data is not None else None

                    refringe_propKW = prop_data['REFRIG DISPLAY'].iloc[sub_index + 2]
                    refringe_propKWH = prop_data['REFRIG DISPLAY'].iloc[sub_index + 1]
                    refringe_baseKW = base_data['REFRIG DISPLAY'].iloc[sub_index + 2]
                    refringe_baseKWH = base_data['REFRIG DISPLAY'].iloc[sub_index + 1] if base_data is not None else None

                    ht_pump_propKW = prop_data['HT PUMP SUPPLEM'].iloc[sub_index + 2]
                    ht_pump_propKWH = prop_data['HT PUMP SUPPLEM'].iloc[sub_index + 1]
                    ht_pump_baseKW = base_data['HT PUMP SUPPLEM'].iloc[sub_index + 2]
                    ht_pump_baseKWH = base_data['HT PUMP SUPPLEM'].iloc[sub_index + 1] if base_data is not None else None

                    total_propKW = prop_data['TOTAL'].iloc[sub_index + 2]
                    total_propKWH = prop_data['TOTAL'].iloc[sub_index + 1]
                    total_baseKW = base_data['TOTAL'].iloc[sub_index + 2]
                    total_baseKWH = base_data['TOTAL'].iloc[sub_index + 1] if base_data is not None else None

                    if elfh_propKWH in ['NaN', 'nan', '', 'KWH']:
                        elfh_propKWH = prop_data['TASK_LIGHTS'].iloc[sub_index + 1]
                        equip_propKWH = prop_data['MISC_EQUIP'].iloc[sub_index + 1]
                        fans_propKWH = prop_data['VENT FANS'].iloc[sub_index + 1]
                        cool_propKWH = prop_data['SPACE_COOLING'].iloc[sub_index + 1]
                        heat_propKWH = prop_data['HEAT_REJECT'].iloc[sub_index + 1]
                        ext_propKWH = prop_data['EXT USAGE'].iloc[sub_index + 1]
                        domest_propKWH = prop_data['DOMEST HOT WTR'].iloc[sub_index + 1]
                        pumps_propKWH = prop_data['PUMPS & AUX'].iloc[sub_index + 1]
                        refringe_propKWH = prop_data['REFRIG DISPLAY'].iloc[sub_index + 1]
                        ht_pump_propKWH = prop_data['HT PUMP SUPPLEM'].iloc[sub_index + 1]
                        total_propKWH = prop_data['TOTAL'].iloc[sub_index + 1]

                    if elfh_baseKWH in ['NaN', 'nan', '', 'KWH']:
                        elfh_baseKWH = base_data['TASK_LIGHTS'].iloc[sub_index + 1] if base_data is not None else None
                        equip_baseKWH = base_data['MISC_EQUIP'].iloc[sub_index + 1] if base_data is not None else None
                        fans_baseKWH = base_data['VENT FANS'].iloc[sub_index + 1] if base_data is not None else None
                        cool_baseKWH = base_data['SPACE_COOLING'].iloc[sub_index + 1] if base_data is not None else None
                        heat_baseKWH = base_data['HEAT_REJECT'].iloc[sub_index + 1] if base_data is not None else None
                        ext_baseKWH = base_data['EXT USAGE'].iloc[sub_index + 1] if base_data is not None else None
                        domest_baseKWH = base_data['DOMEST HOT WTR'].iloc[sub_index + 1] if base_data is not None else None
                        pumps_baseKWH = base_data['PUMPS & AUX'].iloc[sub_index + 1] if base_data is not None else None
                        refringe_baseKWH = base_data['REFRIG DISPLAY'].iloc[sub_index + 1] if base_data is not None else None
                        ht_pump_baseKWH = base_data['HT PUMP SUPPLEM'].iloc[sub_index + 1] if base_data is not None else None
                        total_baseKWH = base_data['TOTAL'].iloc[sub_index + 1] if base_data is not None else None

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
                    cool_propKW = pd.to_numeric(cool_propKW, errors='coerce').round(1)
                    cool_propKWH = pd.to_numeric(cool_propKWH, errors='coerce').round(1)
                    cool_baseKW = pd.to_numeric(cool_baseKW, errors='coerce').round(1)
                    cool_baseKWH = pd.to_numeric(cool_baseKWH, errors='coerce').round(1)
                    heat_propKW = pd.to_numeric(heat_propKW, errors='coerce').round(1)
                    heat_propKWH = pd.to_numeric(heat_propKWH, errors='coerce').round(1)
                    heat_baseKW = pd.to_numeric(heat_baseKW, errors='coerce').round(1)
                    heat_baseKWH = pd.to_numeric(heat_baseKWH, errors='coerce').round(1)
                    ext_propKW = pd.to_numeric(ext_propKW, errors='coerce').round(1)
                    ext_propKWH = pd.to_numeric(ext_propKWH, errors='coerce').round(1)
                    ext_baseKW = pd.to_numeric(ext_baseKW, errors='coerce').round(1)
                    ext_baseKWH = pd.to_numeric(ext_baseKWH, errors='coerce').round(1)
                    domest_propKW = pd.to_numeric(domest_propKW, errors='coerce').round(1)
                    domest_propKWH = pd.to_numeric(domest_propKWH, errors='coerce').round(1)
                    domest_baseKW = pd.to_numeric(domest_baseKW, errors='coerce').round(1)
                    domest_baseKWH = pd.to_numeric(domest_baseKWH, errors='coerce').round(1)
                    pumps_propKW = pd.to_numeric(pumps_propKW, errors='coerce').round(1)
                    pumps_propKWH = pd.to_numeric(pumps_propKWH, errors='coerce').round(1)
                    pumps_baseKW = pd.to_numeric(pumps_baseKW, errors='coerce').round(1)
                    pumps_baseKWH = pd.to_numeric(pumps_baseKWH, errors='coerce').round(1)
                    refringe_propKW = pd.to_numeric(refringe_propKW, errors='coerce').round(1)
                    refringe_propKWH = pd.to_numeric(refringe_propKWH, errors='coerce').round(1)
                    refringe_baseKW = pd.to_numeric(refringe_baseKW, errors='coerce').round(1)
                    refringe_baseKWH = pd.to_numeric(refringe_baseKWH, errors='coerce').round(1)
                    ht_pump_propKW = pd.to_numeric(ht_pump_propKW, errors='coerce').round(1)
                    ht_pump_propKWH = pd.to_numeric(ht_pump_propKWH, errors='coerce').round(1)
                    ht_pump_baseKW = pd.to_numeric(ht_pump_baseKW, errors='coerce').round(1)
                    ht_pump_baseKWH = pd.to_numeric(ht_pump_baseKWH, errors='coerce').round(1)
                    total_propKW = pd.to_numeric(total_propKW, errors='coerce').round(1)
                    total_propKWH = pd.to_numeric(total_propKWH, errors='coerce').round(1)
                    total_baseKW = pd.to_numeric(total_baseKW, errors='coerce').round(1)
                    total_baseKWH = pd.to_numeric(total_baseKWH, errors='coerce').round(1)

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

                    # COOLING
                    if cool_propKWH == cool_propKW and cool_propKW != 0:
                        cool_prop = 1
                    elif cool_propKWH == cool_propKW and cool_propKW == 0:
                        cool_prop = 0
                    else:
                        cool_prop = round((cool_propKWH / cool_propKW), 1)
                    
                    if cool_baseKWH == cool_baseKW and cool_baseKW != 0:
                        cool_base = 1
                    elif cool_baseKWH == cool_baseKW and cool_baseKW == 0:
                        cool_base = 0
                    else:
                        cool_base = round((cool_baseKWH / cool_baseKW), 1)

                    # HEATING
                    if heat_propKWH == heat_propKW and heat_propKW != 0:
                        heat_prop = 1
                    elif heat_propKWH == heat_propKW and heat_propKW == 0:
                        heat_prop = 0
                    else:
                        heat_prop = round((heat_propKWH / heat_propKW), 1)

                    if heat_baseKWH == heat_baseKW and heat_baseKW != 0:
                        heat_base = 1
                    elif heat_baseKWH == heat_baseKW and heat_baseKW == 0:
                        heat_base = 0
                    else:
                        heat_base = round((heat_baseKWH / heat_baseKW), 1)
                    
                    # EXTERNAL
                    if ext_propKWH == ext_propKW and ext_propKW != 0:
                        ext_prop = 1
                    elif ext_propKWH == ext_propKW and ext_propKW == 0:
                        ext_prop = 0
                    else:
                        ext_prop = round((ext_propKWH / ext_propKW), 1)
                    
                    if ext_baseKWH == ext_baseKW and ext_baseKW != 0:
                        ext_base = 1
                    elif ext_baseKWH == ext_baseKW and ext_baseKW == 0:
                        ext_base = 0
                    else:
                        ext_base = round((ext_baseKWH / ext_baseKW), 1)
                    
                    # DOMESTIC
                    if domest_propKWH == domest_propKW and domest_propKW != 0:
                        domest_prop = 1
                    elif domest_propKWH == domest_propKW and domest_propKW == 0:
                        domest_prop = 0
                    else:
                        domest_prop = round((domest_propKWH / domest_propKW), 1)
                    
                    if domest_baseKWH == domest_baseKW and domest_baseKW != 0:
                        domest_base = 1
                    elif domest_baseKWH == domest_baseKW and domest_baseKW == 0:
                        domest_base = 0
                    else:
                        domest_base = round((domest_baseKWH / domest_baseKW), 1)

                    # PUMPS
                    if pumps_baseKWH == pumps_baseKW and pumps_baseKW != 0:
                        pumps_base = 1
                    elif pumps_baseKWH == pumps_baseKW and pumps_baseKW == 0:
                        pumps_base = 0
                    else:
                        pumps_base = round((pumps_baseKWH / pumps_baseKW), 1)
                    
                    if pumps_propKWH == pumps_propKW and pumps_propKW != 0:
                        pumps_prop = 1
                    elif pumps_propKWH == pumps_propKW and pumps_propKW == 0:
                        pumps_prop = 0
                    else:
                        pumps_prop = round((pumps_propKWH / pumps_propKW), 1)

                    # REFRIGERATION
                    if refringe_baseKWH == refringe_baseKW and refringe_baseKW != 0:
                        refringe_base = 1
                    elif refringe_baseKWH == refringe_baseKW and refringe_baseKW == 0:
                        refringe_base = 0
                    else:
                        refringe_base = round((refringe_baseKWH / refringe_baseKWH), 1)

                    if refringe_propKWH == refringe_propKW and refringe_propKW != 0:
                        refringe_prop = 1
                    elif refringe_propKWH == refringe_propKW and refringe_propKW == 0:
                        refringe_prop = 0
                    else:
                        refringe_prop = round((refringe_propKWH / refringe_propKWH), 1)

                    # HT_PUMP
                    if ht_pump_baseKWH == ht_pump_baseKW and ht_pump_baseKW != 0:
                        ht_pump_base = 1
                    elif ht_pump_baseKWH == ht_pump_baseKW and ht_pump_baseKW == 0:
                        ht_pump_base = 0
                    else:
                        ht_pump_base = round((ht_pump_baseKWH / ht_pump_baseKW), 1)

                    if ht_pump_propKWH == ht_pump_propKW and ht_pump_propKW != 0:
                        ht_pump_prop = 1
                    elif ht_pump_propKWH == ht_pump_propKW and ht_pump_propKW == 0:
                        ht_pump_prop = 0
                    else:
                        ht_pump_prop = round((ht_pump_propKWH / ht_pump_propKW), 1)

                    # TOTAL
                    if total_baseKWH == total_baseKW and total_baseKW != 0:
                        total_base = 1
                    elif total_baseKWH == total_baseKW and total_baseKW == 0:
                        total_base = 0
                    else:
                        total_base = round((total_baseKWH / total_baseKW), 1)
                    
                    if total_propKWH == total_propKW and total_propKW != 0:
                        total_prop = 1
                    elif total_propKWH == total_propKW and total_propKW == 0:
                        total_prop = 0
                    else:
                        total_prop = round((total_propKWH / total_propKW), 1)


                    ratio1 = 0 if elfh_baseKWH == elfh_propKWH and elfh_baseKWH == 0 else round((elfh_propKWH / elfh_baseKWH), 1)
                    ratio2 = 0 if elfh_baseKW == elfh_propKW  and elfh_baseKW == 0 else round((elfh_propKW / elfh_baseKW), 1)
                    ratio3 = 0 if equip_baseKWH == equip_propKWH and equip_baseKWH == 0  else round((equip_propKWH / equip_baseKWH), 1)
                    ratio4 = 0 if equip_baseKW == equip_propKW and equip_baseKW == 0  else round((equip_propKW / equip_baseKW), 1)
                    ratio5 = 0 if fans_baseKWH == fans_propKWH and fans_baseKWH == 0  else round((fans_propKWH / fans_baseKWH), 1)
                    ratio6 = 0 if fans_baseKW == fans_propKW and fans_baseKW == 0  else round((fans_propKW / fans_baseKW), 1)
                    ratio7 = 0 if cool_baseKWH == cool_propKWH and cool_baseKWH == 0  else round((cool_propKWH / cool_baseKWH), 1)
                    ratio8 = 0 if cool_baseKW == cool_propKW and cool_baseKW == 0  else round((cool_propKW / cool_baseKW), 1)
                    ratio9 = 0 if heat_baseKWH == heat_propKWH and heat_baseKWH == 0  else round((heat_propKWH / heat_baseKWH), 1)
                    ratio10 = 0 if heat_baseKW == heat_propKW and heat_baseKW == 0  else round((heat_propKW / heat_baseKW), 1)
                    ratio11 = 0 if ext_baseKWH == ext_propKWH and ext_baseKWH == 0  else round((ext_propKWH / ext_baseKWH), 1)
                    ratio12 = 0 if ext_baseKW == ext_propKW and ext_baseKW == 0  else round((ext_propKW / ext_baseKW), 1)
                    ratio13 = 0 if domest_baseKWH == domest_propKWH and domest_baseKWH == 0  else round((domest_propKWH / domest_baseKWH), 1)
                    ratio14 = 0 if domest_baseKW == domest_propKW and domest_baseKW == 0  else round((domest_propKW / domest_baseKW), 1)
                    ratio15 = 0 if pumps_baseKWH == pumps_propKWH and pumps_baseKWH == 0  else round((pumps_propKWH / pumps_baseKWH), 1)
                    ratio16 = 0 if pumps_baseKW == pumps_propKW and pumps_baseKW == 0  else round((pumps_propKW / pumps_baseKW), 1)
                    ratio17 = 0 if refringe_baseKWH == refringe_propKWH and refringe_baseKWH == 0  else round((refringe_propKWH / refringe_baseKWH), 1)
                    ratio18 = 0 if refringe_baseKW == refringe_propKW and refringe_baseKW == 0  else round((refringe_propKW / refringe_baseKW), 1)
                    ratio19 = 0 if ht_pump_baseKWH == ht_pump_propKWH and ht_pump_baseKWH == 0  else round((ht_pump_propKWH / ht_pump_baseKWH), 1)
                    ratio20 = 0 if ht_pump_baseKW == ht_pump_propKW and ht_pump_baseKW == 0  else round((ht_pump_propKW / ht_pump_baseKW), 1)
                    ratio21 = 0 if total_baseKWH == total_propKWH and total_baseKWH == 0  else round((total_propKWH / total_baseKWH), 1)
                    ratio22 = 0 if total_baseKW == total_propKW and total_baseKW == 0  else round((total_propKW / total_baseKW), 1)

                    data_ps_f = {
                        'Item': ['Light', 'Light', 'Equipment', 'Equipment', 'Vent Fans', 'Vent Fans', 'Space Cooling', 'Space Cooling', 'Heat Reject', 'Heat Reject', 'External Usage', 'External Usage', 'Domest Hot Air', 'Domest Hot Air', 'Pumps & AUX', 'Pumps & AUX', 'Refrig Display', 'Refrig Display', 'Ht Pump Suppl', 'Ht Pump Suppl', 'Total', 'Total'],
                        'Unit': ['kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW', 'kWh', 'kW'],
                        'Baseline': [elfh_baseKWH, elfh_baseKW, equip_baseKWH, equip_baseKW, fans_baseKWH, fans_baseKW, cool_baseKWH, cool_baseKW, heat_baseKWH, heat_baseKW, ext_baseKWH, ext_baseKW, domest_baseKWH, domest_baseKW, pumps_baseKWH, pumps_baseKW, refringe_baseKWH, refringe_baseKW, ht_pump_baseKWH, ht_pump_baseKW, total_baseKWH, total_baseKW],
                        'Proposed': [elfh_propKWH, elfh_propKW, equip_propKWH, equip_propKW, fans_propKWH, fans_propKW, cool_propKWH, cool_propKW, heat_propKWH, heat_propKW, ext_propKWH, ext_propKW, domest_propKWH, domest_propKW, pumps_propKWH, pumps_propKW, refringe_propKWH, refringe_propKW, ht_pump_propKWH, ht_pump_propKW, total_propKWH, total_propKW],
                        'Savings(in %)': [(1 - ratio1), (1 - ratio2), (1 - ratio3), (1 - ratio4), (1 - ratio5), (1 - ratio6), (1 - ratio7), (1 - ratio8), (1 - ratio9), (1 - ratio10), (1 - ratio11), (1 - ratio12), (1 - ratio13), (1 - ratio14), (1 - ratio15), (1 - ratio16), (1 - ratio17), (1 - ratio18), (1 - ratio19), (1 - ratio20), (1 - ratio21), (1 - ratio22)],
                    }

                    data_elfh = {
                        'Item': ['Light', 'Equipment', 'Vent Fans', 'Space Cooling', 'Heat Reject', 'External Usage', 'Domest Hot Air', 'Pumps & AUX', 'Refrig Display', 'Ht Pump Suppl', 'Total'],
                        'Baseline(kWh/kW)': [elfh_base, equip_base, fans_base, cool_base, heat_base, ext_base, domest_base, pumps_base, refringe_base, ht_pump_base, total_base],
                        'Proposed(kWh/kW)': [elfh_prop, equip_prop, fans_prop, cool_prop, heat_prop, ext_prop, domest_prop, pumps_prop, refringe_prop, ht_pump_prop, total_prop],
                    }

                    # Create DataFrames
                    df_ps_f = pd.DataFrame(data_ps_f)
                    df_elfh = pd.DataFrame(data_elfh)

                    # Create a function to build the HTML table with merged cells
                    def create_html_table(df):
                        html = '<table border="1" style="border-collapse: collapse; width: 100%;">'
                        html += '<tr>'
                        for col in df.columns:
                            html += f'<th>{col}</th>'
                        html += '</tr>'

                        previous_item = None
                        for i, row in df.iterrows():
                            html += '<tr>'
                            if row['Item'] != previous_item:
                                rowspan = df['Item'].value_counts()[row['Item']]
                                html += f'<td rowspan="{rowspan}">{row["Item"]}</td>'
                                previous_item = row['Item']
                            html += f'<td>{row["Unit"]}</td>'
                            html += f'<td>{row["Baseline"]}</td>'
                            html += f'<td>{row["Proposed"]}</td>'
                            html += f'<td>{row["Savings(in %)"]:.1%}</td>'
                            html += '</tr>'

                        html += '</table>'
                        return html

                    # Generate the HTML table
                    df_ps_f = create_html_table(df_ps_f)
                    st.markdown(df_ps_f, unsafe_allow_html=True)

                    # Display tables with 1 decimal place using st.write
                    # st.write("**Output PS-F**")
                    # st.table(df_ps_f.style.format({
                    #     'Baseline': '{:.1f}',
                    #     'Proposed': '{:.1f}',
                    #     '% savings(1-(P/B))': '{:.1%}'
                    # }))

                    st.markdown("""<h7 style="color:green;"><b>EFLH table</b></h7>""", unsafe_allow_html=True)
                    st.table(df_elfh.style.format({
                        'Baseline(kWh/kW)': '{:.1f}',
                        'Proposed(kWh/kW)': '{:.1f}'
                    }))
                    break
    
    return 0

if __name__ == "__main__":
    # You can add code here to accept input from the command line if desired
    pass
