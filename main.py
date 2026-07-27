"""
Scraper Lowongan Kerja (Job Scraper)

Script ini menggunakan Playwright untuk melakukan scraping lowongan kerja
dari berbagai situs job portal. Dilengkapi dengan stealth mode untuk menghindari deteksi bot.
"""

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_sync
from selectolax.parser import HTML
from typing import List, Dict, Optional
import logging

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def scrape_loker(url_target: str, keyword: str, max_pages: int = 3) -> List[Dict[str, str]]:
    """
    Scraping lowongan kerja dari situs target.
    
    Args:
        url_target: URL dasar situs lowongan kerja (contoh: https://example.com)
        keyword: Kata kunci pencarian (posisi/jabatan)
        max_pages: Jumlah maksimal halaman yang akan di-scrape
    
    Returns:
        List of dict berisi data lowongan dengan key: Posisi, Perusahaan, Link, Lokasi
    """
    logger.info(f"Mencari lowongan untuk: {keyword}...")
    data_loker = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            stealth_sync(page)  # Menyamar sebagai browser asli
            
            # Coba beberapa pola URL umum
            url_patterns = [
                f"{url_target}/jobs?q={keyword}",
                f"{url_target}/search?q={keyword}",
                f"{url_target}/job/search?keyword={keyword}",
                f"{url_target}?q={keyword}"
            ]
            
            success = False
            for pattern in url_patterns:
                try:
                    logger.info(f"Mencoba URL: {pattern}")
                    page.goto(pattern, timeout=60000, wait_until="domcontentloaded")
                    page.wait_for_load_state("networkidle", timeout=30000)
                    success = True
                    break
                except PlaywrightTimeoutError:
                    logger.warning(f"Timeout pada URL: {pattern}, mencoba pola berikutnya...")
                    continue
            
            if not success:
                logger.error("Gagal mengakses semua pola URL")
                browser.close()
                return data_loker
            
            # Scroll halaman untuk memuat konten dinamis
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)  # Tunggu 2 detik setelah scroll
            
            tree = HTML(page.content())
            
            # --- SESUAIKAN CSS SELECTOR DI BAWAH INI DENGAN WEBSITE TARGET ---
            # Contoh struktur umum (misal: Glints/Jobstreet/LinkedIn)
            selectors = {
                'card': ['.job-card', '.job-item', '[data-testid="job-card"]', '.job-listing', '.vacancy-card'],
                'title': ['h2', 'h3', '.job-title', 'a.title', '.position-title'],
                'company': ['.company-name', '.company', 'span.company', '.employer-name'],
                'link': ['a[href*="/job/"]', 'a.job-link', 'a[href*="/jobs/"]', '.job-link a'],
                'location': ['.location', '.job-location', 'span.location', '.city']
            }
            
            job_cards = []
            for card_selector in selectors['card']:
                job_cards = tree.css(card_selector)
                if job_cards:
                    break
            
            for card in job_cards:
                title_el = None
                company_el = None
                link_el = None
                location_el = None
                
                # Cari elemen dengan berbagai selector
                for title_selector in selectors['title']:
                    title_el = card.css_first(title_selector)
                    if title_el:
                        break
                
                for company_selector in selectors['company']:
                    company_el = card.css_first(company_selector)
                    if company_el:
                        break
                
                for link_selector in selectors['link']:
                    link_el = card.css_first(link_selector)
                    if link_el:
                        break
                
                for location_selector in selectors['location']:
                    location_el = card.css_first(location_selector)
                    if location_el:
                        break
                
                if title_el:
                    link = link_el.attributes.get('href') if link_el else "N/A"
                    # Pastikan link absolut
                    if link != "N/A" and not link.startswith('http'):
                        link = url_target + link if link.startswith('/') else f"{url_target}/{link}"
                    
                    data_loker.append({
                        "Posisi": title_el.text(strip=True),
                        "Perusahaan": company_el.text(strip=True) if company_el else "N/A",
                        "Lokasi": location_el.text(strip=True) if location_el else "N/A",
                        "Link": link
                    })
            # ------------------------------------------------------------------
            
            logger.info(f"Ditemukan {len(data_loker)} lowongan dari halaman pertama")
            
            # Scraping halaman berikutnya (jika ada)
            for page_num in range(2, max_pages + 1):
                try:
                    next_button = page.css_first('a.next, button.next, .pagination-next a, [rel="next"]')
                    if not next_button:
                        logger.info(f"Tidak ada halaman berikutnya setelah halaman {page_num - 1}")
                        break
                    
                    next_link = next_button.attributes.get('href')
                    if next_link:
                        page.goto(next_link, timeout=60000, wait_until="domcontentloaded")
                        page.wait_for_load_state("networkidle", timeout=30000)
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        page.wait_for_timeout(2000)
                        
                        tree = HTML(page.content())
                        # Proses kartu lowongan seperti sebelumnya
                        for card_selector in selectors['card']:
                            job_cards = tree.css(card_selector)
                            if job_cards:
                                break
                        
                        for card in job_cards:
                            # (Proses yang sama seperti di atas)
                            title_el = None
                            company_el = None
                            link_el = None
                            location_el = None
                            
                            for title_selector in selectors['title']:
                                title_el = card.css_first(title_selector)
                                if title_el:
                                    break
                            
                            for company_selector in selectors['company']:
                                company_el = card.css_first(company_selector)
                                if company_el:
                                    break
                            
                            for link_selector in selectors['link']:
                                link_el = card.css_first(link_selector)
                                if link_el:
                                    break
                            
                            for location_selector in selectors['location']:
                                location_el = card.css_first(location_selector)
                                if location_el:
                                    break
                            
                            if title_el:
                                link = link_el.attributes.get('href') if link_el else "N/A"
                                if link != "N/A" and not link.startswith('http'):
                                    link = url_target + link if link.startswith('/') else f"{url_target}/{link}"
                                
                                data_loker.append({
                                    "Posisi": title_el.text(strip=True),
                                    "Perusahaan": company_el.text(strip=True) if company_el else "N/A",
                                    "Lokasi": location_el.text(strip=True) if location_el else "N/A",
                                    "Link": link
                                })
                        
                        logger.info(f"Total sementara: {len(data_loker)} lowongan")
                    else:
                        break
                except Exception as e:
                    logger.warning(f"Error saat mengakses halaman {page_num}: {e}")
                    break
            
            browser.close()
            
    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")
    
    return data_loker


def save_to_csv(data: List[Dict[str, str]], filename: str = "hasil_loker.csv") -> bool:
    """
    Menyimpan data lowongan ke file CSV.
    
    Args:
        data: List of dict berisi data lowongan
        filename: Nama file output
    
    Returns:
        True jika berhasil, False jika gagal
    """
    if not data:
        logger.warning("Tidak ada data untuk disimpan")
        return False
    
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        logger.info(f"Berhasil menyimpan {len(data)} lowongan ke '{filename}'")
        return True
    except Exception as e:
        logger.error(f"Gagal menyimpan ke CSV: {e}")
        return False


def main():
    """Fungsi utama untuk menjalankan scraper."""
    # Ganti dengan URL situs loker target (contoh: situs internal, Glints, dll)
    TARGET_SITE = "https://contoh-situs-loker.com" 
    KEYWORD = "Data Analyst"
    MAX_PAGES = 3
    OUTPUT_FILE = "hasil_loker.csv"
    
    hasil = scrape_loker(TARGET_SITE, KEYWORD, max_pages=MAX_PAGES)
    
    if hasil:
        save_to_csv(hasil, OUTPUT_FILE)
        print(f"\n{'='*50}")
        print(f"Scraping selesai!")
        print(f"Total lowongan ditemukan: {len(hasil)}")
        print(f"Data tersimpan di: {OUTPUT_FILE}")
        print(f"{'='*50}")
    else:
        print("\nTidak ada hasil. Periksa:")
        print("  1. CSS Selector sesuai dengan website target")
        print("  2. URL target dapat diakses")
        print("  3. Struktur HTML website target")


if __name__ == "__main__":
    main()
