import glob as gb
import os
from fpdf import FPDF

# Reading sim files line by line
def read_sim_file(sim_file_path):
    if os.path.isfile(sim_file_path):
        with open(sim_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print("SIM file does not exist.")
        return None

# Removed some useless lines of SIM files that were repeated many times
def clean_sim(name):
    with open(name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        cleaned_lines = []
        i = 0
        while i < len(lines) - 1:
            if "REPORT" in lines[i] and "RUN" in lines[i + 1]:
                i += 2
            elif "RUN" in lines[i] and i == len(lines) - 2:
                i += 1
            else:
                cleaned_lines.append(lines[i])
                i += 1

    return ''.join(cleaned_lines)

# Function to modify generated pdf and override in the same folder
def get_report_as_pdf(report_content, folder_name, output_directory, pdf_file_path):
    pdf = FPDF()
    pdf.set_font("Courier", size=6.5)
    pdf.add_page(orientation='L')
    pdf.set_auto_page_break(auto=True, margin=10)

    report_lines = report_content.strip().split('\n')

    for line in report_lines:
        if "RUN" in line:
            pdf.add_page()
        pdf.multi_cell(0, 4, line)

    pdf.output(pdf_file_path)
    print(f"PDF report Generated: {pdf_file_path}")

# Function to generate PDF directly in the "Report Outputs" folder
def generate_pdf(output_directory):
    simfiles = gb.glob(os.path.join(output_directory, '*.sim'))
    if simfiles:
        for sim_file in simfiles:
            folder_name = os.path.splitext(os.path.basename(sim_file))[0]
            report_content = read_sim_file(sim_file)

            if report_content:
                print("\nGenerating PDF report...")
                pdf_file_path = os.path.join(output_directory, f'{folder_name}.pdf')
                get_report_as_pdf(report_content, folder_name, output_directory, pdf_file_path)
                print("PDF report generation complete.")
    else:
        print("No SIM files found in the specified directory.")

# Function to extract relevant data from SIM file based on input reports
def extractReport(input_sim_files, reports):
    try:
        simfiles = gb.glob(os.path.join(input_sim_files, '*.sim'))

        # Create "Report Outputs" folder inside the folder containing SIM files
        output_directory = os.path.join(input_sim_files, "Report Outputs")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        else:
            shutil.rmtree(output_directory)
            os.makedirs(output_directory)

        # Process each SIM file
        for name in simfiles:
            with open(name) as f:
                f_list = f.readlines()
                for num, line in enumerate(f_list):
                    for r in reports:
                        if r in line:
                            rptstart = num - 2
                            lines = 0
                            for line in f_list[rptstart + 3:]:
                                if "REPORT" in line:
                                    rptlen = lines
                                    break
                                lines += 1
                            section = f_list[rptstart:rptstart + rptlen + 4]
                            file_name = "Reports_" + os.path.basename(name)
                            file_path = os.path.join(output_directory, file_name)
                            with open(file_path, "a") as output:
                                for l in section:
                                    output.write(l)
                            break

        # Clean generated SIM files in "Report Outputs" folder
        for filename in os.listdir(output_directory):
            file_path = os.path.join(output_directory, filename)
            cleaned_content = clean_sim(file_path)
            if isinstance(cleaned_content, list):
                cleaned_content = "\n".join(cleaned_content)
            with open(file_path, "w") as cleaned_file:
                cleaned_file.write(cleaned_content)

        # Generate PDF reports from the cleaned SIM files in "Report Outputs" folder
        generate_pdf(output_directory)
        return "Extraction and PDF generation completed successfully."
    except Exception as e:
        error_message = f"Error during extraction: {e}"
        print(error_message)
        return error_message
