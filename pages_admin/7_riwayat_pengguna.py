import streamlit as st
from assets import database as db
import time
from assets import format_laporan as fl


df_pengguna = db.fetch_pengguna()
st.title("RIWAYAT PENGGUNA")

st.subheader("DATA PEMERIKSAAN KESEHATAN")
df_pemeriksaan_kesehatan = db.fetch_pemeriksaan_kesehatan()
if df_pemeriksaan_kesehatan is not None:
    lihat_df_pemeriksaan_kesehatan_html = df_pemeriksaan_kesehatan.to_html(index=False, escape=False)
    st.markdown(st.session_state.style_tabel + lihat_df_pemeriksaan_kesehatan_html, unsafe_allow_html=True)
else:
    st.write("Tidak ada data")
 


st.subheader("DIAGNOSIS PENYAKIT")
df_diagnosis_penyakit = db.fetch_diagnosis_penyakit_admin()

if "page_number" not in st.session_state:
    st.session_state.page_number = 0






if df_diagnosis_penyakit is not None:
    lihat_df_diagnosis_penyakit = df_diagnosis_penyakit.copy()

    baris_per_halaman = st.selectbox("Tampilkan baris halaman", [5, 10, 20, 50], index=0)

    total_halaman = (len(df_diagnosis_penyakit) - 1) // baris_per_halaman + 1
    start_index = st.session_state.page_number * total_halaman
    end_index = start_index + baris_per_halaman
    lihat_df_diagnosis_penyakit = df_diagnosis_penyakit.iloc[start_index:end_index]

    #Menunjukkan tabel
    df_diagnosis_penyakit_html = lihat_df_diagnosis_penyakit.to_html(index=False, escape=False)
    st.markdown(df_diagnosis_penyakit_html, unsafe_allow_html=True)
    
    # Show current page info
    st.write(f"Halaman {st.session_state.page_number + 1} dari {total_halaman}")
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.session_state.page_number > 0:
            if st.button("⬅️ Mundur"):
                st.session_state.page_number -= 1
                st.rerun()

    with col3:
        if st.session_state.page_number < total_halaman - 1:
            if st.button("Lanjut ➡️"):
                st.session_state.page_number += 1
                st.rerun()
else:
    st.write("Tidak ada data")

# Show table with selected number of rows



if df_pemeriksaan_kesehatan is not None and df_diagnosis_penyakit is not None:
   

    pilihan = st.radio("Pilih Opsi untuk Riwayat Pengguna", ("Unduh Hasil", "Hapus Hasil"), horizontal=True)
    
    if pilihan == "Unduh Hasil":
        st.subheader("Unduh Hasil")
    else:
        st.subheader("Hapus Hasil")
    
    id_pengguna = st.selectbox("Pilih ID Pengguna", options=sorted(df_pemeriksaan_kesehatan["ID Pengguna"].unique()), index=0)
    tanggal = st.selectbox("Pilih tanggal", options=df_pemeriksaan_kesehatan.loc[df_pemeriksaan_kesehatan["ID Pengguna"] == id_pengguna, "Tanggal Pemeriksaan"], index=0)

    df_pengguna_tertentu = df_pengguna[df_pengguna["ID Pengguna"] == id_pengguna]

    df_pemeriksaan_kesehatan_pengguna_tertentu = df_pemeriksaan_kesehatan[(df_pemeriksaan_kesehatan["ID Pengguna"] == id_pengguna) & (df_pemeriksaan_kesehatan["Tanggal Pemeriksaan"] == tanggal)]

    df_diagnosis_penyakit_tertentu = df_diagnosis_penyakit[(df_diagnosis_penyakit["ID Pengguna"] == id_pengguna) & (df_diagnosis_penyakit["Tanggal Diagnosis"] == tanggal)]


    if pilihan == "Unduh Hasil":
        
        if not df_diagnosis_penyakit_tertentu.empty:
            row = df_pengguna_tertentu.iloc[0]
            username = row["Username"]
            nama_pengguna = row["Nama Pengguna"]
            jenis_kelamin = row["Jenis Kelamin"]
            alamat = row["Alamat"]
            email = row["Email"]
            pekerjaan = row["Pekerjaan"]
            tanggal_lahir = row["Tanggal Lahir"]
            
            
        
        
        
        if not df_pemeriksaan_kesehatan_pengguna_tertentu.empty:
        
            row = df_pemeriksaan_kesehatan_pengguna_tertentu.iloc[0]  # Get first row safely
            tingkat_gula_darah = row["Tingkat Gula Darah"]
            usia_di_atas_40_tahun = row["Usia di Atas 40 Tahun"]
            riwayat_keluarga_diabetes = row["Riwayat Keluarga Diabetes"]
            riwayat_diabetes_gestasional = row["Riwayat Diabetes Gestasional"]
            riwayat_lahir_di_bawah_2_koma_5_gram = row["Riwayat Lahir Berat Badan Lahir Rendah"]
            riwayat_sindrom_ovariaum_polikistik = row["Riwayat Sindrom Ovariaum Polikistik"]
            riwayat_penyakit_kardiovaskular = row["Riwayat Penyakit Kardiovaskular"]
            konsumsi_alkohol = row["Konsumsi Alkohol"]
            kurang_aktivitas = row["Kurang Aktivitas"]
            merokok = row["Merokok"]
            pola_makan_buruk = row["Pola Makan Buruk"]
            kurang_tidur = row["Kurang Tidur"]
            tinggi_badan = str(row["Tinggi Badan"])
            berat_badan = str(row["Berat Badan"])
            lingkar_perut = str(row["Lingkar Perut"])
            indeks_massa_tubuh = str(row["Indeks Massa Tubuh"])
            tekanan_darah = str(row["Tekanan Darah"])
            gula_darah_sewaktu = str(row["Gula Darah Sewaktu"])
            gula_darah_puasa = str(row["Gula Darah Puasa"])
            gula_darah_2_jam_setelah_makan = str(row["Gula Darah 2 Jam Setelah Makan"])
            HDL = str(row["HDL"])
            LDL = str(row["LDL"])
            trigliserida = str(row["Trigliserida"])
            total_kolestrol = str(row["Total Kolestrol"])
                        
            
        else:
            st.write("Tidak ada data untuk tanggal yang dipilih.")
            
        df_diagnosis_penyakit_tertentu = df_diagnosis_penyakit.loc[df_diagnosis_penyakit["Tanggal Diagnosis"] == tanggal]



        row = df_diagnosis_penyakit_tertentu.head(1)
        nama_pengguna_terpilih = row["Nama Pengguna"].iloc[0]
        
        gejala_digabung = set()
        import pandas as pd
        
        for row in df_diagnosis_penyakit_tertentu['Gejala Cocok']:
            
            if pd.isna(row):
                continue
            
            if row is not None:
                gejala_digabung.update(row.split("; "))
            else:
                gejala_digabung = None
            
            
        if not gejala_digabung:
            gejala_digabung = None
        
        
            
        gejala_terpilih = gejala_digabung
        diagnosis_penyakit_tertentu = df_diagnosis_penyakit_tertentu.iloc[:, 3:]



        #diagnosis_penyakit_tertentu = diagnosis_penyakit_tertentu.drop("Gejala Terpilih", axis=1)

        #Relasi Penyakit dan Gejala
        data_relasi = db.fetch_relasi_nama_penyakit_dan_nama_gejala()
        relasi_penyakit_dan_gejala = {}
        for penyakit, gejala in data_relasi:
            if penyakit not in relasi_penyakit_dan_gejala:
                relasi_penyakit_dan_gejala[penyakit] = []  # Buat list kosong jika penyakit belum ada
            relasi_penyakit_dan_gejala[penyakit].append(gejala) 

        

        if st.button("Unduh Laporan"):
            file_pdf = fl.buat_laporan_riwayat(id_pengguna, nama_pengguna, username, tanggal_lahir, tanggal, jenis_kelamin, alamat,
                    pekerjaan, email, tingkat_gula_darah, usia_di_atas_40_tahun, riwayat_keluarga_diabetes, riwayat_diabetes_gestasional,
                    riwayat_lahir_di_bawah_2_koma_5_gram, riwayat_sindrom_ovariaum_polikistik, riwayat_penyakit_kardiovaskular, konsumsi_alkohol, kurang_aktivitas, merokok, pola_makan_buruk,
                    kurang_tidur, tinggi_badan, berat_badan, lingkar_perut, indeks_massa_tubuh, tekanan_darah, HDL, LDL, trigliserida,
                    total_kolestrol, gula_darah_sewaktu, gula_darah_puasa, gula_darah_2_jam_setelah_makan, gejala_terpilih, df_diagnosis_penyakit_tertentu, relasi_penyakit_dan_gejala)

            #base64_pdf = b64encode(file_pdf).decode("utf-8")
            #pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'

            #st.markdown(pdf_display, unsafe_allow_html=True)
            
            
            
            st.download_button(
                label="Download PDF",
                data=file_pdf,
                file_name = "Laporan Kesehatan_"+nama_pengguna+ "_"+str(tanggal)+".pdf",
                mime="application/pdf"
            )


    if pilihan == "Hapus Hasil":
        if "konfirmasi_hapus_riwayat" not in st.session_state:
            st.session_state.konfirmasi_hapus_riwayat = 0
        if st.button("Hapus Riwayat"):
            st.session_state.konfirmasi_hapus_riwayat = 1
            
            
        if st.session_state.konfirmasi_hapus_riwayat == 1:
            st.warning("Apakah Anda yakin ingin menghapus riwayat tersebut?")
            if st.button("Ya"):
                st.session_state.konfirmasi_hapus_riwayat = 2
        if st.session_state.konfirmasi_hapus_riwayat == 2:
            db.hapus_hasil_pemeriksaan_dan_diagnosis_penyakit_admin(id_pengguna, tanggal)
            st.success("Berhasil Hapus Riwayat")
            st.session_state.konfirmasi_hapus_riwayat = 0
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
