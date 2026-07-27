# 🇮🇩 JobStreet Job Scraper

> **Scraper lowongan kerja JobStreet tanpa login, tanpa cookies, dan alur yang mulus.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)
![License](https://img.shields.io/badge/License-Fahmi%20Alfatah-orange.svg)

---

## ✨ Fitur

- ✅ **Tanpa Login** – Tidak perlu akun atau autentikasi
- ✅ **Tanpa Cookies** – Bersih, tidak menyimpan sesi
- ✅ **Alur Mulus** – Langsung scrape & simpan CSV
- ✅ **Multi-Platform** – Support Windows, macOS, Linux
- ✅ **Browser Otomatis** – Menggunakan Playwright (Chromium)
- ✅ **Headless Mode** – Otomatis untuk Linux tanpa GUI
- ✅ **Target JobStreet** – Khusus jobstreet.co.id

---

## 🚀 Instalasi & Penggunaan

### 🐧 **LINUX UBUNTU**

#### 1. Install Python & Dependencies Sistem

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

#### 2. Buat Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Install Browser Engine (Playwright)

```bash
playwright install chromium
```

> ⚠️ **Catatan untuk Ubuntu:** Jika muncul error saat menjalankan playwright, install dependencies tambahan:
> ```bash
> playwright install-deps chromium
> ```

#### 5. Jalankan Program

```bash
python main.py
```

> 💡 **Mode Headless:** Jika Anda menggunakan Ubuntu Server tanpa GUI, program akan otomatis berjalan dalam mode headless (tanpa window browser).

---

### 🪟 **WINDOWS**

#### 1. Pastikan Python Terinstall

Download dan install Python dari [python.org](https://www.python.org/downloads/)

> ✅ Centang **"Add Python to PATH"** saat instalasi

#### 2. Buat Virtual Environment

Buka **Command Prompt (CMD)** atau **PowerShell**:

```cmd
python -m venv venv
venv\Scripts\activate
```

> Setelah aktivasi, akan muncul `(venv)` di awal prompt

#### 3. Install Dependencies Python

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Install Browser Engine (Playwright)

```cmd
playwright install chromium
```

#### 5. Jalankan Program

```cmd
python main.py
```

> 💡 Browser Chromium akan terbuka secara otomatis saat scraping

---

## 📖 Cara Menggunakan

```bash
python main.py
```

Kemudian masukkan:
- **Posisi pekerjaan** (contoh: `Software Engineer`, `Data Analyst`)
- **Lokasi** (contoh: `Jakarta`, `Bandung`, `Remote`)

Program akan:
1. 🌐 Membuka browser Chromium (atau headless jika tanpa GUI)
2. 🔍 Langsung membuka halaman pencarian JobStreet
3. 📊 Scraping data lowongan (maksimal 20)
4. 💾 Menyimpan hasil ke file CSV

---

## 📁 Output

File CSV akan dibuat dengan nama:  
`lowongan_[posisi]_[lokasi].csv`

**Format CSV:**

| No | Posisi | Perusahaan | Lokasi | Link |
|----|--------|------------|--------|------|
| 1  | Software Engineer | PT Tech Indonesia | Jakarta | https://... |

---

## 🛠 Troubleshooting

### 🔴 Error: "Could not open requirements file"
Pastikan virtual environment sudah diaktifkan dan Anda berada di folder yang benar.

### 🔴 Error: "playwright not found"
Jalankan: `playwright install chromium`

### 🔴 Error: "No module named 'playwright'"
1. Pastikan venv aktif
2. Reinstall: `pip install -r requirements.txt`

### 🔴 Browser tidak muncul (Linux)
- Pastikan display tersedia
- Atau gunakan mode headless (otomatis jika tidak ada DISPLAY)
- Install dependencies: `playwright install-deps chromium`

### 🔴 Permission denied (Linux)
```bash
chmod +x main.py
```

### 🔴 Tidak ada data yang ditemukan
- Periksa koneksi internet
- Coba kata kunci pencarian yang lebih umum
- JobStreet mungkin membatasi akses otomatis

---

## ⚠️ Catatan Penting

- Program ini hanya untuk scraping data **publik**
- JobStreet mungkin membatasi akses jika terlalu banyak request
- Gunakan dengan bijak dan **jangan spam**
- Hasil scraping untuk keperluan pribadi/edukasi

---

## 📄 Lisensi

**© Fahmi Alfatah**  
Dibuat untuk mempermudah pencarian lowongan kerja di Indonesia.  
Gunakan dengan tanggung jawab dan tetap hormati kebijakan JobStreet.

---

## 🙏 Terima Kasih

Terima kasih telah menggunakan JobStreet Job Scraper!  
Semoga membantu menemukan pekerjaan impian. 🎯

---

<div align="center">

**Happy Job Hunting!** 🚀

</div>
