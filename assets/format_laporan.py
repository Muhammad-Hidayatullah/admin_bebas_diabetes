from assets import database as db
from fpdf import FPDF





def buat_laporan_riwayat(kode_pengguna, nama_lengkap, username_pengguna, tanggal_lahir, tanggal_pemeriksaan, jenis_kelamin, alamat,
                 pekerjaan, email, tingkat_gula_darah, usia_di_atas_40_tahun, riwayat_keluarga_diabetes, riwayat_diabetes_gestasional,
                 riwayat_lahir_di_bawah_2_koma_5_gram, riwayat_sindrom_ovariaum_polikistik, riwayat_penyakit_kardiovaskular, konsumsi_alkohol, kurang_aktivitas, merokok, pola_makan_buruk,
                 kurang_tidur, tinggi_badan, berat_badan, lingkar_perut, indeks_massa_tubuh, tekanan_darah, HDL, LDL, trigliserida,
                 total_kolestrol_darah, gula_darah_sewaktu, gula_darah_puasa, gula_darah_2_jam_setelah_makan, gejala_terpilih, diagnosis_penyakit_tertentu, relasi_penyakit_dan_gejala):
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
        ['Kode Pengguna: ', kode_pengguna],
        ['Nama: ', nama_lengkap],
        ["Username: ", username_pengguna],
        ["Tanggal Lahir: ", str(tanggal_lahir)],
        ["Tanggal Pemeriksaan", str(tanggal_pemeriksaan)],
        ['Jenis Kelamin: ', jenis_kelamin],
        ['Alamat: ', alamat],
        ['Pekerjaan: ', pekerjaan],
        ['Email: ', email],
        ["Tingkat Gula Darah: ", tingkat_gula_darah]
    ]
    for row in data_pribadi:
        pdf.cell(75, 10, row[0], 1)
        
        if row[0] == "Tingkat Gula Darah: ":
            if row[1] == "PREDIABETES":
                pdf.set_text_color(139, 128, 0)  # Kuning
            elif row[1] == "DIABETES":
                pdf.set_text_color(255, 0, 0)  # Merah
            elif row[1] == "NORMAL":
                pdf.set_text_color(107, 163, 108)  # Merah
            else:  # Normal
                pdf.set_text_color(0, 128, 0)  # Hijau
                
        pdf.cell(120, 10, row[1], 1)
        pdf.set_text_color(0, 0, 0)
        pdf.ln()  #
    
      # Return PDF as a string
    pdf.ln()    
    
    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Faktor Tidak Bisa Diubah", ln=True)
    pdf.set_font("Arial", size=10)
    
    pola_gaya_hidup = [
        ["Usia di atas 40 tahun: ", usia_di_atas_40_tahun],
        ["Riwayat Keluarga Diabetes: ", riwayat_keluarga_diabetes],
        ["Riwayat Diabetes Gestasional: ", riwayat_diabetes_gestasional],
        ["Riwayat Lahir <2,5 kg atau Prematur: ", riwayat_lahir_di_bawah_2_koma_5_gram],
        ["Riwayat Sindrom Ovarium Polikistik: ", riwayat_sindrom_ovariaum_polikistik],
        ["Riwayat Penyakit Kardiovaskular: ", riwayat_penyakit_kardiovaskular],
         
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
        ["Konsumsi Alkohol: ", konsumsi_alkohol],
        ["Kurang Aktivitas Fisik: ", kurang_aktivitas],
        ["Kebiasaan Merokok: ", merokok],
        ["Pola Makan Buruk : ", pola_makan_buruk],
        ["Tidur Tidak Berkualitas: ", kurang_tidur],
        
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
        ["Tinggi Badan: ", str(tinggi_badan)+" cm", "-"],
        ["Berat Badan: ", str(berat_badan)+" kg", "-"],
        ["Lingkar Perut: ", str(lingkar_perut)+" cm", " Pria <90cm , Wanita <80cm"],
        ["Indeks Massa Tubuh: ", str(indeks_massa_tubuh)+" kg/m2", " <=23 kg/m2"],
        ["Tekanan Darah: ", str(tekanan_darah)+ " mmHg", " <140/90 mmHg"],
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
        ["HDL : ", str(HDL)+" mg/dL", " >=50 mg/dL"],
        ["LDL : ", str(LDL)+" mg/dL", " <=100 mg/dL"],
        ["Trigliserida : ", str(trigliserida)+" mg/dL", " <=150 mg/dL"],
        ["Total Kolestrol Darah: ", str(total_kolestrol_darah)+" mg/dL", " <200 mg/dL"],
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
        ["Gula Darah Sewaktu (GDS): ", str(gula_darah_sewaktu)+" mg/dL", " <140 mg/dL"],
        ["Gula Darah Puasa (GDP): ", str(gula_darah_puasa)+" mg/dL", " <100 mg/dL"],
        ["Gula Darah 2 Jam Setelah Makan (GD2PP): ", str(gula_darah_2_jam_setelah_makan)+" mg/dL", " <140 mg/dL"],

    ]
    
    for row in hasil_laboratorium:
        pdf.cell(90, 10, row[0], 1)
        pdf.cell(50, 10, row[1], 1) 
        pdf.cell(50, 10, row[2], 1) 
        pdf.ln()
    
    pdf.ln(120)
    
    
    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(100, 10, txt=f"Catatan Penting: Anda Tetap Harus Mengunjungi Dokter Untuk Mendapatkan Penanganan yang Tepat", ln=True)
    pdf.set_font("Arial", size=18, style="B")
    pdf.cell(75, 10, txt="Diagnosis Penyakit", ln=True)
    
    pdf.set_font("Arial", size=13, style="B")
    pdf.cell(75, 10, txt="Gejala-Gejala Terpilih", ln=True)
    pdf.set_font("Arial", size=10)
    
    if gejala_terpilih is not None:
        #daftar_gejala_terpilih = gejala_terpilih.split("; ")
        for i, gejala in enumerate(gejala_terpilih, start=1):
            pdf.multi_cell(0, 10, txt=f"{i}. {gejala}")
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
    if diagnosis_penyakit_tertentu is not None:
        for index, row in diagnosis_penyakit_tertentu.iterrows():  
            if row['Nama Penyakit'] is None:
                pdf.set_font("Arial", size=10)
                pdf.cell(200, 10, txt=f"--", ln=True)
            else:
                pdf.set_font("Arial", size=10, style="B")
                pdf.cell(200, 10, txt=f"{row['Nama Penyakit']} : {row['Persentase Kecocokan']:.2f}%", ln=True)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 10, txt=f"{db.get_penjelasan_penyakit(row['Nama Penyakit'])}")
            
            if pdf.get_y() > 220:
                pdf.ln(200)
                
            pdf.set_font("Arial", size=10, style="B")
            pdf.cell(200, 10, txt=f"Gejala yang Cocok", ln=True)
            pdf.set_font("Arial", size=10)
            daftar_gejala = row['Gejala Cocok']
            if daftar_gejala is None:
                pdf.cell(200, 10, txt=f"-", ln=True)
            else:
                daftar_gejala = daftar_gejala.split("; ")
            
                for i, gejala_cocok in enumerate(daftar_gejala, start=1):
                    pdf.multi_cell(0, 10, txt=f"{i}. {gejala_cocok}")
                
            pdf.ln(5)
            if pdf.get_y() > 220:
                pdf.ln(200)
                
            pdf.set_font("Arial", size=10, style="B")
            pdf.cell(200, 10, txt=f"Gejala Penyakit", ln=True)
            pdf.set_font("Arial", size=10)
            
            if row['Nama Penyakit'] is None:
                pdf.cell(200, 10, txt=f"-", ln=True)
            else:
                if relasi_penyakit_dan_gejala is not None:
                    gejala_penyakit = relasi_penyakit_dan_gejala[row['Nama Penyakit']]
                    
                    for i, gejala in enumerate(gejala_penyakit, start=1):
                        pdf.multi_cell(0, 10, txt=f"{i}. {gejala}")
        
                #Solusi
                pdf.ln(5)
                if pdf.get_y() > 220:
                    pdf.ln(200)
                pdf.set_font("Arial", size=10, style="B")
                pdf.multi_cell(0, 10, txt=f"Solusi Penyakit")
                pdf.set_font("Arial", size=10)
                
                solusi_penyakit = db.get_solusi_penyakit(row['Nama Penyakit'])
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
        pdf.cell(200, 10, txt="Tidak ada penyakit yang cocok", ln=True)
    
    #return pdf.output(dest="S").encode("latin1")
    return bytes(pdf.output())
    
