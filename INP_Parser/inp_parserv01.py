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
                
                with open(inp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.write(f"File saved temporarily at {inp_path}")

                # Perform perging operations
                perge_data_annual = perging.perging_data_annual(inp_path)
                if not perge_data_annual:
                    st.error("Failed during perging_data_annual")
                    return None

                perge_data_weekly = perging.perging_data_weekly(perge_data_annual)
                if not perge_data_weekly:
                    st.error("Failed during perging_data_weekly")
                    return None

                perge_data_day = perging.perging_data_day(perge_data_weekly)
                if not perge_data_day:
                    st.error("Failed during perging_data_day")
                    return None

                construction_delete = CLM_delete.perging_data_const(perge_data_day)
                if not construction_delete:
                    st.error("Failed during perging_data_const")
                    return None

                layers_delete = CLM_delete.perging_data_layer(construction_delete)
                if not layers_delete:
                    st.error("Failed during perging_data_layer")
                    return None

                material_delete = CLM_delete.perging_data_material(layers_delete)
                if not material_delete:
                    st.error("Failed during perging_data_material")
                    return None
                
                # Create the updated INP file
                base_name, ext = os.path.splitext(uploaded_file.name)
                updated_file_name = f"{base_name}_updated{ext}"
                updated_file_path = os.path.join(temp_dir, updated_file_name)

                with open(updated_file_path, 'w') as file:
                    file.writelines(material_delete)
                st.write(f"Updated file created at {updated_file_path}")

                if os.path.exists(updated_file_path):
                    st.write(f"Verified: Updated file exists at {updated_file_path}")
                else:
                    st.error(f"Updated file does not exist at {updated_file_path}")
                    return None

                return updated_file_path  # Return the path of the updated INP file
        except Exception as e:
            st.error(f"An error occurred while updating INP file: {e}")
            st.write(f"Error details: {e}")
            return None

def main(uploaded_file):
    updated_file_path = update_inp_file(uploaded_file)
    if updated_file_path and os.path.exists(updated_file_path):
        try:
            # Move the updated INP file to the Downloads directory
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            updated_file_name = os.path.basename(updated_file_path)
            new_file_path = os.path.join(downloads_path, updated_file_name)
            os.rename(updated_file_path, new_file_path)
            st.write(f"Updated file moved to {new_file_path}")

            # Display success message
            st.success("INP Updated Successfully!")

            # Provide download link for the updated INP file
            with open(new_file_path, 'rb') as f:
                st.download_button(
                    label="Download Updated INP",
                    data=f,
                    file_name=updated_file_name,
                    mime='text/plain'
                )
        except Exception as e:
            st.error(f"An error occurred while moving the updated INP file: {e}")
            st.write(f"Error details: {e}")
    else:
        st.error("The updated INP file was not created successfully.")

if __name__ == "__main__":
    uploaded_file = st.file_uploader("Upload your INP file", type=["inp"])
    if uploaded_file is not None:
        main(uploaded_file)
