import streamlit as st
from assets import database as db
import time

import pandas as pd
import re
import datetime

def validasi_email_regex(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def validasi_password(password):
    return len(password) >= 7

st.session_state.pekerjaan_pekerjaan = [
        "Dokter"
        ]


st.title("DAFTAR DOKTER")

st.subheader("Akun Dokter")


dokter_df = db.fetch_dokter()

pengguna_dokter_df = db.fetch_pengguna_dokter()



if pengguna_dokter_df is not None:
    pengguna_dokter_df_html = pengguna_dokter_df.to_html(index=False, escape=False)
    st.markdown(st.session_state.style_tabel + pengguna_dokter_df_html, unsafe_allow_html=True)
else:
    st.warning("Tabel Kosong")


kol_id_pengguna_dokter = pengguna_dokter_df["ID Pengguna"]


df_pengguna_dokter_terpakai = dokter_df["ID Pengguna"]
    
df_pengguna_dokter_tersisa = pengguna_dokter_df[~pengguna_dokter_df["ID Pengguna"].isin(df_pengguna_dokter_terpakai)]
kol_id_pengguna_dokter_tersisa = df_pengguna_dokter_tersisa["ID Pengguna"]

st.subheader("Validasi Dokter")
if dokter_df is not None:
    dokter_df_html = dokter_df.to_html(index=False, escape=False)
    st.markdown(st.session_state.style_tabel + dokter_df_html, unsafe_allow_html=True)
else:
    st.warning("Tabel Kosong")




pilihan = st.radio("Pilih yang ingin Anda Kelola: ", ("Akun Dokter", "Validasi Dokter"), horizontal=True)


if pilihan == "Akun Dokter":
    
    pilihan_dokter = st.radio("Pilih Opsi untuk Kelola Akun Dokter", ("Tambah Dokter", "Update Dokter", "Hapus Dokter"), horizontal=True)

    if pilihan_dokter == "Tambah Dokter":
        st.subheader("Tambah Dokter")
        username_pengguna = st.text_input("Masukkan username: ", placeholder="Username")
   
        password_pengguna = st.text_input("Masukkan password: ", type="password", placeholder="Password")
        
        nama = st.text_input("Nama Lengkap: ", placeholder="Nama Lengkap")
        
        jenis_kelamin = st.radio("Jenis Kelamin", ("LAKI-LAKI", "PEREMPUAN"))
        tanggal_lahir = st.date_input("Masukkan tanggal lahir: (y-m-d)", min_value=datetime.date(1900, 1, 1), max_value=datetime.datetime.now())
        
        
        pekerjaan = st.selectbox("Pekerjaan: ", options=st.session_state.pekerjaan_pekerjaan)
       
        
        
        email = st.text_input("Masukkan email: ", placeholder="Email")
        
        alamat = st.text_input("Alamat Tempat Tinggal: ", placeholder="Alamat")



        if st.button(label="Tambah"):
            cek_validasi_data_pengguna = db.check_data_registrasi_pengguna(username_pengguna, email, password_pengguna, nama, tanggal_lahir, alamat)
                
            if cek_validasi_data_pengguna == True:
                st.success("Berhasil menambahkan akun dokter!")
                enkripsi_password = db.enkripsi_password(password_pengguna)
                jenis_pengguna = "DOKTER"
                db.add_pengguna_dokter(db.menambah_id_pengguna_default(), username_pengguna, enkripsi_password, nama, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir, jenis_pengguna)
                time.sleep(2)
                st.session_state.alur_admin = 0
                st.rerun()
                

    if pilihan_dokter == "Update Dokter":
        st.subheader("Update Dokter")
        id_pengguna_dokter = st.selectbox("Pilih ID Pengguna Dokter: ", options=pengguna_dokter_df["ID Pengguna"], index=0)
        
        
        username_default = pengguna_dokter_df.loc[pengguna_dokter_df["ID Pengguna"] == id_pengguna_dokter, "Username"].values[0]
        username = st.text_input("Masukkan username baru: ", value=username_default)
        
        password_default = pengguna_dokter_df.loc[pengguna_dokter_df["ID Pengguna"] == id_pengguna_dokter, "Password"].values[0]
        password = st.text_input("Masukkan password baru: ", type= "password", value=db.dekripsi_password(password_default))
        
        nama_default = pengguna_dokter_df.loc[pengguna_dokter_df["ID Pengguna"] == id_pengguna_dokter, "Nama Pengguna"].values[0]
        nama = st.text_input("Masukkan nama lengkap baru: ", value=nama_default)
        
        jenis_kelamin_default = pengguna_dokter_df.loc[pengguna_dokter_df["ID Pengguna"] == id_pengguna_dokter, "Jenis Kelamin"].values[0]
        jenis_kelamin = st.radio("Jenis Kelamin: ", ("LAKI-LAKI", "PEREMPUAN"), horizontal=True, index=("LAKI-LAKI", "PEREMPUAN").index(jenis_kelamin_default))
        
        
        alamat_default = pengguna_dokter_df.loc[pengguna_dokter_df["ID Pengguna"] == id_pengguna_dokter, "Alamat"].values[0]
        alamat = st.text_input("Masukkan alamat baru: ", value=alamat_default)
        
        email_default = pengguna_dokter_df.loc[pengguna_dokter_df["ID Pengguna"] == id_pengguna_dokter, "Email"].values[0]
        email = st.text_input("Masukkan email baru: ", value=email_default)
        
        pekerjaan_default = pengguna_dokter_df.loc[pengguna_dokter_df["ID Pengguna"] == id_pengguna_dokter, "Pekerjaan"].values[0]
        pekerjaan = st.selectbox("Masukkan pekerjaan baru: ", options=st.session_state.pekerjaan_pekerjaan, index=st.session_state.pekerjaan_pekerjaan.index(pekerjaan_default)) 
        
        
        tanggal_lahir_default = pengguna_dokter_df.loc[pengguna_dokter_df["ID Pengguna"] == id_pengguna_dokter, "Tanggal Lahir"].values[0]
        tanggal_lahir = st.date_input("Masukkan tanggal lahir: (y-m-d)", min_value=datetime.date(1900, 1, 1), max_value=datetime.datetime.now(), value=tanggal_lahir_default)

        update = 0
        cek_update_data_pengguna = False
        
        if st.button(label="Update"):
            update = 1
        if update == 1:
            cek_update_data_pengguna = db.check_update_data_pengguna(username, password, nama, email, tanggal_lahir, alamat)
           
            
        if cek_update_data_pengguna == True and update == 1:
            enkripsi_password = db.enkripsi_password(password)
            db.update_pengguna(username, enkripsi_password, nama, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir, st.session_state.username)
            st.success("Update Data Anda Berhasil!.")
            
            st.session_state.username = username
            st.session_state.lanjut = 0
            st.session_state.lanjut_pemeriksaan = 0
            time.sleep(2)
            st.rerun()
    
    if pilihan_dokter == "Hapus Dokter":
        st.subheader("Hapus Akun Dokter")
        if "konfirmasi_hapus_akun_dokter" not in st.session_state:
            st.session_state.konfirmasi_hapus_akun_dokter = 0
      
        id_pengguna_dokter = st.selectbox("Pilih ID Pengguna: ", options=pengguna_dokter_df["ID Pengguna"], index=0)
        
        if st.button("Hapus"):
            st.session_state.konfirmasi_hapus_akun_dokter = 1
        if st.session_state.konfirmasi_hapus_akun_dokter == 1:
            st.warning("Apakah Anda yakin ingin menghapus akun dokter tersebut?")
            if st.button("Ya"):
                st.session_state.konfirmasi_hapus_akun_dokter = 2
        if st.session_state.konfirmasi_hapus_akun_dokter == 2:
            hapus_data_pengguna = db.hapus_data_pengguna_dokter(id_pengguna_dokter)
            st.success("Berhasil Hapus Akun Dokter!")
            st.session_state.konfirmasi_hapus_akun_dokter = 0
            time.sleep(2)
            st.rerun()
        
        
        





if pilihan == "Validasi Dokter":

    pilihan_dokter = st.radio("Pilih Opsi untuk Validasi Dokter", ("Tambah Validasi Dokter", "Update Validasi Dokter", "Hapus Validasi Dokter"), horizontal=True)

    if pilihan_dokter == "Tambah Validasi Dokter":
        
        
        st.subheader("Tambah Dokter")
        id_dokter = st.text_input("Masukkan kode dokter: ", db.menambah_id_dokter_default())
        nama_dokter = st.text_input("Masukkan nama dokter: ")
        kualifikasi = st.text_input("Masukkan kualifikasi dokter: ")
        surat_tanda_registrasi = st.text_input("Masukkan STR (Surat Tanda Registrasi): ")
        
        
        no_hp = st.text_input("Masukkan nomor HP: ")
        
        kol_id_pengguna_dokter_tersisa = pd.concat([pd.Series([None], name='id_pengguna'), kol_id_pengguna_dokter_tersisa], ignore_index=True)


        
        
        id_pengguna_dokter = st.selectbox("Pilih ID Pengguna dokter:", options=kol_id_pengguna_dokter_tersisa, index=0)

        
        

        if st.button("Tambah"):
            db.add_dokter(id_dokter, nama_dokter, kualifikasi, surat_tanda_registrasi, no_hp, id_pengguna_dokter)
            time.sleep(2)
            st.rerun()


    if pilihan_dokter == "Update Validasi Dokter":
        st.subheader("Update Dokter")
        
        kol_id_dokter = dokter_df["ID Dokter"]
        
        id_dokter =st.selectbox("Masukkan kode dokter: ", options=kol_id_dokter, index=0)
        
    
        
        nama_dokter_default = dokter_df.loc[dokter_df["ID Dokter"] == id_dokter, "Nama Dokter"].values[0]
        nama_dokter = st.text_input("Masukkan nama dokter baru: ", nama_dokter_default)
        
        kualifikasi_default = dokter_df.loc[dokter_df["ID Dokter"] == id_dokter, "Kualifikasi"].values[0]
        kualifikasi = st.text_input("Masukkan kualifikasi baru: ", kualifikasi_default)
        
        
        str_default = dokter_df.loc[dokter_df["ID Dokter"] == id_dokter, "Nomor STR"].values[0]
        no_str = st.text_input("Masukkan STR baru: ", str_default)
        
        no_hp_default = dokter_df.loc[dokter_df["ID Dokter"] == id_dokter, "Nomor HP"].values[0]
        no_hp = st.text_input("Masukkan nomor HP baru: ", no_hp_default)
        
        
        
        kol_id_pengguna_dokter_tersisa = pd.concat([pd.Series([None], name='id_pengguna'), kol_id_pengguna_dokter_tersisa], ignore_index=True)
        id_pengguna_dokter = st.selectbox("Pilih ID Pengguna dokter:", options=kol_id_pengguna_dokter_tersisa, index=0)
        
        
        
        
        
        if st.button("Update"):
            db.update_dokter(id_dokter, nama_dokter, kualifikasi, no_str, no_hp, id_pengguna_dokter)
            time.sleep(2)
            st.rerun()
            

    if pilihan_dokter == "Hapus Validasi Dokter":
        st.subheader("Hapus Dokter")
        if "konfirmasi_hapus_dokter" not in st.session_state:
            st.session_state.konfirmasi_hapus_dokter = 0
            
        
        
        kol_id_dokter = dokter_df["ID Dokter"]
        
        id_dokter =st.selectbox("Masukkan kode dokter yang ingin dihapus: ", options=kol_id_dokter, index=0)
        
        
        if st.button("Hapus"):
            st.session_state.konfirmasi_hapus_dokter = 1
            
        if st.session_state.konfirmasi_hapus_dokter == 1:
            st.warning("Apakah Anda yakin ingin menghapus data dokter tersebut?")
            if st.button("Ya"):
                st.session_state.konfirmasi_hapus_dokter = 2
        
        if st.session_state.konfirmasi_hapus_dokter == 2:
    
            st.session_state.konfirmasi_hapus_dokter = 0
            db.hapus_dokter(id_dokter)
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
