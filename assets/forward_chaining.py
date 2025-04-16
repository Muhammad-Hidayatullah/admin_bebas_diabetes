

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
    
    # Memfilter penyakit berdasarkan tingkat kecocokan
    hasil = {
        penyakit: data
        for penyakit, data in kemungkinan_penyakit.items()
        if data["tingkat_kecocokan"] > 0.00
    }
    
    return hasil

