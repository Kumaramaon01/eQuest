import os
import streamlit as st
from Perging_INP.src_perge import perging, CLM_delete

def update_inp_file(uploaded_file):
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        inp_path = os.path.join(os.path.expanduser("~"), "Downloads", uploaded_file.name)
        with open(inp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
        perge_data_annual = perging.perging_data_annual(inp_path)
        perge_data_weekly = perging.perging_data_weekly(perge_data_annual)
        perge_data_day = perging.perging_data_day(perge_data_weekly)
        construction_delete = CLM_delete.perging_data_const(perge_data_day)
        layers_delete = CLM_delete.perging_data_layer(construction_delete)
        material_delete = CLM_delete.perging_data_material(layers_delete)
        
        # Create the updated INP file path
        base_name, ext = os.path.splitext(uploaded_file.name)
        updated_file_name = f"{base_name}_updated{ext}"
        updated_file_path = os.path.join(os.path.expanduser("~"), "Downloads", updated_file_name)

        with open(updated_file_path, 'w') as file:
            file.writelines(material_delete)
        
        return updated_file_path  # Return the path of the updated INP file
    else:
        st.error("Invalid INP file path.")

def main(uploaded_file):
    updated_file_path = update_inp_file(uploaded_file)
    if updated_file_path:
        st.success(f"INP Updated Successfully! Updated file saved at: {updated_file_path}")