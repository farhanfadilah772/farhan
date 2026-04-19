
import pdfplumber
import re
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- GOOGLE SHEETS SETUP ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)
sheet = client.open("Rekap Invoice").sheet1


def extract_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([p.extract_text() for p in pdf.pages])

    vendor = re.search(r"Nama:\s*(.+)", text)

    invoice_number = (
        re.search(r"INVOICE #\s*(.+)", text) or
        re.search(r"Invoice number:\s*(.+)", text) or
        re.search(r"Invoice No\s*:\s*(.+)", text)
    )

    invoice_date = (
        re.search(r"Tanggal Invoice\s*:\s*(.+)", text) or
        re.search(r"Invoice date\s*[:]*\s*(.+)", text) or
        re.search(r"\d{2} \w+ \d{4}", text)
    )

    description = (
        re.search(r"Tagihan Pra Bayar.*", text) or
        re.search(r"Google Cloud", text) or
        re.search(r"Connectivity.*", text)
    )

    amount = (
        re.search(r"Jumlah Tagihan\s*([\d\.,]+)", text) or
        re.search(r"Total amount due.*IDR\s*([\d\.,]+)", text) or
        re.search(r"Grand Total\s*([\d\.,]+)", text)
    )

    faktur = re.search(r"Kode dan Nomor Seri Faktur Pajak:\s*(\d+)", text)

    return [
        vendor.group(1) if vendor else "",
        invoice_number.group(1) if invoice_number else "",
        invoice_date.group(0) if invoice_date else "",
        description.group(0) if description else "",
        amount.group(1) if amount else "",
        faktur.group(1) if faktur else "",
        f"https://github.com/USERNAME/REPO/blob/main/{pdf_path}"
    ]


# --- HEADER (hanya sekali) ---
header = [
    "Nama Vendor",
    "Invoice Number",
    "Invoice Date",
    "Description",
    "Amount",
    "Faktur Pajak",
    "Link File"
]

if sheet.row_count == 0:
    sheet.append_row(header)


# --- LOOP FILE ---
folder = "data"

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        path = os.path.join(folder, file)
        row = extract_data(path)
        sheet.append_row(row)

print("✅ Data berhasil masuk Google Sheets!")
