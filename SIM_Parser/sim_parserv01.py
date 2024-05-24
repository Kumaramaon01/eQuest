import os
import streamlit as st
import pandas as pd
from SIM_Parser.src_sim import lv_b, ls_c, lv_d, pv_a, sv_a, beps, bepu, lvd_summary, sva_zone, ps_e, ps_f


def get_report_and_save(report_function, name1, sim_path, file_suffix):
    report = report_function(sim_path)
    # Get the parent directory of the INP file
    parent_directory = os.path.dirname(sim_path)
    file_name = os.path.splitext(os.path.basename(sim_path))[0]
    file_path = os.path.join(parent_directory, f'{file_name}_{file_suffix}.csv')
    if os.path.isfile(file_path):
        os.remove(file_path)
    report.to_csv(file_path, index=False)
    st.success(f"{file_suffix} Report Generated!")

def main(uploaded_file):
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        sim_path = os.path.join(os.path.expanduser("~"), "Downloads", uploaded_file.name)
        with open(sim_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            sim_content = uploaded_file.getvalue()

            get_report_and_save(ls_c.get_LSC_report, sim_content, sim_path, 'lsc')
            get_report_and_save(lv_d.get_LVD_report, sim_content, sim_path, 'lvd')
            get_report_and_save(lvd_summary.get_LVD_Summary_report, sim_content, sim_path, 'lvd_Summary')
            get_report_and_save(pv_a.get_PVA_report, sim_content, sim_path, 'pva')
            get_report_and_save(sv_a.get_SVA_report, sim_content, sim_path, 'sva')
            get_report_and_save(sva_zone.get_SVA_Zone_report, sim_content, sim_path, 'sva_Zone')
            get_report_and_save(beps.get_BEPS_report, sim_content, sim_path, 'beps')
            get_report_and_save(bepu.get_BEPU_report, sim_content, sim_path, 'bepu')
            get_report_and_save(lv_b.get_LVB_report, sim_content, sim_path, 'lvb')
            get_report_and_save(ps_e.get_PSE_report, sim_content, sim_path, 'pse')
            get_report_and_save(ps_f.get_PSF_report, sim_content, sim_path, 'psf')
            st.success("SIM Parsed Successfully!!")

    else:
        st.error("Please upload a SIM file.")