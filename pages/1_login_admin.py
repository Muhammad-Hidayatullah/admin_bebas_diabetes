import streamlit as st
from assets import database as db
import time
import re
import datetime
from assets import fungsi_pemeriksaan

def validasi_password(password):
        return len(password) >= 7






def validasi_email_regex(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None
    
    return re.match(regex, email) is not None
if "logged_in_admin" not in st.session_state:
    st.session_state.logged_in_admin = False
    st.session_state.username = ""
    
if "alur_admin" not in st.session_state:
    st.session_state.alur_admin = 0


st.session_state.pekerjaan_pekerjaan = [
        "Dokter"
        ]

if st.session_state.alur_admin == 0:
    with st.form("login-admin"):
        if not st.session_state.logged_in_admin:
            st.title("Login Admin atau Dokter")
            
            # Input username dan password hanya terlihat jika belum login
            input_username = st.text_input("Masukkan username:", placeholder="username")
            input_password = st.text_input("Masukkan password:", type="password", placeholder="password")
            
            
            col1, col2, col3 = st.columns(3)
            
            berhasil_login = 0
            with col1:
                if st.form_submit_button(label="Login"):
                    # Validasi login
                    if db.check_admin(input_username, input_password) == True:
                        
                        
                        
                        berhasil_login = 1
                    
                    
                    elif db.check_dokter(input_username, input_password) == True:
                        id_pengguna, status, message = db.check_login_dokter(input_username, input_password)

                        if status:
                            berhasil_login = 2
                        else:
                            berhasil_login = 4

                        
                        
                    else:
                        berhasil_login = 3
                        
            if berhasil_login == 1:
                st.session_state.logged_in_admin = True
                st.session_state.masuk_website = "Admin"
                st.session_state.username = input_username
                st.success(f"Login berhasil! Selamat datang {input_username}!.")
                time.sleep(2)
                st.rerun()
                
            if berhasil_login == 2:
                st.session_state.logged_in_admin = True
                st.session_state.masuk_website = "Dokter"
                st.session_state.username = input_username
                st.success(f"Login berhasil! Selamat datang {input_username}!")
                time.sleep(2)
                st.rerun()
                
            if berhasil_login == 3:
                st.error("Username atau password salah.")
            
            if berhasil_login == 4:
                st.warning("Hubungi Admin untuk mengaktifkan akun Anda!")
                st.warning("Email: admbebasdiabetes123@gmail.com")
                st.warning("Kirimkan Username, Nama, Kualifikasi, Nomor Surat Tanda Registrasi, dan Nomor HP Anda dengan Subjek Email 'Validasi Akun Dokter'")
            

            
                        
            with col3:
                if st.form_submit_button("Lupa Password"):
                    st.session_state.alur_admin = 1
                    st.rerun()
            
            st.write("")
            st.write("")
            st.write("Apakah Anda Dokter dan Belum Punya Akun?")
            if st.form_submit_button("Sign Up Dokter"):
                st.session_state.alur_admin = 3
                st.rerun()
            
            
            
                    
if st.session_state.alur_admin == 1:
    with st.form("lupa-password-admin"):
        st.title("Lupa Password")
        st.session_state.input_username_admin = st.text_input("Masukkan username Anda: ", placeholder="Username")
        st.session_state.input_email_admin = st.text_input("Masukkan email Anda:", placeholder="Email")
        validitas_email = 0
        col1, col2, col3 = st.columns(3)
        
        
        with col1:
            if st.form_submit_button("Lanjut"):
                cek_username_email_admin = db.cek_lupa_password_admin(st.session_state.input_username_admin, st.session_state.input_email_admin )
                
                if not validasi_email_regex(st.session_state.input_email_admin):
                    validitas_email = 1
                   
                else:
                    validitas_email = 2
                    
        if validitas_email == 1:
            st.error("Email tidak valid. Pastikan menggunakan format yang benar (@gmail.com, @yahoo.co.id, dan lain-lain)!")
        
        if validitas_email == 2:
            if cek_username_email_admin == True:
                st.session_state.alur_admin = 2
                st.success("Username dan Email Admin Ditemukan")
                time.sleep(2)
                
                st.rerun()
            else:
                st.error("Username dan Email tersebut tidak ditemukan!")
                    
       
        st.write("")
        st.write("")
        st.write("Sudah Ingat Passwordnya?")
        if st.form_submit_button("Kembali"):
            st.session_state.alur_admin = 0
            st.rerun()
                
        
                    
        
        
                    
            
                    
if st.session_state.alur_admin == 2:
    with st.form("reset-password-admin"):
        st.title("Reset Password")
        input_password_baru = st.text_input("Masukkan password baru: ", type="password", placeholder="Passoword Baru")
        input_password_baru_ulang = st.text_input("Ulangi password baru: ", type="password", placeholder="Ulangi Password")
        if st.form_submit_button("Ganti Password"):
            if input_password_baru == input_password_baru_ulang:
                db.reset_password_admin(input_password_baru, st.session_state.input_username_admin, st.session_state.input_email_admin)
                st.success("Password Berhasil Diganti Dengan Password Baru")
                time.sleep(2)
                st.session_state.alur_admin = 0
                st.rerun()
            else:
                st.error("Password Baru dan Password Baru Ulang Tidak Sama!")
                
                

if st.session_state.alur_admin == 3:
    with st.form("signup-doter"):
        st.title("Registrasi")
        st.warning("Silahkan lakukan registrasi")
      
        username_pengguna = st.text_input("Masukkan username: ", placeholder="Username")
   
        password_pengguna = st.text_input("Masukkan password: ", type="password", placeholder="Password")
        
        nama = st.text_input("Nama Lengkap: ", placeholder="Nama Lengkap")
        
        jenis_kelamin = st.radio("Jenis Kelamin", ("LAKI-LAKI", "PEREMPUAN"))
        tanggal_lahir = st.date_input("Masukkan tanggal lahir: (y-m-d)", min_value=datetime.date(1900, 1, 1), max_value=datetime.datetime.now())
        
        
        pekerjaan = st.selectbox("Pekerjaan: ", options=st.session_state.pekerjaan_pekerjaan)
       
        
        
        email = st.text_input("Masukkan email: ", placeholder="Email")
        
        alamat = st.text_input("Alamat Tempat Tinggal: ", placeholder="Alamat")

        
        if st.form_submit_button(label="Registrasi"):
            cek_validasi_data_pengguna = db.check_data_registrasi_pengguna(username_pengguna, email, password_pengguna, nama, tanggal_lahir, alamat)
                
            if cek_validasi_data_pengguna == True:
                st.success("Berhasil melakukan registrasi.")
                enkripsi_password = db.enkripsi_password(password_pengguna)
                jenis_pengguna = "DOKTER"
                db.add_pengguna_dokter(db.menambah_id_pengguna_default(), username_pengguna, enkripsi_password, nama, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir, jenis_pengguna)
                time.sleep(2)
                st.session_state.alur_admin = 0
                st.rerun()
                
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        
        st.write("Sudah memiliki akun? Klik tombol Login di bawah ini!")
        if st.form_submit_button(label="Login"):
            st.session_state.alur_admin = 0
            st.rerun()
        
                                                  
            
            
                    
            
                

        
        

                

        
        


        


        
        
