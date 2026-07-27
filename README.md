# Job Scraper - Scraper Lowongan Kerja

Script Python untuk melakukan scraping lowongan kerja dari berbagai situs job portal menggunakan Playwright dengan stealth mode.

## 📋 Fitur

- **Stealth Mode**: Menggunakan playwright-stealth untuk menghindari deteksi bot
- **Multi-URL Pattern**: Mencoba beberapa pola URL otomatis untuk kompatibilitas lebih baik
- **Pagination Support**: Mendukung scraping multiple halaman
- **Dynamic Content**: Menangani konten yang dimuat secara dinamis dengan JavaScript
- **Logging**: Sistem logging terintegrasi untuk monitoring proses
- **Export CSV**: Hasil scraping dapat disimpan ke file CSV
- **Flexible Selectors**: Multiple CSS selectors untuk kompatibilitas dengan berbagai website

## 🚀 Instalasi

### Prasyarat

- Python 3.8 atau lebih tinggi
- Chromium browser (akan diinstall otomatis oleh Playwright)

---

## 🐧 Panduan Instalasi untuk Linux

### Quick Start (Ubuntu/Debian)

```bash
# 1. Install dependencies sistem
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# 2. Clone atau download project ini
cd /path/ke/folder/proyek

# 3. Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies Python
pip install -r requirements.txt

# 5. Install browser dan dependencies sistem
playwright install chromium
playwright install-deps chromium

# 6. Edit main.py sesuai kebutuhan
nano main.py

# 7. Jalankan scraper
python3 main.py
```

### Langkah Detail per Distro Linux

#### 1. Install Python dan pip (jika belum terinstall)

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

#### 2. Buat virtual environment (direkomendasikan)

```bash
cd /path/ke/folder/proyek
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install pandas playwright playwright-stealth selectolax
```

#### 4. Install browser Playwright dan dependencies sistem

```bash
# Install browser Chromium
playwright install chromium

# Install dependencies sistem yang diperlukan (hanya sekali)
playwright install-deps chromium
```

> **Catatan:** Perintah `playwright install-deps` akan menginstall package sistem seperti `libnss3`, `libatk-bridge2.0-0`, dll yang diperlukan untuk menjalankan browser.

---

## 🪟 Panduan Instalasi untuk Windows

### Quick Start (Windows 10/11)

```powershell
# 1. Install Python dari https://python.org (centang "Add Python to PATH")

# 2. Buka PowerShell atau Command Prompt sebagai Administrator
cd C:\path\ke\folder\proyek

# 3. Buat virtual environment
python -m venv venv

# 4. Aktifkan virtual environment
.\venv\Scripts\Activate.ps1

# 5. Install dependencies Python
pip install -r requirements.txt

# 6. Install browser Chromium
playwright install chromium

# 7. Edit main.py sesuai kebutuhan (gunakan Notepad++ atau VS Code)

# 8. Jalankan scraper
python main.py
```

### Langkah Detail Windows

#### 1. Install Python

1. Download installer Python dari [python.org](https://www.python.org/downloads/)
2. Jalankan installer
3. **PENTING**: Centang opsi **"Add Python to PATH"** sebelum install
4. Klik "Install Now"

Verifikasi instalasi:
```cmd
python --version
pip --version
```

#### 2. Setup Project

Buka **Command Prompt** atau **PowerShell**:

```cmd
# Navigasi ke folder proyek
cd C:\path\ke\folder\proyek

# Buat virtual environment
python -m venv venv
```

#### 3. Aktifkan Virtual Environment

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Command Prompt (CMD):**
```cmd
venv\Scripts\activate.bat
```

> Jika muncul error execution policy di PowerShell, jalankan:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### 4. Install Dependencies

```cmd
pip install -r requirements.txt
```

Atau install manual:
```cmd
pip install pandas playwright playwright-stealth selectolax
```

#### 5. Install Browser Playwright

```cmd
playwright install chromium
```

> **Catatan:** Di Windows, Playwright akan otomatis mendownload dan menginstall Chromium beserta dependencies yang diperlukan. Tidak perlu perintah `install-deps` terpisah.

#### 6. Jalankan Scraper

```cmd
python main.py
```

---

## 🍎 Panduan Instalasi untuk macOS

### Quick Start (macOS)

```bash
# 1. Install Homebrew (jika belum terinstall)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python
brew install python

# 3. Clone atau download project ini
cd /path/to/project

# 4. Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies Python
pip install -r requirements.txt

# 6. Install browser Chromium
playwright install chromium

# 7. Edit main.py sesuai kebutuhan
nano main.py

# 8. Jalankan scraper
python3 main.py
```

### Langkah Detail macOS

#### 1. Install Python

**Menggunakan Homebrew (Direkomendasikan):**
```bash
# Install Homebrew jika belum ada
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

**Alternatif tanpa Homebrew:**
Download installer dari [python.org](https://www.python.org/downloads/macos/)

Verifikasi instalasi:
```bash
python3 --version
pip3 --version
```

#### 2. Buat Virtual Environment

```bash
cd /path/to/project
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install pandas playwright playwright-stealth selectolax
```

#### 4. Install Browser Playwright

```bash
# Install browser Chromium
playwright install chromium

# Install system dependencies (jika diperlukan)
playwright install-deps chromium
```

> **Catatan:** Untuk macOS versi terbaru (Monterey/Ventura/Sonoma), mungkin perlu menginstall Xcode Command Line Tools terlebih dahulu:
> ```bash
> xcode-select --install
> ```

#### 5. Jalankan Scraper

```bash
python3 main.py
```

---

## 📖 Cara Penggunaan

### Penggunaan Dasar

1. Edit file `main.py` dan sesuaikan konfigurasi:

```python
TARGET_SITE = "https://contoh-situs-loker.com"  # Ganti dengan URL target
KEYWORD = "Data Analyst"                        # Kata kunci pencarian
MAX_PAGES = 3                                   # Jumlah halaman maksimal
OUTPUT_FILE = "hasil_loker.csv"                 # Nama file output
```

2. Jalankan script:

**Linux/macOS:**
```bash
# Pastikan venv aktif
source venv/bin/activate

# Jalankan script
python3 main.py
```

**Windows:**
```cmd
# Aktifkan venv (PowerShell)
.\venv\Scripts\Activate.ps1

# Atau (CMD)
venv\Scripts\activate.bat

# Jalankan script
python main.py
```

3. Hasil akan tersimpan di file `hasil_loker.csv`

### Menjalankan dengan Mode Debug (Browser Muncul)

Untuk keperluan debugging, Anda bisa menjalankan browser secara visible (tidak headless):

```bash
# Edit main.py, ubah headless=True menjadi headless=False
python3 main.py    # Linux/macOS
python main.py     # Windows
```

### Menjalankan dengan Argument dari Command Line (Opsional)

Jika ingin menjalankan langsung dari terminal tanpa edit file:

**Linux/macOS:**
```bash
python3 -c "from main import scrape_loker, save_to_csv; data = scrape_loker('https://example.com', 'Python Developer', max_pages=5); save_to_csv(data, 'jobs.csv')"
```

**Windows:**
```cmd
python -c "from main import scrape_loker, save_to_csv; data = scrape_loker('https://example.com', 'Python Developer', max_pages=5); save_to_csv(data, 'jobs.csv')"
```

### Penggunaan sebagai Module

Anda juga bisa menggunakan fungsi-fungsi scraper sebagai module:

```python
from main import scrape_loker, save_to_csv

# Scraping data
data = scrape_loker("https://example.com", "Python Developer", max_pages=5)

# Simpan ke CSV
save_to_csv(data, "python_jobs.csv")
```

---

## ⚙️ Kustomisasi CSS Selector

Untuk menyesuaikan dengan website target, edit bagian `selectors` di fungsi `scrape_loker`:

```python
selectors = {
    'card': ['.job-card', '.job-item', '[data-testid="job-card"]'],
    'title': ['h2', 'h3', '.job-title', 'a.title'],
    'company': ['.company-name', '.company', 'span.company'],
    'link': ['a[href*="/job/"]', 'a.job-link'],
    'location': ['.location', '.job-location']
}
```

**Tips:** Gunakan browser DevTools (F12) untuk inspect elemen HTML website target dan temukan selector yang tepat.

---

## 📁 Struktur Output CSV

File CSV hasil scraping berisi kolom:
- **Posisi**: Judul lowongan pekerjaan
- **Perusahaan**: Nama perusahaan
- **Lokasi**: Lokasi pekerjaan
- **Link**: URL lengkap ke detail lowongan

---

## 🔧 Troubleshooting

### 🐧 Linux

#### Error: "No module named 'playwright'"

```bash
# Pastikan venv aktif (jika menggunakan)
source venv/bin/activate

# Install ulang playwright
pip install playwright
playwright install chromium
```

#### Error: "Chrome/Chromium binary is not available"

Install dependencies sistem yang diperlukan:

**Ubuntu/Debian:**
```bash
sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2
```

**Fedora:**
```bash
sudo dnf install -y alsa-lib.x86_64 atk.x86_64 cups-libs.x86_64 gtk3.x86_64 libXcomposite.x86_64 libXdamage.x86_64 libXext.x86_64 libXfixes.x86_64 libXtst.x86_64 pango.x86_64 xorg-x11-fonts-misc xorg-x11-fonts-Type1 xorg-x11-utils
```

Atau gunakan perintah otomatis:
```bash
playwright install-deps chromium
```

#### Permission Denied saat Menjalankan Script

```bash
# Berikan permission execute
chmod +x main.py

# Atau jalankan dengan python3
python3 main.py
```

#### Browser Crash atau Timeout

- Tambahkan swap memory jika RAM terbatas (minimal 2GB direkomendasikan)
- Tutup aplikasi lain yang berat
- Kurangi `max_pages` menjadi 1-2 halaman terlebih dahulu

---

### 🪟 Windows

#### Error: "python" tidak dikenali sebagai perintah

- Pastikan Python sudah terinstall
- Pastikan opsi "Add Python to PATH" dicentang saat install
- Restart Command Prompt/PowerShell setelah install Python
- Atau tambahkan Python ke PATH manual:
  ```cmd
  setx PATH "%PATH%;C:\Users\YourUsername\AppData\Local\Programs\Python\Python3xx"
  ```

#### Error: Execution Policy di PowerShell

Jika muncul error saat aktivasi venv di PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Error: "No module named 'playwright'"

```cmd
# Pastikan venv aktif
.\venv\Scripts\Activate.ps1

# Install ulang playwright
pip install playwright
playwright install chromium
```

#### Antivirus/Firewall Memblokir

- Beberapa antivirus mungkin memblokir download Chromium
- Tambahkan exception untuk folder proyek atau nonaktifkan sementara
- Download Chromium manual dari Playwright GitHub releases

#### Browser Crash atau Out of Memory

- Tutup aplikasi lain yang berat
- Kurangi `max_pages` menjadi 1-2 halaman
- Tingkatkan virtual memory (pagefile) Windows

---

### 🍎 macOS

#### Error: "command not found: python3"

Install Python dengan Homebrew:
```bash
brew install python
```

#### Error: Certificate Verification Failed

```bash
# Install certificates untuk Python
/Applications/Python\ 3.x/Install\ Certificates.command
```

Atau:
```bash
pip install --upgrade certifi
```

#### Error: Permission Denied

```bash
# Berikan permission
chmod +x main.py

# Atau jalankan dengan sudo (tidak direkomendasikan)
sudo python3 main.py
```

#### Gatekeeper Memblokir Aplikasi

Jika macOS memblokir eksekusi:
1. Buka **System Preferences** → **Security & Privacy**
2. Klik **Allow Anyway** jika muncul pesan blokir
3. Atau nonaktifkan Gatekeeper sementara:
   ```bash
   sudo spctl --master-disable
   ```

#### Apple Silicon (M1/M2/M3) Issues

Untuk Mac dengan chip Apple Silicon:
```bash
# Install Rosetta 2 jika belum
softwareupdate --install-rosetta

# Install dependencies dengan arsitektur yang benar
arch -arm64 pip install -r requirements.txt
```

---

### Umum (Semua Platform)

#### Tidak ada hasil yang ditemukan

1. Periksa CSS Selector sesuai dengan struktur HTML website target
2. Pastikan URL target dapat diakses
3. Website mungkin menggunakan anti-bot protection yang lebih ketat

#### Timeout Error

- Tingkatkan timeout value di parameter `page.goto()`
- Periksa koneksi internet
- Website target mungkin sedang down

#### Browser tidak muncul

- Script berjalan dalam mode headless (tanpa GUI)
- Untuk debug, ubah `headless=True` menjadi `headless=False`

---

## 📦 Dependencies

- **pandas**: Manipulasi dan export data
- **playwright**: Browser automation
- **playwright-stealth**: Stealth mode untuk menghindari deteksi
- **selectolax**: HTML parsing yang cepat

---

## ⚠️ Disclaimer

Gunakan script ini dengan bijak dan bertanggung jawab:
- Patuhi `robots.txt` dari website target
- Jangan melakukan request terlalu sering (rate limiting)
- Gunakan hanya untuk tujuan pembelajaran atau dengan izin
- Hormati terms of service website target

---

## 📝 License

MIT License - Silakan digunakan dan dimodifikasi sesuai kebutuhan.

---

## 🤝 Kontribusi

Kontribusi dan pull request sangat diapresiasi!

---

**Dibuat dengan ❤️ menggunakan Python & Playwright**
