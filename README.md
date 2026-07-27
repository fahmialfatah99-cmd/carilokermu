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
