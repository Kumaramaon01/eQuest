import os
import streamlit as st
import tempfile
from SIM_Parser.src_sim import lv_b, ls_c, lv_d, pv_a, sv_a, beps, bepu, lvd_summary, sva_zone, ps_e, ps_f

def get_report_and_save(report_function, name1, sim_path, file_suffix):
    report = report_function(sim_path)
    file_name = os.path.splitext(os.path.basename(sim_path))[0]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        report.to_csv(temp_file.name, index=False)
        temp_file_path = temp_file.name
    st.success(f"{file_suffix} Report Generated!")
    return temp_file_path

def main(uploaded_file):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name

        sim_path = temp_file_path

        download_links = []

        download_links.append(("LSC", get_report_and_save(ls_c.get_LSC_report, None, sim_path, 'lsc')))
        download_links.append(("LVD", get_report_and_save(lv_d.get_LVD_report, None, sim_path, 'lvd')))
        download_links.append(("LVD Summary", get_report_and_save(lvd_summary.get_LVD_Summary_report, None, sim_path, 'lvd_Summary')))
        download_links.append(("PVA", get_report_and_save(pv_a.get_PVA_report, None, sim_path, 'pva')))
        download_links.append(("SVA", get_report_and_save(sv_a.get_SVA_report, None, sim_path, 'sva')))
        download_links.append(("SVA Zone", get_report_and_save(sva_zone.get_SVA_Zone_report, None, sim_path, 'sva_Zone')))
        download_links.append(("BEPS", get_report_and_save(beps.get_BEPS_report, None, sim_path, 'beps')))
        download_links.append(("BEPU", get_report_and_save(bepu.get_BEPU_report, None, sim_path, 'bepu')))
        download_links.append(("LVB", get_report_and_save(lv_b.get_LVB_report, None, sim_path, 'lvb')))
        download_links.append(("PSE", get_report_and_save(ps_e.get_PSE_report, None, sim_path, 'pse')))
        download_links.append(("PSF", get_report_and_save(ps_f.get_PSF_report, None, sim_path, 'psf')))

        st.success("SIM Parsed Successfully!!")

        for report_name, file_path in download_links:
            st.markdown(f"[Download {report_name} Report](file://{file_path})")

    else:
        st.error("Please upload a SIM file.")
