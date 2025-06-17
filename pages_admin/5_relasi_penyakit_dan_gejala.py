import streamlit as st
from assets import database as db
import time




st.subheader("RELASI PENYAKIT DAN GEJALA")
df_relasi_penyakit_dan_gejala = db.fetch_relasi_penyakit_dan_gejala_full()
relasi_penyakit_dan_gejala_df_html = df_relasi_penyakit_dan_gejala.to_html(index=False, escape=False)
st.markdown(st.session_state.style_tabel + relasi_penyakit_dan_gejala_df_html, unsafe_allow_html=True)




pilihan_relasi = st.radio("Pilih Opsi untuk Kelola Relasi Penyakit dan Gejala: ", ("Tambah Relasi", "Update Relasi", "Hapus Relasi"), horizontal=True)

df_penyakit = db.fetch_penyakit()
kol_id_penyakit = df_penyakit["ID Penyakit"]
kol_nama_penyakit = df_penyakit["Nama Penyakit"]


df_gejala = db.fetch_gejala()
kol_id_gejala = df_gejala["ID Gejala"]
kol_nama_gejala = df_gejala["Nama Gejala"]

df_dokter = db.fetch_dokter()
kol_id_dokter = df_dokter["ID Dokter"]
kol_nama_dokter = df_dokter["Nama Dokter"]


if pilihan_relasi == "Tambah Relasi":
    st.subheader("Tambah Relasi")
    

    nama_komplikasi_penyakit = st.selectbox("Masukkan nama penyakit: ", options=kol_nama_penyakit, index=0)
    id_komplikasi_penyakit = df_penyakit[df_penyakit["Nama Penyakit"] == nama_komplikasi_penyakit]["ID Penyakit"].iloc[0]
    
    
    
    gejala_terpakai = df_relasi_penyakit_dan_gejala[df_relasi_penyakit_dan_gejala["Nama Penyakit"] == nama_komplikasi_penyakit]["ID Gejala"]
    
    
    df_gejala_tersisa = df_gejala[~df_gejala['ID Gejala'].isin(gejala_terpakai)]
    
    kol_nama_gejala_tersisa = df_gejala_tersisa["Nama Gejala"]

        
    
    nama_gejala = st.multiselect("Masukkan nama gejala: ", options=kol_nama_gejala_tersisa, placeholder="Daftar Gejala")
    
    
    
    
    
    if nama_gejala:
        daftar_id_gejala_terpilih = df_gejala[df_gejala["Nama Gejala"].isin(nama_gejala)]["ID Gejala"]
    else:
        daftar_id_gejala_terpilih = []
        
        
    nama_dokter = st.selectbox("Masukkan nama dokter: ", options=kol_nama_dokter, index=0)
    id_dokter = df_dokter[df_dokter["Nama Dokter"] == nama_dokter]["ID Dokter"].iloc[0]
   
   
    if st.button("Tambah Relasi"):
        if len(daftar_id_gejala_terpilih) == 0:
            st.error("Silakan pilih setidaknya satu gejala sebelum menambahkan relasi.")
        else:
            db.add_relasi_penyakit_dan_gejala(id_komplikasi_penyakit, daftar_id_gejala_terpilih, id_dokter)
            st.success("Relasi Penyakit dan Gejala berhasil ditambahkan!")
            time.sleep(2)
            st.rerun()
            
if pilihan_relasi == "Update Relasi":
    st.subheader("Update Relasi")
    
    
    kol_id_penyakit_relasi = df_relasi_penyakit_dan_gejala["ID Penyakit"].unique()
    kol_nama_penyakit_relasi = df_relasi_penyakit_dan_gejala["Nama Penyakit"].unique()
    
    nama_komplikasi_penyakit_relasi = st.selectbox("Masukkan nama penyakit: ", options=kol_nama_penyakit_relasi, index=0)
    id_komplikasi_penyakit_relasi = df_penyakit[df_penyakit["Nama Penyakit"] == nama_komplikasi_penyakit_relasi]["ID Penyakit"].iloc[0]
   
    
    nama_gejala = st.selectbox("Masukkan nama gejala: ", options=df_relasi_penyakit_dan_gejala[df_relasi_penyakit_dan_gejala["Nama Penyakit"] == nama_komplikasi_penyakit_relasi]["Nama Gejala"].unique(), index=0)
    id_gejala = df_relasi_penyakit_dan_gejala[df_relasi_penyakit_dan_gejala["Nama Gejala"] == nama_gejala]["ID Gejala"].iloc[0]


    nama_dokter = st.selectbox("Masukkan nama dokter", options=df_relasi_penyakit_dan_gejala[(df_relasi_penyakit_dan_gejala["Nama Penyakit"] == nama_komplikasi_penyakit_relasi) & (df_relasi_penyakit_dan_gejala["Nama Gejala"] == nama_gejala)]["Nama Dokter"].unique(), index=0)
    
    
    nama_gejala_baru = st.selectbox("Masukkan nama gejala baru: ", options=kol_nama_gejala, index=0)
    id_gejala_baru = df_gejala[df_gejala["Nama Gejala"] == nama_gejala_baru]["ID Gejala"].iloc[0]
    
    
    nama_dokter_default = df_relasi_penyakit_dan_gejala.loc[df_relasi_penyakit_dan_gejala["ID Penyakit"] == id_komplikasi_penyakit_relasi, "Nama Dokter"].values[0]
  
    
    nama_dokter_baru = st.selectbox("Masukkan nama dokter baru: ", options=kol_nama_dokter, index=0)
  
    if st.button("Update Relasi"):
        db.update_relasi_penyakit_dan_gejala(id_komplikasi_penyakit_relasi, id_gejala, id_gejala_baru)
        
        time.sleep(2)
        st.rerun()

if pilihan_relasi == "Hapus Relasi":
    st.subheader("Hapus Relasi")
    if "hapus_relasi" not in st.session_state:
        st.session_state.hapus_relasi = 0
        
    nama_komplikasi_penyakit_relasi = st.selectbox("Masukkan nama penyakit: ", options=df_relasi_penyakit_dan_gejala["Nama Penyakit"].unique(), index=0)

    
    id_komplikasi_penyakit_relasi = df_relasi_penyakit_dan_gejala[df_relasi_penyakit_dan_gejala["Nama Penyakit"] == nama_komplikasi_penyakit_relasi]["ID Penyakit"].iloc[0]
  

    
    nama_gejala_terpakai = df_relasi_penyakit_dan_gejala[df_relasi_penyakit_dan_gejala["Nama Penyakit"] == nama_komplikasi_penyakit_relasi]["Nama Gejala"]

    
    nama_gejala = st.multiselect("Masukkan nama gejala: ", options=nama_gejala_terpakai, placeholder="Daftar Gejala")
    daftar_id_gejala_terpilih = []
    if nama_gejala:
        daftar_id_gejala_terpilih = df_gejala[df_gejala["Nama Gejala"].isin(nama_gejala)]["ID Gejala"]
    
        
    
    if st.button("Hapus Relasi"):
        if len(daftar_id_gejala_terpilih) == 0:
            st.error("Silakan pilih setidaknya satu gejala sebelum menambahkan relasi.")
        else:
            st.session_state.hapus_relasi = 1
    if st.session_state.hapus_relasi == 1:
        st.warning("Apakah Anda yakin ingin menghapus relasi penyakit dan gejala tersebut?")
        if st.button("Ya"):
            st.session_state.hapus_relasi = 2
    if st.session_state.hapus_relasi == 2:
        st.success("Berhapus menghapus relasi penyakit dan gejala")
        st.session_state.hapus_relasi = 0
        db.hapus_relasi_penyakit_dan_gejala(id_komplikasi_penyakit_relasi, daftar_id_gejala_terpilih)
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
