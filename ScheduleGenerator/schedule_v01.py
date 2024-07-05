import pandas as pd
import streamlit as st
from ScheduleGenerator.src import schedule
import matplotlib.pyplot as plt
from io import BytesIO

def get_file_extension(uploaded_file):
    return uploaded_file.name.split('.')[-1]

def get_schedule(uploaded_file):
    try:
        if uploaded_file is not None:
            file_extension = get_file_extension(uploaded_file)
            if file_extension == 'csv':
                schedules = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            elif file_extension == 'xlsx':
                schedules = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a CSV or XLSX file.")
                return

            schedule.getScheduleINP(schedules)
        else:
            st.info("No file uploaded. Please upload a file and try again.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        
def analytics(uploaded_file):
    try:
        if uploaded_file is not None:
            file_extension = get_file_extension(uploaded_file)
            if file_extension == 'csv':
                data = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                st.markdown("""
                <h3 style="color:red;">Schedules of 24 hours</h3>
                """, unsafe_allow_html=True)
                data = data.drop([0, 3])
                first_col_name = data.columns[0]
                index_to_drop_from = data[data[first_col_name] == "Rows can be added to add more weekly schedule"].index[0]
                data = data[:index_to_drop_from]
                df_rotated = data.T
                # Set the first row as the new header
                df_rotated.columns = df_rotated.iloc[0]
                df_rotated = df_rotated[1:]
                # Reset the index to use default integer indexing
                df_rotated.reset_index(drop=True, inplace=True)
                df_rotated = df_rotated.iloc[:, 2:-2]

                # Assume the "Hour" column exists
                hour_column = 'Hour'
                if hour_column not in df_rotated.columns:
                    raise ValueError(f"'{hour_column}' column not found in the DataFrame")
                else:
                    # Identify the column immediately after the "Hour" column
                    hour_index = df_rotated.columns.get_loc(hour_column)
                    value_column = df_rotated.columns[hour_index + 1]

                    # Convert Hour column to numeric
                    df_rotated[hour_column] = pd.to_numeric(df_rotated[hour_column], errors='coerce')
                    df_rotated = df_rotated.dropna(subset=[hour_column])

                    # Filter the DataFrame to include only hours from 1 to 24
                    df_rotated = df_rotated[(df_rotated[hour_column] >= 1) & (df_rotated[hour_column] <= 24)]

                    # Create a bar chart
                    fig, ax = plt.subplots(figsize=(11, 4))
                    ax.bar(df_rotated[hour_column], df_rotated[value_column], color='blue')

                    # Set the labels and title
                    plt.xlabel('Hour')
                    plt.ylabel('Values')
                    plt.title('Bar Chart of Hour vs. Values')

                    # Show the bar chart
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                    # Streamlit plot display
                    st.pyplot(fig)

                    # Add a download button for the plot
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    st.download_button(
                        label="Download chart as PNG",
                        data=buffer,
                        file_name="bar_chart.png",
                        mime="image/png"
                    )
            
            elif file_extension == 'xlsx':
                st.markdown("""
                <h3 style="color:red;">Schedules of 24 hours</h3>
                """, unsafe_allow_html=True)
                data = pd.read_excel(uploaded_file)
                data = data.drop([0, 3])
                first_col_name = data.columns[0]
                index_to_drop_from = data[data[first_col_name] == "Rows can be added to add more weekly schedule"].index[0]
                data = data[:index_to_drop_from]
                df_rotated = data.T
                # Set the first row as the new header
                df_rotated.columns = df_rotated.iloc[0]
                df_rotated = df_rotated[1:]
                # Reset the index to use default integer indexing
                df_rotated.reset_index(drop=True, inplace=True)
                df_rotated = df_rotated.iloc[:, 2:-2]

                # Assume the "Hour" column exists
                hour_column = 'Hour'
                if hour_column not in df_rotated.columns:
                    raise ValueError(f"'{hour_column}' column not found in the DataFrame")
                else:
                    # Identify the column immediately after the "Hour" column
                    hour_index = df_rotated.columns.get_loc(hour_column)
                    value_column = df_rotated.columns[hour_index + 1]

                    # Convert Hour column to numeric
                    df_rotated[hour_column] = pd.to_numeric(df_rotated[hour_column], errors='coerce')
                    df_rotated = df_rotated.dropna(subset=[hour_column])

                    # Filter the DataFrame to include only hours from 1 to 24
                    df_rotated = df_rotated[(df_rotated[hour_column] >= 1) & (df_rotated[hour_column] <= 24)]

                    # Create a bar chart
                    fig, ax = plt.subplots(figsize=(11, 4))
                    ax.bar(df_rotated[hour_column], df_rotated[value_column], color='blue')

                    # Set the labels and title
                    plt.xlabel('Hour')
                    plt.ylabel('Values')
                    plt.title('Bar Chart of Hour vs. Values')

                    # Show the bar chart
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                    # Streamlit plot display
                    st.pyplot(fig)

                    # Add a download button for the plot
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png')
                    buffer.seek(0)
                    st.download_button(
                        label="Download chart as PNG",
                        data=buffer,
                        file_name="bar_chart.png",
                        mime="image/png"
                    )
    
        else:
            st.info("No file uploaded. Please upload a file and try again.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    uploaded_file = st.file_uploader("Upload CSV or EXCEL file", type=["csv", "xlsx"])
    get_schedule(uploaded_file)
