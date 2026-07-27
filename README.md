# CariLoker - Web Scraper Lowongan Kerja

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**CariLoker** adalah tool web scraper untuk mengumpulkan informasi lowongan kerja dari berbagai website secara otomatis. Dibangun dengan Python, Playwright, dan Selectolax untuk performa scraping yang cepat dan efisien.

## ✨ Fitur

- 🔍 **Pencarian Fleksibel**: Cari lowongan berdasarkan kata kunci
- 🌐 **Multi-Website Support**: Dapat disesuaikan untuk berbagai situs lowongan kerja
- 💾 **Multi-Format Export**: Simpan hasil ke CSV, JSON, atau Excel
- 🎭 **Stealth Mode**: Menggunakan playwright-stealth untuk menghindari deteksi bot
- 📊 **Ringkasan Otomatis**: Dapatkan statistik dari hasil scraping
- 🖥️ **CLI Interface**: Mudah digunakan dari command line
- 📝 **Logging Lengkap**: Track semua aktivitas dalam file log
- 🔧 **Custom CSS Selectors**: Sesuaikan selector dengan website target
- ⏱️ **Timeout Handling**: Penanganan timeout yang robust

## 📋 Prasyarat

- Python 3.8 atau lebih tinggi
- Chromium browser (akan diinstall otomatis oleh Playwright)

## 🚀 Instalasi

### 1. Clone atau Download Repository

```bash
cd /path/to/cari-loker
```

### 2. Install Python (jika belum ada)

#### **Windows:**
1. Download installer dari [python.org](https://www.python.org/downloads/)
2. Jalankan installer, pastikan centang "Add Python to PATH"
3. Verifikasi instalasi:
   ```cmd
   python --version
   pip --version
   ```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

#### **Linux (CentOS/RHEL/Fedora):**
```bash
sudo dnf install python3 python3-pip
python3 --version
pip3 --version
```

#### **macOS:**
Menggunakan Homebrew (recommended):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.12
python3 --version
pip3 --version
```

Atau menggunakan pyenv:
```bash
brew install pyenv
pyenv install 3.12.0
pyenv global 3.12.0
```

### 3. Buat Virtual Environment (Recommended)

#### **Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### **Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:

```bash
pip install pandas playwright playwright-stealth selectolax openpyxl
```

### 5. Install Browser Playwright

```bash
playwright install chromium
```

**Catatan untuk Linux:** Jika muncul error dependency, install terlebih dahulu:
```bash
# Ubuntu/Debian
sudo apt-get install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2

# CentOS/RHEL
sudo yum install alsa-lib.x86_64 atk.x86_64 cups-libs.x86_64 gtk3.x86_64 libXcomposite.x86_64 libXdamage.x86_64 libXext.x86_64 libXfixes.x86_64 libXrandr.x86_64 libXtst.x86_64 pango.x86_64 xorg-x11-fonts-misc xorg-x11-fonts-Type1 xorg-x11-utils

# Fedora
sudo dnf install alsa-lib atk cups-libs gtk3 libXcomposite libXdamage libXext libXfixes libXrandr libXtst pango xorg-x11-fonts-misc xorg-x11-fonts-Type1
```

**Catatan untuk macOS:** Pastikan Xcode Command Line Tools terinstall:
```bash
xcode-select --install
```

---

## 📖 Cara Penggunaan

### 🎯 CARA MUDAH: Menggunakan jalan_otomatis.py (RECOMMENDED!)

**Tidak perlu edit file apapun!** Cukup jalankan script dan jawab pertanyaan yang muncul.

#### Langkah-langkah:

1. **Jalankan script:**

   **Windows:**
   ```cmd
   python jalan_otomatis.py
   ```

   **Linux/macOS:**
   ```bash
   python3 jalan_otomatis.py
   ```

2. **Jawab pertanyaan yang muncul di layar:**

   ```
   🔍  JOB SCRAPER OTOMATIS - Pencari Lowongan Kerja
   ======================================================================
   
   Jawab pertanyaan berikut untuk memulai scraping:
   
   Posisi apa yang ingin dicari? []: Administrasi
   Lokasi pencarian (contoh: Jakarta-Selatan-Jakarta-Raya)? []: Jakarta-Selatan-Jakarta-Raya
   Berapa halaman yang ingin discrape? [1]: 3
   Ingin melihat browser berjalan? (y/n) [n]: n
   Nama file output (kosongkan untuk auto-generate) [loker_administrasi_jakarta-selatan-jakarta-raya_20240115_103000.csv]: 
   
   ----------------------------------------------------------------------
   Konfirmasi pengaturan:
     • Posisi: Administrasi
     • Lokasi: Jakarta-Selatan-Jakarta-Raya
     • Halaman: 3
     • Browser: Tersembunyi
     • File output: loker_administrasi_jakarta-selatan-jakarta-raya_20240115_103000.csv
   ----------------------------------------------------------------------
   
   Lanjutkan scraping? (y/n) [y]: y
   ```

3. **Tunggu proses scraping selesai**

4. **Hasil akan otomatis tersimpan dalam file CSV!**

#### Contoh Lengkap: Cari Lowongan Administrasi di Jakarta Selatan

Misalnya Anda ingin mencari lowongan **Administrasi** di **Jakarta Selatan** dari Jobstreet dengan URL:
`https://id.jobstreet.com/id/jobs/in-Jakarta-Selatan-Jakarta-Raya`

**Langkah 1:** Jalankan script
```bash
python3 jalan_otomatis.py
```

**Langkah 2:** Isi pertanyaan:
- Posisi: `Administrasi`
- Lokasi: `Jakarta-Selatan-Jakarta-Raya`
- Halaman: `3` (atau sesuai keinginan)
- Lihat browser: `n` (tidak perlu lihat browser)
- Nama file: tekan Enter (auto-generate)
- Konfirmasi: `y`

**Langkah 3:** Hasil akan tersimpan di file seperti:
```
loker_administrasi_jakarta-selatan-jakarta-raya_20240115_103000.csv
```

**Keuntungan menggunakan jalan_otomatis.py:**
✅ Tidak perlu edit file apapun
✅ Interface interaktif dengan pertanyaan mudah
✅ Auto-generate nama file
✅ Konfirmasi sebelum scraping
✅ Ringkasan hasil otomatis
✅ Error handling yang baik

---

### 🛠️ CARA LANJUTAN: Menggunakan cariloker.py (CLI Mode)

Untuk pengguna advanced yang ingin lebih banyak kontrol melalui command line arguments.

#### Contoh: Cari Lowongan Administrasi di Jakarta Selatan

#### **Windows (Command Prompt):**
```cmd
python cariloker.py -k "Administrasi" -u "https://id.jobstreet.com/id/jobs/in-Jakarta-Selatan-Jakarta-Raya" -f csv
```

#### **Linux/macOS:**
```bash
python3 cariloker.py -k "Administrasi" -u "https://id.jobstreet.com/id/jobs/in-Jakarta-Selatan-Jakarta-Raya" -f csv
```

**Penjelasan:**
- `-k "Administrasi"` : Kata kunci pencarian untuk posisi administrasi
- `-u "https://id.jobstreet.com/id/jobs/in-Jakarta-Selatan-Jakarta-Raya"` : URL target Jobstreet untuk lokasi Jakarta Selatan
- `-f csv` : Format output (bisa diganti `json` atau `excel`)

Hasil akan disimpan dalam file CSV seperti: `hasil_loker_Administrasi_20240115_103000.csv`

### Penggunaan Dasar (Command Line)

Jalankan dengan keyword pencarian:

```bash
python cariloker.py -k "Data Analyst"
```

### Opsi Command Line Lengkap

```bash
python cariloker.py -k "Software Engineer" -u https://jobstreet.co.id -f json --headless true
```

#### Parameter:

| Parameter | Singkatan | Default | Deskripsi |
|-----------|-----------|---------|-----------|
| `--keyword` | `-k` | *required* | Kata kunci pencarian lowongan |
| `--url` | `-u` | `https://contoh-situs-loker.com` | URL base website lowongan |
| `--format` | `-f` | `csv` | Format output: csv, json, excel |
| `--headless` | - | `true` | Mode headless browser: true/false |
| `--timeout` | - | `60000` | Timeout navigasi (ms) |
| `--output` | - | `auto` | Nama file output custom |

### Contoh Penggunaan Lainnya

```bash
# Cari Data Analyst, export ke CSV
python cariloker.py -k "Data Analyst"

# cari Software Engineer di Jobstreet, export ke JSON
python cariloker.py -k "Software Engineer" -u https://jobstreet.co.id -f json

# Cari Marketing Manager, mode visible browser
python cariloker.py -k "Marketing Manager" --headless false

# Custom output filename
python cariloker.py -k "Designer" --output lowongan_designer.csv

# Dengan timeout lebih lama
python cariloker.py -k "Developer" --timeout 90000

# Cari lowongan Akuntansi di Surabaya
python cariloker.py -k "Akuntansi" -u "https://id.jobstreet.com/id/jobs/in-Surabaya-Jawa-Timur" -f excel

# Cari lowongan IT di Bandung dengan format JSON
python cariloker.py -k "IT" -u "https://id.jobstreet.com/id/jobs/in-Bandung-Jawa-Barat" -f json
```

### Penggunaan sebagai Module Python

```python
from cariloker import JobScraper

# Initialize scraper
scraper = JobScraper(headless=True, timeout=60000)

# Run scraping
hasil = scraper.scrape_loker("https://example.com", "Data Analyst")

# Simpan ke berbagai format
scraper.save_to_csv("hasil.csv")
scraper.save_to_json("hasil.json")
scraper.save_to_excel("hasil.xlsx")

# Dapatkan ringkasan
summary = scraper.get_summary()
print(f"Total lowongan: {summary['total_lowongan']}")
```

### Custom CSS Selectors

Untuk website dengan struktur berbeda, Anda bisa customize CSS selectors:

```python
from cariloker import JobScraper

custom_selectors = {
    'card': '.vacancy-card, .job-listing',
    'title': 'h2.job-title, .position-name',
    'company': '.company-name, .employer',
    'link': 'a.job-link, .apply-button',
    'location': '.location, .city',
    'salary': '.salary, .compensation'
}

scraper = JobScraper()
hasil = scraper.scrape_loker(
    "https://target-site.com", 
    "Python Developer",
    css_selectors=custom_selectors
)
```

## 📁 Struktur Output

### CSV Format
```csv
Posisi,Perusahaan,Lokasi,Gaji,Link,Tanggal_Scraping
Data Analyst,PT Tech Company,Jakarta,Rp 8-12M,/jobs/123,2024-01-15 10:30:00
```

### JSON Format
```json
[
  {
    "Posisi": "Data Analyst",
    "Perusahaan": "PT Tech Company",
    "Lokasi": "Jakarta",
    "Gaji": "Rp 8-12M",
    "Link": "/jobs/123",
    "Tanggal_Scraping": "2024-01-15 10:30:00"
  }
]
```

### Ringkasan (Summary)
```
==================================================
RINGKASAN HASIL SCRAPING
==================================================
Total lowongan ditemukan: 25
Total perusahaan unik: 18
Perusahaan dengan lowongan terbanyak: PT Tech Company
File output: hasil_loker_Data_Analyst_20240115_103000.csv
==================================================
```

## 🔧 Konfigurasi CSS Selectors

Untuk menyesuaikan dengan website target, edit bagian ini di kode:

```python
selectors = {
    'card': '.job-card, .job-item, [data-testid="job-card"]',
    'title': 'h2, h3, .job-title, a.title',
    'company': '.company-name, .company, span.company',
    'link': 'a[href*="/job/"], a.job-link',
    'location': '.location, .job-location, span.location',
    'salary': '.salary, .salary-range, span.salary'
}
```

**Tips**: Gunakan browser DevTools (F12) untuk inspect element dan temukan CSS selector yang tepat.

## 📂 File yang Dihasilkan

- `hasil_loker_*.csv` - Hasil scraping format CSV
- `hasil_loker_*.json` - Hasil scraping format JSON
- `hasil_loker_*.xlsx` - Hasil scraping format Excel
- `cariloker.log` - Log file dengan semua aktivitas scraping

## ⚠️ Catatan Penting

1. **Etika Scraping**: 
   - Selalu robots.txt website target
   - Jangan lakukan request terlalu sering
   - Hormati terms of service website

2. **Legalitas**:
   - Pastikan penggunaan sesuai dengan hukum yang berlaku
   - Data hanya untuk keperluan pribadi/edukasi

3. **Stabilitas**:
   - Website mungkin mengubah struktur HTML
   - CSS selectors mungkin perlu update berkala
   - Beberapa website memiliki anti-bot protection

## 🐛 Troubleshooting

### Tidak ada hasil ditemukan
- Periksa CSS selector di kode
- Pastikan URL target benar
- Coba kata kunci yang berbeda
- Periksa apakah website menggunakan JavaScript rendering

### Timeout error
- Tingkatkan timeout parameter
- Periksa koneksi internet
- Website mungkin sedang down

### Deteksi bot
- Gunakan mode headless false untuk debugging
- Pastikan playwright-stealth terinstall
- Tambahkan delay antara requests

## 📦 Dependencies

- **pandas** - Data manipulation dan export
- **playwright** - Browser automation
- **playwright-stealth** - Anti-deteksi untuk Playwright
- **selectolax** - Fast HTML parser
- **openpyxl** - Excel file support

## 🤝 Kontribusi

Kontribusi sangat welcome! Silakan:

1. Fork repository
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buka Pull Request

## 📄 License

Distributed under the MIT License. Lihat `LICENSE` untuk informasi lebih lanjut.

## 👨‍💻 Author

Dibuat dengan ❤️ untuk komunitas developer Indonesia

## 🙏 Acknowledgments

- Playwright team untuk browser automation yang excellent
- Selectolax untuk HTML parsing yang super cepat
- Komunitas Python Indonesia

---

**Happy Scraping!** 🚀
