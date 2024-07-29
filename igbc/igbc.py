import os
import pandas as pd
from src import igbc_parser

def get_report_and_save(report_function, name, name1, file_suffix, folder_name, path, output_text):
    report = report_function(name, name1, path)
    file_path = os.path.join(path, f'{folder_name}_{file_suffix}.csv')
    if os.path.isfile(file_path):
        os.remove(file_path)
    with open(file_path, 'w', newline='') as f:
        report.to_csv(f, header=True, index=False, mode='wt')
    print(f"{file_suffix} Report Generated!")

def open_input_cmd():
    print("Welcome to INP Parser")
    inp_file_path = input("Enter the path of the INP file: ")
    sim_file_path = input("Enter the path of the SIM file: ")
    if os.path.isfile(inp_file_path and sim_file_path):
        folder_name = os.path.basename(inp_file_path).split(".")[0]
        if '- Baseline Design' in inp_file_path:
            folder_name = os.path.basename(inp_file_path).split(" - ")[0]
        else:
            folder_name = os.path.basename(inp_file_path).split(".")[0]
        parent_directory = os.path.dirname(inp_file_path)

        get_report_and_save(igbc_parser.get_HVAC_Zone_report, inp_file_path, sim_file_path, 'IGBC', folder_name, parent_directory, None)
    else:
        print("Invalid INP file path.")

    input("Press Enter to exit...")

open_input_cmd()
