# 🚀 Job Scraper Otomatis & Manual

Tool scraping lowongan kerja yang fleksibel, mendukung **Linux**, **Windows**, dan **macOS**. Tersedia dalam dua mode: **Otomatis (Interaktif)** dan **Manual (Config Code)**.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Playwright](https://img.shields.io/badge/playwright-latest-success)

## ✨ Fitur Utama

- ✅ **Tanpa Batas Halaman**: Default scraping berjalan terus hingga data habis (bisa dibatasi manual).
- ✅ **Multi-Platform**: Panduan instalasi lengkap untuk Linux, Windows, dan Mac.
- ✅ **Dua Mode Penggunaan**:
  - **Easy Mode**: Tinggal jalankan, jawab pertanyaan, selesai.
  - **Pro Mode**: Edit konfigurasi langsung di kode untuk kontrol penuh.
- ✅ **Anti-Deteksi**: Menggunakan teknik stealth untuk menghindari blokir sederhana.
- ✅ **Export CSV**: Hasil tersimpan rapi dalam format Excel/CSV.
- ✅ **Logging**: Memantau proses scraping secara real-time.

---

## 📋 Prasyarat

Pastikan Python 3.8+ sudah terinstal di sistem Anda.

### 1. Instalasi di Linux (Ubuntu/Debian/Kali/Mint)

```bash
# Update paket
sudo apt update

# Install Python & Pip
sudo apt install python3 python3-pip python3-venv -y

# Buat virtual environment (opsional tapi disarankan)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install browser Playwright
playwright install chromium
playwright install-deps chromium
```

### 2. Instalasi di Windows

```bash
# Install Python dari python.org (pastikan centang "Add to PATH")

# Buka Command Prompt atau PowerShell
pip install -r requirements.txt

# Install browser Playwright
playwright install chromium
```

### 3. Instalasi di macOS

```bash
# Install Python via Homebrew
brew install python

# Install dependencies
pip install -r requirements.txt

# Install browser Playwright
playwright install chromium
```

---

## 📁 Struktur File

| File | Deskripsi | Mode | Tingkat Kesulitan |
|------|-----------|------|-------------------|
| `easy_search.py` | Scraper interaktif dengan input user | Otomatis | ⭐ Mudah |
| `main.py` | Scraper dengan konfigurasi di kode | Manual | ⭐⭐ Menengah |
| `jalan_otomatis.py` | Scraper interaktif dengan menu lengkap | Otomatis | ⭐⭐ Menengah |

---

## 🚀 Cara Penggunaan

### Mode 1: Easy Search (Paling Mudah)

Cocok untuk pemula yang ingin cepat mendapatkan hasil tanpa edit kode.

```bash
python easy_search.py
```

**Langkah-langkah:**
1. Jalankan script
2. Masukkan posisi/jabatan yang dicari (contoh: Administrasi)
3. Masukkan kota/lokasi (contoh: Jakarta Selatan)
4. Tentukan jumlah halaman (tekan Enter untuk tanpa batas)
5. Pilih apakah ingin melihat browser berjalan (y/n)
6. Hasil akan tersimpan otomatis dalam format CSV

**Contoh Output:**
```
loker_administrasi_jakarta_selatan.csv
```

---

### Mode 2: Main.py (Konfigurasi Kode)

Cocok untuk pengguna yang ingin kontrol penuh atas parameter scraping.

**Langkah-langkah:**
1. Buka file `main.py` di text editor
2. Edit bagian konfigurasi di baris 14-19:

```python
KEYWORD = "Administrasi"           # Kata kunci pencarian
LOCATION_FILTER = "Jakarta Selatan" # Lokasi yang diinginkan
BASE_URL = "https://id.jobstreet.com/id/jobs/in-Jakarta-Selatan-Jakarta-Raya"
MAX_PAGES = 0                       # 0 = Unlimited, 5 = 5 halaman
OUTPUT_FILE = "loker_admin.csv"     # Nama file output
HEADLESS = True                     # True = browser tersembunyi
```

3. Simpan file
4. Jalankan:

```bash
python main.py
```

---

### Mode 3: Jalan Otomatis (Menu Interaktif Lengkap)

Cocok untuk pengguna yang menginginkan pengalaman interaktif dengan menu lengkap.

```bash
python jalan_otomatis.py
```

**Fitur Khusus:**
- Menu interaktif dengan daftar kota dan kategori populer
- Input user-friendly dengan validasi
- Ringkasan statistik hasil scraping
- Data lebih lengkap (gaji, tipe pekerjaan, pengalaman, pendidikan, dll)

**Data yang Diambil:**
- No
- Posisi
- Perusahaan
- Lokasi
- **Gaji** 💰
- Tipe Pekerjaan
- Pengalaman
- Pendidikan
- Tanggal Posting
- Deskripsi Singkat
- Link
- Waktu Scraping

---

## 📊 Format Output CSV

Semua script menghasilkan file CSV dengan kolom berikut:

| Kolom | Deskripsi |
|-------|-----------|
| Judul/Posisi | Nama jabatan/posisi pekerjaan |
| Perusahaan | Nama perusahaan |
| Lokasi | Lokasi pekerjaan |
| **Gaji** | Informasi gaji (jika tersedia) |
| Link | URL lengkap ke lowongan |
| Sumber | Domain website sumber |

*Catatan: `jalan_otomatis.py` memiliki kolom tambahan yang lebih detail*

---

## ⚙️ Konfigurasi Lanjutan

### Membatasi Jumlah Halaman

Untuk menghemat waktu, Anda bisa membatasi jumlah halaman yang discrape:

- **easy_search.py**: Input angka saat diminta "Jumlah halaman"
- **main.py**: Ubah `MAX_PAGES = 5` (ganti 5 dengan angka yang diinginkan)
- **jalan_otomatis.py**: Input angka saat diminta "Batas jumlah halaman"

### Mode Debug (Melihat Browser)

Jika ingin melihat proses scraping secara visual:

- **easy_search.py**: Jawab 'y' saat ditanya "Tampilkan browser?"
- **main.py**: Ubah `HEADLESS = False`
- **jalan_otomatis.py**: Jawab 'y' saat ditanya "Lihat browser berjalan?"

### Mengubah Website Target

Script ini dirancang untuk JobStreet Indonesia. Untuk mengubah ke website lain:

1. Edit selector CSS di fungsi `scrape_page()`
2. Sesuaikan struktur URL di fungsi pembuat URL
3. Update field yang diambil sesuai struktur website baru

---

## 🔧 Troubleshooting

### Error: "playwright not found"
```bash
playwright install chromium
```

### Error: "No module named 'bs4'"
```bash
pip install beautifulsoup4
```

### Error: "No module named 'playwright'"
```bash
pip install playwright
playwright install chromium
```

### Scraping Berhenti di Tengah Jalan
- Website mungkin mendeteksi bot, coba gunakan mode debug (`HEADLESS = False`)
- Kurangi kecepatan dengan menambah delay di `asyncio.sleep()`
- Pastikan koneksi internet stabil

### Data yang Diambil Sedikit/Nol
- Selector CSS mungkin sudah berubah, update selector di kode
- Website menggunakan lazy loading, tambah timeout
- Coba ganti keyword atau lokasi pencarian

---

## 📝 Catatan Penting

1. **Etika Scraping**: 
   - Gunakan dengan bijak dan jangan overload server
   - Patuhi robots.txt website target
   - Gunakan untuk keperluan pribadi/edukasi

2. **Legalitas**:
   - Data yang diambil adalah data publik
   - Jangan gunakan untuk komersialisasi tanpa izin
   - Hormati hak cipta dan ketentuan website

3. **Kinerja**:
   - Scraping tanpa batas bisa memakan waktu lama
   - Disarankan batasi halaman untuk testing awal
   - File CSV besar bisa dibuka dengan Excel, Google Sheets, atau LibreOffice Calc

4. **Update Berkala**:
   - Struktur website bisa berubah sewaktu-waktu
   - Jika script tiba-tiba tidak bekerja, cek selector CSS
   - Update dependencies secara berkala

---

## 📦 Dependencies

Semua dependencies tercantum dalam `requirements.txt`:

```
playwright>=1.40.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

Install semua dependencies dengan:
```bash
pip install -r requirements.txt
```

---

## 🤝 Kontribusi

Jika Anda menemukan bug atau ingin menambahkan fitur:
1. Fork repository ini
2. Buat branch fitur baru
3. Commit perubahan Anda
4. Push ke branch
5. Buat Pull Request

---

## 📄 License

Project ini dilisensikan di bawah MIT License - lihat file LICENSE untuk detail.

---

## 📞 Support

Jika mengalami masalah:
1. Cek bagian Troubleshooting di atas
2. Pastikan semua dependencies terinstall
3. Jalankan `playwright install chromium` jika belum
4. Periksa log file `scraper_log.txt` untuk error detail

---

**Dibuat dengan ❤️ untuk memudahkan pencarian lowongan kerja di Indonesia**

*Last Updated: 2024*
