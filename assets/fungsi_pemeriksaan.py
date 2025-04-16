import streamlit as st
import datetime

def variabel_awal_pengguna():
    st.session_state.next = -2
    st.session_state.kode_pasien = ""
    st.session_state.nama = ""
    st.session_state.username_pengguna = ""
    st.session_state.password_pengguna = ""
    st.session_state.tanggal_lahir = datetime.date.today()
    st.session_state.pekerjaan = ""
    st.session_state.email = ""
    # sesuai KTP
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

    
    st.session_state.tanggal_pemeriksaan = datetime.date.today()
    st.session_state.alamat = ""
    st.session_state.jenis_kelamin = "LAKI-LAKI"
    

    



def awal_pemeriksaan():
    
    st.session_state.tanggal_pemeriksaan = datetime.date.today()
    # Pemeriksaan fisik
    st.session_state.lanjut_pemeriksaan = 0
    st.session_state.berat_badan = 0.0
    st.session_state.tinggi_badan = 0.0
    st.session_state.lingkar_perut = 0.0
    
    # Faktor Tidak Bisa Diubah
    st.session_state.usia_di_atas_40_tahun = "TIDAK"
    st.session_state.riwayat_keluarga_diabetes = "TIDAK"
    st.session_state.riwayat_diabetes_gestasional = "TIDAK"
    st.session_state.riwayat_lahir_berat_badan_lahir_rendah = "TIDAK"
    st.session_state.riwayat_sindrom_ovariaum_polikistik = "TIDAK"
    st.session_state.riwayat_penyakit_kardiovaskular = "TIDAK"
    # Kebiasaan Hidup
    st.session_state.konsumsi_alkohol = "TIDAK"
    st.session_state.kurang_aktivitas = "TIDAK"
    st.session_state.kurang_tidur = "TIDAK"
    st.session_state.merokok = "TIDAK"
    st.session_state.pola_makan_buruk = "TIDAK"
    st.session_state.tingkat_risiko = "RENDAH"
    
    # Pemeriksaan Lab
    st.session_state.skip_gula_darah = 0
    st.session_state.gula_darah_sewaktu = 0.0
    st.session_state.gula_darah_puasa = 0.0
    st.session_state.gula_darah_2_jam_setelah_makan = 0.0
    st.session_state.tekanan_darah = "0/0"
    st.session_state.sistole, st.session_state.diastole = st.session_state.tekanan_darah.split("/")
    st.session_state.HDL = 0.0
    st.session_state.LDL = 0.0
    st.session_state.trigliserida = 0.0
    st.session_state.total_kolestrol = 0.0
    st.session_state.total_kolestrol_darah = 0.0 # rumusnya: LDL + HDL + 1/5 Trigliserida
    
    # Risiko
    st.session_state.tingkat_gula_darah = "-"