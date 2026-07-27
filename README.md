# LinkedIn Job Scraper (Tanpa Login)

Program sederhana untuk scraping lowongan kerja dari LinkedIn **tanpa perlu login**. Hasil scraping langsung disimpan ke file CSV.

## Fitur
- ✅ Tanpa login / tanpa akun
- ✅ Tanpa cookies
- ✅ Langsung scraping & simpan CSV
- ✅ Support Windows, macOS, Linux
- ✅ Menggunakan Playwright (Chromium)

## Persiapan

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

## Cara Menggunakan

```bash
python main.py
```

Kemudian masukkan:
- Posisi pekerjaan (contoh: `Software Engineer`)
- Lokasi (contoh: `Jakarta` atau `Remote`)

Program akan:
1. Membuka browser Chromium
2. Langsung membuka halaman pencarian LinkedIn
3. Scraping data lowongan
4. Menyimpan hasil ke file CSV

## Output

File CSV akan dibuat dengan nama: `lowongan_[posisi]_[lokasi].csv`

Format CSV:
| No | Posisi | Perusahaan | Lokasi | Link |
|----|--------|------------|--------|------|

## Troubleshooting

### Error: "Could not open requirements file"
Pastikan virtual environment sudah diaktifkan dan Anda berada di folder yang benar.

### Error: "playwright not found"
Jalankan: `playwright install chromium`

### Browser tidak muncul
Pastikan display tersedia (untuk Linux headless server, gunakan Xvfb).

## Catatan Penting

- Program ini hanya untuk scraping data publik
- LinkedIn mungkin membatasi akses jika terlalu banyak request
- Gunakan dengan bijak dan jangan spam

## Lisensi

Free to use untuk keperluan pribadi.
