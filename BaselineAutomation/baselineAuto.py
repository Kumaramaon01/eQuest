import os
import streamlit as st
from BaselineAutomation.src import update_MLC, insertConst, insertGlass, wwr, updateHVAC, HVAC_sys, perging, CLM_delete, update_lpd, updateFreshAir

def main(input_inp_path, input_sim_path, input_climate, input_building_type, input_area, number_floor, heat_type):
    # Convert input_climate to an integer
    input_climate = int(input_climate)
    input_building_type = int(input_building_type)
    input_area = float(input_area)
    floor = int(number_floor)
    heat_type = int(heat_type)
    
    if input_climate < 1 or input_climate > 8 or input_building_type > 1 or input_building_type < 0:
        st.error("Invalid input for climate or building type.")
        return
    
    climate_path = update_MLC.get_climate_path(input_climate, input_building_type)
    system_path = update_MLC.get_system_path(input_building_type, heat_type, input_area, number_floor)
        
    if os.path.isfile(input_inp_path):
        mat_data = update_MLC.insert_material_data(climate_path, input_inp_path)
        lyr_data = update_MLC.insert_layers_data(climate_path, mat_data)
        const_data = update_MLC.insert_const_data(climate_path, lyr_data)
        update_ConstName = insertConst.update_external_wall_roof_undergrnd(const_data)
        updateGlass = insertGlass.update_glass(climate_path, update_ConstName)
        updateGlassType = insertGlass.update_glass_type(updateGlass)
        updateWWR = wwr.UpdateWWR(input_sim_path, updateGlassType)
        modifyHVAC = updateHVAC.HVAC_Modification(updateWWR)
        hvac_sys = HVAC_sys.systems(modifyHVAC, system_path)
        
        value = system_path.split(".inp")[0][-1]
        if value in ['1', '2', '3', '4']:
            update_zone = HVAC_sys.modify_conditioned(hvac_sys, system_path)
        else:
            update_zone = HVAC_sys.modify_floor(hvac_sys, system_path)
            
        perge_data_annual = perging.perging_data_annual(update_zone)
        perge_data_weekly = perging.perging_data_weekly(perge_data_annual)
        perge_data_day = perging.perging_data_day(perge_data_weekly)
        construction_delete = CLM_delete.perging_data_const(perge_data_day)
        layers_delete = CLM_delete.perging_data_layer(construction_delete)
        material_delete = CLM_delete.perging_data_material(layers_delete)
        modify_lpd = update_lpd.updateLPD(material_delete, input_sim_path)
        modify_freshAir = updateFreshAir.updateBCVentilation(modify_lpd, input_sim_path)
            
        directory_path, filename = os.path.split(input_inp_path)
        new_filename = filename.replace(".inp", "_Baseline_Automation.inp")
        output_file = os.path.join(directory_path, new_filename)

        # Write modified inp file 
        with open(output_file, 'w') as file:
            file.writelines(modify_freshAir)

        st.success("INP file successfully updated.")

        # Add a download button
        st.download_button(
            label="Download Updated INP File",
            data=open(output_file, 'rb'),
            file_name=new_filename,
            mime="text/plain"
        )
        
    else:
        st.error("Error: Input INP file not found.")

if __name__ == "__main__":
    uploaded_file1 = st.file_uploader("Upload your INP file", type=["inp"])
    uploaded_file2 = st.file_uploader("Upload your SIM file", type=["sim"])
    input_climate = st.number_input("Enter the Climate Zone (1 to 8):", min_value=1, max_value=8, step=1)
    input_building_type = st.number_input("Select the Building Type, (Residential - 0), (Non-Residential - 1):", min_value=0, max_value=1, step=1)
    input_area = st.number_input("Enter area:", min_value=0.0, step=0.01)
    number_floor = st.number_input("Enter floor number:", min_value=1, step=1)
    heat_type = st.number_input("Select Heating Type, (Hybrid/Fossil - 0), (Electric - 1):", min_value=0, max_value=1, step=1)

    if st.button("Run Baseline Automation"):
        main(uploaded_file1, uploaded_file2, input_climate, input_building_type, input_area, number_floor, heat_type)
