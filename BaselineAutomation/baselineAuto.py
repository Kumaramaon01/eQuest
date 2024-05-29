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

    # st.success(input_inp_path)
    # st.success(input_sim_path)
    
    if input_climate < 1 or input_climate > 8 or input_building_type > 1 or input_building_type < 0:
        st.success("Climate input or Building type is Wrong!\n")
    else:
        climate_path = update_MLC.get_climate_path(input_climate, input_building_type)
        system_path = update_MLC.get_system_path(input_building_type, heat_type, input_area, number_floor)
        st.success(climate_path)
        st.success(system_path)
        # climate_path = os.path.abspath(climate_path)
        # st.success(climate_path)

        if os.path.isfile(input_inp_path):
            mat_data = update_MLC.insert_material_data(climate_path, input_inp_path)
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
            updateWWR = wwr.UpdateWWR(input_sim_path, updateGlassType)
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
            modify_lpd = update_lpd.updateLPD(material_delete, input_sim_path)
            st.success("LPD Updated")

            modify_freshAir = updateFreshAir.updateBCVentilation(modify_lpd, input_sim_path)
            st.success("FreshAir Updated!!\n")

        ######################################################################################
        ################################## CLEAN INP FILE ####################################
        ######################################################################################
            
            directory_path, filename = os.path.split(input_inp_path)
            new_filename = filename.replace(".inp", "_Baseline_Automation.inp")
            output_file = os.path.join(directory_path, new_filename)

            # Write modified inp file 
            with open(output_file, 'w') as file:
                file.writelines(modify_freshAir)
            
            return output_file
            
        else:
            st.error("Not reading INP File")
            
if __name__ == "__main__":
    uploaded_file1 = st.file_uploader("Upload your INP file", type=["inp"])
    uploaded_file2 = st.file_uploader("Upload your SIM file", type=["sim"])
    main(uploaded_file1, uploaded_file2, input_climate, input_building_type, input_area, floor, heat_type)
