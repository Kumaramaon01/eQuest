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
    
    if os.path.isfile(sim_p_path):
        ###################################################### FRESH AIR ##################################################
        zone_space_df = aa.zoneSpace(inp_path)
        modify_dataframe = updateFreshAir.updateBCVentilation(zone_space_df, inp_path, sim_path)
        modify_freshAi = freshAir.updateFresh(modify_dataframe, inp_path)
        modify_freshAir = freshAir.remove_OAs(modify_freshAi)
        
        ######################################################## MLC INSERTION #############################################
        mat_data = update_MLC.insert_material_data(climate_path, modify_freshAir)
        st.success("Inserted Material Data")
        lyr_data = update_MLC.insert_layers_data(climate_path, mat_data)
        st.success("Inserted Layer Data")
        const_data = update_MLC.insert_const_data(climate_path, lyr_data)
        st.success("Construction Data Inserted")
        
        ######################################################## W,R,U Updated ##############################################
        update_ConstName = insertConst.update_external_wall_roof_undergrnd(const_data)
        st.success("In MLC:- Construction name based on Wall, roof and underground is updated")

        ######################################################## GLASS INSERTION #############################################
        updateGlass = insertGlass.update_glass(climate_path, update_ConstName)
        st.success("Inserted Glass Data")
        updateGlassType = insertGlass.update_glass_type(climate_path, updateGlass)
        st.success("Glass-Type Data is Updated by All Win")

        ######################################################## WWR #########################################################
        updateWWR = wwr.UpdateWWR(sim_path, updateGlassType)
        st.success("Updated WWR if ratio > 0.4")

        # ######################################################## HVAC #########################################################
        modifyHVAC = updateHVAC.HVAC_Modification(updateWWR)
        st.success("HVAC_Updated (All System Deleted)")
        hvac_sys = HVAC_sys.systems(modifyHVAC, system_path)
        st.success("Data Replaces HVAC")
        value = system_path.split(".inp")[0][-1]
        if value in ['1', '2', '3', '4']:
            update_zone = HVAC_sys.modify_conditioned(hvac_sys, system_path)
            st.success("Conditioned_zone updated")
        else:
            update_zone = HVAC_sys.modify_floor(hvac_sys, system_path)
            st.success("Floor updated")
    
        ######################################################### LPD #########################################################
        modify_lpd = update_lpd.updateLPD(update_zone, sim_path)
        st.success("LPD Updated")
        st.success("FreshAir Updated!!")

        # ######################################################### FRESH AIR ###################################################
        # zone_space_df = aa.zoneSpace(input_inp_path)
        # modify_dataframe = updateFreshAir.updateBCVentilation(zone_space_df, modify_lpd, input_sim_path)
        # modify_freshAir = freshAir.updateFresh(modify_dataframe, modify_lpd)

        # ######################################################### FRESH AIR ###################################################
        # modify_freshAir = updateFreshAir.updateBCVentilation(modify_lpd, sim_path)
        # st.success("FreshAir Updated!!\n")

        ###################################################### PURGING #######################################################
        ##### Removing unique value from data or purging ######
        perge_data_annual = perging.perging_data_annual(modify_lpd)
        perge_data_weekly = perging.perging_data_weekly(perge_data_annual)
        perge_data_day = perging.perging_data_day(perge_data_weekly)
        construction_delete = CLM_delete.perging_data_const(perge_data_day)
        layers_delete = CLM_delete.perging_data_layer(construction_delete)
        material_delete = CLM_delete.perging_data_material(layers_delete)
         
        directory_path, filename = os.path.split(inp_path)
        new_filename = re.sub(r'\.inp?$', '_Baseline_Automation.inp', filename, flags=re.IGNORECASE)
        input_inp_ = input_inp_path.name.split('.')[0]
        
        # Write modified inp file 
        with open(new_filename, 'w', newline = '\r\n') as file:
            file.writelines(material_delete)

        with open(new_filename, 'rb') as f:
            st.download_button(
                label="Download Updated INP",
                data=f,
                file_name=f"{os.path.basename(input_inp_)}_Baseline_Automation.inp",
            )

if __name__ == "__main__":
    # You can add code here to accept input from the command line if desired
    pass
