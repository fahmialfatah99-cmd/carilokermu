# 🎯 JobStreet Scraper - Sistem Pencari Lowongan Kerja Otomatis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15+-green.svg)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Scraper lowongan kerja dari JobStreet Indonesia yang dibangun dengan **Selenium + Chromium** untuk performa maksimal dan skalabilitas besar. Dilengkapi dengan fitur anti-detection, rotasi user agent, dan penyimpanan data dalam format CSV dan JSON.

## ✨ Fitur Utama

### 🔥 Fitur Inti
- **Selenium + Chromium**: Menggunakan browser automation modern untuk scraping yang lebih stabil
- **Anti-Detection**: Bypass sistem bot detection dengan teknik terbaru
- **Rotasi User Agent**: Mengganti user agent secara otomatis untuk menghindari blocking
- **Lazy Loading Handler**: Scroll otomatis untuk memuat semua konten dinamis
- **Duplicate Prevention**: Mencegah data duplikat berdasarkan URL lowongan
- **Human-Like Behavior**: Delay acak yang meniru perilaku manusia

### 📊 Fitur Skala Besar
- **Multi-Keyword Scraping**: Scraping beberapa kata kunci secara berurutan
- **Konfigurasi Fleksibel**: Pengaturan timeout, jumlah halaman, proxy, dll
- **Logging Lengkap**: Semua aktivitas tercatat dalam file log
- **Export Multi-Format**: Simpan hasil ke CSV dan JSON sekaligus
- **Error Handling**: Retry mechanism dan error recovery yang robust

### 🛡️ Fitur Keamanan
- **Headless Mode**: Operasi tanpa UI untuk server/production
- **Proxy Support**: Dukungan rotasi proxy untuk distribusi request
- **Rate Limiting**: Delay otomatis antar request
- **Session Management**: Cleanup session yang proper

## 📋 Prasyarat

- Python 3.8 atau lebih tinggi
- Google Chrome / Chromium terinstall di sistem
- Koneksi internet stabil

## 🐧 Panduan Khusus Linux (Virtual Environment)

### Mengapa Menggunakan Virtual Environment?

Virtual environment (`venv`) sangat **direkomendasikan** untuk:
- ✅ Mengisolasi dependencies project ini dari sistem
- ✅ Mencegah konflik versi package dengan project lain
- ✅ Memudahkan deployment dan cleanup
- ✅ Best practice development Python profesional

### Langkah-langkah Setup Virtual Environment di Linux

#### 1. Install Python venv (jika belum ada)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-venv python3-pip

# Fedora/RHEL
sudo dnf install python3-venv python3-pip

# Arch Linux
sudo pacman -S python-venv python-pip
```

#### 2. Buat Virtual Environment

```bash
# Masuk ke folder project
cd /workspace

# Buat virtual environment bernama 'venv'
python3 -m venv venv

# Atau jika python command tidak tersedia
python3 -m venv venv
```

#### 3. Aktifkan Virtual Environment

```bash
# Aktifkan virtual environment
source venv/bin/activate

# Anda akan melihat (venv) di awal prompt terminal
# Contoh: (venv) user@linux:~/workspace$
```

#### 4. Install Dependencies dalam Virtual Environment

```bash
# Pastikan venv aktif (lihat ada tulisan (venv) di terminal)
pip install --upgrade pip

# Install semua dependencies
pip install -r requirements.txt
```

#### 5. Jalankan Scraper

```bash
# Pastikan masih dalam virtual environment
python jalan_otomatis.py
```

#### 6. Nonaktifkan Virtual Environment

```bash
# Setelah selesai, keluar dari virtual environment
deactivate
```

### Manajemen Virtual Environment

```bash
# Cek apakah venv aktif
echo $VIRTUAL_ENV  # Akan menampilkan path venv jika aktif

# Lihat package yang terinstall di venv
pip list

# Freeze dependencies ke requirements.txt
pip freeze > requirements.txt

# Hapus virtual environment (jika ingin reset)
rm -rf venv
```

### Menjalankan dengan Cron Job (Linux Automation)

Untuk menjalankan scraper secara otomatis dengan cron:

```bash
# Edit crontab
crontab -e

# Tambahkan job (contoh: jalankan setiap hari jam 9 pagi)
0 9 * * * /workspace/venv/bin/python /workspace/jalan_otomatis.py >> /workspace/cron.log 2>&1
```

### Troubleshooting Linux

**Error: `python3-venv is not installed`**
```bash
sudo apt install python3-venv  # Ubuntu/Debian
sudo dnf install python3-venv  # Fedora
```

**Error: `pip command not found`**
```bash
sudo apt install python3-pip  # Ubuntu/Debian
```

**Permission denied saat install**
```bash
# Jangan gunakan sudo dengan pip di venv!
# Pastikan venv aktif terlebih dahulu
source venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install WebDriver (Otomatis)

WebDriver akan di-download otomatis oleh `webdriver-manager` saat pertama kali dijalankan.

## 💻 Cara Penggunaan

### Mode Interaktif (Recommended untuk Pemula)

```bash
python jalan_otomatis.py
```

Ikuti instruksi di layar:
1. Masukkan nama kota (misal: Jakarta, Bandung, Surabaya)
2. Masukkan posisi/kata kunci (misal: Admin, Programmer, Sales)
3. Tentukan batas halaman (kosongkan untuk unlimited)
4. Pilih apakah ingin melihat browser berjalan (y/n)

### Mode Programmatic (Untuk Developer)

```python
from jalan_otomatis import JobStreetScraper, ScraperConfig, save_csv, save_json

# Buat konfigurasi
config = ScraperConfig(
    max_pages=10,              # Batas halaman
    headless=True,             # Mode tanpa UI
    disable_images=True,       # Disable gambar untuk kecepatan
    rotate_user_agent=True,    # Rotasi user agent
    timeout_page_load=30,      # Timeout load halaman
    timeout_element=15         # Timeout elemen
)

# Inisialisasi scraper
scraper = JobStreetScraper(config)

# Jalankan scraping
results = scraper.scrape("Software Engineer", "Jakarta")

# Simpan hasil
if results:
    csv_data = [job.to_csv_row() for job in results]
    save_csv(csv_data, "loker_jakarta.csv")
    save_json(results, "loker_jakarta.json")
    
    print(f"✅ Ditemukan {len(results)} lowongan!")
```

### Mode Multi-Keyword

```python
from jalan_otomatis import MultiKeywordScraper, ScraperConfig

config = ScraperConfig(max_pages=5, headless=True)
multi_scraper = MultiKeywordScraper(config)

keywords = ["Programmer", "Developer", "Engineer", "IT Staff"]
results = multi_scraper.scrape_multiple(keywords, "Jakarta")

# Simpan semua hasil
multi_scraper.save_all_results("loker_it_jakarta", format="both")
```

## 📁 Struktur Output

### Format CSV
```csv
No,Posisi,Perusahaan,Lokasi,Gaji,Tipe Pekerjaan,Pengalaman,Pendidikan,Tanggal Posting,Deskripsi Singkat,Link,Waktu Scraping
1,Software Engineer,PT Tech Company,Jakarta,Rp 8-12 juta,Full-time,2 tahun,S1,2 hari yang lalu,Mencari software engineer...,https://id.jobstreet.com/...,2024-01-15 10:30:00
```

### Format JSON
```json
[
  {
    "no": 1,
    "posisi": "Software Engineer",
    "perusahaan": "PT Tech Company",
    "lokasi": "Jakarta",
    "gaji": "Rp 8-12 juta",
    "tipe_pekerjaan": "Full-time",
    "pengalaman": "2 tahun",
    "pendidikan": "S1",
    "tanggal_posting": "2 hari yang lalu",
    "deskripsi_singkat": "Mencari software engineer...",
    "link": "https://id.jobstreet.com/...",
    "waktu_scraping": "2024-01-15 10:30:00",
    "page_number": 1
  }
]
```

## ⚙️ Konfigurasi Lanjutan

### ScraperConfig Options

| Parameter | Tipe | Default | Deskripsi |
|-----------|------|---------|-----------|
| `max_pages` | int | 10 | Jumlah maksimal halaman yang discrape |
| `max_jobs_per_page` | int | 50 | Maksimal jobs per halaman |
| `timeout_page_load` | int | 30 | Timeout untuk load halaman (detik) |
| `timeout_element` | int | 15 | Timeout untuk menunggu elemen (detik) |
| `scroll_delay` | float | 2.0 | Delay saat scroll (detik) |
| `click_delay` | float | 1.5 | Delay saat klik (detik) |
| `headless` | bool | True | Mode tanpa UI browser |
| `disable_images` | bool | True | Disable loading gambar |
| `use_proxy` | bool | False | Aktifkan proxy |
| `proxy_list` | List[str] | None | Daftar proxy server |
| `rotate_user_agent` | bool | True | Rotasi user agent |
| `max_workers` | int | 3 | Jumlah worker untuk multi-threading |
| `retry_attempts` | int | 3 | Jumlah percobaan retry |
| `save_format` | str | 'csv' | Format penyimpanan (csv/json/both) |

### Contoh Konfigurasi Proxy

```python
config = ScraperConfig(
    use_proxy=True,
    proxy_list=[
        "http://proxy1.example.com:8080",
        "http://proxy2.example.com:8080",
        "socks5://proxy3.example.com:1080"
    ],
    rotate_user_agent=True
)
```

## 📊 Logging

Semua aktivitas dicatat dalam file `job_scraper.log`:

```bash
tail -f job_scraper.log  # Linux/Mac
Get-Content job_scraper.log -Tail 50 -Wait  # Windows PowerShell
```

## 🎯 Tips untuk Hasil Maksimal

### 1. Untuk Skala Besar
- Gunakan mode `headless=True` untuk kecepatan
- Set `disable_images=True` untuk mengurangi bandwidth
- Gunakan proxy rotation untuk menghindari IP ban
- Tambahkan delay yang cukup antar request

### 2. Untuk Kualitas Data
- Scraping di jam kerja (9 AM - 5 PM) untuk data fresh
- Gunakan keyword yang spesifik
- Set `max_pages` sesuai kebutuhan

### 3. Untuk Menghindari Blocking
- Rotasi user agent selalu aktif
- Gunakan delay random (sudah default)
- Jangan scrape terlalu banyak halaman sekaligus
- Gunakan proxy jika scraping intensif

## 🐛 Troubleshooting

### Error: "Chrome tidak ditemukan"
```bash
# Install Chromium
sudo apt-get install chromium-browser  # Ubuntu/Debian
brew install chromium  # macOS
```

### Error: "WebDriverException"
```bash
# Reinstall webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager
```

### Error: "TimeoutException"
- Tingkatkan `timeout_page_load` dan `timeout_element`
- Periksa koneksi internet
- Coba gunakan proxy

### Error: "Tidak ada lowongan ditemukan"
- Periksa keyword dan lokasi
- Website mungkin sedang maintenance
- Coba gunakan keyword yang lebih umum

## 📝 Contoh Kasus Penggunaan

### 1. Monitoring Lowongan Harian
```python
# Script untuk cron job harian
from jalan_otomatis import JobStreetScraper, ScraperConfig, save_csv
from datetime import datetime

config = ScraperConfig(max_pages=5, headless=True)
scraper = JobStreetScraper(config)

today = datetime.now().strftime("%Y%m%d")
results = scraper.scrape("Data Scientist", "Remote")

if results:
    save_csv([j.to_csv_row() for j in results], f"daily_loker_{today}.csv")
```

### 2. Bulk Scraping Multiple Cities
```python
cities = ["Jakarta", "Bandung", "Surabaya", "Yogyakarta"]
keyword = "Marketing"

all_results = []
for city in cities:
    scraper = JobStreetScraper(ScraperConfig(max_pages=3))
    results = scraper.scrape(keyword, city)
    all_results.extend(results)

# Save combined results
save_csv([j.to_csv_row() for j in all_results], f"marketing_all_cities.csv")
```

## 🔒 Etika Penggunaan

⚠️ **PENTING**: Gunakan tool ini dengan bijak dan bertanggung jawab:
- Hormati `robots.txt` website target
- Jangan overload server dengan request berlebihan
- Gunakan untuk keperluan pribadi/edukasi
- Patuhi Terms of Service JobStreet
- Jangan gunakan untuk komersialisasi data tanpa izin

## 📄 License

MIT License - lihat file LICENSE untuk detail.

## 🤝 Kontribusi

Kontribusi sangat diapresiasi! Silakan:
1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support

Jika mengalami masalah:
1. Cek file `job_scraper.log` untuk detail error
2. Pastikan semua dependencies terinstall
3. Update Chrome/Chromium ke versi terbaru
4. Buka issue di GitHub dengan detail error

## 🗺️ Roadmap

- [ ] Support multiple job portals (LinkedIn, Kalibrr, etc.)
- [ ] GUI interface dengan Tkinter/PyQt
- [ ] API endpoint untuk integrasi
- [ ] Database storage (SQLite/PostgreSQL)
- [ ] Email notification untuk lowongan baru
- [ ] Dashboard analytics
- [ ] Docker containerization

---

**Dibuat dengan ❤️ untuk komunitas developer Indonesia**

*Last Updated: 2024*
