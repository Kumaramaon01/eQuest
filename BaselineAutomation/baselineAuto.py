import os
import streamlit as st
import tempfile
from BaselineAutomation.src import update_MLC, insertConst, insertGlass, wwr, updateHVAC, HVAC_sys, perging, CLM_delete, update_lpd, updateFreshAir

def getInp(input_inp_path, sim_file_path, input_climate, input_building_type, input_area, number_floor, heat_type):

    if input_inp_path is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(input_inp_path.getbuffer())
            temp_file_path = temp_file.name
        inp_path = temp_file_path

    if sim_file_path is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(sim_file_path.getbuffer())
            temp_file_path = temp_file.name
        sim_path = temp_file_path

    # Convert inputs to appropriate types
    input_climate = int(input_climate)
    input_building_type = int(input_building_type)
    input_area = float(input_area)
    number_floor = int(number_floor)
    heat_type = int(heat_type)

    if input_climate < 1 or input_climate > 8 or input_building_type > 1 or input_building_type < 0:
        st.error("Error: Climate input or Building type is Wrong!\n")
        return

    # Get climate and system paths
    climate_path = update_MLC.get_climate_path(input_climate, input_building_type)
    system_path = update_MLC.get_system_path(input_building_type, heat_type, input_area, number_floor)

    # Convert paths to absolute paths
    climate_path = os.path.abspath(climate_path)
    # climate_path = "D:\EDS\Test Projects\web equest\BaselineAutomation\library\Residential_Construction\Climate zone 1.inp"

    if os.path.isfile(inp_path):
        mat_data = update_MLC.insert_material_data(climate_path, inp_path)
        st.success("Inserted Material Data")
        lyr_data = update_MLC.insert_layers_data(climate_path, mat_data)
        st.success("Inserted Layer Data")
        const_data = update_MLC.insert_const_data(climate_path, lyr_data)
        st.success("Construction Data Inserted")
        update_ConstName = insertConst.update_external_wall_roof_undergrnd(const_data)
        st.success("Construction name based on Wall, roof and underground is updated")
        updateGlass = insertGlass.update_glass(climate_path, update_ConstName)
        st.success("Inserted Glass Data")
        updateGlassType = insertGlass.update_glass_type(updateGlass)
        st.success("Glass-Type Data is Updated by All Win")
        updateWWR = wwr.UpdateWWR(sim_path, updateGlassType)
        st.success("Updated WWR")
        modifyHVAC = updateHVAC.HVAC_Modification(updateWWR)
        st.success("HVAC_Updated")
        hvac_sys = HVAC_sys.systems(modifyHVAC, system_path)
        st.success("System_updated")
        
        value = system_path.split(".inp")[0][-1]
        if value in ['1', '2', '3', '4']:
            update_zone = HVAC_sys.modify_conditioned(hvac_sys, system_path)
            st.success("Conditioned_zone updated")
        else:
            update_zone = HVAC_sys.modify_floor(hvac_sys, system_path)
            st.success("Floor updated")
        
        ###### removing unique value from data or perging ######
        perge_data_annual = perging.perging_data_annual(update_zone)
        perge_data_weekly = perging.perging_data_weekly(perge_data_annual)
        perge_data_day = perging.perging_data_day(perge_data_weekly)
        construction_delete = CLM_delete.perging_data_const(perge_data_day)
        layers_delete = CLM_delete.perging_data_layer(construction_delete)
        material_delete = CLM_delete.perging_data_material(layers_delete)
    
    ######################################################################################
        modify_lpd = update_lpd.updateLPD(material_delete, sim_path)
        st.success("LPD Updated")

        modify_freshAir = updateFreshAir.updateBCVentilation(modify_lpd, sim_path)
        st.success("FreshAir Updated!!\n")

    ######################################################################################
    ################################## CLEAN INP FILE ####################################
    ######################################################################################
         
        directory_path, filename = os.path.split(inp_path)
        new_filename = filename.replace(".inp", "_Baseline_Automation.inp")
        input_inp_ = input_inp_path.name.split('.')[0]

        # Write modified inp file 
        with open(new_filename, 'w') as file:
            file.writelines(modify_freshAir)

        # Provide download link for the zip file
        with open(new_filename, 'rb') as f:
            st.download_button(
                label="Download Updated INP",
                data=f,
                file_name=f"{os.path.basename(input_inp_)}_Baseline_Automation.inp",
            )

if __name__ == "__main__":
    # You can add code here to accept input from the command line if desired
    pass
