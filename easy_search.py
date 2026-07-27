#!/usr/bin/env python3
"""
Script Mudah Pencari Lowongan Kerja
Cara Pakai:
1. Jalankan: python3 easy_search.py
2. Ikuti pertanyaan yang muncul
3. Hasil otomatis tersimpan di file CSV
"""

import csv
import logging
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("❌ Error: Playwright belum terinstall!")
    print("   Jalankan: pip install playwright")
    print("   Lalu: playwright install chromium")
    exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def tanyakan_input():
    """Meminta input dari user dengan cara mudah"""
    print("\n" + "="*50)
    print("🔍 PENCARI LOWONGAN KERJA MUDAH")
    print("="*50)
    
    # Pertanyaan 1: Posisi
    posisi = input("\n1. Mau cari posisi apa? (contoh: Administrasi, Staff, Driver): ")
    if not posisi.strip():
        posisi = "Umum"
    
    # Pertanyaan 2: Lokasi
    lokasi = input("2. Di kota/daerah mana? (contoh: Jakarta, Surabaya, Bandung): ")
    if not lokasi.strip():
        lokasi = "Indonesia"
    
    # Pertanyaan 3: Jumlah halaman
    try:
        halaman = input("3. Mau ambil berapa halaman hasil? (default 3, max 10): ")
        if not halaman.strip():
            halaman = 3
        else:
            halaman = int(halaman)
            if halaman > 10:
                halaman = 10
                print("   → Dibatasi maksimal 10 halaman")
    except ValueError:
        halaman = 3
        print("   → Input tidak valid, menggunakan default 3 halaman")
    
    # Pertanyaan 4: Mode browser
    mode = input("4. Tampilkan browser saat mencari? (y/n, default n): ").lower()
    headless = mode != 'y'
    
    print("\n" + "="*50)
    print(f"📋 Ringkasan Pencarian:")
    print(f"   • Posisi: {posisi}")
    print(f"   • Lokasi: {lokasi}")
    print(f"   • Halaman: {halaman}")
    print(f"   • Mode: {'Tampil' if not headless else 'Silent'}")
    print("="*50)
    
    konfirmasi = input("\nLanjutkan pencarian? (y/n): ").lower()
    if konfirmasi != 'y':
        return None
    
    return {
        'keyword': posisi,
        'location': lokasi,
        'max_pages': halaman,
        'headless': headless
    }

def buat_url_pencarian(keyword: str, location: str) -> str:
    """Membuat URL pencarian JobStreet berdasarkan keyword dan lokasi"""
    # Format URL JobStreet Indonesia
    location_slug = location.lower().replace(' ', '-')
    base_url = "https://id.jobstreet.com/id/jobs"
    
    # Coba format URL dengan lokasi
    if location and location.lower() != 'indonesia':
        url = f"{base_url}/in-{location_slug}"
    else:
        url = base_url
    
    return url

def scrape_loker(url: str, keyword: str, max_pages: int = 3, headless: bool = True) -> List[Dict]:
    """Scrape lowongan kerja dari website"""
    all_jobs = []
    
    logger.info(f"🚀 Memulai pencarian: '{keyword}' di {url}")
    logger.info(f"📄 Maksimum {max_pages} halaman")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        try:
            # Kunjungi halaman pertama
            page.goto(url, timeout=60000, wait_until='domcontentloaded')
            page.wait_for_timeout(3000)  # Tunggu loading
            
            # Cari input search jika ada
            try:
                search_input = page.locator('input[placeholder*="cari"], input[name*="search"], input[type="search"]').first
                if search_input.is_visible():
                    search_input.fill(keyword)
                    
                    # Klik tombol search
                    search_button = page.locator('button[type="submit"], button:has-text("Cari"), button:has-text("Search"), .search-button').first
                    if search_button.is_visible():
                        search_button.click()
                        page.wait_for_timeout(3000)
                        logger.info("✅ Keyword dimasukkan dan search diklik")
            except Exception as e:
                logger.warning(f"⚠️ Tidak bisa input keyword otomatis: {e}")
                logger.info("   Melanjutkan dengan URL saat ini...")
            
            # Loop melalui halaman
            for page_num in range(1, max_pages + 1):
                logger.info(f"📑 Scraping halaman {page_num}/{max_pages}")
                
                # Tunggu konten loaded
                page.wait_for_timeout(2000)
                
                # Ambil semua job listing
                # Coba berbagai selector umum
                selectors = [
                    'article', 
                    '.job-card', 
                    '[data-automation="jobCard"]',
                    '.job-listing',
                    'div[class*="job"]',
                    'section[class*="job"]'
                ]
                
                job_elements = []
                for selector in selectors:
                    elements = page.locator(selector).all()
                    if elements:
                        job_elements = elements
                        logger.info(f"   Found {len(elements)} jobs dengan selector: {selector}")
                        break
                
                if not job_elements:
                    # Fallback: ambil semua div yang mungkin job card
                    job_elements = page.locator('div').filter(has_text=keyword).all()[:20]
                
                # Ekstrak data dari setiap elemen
                for idx, element in enumerate(job_elements):
                    try:
                        # Judul pekerjaan
                        title_selectors = ['h1', 'h2', 'h3', 'a', '[data-automation="jobTitle"]', '.job-title']
                        title = ""
                        for ts in title_selectors:
                            try:
                                title_elem = element.locator(ts).first
                                if title_elem.is_visible():
                                    title = title_elem.inner_text().strip()
                                    if title:
                                        break
                            except:
                                continue
                        
                        if not title or len(title) < 3:
                            continue
                        
                        # Perusahaan
                        company_selectors = ['[data-automation="jobCompany"]', '.company-name', 'span[class*="company"]']
                        company = ""
                        for cs in company_selectors:
                            try:
                                company_elem = element.locator(cs).first
                                if company_elem.is_visible():
                                    company = company_elem.inner_text().strip()
                                    if company:
                                        break
                            except:
                                continue
                        
                        # Lokasi
                        location_selectors = ['[data-automation="jobLocation"]', '.job-location', 'span[class*="location"]']
                        location = ""
                        for ls in location_selectors:
                            try:
                                location_elem = element.locator(ls).first
                                if location_elem.is_visible():
                                    location = location_elem.inner_text().strip()
                                    if location:
                                        break
                            except:
                                continue
                        
                        # Link detail
                        link = ""
                        try:
                            link_elem = element.locator('a[href*="/job/"], a[href*="/jobs/"]').first
                            if link_elem.is_visible():
                                href = link_elem.get_attribute('href')
                                if href:
                                    link = urljoin(url, href)
                        except:
                            pass
                        
                        # Gaji (opsional)
                        salary = ""
                        try:
                            salary_elem = element.locator('[data-automation="jobSalary"], .salary, span[class*="salary"]').first
                            if salary_elem.is_visible():
                                salary = salary_elem.inner_text().strip()
                        except:
                            pass
                        
                        job_data = {
                            'no': len(all_jobs) + 1,
                            'judul': title,
                            'perusahaan': company,
                            'lokasi': location if location else 'Tidak disebutkan',
                            'gaji': salary if salary else '-',
                            'link': link if link else url,
                            'tanggal_scrape': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        all_jobs.append(job_data)
                        
                    except Exception as e:
                        logger.debug(f"   Skip element {idx}: {e}")
                        continue
                
                logger.info(f"   ✅ Ditemukan {len(all_jobs)} total lowongan sampai sekarang")
                
                # Coba pindah ke halaman berikutnya
                if page_num < max_pages:
                    next_selectors = [
                        'a:has-text("Next")',
                        'a:has-text("Berikutnya")',
                        'button:has-text("Next")',
                        '.pagination-next',
                        '[aria-label="Next page"]'
                    ]
                    
                    next_button = None
                    for ns in next_selectors:
                        try:
                            next_button = page.locator(ns).first
                            if next_button.is_visible():
                                break
                            next_button = None
                        except:
                            continue
                    
                    if next_button:
                        next_button.click()
                        page.wait_for_timeout(3000)
                        logger.info("   → Pindah ke halaman berikutnya")
                    else:
                        logger.info("   ⚠️ Tidak ada halaman berikutnya atau sudah akhir")
                        break
                        
        except PlaywrightTimeout:
            logger.error("⏰ Timeout: Website terlalu lama merespon")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
        finally:
            browser.close()
    
    return all_jobs

def simpan_ke_csv(data: List[Dict], nama_file: str):
    """Simpan data ke file CSV"""
    if not data:
        logger.warning("⚠️ Tidak ada data untuk disimpan")
        return False
    
    try:
        with open(nama_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['no', 'judul', 'perusahaan', 'lokasi', 'gaji', 'link', 'tanggal_scrape']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"✅ Berhasil menyimpan {len(data)} lowongan ke file: {nama_file}")
        return True
    except Exception as e:
        logger.error(f"❌ Gagal menyimpan file: {e}")
        return False

def main():
    """Fungsi utama"""
    # Minta input dari user
    config = tanyakan_input()
    
    if not config:
        print("\n❌ Pencarian dibatalkan")
        return
    
    # Buat URL pencarian
    base_url = buat_url_pencarian(config['keyword'], config['location'])
    
    # Jalankan scraping
    results = scrape_loker(
        url=base_url,
        keyword=config['keyword'],
        max_pages=config['max_pages'],
        headless=config['headless']
    )
    
    # Simpan hasil
    if results:
        nama_file = f"loker_{config['keyword'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        simpan_ke_csv(results, nama_file)
        
        print("\n" + "="*50)
        print("🎉 SELESAI!")
        print(f"   Total lowongan ditemukan: {len(results)}")
        print(f"   File hasil: {nama_file}")
        print("   Buka file tersebut dengan Excel atau Google Sheets")
        print("="*50 + "\n")
    else:
        print("\n❌ Tidak menemukan lowongan kerja. Coba kata kunci lain.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Program dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error tak terduga: {e}")
        print("   Pastikan playwright sudah terinstall:")
        print("   pip install playwright")
        print("   playwright install chromium")
