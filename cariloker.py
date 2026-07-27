import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import Stealth
from selectolax.parser import HTMLParser
import logging
import argparse
from typing import List, Dict, Optional
from datetime import datetime
import json
import os

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cariloker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class JobScraper:
    """Class untuk scraping lowongan kerja dari berbagai website."""
    
    def __init__(self, headless: bool = True, timeout: int = 60000):
        """
        Inisialisasi JobScraper.
        
        Args:
            headless: Jalankan browser dalam mode headless
            timeout: Timeout untuk navigasi halaman (ms)
        """
        self.headless = headless
        self.timeout = timeout
        self.data_loker: List[Dict] = []
    
    def scrape_loker(self, url_target: str, keyword: str, 
                     css_selectors: Optional[Dict] = None) -> List[Dict]:
        """
        Scraping lowongan kerja dari website target.
        
        Args:
            url_target: URL base dari website lowongan kerja
            keyword: Kata kunci pencarian lowongan
            css_selectors: Dictionary custom CSS selectors (optional)
        
        Returns:
            List of dictionaries containing job data
        """
        logger.info(f"Mencari lowongan untuk: {keyword}")
        self.data_loker = []
        
        # Default CSS selectors
        selectors = css_selectors or {
            'card': '.job-card, .job-item, [data-testid="job-card"]',
            'title': 'h2, h3, .job-title, a.title',
            'company': '.company-name, .company, span.company',
            'link': 'a[href*="/job/"], a.job-link',
            'location': '.location, .job-location, span.location',
            'salary': '.salary, .salary-range, span.salary'
        }
        
        try:
            with sync_playwright() as p:
                stealth = Stealth()
                browser = p.firefox.launch(headless=self.headless)
                page = browser.new_page()
                stealth.apply_stealth_sync(page)  # Menyamar sebagai browser asli
                
                # Set user agent dan viewport
                page.set_viewport_size({"width": 1920, "height": 1080})
                
                # Navigasi ke URL pencarian
                search_url = f"{url_target}/jobs?q={keyword}"
                logger.info(f"Navigasi ke: {search_url}")
                
                try:
                    page.goto(search_url, timeout=self.timeout)
                    page.wait_for_load_state("networkidle")
                except PlaywrightTimeoutError:
                    logger.warning("Timeout saat menunggu halaman, melanjutkan dengan konten yang ada")
                
                # Tunggu sebentar untuk memastikan JS sudah selesai render
                page.wait_for_timeout(2000)
                
                tree = HTMLParser(page.content())
                
                # Parse job cards
                for card in tree.css(selectors['card']):
                    job_data = self._parse_job_card(card, selectors)
                    if job_data:
                        self.data_loker.append(job_data)
                
                browser.close()
                
        except Exception as e:
            logger.error(f"Error saat scraping: {str(e)}")
            raise
        
        logger.info(f"Ditemukan {len(self.data_loker)} lowongan")
        return self.data_loker
    
    def _parse_job_card(self, card, selectors: Dict) -> Optional[Dict]:
        """
        Parse informasi dari satu job card.
        
        Args:
            card: Element job card dari HTML
            selectors: Dictionary CSS selectors
        
        Returns:
            Dictionary containing job information or None
        """
        title_el = card.css_first(selectors['title'])
        company_el = card.css_first(selectors['company'])
        link_el = card.css_first(selectors['link'])
        location_el = card.css_first(selectors.get('location', ''))
        salary_el = card.css_first(selectors.get('salary', ''))
        
        if not title_el:
            return None
        
        # Ekstrak text dan clean
        title = title_el.text(strip=True) if title_el else "N/A"
        company = company_el.text(strip=True) if company_el else "N/A"
        location = location_el.text(strip=True) if location_el else "N/A"
        salary = salary_el.text(strip=True) if salary_el else "N/A"
        
        # Ekstrak link
        link = "N/A"
        if link_el:
            href = link_el.attributes.get('href', '')
            if href:
                # Convert relative URL to absolute if needed
                if href.startswith('/'):
                    link = href
                elif href.startswith('http'):
                    link = href
                else:
                    link = f"/{href}"
        
        return {
            "Posisi": title,
            "Perusahaan": company,
            "Lokasi": location,
            "Gaji": salary,
            "Link": link,
            "Tanggal_Scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def save_to_csv(self, filename: str = "hasil_loker.csv") -> bool:
        """
        Simpan hasil scraping ke file CSV.
        
        Args:
            filename: Nama file output
        
        Returns:
            True jika berhasil, False jika tidak ada data
        """
        if not self.data_loker:
            logger.warning("Tidak ada data untuk disimpan")
            return False
        
        try:
            df = pd.DataFrame(self.data_loker)
            df.to_csv(filename, index=False, encoding="utf-8-sig")
            logger.info(f"Berhasil menyimpan {len(self.data_loker)} lowongan ke '{filename}'")
            return True
        except Exception as e:
            logger.error(f"Error saat menyimpan CSV: {str(e)}")
            return False
    
    def save_to_json(self, filename: str = "hasil_loker.json", indent: int = 2) -> bool:
        """
        Simpan hasil scraping ke file JSON.
        
        Args:
            filename: Nama file output
            indent: Jumlah spasi untuk indentasi JSON
        
        Returns:
            True jika berhasil, False jika tidak ada data
        """
        if not self.data_loker:
            logger.warning("Tidak ada data untuk disimpan")
            return False
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data_loker, f, ensure_ascii=False, indent=indent)
            logger.info(f"Berhasil menyimpan {len(self.data_loker)} lowongan ke '{filename}'")
            return True
        except Exception as e:
            logger.error(f"Error saat menyimpan JSON: {str(e)}")
            return False
    
    def save_to_excel(self, filename: str = "hasil_loker.xlsx") -> bool:
        """
        Simpan hasil scraping ke file Excel.
        
        Args:
            filename: Nama file output
        
        Returns:
            True jika berhasil, False jika tidak ada data
        """
        if not self.data_loker:
            logger.warning("Tidak ada data untuk disimpan")
            return False
        
        try:
            df = pd.DataFrame(self.data_loker)
            df.to_excel(filename, index=False, engine='openpyxl')
            logger.info(f"Berhasil menyimpan {len(self.data_loker)} lowongan ke '{filename}'")
            return True
        except Exception as e:
            logger.error(f"Error saat menyimpan Excel: {str(e)}")
            return False
    
    def get_summary(self) -> Dict:
        """
        Dapatkan ringkasan hasil scraping.
        
        Returns:
            Dictionary containing summary statistics
        """
        if not self.data_loker:
            return {"total": 0}
        
        companies = [job["Perusahaan"] for job in self.data_loker if job["Perusahaan"] != "N/A"]
        unique_companies = set(companies)
        
        return {
            "total_lowongan": len(self.data_loker),
            "total_perusahaan_unik": len(unique_companies),
            "perusahaan_terbanyak": max(set(companies), key=companies.count) if companies else "N/A",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


def main():
    """Main function untuk menjalankan scraper dari command line."""
    parser = argparse.ArgumentParser(
        description='Scraper lowongan kerja dengan Playwright',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python cariloker.py -k "Data Analyst"
  python cariloker.py -k "Software Engineer" -u https://jobstreet.co.id
  python cariloker.py -k "Marketing" --format json
  python cariloker.py -k "Designer" --headless false
        """
    )
    
    parser.add_argument('-k', '--keyword', type=str, required=True,
                        help='Kata kunci pencarian lowongan')
    parser.add_argument('-u', '--url', type=str, 
                        default='https://contoh-situs-loker.com',
                        help='URL base website lowongan kerja (default: https://contoh-situs-loker.com)')
    parser.add_argument('-f', '--format', type=str, choices=['csv', 'json', 'excel'],
                        default='csv', help='Format output file (default: csv)')
    parser.add_argument('--headless', type=str, default='true',
                        choices=['true', 'false'], help='Mode headless browser (default: true)')
    parser.add_argument('--timeout', type=int, default=60000,
                        help='Timeout navigasi dalam milidetik (default: 60000)')
    parser.add_argument('--output', type=str, default=None,
                        help='Nama file output (optional)')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = JobScraper(
        headless=args.headless.lower() == 'true',
        timeout=args.timeout
    )
    
    try:
        # Run scraping
        hasil = scraper.scrape_loker(args.url, args.keyword)
        
        if hasil:
            # Tentukan nama file output
            if args.output:
                filename = args.output
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                ext = {'csv': 'csv', 'json': 'json', 'excel': 'xlsx'}
                filename = f"hasil_loker_{args.keyword.replace(' ', '_')}_{timestamp}.{ext[args.format]}"
            
            # Simpan sesuai format yang dipilih
            if args.format == 'csv':
                scraper.save_to_csv(filename)
            elif args.format == 'json':
                scraper.save_to_json(filename)
            elif args.format == 'excel':
                scraper.save_to_excel(filename)
            
            # Tampilkan ringkasan
            summary = scraper.get_summary()
            print("\n" + "="*50)
            print("RINGKASAN HASIL SCRAPING")
            print("="*50)
            print(f"Total lowongan ditemukan: {summary['total_lowongan']}")
            print(f"Total perusahaan unik: {summary['total_perusahaan_unik']}")
            if summary['total_perusahaan_unik'] > 0:
                print(f"Perusahaan dengan lowongan terbanyak: {summary['perusahaan_terbanyak']}")
            print(f"File output: {filename}")
            print("="*50)
        else:
            print("\nTidak ada hasil ditemukan.")
            print("Tips:")
            print("  - Periksa CSS selector di kode")
            print("  - Pastikan URL target benar")
            print("  - Coba kata kunci yang berbeda")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"\nTerjadi error: {str(e)}")
        return 1
    
    return 0


# === BACKWARD COMPATIBILITY ===
# Fungsi lama tetap tersedia untuk kompatibilitas
def scrape_loker(url_target: str, keyword: str, 
                 css_selectors: Optional[Dict] = None) -> List[Dict]:
    """
    Fungsi legacy untuk backward compatibility.
    Gunakan class JobScraper untuk fitur lebih lengkap.
    """
    scraper = JobScraper()
    return scraper.scrape_loker(url_target, keyword, css_selectors)


if __name__ == "__main__":
    exit(main())
