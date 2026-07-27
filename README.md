# 🔍 CariLokerMu - Job Portal Scraper & Auto Apply

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Aplikasi otomatis untuk mencari, melamar, dan mengelola lowongan kerja dari berbagai job portal (khususnya **Jobstreet**) dengan fitur scraping cerdas, generator CV otomatis, dan auto-submit aplikasi.

---

## ✨ Fitur Utama

| Fitur | Deskripsi | Status |
|-------|-----------|--------|
| 🔍 **Smart Scraping** | Mencari lowongan berdasarkan keyword & lokasi | ✅ Siap Pakai |
| 📄 **Auto CV Generator** | Buat CV & Cover Letter otomatis dalam format DOCX/PDF | ✅ Siap Pakai |
| 🤖 **Auto Apply Jobstreet** | Lamar otomatis ke semua lowongan di Jobstreet | ✅ Siap Pakai |
| 📊 **Export Data** | Simpan hasil pencarian ke CSV/Excel | ✅ Siap Pakai |
| 🎯 **Multi-Mode** | Mode Easy, Manual, dan Auto Apply | ✅ Siap Pakai |
| 🌐 **Auto-Buka Browser** | Browser terbuka otomatis untuk proses scraping & apply | ✅ Siap Pakai |
| ⌨️ **Ketik Otomatis** | Input field diisi otomatis seperti manusia mengetik | ✅ Siap Pakai |
| 📍 **Pilih Lokasi Manual** | Bisa memilih lokasi spesifik sesuai kebutuhan | ✅ Siap Pakai |

---

## 📋 Prasyarat

Pastikan Anda telah menginstall:
- Python 3.8 atau lebih baru
- pip (Python package manager)
- Chrome/Chromium browser (untuk auto apply)

---

## 🛠️ Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/username/carilokermu.git
cd carilokermu
```

### 2. Setup Virtual Environment (Wajib)
Kita menggunakan `venv` untuk mengisolasi dependensi proyek agar tidak bentrok dengan paket sistem Linux.

```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Verifikasi: Harus muncul (venv) di awal prompt terminal Anda
# Contoh: (venv) fahmial@linux:~/carilokermu$
```

> 💡 **Tips Linux**: Jika perintah `python3 -m venv` gagal, install paket `python3-venv`:
> - Ubuntu/Debian: `sudo apt install python3-venv`
> - Fedora/RHEL: `sudo dnf install python3-virtualenv`

### 3. Install Dependencies Python
Dengan status `(venv)` aktif di terminal, install semua library yang dibutuhkan:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Browser Engine Playwright (WAJIB!)

Ini adalah langkah yang **sering terlewatkan** dan menyebabkan error `Playwright tidak terinstall`.
Playwright membutuhkan browser engine khusus yang harus diunduh terpisah.

```bash
# Unduh dan install Chromium engine untuk Playwright
playwright install chromium

# (Opsional) Install dependencies sistem Linux jika diperlukan
playwright install-deps chromium
```

> ⚠️ **PENTING**: 
> - Jangan lewatkan langkah ini! Error `Playwright tidak terinstall` muncul karena browser engine belum diunduh.
> - Perintah ini hanya perlu dilakukan **sekali saja** setelah instalasi awal.
> - Ukuran download sekitar 100-150 MB.

---

### 5. Setup Browser Sistem (Khusus Chromium di Linux)

Jika Anda menggunakan **Chromium** bawaan sistem Linux (bukan yang diunduh Playwright), pastikan driver-nya terinstall:

#### **Untuk Ubuntu/Debian/Mint:**
```bash
sudo apt update
sudo apt install chromium-browser chromium-chromedriver -y
```

#### **Untuk Fedora/RHEL/CentOS:**
```bash
sudo dnf install chromium chromium-chromedriver -y
```

#### **Verifikasi Instalasi:**
```bash
chromium --version
chromium-chromedriver --version
```
*Pastikan versi utama keduanya sama (misal: v120.x.xxx).*

> ⚠️ **Penting untuk Pengguna Snap (Ubuntu 22.04+)**:
> Jika Chromium terinstall via Snap, mungkin ada masalah izin. Jalankan ini:
> ```bash
> sudo snap connect chromium:home
> ```

#### **Alternatif: Menggunakan Google Chrome**
Jika lebih memilih Chrome resmi:
```bash
# Download dan install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y  # Fix dependencies jika ada error
```

---

### 🔧 Troubleshooting Instalasi

| Sistem Operasi | Masalah Umum | Solusi |
|----------------|--------------|--------|
| **Linux (Chromium)** | `chromium` tidak ditemukan | Install: `sudo apt install chromium-browser chromium-chromedriver -y` |
| **Linux (Chromium)** | ChromeDriver version mismatch | Pastikan versi chromedriver sesuai: `chromium-chromedriver --version` |
| **Linux (Chrome)** | `Permission denied` saat install | Gunakan `sudo` atau `--user` flag: `pip3 install --user -r requirements.txt` |
| **Linux (Chrome)** | Chrome tidak ditemukan | Pastikan path Chrome: `/usr/bin/google-chrome` |
| **Linux (Snap)** | Chromium tidak bisa akses folder | Berikan permission: `sudo snap connect chromium:home` |
| **macOS** | Certificate verify failed | Jalankan: `/Applications/Python\ 3.x/Install\ Certificates.command` |
| **Windows** | `pip` tidak dikenali | Tambahkan Python ke PATH atau gunakan `py -m pip` |
| **Semua** | Module `docx` tidak ditemukan | Aktifkan venv dulu, lalu: `pip install python-docx reportlab` |

#### Tips Khusus Linux Users dengan Chromium

```bash
# Jika Chromium tidak mau jalan sebagai root
export CHROME_ALLOW_ROOT=1

# Jika ada masalah permission pada folder output
chmod -R 755 /path/to/carilokermu/

# Cek apakah Chromium terinstall dengan benar
chromium --version

# Cek chromedriver
chromium-chromedriver --version

# Jika menggunakan Snap (Ubuntu 22.04+)
# Hubungkan permission home agar bisa akses file
sudo snap connect chromium:home

# Set path browser secara manual jika diperlukan
export CHROME_PATH=/usr/bin/chromium
```

---

## 🚀 Cara Penggunaan (Step-by-Step)

Berikut adalah panduan lengkap penggunaan dari awal hingga melamar otomatis:

### **Langkah 1: Cari Lowongan Kerja (INTERAKTIF)**

Script `main.py` sekarang memiliki menu interaktif untuk memilih lowongan langsung setelah scraping!

```bash
python3 main.py
```

**Program akan memandu Anda melalui:**

1. **Input posisi/kata kunci** (contoh: `admin`, `data analyst`)
2. **Input lokasi/kota** (contoh: `Jakarta`, `Surabaya`) - bisa dipilih manual
3. **Input jumlah halaman** yang akan di-scrape (default: 3)
4. **Browser terbuka otomatis** untuk menampilkan proses scraping
5. **Input field diisi otomatis** seperti manusia mengetik
6. **Menampilkan daftar lowongan** yang ditemukan
7. **Memilih lowongan** untuk dilamar:
   - Input nomor lowongan (pisahkan dengan koma untuk multiple)
   - Ketik `all` untuk memilih semua
   - Ketik `q` untuk keluar
8. **Generate CV otomatis** (opsional) untuk lowongan terpilih

**Contoh Sesi Lengkap:**
```
============================================================
🔍 PENCARI LOWONGAN KERJA OTOMATIS (JOBSTREET)
============================================================

💼 Posisi / Kata Kunci (contoh: Admin, Staff Gudang): Admin
📍 Lokasi / Kota (contoh: Jakarta, Surabaya): Jakarta
📄 Jumlah Halaman (default 3): 3

⏳ Memulai pencarian: 'Admin' di 'Jakarta'...
------------------------------------------------------------
🌐 Membuka Jobstreet.co.id...
⌨️ Mengetik posisi: 'Admin'...
⌨️ Mengetik lokasi: 'Jakarta'...
🔍 Mengklik tombol cari...

📄 Memproses Halaman 1...
   Ditemukan 10 lowongan di halaman ini.
   [1] Staff Administrasi - PT Maju Jaya
   [2] Admin Officer - CV Berkah Sentosa
   ...

============================================================
✅ SELESAI! Total lowongan ditemukan: 30
💾 Disimpan ke: loker_admin_jakarta_20260727_160440.csv
============================================================
```

**Fitur Unggulan:**
- ✅ **Auto-buka browser**: Browser terbuka otomatis untuk melihat proses
- ✅ **Ketik otomatis**: Input field diisi karakter per karakter seperti manusia
- ✅ **Pilih lokasi manual**: Bisa menentukan lokasi spesifik sesuai kebutuhan
- ✅ **Tanpa error**: Handle error yang baik dengan fallback metode alternatif

---

### **Langkah 2: Generate CV & Cover Letter (Opsional)**

Jika Anda melewatkan generate CV di Langkah 1, atau ingin membuat CV baru:

```bash
python3 auto_cv_selector.py
```

**Proses Interaktif:**
1. Script akan membaca file CSV hasil scraping terbaru
2. Menampilkan daftar lowongan yang ditemukan
3. **Anda diminta memilih nomor lowongan** yang ingin dilamar (bisa pilih beberapa)
4. CV dan Cover Letter akan dibuat otomatis dalam format `.docx` dan `.pdf`
5. File tersimpan di folder `carilokermu/cv_generated/`

**Contoh Output:**
```
================================================================================
🚀 AUTO CV GENERATOR - PILIH LOWONGAN & LAMAR OTOMATIS
================================================================================

📂 Memuat data diri...
✅ Data diri dimuat: Nama Anda

📂 Memuat hasil scraping...
📄 Membaca dari: loker_admin_jakarta_20260727_160440.csv

================================================================================
📋 DAFTAR LOWONGAN TERSEDIA
================================================================================

[1] Staff Administrasi
    🏢 Perusahaan: PT Maju Jaya
    📍 Lokasi: Jakarta
    💰 Gaji: N/A
    📅 Scraped: 2026-07-27 16:04:40
    🔗 Link: https://www.jobstreet.co.id/job/...

👉 Masukkan nomor lowongan yang ingin dilamar (atau 0 untuk keluar): 1

🎯 Anda memilih: Staff Administrasi di PT Maju Jaya

👉 Lanjutkan generate CV & Cover Letter? (y/n): y

⚙️  Generating CV...
✅ CV berhasil dibuat: CV_Nama_Administrasi_20260727_160440.docx

⚙️  Generating Cover Letter...
✅ Cover Letter berhasil dibuat: CoverLetter_Nama_Administrasi_20260727_160440.docx
```

**Tips:** 
- Jika ingin melamar semua lowongan, skip langkah ini dan gunakan CV default
- Gunakan langkah ini untuk melamar ke posisi favorit dengan CV yang lebih targeted

---

### **Langkah 3: Auto Apply ke Jobstreet**

Setelah memiliki daftar lowongan dan CV, jalankan auto apply untuk melamar secara otomatis.

```bash
python3 auto_apply_jobstreet.py
```

**Cara Kerja:**
1. Script akan membuka browser Chromium secara otomatis
2. Anda harus **login manual sekali** ke akun Jobstreet Anda
3. Setelah login, script akan:
   - Membaca file CSV hasil scraping
   - Membuka satu per satu link lowongan
   - Mengisi form lamaran otomatis
   - Upload CV (jika ada di folder `carilokermu/` atau CV default)
   - Submit aplikasi
4. Progress ditampilkan di terminal

**Catatan Penting:**
- Jangan tutup browser saat proses berjalan
- Pastikan koneksi internet stabil
- Jika terjadi captcha, selesaikan manual lalu lanjutkan (script akan menunggu)

---

## 📂 Struktur Output

Setelah menjalankan seluruh proses, Anda akan memiliki struktur file seperti ini:

```
carilokermu/
├── loker_admin_jakarta_20260727_160440.csv    # Hasil scraping lowongan
├── cv_generated/
│   ├── CV_Nama_Administrasi.docx           # CV format Word
│   ├── CV_Nama_Administrasi.pdf            # CV format PDF
│   └── Cover_Letter_Nama.docx        # Surat lamaran
├── logs/
│   └── auto_apply_20260727.log       # Log proses auto apply
└── carilokermu/
    └── data_diri.json             # Data diri pengguna
```

---

## ⚙️ Konfigurasi

### Mengatur Data Diri
Edit file `carilokermu/data_diri.json` untuk mengisi data diri yang akan digunakan pada CV dan form lamaran:

```json
{
  "nama_lengkap": "Nama Anda",
  "email": "email@anda.com",
  "telepon": "08123456789",
  "linkedin": "linkedin.com/in/anda",
  "pendidikan_nama": "Universitas Contoh",
  "pendidikan_jurusan": "Teknik Informatika",
  "pendidikan_gelar": "S1",
  "pendidikan_tahun_masuk": "2018",
  "pendidikan_tahun_lulus": "2022",
  "pendidikan_ipk": "3.75",
  "pengalaman_jumlah": "2",
  "keahlian_teknis": "Python, JavaScript, SQL",
  "keahlian_soft_skill": "Komunikasi, Teamwork",
  "bahasa": "Indonesia, Inggris"
}
```

---

## 🔧 Troubleshooting

### Masalah Instalasi

| Sistem Operasi | Masalah Umum | Solusi |
|----------------|--------------|--------|
| **Linux (Ubuntu/Debian)** | `Permission denied` saat install | Gunakan: `pip3 install --user -r requirements.txt` |
| **Linux** | Chrome tidak ditemukan | Pastikan path: `/usr/bin/google-chrome` atau install ulang |
| **Linux** | Error `dpkg` saat install Chrome | Jalankan: `sudo apt-get install -f -y` |
| **macOS** | Certificate verify failed | Jalankan: `/Applications/Python\ 3.x/Install\ Certificates.command` |
| **Windows** | `pip` tidak dikenali | Tambahkan Python ke PATH atau gunakan `py -m pip` |
| **Semua** | Module `docx` tidak ditemukan | Aktifkan venv dulu, lalu: `pip install python-docx reportlab` |

### Masalah Saat Running

| Masalah | Solusi |
|---------|--------|
| Browser tidak terbuka saat auto apply | Pastikan Chrome/Chromium terinstall dan tertutup sebelum menjalankan script |
| Login Jobstreet gagal | Clear cookie browser atau gunakan mode incognito manual |
| CSV kosong/tidak ada data | Coba ubah keyword, tambah jumlah loker, atau cek koneksi internet |
| Auto apply stuck di captcha | Selesaikan captcha manual, script akan lanjut otomatis setelah 30 detik |
| CV tidak tergenerate | Cek folder `cv_generated/` dan pastikan `carilokermu/data_diri.json` sudah diisi |
| Error `Connection Reset` | Tunggu 5-10 menit lalu jalankan lagi (rate limiting) |
| Script terlalu lambat | Normal, script memberi delay 3-5 detik antar lamaran untuk hindari blokir |
| Chromium tidak bisa akses folder home | Jalankan: `sudo snap connect chromium:home` (untuk Snap users) |
| Versi ChromeDriver tidak match | Update chromedriver: `sudo apt install --reinstall chromium-chromedriver` |

### Tips untuk Linux Users (Chrome & Chromium)

```bash
# Jika browser tidak mau jalan sebagai root
export CHROME_ALLOW_ROOT=1

# Jika ada masalah permission pada folder output
chmod -R 755 /path/to/carilokermu/

# Cek apakah browser terinstall dengan benar
chromium --version      # Untuk Chromium
google-chrome --version # Untuk Chrome

# Install chromedriver jika diperlukan
sudo apt install chromium-chromedriver -y  # Untuk Chromium

# Set path browser secara manual jika script tidak menemukannya
export CHROME_PATH=/usr/bin/chromium
# atau
export CHROME_PATH=/usr/bin/google-chrome

# Untuk Snap users (Ubuntu 22.04+)
sudo snap connect chromium:home
```

---

## 📝 Contoh Skenario Penggunaan

### Skenario 1: Lamar Cepat (5 Menit)
```bash
# 1. Cari 10 loker admin
python3 main.py

# 2. Langsung auto apply (pakai CV default)
python3 auto_apply_jobstreet.py
```

### Skenario 2: Pilih Lowongan Favorit & Generate CV Custom
```bash
# 1. Cari 20 loker
python3 main.py

# 2. Jalankan selector untuk memilih lowongan favorit secara interaktif
#    Script akan menampilkan daftar dan Anda pilih nomor yang diinginkan
python3 auto_cv_selector.py
#    >> Masukkan pilihan: 1,3,5 (pilih 3 lowongan terbaik)

# 3. Auto apply dengan CV custom yang sudah dibuat
python3 auto_apply_jobstreet.py
```

### Skenario 3: Monitoring & Analisis
```bash
# 1. Cari 50 loker untuk analisis pasar
python3 main.py

# 2. Buka CSV di Excel untuk analisis
# 3. Filter manual loker yang sesuai
# 4. Gunakan auto_cv_selector.py untuk pilih yang terbaik
python3 auto_cv_selector.py

# 5. Auto apply hanya untuk yang terpilih
python3 auto_apply_jobstreet.py
```

---

## 🚧 Batasan & Catatan

1. **Jobstreet Only:** Fitur auto apply saat ini hanya mendukung Jobstreet karena konsistensi form
2. **Rate Limit:** Jangan jalankan terlalu cepat untuk menghindari blokir IP
3. **Captcha:** Beberapa website mungkin menampilkan captcha yang harus diselesaikan manual
4. **Update UI:** Jika Jobstreet mengubah tampilan form, script perlu diupdate

---

## 📄 License

MIT License - lihat file [LICENSE](LICENSE) untuk detail

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan buat issue atau pull request untuk:
- Menambahkan support job portal lain
- Memperbaiki bug
- Menambah fitur baru

---

## 📞 Support

Jika mengalami kendala, buka issue di GitHub atau hubungi:
- Email: support@carilokermu.com
- Telegram: @carilokermu_support

---

**Happy Job Hunting! 🎯**
