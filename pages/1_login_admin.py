import streamlit as st
from assets import database as db
import time
import re

def validasi_email_regex(email):
    regex = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    
    return re.match(regex, email) is not None
if "logged_in_admin" not in st.session_state:
    st.session_state.logged_in_admin = False
    st.session_state.username = ""
    
if "alur_admin" not in st.session_state:
    st.session_state.alur_admin = 0


if st.session_state.alur_admin == 0:
    with st.form("login-admin"):
        if not st.session_state.logged_in_admin:
            st.title("Login Admin")
            
            # Input username dan password hanya terlihat jika belum login
            input_username = st.text_input("Masukkan username admin:")
            input_password = st.text_input("Masukkan password:", type="password")
            
            
            col1, col2, col3 = st.columns(3)
            
            berhasil_login = 0
            with col1:
                if st.form_submit_button(label="Login"):
                    # Validasi login
                    if db.check_admin(input_username, input_password) == True:
                        berhasil_login = 1
                        
                        
                    else:
                        berhasil_login = 2
                        
            if berhasil_login == 1:
                st.session_state.logged_in_admin = True
                st.session_state.masuk_website = "Admin"
                st.session_state.username = input_username
                st.success(f"Login berhasil! Selamat datang, {input_username}.")
                time.sleep(2)
                st.rerun()
                
            if berhasil_login == 2:
                st.error("Username atau password salah.")
            
                        
            with col3:
                if st.form_submit_button("Lupa Password"):
                    st.session_state.alur_admin = 1
                    st.rerun()
            
            
                    
if st.session_state.alur_admin == 1:
    with st.form("lupa-password-admin"):
        st.title("Lupa Password Admin")
        st.session_state.input_username_admin = st.text_input("Masukkan username Anda: ")
        st.session_state.input_email_admin = st.text_input("Masukkan email Anda:")
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
            st.error("Email tidak valid. Pastikan menggunakan format yang benar (@gmail.com)!")
        
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
        st.title("Reset Password Admin")
        input_password_baru = st.text_input("Masukkan password baru: ", type="password")
        input_password_baru_ulang = st.text_input("Ulangi password baru: ", type="password")
        if st.form_submit_button("Ganti Password"):
            if input_password_baru == input_password_baru_ulang:
                db.reset_password_admin(input_password_baru, st.session_state.input_username_admin, st.session_state.input_email_admin)
                st.success("Password Berhasil Diganti Dengan Password Baru")
                time.sleep(2)
                st.session_state.alur_admin = 0
                st.rerun()
            else:
                st.error("Password Baru dan Password Baru Ulang Tidak Sama!")
                
                
        
                                                  
            
            
                    
            
                

        
        

                

        
        


        


        
        
