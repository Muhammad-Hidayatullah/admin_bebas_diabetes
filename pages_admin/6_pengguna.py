import streamlit as st
from assets import database as db
import time
import datetime
import re
import pandas as pd
from fpdf import FPDF
from assets import format_laporan as fl

st.title("PENGGUNA")
df_pengguna = db.fetch_pengguna()
if df_pengguna is not None:
    df_pengguna_html = df_pengguna.to_html(index=False, escape=False)
    st.markdown(st.session_state.style_tabel + df_pengguna_html, unsafe_allow_html=True)



    st.session_state.pekerjaan_pekerjaan = [
        "Belum / Tidak Bekerja",
        "Mengurus Rumah Tangga",
        "Pelajar / Mahasiswa",
        "Pensiunan",
        "Pegawai Negeri Sipil",
        "Tentara Nasional Indonesia",
        "Kepolisian RI",
        "Perdagangan",
        "Petani / Pekebun",
        "Peternak",
        "Nelayan / Perikanan",
        "Industri",
        "Konstruksi",
        "Transportasi",
        "Karyawan Swasta",
        "Karyawan BUMN",
        "Karyawan BUMD",
        "Karyawan Honorer",
        "Buruh Harian Lepas",
        "Buruh Tani / Perkebunan",
        "Buruh Nelayan / Perikanan",
        "Buruh Peternakan",
        "Pembantu Rumah Tangga",
        "Tukang Cukur",
        "Tukang Listrik",
        "Tukang Batu",
        "Tukang Kayu",
        "Tukang Sol Sepatu",
        "Tukang Las / Pandai Besi",
        "Tukang Jahit",
        "Penata Rambut",
        "Penata Rias",
        "Penata Busana",
        "Mekanik",
        "Tukang Gigi",
        "Seniman",
        "Tabib",
        "Paraji",
        "Perancang Busana",
        "Penterjemah",
        "Imam Masjid",
        "Pendeta",
        "Pastur",
        "Wartawan",
        "Ustadz / Mubaligh",
        "Juru Masak",
        "Promotor Acara",
        "Anggota DPR-RI",
        "Anggota DPD",
        "Anggota BPK",
        "Presiden",
        "Wakil Presiden",
        "Anggota Mahkamah Konstitusi",
        "Anggota Kabinet / Kementerian",
        "Duta Besar",
        "Gubernur",
        "Wakil Gubernur",
        "Bupati",
        "Wakil Bupati",
        "Walikota",
        "Wakil Walikota",
        "Anggota DPRD Propinsi",
        "Anggota DPRD Kabupaten / Kota",
        "Dosen",
        "Guru",
        "Pilot",
        "Pengacara",
        "Notaris",
        "Arsitek",
        "Akuntan",
        "Konsultan",
        "Dokter",
        "Bidan",
        "Perawat",
        "Apoteker",
        "Psikiater / Psikolog",
        "Penyiar Televisi",
        "Penyiar Radio",
        "Pelaut",
        "Peneliti",
        "Sopir",
        "Pialang",
        "Paranormal",
        "Pedagang",
        "Perangkat Desa",
        "Kepala Desa",
        "Biarawati",
        "Wiraswasta",
        "Anggota Lembaga Tinggi",
        "Artis",
        "Atlit",
        "Cheff",
        "Manajer",
        "Tenaga Tata Usaha",
        "Operator",
        "Pekerja Pengolahan", 
        "Kerajinan",
        "Teknisi",
        "Asisten Ahli",
        "Lainnya"
        ]

    def validasi_password(password):
        return len(password) >= 7

    def validasi_email_regex(email):
        regex = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
        return re.match(regex, email) is not None


    pilihan_pengguna = st.radio("Pilih Opsi untuk Kelola Pengguna", ("Tambah Pengguna", "Update Pengguna", "Hapus Pengguna"), horizontal=True)
    if pilihan_pengguna == "Tambah Pengguna":
        st.subheader("Tambah Pengguna")
        username_pengguna = st.text_input("Masukkan username: ")
        password_pengguna = st.text_input("Masukkan password: ", type="password")
        nama = st.text_input("Nama Lengkap: ")
        jenis_kelamin = st.radio("Jenis Kelamin", ("LAKI-LAKI", "PEREMPUAN"))
        tanggal_lahir = st.date_input("Masukkan tanggal lahir: (y-m-d)", min_value=datetime.date(1900, 1, 1), max_value=datetime.datetime.now())
        
        
        pekerjaan = st.selectbox("Pekerjaan: ", options=st.session_state.pekerjaan_pekerjaan)
        if pekerjaan == "Lainnya":
            pekerjaan_lainnya = st.text_input("Pekerjaan: ")
            pekerjaan = pekerjaan_lainnya
        
        
        email = st.text_input("Masukkan email: ")
        alamat = st.text_input("Alamat Tempat Tinggal: ")

        
        if st.button(label="Tambah Pengguna"):
            
            cek_validasi_data_pengguna = db.check_data_registrasi_pengguna(username_pengguna, email, password_pengguna, nama, tanggal_lahir, alamat)
            
            if cek_validasi_data_pengguna == True:
                enkripsi_password = db.enkripsi_password(password_pengguna)
                st.success("Data valid.")
                db.add_pengguna(db.menambah_id_pengguna_default(), username_pengguna, enkripsi_password, nama, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir)
                time.sleep(2)
                st.rerun()
            
    if pilihan_pengguna == "Update Pengguna":
        st.subheader("Update Pengguna")
        id_pengguna = st.selectbox("Pilih ID Pengguna: ", options=df_pengguna["ID Pengguna"], index=0)
        
        username_default = df_pengguna.loc[df_pengguna["ID Pengguna"] == id_pengguna, "Username"].values[0]
        username = st.text_input("Masukkan username baru: ", value=username_default)
        
        password_default = df_pengguna.loc[df_pengguna["ID Pengguna"] == id_pengguna, "Password"].values[0]
        password = st.text_input("Masukkan password baru: ", type= "password", value=db.dekripsi_password(password_default))
        
        nama_default = df_pengguna.loc[df_pengguna["ID Pengguna"] == id_pengguna, "Nama Pengguna"].values[0]
        nama = st.text_input("Masukkan nama lengkap baru: ", value=nama_default)
        
        jenis_kelamin_default = df_pengguna.loc[df_pengguna["ID Pengguna"] == id_pengguna, "Jenis Kelamin"].values[0]
        jenis_kelamin = st.radio("Jenis Kelamin: ", ("LAKI-LAKI", "PEREMPUAN"), horizontal=True, index=("LAKI-LAKI", "PEREMPUAN").index(jenis_kelamin_default))
        
        
        alamat_default = df_pengguna.loc[df_pengguna["ID Pengguna"] == id_pengguna, "Alamat"].values[0]
        alamat = st.text_input("Masukkan alamat baru: ", value=alamat_default)
        
        email_default = df_pengguna.loc[df_pengguna["ID Pengguna"] == id_pengguna, "Email"].values[0]
        email = st.text_input("Masukkan email baru: ", value=email_default)
        
        pekerjaan_default = df_pengguna.loc[df_pengguna["ID Pengguna"] == id_pengguna, "Pekerjaan"].values[0]
        pekerjaan = st.selectbox("Masukkan pekerjaan baru: ", options=st.session_state.pekerjaan_pekerjaan, index=st.session_state.pekerjaan_pekerjaan.index(pekerjaan_default)) 
        if pekerjaan == "Lainnya":
            pekerjaan_lainnya = st.text_input("Masukkan pekerjaan baru: ")
            pekerjaan = pekerjaan_lainnya
        
        tanggal_lahir_default = df_pengguna.loc[df_pengguna["ID Pengguna"] == id_pengguna, "Tanggal Lahir"].values[0]
        tanggal_lahir = st.date_input("Masukkan tanggal lahir: (y-m-d)", min_value=datetime.date(1900, 1, 1), max_value=datetime.datetime.now(), value=tanggal_lahir_default)

        if st.button("Update"):
            cek_update_data_pengguna = db.check_update_data_pengguna(username, password, nama, email, tanggal_lahir, alamat)
        
            if cek_update_data_pengguna == True:
                st.success("Update Data Berhasil.")
                enkripsi_password = db.enkripsi_password(password)
                db.update_pengguna(username, enkripsi_password, nama, jenis_kelamin, alamat, email, pekerjaan, tanggal_lahir, username_default)
                time.sleep(2)
                st.rerun()
                
    if pilihan_pengguna == "Hapus Pengguna":
        if "konfirmasi_hapus" not in st.session_state:
            st.session_state.konfirmasi_hapus = 0
        st.subheader("Hapus Pengguna")
        id_pengguna = st.selectbox("Pilih ID Pengguna: ", options=df_pengguna["ID Pengguna"], index=0)
        
        if st.button("Hapus"):
            st.session_state.konfirmasi_hapus = 1
        if st.session_state.konfirmasi_hapus == 1:
            st.warning("Apakah Anda yakin ingin menghapus pengguna tersebut? Semua data terkait pengguna tersebut akan terhapus!")
            if st.button("Ya"):
                st.session_state.konfirmasi_hapus = 2
        if st.session_state.konfirmasi_hapus == 2:
            hapus_data_pengguna = db.hapus_data_pengguna(id_pengguna)
            st.success("Berhasil Hapus Data Pengguna")
            st.session_state.konfirmasi_hapus = 0
            time.sleep(2)
            st.rerun()
        

else:
    st.write("--")


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

