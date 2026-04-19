import pdfplumber
import re
import os
import pandas as pd

def extract_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([p.extract_text() for p in pdf.pages])

    # --- Vendor ---
    vendor = re.search(r"Nama:\s*(.+)", text)
    
    # --- Invoice Number (multi format) ---
    invoice_number = (
        re.search(r"INVOICE #\s*(.+)", text) or
        re.search(r"Invoice number:\s*(.+)", text) or
        re.search(r"Invoice No\s*:\s*(.+)", text)
    )

    # --- Invoice Date ---
    invoice_date = (
        re.search(r"Tanggal Invoice\s*:\s*(.+)", text) or
        re.search(r"Invoice date\s*[:]*\s*(.+)", text) or
        re.search(r"\:\s*(\d{2} \w+ \d{4})", text)
    )

    # --- Description ---
    description = (
        re.search(r"Tagihan Pra Bayar.*", text) or
        re.search(r"Google Cloud", text) or
        re.search(r"Connectivity.*", text)
    )

    # --- Amount ---
    amount = (
        re.search(r"Jumlah Tagihan\s*([\d\.,]+)", text) or
        re.search(r"Total amount due.*IDR\s*([\d\.,]+)", text) or
        re.search(r"Grand Total\s*([\d\.,]+)", text)
    )

    # --- Faktur Pajak ---
    faktur = re.search(r"Kode dan Nomor Seri Faktur Pajak:\s*(\d+)", text)

    return {
        "Nama Vendor": vendor.group(1) if vendor else "",
        "Invoice Number": invoice_number.group(1) if invoice_number else "",
        "Invoice Date": invoice_date.group(1) if invoice_date else "",
        "Description": description.group(0) if description else "",
        "Amount": amount.group(1) if amount else "",
        "Faktur Pajak": faktur.group(1) if faktur else "",
        "Link File": f"https://github.com/USERNAME/REPO/blob/main/{pdf_path}"
    }


# --- LOOP SEMUA PDF ---
folder = "data"
all_data = []

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        path = os.path.join(folder, file)
        data = extract_data(path)
        all_data.append(data)

# --- SIMPAN KE EXCEL ---
df = pd.DataFrame(all_data)
df.to_excel("rekap.xlsx", index=False)

print("✅ Rekap selesai!")
