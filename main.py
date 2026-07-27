#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carilokermu - Pencari Kerja Otomatis Khusus Jobstreet
Prinsip: Cepat, Spesifik Jobstreet, Interaktif, Virtual Environment
"""

import os
import sys
import csv
import time
import random
import logging
from datetime import datetime
from urllib.parse import urljoin, quote_plus

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

try:
    from playwright.sync_api import sync_playwright
    from playwright_stealth import stealth_sync
except ImportError:
    logger.error("Playwright tidak terinstall. Jalankan: pip install playwright playwright-stealth")
    sys.exit(1)

# Konfigurasi Khusus Jobstreet
JOBSTREET_BASE_URL = "https://www.jobstreet.co.id"
JOBSTREET_SEARCH_URL = "https://www.jobstreet.co.id/id/pekerjaan"

# CSS Selectors Khusus Jobstreet (Update sesuai struktur terbaru)
SELECTORS = {
    'job_card': 'article[data-jk] div[data-automation="jobTitle"], a[data-automation="jobTitle"], div[data-automation="jobListing"]',
    'job_title': 'span[data-automation="jobTitle"], h1[data-automation="jobTitle"]',
    'company_name': 'span[data-automation="jobCompany"], a[data-automation="jobCompany"]',
    'location': 'span[data-automation="jobLocation"]',
    'salary': 'span[data-automation="jobSalary"]',
    'description': 'div[data-automation="jobDescription"], section[data-automation="jobDescription"]',
    'next_page': 'a[aria-label="Next Page"], button:contains("Next"), a.pagination-next',
    'error_msg': 'div[class*="error"], div[class*="no-result"]'
}

CITIES = [
    "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Semarang",
    "Medan", "Bali", "Makassar", "Palembang", "Tangerang",
    "Bekasi", "Depok", "Batam", "Malang", "Balikpapan"
]

def get_user_input():
    """Menu interaktif khusus Jobstreet"""
    print("\n" + "="*60)
    print("🔍 PENCARI LOWONGAN KERJA - KHUSUS JOBSTREET")
    print("="*60)
    
    # Pilihan Kota
    print("\n📍 Pilih Lokasi:")
    for i, city in enumerate(CITIES, 1):
        print(f"   {i}. {city}")
    print(f"   0. Semua Lokasi")
    
    while True:
        try:
            city_choice = input("\nMasukkan nomor lokasi (default: 0): ").strip()
            if city_choice == "" or city_choice == "0":
                location = ""
                break
            elif city_choice.isdigit() and 1 <= int(city_choice) <= len(CITIES):
                location = CITIES[int(city_choice)-1]
                break
            else:
                print("❌ Pilihan tidak valid. Masukkan angka 0-{}.".format(len(CITIES)))
        except KeyboardInterrupt:
            print("\n\nDibatalkan oleh pengguna.")
            sys.exit(0)

    # Keyword
    while True:
        keyword = input("\n💼 Kata kunci pekerjaan (contoh: Admin, Staff, IT): ").strip()
        if keyword:
            break
        print("❌ Kata kunci tidak boleh kosong.")

    # Jumlah Halaman
    while True:
        try:
            pages = input("\n📄 Jumlah halaman (default: 3, maks 10): ").strip()
            max_pages = int(pages) if pages else 3
            if 1 <= max_pages <= 10:
                break
            print("❌ Masukkan angka antara 1 sampai 10.")
        except ValueError:
            print("❌ Input harus angka.")
        except KeyboardInterrupt:
            print("\n\nDibatalkan.")
            sys.exit(0)

    return keyword, location, max_pages

def scrape_jobstreet(keyword, location="", max_pages=3):
    """Scraping khusus Jobstreet dengan stealth mode"""
    jobs = []
    
    # Bangun URL pencarian Jobstreet
    params = f"?keyword={quote_plus(keyword)}"
    if location:
        params += f"&location={quote_plus(location)}"
    
    target_url = f"{JOBSTREET_SEARCH_URL}{params}"
    
    logger.info(f"Mencari: '{keyword}' di {location if location else 'Seluruh Indonesia'}...")
    logger.info(f"URL: {target_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        
        # Aktifkan stealth mode
        try:
            stealth_sync(page)
        except Exception as e:
            logger.warning(f"Gagal mengaktifkan stealth_sync: {e}. Melanjutkan tanpa stealth penuh.")

        try:
            for page_num in range(1, max_pages + 1):
                if page_num > 1:
                    next_url = f"{target_url}&page={page_num}"
                    logger.info(f"Membuka halaman {page_num}: {next_url}")
                    page.goto(next_url, wait_until='networkidle', timeout=30000)
                else:
                    logger.info(f"Membuka halaman 1...")
                    page.goto(target_url, wait_until='networkidle', timeout=30000)

                time.sleep(random.uniform(2, 4))
                
                job_cards = page.query_selector_all(SELECTORS['job_card'])
                
                if not job_cards:
                    logger.warning(f"Tidak ditemukan lowongan di halaman {page_num}.")
                    if page.query_selector(SELECTORS['error_msg']):
                        logger.error("Website mendeteksi bot atau tidak ada hasil.")
                        break
                    continue

                logger.info(f"Ditemukan {len(job_cards)} lowongan di halaman {page_num}.")

                for idx, card in enumerate(job_cards):
                    try:
                        title_el = card.query_selector(SELECTORS['job_title'])
                        company_el = card.query_selector(SELECTORS['company_name'])
                        loc_el = card.query_selector(SELECTORS['location'])
                        salary_el = card.query_selector(SELECTORS['salary'])
                        
                        link_el = card.query_selector('a')
                        job_link = link_el.get_attribute('href') if link_el else ""
                        if job_link and not job_link.startswith('http'):
                            job_link = urljoin(JOBSTREET_BASE_URL, job_link)

                        job_data = {
                            'no': len(jobs) + 1,
                            'judul': title_el.inner_text().strip() if title_el else "Tidak ada judul",
                            'perusahaan': company_el.inner_text().strip() if company_el else "Rahasia / Tidak disebutkan",
                            'lokasi': loc_el.inner_text().strip() if loc_el else "-",
                            'gaji': salary_el.inner_text().strip() if salary_el else "-",
                            'link': job_link,
                            'tanggal': datetime.now().strftime('%Y-%m-%d')
                        }
                        
                        if not any(j['link'] == job_link for j in jobs):
                            jobs.append(job_data)
                            print(f"   [{len(jobs)}] {job_data['judul']} - {job_data['perusahaan']} ({job_data['lokasi']})")
                    
                    except Exception as e:
                        logger.debug(f"Gagal memproses satu kartu lowongan: {e}")
                        continue

                if page_num < max_pages:
                    next_btn = page.query_selector(SELECTORS['next_page'])
                    if not next_btn:
                        logger.info("Tidak ada halaman berikutnya.")
                        break
                    
        except Exception as e:
            logger.error(f"Terjadi kesalahan saat scraping: {e}")
        
        finally:
            browser.close()

    return jobs

def save_to_csv(jobs, keyword, location):
    """Simpan hasil ke CSV"""
    if not jobs:
        print("\n❌ Tidak ada data untuk disimpan.")
        return None

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    loc_suffix = location.replace(" ", "_").lower() if location else "all"
    filename = f"loker_{keyword.lower().replace(' ', '_')}_{loc_suffix}_{timestamp}.csv"
    
    os.makedirs('output', exist_ok=True)
    filepath = os.path.join('output', filename)

    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['no', 'judul', 'perusahaan', 'lokasi', 'gaji', 'link', 'tanggal']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

    print("\n" + "="*60)
    print(f"✅ SELESAI!")
    print(f"   Total lowongan ditemukan: {len(jobs)}")
    print(f"   File hasil: {filepath}")
    print(f"   Buka file tersebut dengan Excel atau gunakan script auto_cv_selector.py")
    print("="*60)
    
    return filepath

def interactive_selection(jobs, csv_path):
    """Menu interaktif untuk memilih lowongan yang akan dilamar"""
    if not jobs:
        return

    print("\n📋 DAFTAR LOWONGAN DITEMUKAN:")
    print("-" * 60)
    for job in jobs:
        print(f"{job['no']}. {job['judul']} | {job['perusahaan']} | {job['lokasi']}")
    
    print("\n💡 PILIHAN:")
    print("   - Ketik nomor lowongan (misal: 1 atau 1,3,5)")
    print("   - Ketik 'all' untuk memilih semua")
    print("   - Ketik 'q' untuk keluar")
    
    choice = input("\nPilih lowongan yang ingin dilamar: ").strip().lower()
    
    if choice == 'q':
        print("Keluar dari program.")
        return
    
    selected_jobs = []
    if choice == 'all':
        selected_jobs = jobs
        print(f"✅ Memilih semua {len(jobs)} lowongan.")
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(',')]
            selected_jobs = [j for j in jobs if j['no'] in indices]
            if not selected_jobs:
                print("❌ Nomor tidak valid.")
                return
            print(f"✅ Memilih {len(selected_jobs)} lowongan.")
        except ValueError:
            print("❌ Format input salah. Gunakan angka dipisah koma (contoh: 1,2,3).")
            return

    selection_file = csv_path.replace('.csv', '_selected.txt')
    with open(selection_file, 'w') as f:
        for job in selected_jobs:
            f.write(f"{job['link']}\n")
    
    print(f"\n💾 Pilihan disimpan di: {selection_file}")
    print("🚀 Langkah selanjutnya:")
    print(f"   python3 auto_cv_selector.py {selection_file}")

def main():
    try:
        keyword, location, max_pages = get_user_input()
        jobs = scrape_jobstreet(keyword, location, max_pages)
        
        if jobs:
            csv_path = save_to_csv(jobs, keyword, location)
            if csv_path:
                interactive_selection(jobs, csv_path)
        else:
            print("\n❌ Tidak ada lowongan ditemukan. Coba kata kunci lain atau lokasi berbeda.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Program dihentikan oleh pengguna.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Terjadi kesalahan fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
