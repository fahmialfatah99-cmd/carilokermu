# Job Scraper - Pencari Lowongan Kerja Otomatis 🚀

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev/)

Script Python untuk melakukan scraping lowongan kerja dari berbagai situs job portal secara otomatis. Dilengkapi dengan **2 mode penggunaan**: Mode Manual (untuk developer) dan Mode Otomatis (untuk pengguna umum).

---

## ✨ Fitur Utama

### 🎯 Mode Otomatis (Easy Search)
- **Tanpa Edit Kode**: Cukup jalankan dan jawab pertanyaan
- **Interaktif**: Input posisi, lokasi, dan preferensi langsung dari terminal
- **Auto-Save**: Hasil otomatis tersimpan dalam format CSV
- **User-Friendly**: Cocok untuk non-programmer

### 🔧 Mode Manual (Advanced)
- **Stealth Mode**: Menggunakan playwright-stealth untuk menghindari deteksi bot
- **Multi-URL Pattern**: Mencoba beberapa pola URL otomatis
- **Pagination Support**: Scraping multiple halaman sekaligus
- **Dynamic Content**: Menangani konten JavaScript dinamis
- **Flexible Selectors**: Kompatibel dengan berbagai website job portal
- **Logging System**: Monitoring proses real-time
- **Export CSV**: Data terstruktur siap analisis

---

## 📋 Daftar Isi

- [Instalasi](#-instalasi)
  - [Linux](#linux-)
  - [Windows](#windows-)
  - [macOS](#macos-)
- [Cara Penggunaan](#-cara-penggunaan)
  - [Mode Otomatis (Recommended)](#mode-otomatis-recommended)
  - [Mode Manual](#mode-manual)
- [Troubleshooting](#-troubleshooting)
- [Struktur Output](#-struktur-output)
- [Kontribusi](#-kontribusi)
- [License](#-license)

---

## 🚀 Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Koneksi internet (untuk download browser Chromium)

---

### Linux 🐧

#### Quick Start (Ubuntu/Debian)

```bash
# 1. Install dependencies
sudo apt update && sudo apt install python3 python3-pip python3-venv -y

# 2. Clone repository
cd /path/ke/folder/proyek

# 3. Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install browser Chromium
playwright install chromium
playwright install-deps chromium

# 6. Jalankan mode otomatis
python3 easy_search.py
```

#### Detail per Distro

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install python3 python3-pip -y
```

**Arch Linux/Manjaro:**
```bash
sudo pacman -S python python-pip python-virtualenv
```

**openSUSE:**
```bash
sudo zypper install python3 python3-pip python3-virtualenv
```

**Setup lanjutan:**
```bash
# Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install browser
playwright install chromium
playwright install-deps chromium
```

---

### Windows 🪟

#### Quick Start (Windows 10/11)

```powershell
# 1. Install Python dari https://python.org
#    CENTANG: "Add Python to PATH" saat instalasi

# 2. Buka PowerShell sebagai Administrator
cd C:\path\ke\folder\proyek

# 3. Buat virtual environment
python -m venv venv

# 4. Aktifkan virtual environment
.\venv\Scripts\Activate.ps1

# 5. Install dependencies
pip install -r requirements.txt

# 6. Install browser Chromium
playwright install chromium

# 7. Jalankan mode otomatis
python easy_search.py
```

#### Langkah Detail

**1. Install Python:**
1. Download dari [python.org](https://www.python.org/downloads/)
2. Jalankan installer
3. **PENTING**: Centang ✅ "Add Python to PATH"
4. Klik "Install Now"

**2. Verifikasi instalasi:**
```cmd
python --version
pip --version
```

**3. Setup project:**
```cmd
# Navigasi ke folder
cd C:\path\ke\folder\proyek

# Buat virtual environment
python -m venv venv
```

**4. Aktifkan virtual environment:**

PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

CMD:
```cmd
venv\Scripts\activate.bat
```

> ⚠️ Jika error di PowerShell, jalankan:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**5. Install dependencies:**
```cmd
pip install -r requirements.txt
playwright install chromium
```

**6. Jalankan:**
```cmd
python easy_search.py
```

---

### macOS 🍎

#### Quick Start

```bash
# 1. Install Homebrew (jika belum)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python
brew install python

# 3. Clone repository
cd /path/to/project

# 4. Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Install browser Chromium
playwright install chromium

# 7. Jalankan mode otomatis
python3 easy_search.py
```

#### Apple Silicon (M1/M2/M3)

Untuk Mac dengan chip Apple Silicon:
```bash
# Install Rosetta 2 (jika belum)
softwareupdate --install-rosetta

# Install dengan arsitektur ARM64
arch -arm64 pip install -r requirements.txt
```

#### Troubleshooting macOS

**Certificate Error:**
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

**Gatekeeper Blocking:**
1. System Preferences → Security & Privacy
2. Klik "Allow Anyway" jika muncul pesan blokir

---

## 📖 Cara Penggunaan

### Mode Otomatis (Recommended) ⭐

Cocok untuk semua pengguna, **tanpa perlu edit kode**!

#### Langkah-langkah:

1. **Jalankan script:**
   ```bash
   # Linux/macOS
   python3 easy_search.py
   
   # Windows
   python easy_search.py
   ```

2. **Jawab pertanyaan yang muncul:**
   ```
   🔍 PENCARI LOWONGAN KERJA MUDAH
   ==================================================
   
   1. Mau cari posisi apa? (contoh: Administrasi, Staff, Driver): Administrasi
   
   2. Di kota/daerah mana? (contoh: Jakarta, Surabaya, Bandung): Jakarta Selatan
   
   3. Mau ambil berapa halaman hasil? (default 3, max 10): 5
   
   4. Tampilkan browser saat mencari? (y/n, default n): n
   
   ==================================================
   📋 Ringkasan Pencarian:
      • Posisi: Administrasi
      • Lokasi: Jakarta Selatan
      • Halaman: 5
      • Mode: Silent
   ==================================================
   
   Lanjutkan pencarian? (y/n): y
   ```

3. **Tunggu proses scraping selesai**

4. **Hasil otomatis tersimpan** dalam file CSV dengan nama:
   ```
   loker_administrasi_20240115_143022.csv
   ```

5. **Buka file CSV** dengan Excel, Google Sheets, atau aplikasi spreadsheet lainnya

#### Contoh Kasus Nyata:

**Mencari lowongan Administrasi di Jakarta Selatan:**

```bash
$ python3 easy_search.py

🔍 PENCARI LOWONGAN KERJA MUDAH
==================================================

1. Mau cari posisi apa? (contoh: Administrasi, Staff, Driver): Administrasi

2. Di kota/daerah mana? (contoh: Jakarta, Surabaya, Bandung): Jakarta Selatan

3. Mau ambil berapa halaman hasil? (default 3, max 10): [tekan Enter untuk default]

4. Tampilkan browser saat mencari? (y/n, default n): [tekan Enter untuk default]

==================================================
📋 Ringkasan Pencarian:
   • Posisi: Administrasi
   • Lokasi: Jakarta Selatan
   • Halaman: 3
   • Mode: Silent
==================================================

Lanjutkan pencarian? (y/n): y

🚀 Memulai pencarian: 'Administrasi' di https://id.jobstreet.com/id/jobs/in-jakarta-selatan
📄 Maksimum 3 halaman
📑 Scraping halaman 1/3
   Found 15 jobs dengan selector: article
   ✅ Ditemukan 15 total lowongan sampai sekarang
...
✅ Berhasil menyimpan 45 lowongan ke file: loker_administrasi_20240115_143022.csv

==================================================
🎉 SELESAI!
   Total lowongan ditemukan: 45
   File hasil: loker_administrasi_20240115_143022.csv
   Buka file tersebut dengan Excel atau Google Sheets
==================================================
```

---

### Mode Manual 🔧

Untuk developer yang ingin kustomisasi lebih lanjut.

#### 1. Edit Konfigurasi

Buka file `main.py` dengan text editor favorit:

**Linux:**
```bash
nano main.py          # Terminal
gedit main.py &       # GUI GNOME
code main.py          # VS Code
```

**Windows:**
```cmd
notepad main.py       # Notepad
code main.py          # VS Code
notepad++.exe main.py # Notepad++
```

**macOS:**
```bash
nano main.py                    # Terminal
open -a TextEdit main.py        # TextEdit
code main.py                    # VS Code
```

#### 2. Sesuaikan Parameter

Ubah bagian ini di `main.py`:

```python
TARGET_SITE = "https://id.jobstreet.com/id/jobs"
KEYWORD = "Data Analyst"
MAX_PAGES = 5
OUTPUT_FILE = "loker_data_analyst.csv"
```

#### 3. Jalankan Script

```bash
# Linux/macOS
python3 main.py

# Windows
python main.py
```

#### 4. Gunakan sebagai Module

Anda juga bisa import fungsi scraper ke script lain:

```python
from main import scrape_loker, save_to_csv

# Scraping data
data = scrape_loker(
    url_target="https://id.jobstreet.com/id/jobs",
    keyword="Python Developer",
    max_pages=5
)

# Simpan ke CSV
save_to_csv(data, "python_jobs.csv")
```

---

## 🔧 Troubleshooting

### Linux 🐧

**Error: "No module named 'playwright'"**
```bash
source venv/bin/activate
pip install playwright
playwright install chromium
```

**Error: Chrome binary not available**
```bash
# Install dependencies sistem
playwright install-deps chromium

# Atau manual (Ubuntu/Debian)
sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2
```

**Permission Denied**
```bash
chmod +x easy_search.py main.py
```

---

### Windows 🪟

**Error: "python" tidak dikenali**
- Pastikan Python sudah terinstall
- Restart Command Prompt/PowerShell
- Tambahkan Python ke PATH manual jika perlu

**PowerShell Execution Policy Error**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Antivirus Memblokir**
- Tambahkan exception untuk folder proyek
- Nonaktifkan sementara saat install Chromium

---

### macOS 🍎

**Error: "python3" command not found**
```bash
brew install python
```

**Certificate Verification Failed**
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

**Apple Silicon Issues**
```bash
softwareupdate --install-rosetta
arch -arm64 pip install -r requirements.txt
```

---

### Umum (Semua Platform)

**Tidak ada hasil yang ditemukan**
1. Periksa koneksi internet
2. Coba kata kunci berbeda
3. Website target mungkin mengubah struktur HTML

**Timeout Error**
- Periksa koneksi internet
- Kurangi `max_pages` menjadi 1-2
- Website target mungkin sedang down

**Browser tidak muncul**
- Script berjalan dalam mode headless (normal)
- Untuk debug, pilih 'y' pada pertanyaan "Tampilkan browser?"

---

## 📁 Struktur Output

File CSV berisi kolom-kolom berikut:

| Kolom | Deskripsi |
|-------|-----------|
| `no` | Nomor urut lowongan |
| `judul` | Judul posisi pekerjaan |
| `perusahaan` | Nama perusahaan |
| `lokasi` | Lokasi pekerjaan |
| `gaji` | Informasi gaji (jika ada) |
| `link` | URL lengkap ke detail lowongan |
| `tanggal_scrape` | Waktu scraping dilakukan |

**Contoh isi CSV:**
```csv
no,judul,perusahaan,lokasi,gaji,link,tanggal_scrape
1,Staff Administrasi,PT Maju Jaya,Jakarta Selatan,Rp 5-7 juta,https://...,2024-01-15 14:30:22
2,Admin Officer,CV Berkah,Bandung,-,https://...,2024-01-15 14:30:22
```

---

## ⚙️ Kustomisasi CSS Selector (Mode Manual)

Untuk menyesuaikan dengan website target, edit bagian `selectors` di `main.py`:

```python
selectors = {
    'card': ['.job-card', '.job-item', '[data-testid="job-card"]'],
    'title': ['h2', 'h3', '.job-title', 'a.title'],
    'company': ['.company-name', '.company', 'span.company'],
    'link': ['a[href*="/job/"]', 'a.job-link'],
    'location': ['.location', '.job-location']
}
```

**Tips:** Gunakan browser DevTools (F12) untuk inspect elemen HTML website target.

---

## 🤝 Kontribusi

Kontribusi sangat diapresiasi! Silakan:

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

Distributed under the MIT License. Lihat `LICENSE` untuk informasi lebih lanjut.

---

## ⚠️ Disclaimer

Gunakan script ini dengan bijak dan bertanggung jawab:

- ✅ Patuhi `robots.txt` dari website target
- ✅ Jangan melakukan request terlalu sering (rate limiting)
- ✅ Gunakan hanya untuk tujuan pembelajaran atau dengan izin
- ✅ Hormati terms of service website target
- ❌ Jangan gunakan untuk spamming atau aktivitas ilegal

---

## 📦 Dependencies

- [pandas](https://pandas.pydata.org/) - Manipulasi dan export data
- [playwright](https://playwright.dev/) - Browser automation
- [playwright-stealth](https://github.com/AtuboDad/playwright-stealth) - Stealth mode
- [selectolax](https://github.com/rushter/selectolax) - HTML parsing cepat

---

## 📞 Support

Jika mengalami masalah:

1. Cek bagian [Troubleshooting](#-troubleshooting) di atas
2. Baca dokumentasi Playwright: https://playwright.dev/
3. Buka issue di repository ini

---

**Dibuat dengan ❤️ menggunakan Python & Playwright**

---

## 🎯 Quick Reference

### Perintah Cepat

| Tujuan | Linux/macOS | Windows |
|--------|-------------|---------|
| Install dependencies | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Install browser | `playwright install chromium` | `playwright install chromium` |
| Jalankan mode otomatis | `python3 easy_search.py` | `python easy_search.py` |
| Jalankan mode manual | `python3 main.py` | `python main.py` |
| Aktifkan venv | `source venv/bin/activate` | `.\venv\Scripts\Activate.ps1` |

### Struktur Folder

```
job-scraper/
├── README.md           # Dokumentasi ini
├── requirements.txt    # Dependencies Python
├── easy_search.py     # Mode otomatis (recommended)
├── main.py            # Mode manual (advanced)
├── .gitignore         # Git ignore rules
└── *.csv              # Output files (auto-generated)
```

---

Happy Job Hunting! 🎉
