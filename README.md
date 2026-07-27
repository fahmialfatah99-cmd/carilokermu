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

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:

```bash
pip install pandas playwright playwright-stealth selectolax openpyxl
```

### 3. Install Browser Playwright

```bash
playwright install chromium
```

## 📖 Cara Penggunaan

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

### Contoh Penggunaan

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
