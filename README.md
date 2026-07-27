# 🚀 Job Scraper Otomatis & Manual - Selenium + Playwright + BeautifulSoup

Tool scraping lowongan kerja yang fleksibel, mendukung **Linux**, **Windows**, dan **macOS**. Tersedia dalam berbagai mode: **Selenium Max**, **BeautifulSoup (Ringan)**, **Otomatis (Interaktif)**, dan **Manual (Config Code)**.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Selenium](https://img.shields.io/badge/selenium-latest-success)
![Playwright](https://img.shields.io/badge/playwright-latest-success)
![BeautifulSoup](https://img.shields.io/badge/beautifulsoup-latest-success)

## ✨ Fitur Utama

- ✅ **SCRAPING MAKSIMAL TANPA BATASAN**: Menggunakan Selenium + Chromium dengan konfigurasi optimal.
- ✅ **DATA GAJI & PERUSAHAAN WAJIB ADA**: Validasi otomatis memastikan data penting selalu tersedia.
- ✅ **Tanpa Batas Halaman**: Default scraping berjalan terus hingga data habis (bisa dibatasi manual).
- ✅ **Multi-Platform**: Panduan instalasi lengkap untuk Linux, Windows, dan Mac.
- ✅ **Empat Mode Penggunaan**:
  - **Selenium Max Mode**: Scraping maksimal dengan anti-deteksi tingkat tinggi.
  - **BeautifulSoup Mode**: Ringan, cepat, TIDAK PERLU CHROME/SELENIUM! ⭐ RECOMMENDED
  - **Easy Mode**: Tinggal jalankan, jawab pertanyaan, selesai.
  - **Pro Mode**: Edit konfigurasi langsung di kode untuk kontrol penuh.
- ✅ **Anti-Deteksi Canggih**: User agent random, stealth mode, scroll otomatis, retry otomatis.
- ✅ **Export CSV Lengkap**: Hasil tersimpan rapi dengan semua kolom penting.
- ✅ **Logging Real-time**: Memantau proses scraping dengan detail.

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

# Install browser untuk Playwright
playwright install chromium
playwright install-deps chromium

# Install Chrome/Chromium untuk Selenium
sudo apt install chromium-browser -y
# Atau download Chrome dari https://www.google.com/chrome/
```

### 2. Instalasi di Windows

```bash
# Install Python dari python.org (pastikan centang "Add to PATH")

# Buka Command Prompt atau PowerShell
pip install -r requirements.txt

# Install browser Playwright
playwright install chromium

# Install Chrome untuk Selenium
# Download dan install Chrome dari https://www.google.com/chrome/
# ChromeDriver akan diinstall otomatis oleh webdriver-manager
```

### 3. Instalasi di macOS

```bash
# Install Python via Homebrew
brew install python

# Install dependencies
pip install -r requirements.txt

# Install browser Playwright
playwright install chromium

# Install Chrome untuk Selenium
brew install --cask google-chrome
```

---

## 📁 Struktur File

| File | Deskripsi | Mode | Tingkat Kesulitan |
|------|-----------|------|-------------------|
| `beautifulsoup_scraper.py` | **SCRAPER RINGAN** dengan Requests + BeautifulSoup | Otomatis | ⭐ Mudah |
| `selenium_max_scraper.py` | **SCRAPER MAKSIMAL** dengan Selenium + Chromium | Otomatis | ⭐⭐ Menengah |
| `easy_search.py` | Scraper interaktif dengan input user (Playwright) | Otomatis | ⭐ Mudah |
| `main.py` | Scraper dengan konfigurasi di kode (Playwright) | Manual | ⭐⭐ Menengah |
| `jalan_otomatis.py` | Scraper interaktif dengan menu lengkap (Playwright) | Otomatis | ⭐⭐ Menengah |

---

## 🚀 Cara Penggunaan

### Mode 1: BeautifulSoup Scraper (PALING RINGAN) ⭐ RECOMMENDED UNTUK PEMULA

Cocok untuk pengguna yang ingin scraping cepat, ringan, TANPA PERLU INSTALL CHROME/SELENIUM!

```bash
python beautifulsoup_scraper.py
```

**Langkah-langkah:**
1. Jalankan script
2. Masukkan posisi/jabatan yang dicari (contoh: Administrasi)
3. Masukkan kota/lokasi (contoh: Jakarta Selatan)
4. Tentukan batas halaman (tekan Enter untuk unlimited)
5. Scraping berjalan otomatis dengan retry logic dan user agent random
6. Hasil tersimpan dengan kolom lengkap termasuk **Gaji** dan **Perusahaan**

**Keunggulan:**
- ✅ TIDAK PERLU CHROME/CHROMIUM - Hanya butuh Python + requests
- ✅ Sangat ringan dan cepat
- ✅ User agent random untuk menghindari blocking
- ✅ Retry otomatis jika gagal fetch
- ✅ Multi-selector fallback untuk elemen yang sulit diambil
- ✅ Validasi wajib: Gaji dan Perusahaan harus ada

**Kekurangan:**
- ⚠️ Tidak bisa handle JavaScript-heavy content (tapi JobStreet tetap bisa discrape)
- ⚠️ Mungkin perlu update headers jika website berubah

**Contoh Output:**
```
loker_bs4_Admin_Jakarta_20240101_120000.csv
```

---

### Mode 2: Selenium Max Scraper (HASIL MAKSIMAL) ⭐ RECOMMENDED UNTUK ADVANCED

Cocok untuk pengguna yang menginginkan hasil scraping maksimal tanpa batasan dengan anti-deteksi tingkat tinggi.

```bash
python selenium_max_scraper.py
```

**Langkah-langkah:**
1. Jalankan script
2. Masukkan posisi/jabatan yang dicari (contoh: Administrasi)
3. Masukkan kota/lokasi (contoh: Jakarta Selatan)
4. Tentukan batas halaman (tekan Enter untuk unlimited)
5. Pilih mode headless (y/n, default n = browser terlihat)
6. Scraping berjalan otomatis dengan scroll, retry, dan validasi data
7. Hasil tersimpan dengan kolom lengkap termasuk **Gaji** dan **Perusahaan**

**Fitur Unggulan:**
- ✅ User agent random untuk menghindari deteksi bot
- ✅ Scroll otomatis untuk trigger lazy loading
- ✅ Retry otomatis jika gagal load
- ✅ Validasi wajib: Gaji dan Perusahaan harus ada
- ✅ Multi-selector fallback untuk elemen yang sulit diambil
- ✅ Stealth mode dengan CDP commands

**Persyaratan:**
- ⚠️ HARUS INSTALL CHROME/CHROMIUM terlebih dahulu
- ⚠️ Lebih berat dan lambat dibanding BeautifulSoup

**Contoh Output:**
```
loker_selenium_Admin_Jakarta_20240101_120000.csv
```

---

### Mode 3: Easy Search (Paling Mudah)

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

### Mode 4: Main.py (Konfigurasi Kode)

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

### Mode 5: Jalan Otomatis (Menu Interaktif Lengkap)

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
| No | Nomor urut data |
| Posisi | Nama jabatan/posisi pekerjaan |
| Perusahaan | Nama perusahaan (WAJIB ADA) |
| Lokasi | Lokasi pekerjaan |
| **Gaji** | Informasi gaji (WAJIB ADA) 💰 |
| Tipe Pekerjaan | Full-time, Part-time, Contract, dll |
| Pengalaman | Pengalaman yang dibutuhkan |
| Pendidikan | Tingkat pendidikan minimal |
| Tanggal Posting | Kapan lowongan diposting |
| Deskripsi Singkat | Ringkasan deskripsi pekerjaan |
| Link | URL lengkap ke lowongan |
| Waktu Scraping | Waktu pengambilan data |

*Catatan: `beautifulsoup_scraper.py`, `selenium_max_scraper.py` dan `jalan_otomatis.py` memiliki kolom paling lengkap*

---

## ⚙️ Konfigurasi Lanjutan

### Membatasi Jumlah Halaman

Untuk menghemat waktu, Anda bisa membatasi jumlah halaman yang discrape:

- **selenium_max_scraper.py**: Input angka saat diminta "Batas jumlah halaman"
- **easy_search.py**: Input angka saat diminta "Jumlah halaman"
- **main.py**: Ubah `MAX_PAGES = 5` (ganti 5 dengan angka yang diinginkan)
- **jalan_otomatis.py**: Input angka saat diminta "Batas jumlah halaman"

### Mode Debug (Melihat Browser)

Jika ingin melihat proses scraping secara visual:

- **selenium_max_scraper.py**: Jawab 'n' saat ditanya "Browser tersembunyi?" (default n = terlihat)
- **easy_search.py**: Jawab 'y' saat ditanya "Tampilkan browser?"
- **main.py**: Ubah `HEADLESS = False`
- **jalan_otomatis.py**: Jawab 'y' saat ditanya "Lihat browser berjalan?"

### Konfigurasi Advanced Selenium Max Scraper

Edit bagian `CONFIG` di `selenium_max_scraper.py`:

```python
CONFIG = {
    'max_pages': 0,  # 0 = unlimited
    'headless': False,  # False = browser terlihat
    'explicit_wait': 15,  # Timeout tunggu elemen (detik)
    'scroll_pause': 2,  # Jeda saat scroll (detik)
    'retry_attempts': 3,  # Jumlah percobaan ulang
    'ensure_salary_company': True,  # Paksa ambil gaji dan perusahaan
}
```

### Konfigurasi BeautifulSoup Scraper

Edit bagian `CONFIG` di `beautifulsoup_scraper.py`:

```python
CONFIG = {
    'max_pages': 0,  # 0 = unlimited
    'retry_attempts': 3,  # Jumlah percobaan ulang jika gagal fetch
    'timeout': 30,  # Timeout request (detik)
    'ensure_salary_company': True,  # Paksa ambil gaji dan perusahaan
}
```

### Mengubah Website Target

Script ini dirancang untuk JobStreet Indonesia. Untuk mengubah ke website lain:

1. Edit selector CSS di variabel `SELECTORS`
2. Sesuaikan struktur URL di fungsi `build_search_url()`
3. Update field yang diambil sesuai struktur website baru

---

## 🔧 Troubleshooting

### Error: "playwright not found" atau "selenium not found"
```bash
pip install -r requirements.txt
playwright install chromium
```

### Error: "No module named 'bs4'" atau "No module named 'fake_useragent'"
```bash
pip install beautifulsoup4 fake-useragent
```

### Error: "ChromeDriver not found" (Selenium)
```bash
# ChromeDriver akan diinstall otomatis oleh webdriver-manager
# Pastikan Chrome browser sudah terinstall
```

### Error: "No module named 'playwright'" atau "No module named 'selenium'"
```bash
pip install playwright selenium
playwright install chromium
```

### Scraping Berhenti di Tengah Jalan
- Website mungkin mendeteksi bot, coba gunakan mode debug (jangan headless)
- Kurangi kecepatan dengan menambah delay di konfigurasi
- Pastikan koneksi internet stabil
- Coba gunakan `selenium_max_scraper.py` yang memiliki retry otomatis

### Data yang Diambil Sedikit/Nol
- Selector CSS mungkin sudah berubah, update selector di variabel `SELECTORS`
- Website menggunakan lazy loading, script sudah punya scroll otomatis
- Coba ganti keyword atau lokasi pencarian
- Pastikan tidak terkena CAPTCHA atau block

### Browser Terbuka Tapi Tidak Ada Data
- Tunggu lebih lama, scraping butuh waktu untuk load
- Cek console untuk error detail
- Coba jalankan dengan mode terlihat (bukan headless)
- Update selector jika struktur website berubah

---

## 📝 Catatan Penting

1. **Etika Scraping**: 
   - Gunakan dengan bijak dan jangan overload server
   - Patuhi robots.txt website target
   - Gunakan untuk keperluan pribadi/edukasi
   - Hindari scraping terlalu cepat, biarkan ada delay antar request

2. **Legalitas**:
   - Data yang diambil adalah data publik
   - Jangan gunakan untuk komersialisasi tanpa izin
   - Hormati hak cipta dan ketentuan website
   - Bertanggung jawab atas penggunaan data

3. **Kinerja**:
   - Scraping tanpa batas bisa memakan waktu lama
   - Disarankan batasi halaman untuk testing awal
   - File CSV besar bisa dibuka dengan Excel, Google Sheets, atau LibreOffice Calc
   - `selenium_max_scraper.py` lebih lambat tapi hasil lebih maksimal

4. **Update Berkala**:
   - Struktur website bisa berubah sewaktu-waktu
   - Jika script tiba-tiba tidak bekerja, cek selector CSS di variabel `SELECTORS`
   - Update dependencies secara berkala dengan `pip install --upgrade -r requirements.txt`

5. **Tips Hasil Maksimal**:
   - Gunakan `selenium_max_scraper.py` untuk hasil terbaik
   - Jangan gunakan mode headless jika ingin hasil lebih stabil
   - Pastikan koneksi internet stabil
   - Jalankan di waktu traffic rendah (malam/pagi)

---

## 📦 Dependencies

Semua dependencies tercantum dalam `requirements.txt`:

```
playwright>=1.40.0
beautifulsoup4>=4.12.0
lxml>=5.1.0
selenium>=4.15.0
fake-useragent>=1.4.0
webdriver-manager>=4.0.0
requests>=2.31.0
```

Install semua dependencies dengan:
```bash
pip install -r requirements.txt
```

**Catatan:** 
- `beautifulsoup4` + `requests` untuk BeautifulSoup Scraper (RINGAN!)
- `selenium` + `webdriver-manager` untuk Selenium Max Scraper
- `playwright` untuk easy_search.py, main.py, dan jalan_otomatis.py
- `fake-useragent` untuk user agent random anti-deteksi

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

## 🎯 Rekomendasi Script

| Kebutuhan | Script yang Direkomendasikan |
|-----------|------------------------------|
| **Ringan & Cepat (TANPA CHROME)** | `beautifulsoup_scraper.py` ⭐⭐⭐ |
| **Hasil MAKSIMAL** | `selenium_max_scraper.py` ⭐⭐ |
| Cepat & Simpel | `easy_search.py` |
| Kontrol Penuh | `main.py` |
| Menu Interaktif Lengkap | `jalan_otomatis.py` |

---

**Dibuat dengan ❤️ untuk memudahkan pencarian lowongan kerja di Indonesia**

*Last Updated: 2024 - Sekarang dengan Selenium Max Scraper + BeautifulSoup Scraper*
