import streamlit as st
from assets import database as db
import time


st.title("GEJALA")
df_gejala = db.fetch_gejala()
gejala_df_html = df_gejala.to_html(index=False, escape=False)
st.markdown(st.session_state.style_tabel + gejala_df_html, unsafe_allow_html=True)



pilihan_gejala = st.radio("Pilih Opsi untuk Kelola Gejala", ("Tambah Gejala", "Update Gejala", "Hapus Gejala"), horizontal=True)

kol_id_gejala = df_gejala["ID Gejala"]

if pilihan_gejala == "Tambah Gejala":
    st.subheader("Tambah Gejala")
    nama_gejala = ""
    id_gejala = st.text_input("Masukkan kode gejala: ", db.menambah_id_gejala_default())
    nama_gejala = st.text_input("Masukkan nama gejala: ")
    if st.button("Tambah Gejala"):
        db.add_gejala(id_gejala, nama_gejala)
        
        time.sleep(2)
        
        st.rerun()
        nama_gejala = ""

if pilihan_gejala == "Update Gejala":
    st.subheader("Update Gejala")
    id_gejala = st.selectbox("Masukkan kode gejala: ", options=kol_id_gejala, index=0)
    
    nama_gejala_default = df_gejala.loc[df_gejala["ID Gejala"] == id_gejala, "Nama Gejala"].values[0]
    nama_gejala = st.text_input("Masukkan nama gejala baru: ", nama_gejala_default)
    if st.button("Update"):
        db.update_gejala(id_gejala, nama_gejala)
        time.sleep(2)
        st.rerun()
    
if pilihan_gejala == "Hapus Gejala":
    st.subheader("Hapus Gejala")
    if "konfirmasi_menghapus_gejala" not in st.session_state:
        st.session_state.konfirmasi_menghapus_gejala = 0
    
    id_gejala = st.selectbox("Masukkan kode gejala yang ingin dihapus: ", options=kol_id_gejala, index=0)
    if st.button("Hapus"):
        st.session_state.konfirmasi_menghapus_gejala = 1 
    
    if st.session_state.konfirmasi_menghapus_gejala == 1:
        st.warning("Apakah Anda yakin ingin menghapus gejala tersebut?")
        if st.button("Ya"):
            st.session_state.konfirmasi_menghapus_gejala = 2 
            
    if st.session_state.konfirmasi_menghapus_gejala == 2:
        
        st.session_state.konfirmasi_menghapus_gejala = 0
        db.hapus_gejala(id_gejala)
        time.sleep(2)
        st.rerun()


st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
