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

### Langkah Instalasi

1. Clone atau download repository ini

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install pandas playwright playwright-stealth selectolax
```

3. Install browser Playwright:
```bash
playwright install chromium
```

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
```bash
python main.py
```

3. Hasil akan tersimpan di file `hasil_loker.csv`

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

## 🔧 Troubleshooting

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
