import streamlit as st
from assets import database as db
import datetime

import time

import re
from assets import fungsi_pemeriksaan

def validasi_email_regex(email):
    regex = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(regex, email) is not None



def validasi_password(password):
    return len(password) >= 7  # Minimum length of 6 characters


if "lanjut" not in st.session_state:
    st.session_state.lanjut = 0
    
    
    
def data_pengguna():
    st.session_state.kode_pengguna = ""
    st.session_state.username_pengguna = ""
    st.session_state.password_pengguna = ""
    st.session_state.nama_lengkap = ""
    st.session_state.jenis_kelamin = ""
    st.session_state.alamat = ""
    st.session_state.email = ""
    st.session_state.pekerjaan = ""
    st.session_state.tanggal_lahir = ""

if st.session_state.lanjut == 0:
    with st.form("form_data_pengguna"):
        
        data_pengguna()
        if "data_pengguna" not in st.session_state:
            st.session_state.data_pengguna = []
        
        
        st.session_state.data_pengguna = db.get_data_pengguna(st.session_state.username_pengguna)
        
        # Mengambil data dari database
        st.session_state.kode_pengguna = st.session_state.data_pengguna[0]
        st.session_state.username_pengguna = st.session_state.data_pengguna[1]
        st.session_state.password_pengguna = db.dekripsi_password(st.session_state.data_pengguna[2])
        st.session_state.nama_lengkap = st.session_state.data_pengguna[3]
        st.session_state.jenis_kelamin = st.session_state.data_pengguna[4]
        st.session_state.alamat = st.session_state.data_pengguna[5]
        st.session_state.email = st.session_state.data_pengguna[6]
        st.session_state.pekerjaan = st.session_state.data_pengguna[7]
        st.session_state.tanggal_lahir = st.session_state.data_pengguna[8]
        
        
        
        st.title("Data Profil")        
        st.write("Kode pengguna       : " + st.session_state.kode_pengguna)
        st.write("Username          : " + st.session_state.username_pengguna)
        st.write("Password          : " + len(st.session_state.password_pengguna) * "*")
        st.write("Nama Lengkap      : " + st.session_state.nama_lengkap)
        st.write("Jenis Kelamin     : " + st.session_state.jenis_kelamin)
        st.write("Alamat            : " + st.session_state.alamat)
        st.write("Email             : " + st.session_state.email)
        st.write("Pekerjaan         : " + st.session_state.pekerjaan)
        st.write("Tanggal Lahir     : " + str(st.session_state.tanggal_lahir))


        if "update_data" not in st.session_state:
            st.session_state.update_data = 0

        st.write("")
        st.write("")

        
                
        if st.form_submit_button("Update"):
            st.session_state.lanjut = 2
            st.session_state.update_data = 0
            st.rerun()
            

if st.session_state.lanjut == 2:
    update_data_berhasil = False
    with st.form("form-update-data-pengguna"):
        st.title("Update Data pengguna")
        st.warning("Apabila ada nilai yang tidak ingin diubah, jangan diganti!")
        username = st.text_input("Masukkan username baru: ", value=st.session_state.username_pengguna)
        password = st.text_input("Masukkan password baru: ", type= "password", value=st.session_state.password_pengguna)
        nama = st.text_input("Masukkan nama lengkap baru: ", value=st.session_state.nama_lengkap)
        jenis_kelamin = st.radio("Jenis Kelamin: ", ("LAKI-LAKI", "PEREMPUAN"), horizontal=True, index=("LAKI-LAKI", "PEREMPUAN").index(st.session_state.jenis_kelamin))
        alamat = st.text_input("Masukkan alamat baru: ", value=st.session_state.alamat)
        email = st.text_input("Masukkan email baru: ", value=st.session_state.email)
        

        pekerjaan = st.selectbox("Masukkan pekerjaan baru: ", options=st.session_state.pekerjaan_pekerjaan, index=st.session_state.pekerjaan_pekerjaan.index(st.session_state.pekerjaan)) 
        
        tanggal_lahir = st.date_input("Masukkan tanggal lahir: (y-m-d)", min_value=datetime.date(1900, 1, 1), max_value=datetime.datetime.now(), value=st.session_state.tanggal_lahir)
        
        
        col1, col2 = st.columns(2)
        validation_errors = False
        update = 0
       
        cek_update_data_pengguna = False
        with col1:
            if st.form_submit_button(label="Kembali"):
                st.session_state.lanjut = 0
                st.rerun()
                
        with col2:
            update_data_berhasil = False
            if st.form_submit_button(label="Update"):
                update = 1
                
        
        if update == 1:
            cek_update_data_pengguna = db.check_update_data_pengguna(username, password, nama, email, tanggal_lahir, alamat)
           
            
        if cek_update_data_pengguna == True and update == 1:
            enkripsi_password = db.enkripsi_password(password)
            db.update_pengguna(username, enkripsi_password, nama, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir, st.session_state.username_pengguna)
            st.success("Update Data Anda Berhasil!.")
            fungsi_pemeriksaan.awal_pemeriksaan()
            st.session_state.username_pengguna = username
            st.session_state.lanjut = 0
            st.session_state.lanjut_pemeriksaan = 0
            time.sleep(2)
            st.rerun()
        
    
