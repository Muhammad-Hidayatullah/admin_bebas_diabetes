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



halaman_penyakit = st.Page(
    page="pages_admin/2_penyakit.py",
    title="Penyakit",
    icon=":material/microbiology:",
)

halaman_gejala = st.Page(
    page="pages_admin/3_gejala.py",
    title="Gejala",
    icon=":material/symptoms:",
)

halaman_relasi_dan_gejala = st.Page(
    page="pages_admin/4_relasi_penyakit_dan_gejala.py",
    title="Relasi Penyakit dan Gejala",
    icon=":material/fact_check:",
)

halaman_artikel = st.Page(
    page="pages_admin/5_artikel.py",
    title="Artikel",
    icon=":material/article:",
)

halaman_pengguna = st.Page(
    page="pages_admin/6_pengguna.py",
    title="Pengguna",
    icon=":material/patient_list:",
)

halaman_riwayat_pengguna = st.Page(
    page="pages_admin/7_riwayat_pengguna.py",
    title="Riwayat Pengguna",
    icon=":material/summarize:"
)

halaman_log_out = st.Page(
    page="pages_admin/8_log_out.py",
    title="Log Out",
    icon=":material/logout:"
)




if "masuk_website" not in st.session_state:
    st.session_state.masuk_website = None

if st.session_state.masuk_website == None:
    st.session_state.pg = st.navigation(pages=[admin])
    
    
    st.session_state.pg.run()
    
if st.session_state.masuk_website == "Admin":
    st.session_state.pg = st.navigation(pages=[home_website_admin, halaman_penyakit, halaman_gejala, halaman_relasi_dan_gejala, 
                                               halaman_pengguna, halaman_riwayat_pengguna, halaman_artikel, halaman_log_out])
    st.session_state.pg.run()
    






