import streamlit as st
import tempfile
from INP_Parser import inp_parserv01
from Perging_INP import perge  # Import the perge function directly
from SIM_Parser import sim_parserv01
from SIM2PDF import sim_print
from BaselineAutomation import baselineAuto  # Import the baseline automation script

def main():
    st.set_page_config(page_title="eQuest Utilities", page_icon="💡")

    # Add custom CSS to set the background color and hide Streamlit branding elements
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;  /* Set your desired background color here */
        }
        .css-18e3th9 {
            padding-top: 0rem;  /* Adjust the padding at the top */
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .viewerBadge_container__1QSob {visibility: hidden;}
        .stActionButton {margin: 5px;} /* Optional: Adjust button spacing */
        header .stApp [title="View source on GitHub"] {
            display: none;
        }
        .stApp header, .stApp footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state for script_choice if it does not exist
    if 'script_choice' not in st.session_state:
        st.session_state.script_choice = "about"  # Set default to "about"

    # Header section with logo and title
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("EDSlogo.png", width=120)  # Replace with the path to your logo file
    with col2:
        st.markdown("<h1 style='text-align: left;'>eQuest Utilities</h1>", unsafe_allow_html=True)

    # Navigation bar with buttons below the header
    st.markdown("---")
    col3, col4, col5, col6 = st.columns([1, 1, 1, 1])
    with col3:
        if st.button("About eQuest"):
            st.session_state.script_choice = "about"
    with col4:
        if st.button("INP Parser"):
            st.session_state.script_choice = "INP Parser"
    with col5:
        if st.button("Purging INP"):
            st.session_state.script_choice = "Purging INP"
    with col6:
        if st.button("SIM Parser"):
            st.session_state.script_choice = "SIM Parser"
    
    col7, col8 = st.columns([1, 1])
    with col7:
        if st.button("SIM to PDF"):
            st.session_state.script_choice = "SIM to PDF"
    with col8:
        if st.button("Baseline Automation"):
            st.session_state.script_choice = "baselineAutomation"

    # Based on the user selection, display appropriate input fields and run the script
    if st.session_state.script_choice == "about":
        st.markdown("""
        ### Welcome to eQuest Utilities

        eQuest Utilities is a comprehensive suite of tools designed to help you work with eQuest more efficiently. 
        Our utilities include:

        - **INP Parser:** A tool to parse INP files and extract meaningful data.
        - **Purging INP:** A utility to update and clean your INP files.
        - **SIM Parser:** A parser for SIM files to streamline your simulation data processing.
        - **SIM to PDF Converter:** Easily convert your SIM files into PDF format for better sharing and documentation.

        Navigate through the tools using the buttons above to get started. Each tool is designed to simplify 
        specific tasks related to eQuest project management. We hope these utilities make your workflow smoother 
        and more productive.
        """)

    elif st.session_state.script_choice == "INP Parser":
        st.header("INP Parser")
        uploaded_file = st.file_uploader("Upload an INP file", type="inp", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run INP Parser"):
                inp_parserv01.main(uploaded_file)

    elif st.session_state.script_choice == "Purging INP":
        st.header("Purging INP")
        uploaded_file = st.file_uploader("Upload an INP file", type="inp", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run INP Purging"):
                perge.main(uploaded_file)

    elif st.session_state.script_choice == "SIM Parser":
        st.header("SIM Parser")
        uploaded_file = st.file_uploader("Upload a SIM file", type="sim", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run SIM Parser"):
                sim_parserv01.main(uploaded_file)

    elif st.session_state.script_choice == "SIM to PDF":
        st.header("SIM to PDF Converter")
        st.write('This application is currently under maintenance. Please try again later.')
        # reports_input = st.text_input("Enter the desired reports (comma-separated, case-sensitive):")
        # reports = [r.strip() for r in reports_input.split(',')]
        # input_sim_files = st.text_input("Enter the path of the directory containing SIM files:")
    
        # if st.button("Generate PDFs"):
            # st.success(input_sim_files)
            # sim_print.main(input_sim_files, reports)

    elif st.session_state.script_choice == "baselineAutomation":
        st.header("INP Baseline Automation")
        uploaded_inp_file = st.file_uploader("Upload a INP file", type="inp", accept_multiple_files=False)
        uploaded_sim_file = st.file_uploader("Upload a SIM file", type="sim", accept_multiple_files=False)
        input_climate = st.number_input("Enter the Climate Zone (1 to 8):", min_value=1, max_value=8, step=1)
        input_building_type = st.number_input("Select the Building Type, (Residential - 0), (Non-Residential - 1):", min_value=0, max_value=1, step=1)
        input_area = st.number_input("Enter area:", min_value=0.0, step=0.01)
        number_floor = st.number_input("Enter floor number:", min_value=1, step=1)
        heat_type = st.number_input("Select Heating Type, (Hybrid/Fossil - 0), (Electric - 1):", min_value=0, max_value=1, step=1)

        if st.button("Run Baseline Automation"):
            if uploaded_inp_file is not None and uploaded_sim_file is not None:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".inp") as inp_temp_file, \
                     tempfile.NamedTemporaryFile(delete=False, suffix=".sim") as sim_temp_file, \
                     tempfile.NamedTemporaryFile(delete=False, suffix=".inp") as output_temp_file:
                    
                    # Write the uploaded files to the temporary files
                    inp_temp_file.write(uploaded_inp_file.read())
                    sim_temp_file.write(uploaded_sim_file.read())
                    
                    inp_temp_file_path = inp_temp_file.name
                    sim_temp_file_path = sim_temp_file.name
                    output_temp_file_path = output_temp_file.name
                    
                    # Run baseline automation
                    baselineAuto.main(inp_temp_file_path, sim_temp_file_path, input_climate, input_building_type, input_area, number_floor, heat_type, output_temp_file_path)
                    st.success("Baseline automation run successfully.")

                    # Provide a download link for the output file
                    with open(output_temp_file_path, "rb") as file:
                        st.download_button(
                            label="Download updated INP file",
                            data=file,
                            file_name="updated_baseline.inp"
                        )
            else:
                st.error("Please upload both INP and SIM files.")

if __name__ == "__main__":
    main()
