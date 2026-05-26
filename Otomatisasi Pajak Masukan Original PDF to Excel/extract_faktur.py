import pdfplumber
import pandas as pd
from pathlib import Path
import re
from datetime import datetime

# Lokasi folder tempat file PDF berada
pdf_folder = Path.home() / "Desktop" / "Otomatisasi Pajak Masukan Original PDF to Excel"
pdf_files = list(pdf_folder.glob("*.pdf"))

# Folder output untuk simpan Excel per PDF
output_folder = pdf_folder / "hasil pdf to excel"
output_folder.mkdir(exist_ok=True)

def extract_from_pdf(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

        print(f"=== DEBUG: {pdf_path.name} ===")
        print(text)

        # Nomor Faktur
        faktur_match = re.search(r"Kode dan Nomor Seri Faktur Pajak:\s*(\d+)", text)
        no_faktur = faktur_match.group(1) if faktur_match else ""

        # Tanggal Faktur (lebih fleksibel, ambil baris yang punya format tanggal)
        tanggal_match = re.search(r"(\d{1,2}\s+\w+\s+\d{4})", text)
        tanggal_str = tanggal_match.group(1) if tanggal_match else ""
        try:
            tanggal = datetime.strptime(tanggal_str, "%d %B %Y").date()
        except:
            tanggal = ""

        # DPP dan PPN
        dpp_match = re.search(r"Dasar Pengenaan Pajak\s+([\d\.]+,\d{2})", text)
        ppn_match = re.search(r"Jumlah PPN.*?([\d\.]+,\d{2})", text)
        dpp = dpp_match.group(1).replace('.', '').replace(',', '.') if dpp_match else "0"
        ppn = ppn_match.group(1).replace('.', '').replace(',', '.') if ppn_match else "0"

        # Ekstrak item barang lebih fleksibel: Piece, Boks, Dus, dll
        item_lines = re.findall(r"(.*?)\nRp\s([\d\.,]+) x ([\d\.,]+) \w+", text)

        for nama_barang, harga_str, qty_str in item_lines:
            harga = harga_str.replace('.', '').replace(',', '.')
            qty = qty_str.replace('.', '').replace(',', '.')
            try:
                total = float(harga) * float(qty)
            except:
                total = 0.0

            data.append({
                "Nama File": pdf_path.name,
                "No Faktur": no_faktur,
                "Tanggal": tanggal,
                "Barang": nama_barang.strip(),
                "Qty": float(qty),
                "Harga": float(harga),
                "Total": total,
                "DPP": float(dpp),
                "PPN": float(ppn)
            })

    # Simpan hasil ke file Excel terpisah per PDF
    df = pd.DataFrame(data)
    output_file = output_folder / f"{pdf_path.stem}.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Simpan: {output_file}")

# Proses semua PDF
total_files = len(pdf_files)
print(f"Memproses {total_files} file PDF...")
for pdf_file in pdf_files:
    extract_from_pdf(pdf_file)

print(f" Sukses Asisten Ai telah selesai : {output_folder}")
