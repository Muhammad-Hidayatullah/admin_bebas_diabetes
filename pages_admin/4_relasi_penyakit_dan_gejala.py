import streamlit as st
from assets import database as db
import time

st.title("RELASI PENYAKIT DAN GEJALA")
st.subheader("PENYAKIT")
penyakit_df = db.fetch_penyakit()
penyakit_df_html = penyakit_df.to_html(index=False, escape=False)
st.markdown(st.session_state.style_tabel + penyakit_df_html, unsafe_allow_html=True)

st.subheader("GEJALA")
gejala_df = db.fetch_gejala()
gejala_df_html = gejala_df.to_html(index=False, escape=False)
st.markdown(st.session_state.style_tabel + gejala_df_html, unsafe_allow_html=True)

st.subheader("RELASI PENYAKIT DAN GEJALA")
df_relasi_penyakit_dan_gejala = db.fetch_relasi_penyakit_dan_gejala_full()
relasi_penyakit_dan_gejala_df_html = df_relasi_penyakit_dan_gejala.to_html(index=False, escape=False)
st.markdown(st.session_state.style_tabel + relasi_penyakit_dan_gejala_df_html, unsafe_allow_html=True)




pilihan_relasi = st.radio("Pilih Opsi untuk Kelola Relasi Penyakit dan Gejala: ", ("Tambah Relasi", "Update Relasi", "Hapus Relasi"), horizontal=True)

df_penyakit = db.fetch_penyakit()
kol_id_penyakit = df_penyakit["ID Penyakit"]

df_gejala = db.fetch_gejala()
kol_id_gejala = df_gejala["ID Gejala"]


if pilihan_relasi == "Tambah Relasi":
    st.subheader("Tambah Relasi")
    id_komplikasi_penyakit = st.selectbox("Masukkan kode penyakit: ", options=kol_id_penyakit, index=0)
    id_gejala = st.selectbox("Masukkan kode gejala: ", options=kol_id_gejala, index=0)
    if st.button("Tambah Relasi"):
        db.add_relasi_penyakit_dan_gejala(id_komplikasi_penyakit, id_gejala)
        time.sleep(2)
        st.rerun()
if pilihan_relasi == "Update Relasi":
    st.subheader("Update Relasi")
    id_komplikasi_penyakit = st.selectbox("Masukkan kode penyakit: ", options=kol_id_penyakit, index=0)
    id_gejala = st.selectbox("Masukkan kode gejala: ", options=df_relasi_penyakit_dan_gejala[df_relasi_penyakit_dan_gejala["ID Penyakit"] == id_komplikasi_penyakit]["ID Gejala"], index=0)
    
    id_komplikasi_penyakit_baru = st.selectbox("Masukkan kode penyakit baru: ", options=kol_id_penyakit)
    id_gejala_baru = st.selectbox("Masukkan kode gejala baru: ", options=kol_id_gejala, index=0)
    
    if st.button("Update Relasi"):
        db.update_relasi_penyakit_dan_gejala(id_komplikasi_penyakit, id_gejala, id_gejala_baru)
        time.sleep(2)
        st.rerun()

if pilihan_relasi == "Hapus Relasi":
    st.subheader("Hapus Relasi")
    if "hapus_relasi" not in st.session_state:
        st.session_state.hapus_relasi = 0
        
    id_komplikasi_penyakit = st.selectbox("Masukkan kode penyakit: ", options=df_relasi_penyakit_dan_gejala["ID Penyakit"].unique(), index=0)
    id_gejala = st.selectbox("Masukkan kode gejala: ", options=df_relasi_penyakit_dan_gejala[df_relasi_penyakit_dan_gejala["ID Penyakit"] == id_komplikasi_penyakit]["ID Gejala"], index=0)
    if st.button("Hapus Relasi"):
        st.session_state.hapus_relasi = 1
    if st.session_state.hapus_relasi == 1:
        st.warning("Apakah Anda yakin ingin menghapus relasi penyakit dan gejala tersebut?")
        if st.button("Ya"):
            st.session_state.hapus_relasi = 2
    if st.session_state.hapus_relasi == 2:
        st.success("Berhapus menghapus relasi penyakit dan gejala")
        st.session_state.hapus_relasi = 0
        db.hapus_relasi_penyakit_dan_gejala(id_komplikasi_penyakit, id_gejala)
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
