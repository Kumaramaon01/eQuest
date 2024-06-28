import streamlit as st
import subprocess
import os
import pandas as pd
from INP_Parser import inp_parserv01
from Perging_INP import perge
from SIM_Parser import sim_parserv01
from SIM2PDF import sim_print
from BaselineAutomation import baselineAuto
from ScheduleGenerator import schedule_v01
from streamlit_card import card
from PIL import Image as PILImage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Email credentials and recipient
TO_EMAIL = "rajeev@edsglobal.com"
# Set the page configuration with additional options layout='wide',
st.set_page_config(page_title="eQuest Utilities", page_icon="💡", layout='wide',
    menu_items={                          # Custom menu items
        'Get Help': 'https://www.example.com/help',
        'Report a bug': 'https://www.example.com/bug',
        'About': '# This is an **eQuest Utilities** application!'
    }
)

# Function to set the background image using CSS
def set_dark_theme():
    """
    Function to set a dark theme using CSS.
    """
    # Define the HTML code with CSS for a dark theme
    html_code = """
    <style>
    .stApp {
        background-color: black;  /* Set background color to black */
        color: white;  /* Set text color to white */
    }
    .stMarkdown, .stImage, .stDataFrame, .stTable {
        background-color: transparent !important; /* Make elements' background transparent */
        color: white !important;  /* Ensure text color within these elements is white */
    }
    </style>
    """
    # Inject the HTML code in the Streamlit app
    st.markdown(html_code, unsafe_allow_html=True)

# Function to send email
def send_email(subject, message, from_email, to_email):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        # print(f"Failed to send email: {e}")
        st.success("Email sent successfully!")
        return False

button_style = """
    <style>
        .stButton>button {
            box-shadow: 1px 1px 1px rgba(0, 0, 0, 0.8);
        }
    </style>
"""

# Render the button with the defined style
st.markdown(button_style, unsafe_allow_html=True)

# Define CSS style with text-shadow effect for the heading
heading_style = """
    <style>
    .heading-with-shadow {
        text-align: left;
        color: red;
        text-shadow: 0px 8px 4px rgba(255, 255, 255, 0.4);
        background-color: white;
    }
</style>
"""

# Render the heading with the defined style
st.markdown(heading_style, unsafe_allow_html=True)

# Define button carousel items
carousel_items = ["About EDS", "About eQuest", "INP Parser", "Purging INP", "SIM Parser", "SIM to PDF", "Baseline Automation", "EXE Files", "Queries", "Visual"]

def main(): 
    # Add custom CSS to set the background color and hide Streamlit branding elements
    card_button_style = """
        <style>
        .card-button {
            width: 100%;
            padding: 20px;
            background-color: white;
            border: none;
            border-radius: 10px;
            box-shadow: 0 2px 2px rgba(0,0,0,0.2);
            transition: box-shadow 0.3s ease;
            text-align: center;
            font-size: 16px;
            cursor: pointer;
        }
        .card-button:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }
        </style>
    """
    
    st.markdown(
        """
        <style>
        body {
            background-color: #bfe1ff;  /* Set your desired background color here */
            animation: changeColor 5s infinite;
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
        
    # URL and image path
    logo_url = "https://equest-utilities-edsglobal.streamlit.app/"
    logo_image_path = "images/eQcb_142.gif"

    # Header section with logo and title
    col1, col2, col3 = st.columns([1, 1, 0.5])
    with col1:
        # Display the image
        st.image(logo_image_path, width=80)
    with col2:
        st.markdown("<h1 class='heading-with-shadow'>eQuest Utilities</h1>", unsafe_allow_html=True)
        
    on = st.toggle("Select Theme")
    if on:
        # set_dark_theme()  # Call your function to set the dark theme
        pass  # Do nothing
        # Set your background image URL
        background_image_url = "https://i.pinimg.com/originals/cf/04/e9/cf04e9530f25312133dc7f93586591ff.gif"
        # Call the function to set the background
        # set_background(background_image_url)
    
    icon_with_tooltip1 = """
    <div style="text-align:center">
        <span style="font-size:34px">
            <a href="https://mail.google.com/mail/u/0/#inbox" title="Click to check your inbox" onmouseover="if (confirm('Do you want to ask a question?'))">
                <span>&#x1F4E7;</span>
            </a>
        </span>
    </div>
    """

    icon_with_tooltip2 = """
    <div style="text-align:center">
        <span style="font-size:44px">
            <a href="https://wa.me/917091895623" title="Chat on WhatsApp" onmouseover="if (confirm('Do you want to ask a question?'))">
                <span>&#x1F4F1;</span>
            </a>
        </span>
    </div>
    """

    # Add icon and tooltip to col3
    with col3:
        # st.write(icon_with_tooltip1, unsafe_allow_html=True)
        st.image("images/EDSlogo.jpg", width=120)

    # Navigation bar with buttons below the header
    #st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)
    st.markdown(
        """
        <svg height="100" width="100%">
          <!-- Bold gold-colored horizontal line -->
          <line x1="0" y1="50" x2="95%" y2="50" style="stroke:goldenrod;stroke-width:3" />
        
          <!-- Earring-like golden ring -->
          <circle cx="95%" cy="50" r="15" stroke="goldenrod" stroke-width="1" fill="gold" />
        
          <!-- Pendulum-like motion effect -->
          <animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0" to="0" begin="5s" dur="60s" repeatCount="indefinite"/>
        </svg>
        """,
        unsafe_allow_html=True
    )

    col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns([0.9, 1, 0.9, 0.9, 0.9, 0.9, 1.3, 0.7, 1.2, 0.7])
    with col2:
        if st.button("About EDS", key="buttons"):
            st.session_state.script_choice = "eds"
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
    with col7:
        if st.button("SIM to PDF"):
            st.session_state.script_choice = "SIM to PDF"
    with col8:
        if st.button("Baseline Automation"):
            st.session_state.script_choice = "baselineAutomation"
    with col9:
        if st.button("EXE Files"):#EXE Files
            st.session_state.script_choice = "exe"
    with col10:
        if st.button("Schedule Generator"): #Schedule Generator
            st.session_state.script_choice = "sh"
    with col11:
        if st.button("Queries"): #Queries
            st.session_state.script_choice = "ask"

    # Based on the user selection, display appropriate input fields and run the script
    if st.session_state.script_choice == "about":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <h3 style="color:red;">Welcome to eQuest Utilities</h3>
    
            eQuest Utilities is a comprehensive suite of tools designed to help you work with eQuest more efficiently. 
            Our utilities include:
    
            - <b style="color:red;">INP Parser:</b> A tool to parse INP files and extract meaningful data.
            - <b style="color:red;">Purging INP:</b> A utility to update and clean your INP files.
            - <b style="color:red;">SIM Parser:</b> A parser for SIM files to streamline your simulation data processing.
            - <b style="color:red;">SIM to PDF Converter:</b> Easily convert your SIM files into PDF format for better sharing and documentation.
            - <b style="color:red;">Baseline Automation:</b> Modifies INP files based on the user input.
    
            Navigate through the tools using the buttons above to get started. Each tool is designed to simplify 
            specific tasks related to eQuest project management. We hope these utilities make your workflow smoother 
            and more productive.
            """, unsafe_allow_html=True)
        with col2:
            st.image("https://www.filepicker.io/api/file/ISb3e710QSmh95AYIdef", width=560)
        
    elif st.session_state.script_choice == "eds":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <h3 style="color:red;">Overview</h3>
    
            Environmental Design Solutions [EDS] is a sustainability advisory firm focusing on the built environment. Since its inception in 2002,
            EDS has worked on over 800 green building and energy efficiency projects worldwide. The diverse milieu of its team of experts converges on
            climate change mitigation policies, energy efficient building design, building code development, energy efficiency policy development, energy
            simulation and green building certification.<br>
    
            EDS has extensive experience in providing sustainable solutions at both, the macro level of policy advisory and planning, as well as a micro
            level of developing standards and labeling for products and appliances. The scope of EDS projects range from international and national level
            policy and code formulation to building-level integration of energy-efficiency parameters. EDS team has worked on developing the Energy Conservation
            Building Code [ECBC] in India and supporting several other international building energy code development, training, impact assessment, and 
            implementation. EDS has the experience of data collection & analysis, benchmarking, energy savings analysis, GHG impact assessment, and developing
            large scale implementation programs.<br>
    
            EDS’ work supports the global endeavour towards a sustainable environment primarily through the following broad categories:
            - Sustainable Solutions for the Built Environment
            - Strategy Consulting for Policy & Codes, and Research
            - Outreach, Communication, Documentation, and Training
    
            """, unsafe_allow_html=True)
            st.link_button("Know More", "https://edsglobal.com", type="primary")
        with col2:
            st.image("https://images.jdmagicbox.com/comp/delhi/k8/011pxx11.xx11.180809193209.h6k8/catalogue/environmental-design-solutions-vasant-vihar-delhi-environmental-management-consultants-leuub0bjnn.jpg", width=590)
        
    elif st.session_state.script_choice == "sh":
        st.markdown("""
        <h3 style="color:red;">Schedule Generator</h3>
        <b>Purpose:</b> Our CSV-Based Schedule Generator Tool is designed to simplify and automate the process of creating schedules. By leveraging data from a CSV file, this tool efficiently generates a structured and optimized schedule tailored to your specific needs.<br>
        <br>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload CSV or EXCEL file", type=["csv", "xlsx"], accept_multiple_files=False)
    
        if uploaded_file is not None:
            if st.button("Generate INP"):
                schedule_v01.getCSV(uploaded_file)

    elif st.session_state.script_choice == "INP Parser":
        st.markdown("""
        <h3 style="color:red;">INP Parser</h3>
        <b>Purpose:</b> The INP Parser is designed to read and interpret INP files, which are the primary project files used by eQuest. These files contain all the necessary data about a building's energy model, including geometry, materials, systems, and schedules.<br>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload an INP file", type="inp", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run INP Parser"):
                inp_parserv01.main(uploaded_file)

    elif st.session_state.script_choice == "Purging INP":
        st.markdown("""
        <h3 style="color:red;">Purging INP</h3>
        <b>Purpose:</b> The Purging INP tool helps clean and update your INP files to ensure they are optimized and free of unnecessary data.
        - Removes redundant or obsolete data entries.
        - Updates outdated references to newer standards or templates.
        - Improves the overall performance and manageability of the INP file.<br>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload an INP file", type="inp", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run INP Purging"):
                perge.main(uploaded_file)

    elif st.session_state.script_choice == "SIM Parser":
        st.markdown("""
        <h3 style="color:red;">SIM Parser</h3>
        <b>Purpose:</b> The SIM Parser is used to process SIM files generated by eQuest simulations. SIM files contain detailed results of energy simulations, including energy consumption, system performance, and cost estimates.<br>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a SIM file", type="sim", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run SIM Parser"):
                sim_parserv01.main(uploaded_file)

    elif st.session_state.script_choice == "SIM to PDF":
        st.markdown("""
        <h3 style="color:red;">SIM to PDF Converter</h3>
        <b>Purpose:</b> This tool converts SIM files into PDF format, making it easier to share and document simulation results.
        """, unsafe_allow_html=True)
        
        st.markdown("""Enter Reports in following format (comma-seperated and case-sensitive). And, It can accept multiple sim files.""", unsafe_allow_html=True)
        
        # Allow multiple .sim files to be uploaded
        uploaded_files = st.file_uploader("Upload SIM files", type="sim", accept_multiple_files=True)
        # Provide options for report selection
        reports_input = st.multiselect(
            "Enter Reports",
            ["LV-B", "LV-D", "LV-M", "LV-A", "LV-C", "LV-E", "LV-F", "LV-G", "LV-H", "LV-I", "LV-J", 
             "LS-A", "LS-B", "LS-D", "LS-L", "LV-N", "LS-C", "LS-E", "LS-F", "LS-K", "PV-A", "BEPS", 
             "BEPU", "SV-A", "PV-A", "PS-E", "SS-A", "SS-B", "SS-C", "SS-D", "SS-E", "SS-M"],
            ["LV-B"]
        )
        
        # Check if files and reports are selected
        if uploaded_files and reports_input:
            if st.button("Convert to PDF"):
                # Clean up each report name
                reports = [r.strip() for r in reports_input]
                
                # Display success messages
                st.success(f"Selected reports: {reports}")
                st.success(f"Uploaded files: {[file.name for file in uploaded_files]}")
                
                # Process each uploaded file
                for uploaded_file in uploaded_files:
                    # Call the main function with reports and each file
                    sim_print.main(reports, uploaded_file)
        # else:
        #     st.warning("Please upload SIM files and select reports.")
                
    elif st.session_state.script_choice == "ask":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(icon_with_tooltip1, unsafe_allow_html=True)
            email = st.text_input("Enter your mail:")
            user_input = st.text_area("Enter your Queries:")
        with col2:
            st.image("https://images.jdmagicbox.com/comp/delhi/k8/011pxx11.xx11.180809193209.h6k8/catalogue/environmental-design-solutions-vasant-vihar-delhi-environmental-management-consultants-leuub0bjnn.jpg", width=290)
        with col3:
            st.image("data:image/jpeg;base64,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", width=380)
    
        # Submit button
        if st.button("Submit"):
            if user_input and email:
                subject = "Text Area Submission"
                message = user_input
                EMAIL = email
                if send_email(subject, message, EMAIL, TO_EMAIL):
                    st.success("Email sent successfully!")
            else:
                st.warning("Please enter your Queries.")

    elif st.session_state.script_choice == "exe":
        st.markdown("""
        <h3 style="color:red;">EXE Files</h3>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            # st.markdown("<h2>INP Parser</h2>", unsafe_allow_html=True)
            # st.write("Parsing INP files")
            st.image("images/INP_Parser_logo.png", width = 110)
            st.write("[Download](https://drive.google.com/file/d/1_jgaEfJCuoqfZOq3hY33D-3x31-v-nTH/view?usp=drive_link)")
        with col2:
            # st.markdown("<h2>SIM Parser</h2>", unsafe_allow_html=True)
            # st.write("Parsing SIM files")
            st.image("images/SIM_Parser_logo.png", width = 110)
            st.write("[Download](https://drive.google.com/file/d/1jhIyXWMRo7z0J6n32R6omVNpM3Xd8beY/view?usp=drive_link)")
        with col3:
            # st.markdown("<h2>EXE 3</h2>", unsafe_allow_html=True)
            # st.write("Purging INP")
            st.image("images/purging_inp_logo.png", width = 110)
            st.write("[Download](https://drive.google.com/file/d/1oIQmgVAMy871cwwQPnlm3FAAlEB_Bl7o/view?usp=drive_link)")
        with col4:
            # st.markdown("<h2>EXE 3</h2>", unsafe_allow_html=True)
            # st.write("Purging INP")
            st.image("images/SIM_pdf.png", width=110)  # Replace with the path to your logo file
            st.write("[Download](https://drive.google.com/file/d/10jga6aMVQHgEIG1rhMaqs_sXTt3yEJXK/view?usp=drive_link)")
        with col5:
            st.image("images/baseline.png", width = 110)
            # st.write("[Download](url_to_exe_1)")
            
        st.markdown("""
            <h5 style="color:black;">Documents to read</h5>
            <ul>
                <li><b style="color:red;">SIM to PDF:</b> <a href="https://docs.google.com/presentation/d/1WTdX3zmSMmyp0h1E5lfOsER8EkvFoOEj/edit?usp=drive_link&ouid=104083687366839123092&rtpof=true&sd=true" target="_blank">Data Extraction Tool: SIM to PDF</a></li>
                <li><b style="color:red;">INP Parser:</b> <a href="https://docs.google.com/presentation/d/1zJ24RgUWW772xFIiWD5GruVEVQrrcdtT/edit?usp=drive_link&ouid=104083687366839123092&rtpof=true&sd=true" target="_blank">INP Data to CSVs based on Reports</a></li>
                <li><b style="color:red;">SIM Parser:</b> <a href="https://docs.google.com/presentation/d/11fyPNx9e3g-xC11kEMJhGvmCQXvyBlsQ/edit?usp=drive_link&ouid=104083687366839123092&rtpof=true&sd=true" target="_blank">SIM Data to CSVs based on Reports</a></li>
                <li><b style="color:red;">User Manual:</b> <a href="https://docs.google.com/presentation/d/1W8zTyj1kD-dRlk7XHinJ3_piOnaADx0w/edit?usp=drive_link&ouid=104083687366839123092&rtpof=true&sd=true" target="_blank">User Manual</a></li>
            </ul>
            """, unsafe_allow_html=True)
        
        # Add more cards as needed
        st.markdown("""
        #### Note:
        Due to the large size of eQuest Utilities exe files, they may not be suitable for direct hosting on our website. 
        However, they are available for download.
        """)

    elif st.session_state.script_choice == "baselineAutomation":
        st.markdown("""
        <h3 style="color:red;">Baseline Automation</h3>
        """, unsafe_allow_html=True)
        st.markdown("""
        <b>Purpose:</b> The Baseline Automation tool assists in modifying INP files based on user-defined criteria to create baseline models for comparison.
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            uploaded_inp_file = st.file_uploader("Upload an INP file", type="inp", accept_multiple_files=False)
        with col2:
            uploaded_sim_file = st.file_uploader("Upload a SIM file", type="sim", accept_multiple_files=False)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            input_climate = st.selectbox("Climate Zone", options=[1, 2, 3, 4, 5, 6, 7, 8])
        with col2:
            input_building_type = st.selectbox("Building Type", options=[0, 1], format_func=lambda x: "Residential" if x == 0 else "Non-Residential")
        with col3:
            input_area = st.number_input("Enter Area (Sqft)", min_value=0.0, step=0.1)
        with col4:
            number_floor = st.number_input("Number of Floors", min_value=1, step=1)
        with col5:
            heat_type = st.selectbox("Heating Type", options=[0, 1], format_func=lambda x: "Hybrid/Fossil" if x == 0 else "Electric")

        if uploaded_inp_file and uploaded_sim_file:
            if st.button("Run Baseline Automation"):
                baselineAuto.getInp(
                    uploaded_inp_file,
                    uploaded_sim_file,
                    input_climate,
                    input_building_type,
                    input_area,
                    number_floor,
                    heat_type)
                
if __name__ == "__main__":
    main()
    
# Navigation bar with buttons below the header
st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)
 # Adding the Font Awesome CSS
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    .social-media {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .social-media a {
        margin: 0 10px;
        text-decoration: none;
        color: blue;
    }
    .social-media i {
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# Designed and Developed by section
st.markdown(
    """
    <div class="social-media" style="margin-top: 10px;">
        <p>Designed and Developed by <a href="https://edsglobal.com" target="_blank"><b style="text-color: red;"><u>Environmental Design Solutions, Pvt. Ltd</u>
        </b></a></p>
        <a href="https://twitter.com/edsglobal?lang=en" target="_blank"><i class="fab fa-twitter"></i></a>
        <a href="https://www.facebook.com/Environmental.Design.Solutions/" target="_blank"><i class="fab fa-facebook"></i></a>
        <a href="https://www.instagram.com/eds_global/?hl=en" target="_blank"><i class="fab fa-instagram"></i></a>
        <a href="https://www.linkedin.com/company/environmental-design-solutions/" target="_blank"><i class="fab fa-linkedin"></i></a>
    </div>
    """,
    unsafe_allow_html=True
)
# st.snow()
