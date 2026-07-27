# 🎯 Sistem Pencari Lowongan Kerja Otomatis

Aplikasi Python untuk mencari lowongan kerja dari JobStreet secara otomatis dengan data lengkap dan jelas. Dilengkapi dengan menu interaktif untuk memilih kota dan kategori pekerjaan.

## ✨ Fitur Utama

- **Input Fleksibel**: Ketik langsung nama kota dan posisi yang diinginkan (tidak perlu pilih nomor)
- **Contoh Kota & Pekerjaan**: Tampilan contoh kota dan kategori populer sebagai referensi
- **Unlimited Halaman**: Bisa scrape semua halaman atau batasi sesuai kebutuhan
- **Data Lengkap**: 
  - Posisi/Jabatan
  - Nama Perusahaan
  - Lokasi
  - Informasi Gaji
  - Tipe Pekerjaan (Full-time/Part-time)
  - Pengalaman yang Dibutuhkan
  - Tingkat Pendidikan
  - Tanggal Posting
  - Deskripsi Singkat
  - Link Lowongan
  - Waktu Scraping
- **Export ke CSV**: Data tersimpan rapi dalam format Excel-compatible
- **Ringkasan Otomatis**: Statistik hasil pencarian ditampilkan di akhir
- **Anti-Bot Protection**: User agent customization untuk menghindari deteksi bot
- **Auto Pagination**: Navigasi otomatis ke halaman berikutnya sampai selesai

## 📋 Prasyarat

Sebelum menggunakan aplikasi ini, pastikan Anda telah menginstall:

- Python 3.7 atau lebih tinggi
- pip (Python package manager)

## 🚀 Instalasi

### 1. Clone atau Download Repository

```bash
cd /workspace
```

### 2. Buat Virtual Environment (Rekomendasi untuk Linux)

Menggunakan virtual environment sangat disarankan untuk mengisolasi dependensi proyek:

```bash
# Install virtualenv jika belum terinstall
pip install virtualenv

# Buat virtual environment dengan nama 'venv'
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate
```

Setelah diaktifkan, prompt terminal akan berubah menjadi:
```bash
(venv) user@linux:~/workspace$
```

**Catatan**: Setiap kali Anda ingin menggunakan aplikasi ini, aktifkan terlebih dahulu virtual environment dengan perintah `source venv/bin/activate`

### 3. Install Dependencies

Install library Playwright dalam virtual environment:

```bash
pip install playwright
```

### 4. Install Browser Chromium

Playwright memerlukan browser untuk scraping:

```bash
playwright install chromium
```

**Untuk Linux**: Jika terjadi error terkait dependencies sistem, install juga dependencies berikut:

```bash
# Untuk Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2

# Untuk Fedora/RHEL
sudo dnf install -y alsa-lib libatk-bridge2.0 libatk cups-libs libdrm libxkbcommon xorg-x11-server-Xwayland libXcomposite libXdamage libXfixes libXrandr libGBM libpango cairo glibc
```

## 📖 Cara Menggunakan

### Langkah 1: Aktifkan Virtual Environment (Linux)

Sebelum menjalankan aplikasi, pastikan virtual environment sudah aktif:

```bash
source venv/bin/activate
```

Anda akan melihat `(venv)` di awal prompt terminal.

### Langkah 2: Jalankan Aplikasi

```bash
python jalan_otomatis.py
```

### Langkah 3: Pilih Kota

Aplikasi akan menampilkan contoh kota-kota populer. **Ketik langsung nama kota** yang diinginkan.

```
📋 KOTA POPULER (contoh):
----------------------------------------
   • Jakarta
   • Bandung
   • Surabaya
   ... dan 15 kota lainnya

💡 Ketik nama kota apa saja (misal: Jakarta, Bandung, Surabaya)

🏙️  Masukkan nama kota: 
```

### Langkah 4: Pilih Posisi/Kata Kunci

**Ketik langsung posisi atau kata kunci** pekerjaan yang dicari.

```
💼 KATEGORI PEKERJAAN POPULER (contoh):
----------------------------------------
   • Administrasi
   • Akuntansi
   • Customer Service
   ... dan 16 kategori lainnya

💡 Ketik posisi/kata kunci apa saja (misal: Admin, Programmer, Sales)

💼 Masukkan posisi/kata kunci: 
```

### Langkah 5: Atur Opsi Pencarian

- **Batas Jumlah Halaman**: Kosongkan untuk unlimited ( scrape semua halaman ), atau isi angka tertentu
- **Mode Debug**: Lihat browser berjalan (y/n, default: n)

```
⚙️  OPSI PENCARIAN:
----------------------------------------
   Batas jumlah halaman (kosongkan untuk unlimited): 
   Lihat browser berjalan? (y/n, default n): 
```

### Langkah 6: Tunggu Proses Scraping

Aplikasi akan menampilkan progress pencarian secara real-time.

### Langkah 7: Lihat Hasil

Setelah selesai, Anda akan melihat:
- Ringkasan total lowongan ditemukan
- Jumlah perusahaan unik
- Variasi lokasi
- Distribusi tipe pekerjaan
- Preview 5 lowongan pertama

### Langkah 8: Buka File CSV

Data tersimpan otomatis dengan format:
```
loker_[posisi]_[kota]_[timestamp].csv
```

Buka file CSV dengan Excel, Google Sheets, atau aplikasi spreadsheet lainnya.

## 📊 Contoh Output CSV

| No | Posisi | Perusahaan | Lokasi | Gaji | Tipe Pekerjaan | Pengalaman | Pendidikan | Tanggal Posting | Deskripsi Singkat | Link | Waktu Scraping |
|----|--------|------------|--------|------|----------------|------------|------------|-----------------|-------------------|------|----------------|
| 1 | Staff Administrasi | PT ABC | Jakarta | Rp 4-6 Juta | Full Time | 1 tahun | D3 | 2 hari lalu | Bertanggung jawab... | https://... | 2024-01-15 10:30:00 |

## 🏙️ Contoh Kota yang Bisa Digunakan

Anda bisa mengetik nama kota apa saja, contohnya:
- Jakarta
- Bandung
- Surabaya
- Yogyakarta
- Semarang
- Medan
- Denpasar
- Makassar
- Tangerang
- Bekasi
- Dan kota lainnya di Indonesia

## 💼 Contoh Posisi/Kata Kunci

Anda bisa mengetik posisi atau kata kunci apa saja, contohnya:
- Administrasi
- Programmer
- Sales
- Marketing
- Engineer
- Designer
- Accountant
- Customer Service
- Data Entry
- Dan posisi lainnya

## ⚠️ Catatan Penting

1. **Koneksi Internet**: Pastikan koneksi internet stabil selama proses scraping
2. **Rate Limiting**: Jangan scrape terlalu banyak halaman sekaligus untuk menghindari blokir
3. **Terms of Service**: Gunakan aplikasi ini dengan bijak dan hormati ketentuan JobStreet
4. **Data Accuracy**: Data yang ditampilkan adalah snapshot pada waktu scraping
5. **Browser Visibility**: Gunakan mode debug (y) jika mengalami masalah untuk melihat proses secara visual

## 🛠️ Troubleshooting

### Error: "playwright tidak ditemukan"
```bash
# Pastikan virtual environment aktif
source venv/bin/activate
pip install playwright
playwright install chromium
```

### Error: "ModuleNotFoundError: No module named 'playwright'"
```bash
# Aktifkan virtual environment terlebih dahulu
source venv/bin/activate
pip install playwright
```

### Error: "Timeout menunggu job cards"
- Periksa koneksi internet
- Coba jalankan ulang dengan mode debug (y)
- Kurangi jumlah halaman yang discrape

### Error: "Tidak ditemukan lowongan"
- Coba kata kunci yang lebih umum
- Periksa apakah lokasi sudah benar
- Website mungkin sedang maintenance

### Error: "Terdeteksi sebagai bot"
- Gunakan mode debug untuk melihat apa yang terjadi
- Tunggu beberapa saat sebelum mencoba lagi
- Kurangi kecepatan scraping dengan menambah delay

### Error: "Missing dependencies di Linux"
Install dependencies sistem yang diperlukan:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2
```

### Deaktivasi Virtual Environment
Jika ingin keluar dari virtual environment:
```bash
deactivate
```

## 📝 Struktur File

```
/workspace/
├── jalan_otomatis.py      # Script utama aplikasi
├── README.md              # Dokumentasi (file ini)
├── venv/                  # Virtual environment (dibuat otomatis)
│   ├── bin/
│   │   ├── activate       # Script untuk aktifkan virtual environment
│   │   ├── python         # Python interpreter dalam venv
│   │   └── pip            # Pip dalam venv
│   └── lib/
└── loker_*.csv           # File output (dibuat otomatis)
```

## 💡 Tips untuk Pengguna Linux

1. **Selalu gunakan virtual environment** untuk mengisolasi dependensi proyek
2. **Aktifkan venv setiap kali** ingin menjalankan aplikasi: `source venv/bin/activate`
3. **Cek apakah venv aktif** dengan melihat ada `(venv)` di prompt terminal
4. **Install dependencies sistem** jika playwright error saat install chromium
5. **Gunakan mode debug** (`y`) jika mengalami masalah untuk melihat browser berjalan
6. **Deaktivasi venv** dengan perintah `deactivate` jika sudah selesai

## 🔧 Kustomisasi

### Menambah Kota Baru

Edit bagian `CITIES` di `jalan_otomatis.py`:

```python
CITIES = [
    "Jakarta",
    "Bandung",
    # Tambah kota baru di sini
    "Kota Baru",
]
```

### Menambah Kategori Pekerjaan

Edit bagian `JOB_CATEGORIES` di `jalan_otomatis.py`:

```python
JOB_CATEGORIES = [
    "Administrasi",
    # Tambah kategori baru di sini
    "Kategori Baru",
]
```

### Mengubah Jumlah Halaman Maksimum

Edit fungsi `get_search_options()`:

```python
if 1 <= pages <= 20:  # Ubah dari 10 menjadi 20
```

## 📄 License

Gunakan aplikasi ini dengan bijak dan bertanggung jawab.

## 🤝 Kontribusi

Silakan fork dan submit pull request untuk improvement!

## 📞 Support

Jika mengalami masalah, silakan:
1. Baca bagian Troubleshooting di atas
2. Pastikan semua dependencies terinstall
3. Jalankan dengan mode debug untuk melihat detail error

---

**Happy Job Hunting! 🎉**
