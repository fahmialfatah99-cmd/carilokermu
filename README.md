# 🚀 CariLokerMu - Job Portal Scraper & Auto Apply

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

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verifikasi Instalasi
```bash
python3 main.py --help
```

---

## 🚀 Cara Penggunaan (Step-by-Step)

Berikut adalah panduan lengkap penggunaan dari awal hingga melamar otomatis:

### Langkah 1: Cari Lowongan Kerja
Jalankan scraper untuk menemukan lowongan sesuai keyword yang diinginkan.

```bash
# Format: python3 main.py "<keyword>" <jumlah_loker>
python3 main.py "admin" 30
```

**Output:**
- File CSV berisi daftar lowongan (contoh: `loker_admin_20260727_160440.csv`)
- File ini berisi judul, perusahaan, lokasi, gaji, dan **link lowongan**

---

### Langkah 2: Generate CV & Cover Letter (Opsional tapi Disarankan)
Gunakan script ini untuk memilih lowongan dari hasil scrape dan membuat CV yang disesuaikan.

```bash
python3 auto_cv_selector.py
```

**Proses:**
1. Script akan membaca file CSV hasil scraping terbaru
2. Anda diminta memilih nomor lowongan yang ingin dilamar
3. CV dan Cover Letter akan dibuat otomatis dalam format `.docx` dan `.pdf`
4. File tersimpan di folder `output_cv/`

**Tips:** Jika ingin melamar banyak lowongan sekaligus, Anda bisa skip langkah ini dan gunakan CV standar Anda.

---

### Langkah 3: Auto Apply ke Jobstreet
Setelah memiliki daftar lowongan dan CV, jalankan auto apply untuk melamar secara otomatis.

```bash
python3 auto_apply_jobstreet.py
```

**Cara Kerja:**
1. Script akan membuka browser Chrome secara otomatis
2. Anda harus **login manual sekali** ke akun Jobstreet Anda
3. Setelah login, script akan:
   - Membaca file CSV hasil scraping
   - Membuka satu per satu link lowongan
   - Mengisi form lamaran otomatis
   - Upload CV (jika ada di folder `output_cv/` atau CV default)
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
├── loker_admin_20260727_160440.csv    # Hasil scraping lowongan
├── output_cv/
│   ├── CV_Nama_Posisi.docx           # CV format Word
│   ├── CV_Nama_Posisi.pdf            # CV format PDF
│   └── Cover_Letter_Nama.docx        # Surat lamaran
├── logs/
│   └── auto_apply_20260727.log       # Log proses auto apply
└── config/
    └── user_profile.json             # Data diri pengguna
```

---

## ⚙️ Konfigurasi

### Mengatur Data Diri
Edit file `config/user_profile.json` untuk mengisi data diri yang akan digunakan pada CV dan form lamaran:

```json
{
  "nama_lengkap": "Nama Anda",
  "email": "email@anda.com",
  "telepon": "08123456789",
  "linkedin": "linkedin.com/in/anda",
  "pendidikan": "S1 Teknik Informatika",
  "pengalaman": "2 tahun sebagai Admin"
}
```

### Mengatur Lokasi Pencarian
Edit file `config/search_config.json` untuk set lokasi default:

```json
{
  "lokasi": "Jakarta",
  "gaji_min": 5000000,
  "tipe_pekerjaan": "Full-time"
}
```

---

## 🔧 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError: No module named 'docx'` | Jalankan: `pip install python-docx reportlab` |
| Browser tidak terbuka saat auto apply | Pastikan Chrome terinstall dan path-nya benar |
| Login Jobstreet gagal | Clear cookie browser atau gunakan mode incognito |
| CSV kosong/tidak ada data | Coba ubah keyword atau tambah jumlah loker |
| Auto apply stuck di captcha | Selesaikan captcha manual, script akan lanjut otomatis |

---

## 📝 Contoh Skenario Penggunaan

### Skenario 1: Lamar Cepat (5 Menit)
```bash
# 1. Cari 10 loker admin
python3 main.py "admin" 10

# 2. Langsung auto apply (pakai CV default)
python3 auto_apply_jobstreet.py
```

### Skenario 2: Lamar dengan CV Custom
```bash
# 1. Cari 20 loker
python3 main.py "staff" 20

# 2. Pilih 5 loker terbaik & generate CV
python3 auto_cv_selector.py

# 3. Auto apply dengan CV custom
python3 auto_apply_jobstreet.py
```

### Skenario 3: Monitoring & Analisis
```bash
# 1. Cari 50 loker untuk analisis pasar
python3 main.py "marketing" 50

# 2. Buka CSV di Excel untuk analisis
# 3. Filter manual loker yang sesuai
# 4. Auto apply hanya untuk yang terpilih
python3 auto_apply_jobstreet.py --filter "PT. Perusahaan Besar"
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
