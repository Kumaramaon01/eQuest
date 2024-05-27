import os
import streamlit as st
import tempfile
from Perging_INP.src_perge import perging, CLM_delete

def update_inp_file(uploaded_file):
    if uploaded_file is not None:
        try:
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save the uploaded file temporarily
                inp_path = os.path.join(temp_dir, uploaded_file.name)
                st.info(f"Saving uploaded file to {inp_path}")
                
                with open(inp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Perform perging operations
                perge_data_annual = perging.perging_data_annual(inp_path)
                perge_data_weekly = perging.perging_data_weekly(perge_data_annual)
                perge_data_day = perging.perging_data_day(perge_data_weekly)
                construction_delete = CLM_delete.perging_data_const(perge_data_day)
                layers_delete = CLM_delete.perging_data_layer(construction_delete)
                material_delete = CLM_delete.perging_data_material(layers_delete)
                
                # Create the updated INP file
                base_name, ext = os.path.splitext(uploaded_file.name)
                updated_file_name = f"{base_name}_updated{ext}"
                updated_file_path = os.path.join(temp_dir, updated_file_name)

                with open(updated_file_path, 'w') as file:
                    file.writelines(material_delete)

                return inp_path, updated_file_path  # Return the paths of the original and updated INP files
        except Exception as e:
            st.error(f"An error occurred while updating INP file: {e}")

def main(uploaded_file):
    original_file_path, updated_file_path = update_inp_file(uploaded_file)
    if original_file_path and updated_file_path:
        # Provide download buttons for both the original and updated INP files
        with open(original_file_path, 'rb') as f:
            st.download_button(
                label="Download Original INP",
                data=f,
                file_name=os.path.basename(original_file_path),
                mime='text/plain'
            )
        with open(updated_file_path, 'rb') as f:
            st.download_button(
                label="Download Updated INP",
                data=f,
                file_name=os.path.basename(updated_file_path),
                mime='text/plain'
            )
        st.success(f"INP Updated Successfully! Updated file saved at: {updated_file_path}")
