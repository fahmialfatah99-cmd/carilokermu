# 🚀 Jalan Otomatis - Selenium Max Scraper JobStreet

Tool scraping lowongan kerja **MAKSIMAL** menggunakan **Selenium + Chromium** dengan konfigurasi optimal untuk hasil skala besar tanpa batasan.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Selenium](https://img.shields.io/badge/selenium-latest-success)

## ✨ Fitur Utama

- ✅ **SCRAPING MAKSIMAL TANPA BATASAN**: Scraping berjalan terus hingga data habis (bisa dibatasi manual).
- ✅ **DATA GAJI & PERUSAHAAN WAJIB ADA**: Validasi otomatis memastikan data penting selalu tersedia.
- ✅ **SKALA BESAR**: Dirancang untuk scraping ratusan/halaman tanpa henti.
- ✅ **Anti-Deteksi Canggih**: 
  - User agent random dengan `fake-useragent`
  - Stealth mode dengan CDP commands
  - Disable automation flags
  - Window size dan viewport realistis
- ✅ **Multi-Selector Fallback**: Beberapa selector CSS untuk setiap elemen agar tidak gagal ambil data.
- ✅ **Scroll Otomatis**: Trigger lazy loading untuk memuat semua konten.
- ✅ **Retry & Error Handling**: Tahan terhadap error network dan timeout.
- ✅ **Export CSV Lengkap**: 12 kolom data termasuk Gaji, Perusahaan, Posisi, Lokasi, dll.
- ✅ **Logging Real-time**: Memantau proses scraping dengan detail.

---

## 📋 Prasyarat

### 1. Instalasi di Linux (Ubuntu/Debian/Kali/Mint)

```bash
# Update paket
sudo apt update

# Install Python & Pip
sudo apt install python3 python3-pip python3-venv chromium-browser -y

# Buat virtual environment (opsional tapi disarankan)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Instalasi di Windows

```bash
# Install Python dari python.org (pastikan centang "Add to PATH")

# Buka Command Prompt atau PowerShell
pip install -r requirements.txt

# Download dan install Chrome dari https://www.google.com/chrome/
# ChromeDriver akan diinstall otomatis oleh webdriver-manager
```

### 3. Instalasi di macOS

```bash
# Install Python via Homebrew
brew install python

# Install dependencies
pip install -r requirements.txt

# Install Chrome
brew install --cask google-chrome
```

---

## 📁 File Utama

| File | Deskripsi |
|------|-----------|
| `jalan_otomatis.py` | **SCRAPER MAKSIMAL** dengan Selenium + Chromium untuk hasil skala besar |

---

## 🚀 Cara Penggunaan

### Langkah Cepat

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Jalankan scraper
python jalan_otomatis.py
```

### Langkah Detail

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Pastikan Chrome/Chromium Terinstall**
   - Linux: `sudo apt install chromium-browser`
   - Windows: Download dari https://www.google.com/chrome/
   - macOS: `brew install --cask google-chrome`

3. **Jalankan Script**
   ```bash
   python jalan_otomatis.py
   ```

4. **Ikuti Instruksi:**
   - Masukkan posisi/jabatan (contoh: `staff`, `admin`, `programmer`)
   - Masukkan lokasi (contoh: `Jakarta`, `Surabaya`)
   - Tentukan batas halaman (tekan **Enter** untuk unlimited)
   - Pilih mode headless (`y` = browser tersembunyi, `n` = browser terlihat)

5. **Hasil Tersimpan Otomatis**
   - Format: `loker_max_<posisi>_<lokasi>_<timestamp>.csv`
   - Contoh: `loker_max_staff_Jakarta_20240127_163000.csv`

---

## 📊 Format Output CSV

File CSV mengandung **12 kolom lengkap**:

| Kolom | Deskripsi |
|-------|-----------|
| No | Nomor urut data |
| Posisi | Nama jabatan/posisi pekerjaan |
| **Perusahaan** | Nama perusahaan **(WAJIB ADA)** ✅ |
| Lokasi | Lokasi pekerjaan |
| **Gaji** | Informasi gaji **(WAJIB ADA)** 💰 ✅ |
| Tipe Pekerjaan | Full-time, Part-time, Contract, dll |
| Pengalaman | Pengalaman yang dibutuhkan |
| Pendidikan | Tingkat pendidikan minimal |
| Tanggal Posting | Kapan lowongan diposting |
| Deskripsi Singkat | Ringkasan deskripsi pekerjaan (max 300 karakter) |
| Link | URL lengkap ke lowongan |
| Waktu Scraping | Waktu pengambilan data |

**Catatan Penting:**
- Hanya lowongan yang memiliki **GAJI** dan **PERUSAHAAN** yang disimpan
- Data divalidasi otomatis sebelum ditambahkan ke hasil

---

## ⚙️ Konfigurasi Lanjutan

### Konfigurasi Default di Kode

Script sudah dikonfigurasi dengan setting optimal untuk scraping maksimal:

```python
# Konfigurasi maksimal untuk scraping skala besar
MAX_RETRY = 3              # Jumlah percobaan ulang jika gagal
SCROLL_PAUSE = 2           # Jeda saat scroll (detik)
PAGE_LOAD_TIMEOUT = 60     # Timeout load halaman (detik)
ELEMENT_WAIT_TIMEOUT = 15  # Timeout tunggu elemen (detik)
```

### Mode Headless vs Visible

- **Headless (y)**: Browser tersembunyi, lebih cepat, cocok untuk server/VPS
- **Visible (n)**: Browser terlihat, lebih stabil, bisa monitor proses

### Membatasi Halaman

Untuk testing atau menghemat waktu, masukkan angka saat diminta:
- `3` = hanya scrape 3 halaman
- `10` = hanya scrape 10 halaman
- `Enter` (kosong) = unlimited sampai data habis

---

## 🔧 Troubleshooting

### Error: "No module named 'selenium'"
```bash
pip install selenium webdriver-manager fake-useragent
```

### Error: "ChromeDriver not found"
- Pastikan Chrome/Chromium browser sudah terinstall
- `webdriver-manager` akan download ChromeDriver otomatis
- Jika masih error, reinstall Chrome

### Error: "SessionNotCreatedException" atau "DevToolsActivePort file doesn't exist"
```bash
# Di Linux, tambahkan flag ini di kode atau jalankan sebagai user biasa
# Jangan run sebagai root tanpa flag --no-sandbox
```

### Scraping Berhenti di Tengah Jalan / Tidak Ada Data
- **JobStreet mungkin mendeteksi bot** - Coba mode visible (jawab `n` saat ditanya headless)
- **Koneksi internet tidak stabil** - Pastikan koneksi bagus
- **IP diblokir** - Gunakan VPN/proxy residential
- **Struktur website berubah** - Selector CSS mungkin perlu diupdate

### Data yang Diambil Sedikit/Nol
- Website menggunakan proteksi bot yang ketat
- Coba gunakan VPN dengan IP Indonesia
- Ubah kata kunci pencarian (misal: "staff" → "admin")
- Jalankan di waktu traffic rendah (malam/pagi dini hari)

### Browser Terbuka Tapi Langsung Tutup
- Cek log error di console
- Pastikan Chrome versi terbaru
- Reinstall dependencies: `pip uninstall selenium && pip install selenium`

---

## 📝 Catatan Penting

### 1. Etika Scraping
- Gunakan dengan bijak, jangan overload server JobStreet
- Patuhi `robots.txt` dan Terms of Service
- Gunakan untuk keperluan pribadi/edukasi
- Beri delay antar request (sudah ada di script)

### 2. Legalitas
- Data yang diambil adalah data publik
- Jangan gunakan untuk komersialisasi tanpa izin
- Hormati hak cipta dan ketentuan JobStreet
- Bertanggung jawab atas penggunaan data

### 3. Kinerja
- Scraping unlimited bisa memakan waktu lama (bergantung jumlah halaman)
- Disarankan batasi halaman untuk testing awal
- File CSV besar bisa dibuka dengan Excel, Google Sheets, atau LibreOffice Calc
- Script dirancang untuk stabilitas jangka panjang

### 4. Proteksi Bot JobStreet
JobStreet memiliki proteksi bot yang cukup ketat. Jika mengalami blocking:
- Gunakan **VPN** dengan IP Indonesia/residential
- Gunakan **proxy rotating**
- Jalankan di waktu traffic rendah
- Gunakan mode **visible** (bukan headless)
- Kurangi kecepatan dengan menambah delay

### 5. Tips Hasil Maksimal
✅ **Gunakan VPN/proxy** untuk menghindari blocking  
✅ **Mode visible** lebih stabil daripada headless  
✅ **Koneksi internet stabil** sangat penting  
✅ **Waktu eksekusi**: malam/pagi (traffic rendah)  
✅ **Keyword spesifik** menghasilkan data lebih relevan  
✅ **Validasi otomatis** memastikan hanya data berkualitas tersimpan  

---

## 📦 Dependencies

Semua dependencies tercantum dalam `requirements.txt`:

```txt
selenium>=4.15.0
webdriver-manager>=4.0.0
fake-useragent>=1.4.0
```

Install dengan:
```bash
pip install -r requirements.txt
```

**Penjelasan:**
- `selenium` - Automasi browser Chromium
- `webdriver-manager` - Manage ChromeDriver otomatis
- `fake-useragent` - User agent random anti-deteksi

---

## 🎯 Keunggulan Script Ini

| Fitur | Keterangan |
|-------|------------|
| **Multi-Selector** | 5+ selector fallback per elemen |
| **Validasi Wajib** | Gaji & Perusahaan harus ada |
| **Stealth Mode** | CDP commands untuk hide automation |
| **Auto Scroll** | Trigger lazy loading maksimal |
| **Error Recovery** | Retry otomatis jika gagal |
| **Unlimited Pages** | Bisa scrape ratusan halaman |
| **CSV Lengkap** | 12 kolom data siap analisis |

---

## 📞 Support

Jika mengalami masalah:
1. Pastikan Chrome/Chromium terinstall
2. Jalankan `pip install -r requirements.txt`
3. Coba mode visible (bukan headless)
4. Gunakan VPN jika terkena blocking
5. Cek log error di console untuk detail

---

## 📄 License

Project ini dilisensikan di bawah **MIT License**.

---

## ⚠️ Disclaimer

- Script ini untuk tujuan **edukasi dan pembelajaran**
- Penulis tidak bertanggung jawab atas penyalahgunaan
- Hormati Terms of Service JobStreet
- Gunakan dengan bijak dan bertanggung jawab

---

**Dibuat dengan ❤️ untuk scraping maksimal skala besar**

*Last Updated: 2024 - Selenium + Chromium Max Scraper*
