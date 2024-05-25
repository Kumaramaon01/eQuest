import os
import streamlit as st
import tempfile
from SIM_Parser.src_sim import lv_b, ls_c, lv_d, pv_a, sv_a, beps, bepu, lvd_summary, sva_zone, ps_e, ps_f

def get_report_and_save(report_function, name1, sim_path, file_suffix):
    report = report_function(sim_path)
    # Get the parent directory of the SIM file
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
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name

        sim_path = temp_file_path

        get_report_and_save(ls_c.get_LSC_report, None, sim_path, 'lsc')
        get_report_and_save(lv_d.get_LVD_report, None, sim_path, 'lvd')
        get_report_and_save(lvd_summary.get_LVD_Summary_report, None, sim_path, 'lvd_Summary')
        get_report_and_save(pv_a.get_PVA_report, None, sim_path, 'pva')
        get_report_and_save(sv_a.get_SVA_report, None, sim_path, 'sva')
        get_report_and_save(sva_zone.get_SVA_Zone_report, None, sim_path, 'sva_Zone')
        get_report_and_save(beps.get_BEPS_report, None, sim_path, 'beps')
        get_report_and_save(bepu.get_BEPU_report, None, sim_path, 'bepu')
        get_report_and_save(lv_b.get_LVB_report, None, sim_path, 'lvb')
        get_report_and_save(ps_e.get_PSE_report, None, sim_path, 'pse')
        get_report_and_save(ps_f.get_PSF_report, None, sim_path, 'psf')
        
        st.success("SIM Parsed Successfully!!")
    else:
        st.error("Please upload a SIM file.")
