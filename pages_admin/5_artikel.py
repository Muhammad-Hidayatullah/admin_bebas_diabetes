import streamlit as st
from assets import database as db
import time

st.title("ARTIKEL")
st.cache_data()
df_artikel = db.fetch_artikel()

df_artikel_html = df_artikel.to_html(index=False, escape=False)
st.markdown(st.session_state.style_tabel + df_artikel_html, unsafe_allow_html=True)



pilihan_artikel = st.radio("Pilih Opsi untuk Kelola Artikel: ", ("Tambah Artikel", "Update Artikel", "Hapus Artikel"), horizontal=True)
if pilihan_artikel == "Tambah Artikel":
    st.subheader("Tambah Artikel")
    nama_website = st.text_input("Masukkan nama website: ")
    link_gambar = st.text_input("Masukkan link gambar: ")
    judul_artikel = st.text_input("Masukkan judul artikel: ")
    nama_penulis = st.text_input("Masukkan nama penulis: ")
    tanggal_artikel = st.date_input("Masukkan tanggal artikel dibuat: ")
    link_artikel = st.text_input("Masukkan link artikel di sini: ")
    if st.button("Tambah Artikel"):
        db.add_artikel(nama_website, link_gambar, judul_artikel, nama_penulis, tanggal_artikel, link_artikel, db.get_id_pengguna_milik_admin(st.session_state.username))
        st.success("Artikel Berhasil Ditambahkan")
        time.sleep(2)
        st.rerun()
if pilihan_artikel == "Update Artikel":
    st.subheader("Update Artikel")
    id_artikel = st.selectbox("Pilih id artikel: ", options=df_artikel["ID Artikel"], index=0)
    
    nama_website_default = df_artikel.loc[df_artikel["ID Artikel"] == id_artikel, "Nama Website"].values[0]
    nama_website = st.text_input("Masukkan nama website baru: ", nama_website_default)
    
    link_gambar_default = df_artikel.loc[df_artikel["ID Artikel"] == id_artikel, "Link Gambar"].values[0]
    link_gambar = st.text_input("Masukkan link gambar baru: ", link_gambar_default)
    
    judul_artikel_default = df_artikel.loc[df_artikel["ID Artikel"] == id_artikel, "Judul Artikel"].values[0]
    judul_artikel = st.text_input("Masukkan judul artikel baru: ", link_gambar_default)
    
    
    nama_penulis_default = df_artikel.loc[df_artikel["ID Artikel"] == id_artikel, "Nama Penulis"].values[0]
    nama_penulis = st.text_input("Masukkan nama penulis baru: ", nama_penulis_default)
    
    tanggal_artikel_default = df_artikel.loc[df_artikel["ID Artikel"] == id_artikel, "Tanggal Artikel"].values[0]
    tanggal_artikel = st.date_input("Masukkan tanggal artikel baru: ", tanggal_artikel_default)
    
    link_artikel_default = df_artikel.loc[df_artikel["ID Artikel"] == id_artikel, "Link Artikel"].values[0]
    link_artikel = st.text_input("Masukkan link artikel baru: ", link_artikel_default)
    
    if st.button("Update Artikel"):
        db.update_artikel(nama_website, link_gambar, judul_artikel, nama_penulis, tanggal_artikel, link_artikel, db.get_id_pengguna_milik_admin(st.session_state.username), id_artikel)
        st.success("Berhasil Update Artikel!")
        time.sleep(2)
        st.rerun()

if pilihan_artikel == "Hapus Artikel":
    st.subheader("Hapus Artikel")
    if "konfirmasi_hapus_artikel" not in st.session_state:
        st.session_state.konfirmasi_hapus_artikel = 0
        
    id_artikel = st.selectbox("Masukkan ID artikel yang ingin dihapus: ", options=df_artikel["ID Artikel"], index=0)
    
    if st.button("Hapus Artikel"):
        st.session_state.konfirmasi_hapus_artikel = 1
    
    if st.session_state.konfirmasi_hapus_artikel == 1:
        st.warning("Apakah Anda yakin ingin menghapus artikel tersebut?")
        if st.button("Ya"):
            st.session_state.konfirmasi_hapus_artikel = 2
    if st.session_state.konfirmasi_hapus_artikel == 2:
        db.hapus_artikel(id_artikel)
        st.session_state.konfirmasi_hapus_artikel = 0
        st.success("Artikel Berhasil Dihapus")
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
