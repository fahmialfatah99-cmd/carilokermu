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

## 🐧 Panduan Lengkap untuk Linux

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

## 🚀 Instalasi

### Prasyarat

- Python 3.8 atau lebih tinggi
- Chromium browser (akan diinstall otomatis oleh Playwright)

### Langkah Instalasi di Linux

#### 1. Install Python dan pip (jika belum terinstall)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip -y
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
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

**Jika menggunakan virtual environment:**
```bash
# Pastikan venv aktif
source venv/bin/activate

# Jalankan script
python3 main.py
```

**Atau tanpa virtual environment:**
```bash
python3 main.py
```

3. Hasil akan tersimpan di file `hasil_loker.csv`

### Menjalankan dengan Mode Debug (Browser Muncul)

Untuk keperluan debugging, Anda bisa menjalankan browser secara visible (tidak headless):

```bash
# Edit main.py, ubah headless=True menjadi headless=False
python3 main.py
```

### Menjalankan dengan Argument dari Command Line (Opsional)

Jika ingin menjalankan langsung dari terminal tanpa edit file:

```bash
python3 -c "from main import scrape_loker, save_to_csv; data = scrape_loker('https://example.com', 'Python Developer', max_pages=5); save_to_csv(data, 'jobs.csv')"
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

## 📁 Struktur Output CSV

File CSV hasil scraping berisi kolom:
- **Posisi**: Judul lowongan pekerjaan
- **Perusahaan**: Nama perusahaan
- **Lokasi**: Lokasi pekerjaan
- **Link**: URL lengkap ke detail lowongan

## 🔧 Troubleshooting di Linux

### Error: "No module named 'playwright'"

```bash
# Pastikan venv aktif (jika menggunakan)
source venv/bin/activate

# Install ulang playwright
pip install playwright
playwright install chromium
```

### Error: "Chrome/Chromium binary is not available"

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

### Permission Denied saat Menjalankan Script

```bash
# Berikan permission execute
chmod +x main.py

# Atau jalankan dengan python3
python3 main.py
```

### Browser Crash atau Timeout

- Tambahkan swap memory jika RAM terbatas (minimal 2GB direkomendasikan)
- Tutup aplikasi lain yang berat
- Kurangi `max_pages` menjadi 1-2 halaman terlebih dahulu

### Tidak ada hasil yang ditemukan

1. Periksa CSS Selector sesuai dengan struktur HTML website target
2. Pastikan URL target dapat diakses
3. Website mungkin menggunakan anti-bot protection yang lebih ketat

### Timeout Error

- Tingkatkan timeout value di parameter `page.goto()`
- Periksa koneksi internet
- Website target mungkin sedang down

### Browser tidak muncul

- Script berjalan dalam mode headless (tanpa GUI)
- Untuk debug, ubah `headless=True` menjadi `headless=False`

## 📦 Dependencies

- **pandas**: Manipulasi dan export data
- **playwright**: Browser automation
- **playwright-stealth**: Stealth mode untuk menghindari deteksi
- **selectolax**: HTML parsing yang cepat

## ⚠️ Disclaimer

Gunakan script ini dengan bijak dan bertanggung jawab:
- Patuhi `robots.txt` dari website target
- Jangan melakukan request terlalu sering (rate limiting)
- Gunakan hanya untuk tujuan pembelajaran atau dengan izin
- Hormati terms of service website target

## 📝 License

MIT License - Silakan digunakan dan dimodifikasi sesuai kebutuhan.

## 🤝 Kontribusi

Kontribusi dan pull request sangat diapresiasi!

---

**Dibuat dengan ❤️ menggunakan Python & Playwright**
