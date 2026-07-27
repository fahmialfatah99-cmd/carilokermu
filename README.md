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
- ✅ **Target JobStreet** – Khusus jobstreet.co.id

---

## 🚀 Persiapan

### 1. Buat Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Browser Engine
```bash
playwright install chromium
```

---

## 📖 Cara Menggunakan

```bash
python main.py
```

Kemudian masukkan:
- **Posisi pekerjaan** (contoh: `Software Engineer`, `Data Analyst`)
- **Lokasi** (contoh: `Jakarta`, `Bandung`, `Remote`)

Program akan:
1. 🌐 Membuka browser Chromium
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

### Error: "Could not open requirements file"
Pastikan virtual environment sudah diaktifkan dan Anda berada di folder yang benar.

### Error: "playwright not found"
Jalankan: `playwright install chromium`

### Browser tidak muncul
Pastikan display tersedia (untuk Linux headless server, gunakan Xvfb).

### Tidak ada data yang ditemukan
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
