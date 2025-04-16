#return bytes(pdf.output())

#return pdf.output(dest="S").encode("latin1")

import streamlit as st
import pandas as pd

st.markdown(
    """
    <style>
    [data-testid="stHeader"]{
        background-color: none;
        
    </style>

    """, unsafe_allow_html=True
)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DA;">
  <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

# Sample DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Class": ["10A", "11B", "12C"],
    "Student ID": [101, 102, 103],
    "Birthdate": ["2005-01-01", "2004-02-15", "2003-03-22"],
    "Birthcity": ["New York", "Los Angeles", "Chicago"]
}
df = pd.DataFrame(data)

# Drop unnecessary columns
df_cleaned = df.drop(columns=["Birthdate", "Birthcity"])

# Custom CSS for styling
table_style = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
            font-size: 16px;
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
            background-color: #f9f9f9; /* Light gray for alternating rows */
        }
    </style>
"""

# Convert DataFrame to HTML
table_html = df_cleaned.to_html(index=False, escape=False)

# Display in Streamlit
st.markdown(table_style + table_html, unsafe_allow_html=True)


from fpdf import FPDF

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=10)  # Aktifkan pemutusan halaman otomatis dengan margin 10 mm
pdf.add_page()

pdf.set_font("Arial", size=12)

for i in range(1, 50):  # Coba masukkan 50 baris teks
    if pdf.get_y() > 270:  # Jika teks mendekati batas bawah, tambah halaman
        pdf.add_page()
    pdf.cell(0, 10, f"Baris ke-{i}", ln=True)

pdf.output("output.pdf")

from base64 import b64encode
def test():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for i in range(1, 50):
        if pdf.get_y() > 210:  # Jika mendekati batas bawah, beri spasi 10 mm
            pdf.ln(200)
        pdf.cell(0, 10, f"Teks ke-{i}", ln=True)

    return bytes(pdf.output())

base64_pdf = b64encode(test()).decode("utf-8")
pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
st.markdown(pdf_display, unsafe_allow_html=True)

