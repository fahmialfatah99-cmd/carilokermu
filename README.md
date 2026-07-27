# 🔍 CariLokerMu - Job Portal Scraper

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Aplikasi otomatis untuk mencari lowongan kerja dari **Jobstreet** dengan fitur scraping cerdas dan export data ke CSV.

---

## ✨ Fitur Utama

| Fitur | Deskripsi | Status |
|-------|-----------|--------|
| 🔍 **Smart Scraping** | Mencari lowongan berdasarkan keyword & lokasi | ✅ Siap Pakai |
| 📊 **Export Data** | Simpan hasil pencarian ke CSV/Excel | ✅ Siap Pakai |
| 🌐 **Auto-Buka Browser** | Browser terbuka otomatis untuk proses scraping | ✅ Siap Pakai |
| ⌨️ **Ketik Otomatis** | Input field diisi otomatis seperti manusia mengetik | ✅ Siap Pakai |

---

## 📋 Prasyarat

Pastikan Anda telah menginstall:
- Python 3.8 atau lebih baru
- pip (Python package manager)

---

## 🛠️ Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/username/carilokermu.git
cd carilokermu
```

### 2. Install Dependencies Python
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Browser Engine Playwright (WAJIB!)

Ini adalah langkah yang **sering terlewatkan** dan menyebabkan error `Playwright tidak terinstall`.
Playwright membutuhkan browser engine khusus yang harus diunduh terpisah.

```bash
# Unduh dan install Chromium engine untuk Playwright
playwright install chromium

# (Opsional) Install dependencies sistem Linux jika diperlukan
playwright install-deps chromium
```

> ⚠️ **PENTING**: 
> - Jangan lewatkan langkah ini! Error `Playwright tidak terinstall` muncul karena browser engine belum diunduh.
> - Perintah ini hanya perlu dilakukan **sekali saja** setelah instalasi awal.
> - Ukuran download sekitar 100-150 MB.

---

## 🚀 Cara Penggunaan

### Cari Lowongan Kerja

```bash
python3 main.py
```

**Program akan memandu Anda melalui:**

1. **Input posisi/kata kunci** (contoh: `admin`, `data analyst`)
2. **Input lokasi/kota** (contoh: `Jakarta`, `Surabaya`)
3. **Input jumlah halaman** yang akan di-scrape (default: 3)
4. **Browser terbuka otomatis** untuk menampilkan proses scraping
5. **Input field diisi otomatis** seperti manusia mengetik
6. **Menampilkan daftar lowongan** yang ditemukan
7. **Data tersimpan ke CSV** untuk dibuka di Excel/Google Sheets

**Contoh Sesi:**
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

**Fitur Unggulan:**
- ✅ **Auto-buka browser**: Browser terbuka otomatis untuk melihat proses
- ✅ **Ketik otomatis**: Input field diisi karakter per karakter seperti manusia
- ✅ **Tanpa login**: Langsung bisa mencari lowongan tanpa perlu login

---

## 📂 Struktur Output

Setelah menjalankan program, Anda akan memiliki file CSV seperti ini:

```
carilokermu/
├── loker_admin_jakarta_20260727_160440.csv    # Hasil scraping lowongan
└── carilokermu/                                # Folder output
```

File CSV berisi kolom:
- No: Nomor urut
- Posisi: Judul lowongan
- Perusahaan: Nama perusahaan
- Lokasi: Lokasi pekerjaan
- Link: Link ke lowongan
- Halaman: Halaman tempat lowongan ditemukan

---

## 🔧 Troubleshooting

### Masalah Instalasi

| Sistem Operasi | Masalah Umum | Solusi |
|----------------|--------------|--------|
| **Linux (Ubuntu/Debian)** | `Permission denied` saat install | Gunakan: `pip3 install --user -r requirements.txt` |
| **macOS** | Certificate verify failed | Jalankan: `/Applications/Python\ 3.x/Install\ Certificates.command` |
| **Windows** | `pip` tidak dikenali | Tambahkan Python ke PATH atau gunakan `py -m pip` |
| **Semua** | Module `playwright` tidak ditemukan | Jalankan: `pip install playwright playwright-stealth` |

### Masalah Saat Running

| Masalah | Solusi |
|---------|--------|
| Browser tidak terbuka | Pastikan Chromium terinstall: `playwright install chromium` |
| CSV kosong/tidak ada data | Coba ubah keyword, tambah jumlah halaman, atau cek koneksi internet |
| Error `Connection Reset` | Tunggu 5-10 menit lalu jalankan lagi (rate limiting) |
| Script terlalu lambat | Normal, script memberi delay untuk hindari blokir |

### Tips Khusus Linux Users

```bash
# Jika Chromium tidak mau jalan sebagai root
export CHROME_ALLOW_ROOT=1

# Jika ada masalah permission pada folder output
chmod -R 755 /path/to/carilokermu/

# Cek apakah Chromium terinstall dengan benar
chromium --version

# Untuk Snap users (Ubuntu 22.04+)
sudo snap connect chromium:home
```

---

## 🚧 Batasan & Catatan

1. **Tanpa Login:** Program ini tidak memerlukan login ke Jobstreet untuk mencari lowongan
2. **Rate Limit:** Jangan jalankan terlalu cepat untuk menghindari blokir IP
3. **Captcha:** Beberapa website mungkin menampilkan captcha yang harus diselesaikan manual
4. **Update UI:** Jika Jobstreet mengubah tampilan form, script perlu diupdate

---

## 📄 License

MIT License - lihat file [LICENSE](LICENSE) untuk detail

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan buat issue atau pull request untuk:
- Menambahkan support job portal lain
- Memperbaiki bug
- Menambah fitur baru

---

## 📞 Support

Jika mengalami kendala, buka issue di GitHub atau hubungi:
- Email: support@carilokermu.com
- Telegram: @carilokermu_support

---

**Happy Job Hunting! 🎯**
