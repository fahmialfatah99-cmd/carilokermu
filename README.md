# 🔍 CariLokerMu - Pencari Lowongan Kerja Otomatis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Aplikasi sederhana untuk mencari lowongan kerja dari **Jobstreet** tanpa login dan export hasil ke CSV.

---

## ✨ Fitur

- 🔍 **Cari Lowongan** - Berdasarkan posisi dan lokasi
- 📊 **Export CSV** - Hasil disimpan otomatis ke file CSV
- 🌐 **Browser Otomatis** - Proses scraping terlihat di browser
- ⚡ **Tanpa Login** - Langsung pakai, tidak perlu akun
- 🤖 **Anti-Deteksi** - Stealth mode untuk menghindari blokir

---

## 📋 Prasyarat

- Python 3.8 atau lebih baru
- pip (Python package manager)

---

## 🛠️ Instalasi

### 1. Clone atau Download Repository

```bash
git clone https://github.com/username/carilokermu.git
cd carilokermu
```

### 2. Buat Virtual Environment (Disarankan)

Virtual environment membuat dependencies terisolasi dan tidak mengganggu sistem utama.

#### **Windows (CMD/PowerShell)**
```bash
python -m venv venv
venv\Scripts\activate
```

#### **macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

Setelah aktivasi, akan muncul `(venv)` di awal terminal.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Browser Engine Playwright (WAJIB!)

Playwright butuh browser engine khusus yang harus diunduh terpisah:

```bash
playwright install chromium
```

**Untuk Linux (Ubuntu/Debian)**, mungkin perlu install dependencies tambahan:
```bash
playwright install-deps chromium
```

> ⚠️ **PENTING**: Langkah ini hanya dilakukan **sekali saja** setelah instalasi pertama.

---

## 🚀 Cara Penggunaan

### Jalankan Program

```bash
python main.py
```

**atau jika di Windows:**
```bash
py main.py
```

### Alur Program:

1. **Input posisi** (contoh: `Admin`, `Data Analyst`)
2. **Input lokasi** (contoh: `Jakarta`, `Surabaya`)
3. **Input jumlah halaman** (default: 3)
4. **Browser terbuka** dan proses scraping berjalan otomatis
5. **Hasil ditampilkan** di terminal
6. **Data tersimpan** ke file CSV

### Contoh Output:

```
============================================================
🔍 PENCARI LOWONGAN KERJA OTOMATIS (JOBSTREET)
============================================================

💼 Posisi / Kata Kunci (contoh: Admin, Staff Gudang): Admin
📍 Lokasi / Kota (contoh: Jakarta, Surabaya): Jakarta
📄 Jumlah Halaman (default 3): 3

⏳ Memulai pencarian: 'Admin' di 'Jakarta'...
------------------------------------------------------------
🌐 Membuka Jobstreet.co.id...
⌨️ Mengetik posisi: 'Admin'...
⌨️ Mengetik lokasi: 'Jakarta'...
🔍 Mengklik tombol cari...

📄 Memproses Halaman 1...
   Ditemukan 10 lowongan di halaman ini.
   [1] Staff Administrasi - PT Maju Jaya
   [2] Admin Officer - CV Berkah Sentosa
   ...

============================================================
✅ SELESAI! Total lowongan ditemukan: 30
💾 Disimpan ke: loker_admin_jakarta_20260727_160440.csv
============================================================
```

---

## 📂 Hasil Output

File CSV tersimpan di folder yang sama dengan nama format:
```
loker_{posisi}_{lokasi}_{tanggal_waktu}.csv
```

**Kolom CSV:**
- No: Nomor urut
- Posisi: Judul lowongan
- Perusahaan: Nama perusahaan
- Lokasi: Lokasi pekerjaan
- Link: Link ke lowongan
- Halaman: Halaman tempat ditemukan

---

## 🔧 Troubleshooting

### Error Umum & Solusi

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError: No module named 'playwright'` | Jalankan: `pip install playwright playwright-stealth` |
| `Playwright tidak terinstall` | Jalankan: `playwright install chromium` |
| Browser tidak terbuka | Pastikan langkah install Chromium sudah dilakukan |
| CSV kosong | Coba keyword lain, tambah halaman, atau cek koneksi internet |
| Error connection/reset | Tunggu beberapa menit (rate limiting dari website) |

### Panduan Per OS

#### **Windows**
- Jika `pip` tidak dikenali, gunakan: `py -m pip install -r requirements.txt`
- Pastikan Python ditambahkan ke PATH
- Gunakan PowerShell atau CMD sebagai administrator jika ada error permission

#### **macOS**
- Jika ada error certificate, jalankan: `/Applications/Python\ 3.x/Install\ Certificates.command`
- Gunakan `python3` bukan `python`

#### **Linux (Ubuntu/Debian)**
- Install dependencies sistem: `sudo apt-get install -y libgbm1 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libpango-1.0-0 libcairo2 libglib2.0-0 libdrm2 libdbus-1-3 libatspi2.0-0`
- Atau gunakan: `playwright install-deps chromium`
- Jika running sebagai root, tambahkan: `export CHROME_ALLOW_ROOT=1`

---

## 🚧 Catatan Penting

1. **Tanpa Login** - Program tidak memerlukan login ke Jobstreet
2. **Rate Limit** - Jangan jalankan terlalu cepat untuk menghindari blokir IP
3. **Captcha** - Website mungkin menampilkan captcha yang harus diselesaikan manual
4. **UI Changes** - Jika tampilan Jobstreet berubah, script mungkin perlu update

---

## 📄 License

MIT License - Silakan digunakan dan dimodifikasi sesuai kebutuhan.

---

**Happy Job Hunting! 🎯**
