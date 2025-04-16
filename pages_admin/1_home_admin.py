import streamlit as st

from assets import database as db

st.session_state.style_tabel = """
<style>
    table {
        width: 100%;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
        font-size: 12px;
    }
    th {
        background-color: green;
        color: white;
        padding: 10px;
        text-align: left;
    }
    td {
        background-color: white;
        padding: 10px;
        border: 1px solid #ddd;
        text-align: left;
    }
    tr:nth-child(even) td {
        background-color: #f9f9f9;
    }
</style>
"""



def kartu(total_apa, nilai):
    style_kartu = f"""
    <div style="
        width: 150px;
        padding: 5px;
        border-radius: 3px;
        background-color: #f0f2f6;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    ">
        <p style="color: #333; font-weight: bold; font-size: 18px; margin: 5px 0;">{total_apa}</p>
        <p style="font-size: 20px; font-weight: bold; color: #007BFF; margin: 5px 0;">{nilai}</p>
    </div>
    """
    st.markdown(style_kartu, unsafe_allow_html=True)

# Contoh penggunaan





st.title("DASBOR ADMIN")

col1, col2, col3 = st.columns(3)
jumlah_pengguna = db.get_jumlah_pengguna()
jumlah_penyakit = db.get_jumlah_penyakit()
jumlah_gejala = db.get_jumlah_gejala()

with col1:
    kartu("Jumlah User", jumlah_pengguna)
with col2:
    kartu("Jumlah Penyakit", jumlah_penyakit)
with col3:
    kartu("Jumlah Gejala", jumlah_gejala)

st.write("")
st.image("./assets/admin.png", width=300)

st.write("Silahkan pilih menu-menu berikut dan atur sesuai kebutuhan")


