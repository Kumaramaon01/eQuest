import os
import pandas as pd
import streamlit as st
import tempfile
from INP_Parser.src_inp import hvac_system

def get_report_and_save(report_function, inp_path, file_suffix):
    try:
        report = report_function(inp_path)
        # Get the parent directory of the INP file
        parent_directory = os.path.dirname(inp_path)
        file_name = os.path.splitext(os.path.basename(inp_path))[0]
        file_path = os.path.join(parent_directory, f'{file_name}_{file_suffix}.csv')
        if os.path.isfile(file_path):
            os.remove(file_path)
        report.to_csv(file_path, index=False)
        return file_path
    except Exception as e:
        st.error(f"Error generating {file_suffix} report: {e}")
        return None

def main(uploaded_file):
    if uploaded_file is not None:
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                inp_path = temp_file.name
                st.info(f"Saving uploaded file to {inp_path}")
                
                temp_file.write(uploaded_file.getbuffer())
            
            # Generate reports
            sys_report_path = get_report_and_save(hvac_system.get_HVAC_System_report, inp_path, 'Sys_INP')
            zone_report_path = get_report_and_save(hvac_system.get_HVAC_Zone_report, inp_path, 'Zone_INP')
            
            if sys_report_path and zone_report_path:
                st.success("INP Parsed Successfully!!")
                
                # Provide download links for the generated reports
                with open(sys_report_path, 'rb') as f:
                    st.download_button(
                        label="Download System Report",
                        data=f,
                        file_name=os.path.basename(sys_report_path),
                        mime='text/csv'
                    )
                with open(zone_report_path, 'rb') as f:
                    st.download_button(
                        label="Download Zone Report",
                        data=f,
                        file_name=os.path.basename(zone_report_path),
                        mime='text/csv'
                    )

            # Optionally, clean up the temp file after processing
            os.remove(inp_path)
            st.info(f"Temporary file {inp_path} deleted.")
        except FileNotFoundError as fnf_error:
            st.error(f"FileNotFoundError: {fnf_error}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
