import pdfplumber
import re

def extract_invoice(file_path):
    result = {}

    with pdfplumber.open(file_path) as pdf:
        text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

    # 🔑 Invoice Number
    inv = re.search(r'INV/[A-Z/0-9]+', text)
    if inv:
        result['invoice_no'] = inv.group()

    # 📅 Tanggal
    date = re.search(r'Tanggal Invoice\s*:\s*(.*)', text)
    if date:
        result['invoice_date'] = date.group(1).strip()

    due = re.search(r'Tanggal Jatuh Tempo\s*:\s*(.*)', text)
    if due:
        result['due_date'] = due.group(1).strip()

    # 💰 Total
    total = re.search(r'Jumlah Tagihan\s*([\d.,]+)', text)
    if total:
        result['total'] = total.group(1)

    # 💸 PPN
    ppn = re.search(r'PPN.*\s([\d.,]+)', text)
    if ppn:
        result['ppn'] = ppn.group(1)

    # 📦 Qty
    qty = re.search(r'untuk\s*(\d+)\s*orang', text)
    if qty:
        result['qty'] = qty.group(1)

    # 🏢 Customer
    cust = re.search(r'Ditujukan kepada\s*:\s*(.*?)\n', text)
    if cust:
        result['customer'] = cust.group(1)

    return result

import streamlit as st

uploaded_file = st.file_uploader("Upload Invoice", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    data = extract_invoice("temp.pdf")

    st.json(data)
