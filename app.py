import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(page_title="Mini Dashboard", page_icon="📊")

st.title("📊 Mini Dashboard + PDF Reader")

# ======================
# INPUT USER
# ======================
st.header("📝 Input Data")

nama = st.text_input("Nama kamu")
umur = st.number_input("Umur", 0, 100)
hobi = st.text_input("Hobi kamu")

if st.button("Submit"):
    st.success(f"Halo {nama} 👋")
    st.write("Umur:", umur)
    st.write("Hobi:", hobi)

# ======================
# CSV UPLOAD
# ======================
st.header("📂 Upload CSV")

csv_file = st.file_uploader("Upload file CSV", type=["csv"])

if csv_file:
    df = pd.read_csv(csv_file)
    st.dataframe(df)
    st.write(df.describe())

# ======================
# PDF UPLOAD
# ======================
st.header("📄 Upload PDF")

pdf_file = st.file_uploader("Upload file PDF", type=["pdf"])

if pdf_file:
    reader = PdfReader(pdf_file)

    st.write(f"Jumlah halaman: {len(reader.pages)}")

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    st.subheader("Isi PDF:")
    st.write(text)
