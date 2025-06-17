import streamlit as st
from assets import database as db
import time

st.logo("assets/logo_diabetes.png", size="large")
st.html("""
  <style>
    [alt=Logo] {
      height: 6rem;
    }
  </style>
        """)
st.logo("assets/logo_diabetes.png", size="large")



pg_bg_img = """
<style> 

[data-testid="stSidebar"]{
    background-image: url("https://images.unsplash.com/photo-1581159186721-b68b78da4ec9?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
}
</style>

"""

st.markdown(pg_bg_img, unsafe_allow_html=True)







admin = st.Page(
    page="pages/1_login_admin.py",
    title="Login Admin",
    icon=":material/diagnosis:",
)


#Halaman untuk admin
home_website_admin = st.Page(
    page="pages_admin/1_home_admin.py",
    title="Dasbor",
    icon=":material/home:",
)   

halaman_dokter = st.Page(
    page="pages_admin/2_dokter.py",
    title="Dokter",
    icon=":material/stethoscope:",
)

halaman_penyakit = st.Page(
    page="pages_admin/3_penyakit.py",
    title="Penyakit",
    icon=":material/microbiology:",
)

halaman_gejala = st.Page(
    page="pages_admin/4_gejala.py",
    title="Gejala",
    icon=":material/symptoms:",
)

halaman_relasi_dan_gejala = st.Page(
    page="pages_admin/5_relasi_penyakit_dan_gejala.py",
    title="Relasi Penyakit dan Gejala",
    icon=":material/fact_check:",
)

halaman_artikel = st.Page(
    page="pages_admin/8_artikel.py",
    title="Artikel",
    icon=":material/article:",
)

halaman_pengguna = st.Page(
    page="pages_admin/6_pengguna.py",
    title="Pengguna",
    icon=":material/patient_list:",
)



halaman_log_out = st.Page(
    page="pages_admin/9_log_out.py",
    title="Log Out",
    icon=":material/logout:"
)


home_website_dokter = st.Page(
    page="pages_dokter/1_home_dokter.py",
    title="Dokter",
    icon=":material/endocrinology:",
)  

data_profil_dokter = st.Page(
    page="pages_dokter/2_data_profil_dokter.py",
    title="Profil Dokter",
    icon=":material/account_circle:",
) 

halaman_riwayat_pengguna_dokter = st.Page(
    page="pages_dokter/3_riwayat_pengguna.py",
    title="Riwayat Pengguna",
    icon=":material/medical_information:"
)


halaman_log_out_dokter = st.Page(
    page="pages_dokter/4_logout.py",
    title="Log Out",
    icon=":material/logout:"
)
if "masuk_website" not in st.session_state:
    st.session_state.masuk_website = None

if st.session_state.masuk_website == None:
    st.session_state.pg = st.navigation(pages=[admin])
    
    
    st.session_state.pg.run()
    
if st.session_state.masuk_website == "Admin":
    st.session_state.pg = st.navigation(pages=[home_website_admin, halaman_dokter, halaman_penyakit, halaman_gejala, halaman_relasi_dan_gejala, 
                                               halaman_pengguna, halaman_artikel, halaman_log_out])
    st.session_state.pg.run()
    
if st.session_state.masuk_website == "Dokter":
    st.session_state.pg = st.navigation(pages=[home_website_dokter, data_profil_dokter, halaman_riwayat_pengguna_dokter, halaman_log_out_dokter])
    st.session_state.pg.run()






