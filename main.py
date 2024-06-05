import streamlit as st
import subprocess
import os
from INP_Parser import inp_parserv01
from Perging_INP import perge
from SIM_Parser import sim_parserv01
from SIM2PDF import sim_print
from BaselineAutomation import baselineAuto
from streamlit_card import card
from PIL import Image as PILImage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials and recipient
TO_EMAIL = "rajeev@edsglobal.com"

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

def main(): 
    st.set_page_config(page_title="eQuest Utilities", page_icon="💡")

    # Add custom CSS to set the background color and hide Streamlit branding elements
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

    # Header section with logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image("images/EDSlogo.png", width=120)  # Replace with the path to your logo file
    with col2:
        st.markdown("<h1 style='text-align: left; color:red;'>eQuest Utilities</h1>", unsafe_allow_html=True)

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
        st.write(icon_with_tooltip1, unsafe_allow_html=True)
    # Add icon and tooltip to col3

    # Navigation bar with buttons below the header
    st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)
    
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
    
    # Use a fixed width for the columns to ensure buttons have the same size
    col7, col8, col9, col10 = st.columns([0.9, 1.3, 1, 1])
    with col7:
        if st.button("SIM to PDF"):
            st.session_state.script_choice = "SIM to PDF"
    with col8:
        if st.button("Baseline Automation"):
            st.session_state.script_choice = "baselineAutomation"
    with col9:
        if st.button("EXE Files"):
            st.session_state.script_choice = "exe"
    with col10:
        if st.button("Queries"):
            st.session_state.script_choice = "ask"

    # Based on the user selection, display appropriate input fields and run the script
    if st.session_state.script_choice == "about":
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

    elif st.session_state.script_choice == "INP Parser":
        st.markdown("""
        <h3 style="color:red;">INP Parser</h3>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload an INP file", type="inp", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run INP Parser"):
                inp_parserv01.main(uploaded_file)

    elif st.session_state.script_choice == "Purging INP":
        st.markdown("""
        <h3 style="color:red;">Purging INP</h3>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload an INP file", type="inp", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run INP Purging"):
                perge.main(uploaded_file)

    elif st.session_state.script_choice == "SIM Parser":
        st.markdown("""
        <h3 style="color:red;">SIM Parser</h3>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a SIM file", type="sim", accept_multiple_files=False)
        
        if uploaded_file is not None:
            if st.button("Run SIM Parser"):
                sim_parserv01.main(uploaded_file)

    elif st.session_state.script_choice == "SIM to PDF":
        st.markdown("""
        <h3 style="color:red;">SIM to PDF Converter</h3>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        Enter Reports in following format (comma-seperated and case-sensitive). And, It can accept multiple sim files.
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload a SIM file", type="sim", accept_multiple_files=True)
        reports_input = st.text_input("Enter Reports")
        
        if uploaded_file is not None:
            if st.button("Convert to PDF"):
                reports = [r.strip() for r in reports_input.split(',')]
                sim_print.main(reports, uploaded_file)
                
    elif st.session_state.script_choice == "ask":
        # st.header("Reach Out to Queries")
        col1, col2 = st.columns(2)
        with col1:
            st.write(icon_with_tooltip1, unsafe_allow_html=True)
        with col2:
            st.write(icon_with_tooltip2, unsafe_allow_html=True)

        email = st.text_input("Enter your mail:")
        user_input = st.text_area("Enter your Queries:")
    
        # Submit button
        if st.button("Submit"):
            if user_input:
                subject = "Text Area Submission"
                message = user_input
                EMAIL = email
                if send_email(subject, message, EMAIL, TO_EMAIL):
                    st.success("Email sent successfully!")
                # else:
                #     st.error("Failed to send email.")
            else:
                st.warning("Please enter some text.")

    elif st.session_state.script_choice == "exe":
        st.markdown("""
        <h3 style="color:red;">EXE Files</h3>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            # st.markdown("<h2>INP Parser</h2>", unsafe_allow_html=True)
            # st.write("Parsing INP files")
            st.image(PILImage.open("images/INP_Parser_logo.png"), use_column_width=True)
            st.write("[Download](https://drive.google.com/file/d/1_jgaEfJCuoqfZOq3hY33D-3x31-v-nTH/view?usp=drive_link)")
        with col2:
            # st.markdown("<h2>SIM Parser</h2>", unsafe_allow_html=True)
            # st.write("Parsing SIM files")
            st.image(PILImage.open("images/SIM_Parser_logo.png"), use_column_width=True)
            st.write("[Download](https://drive.google.com/file/d/1jhIyXWMRo7z0J6n32R6omVNpM3Xd8beY/view?usp=drive_link)")
        with col3:
            # st.markdown("<h2>EXE 3</h2>", unsafe_allow_html=True)
            # st.write("Purging INP")
            st.image(PILImage.open("images/perging_inp_logo.ico"), use_column_width=True)
            st.write("[Download](https://drive.google.com/file/d/1oIQmgVAMy871cwwQPnlm3FAAlEB_Bl7o/view?usp=drive_link)")
        with col4:
            # st.markdown("<h2>EXE 3</h2>", unsafe_allow_html=True)
            # st.write("Purging INP")
            st.image(PILImage.open("images/SIM_pdf.png"), use_column_width=True)
            st.write("[Download](https://drive.google.com/file/d/10jga6aMVQHgEIG1rhMaqs_sXTt3yEJXK/view?usp=drive_link)")
        with col5:
            st.image(PILImage.open("images/baseline.png"), use_column_width=True)
            st.write("[Download](url_to_exe_1)")
        
        # Add more cards as needed
        st.markdown("""
        #### Note:
        Due to the large size of eQuest Utilities exe files, they may not be suitable for direct hosting on our website. 
        However, they are available for download.
        """)
        # Add more cards as needed

    elif st.session_state.script_choice == "baselineAutomation":
        st.markdown("""
        <h3 style="color:red;">Baseline Automation</h3>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            uploaded_inp_file = st.file_uploader("Upload an INP file", type="inp", accept_multiple_files=False)
        with col2:
            uploaded_sim_file = st.file_uploader("Upload a SIM file", type="sim", accept_multiple_files=False)
        col1, col2, col3 = st.columns(3)
        with col1:
            input_climate = st.selectbox("Climate Zone", options=[1, 2, 3, 4, 5, 6, 7, 8])
        with col2:
            input_building_type = st.selectbox("Building Type", options=[0, 1], format_func=lambda x: "Residential" if x == 0 else "Non-Residential")
        with col3:
            input_area = st.number_input("Enter Area (Sqft)", min_value=0.0, step=0.1)
        col1, col2 = st.columns(2)
        with col1:
            number_floor = st.number_input("Number of Floors", min_value=1, step=1)
        with col2:
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
