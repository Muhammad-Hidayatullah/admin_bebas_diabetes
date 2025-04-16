import streamlit as st
import datetime
from fpdf import FPDF
from assets import database as db
import re
import time
from assets import fungsi_pemeriksaan, forward_chaining as fc


st.title("DIAGNOSIS DIABETES TIPE 2")

if "lanjut_pemeriksaan" not in st.session_state:
    fungsi_pemeriksaan.awal_pemeriksaan()


if st.session_state.lanjut_pemeriksaan == 0:
    
    st.session_state.faktor_risiko_1 = 0
    st.session_state.daftar_faktor_risiko_1 = []
    
    with st.form(key="form_faktor_tidak_bisa_diubah"):
        st.subheader("Tanggal Pemeriksaan")
        st.session_state.tanggal_pemeriksaan = st.date_input("Masukkan tanggal pemeriksaan", min_value = datetime.date(1900, 1, 1), max_value = datetime.date.today(), value=st.session_state.tanggal_pemeriksaan)
        
        st.subheader("Faktor Tidak Bisa Diubah")

    
        st.session_state.usia_di_atas_40_tahun = st.radio("Usia di atas 40 tahun", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.usia_di_atas_40_tahun))
        
            
        st.session_state.riwayat_keluarga_diabetes = st.radio("Riwayat Keluarga Diabetes", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.riwayat_keluarga_diabetes))
        
        jenis_kelamin = db.get_jenis_kelamin(st.session_state.username_pengguna)
        if jenis_kelamin == "PEREMPUAN":
            st.session_state.riwayat_diabetes_gestasional = st.radio("Riwayat Melahirkan Bayi > 4 kg atau Terkena Diabetes Mellitus Gestasional", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.riwayat_diabetes_gestasional))

            st.session_state.riwayat_sindrom_ovariaum_polikistik = st.radio("Riwayat Terkena Sindrom Ovarium Polikistik", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.riwayat_sindrom_ovariaum_polikistik))
        else:
            st.session_state.riwayat_diabetes_gestasional = "TIDAK"
            st.session_state.riwayat_sindrom_ovariaum_polikistik = "TIDAK"
            
        st.session_state.riwayat_lahir_berat_badan_lahir_rendah = st.radio("Riwayat Lahir <2,5 kg atau terlahir prematur", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.riwayat_lahir_berat_badan_lahir_rendah))
        
        st.session_state.riwayat_penyakit_kardiovaskular = st.radio("Riwayat Penyakit Kardiovaskular", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.riwayat_penyakit_kardiovaskular))
        
        if st.session_state.usia_di_atas_40_tahun == "YA":
            st.session_state.faktor_risiko_1 = st.session_state.faktor_risiko_1 + 1
            st.session_state.daftar_faktor_risiko_1.append("Usia Di Atas 40 Tahun")
        if st.session_state.riwayat_keluarga_diabetes == "YA":
            st.session_state.faktor_risiko_1 = st.session_state.faktor_risiko_1 + 1
            st.session_state.daftar_faktor_risiko_1.append("Riwayat Keluarga Diabetes")
        if jenis_kelamin == "PEREMPUAN" and st.session_state.riwayat_diabetes_gestasional == "YA":
            st.session_state.faktor_risiko_1 = st.session_state.faktor_risiko_1 + 1
            st.session_state.daftar_faktor_risiko_1.append("Riwayat Melahirkan Bayi > 4 kg atau Terkena Diabetes Mellitus Gestasional")
        if jenis_kelamin == "PEREMPUAN" and st.session_state.riwayat_sindrom_ovariaum_polikistik == "YA":
            st.session_state.faktor_risiko_1 = st.session_state.faktor_risiko_1 + 1
            st.session_state.daftar_faktor_risiko_1.append("Riwayat Terkena Sindrom Ovarium Polikistik")
        
        if st.session_state.riwayat_lahir_berat_badan_lahir_rendah == "YA":
            st.session_state.faktor_risiko_1 = st.session_state.faktor_risiko_1 + 1
            st.session_state.daftar_faktor_risiko_1.append("Riwayat Lahir di bawah 2,5 kg")
            
        if st.session_state.riwayat_penyakit_kardiovaskular == "YA":
            st.session_state.faktor_risiko_1 = st.session_state.faktor_risiko_1 + 1
            st.session_state.daftar_faktor_risiko_1.append("Riwayat Penyakit Kardiovaskular")
    
       
        
        if st.form_submit_button("Lanjut"):
            st.session_state.total_faktor_risiko = st.session_state.faktor_risiko_1
            st.session_state.lanjut_pemeriksaan = 1
            st.rerun()
           

def cek_validasi_tekanan_darah(tekanan_darah):
    pola = r'^\d{1,3}/\d{1,3}$'
    return bool(re.match(pola, tekanan_darah))
     
     
def forward_chaining(fakta, aturan):
    # Fakta yang diketahui
    
    fakta = set(fakta)
    
    # Kemungkinan penyakit
    kemungkinan_penyakit = {}
    
    for penyakit, gejala_penyakit in aturan.items():
        # Hitung gejala yang cocok
        gejala_cocok = fakta.intersection(gejala_penyakit)
        tingkat_kecocokan = len(gejala_cocok) / len(gejala_penyakit)
        
        # Simpan hasil (penyakit, tingkat kecocokan, gejala cocok)
        kemungkinan_penyakit[penyakit] = {
            "tingkat_kecocokan": tingkat_kecocokan,
            "gejala_cocok": gejala_cocok,
            "gejala_penyakit" : gejala_penyakit,
        }
    
    # Filter penyakit dengan tingkat kecocokan tinggi (contoh: > 50%)
    hasil = {
        penyakit: data
        for penyakit, data in kemungkinan_penyakit.items()
        if data["tingkat_kecocokan"] >= 0.01
    }
    
    return hasil
     

def buat_laporan():
    pdf = FPDF()
    pdf.add_page()
    
    pdf.image("assets/logo_diabetes.png", x=10, y=8, w=30)  # Adjust x, y, and w for logo position and size
    pdf.image("assets/puskesmas_pkc_taman_sari.jpeg", x=170, y=8, w=30)
    
    # Menambahkan judul
    pdf.set_font("Arial", size=18, style="B")
    pdf.cell(200, 15, txt="LAPORAN HASIL PEMERIKSAAN ", ln=True, align='C')

    pdf.ln(5) 

    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Data Pengguna", ln=True)
    
    pdf.set_font("Arial", size=10)
    data_pribadi = [
        ['Kode Pengguna: ', st.session_state.kode_pengguna],
        ['Nama: ', st.session_state.nama_lengkap],
        ["Username: ", st.session_state.username_pengguna],
        ["Tanggal Lahir: ", str(st.session_state.tanggal_lahir)],
        ["Tanggal Pemeriksaan", str(st.session_state.tanggal_pemeriksaan)],
        ['Jenis Kelamin: ', st.session_state.jenis_kelamin],
        ['Alamat: ', st.session_state.alamat],
        ['Pekerjaan: ', st.session_state.pekerjaan],
        ['Email: ', st.session_state.email],
        ["Tingkat Gula Darah: ", st.session_state.tingkat_gula_darah]
    ]
    for row in data_pribadi:
        pdf.cell(75, 10, row[0], 1)
        
        if row[0] == "Tingkat Gula Darah: ":
            if row[1] == "PREDIABETES":
                pdf.set_text_color(255, 255, 0)  # Kuning
            elif row[1] == "DIABETES":
                pdf.set_text_color(255, 0, 0)  # Merah
            elif row[1] == "NORMAL":
                pdf.set_text_color(0, 255, 0)
            else:  # Normal
                pdf.set_text_color(0, 128, 0)  # Hijau
                
        pdf.cell(120, 10, row[1], 1)
        pdf.set_text_color(0, 0, 0)
        pdf.ln()  # Move to the next line

      # Return PDF as a string
    pdf.ln()    
    
    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Faktor Tidak Bisa Diubah", ln=True)
    pdf.set_font("Arial", size=10)
    
    pola_gaya_hidup = [
        ["Usia di atas 40 tahun: ", st.session_state.usia_di_atas_40_tahun],
        ["Riwayat Keluarga Diabetes: ", st.session_state.riwayat_keluarga_diabetes],
        ["Riwayat Diabetes Gestasional: ", st.session_state.riwayat_diabetes_gestasional],
        ["Riwayat Lahir <2,5 kg atau Prematur: ", st.session_state.riwayat_lahir_berat_badan_lahir_rendah ],
        ["Riwayat Sindrom Ovarium Polikistik: ", st.session_state.riwayat_sindrom_ovariaum_polikistik],
        ["Riwayat Penyakit Kardiovaskular: ", st.session_state.riwayat_penyakit_kardiovaskular],
    ]
    
    
    for row in pola_gaya_hidup:
        pdf.cell(75, 10, row[0], 1)  # First column
        pdf.cell(120, 10, row[1], 1)  # Second column
        pdf.ln()
    
    pdf.ln()
    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Pola Gaya Hidup", ln=True)
    pdf.set_font("Arial", size=10)
    pola_gaya_hidup = [
        ["Konsumsi Alkohol: ", st.session_state.konsumsi_alkohol],
        ["Kurang Aktivitas Fisik: ", st.session_state.kurang_aktivitas],
        ["Kebiasaan Merokok: ", st.session_state.merokok],
        ["Pola Makan Buruk : ", st.session_state.pola_makan_buruk],
        ["Tidur Tidak Berkualitas: ", st.session_state.kurang_tidur],
        
    ]
    for row in pola_gaya_hidup:
        pdf.cell(75, 10, row[0], 1)  # First column
        pdf.cell(120, 10, row[1], 1)  # Second column
        pdf.ln()
    
    pdf.ln()
    
    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Pemeriksaan Fisik", ln=True)
    pdf.set_font("Arial", size=10)
    
    pemeriksaan_fisik = [
        ["Parameter", "Hasil", "Nilai Normal"],
        ["Tinggi Badan: ", str(st.session_state.tinggi_badan)+" cm", "-"],
        ["Berat Badan: ", str(st.session_state.berat_badan)+" kg", "-"],
        ["Lingkar Perut: ", str(st.session_state.lingkar_perut)+" cm", " Pria <90cm , Wanita <80cm"],
        ["Indeks Massa Tubuh: ", str( st.session_state.indeks_massa_tubuh)+" kg/m2", " <=23 kg/m2"],
        ["Tekanan Darah: ", str(st.session_state.tekanan_darah)+" mmHg", " <140/90 mmHg"],
    ]
    
    for row in pemeriksaan_fisik:
        pdf.cell(50, 10, row[0], 1)  # First column
        pdf.cell(50, 10, row[1], 1)
        pdf.cell(60, 10, row[2], 1)# Second column
        pdf.ln()
    
    pdf.ln()
    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Kolestrol Darah", ln=True)
    pdf.set_font("Arial", size=10)
    hasil_laboratorium = [
        
        ["Parameter", "Hasil", "Nilai Normal"],
        ["HDL : ", str(st.session_state.HDL)+" mg/dL", " >50 mg/dL"],
        ["LDL : ", str(st.session_state.LDL)+" mg/dL", " <100 mg/dL"],
        ["Trigliserida : ", str(st.session_state.trigliserida)+" mg/dL", " <150 mg/dL"],
        ["Total Kolestrol Darah: ", str(st.session_state.total_kolestrol_darah)+" mg/dL", " <200 mg/dL"],
    ]
   
    
    for row in hasil_laboratorium:
        pdf.cell(50, 10, row[0], 1)  # First column
        pdf.cell(50, 10, row[1], 1) # Second column
        pdf.cell(50, 10, row[2], 1)
        pdf.ln()
    
    pdf.ln()
    
    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Hasil Laboratorium", ln=True)
    pdf.set_font("Arial", size=10)
    hasil_laboratorium = [
        ["Parameter", "Nilai", "Nilai Normal"],
        ["Gula Darah Sewaktu (GDS): ", str(st.session_state.gula_darah_sewaktu)+" mg/dL", " <140 mg/dL"],
        ["Gula Darah Puasa (GDP): ", str(st.session_state.gula_darah_puasa)+" mg/dL", " <100 mg/dL"],
        ["Gula Darah 2 Jam Setelah Makan (GD2PP): ", str(st.session_state.gula_darah_2_jam_setelah_makan)+" mg/dL", " <140 mg/dL"],

    ]
    
    for row in hasil_laboratorium:
        pdf.cell(90, 10, row[0], 1)
        pdf.cell(50, 10, row[1], 1) 
        pdf.cell(50, 10, row[2], 1) 
        pdf.ln()
    
    pdf.ln(120)

    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(200, 10, txt=f"Catatan Penting: Anda Tetap Harus Mengunjungi Dokter Untuk Mendapatkan Penanganan yang Tepat", ln=True)
    pdf.set_font("Arial", size=18, style="B")
    pdf.cell(75, 10, txt="Diagnosis Penyakit", ln=True)
    
    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Gejala-Gejala Terpilih", ln=True)
    pdf.set_font("Arial", size=10)
    
    if st.session_state.gejala_terpilih:
        for i, gejala in enumerate(st.session_state.gejala_terpilih, start=1):
            pdf.multi_cell(200, 10, txt=f"{i}. {gejala}")
        if i >= 18 and i <= 24:
            pdf.ln(120)
        
    else:            
        pdf.cell(200, 10, txt="--", ln=True)
        
    pdf.ln(5)
    if pdf.get_y() > 220:
        pdf.ln(200)
    
    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Komplikasi Penyakit", ln=True)
    pdf.set_font("Arial", size=10)
    
    if st.session_state.hasil_diagnosis:
        for penyakit, data in st.session_state.hasil_diagnosis.items():
            kecocokan = data["tingkat_kecocokan"] * 100
            gejala_cocok = "; ".join(data["gejala_cocok"])
            gejala_penyakit = "; ".join(data["gejala_penyakit"])
            
            
            pdf.set_font("Arial", size=10, style="B")
            pdf.cell(200, 10, txt=f"{penyakit} : {kecocokan:.2f}%", ln=True)
            
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 10, txt=f"{db.get_penjelasan_penyakit(penyakit)}")

            pdf.ln(5)
            if pdf.get_y() > 220:
                pdf.ln(200)
            pdf.set_font("Arial", size=10, style="B")
            pdf.cell(200, 10, txt=f"Gejala yang Cocok", ln=True)
            
            pdf.set_font("Arial", size=10)
            pisah_gejala_cocok = gejala_cocok.split("; ")
            
            for i, gejala in enumerate(pisah_gejala_cocok, start=1):
                
                pdf.multi_cell(0, 10, txt=f"{i}. {gejala}")
            
            pdf.ln(5)
            if pdf.get_y() > 220:
                pdf.ln(200)
            pdf.set_font("Arial", size=10, style="B")
            pdf.cell(200, 10, txt=f"Gejala Penyakit", ln=True)
            pdf.set_font("Arial", size=10)
            
            pisah_gejala_penyakit = gejala_penyakit.split("; ")
            for i, gejala_penyakit in enumerate(pisah_gejala_penyakit, start=1):
                pdf.multi_cell(0, 10, txt=f"{i}. {gejala_penyakit}")
            
            
            pdf.ln(5)
            if pdf.get_y() > 220:
                pdf.ln(200)
            pdf.set_font("Arial", size=10, style="B")
            pdf.cell(200, 10, txt=f"Solusi Penyakit", ln=True)
            pdf.set_font("Arial", size=10)
            
            # Loop untuk menampilkan dengan nomor urut
            solusi_penyakit = db.get_solusi_penyakit(penyakit)
            solusi_penyakit = solusi_penyakit.split(";")

        
            daftar_solusi = []
            
            for frasa in solusi_penyakit:
                daftar_solusi.append(frasa.strip())
            
            # Loop untuk menampilkan dengan nomor urut
            for i, frasa in enumerate(daftar_solusi, start=1):
                pdf.multi_cell(0, 10, txt=f"{i}. {frasa}")
               
            pdf.ln(10)
            if pdf.get_y() > 220:
                pdf.ln(200)

    else:
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"--", ln=True)

    return bytes(pdf.output())
    #return pdf.output(dest="S").encode("latin1")
   



if st.session_state.lanjut_pemeriksaan == 1:
    st.session_state.faktor_risiko_2 = 0
    st.session_state.daftar_faktor_risiko_2 = []
    
    with st.form(key="form_faktor_bisa_diubah"):
        st.subheader("Pemeriksaan Gaya Hidup")
        st.session_state.konsumsi_alkohol = st.radio("Konsumsi Alkohol", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.konsumsi_alkohol))
        st.session_state.kurang_aktivitas = st.radio("Kurang Aktivitas Fisik (< 150 menit/minggu)", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.kurang_aktivitas))
        st.session_state.merokok = st.radio("Kebiasaan Merokok", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.merokok))
        st.session_state.pola_makan_buruk = st.radio("Pola Makan Buruk (Tinggi gula, garam, dan lemak; rendah serat; serta jarang makan sayur dan buah)", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.pola_makan_buruk))
        st.session_state.kurang_tidur = st.radio("Kurang tidur/gangguan tidur/tidur tidak berkualitas < 6 jam", ("TIDAK", "YA"), horizontal=True, index=("TIDAK", "YA").index(st.session_state.kurang_tidur))
        
        
        
        st.markdown("---")
        
        st.subheader("Pemeriksaan Fisik")
        st.session_state.tinggi_badan = st.number_input("Tinggi Badan (cm): ", min_value=0.0, max_value=999.0, value=st.session_state.tinggi_badan)
        st.session_state.berat_badan = st.number_input("Berat Badan (kg): ", min_value=0.0, max_value=999.0, value=st.session_state.berat_badan)
        st.session_state.lingkar_perut = st.number_input("Lingkar perut (cm): ", min_value=0.0, max_value=240.0, step=None, value=st.session_state.lingkar_perut)
        st.session_state.tekanan_darah = st.text_input("Tekanan Darah (mmHg): ", value=st.session_state.tekanan_darah)
        cek_tekanan_darah = 0
        
        
        
        
        st.markdown("---")
        
        st.subheader("Kolestrol Darah")

        st.session_state.HDL = st.number_input("HDL (mg/dL): ", min_value=0.0, max_value=999.0, value=st.session_state.HDL)
        
        st.session_state.LDL = st.number_input("LDL (mg/dL): ", min_value=0.0, max_value=999.0, value=st.session_state.LDL)
        
        st.session_state.trigliserida = st.number_input("Trigliserida (mg/dL): ", min_value=0.0, max_value=999.0, value=st.session_state.trigliserida)
        
        st.session_state.total_kolestrol = st.number_input("Total Kolestrol Darah (mg/dL) (Kosongkan saja apabila HDL, LDL, dan trigliserida terisi): ", min_value=0.0, max_value=999.0, value=st.session_state.total_kolestrol)

        col1, col2, col3 = st.columns(3)

        with col3:
            if st.form_submit_button("Lanjut"):
                if st.session_state.konsumsi_alkohol == "YA":
                    st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                    st.session_state.daftar_faktor_risiko_2.append("Konsumsi Alkohol")
                if st.session_state.kurang_aktivitas == "YA":
                    st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                    st.session_state.daftar_faktor_risiko_2.append("Kurang Aktivitas")
                if st.session_state.merokok == "YA":
                    st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                    st.session_state.daftar_faktor_risiko_2.append("Aktif Merokok")
                if st.session_state.pola_makan_buruk == "YA":
                    st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                    st.session_state.daftar_faktor_risiko_2.append("Pola Makan Buruk (Tinggi gula, garam, dan lemak; rendah serat; serta jarang makan sayur dan buah)")
                if st.session_state.kurang_tidur == "YA":
                    st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                    st.session_state.daftar_faktor_risiko_2.append("Kurang tidur/gangguan tidur/tidur tidak berkualitas < 6 jam")
                
                
        
                st.session_state.indeks_massa_tubuh = 0.0
                if st.session_state.berat_badan is None:
                    st.session_state.berat_badan = 0.0
                if st.session_state.tinggi_badan is None:
                    st.session_state.tinggi_badan = 0.0
                    
                if st.session_state.berat_badan == 0.0 or st.session_state.tinggi_badan == 0.0:
                    st.session_state.indeks_massa_tubuh = 0.0
                else:
                    st.session_state.indeks_massa_tubuh = st.session_state.berat_badan/((st.session_state.tinggi_badan) ** 2) * 10000
                    st.session_state.indeks_massa_tubuh = round(st.session_state.indeks_massa_tubuh, 1)
                    
                if st.session_state.indeks_massa_tubuh > 23.0:
                    st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                    kelebihan_berat_badan = "Kelebihan Berat Badan: " + str(st.session_state.indeks_massa_tubuh) + " kg/m2"
                    st.session_state.daftar_faktor_risiko_2.append(kelebihan_berat_badan)
    
                if st.session_state.lingkar_perut is None:
                    st.session_state.lingkar_perut = 0.0
                    
                if st.session_state.jenis_kelamin == "PEREMPUAN" and st.session_state.lingkar_perut >= 80.0:
                    st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                    obesitas_sentral = "Obesitas Sentral: " + str(st.session_state.lingkar_perut) + " cm"
                    st.session_state.daftar_faktor_risiko_2.append(obesitas_sentral)
                    
                
                    
                if st.session_state.jenis_kelamin == "LAKI-LAKI" and st.session_state.lingkar_perut >= 90.0:
                    st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                    obesitas_sentral = "Obesitas Sentral: " + str(st.session_state.lingkar_perut) + " cm"
                    st.session_state.daftar_faktor_risiko_2.append(obesitas_sentral)
                        
                
                
                
                

                
                if cek_validasi_tekanan_darah(st.session_state.tekanan_darah) == False or st.session_state.tekanan_darah == "":
                    cek_tekanan_darah = 1
                    
        
                if cek_validasi_tekanan_darah(st.session_state.tekanan_darah) == True:
                    st.session_state.sistole, st.session_state.diastole = st.session_state.tekanan_darah.split("/")
                    st.session_state.sistole = int(st.session_state.sistole)
                    st.session_state.diastole = int(st.session_state.diastole)
                    if st.session_state.sistole < st.session_state.diastole:
                        cek_tekanan_darah = 2
                    if st.session_state.sistole >= 140 or st.session_state.diastole >= 90:
                        st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                        hipertensi = "Hipertensi: " + st.session_state.tekanan_darah + " mmHg"
                        st.session_state.daftar_faktor_risiko_2.append(hipertensi)
                
                st.session_state.total_kolestrol_darah = st.session_state.HDL + st.session_state.LDL + (st.session_state.trigliserida/5.0)
                if st.session_state.total_kolestrol_darah > 0:
                    st.session_state.total_kolestrol = st.session_state.total_kolestrol_darah
            
       
            
                if st.session_state.total_kolestrol_darah >= 200.0 or st.session_state.total_kolestrol >= 200.0 or ((st.session_state.HDL != 0.0 and st.session_state.HDL < 50.0) or st.session_state.LDL > 100.0 or st.session_state.trigliserida > 150.0):
                    st.session_state.faktor_risiko_2 = st.session_state.faktor_risiko_2 + 1
                    
                    disiplidemia = "Disiplidemia: "
                    
                       
    
                    if st.session_state.total_kolestrol >= 200:
                        disiplidemia = disiplidemia + "Total Kolestrol Tinggi sebesar " + str(st.session_state.total_kolestrol) + " mg/dL "
                    
                
    
                    
                    
                    if (st.session_state.HDL != 0.00 and st.session_state.HDL < 50.0):
                        disiplidemia = disiplidemia + "HDL = " + str(st.session_state.HDL) + " mg/dL "
                    if st.session_state.LDL > 100.0:
                        disiplidemia = disiplidemia + "LDL = " + str(st.session_state.LDL) + " mg/dL "
                    if st.session_state.trigliserida > 150.0:
                        disiplidemia = disiplidemia + "Trigliserida = " + str(st.session_state.trigliserida) + " mg/dL "
                    
                    st.session_state.daftar_faktor_risiko_2.append(disiplidemia)
                
                
                
                if cek_tekanan_darah == 0:
                    st.session_state.lanjut_pemeriksaan = 2
                    st.rerun()
            with col1:
                if st.form_submit_button("Kembali"):  
                    st.session_state.lanjut_pemeriksaan = 0
                    st.rerun()
    
        if cek_tekanan_darah == 1:
            st.error("Tekanan Darah Anda Salah! Buat dengan format : 120/80")
        if cek_tekanan_darah == 2:
            st.error("Tekanan darah anda salah! Yang pertama harus lebih besar daripada yang kedua dengan format: 120/80 bukan 80/120!")
        
    
if st.session_state.lanjut_pemeriksaan == 2:
    
    st.session_state.daftar_faktor_risiko = []
    
    if st.session_state.daftar_faktor_risiko_1:
        st.session_state.daftar_faktor_risiko.extend(st.session_state.daftar_faktor_risiko_1)

    if st.session_state.daftar_faktor_risiko_2:
        st.session_state.daftar_faktor_risiko.extend(st.session_state.daftar_faktor_risiko_2)
            
    #menghitung total faktor risiko
    st.session_state.total_faktor_risiko = st.session_state.faktor_risiko_1 + st.session_state.faktor_risiko_2
    
    with st.form(key="hitung_total_faktor_risiko"):
        st.subheader("Total Faktor Risiko Anda: " + str(st.session_state.total_faktor_risiko))
        
        kembali = 0
        if st.session_state.total_faktor_risiko == 0:
            st.success("Anda Tidak Memiliki Faktor Risiko dan Risiko Rendah Terkena Diabetes Mellitus Tipe 2")
            st.success("Tetap Jaga Pola Hidup Sehat!")
            st.session_state.tingkat_risiko = "RENDAH"
        if st.session_state.total_faktor_risiko == 1 or st.session_state.total_faktor_risiko == 2:
            st.warning("Anda Memiliki 1 atau 2 Faktor Risiko dan Risiko Menengah Terkena Diabetes Mellitus Tipe 2")
            st.session_state.tingkat_risiko = "SEDANG"
        if st.session_state.total_faktor_risiko >= 3:
            st.error("Anda Memiliki Faktor Risiko ≥3 dan Risiko Tinggi Terkena Diabetes Mellitus Tipe 2")
            st.session_state.tingkat_risiko = "TINGGI"
        for i in st.session_state.daftar_faktor_risiko:
            st.warning(i)
        
        
        col1, col2, col3 = st.columns(3)
        cek = 0
        with col1:
            if st.form_submit_button("Kembali"):
                st.session_state.lanjut_pemeriksaan = 1
                st.session_state.daftar_faktor_risiko = []
               
                st.rerun()
      
            
                    
            
        with col3:
            if st.form_submit_button("Lanjut"):
                st.session_state.lanjut_pemeriksaan = 3
                st.rerun()
                
        if kembali == 1:
            st.success("Kembali ke menu awal")
            st.session_state.lanjut_pemeriksaan = 0
            time.sleep(2)
            st.rerun()
                
if st.session_state.lanjut_pemeriksaan == 3:
    if "selesai" not in st.session_state:
        st.session_state.selesai = 0
    if "sudah_diisi" not in st.session_state:
        st.session_state.sudah_diisi = 0
    if "hapus" not in st.session_state:
        st.session_state.hapus = 0
    with st.form(key="form_pemeriksaan_gula_darah"):
        st.session_state.gula_darah_sewaktu = 0.0
        st.session_state.gula_darah_puasa = 0.0
        st.session_state.gula_darah_2_jam_setelah_makan = 0.0
        st.subheader("Pemeriksaan Gula Darah")
        st.session_state.gula_darah_sewaktu = st.number_input("Gula Darah Sewaktu (mg/dL): ", min_value=0.0, max_value=999.0, value=st.session_state.gula_darah_sewaktu)
        st.session_state.gula_darah_puasa = st.number_input("Gula Darah Puasa (mg/dL): ", min_value=0.0, max_value=999.0, value=st.session_state.gula_darah_puasa)
        st.session_state.gula_darah_2_jam_setelah_makan = st.number_input("Gula Darah 2 Jam Setelah Makan (mg/dL): ", min_value=0.0, max_value=1000.0, value=st.session_state.gula_darah_2_jam_setelah_makan)

        
        if st.form_submit_button("Lanjut"):
            if (st.session_state.gula_darah_sewaktu is None and st.session_state.gula_darah_puasa is None and st.session_state.gula_darah_2_jam_setelah_makan is None) or (st.session_state.gula_darah_sewaktu == 0.0 and st.session_state.gula_darah_puasa == 0.0 and st.session_state.gula_darah_2_jam_setelah_makan == 0.0):
                st.error("Salah satu Gula darah harus diisi untuk lanjut!")
            else:
                st.session_state.skip_gula_darah = 0
                st.session_state.lanjut_pemeriksaan = 4
                st.rerun()
        if st.session_state.total_faktor_risiko > 0:
            if st.form_submit_button("Belum Cek Darah? Langsung Isi Gejala"):
                
                st.session_state.gula_darah_sewaktu = 0.0
                st.session_state.gula_darah_puasa = 0.0
                st.session_state.gula_darah_2_jam_setelah_makan = 0.0
                st.session_state.lanjut_pemeriksaan = 5
                st.session_state.skip_gula_darah = 1
                st.rerun()
        else:
            if st.form_submit_button("Belum Cek Darah? Selesai"):
                
                if st.session_state.tanggal_pemeriksaan == db.get_tanggal_terkini(st.session_state.kode_pengguna):
                    st.session_state.sudah_diisi = 1
                else:
                    st.session_state.selesai = 1
                
                
       
        if st.session_state.sudah_diisi == 1:
            st.session_state.selesai = 0
          
            st.warning("Tanggal tersebut sudah pernah terisi, apakah Anda ingin menggantinya dengan yang terbaru?")
            if st.form_submit_button("Ya"):
                st.session_state.hapus = 1
                
            
        
            if st.session_state.hapus == 1:
                st.success("Menghapus data yang lama!")
                db.hapus_pemeriksaan_kesehatan_dan_diagnosis(st.session_state.tanggal_pemeriksaan)
                st.session_state.selesai = 1
                
                
        
    
                
        if st.session_state.selesai == 1:
            
            id_pemeriksaan_default = db.menambah_id_pemeriksaan_kesehatan_default()
            db.add_pemeriksaan_kesehatan(id_pemeriksaan_default, db.get_id_pengguna(st.session_state.username_pengguna), st.session_state.tingkat_gula_darah, st.session_state.tanggal_pemeriksaan)
            db.add_pemeriksaan_faktor_permanen(id_pemeriksaan_default, st.session_state.usia_di_atas_40_tahun, st.session_state.riwayat_keluarga_diabetes, st.session_state.riwayat_diabetes_gestasional, st.session_state.riwayat_lahir_berat_badan_lahir_rendah, st.session_state.riwayat_sindrom_ovariaum_polikistik, st.session_state.riwayat_penyakit_kardiovaskular)
            db.add_pemeriksaan_fisik(id_pemeriksaan_default, st.session_state.tinggi_badan, st.session_state.berat_badan, st.session_state.lingkar_perut, st.session_state.indeks_massa_tubuh, st.session_state.tekanan_darah)
            db.add_pemeriksaan_laboratorium(id_pemeriksaan_default, st.session_state.gula_darah_sewaktu, st.session_state.gula_darah_puasa, st.session_state.gula_darah_2_jam_setelah_makan, st.session_state.HDL, st.session_state.LDL, st.session_state.trigliserida, st.session_state.total_kolestrol)
            db.add_kebiasaan_hidup(id_pemeriksaan_default, st.session_state.konsumsi_alkohol, st.session_state.kurang_aktivitas, st.session_state.merokok, st.session_state.pola_makan_buruk, st.session_state.kurang_tidur)
            db.insert_diagnosis_penyakit(db.menambah_id_diagnosis_default(), st.session_state.data_pengguna[0], None, None, None, st.session_state.tanggal_pemeriksaan)
            fungsi_pemeriksaan.awal_pemeriksaan()
            
            st.success("Kembali ke menu awal")
            st.session_state.lanjut_pemeriksaan = 0
            st.session_state.selesai = 0
    
            st.session_state.sudah_diisi = 0
    
            st.session_state.hapus = 0
            
            time.sleep(2)
            st.rerun()
            
        if st.form_submit_button("Kembali"):
            
            st.session_state.lanjut_pemeriksaan = 2
            st.rerun()
       
        

if st.session_state.lanjut_pemeriksaan == 4:
    with st.form(key="form_tingkat_risiko"):
        st.subheader("Hasil Tingkat Gula Darah")
        if st.session_state.gula_darah_sewaktu != 0:
            st.write("Gula Darah Sewaktu (GDS): " + str(st.session_state.gula_darah_sewaktu) + " mg/dL")
            if st.session_state.gula_darah_sewaktu >= 200.0:
                st.error("Gula Darah Sewaktu Tinggi Berada di Nilai ≥200 mg/dL!")
            if st.session_state.gula_darah_sewaktu >= 140.0 and st.session_state.gula_darah_sewaktu < 200:
                st.warning("Gula Darah Sewaktu Berada di Level Prediabetes Antara 140 dan 199 mg/dL!")
            if st.session_state.gula_darah_sewaktu < 140.0:
                st.success("Gula Darah Sewaktu Aman di <140 mg/dL!")
        
        
        if st.session_state.gula_darah_puasa != 0:
            st.write("Gula Darah Puasa (GDP): " + str(st.session_state.gula_darah_puasa) + " mg/dL")
            if st.session_state.gula_darah_puasa >= 126.0:
                st.error("Gula Darah Puasa Tinggi Berada di Nilai ≥126 mg/dL!")
            if st.session_state.gula_darah_puasa >= 100.0 and st.session_state.gula_darah_puasa < 126.0:
                st.warning("Gula Darah Puasa Berada Di Level Prediabetes Antara 100 dan 125 mg/dL!")
            if st.session_state.gula_darah_puasa < 100.0:
                st.success("Gula Darah Puasa Aman di <100 mg/dL!")
        
        if st.session_state.gula_darah_2_jam_setelah_makan != 0:
            st.write("Gula Darah 2 Jam Setelah Makan: " + str(st.session_state.gula_darah_2_jam_setelah_makan) + " mg/dL")
            if st.session_state.gula_darah_2_jam_setelah_makan >= 200.0:
                st.error("Gula Darah 2 Jam Setelah Makan Tinggi Berada di Nilai ≥200 mg/dL!")
            if st.session_state.gula_darah_2_jam_setelah_makan >= 140.0 and st.session_state.gula_darah_2_jam_setelah_makan < 200.0:
                st.warning("Gula Darah 2 Jam Setelah Makan Berada Di Level Prediabetes Antara 140 dan 199 mg/dL!")
            if st.session_state.gula_darah_2_jam_setelah_makan < 140.0:
                st.success("Gula Darah 2 Jam Setelah Makan Anda Aman di <140 mg/dL!")
        st.subheader("Diagnosis:")
        # Faktor Risiko 0
        if (st.session_state.gula_darah_sewaktu >= 200.0 or 
            st.session_state.gula_darah_puasa >= 126.0 or 
            st.session_state.gula_darah_2_jam_setelah_makan >= 200.0) and st.session_state.total_faktor_risiko == 0:
            
            st.error("Gula darah sudah masuk ke dalam level diabetes meskipun tidak memiliki faktor risiko. Anda disarankan untuk segera menerapkan pola hidup sehat dan berkonsultasi dengan dokter")
            st.session_state.tingkat_gula_darah = "DIABETES"
          

        elif (140 <= st.session_state.gula_darah_sewaktu < 200.0 or 
            100 <= st.session_state.gula_darah_puasa < 126.0 or 
            140 <= st.session_state.gula_darah_2_jam_setelah_makan < 200.0) and st.session_state.total_faktor_risiko == 0:
            st.warning("Tidak ada faktor risiko namun gula sudah masuk ke dalam level prediabetes. Disarankan untuk menerapkan pola hidup sehat dan mengurangi makanan yang mengandung tinggi gula!")
            st.session_state.tingkat_gula_darah = "PREDIABETES"
            

        elif (st.session_state.gula_darah_sewaktu < 140.0 and 
            st.session_state.gula_darah_puasa < 100.0 and 
            st.session_state.gula_darah_2_jam_setelah_makan < 140.0) and st.session_state.total_faktor_risiko == 0:
            st.success("Gula darah normal dan tidak ada faktor risiko")
            st.success("Tetap jaga pola hidup sehat")
            st.session_state.tingkat_gula_darah = "NORMAL"
            
    
        # Faktor Risiko 1 atau 2
        if (st.session_state.gula_darah_sewaktu >= 200.0 or st.session_state.gula_darah_puasa >= 126.0 or st.session_state.gula_darah_2_jam_setelah_makan >= 200.0) and (st.session_state.total_faktor_risiko == 1 or st.session_state.total_faktor_risiko == 2):
            st.error("Gula darah sudah masuk ke dalam level diabetes dan terdapat beberapa faktor risiko. Anda sangat disarankan untuk segera berkonsultasi ke dokter dan menerapkan pola hidup sehat")
            st.session_state.tingkat_gula_darah = "DIABETES"
        
        elif (st.session_state.gula_darah_sewaktu >= 140.0 and st.session_state.gula_darah_sewaktu < 200.0 or st.session_state.gula_darah_puasa >= 100.0 and st.session_state.gula_darah_puasa < 126.0 or st.session_state.gula_darah_2_jam_setelah_makan >= 140.0 and st.session_state.gula_darah_2_jam_setelah_makan < 200.0) and (st.session_state.total_faktor_risiko == 1 or st.session_state.total_faktor_risiko == 2):
            st.warning("Gula darah sudah mencapai level prediabetes dan terdapat beberapa faktor risiko. Disarankan untuk segera mengubah pola hidup menjadi lebih sehat")     
            st.session_state.tingkat_gula_darah = "PREDIABETES"
        elif (st.session_state.gula_darah_sewaktu < 140.0 or st.session_state.gula_darah_puasa < 100.0 or st.session_state.gula_darah_2_jam_setelah_makan < 140.0) and (st.session_state.total_faktor_risiko == 1 or st.session_state.total_faktor_risiko == 2):
            st.warning("Gula darah normal namun terdapat faktor risiko, terapkan pola hidup sehat!")
            st.session_state.tingkat_gula_darah = "NORMAL"
         
         
        if (st.session_state.gula_darah_sewaktu >= 200.0 or st.session_state.gula_darah_puasa >= 126.0 or st.session_state.gula_darah_2_jam_setelah_makan >= 200.0) and st.session_state.total_faktor_risiko >= 3:
            
            st.error("Anda memiliki banyak faktor risiko dan gula darah sudah mencapai level diabetes. Sangat disarankan untuk segera berkonsultasi dengan dokter untuk mendapatkan pengobatan dan penanganan!")
            st.session_state.tingkat_gula_darah = "DIABETES"
        elif (st.session_state.gula_darah_sewaktu >= 140.0 and st.session_state.gula_darah_sewaktu < 200.0 or st.session_state.gula_darah_puasa >= 100.0 and st.session_state.gula_darah_puasa < 126.0 or st.session_state.gula_darah_2_jam_setelah_makan >= 140.0 and st.session_state.gula_darah_2_jam_setelah_makan < 200.0) and st.session_state.total_faktor_risiko >= 3:
       
            st.warning("Anda memiliki banyak faktor risiko dan gula sudah masuk ke dalam level prediabetes. Disarankan untuk segera menerapkan pola hidup sehat dan ikuti saran di bawah ini")     
            st.session_state.tingkat_gula_darah = "PREDIABETES"
        elif (st.session_state.gula_darah_sewaktu < 140.0 or st.session_state.gula_darah_puasa < 100.0 or st.session_state.gula_darah_2_jam_setelah_makan < 140.0) and st.session_state.total_faktor_risiko >= 3:
            st.warning("Gula darah normal namun banyak faktor risiko yang dapat menyebabkan Diabetes Mellitus 2 Tipe di masa yang akan datang")
            st.session_state.tingkat_gula_darah = "NORMAL"
        
        st.write("")
        
        
        
        if st.session_state.tingkat_gula_darah != "NORMAL":
            st.subheader("Saran untuk menurunkan gula darah: ")
            solusi = [
            "Melakukan aktivitas fisik secara rutin untuk menjaga kebugaran tubuh.",
            "Meningkatkan kualitas tidur dengan tidur selama kurang lebih 8 jam per hari.",
            "Menghindari atau mengurangi konsumsi rokok dan alkohol.",
            "Menjaga berat badan ideal, terutama jika telah melebihi standar Indeks Massa Tubuh (IMT) sebesar < 23 kg/m².",
            "Menghindari konsumsi makanan dalam porsi besar dan berlebihan.",
            "Membatasi konsumsi makanan yang mengandung karbohidrat atau gula, seperti nasi dan roti putih, serta meningkatkan asupan serat dari buah-buahan, biji-bijian, kacang-kacangan, dan sumber nabati lainnya.",
            "Mengelola stres dengan teknik relaksasi seperti meditasi atau melakukan aktivitas positif sebagai distraksi.",
            "Meningkatkan konsumsi air putih untuk mencegah dehidrasi dan membantu ginjal dalam mengeluarkan kelebihan gula melalui urin.",
            "Melakukan pemeriksaan kadar gula darah secara rutin untuk memantau kondisi kesehatan."
            ]
            for i, solusi in enumerate(solusi, start=1):
                st.warning(f"{i}. {solusi}")

        

        
        st.write("")
            
        
        
        
    
        if st.form_submit_button("Lanjut Memilih Gejala"):
            st.session_state.lanjut_pemeriksaan = 5
            st.rerun()
        if st.form_submit_button("Kembali"):
            st.session_state.lanjut_pemeriksaan = 3
            st.rerun()
            
if st.session_state.lanjut_pemeriksaan == 5:
    with st.form(key="form_pemeriksaan_komplikasi"):
        st.subheader("Piih Gejala yang Anda Alami")
        col1, col2, col3 = st.columns(3)
        df_gejala = db.fetch_gejala()
        st.session_state.gejala_terpilih = []
        
        for index, row in df_gejala.iterrows():
            if index % 3 == 0:
                with col1:
                    if st.checkbox(row["Nama Gejala"]):
                        st.session_state.gejala_terpilih.append(row["Nama Gejala"])
            if index % 3 == 1:
                with col2:
                    if st.checkbox(row["Nama Gejala"]):
                        st.session_state.gejala_terpilih.append(row["Nama Gejala"])
            if index % 3 == 2:
                with col3:
                    if st.checkbox(row["Nama Gejala"]):
                        st.session_state.gejala_terpilih.append(row["Nama Gejala"])
        

        col1, col2 = st.columns(2)
        
        with col1:
            if st.form_submit_button("Kembali"):
                if st.session_state.skip_gula_darah == 1:
                    st.session_state.lanjut_pemeriksaan = 3
                    st.session_state.tingkat_gula_darah = "-"
                else:
                    st.session_state.lanjut_pemeriksaan = 4
                st.rerun()
        with col2:
            if st.form_submit_button("Lanjut"):
                st.session_state.lanjut_pemeriksaan = 6
                st.rerun()


            
if st.session_state.lanjut_pemeriksaan == 6:
    if "hasil_diagnosis" not in st.session_state:
        st.session_state.hasil_diagnosis = {}
        
   
    catatan = False
    with st.form(key="form_hasil_komplikasi"):    
        st.subheader("Gejala-Gejala Yang Terpilih")
        
        for i, gejala_terpilih in enumerate(st.session_state.gejala_terpilih, start=1):
            st.write(f"{i}. {gejala_terpilih}")
        
        if not st.session_state.gejala_terpilih:
            st.write("Tidak Ada Gejala yang Terpilih")
            
        
        st.subheader("Komplikasi Penyakit")
        
        # Ambil data relasi dari database             
        data_relasi = db.fetch_relasi_nama_penyakit_dan_nama_gejala()
        
        #Relasi Penyakit dan Gejala
        relasi_dict = {}
        for penyakit, gejala in data_relasi:
            if penyakit not in relasi_dict:
                relasi_dict[penyakit] = []  # Buat list kosong jika penyakit belum ada
            relasi_dict[penyakit].append(gejala)  # Tambahkan gejala ke list penyakit tersebut
       
       
        if st.session_state.gejala_terpilih:
            st.session_state.hasil_diagnosis = fc.forward_chaining(st.session_state.gejala_terpilih, relasi_dict)
       
            if st.session_state.hasil_diagnosis:
                
                for penyakit, data in st.session_state.hasil_diagnosis.items():
                    kecocokan = data["tingkat_kecocokan"] * 100
                    gejala_cocok = "; ".join(data["gejala_cocok"])
                    gejala_penyakit = "; ".join(data["gejala_penyakit"])
                    
             
                    st.error(f"**{penyakit}: {kecocokan:.2f}%**")
                    st.write(db.get_penjelasan_penyakit(penyakit))
                    
                    st.write("**Gejala yang Cocok**")
                    st.write(gejala_cocok)
                    st.write("**Gejala Penyakit**")
                    st.write(gejala_penyakit)
                    
                    solusi_penyakit = db.get_solusi_penyakit(penyakit)
                    
                    #frasa_list = [frasa.strip() for frasa in solusi_penyakit.split(",")]
                    
                    # Pecah string berdasarkan koma
                    solusi_penyakit = solusi_penyakit.split(";")

                    # Bersihkan spasi di setiap frasa
                    st.session_state.daftar_solusi = []
                    
                    for frasa in solusi_penyakit:
                        st.session_state.daftar_solusi.append(frasa.strip())

                    st.write("**Solusi**")
                    # Loop untuk menampilkan dengan nomor urut
                    for i, frasa in enumerate(st.session_state.daftar_solusi, start=1):
                        st.write(f"{i}. {frasa}")
                    
                    
                    st.write("")                              
                catatan = True
            
                    
            else:
                st.write("Tidak ditemukan komplikasi yang cocok.")
                
        else:
            st.write("Tidak ada gejala yang bisa diproses.")


        if catatan == True:
            st.warning("**Catatan Penting**: Anda Harus Tetap Berkunjung Ke Dokter untuk Mendapatkan Pengobatan dan Solusi Lebih Lanjut!")
        
        

        col1, col2 = st.columns(2)
        if "cek" not in st.session_state:
                st.session_state.cek = 0
            
        with col1:
            if st.form_submit_button("Kembali"):
                st.session_state.lanjut_pemeriksaan = 5
                st.session_state.hasil_diagnosis = {}
                st.rerun()
            
        
        with col2:
            if st.form_submit_button("Selesai"):
                    st.session_state.cek = 1
        if st.session_state.cek == 1:
            if st.session_state.tanggal_pemeriksaan == db.get_tanggal_terkini(st.session_state.kode_pengguna):
                st.warning("Anda sudah melakukan pemeriksaan hari ini, apakah Anda ingin menggantinya dengan yang terbaru?")
                if st.form_submit_button("Ya"):
                    st.session_state.cek = 2
                    st.success("Tunggu Sebentar!")
                    db.hapus_pemeriksaan_kesehatan_dan_diagnosis(st.session_state.tanggal_pemeriksaan)
                    st.success("Diagnosis sebelumnya berhasil terhapus!")
                    
            if st.session_state.cek == 2 or st.session_state.tanggal_pemeriksaan != db.get_tanggal_terkini(st.session_state.kode_pengguna):
                st.session_state.cek = 0
                st.session_state.lanjut_pemeriksaan = 7

                st.success("Tunggu Sebentar, sedang dimasukkan database dan pembuatan laporan!")
                id_pemeriksaan_default = db.menambah_id_pemeriksaan_kesehatan_default()
                db.add_pemeriksaan_kesehatan(id_pemeriksaan_default, db.get_id_pengguna(st.session_state.username_pengguna), st.session_state.tingkat_gula_darah, st.session_state.tanggal_pemeriksaan)
                db.add_pemeriksaan_faktor_permanen(id_pemeriksaan_default, st.session_state.usia_di_atas_40_tahun, st.session_state.riwayat_keluarga_diabetes, st.session_state.riwayat_diabetes_gestasional, st.session_state.riwayat_lahir_berat_badan_lahir_rendah, st.session_state.riwayat_sindrom_ovariaum_polikistik, st.session_state.riwayat_penyakit_kardiovaskular)
                db.add_pemeriksaan_fisik(id_pemeriksaan_default, st.session_state.tinggi_badan, st.session_state.berat_badan, st.session_state.lingkar_perut, st.session_state.indeks_massa_tubuh, st.session_state.tekanan_darah)
                db.add_pemeriksaan_laboratorium(id_pemeriksaan_default, st.session_state.gula_darah_sewaktu, st.session_state.gula_darah_puasa, st.session_state.gula_darah_2_jam_setelah_makan, st.session_state.HDL, st.session_state.LDL, st.session_state.trigliserida, st.session_state.total_kolestrol)
                db.add_kebiasaan_hidup(id_pemeriksaan_default, st.session_state.konsumsi_alkohol, st.session_state.kurang_aktivitas, st.session_state.merokok, st.session_state.pola_makan_buruk, st.session_state.kurang_tidur)
                
                
                if st.session_state.gejala_terpilih is not None:
                    st.session_state.hasil_diagnosis = fc.forward_chaining(st.session_state.gejala_terpilih, relasi_dict)
                    gejala_terpilih = "; ".join(st.session_state.gejala_terpilih)
                    
                    
                    if st.session_state.hasil_diagnosis:
                        
                        for penyakit, data in st.session_state.hasil_diagnosis.items():
                            kecocokan = data["tingkat_kecocokan"] * 100
                            gejala_cocok = "; ".join(data["gejala_cocok"])
                            gejala_penyakit = "; ".join(data["gejala_penyakit"])
                            
                            
                                        
                            db.insert_diagnosis_penyakit(db.menambah_id_diagnosis_default(), st.session_state.data_pengguna[0], db.get_id_penyakit(penyakit), gejala_cocok, kecocokan, st.session_state.tanggal_pemeriksaan)
                            
                    else:   
                        st.success("Tidak ada penyakit yang terdeteksi")             
                        db.insert_diagnosis_penyakit(db.menambah_id_diagnosis_default(), st.session_state.data_pengguna[0], None, None, None, st.session_state.tanggal_pemeriksaan)
                        
                else:
                    db.insert_diagnosis_penyakit(db.menambah_id_diagnosis_default(), st.session_state.data_pengguna[0], None, None, None, st.session_state.tanggal_pemeriksaan)
                
                
                st.success("Diagnosis Berhasil dan Telah Tersimpan!")

                time.sleep(2)
                
                st.rerun()

if st.session_state.lanjut_pemeriksaan == 7:

    # Display "Faktor Tidak Bisa Diubah"
    st.subheader("Faktor Tidak Bisa Diubah")
    st.write("Usia di atas 40 tahun: " + st.session_state.usia_di_atas_40_tahun)
    st.write("Riwayat Keluarga Diabetes: " + st.session_state.riwayat_keluarga_diabetes)
    st.write("Riwayat Diabetes Gestasional: " + st.session_state.riwayat_diabetes_gestasional)
    st.write("Riwayat Lahir <2,5 kg atau Prematur: " + st.session_state.riwayat_lahir_berat_badan_lahir_rendah)

    # Display "Pola Gaya Hidup"
    st.subheader("Pola Gaya Hidup")
    st.write("Konsumsi Alkohol: " + st.session_state.konsumsi_alkohol)
    st.write("Kurang Aktivitas Fisik: " + st.session_state.kurang_aktivitas)
    st.write("Kebiasaan Merokok: " + st.session_state.merokok)
    st.write("Pola Makan Buruk: " + st.session_state.pola_makan_buruk)
    st.write("Tidur Tidak Berkualitas: " + st.session_state.kurang_tidur)

    # Display "Pemeriksaan Fisik"
    st.subheader("Pemeriksaan Fisik")
    st.write("Tinggi Badan: " + str(st.session_state.tinggi_badan) + " cm")
    st.write("Berat Badan: " + str(st.session_state.berat_badan) + " kg")
    st.write("Lingkar Perut: " + str(st.session_state.lingkar_perut) + " cm")
    st.write("Indeks Massa Tubuh: " + str(st.session_state.indeks_massa_tubuh) + " kg/m²")
    st.write("Tekanan Darah: " + str(st.session_state.tekanan_darah) + " mmHg")

    # Display "Hasil Tekanan Darah dan Kolesterol Darah"
    st.subheader("Kolesterol Darah")
    st.write("HDL: " + str(st.session_state.HDL) + " mg/dL")
    st.write("LDL: " + str(st.session_state.LDL) + " mg/dL")
    st.write("Trigliserida: " + str(st.session_state.trigliserida) + " mg/dL")
    st.write("Total Kolesterol Darah: " + str(st.session_state.total_kolestrol_darah) + " mg/dL")

    # Display "Hasil Laboratorium"
    st.subheader("Hasil Laboratorium")
    st.write("Gula Darah Sewaktu (GDS): " + str(st.session_state.gula_darah_sewaktu) + " mg/dL")
    st.write("Gula Darah Puasa (GDP): " + str(st.session_state.gula_darah_puasa) + " mg/dL")
    st.write("Gula Darah 2 Jam Setelah Makan (GD2PP): " + str(st.session_state.gula_darah_2_jam_setelah_makan) + " mg/dL")

    # Display "Diagnosis Penyakit"
    st.subheader("Diagnosis Penyakit")
    st.write("**Gejala-Gejala Terpilih:** ")
    if st.session_state.gejala_terpilih:
        for i, gejala in enumerate(st.session_state.gejala_terpilih, start=1):
            st.write(f"{i}. {gejala}")
    else:
        st.write("--")

    st.write("**Komplikasi Penyakit:** ")
    if st.session_state.hasil_diagnosis:
        for penyakit, data in st.session_state.hasil_diagnosis.items():
            kecocokan = data["tingkat_kecocokan"] * 100
            gejala_cocok = "; ".join(data["gejala_cocok"])
            gejala_penyakit = "; ".join(data["gejala_penyakit"])
            
            st.error(f"**{penyakit}: {kecocokan:.2f}%**")
            st.write(db.get_penjelasan_penyakit(penyakit))
            st.write("**Gejala yang Cocok:** ")
            for i, gejala in enumerate(gejala_cocok.split("; "), start=1):
                st.write(f"{i}. {gejala}")
            
            st.write("**Gejala Penyakit:** ")
            for i, gejala_penyakit in enumerate(gejala_penyakit.split("; "), start=1):
                st.write(f"{i}. {gejala_penyakit}")
            
            st.write("**Solusi Penyakit:** ")
            solusi_penyakit = db.get_solusi_penyakit(penyakit).split(";")
            for i, frasa in enumerate([frasa.strip() for frasa in solusi_penyakit], start=1):
                st.write(f"{i}. {frasa}")
                
            st.write("")
            st.write("")
    else:
        st.write("--")

    
    
    
    file_pdf = buat_laporan()
    
    #base64_pdf = b64encode(buat_laporan()).decode("utf-8")
    #pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
    #st.markdown(pdf_display, unsafe_allow_html=True)
    
    st.download_button(
        label="Download PDF",
        data=file_pdf,
        file_name = "Laporan Kesehatan_"+st.session_state.nama_lengkap+ "_"+str(st.session_state.tanggal_pemeriksaan)+".pdf",
        mime="application/pdf"
    )
    
    if st.button("Kembali ke Awal"):
        st.session_state.lanjut_pemeriksaan = 0
        st.session_state.hasil_diagnosis = {}
        fungsi_pemeriksaan.awal_pemeriksaan()
        st.success("Kembali ke Awal Lagi!")
        time.sleep(1)
        st.rerun()
