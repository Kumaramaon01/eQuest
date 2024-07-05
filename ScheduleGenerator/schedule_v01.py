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
            st.info("Please upload a file to see some analytics.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        
def plot_chart(df, hour_column, value_column):
    # Create a bar chart
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjust size as needed
    ax.bar(df[hour_column], df[value_column], color='blue')

    # Set the labels and title
    ax.set_xlabel('Hour')
    ax.set_ylabel('Values')
    ax.set_title(f'{value_column} vs. Hour')

    # Ensure all x-axis values from 1 to 24 are visible
    ax.set_xticks(range(1, 25))

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45)

    # Adjust layout
    plt.tight_layout()

    return fig

def analytics(uploaded_file):
    try:
        if uploaded_file is not None:
            file_extension = get_file_extension(uploaded_file)
            if file_extension == 'csv':
                data = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            elif file_extension == 'xlsx':
                data = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a CSV or XLSX file.")
                return

            st.markdown("""
            <h3 style="color:red;">Schedules of 24 hours</h3>
            """, unsafe_allow_html=True)

            # Your data processing code
            data = data.drop([0, 3])
            first_col_name = data.columns[0]
            index_to_drop_from = data[data[first_col_name] == "Rows can be added to add more weekly schedule"].index[0]
            data = data[:index_to_drop_from]

            df_rotated = data.T
            df_rotated.columns = df_rotated.iloc[0]
            df_rotated = df_rotated[1:]
            df_rotated.reset_index(drop=True, inplace=True)
            df_rotated = df_rotated.iloc[:, 2:-2]

            hour_column = 'Hour'
            if hour_column not in df_rotated.columns:
                raise ValueError(f"'{hour_column}' column not found in the DataFrame")

            value_columns = df_rotated.columns[df_rotated.columns.get_loc(hour_column) + 1:]

            # Display charts in rows of two
            num_charts = len(value_columns)
            num_cols = 2
            num_rows = (num_charts + 1) // num_cols  # Calculate number of rows needed

            for i, value_column in enumerate(value_columns):
                if i % num_cols == 0:
                    columns = st.columns(num_cols)  # Create columns layout
                fig_chart = plot_chart(df_rotated, hour_column, value_column)
                with columns[i % num_cols]:  # Place chart in the current column
                    st.pyplot(fig_chart)

                    # Add a download button for the plot
                    buffer = BytesIO()
                    fig_chart.savefig(buffer, format='png')
                    buffer.seek(0)
                    st.download_button(
                        # label=f"Download {value_column} chart",
                        label=f"Download",
                        data=buffer,
                        file_name=f"bar_chart_{value_column}.png",
                        mime="image/png"
                    )

        else:
            st.info("Please upload a file to see Analytics.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")


if __name__ == "__main__":
    uploaded_file = st.file_uploader("Upload CSV or EXCEL file", type=["csv", "xlsx"])
    get_schedule(uploaded_file)
