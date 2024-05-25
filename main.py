import streamlit as st
from INP_Parser import inp_parserv01
from Perging_INP import perge
from SIM_Parser import sim_parserv01
from SIM2PDF import sim_print
from BaselineAutomation import baselineAuto
import tempfile

def main():
    st.set_page_config(page_title="eQuest Utilities", page_icon="💡")

    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
        }
        .css-18e3th9 {
            padding-top: 0rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if 'script_choice' not in st.session_state:
        st.session_state.script_choice = "about"

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("EDSlogo.png", width=120)
    with col2:
        st.markdown("<h1 style='text-align: left;'>eQuest Utilities</h1>", unsafe_allow_html=True)

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

    if st.session_state.script_choice == "about":
        st.header("About eQuest")
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
                updated_file_path = perge.update_inp_file(uploaded_file)
                if updated_file_path:
                    st.success(f"INP Updated Successfully! Updated file saved at: {updated_file_path}")

    elif st.session_state.script_choice == "SIM Parser":
        st.header("SIM Parser")
        uploaded_file = st.file_uploader("Upload a SIM file", type="sim", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run SIM Parser"):
                sim_parserv01.main(uploaded_file)

    elif st.session_state.script_choice == "SIM to PDF":
        st.header("SIM to PDF Converter")

        reports_input = st.text_input("Enter the desired reports (comma-separated, case-sensitive):")
        reports = [r.strip() for r in reports_input.split(',')]
        input_sim_files = st.text_input("Enter the path of the directory containing SIM files:")

        if st.button("Generate PDFs"):
            sim_print.main(input_sim_files, reports)

    elif st.session_state.script_choice == "baselineAutomation":
        st.header("INP Baseline Automation")
        uploaded_inp_file = st.file_uploader("Upload an INP file", type="inp", accept_multiple_files=False)
        uploaded_sim_file = st.file_uploader("Upload a SIM file", type="sim", accept_multiple_files=False)
        input_climate = st.number_input("Enter the Climate Zone (1 to 8):", min_value=1, max_value=8, step=1)
        input_building_type = st.selectbox("Select the Building Type:", [("Residential", 0), ("Non-Residential", 1)])
        input_area = st.number_input("Enter area:", min_value=0.0, step=0.01)
        number_floor = st.number_input("Enter floor number:", min_value=1, step=1)
        heat_type = st.selectbox("Select Heating Type:", [("Hybrid/Fossil", 0), ("Electric", 1)])

        if st.button("Run Baseline Automation"):
            baselineAuto.run_baseline_automation(
                uploaded_inp_file,
                uploaded_sim_file,
                input_climate,
                input_building_type[1],
                input_area,
                number_floor,
                heat_type[1]
            )

if __name__ == "__main__":
    main()
