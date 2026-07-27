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
import time

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
    
    def scrape_loker(self, url_target: str, keyword: str, location: str = "",
                     max_pages: int = 1, css_selectors: Optional[Dict] = None) -> List[Dict]:
        """
        Scraping lowongan kerja dari website target dengan dukungan multi-halaman.
        
        Args:
            url_target: URL base dari website lowongan kerja
            keyword: Kata kunci pencarian lowongan
            location: Lokasi/region pencarian
            max_pages: Jumlah maksimal halaman yang akan di-scraping
            css_selectors: Dictionary custom CSS selectors (optional)
        
        Returns:
            List of dictionaries containing job data
        """
        logger.info(f"Mencari lowongan untuk: {keyword} di lokasi: {location or 'Semua Lokasi'}")
        logger.info(f"Target scraping: {max_pages} halaman")
        self.data_loker = []
        
        # Default CSS selectors
        selectors = css_selectors or {
            'card': '.job-card, .job-item, [data-testid="job-card"], .job-search-result',
            'title': 'h2, h3, .job-title, a.title',
            'company': '.company-name, .company, span.company',
            'link': 'a[href*="/job/"], a.job-link',
            'location': '.location, .job-location, span.location',
            'salary': '.salary, .salary-range, span.salary',
            'description': '.job-description, .description, .job-detail',
            'posted_date': '.posted-date, .date-posted, .time-posted',
            'job_type': '.job-type, .employment-type, .full-time, .part-time'
        }
        
        try:
            with sync_playwright() as p:
                stealth = Stealth()
                browser = p.firefox.launch(headless=self.headless)
                page = browser.new_page()
                stealth.apply_stealth_sync(page)  # Menyamar sebagai browser asli
                
                # Set user agent dan viewport
                page.set_viewport_size({"width": 1920, "height": 1080})
                
                for page_num in range(1, max_pages + 1):
                    logger.info(f"Scraping halaman {page_num}/{max_pages}")
                    
                    # Bangun URL pencarian dengan parameter
                    search_url = f"{url_target}/jobs?q={keyword}"
                    if location:
                        search_url += f"&location={location}"
                    if page_num > 1:
                        search_url += f"&page={page_num}"
                    
                    logger.info(f"Navigasi ke: {search_url}")
                    
                    try:
                        page.goto(search_url, timeout=self.timeout)
                        page.wait_for_load_state("networkidle")
                    except PlaywrightTimeoutError:
                        logger.warning("Timeout saat menunggu halaman, melanjutkan dengan konten yang ada")
                    
                    # Tunggu sebentar untuk memastikan JS sudah selesai render
                    page.wait_for_timeout(3000)
                    
                    # Scroll halaman untuk memuat semua konten dinamis
                    self._scroll_page(page)
                    
                    tree = HTMLParser(page.content())
                    
                    # Parse job cards
                    page_count = 0
                    for card in tree.css(selectors['card']):
                        job_data = self._parse_job_card(card, selectors, url_target)
                        if job_data:
                            job_data['Halaman'] = page_num
                            self.data_loker.append(job_data)
                            page_count += 1
                    
                    logger.info(f"Ditemukan {page_count} lowongan di halaman {page_num}")
                    
                    # Delay antar halaman untuk menghindari blocking
                    if page_num < max_pages:
                        delay = 2 + (page_num * 0.5)  # Delay bertambah per halaman
                        logger.info(f"Menunggu {delay:.1f} detik sebelum halaman berikutnya...")
                        time.sleep(delay)
                
                browser.close()
                
        except Exception as e:
            logger.error(f"Error saat scraping: {str(e)}")
            raise
        
        logger.info(f"Total ditemukan {len(self.data_loker)} lowongan dari {max_pages} halaman")
        return self.data_loker
    
    def _scroll_page(self, page, scroll_times: int = 3):
        """
        Scroll halaman untuk memuat konten dinamis.
        
        Args:
            page: Playwright page object
            scroll_times: Jumlah kali scroll
        """
        try:
            for i in range(scroll_times):
                page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {(i+1)/scroll_times})")
                page.wait_for_timeout(500)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(500)
        except Exception as e:
            logger.warning(f"Gagal scroll halaman: {str(e)}")
    
    def _parse_job_card(self, card, selectors: Dict, base_url: str = "") -> Optional[Dict]:
        """
        Parse informasi dari satu job card dengan data lengkap.
        
        Args:
            card: Element job card dari HTML
            selectors: Dictionary CSS selectors
            base_url: Base URL untuk convert relative links
        
        Returns:
            Dictionary containing job information or None
        """
        title_el = card.css_first(selectors['title'])
        company_el = card.css_first(selectors['company'])
        link_el = card.css_first(selectors['link'])
        location_el = card.css_first(selectors.get('location', ''))
        salary_el = card.css_first(selectors.get('salary', ''))
        desc_el = card.css_first(selectors.get('description', ''))
        date_el = card.css_first(selectors.get('posted_date', ''))
        type_el = card.css_first(selectors.get('job_type', ''))
        
        if not title_el:
            return None
        
        # Ekstrak text dan clean
        title = title_el.text(strip=True) if title_el else "N/A"
        company = company_el.text(strip=True) if company_el else "N/A"
        location = location_el.text(strip=True) if location_el else "N/A"
        salary = salary_el.text(strip=True) if salary_el else "N/A"
        description = desc_el.text(strip=True) if desc_el else "N/A"
        posted_date = date_el.text(strip=True) if date_el else "N/A"
        job_type = type_el.text(strip=True) if type_el else "N/A"
        
        # Ekstrak link
        link = "N/A"
        if link_el:
            href = link_el.attributes.get('href', '')
            if href:
                # Convert relative URL to absolute if needed
                if href.startswith('/'):
                    link = base_url + href
                elif href.startswith('http'):
                    link = href
                else:
                    link = base_url + "/" + href
        
        return {
            "Posisi": title,
            "Perusahaan": company,
            "Lokasi": location,
            "Gaji": salary,
            "Tipe_Pekerjaan": job_type,
            "Tanggal_Posting": posted_date,
            "Deskripsi_Singkat": description[:200] if description != "N/A" else "N/A",
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
            # Urutkan kolom agar lebih rapi
            column_order = ['Posisi', 'Perusahaan', 'Lokasi', 'Gaji', 'Tipe_Pekerjaan', 
                           'Tanggal_Posting', 'Deskripsi_Singkat', 'Link', 'Tanggal_Scraping', 'Halaman']
            existing_columns = [col for col in column_order if col in df.columns]
            df = df[existing_columns]
            
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
            # Urutkan kolom agar lebih rapi
            column_order = ['Posisi', 'Perusahaan', 'Lokasi', 'Gaji', 'Tipe_Pekerjaan', 
                           'Tanggal_Posting', 'Deskripsi_Singkat', 'Link', 'Tanggal_Scraping', 'Halaman']
            existing_columns = [col for col in column_order if col in df.columns]
            df = df[existing_columns]
            
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
        locations = [job["Lokasi"] for job in self.data_loker if job["Lokasi"] != "N/A"]
        unique_companies = set(companies)
        unique_locations = set(locations)
        
        return {
            "total_lowongan": len(self.data_loker),
            "total_perusahaan_unik": len(unique_companies),
            "total_lokasi_unik": len(unique_locations),
            "perusahaan_terbanyak": max(set(companies), key=companies.count) if companies else "N/A",
            "lokasi_terbanyak": max(set(locations), key=locations.count) if locations else "N/A",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def display_results(self, limit: int = 10):
        """
        Tampilkan hasil scraping dalam format tabel yang rapi.
        
        Args:
            limit: Jumlah maksimal hasil yang ditampilkan
        """
        if not self.data_loker:
            print("\nTidak ada data untuk ditampilkan.")
            return
        
        print("\n" + "="*80)
        print("HASIL SCRAPING LOWONGAN KERJA")
        print("="*80)
        
        display_count = min(limit, len(self.data_loker))
        for i, job in enumerate(self.data_loker[:display_count], 1):
            print(f"\n{i}. {job.get('Posisi', 'N/A')}")
            print(f"   Perusahaan: {job.get('Perusahaan', 'N/A')}")
            print(f"   Lokasi: {job.get('Lokasi', 'N/A')}")
            print(f"   Gaji: {job.get('Gaji', 'N/A')}")
            print(f"   Tipe: {job.get('Tipe_Pekerjaan', 'N/A')}")
            print(f"   Posting: {job.get('Tanggal_Posting', 'N/A')}")
            print(f"   Link: {job.get('Link', 'N/A')}")
        
        if len(self.data_loker) > limit:
            print(f"\n... dan {len(self.data_loker) - limit} lowongan lainnya")
        
        print("="*80)


def interactive_menu():
    """Menu interaktif untuk input pengguna."""
    print("\n" + "="*60)
    print("🔍 APLIKASI PENCARI LOWONGAN KERJA")
    print("="*60)
    
    # Input lokasi
    print("\n📍 LOKASI PENCARIAN")
    print("Pilih lokasi atau ketik lokasi spesifik:")
    print("1. Jakarta")
    print("2. Bandung")
    print("3. Surabaya")
    print("4. Yogyakarta")
    print("5. Semarang")
    print("6. Medan")
    print("7. Bali")
    print("8. Semua Lokasi")
    print("9. Custom (ketik sendiri)")
    
    location_choice = input("\nPilihan lokasi (1-9): ").strip()
    location_map = {
        '1': 'Jakarta',
        '2': 'Bandung',
        '3': 'Surabaya',
        '4': 'Yogyakarta',
        '5': 'Semarang',
        '6': 'Medan',
        '7': 'Bali',
        '8': ''
    }
    
    if location_choice == '9':
        location = input("Ketik lokasi: ").strip()
    else:
        location = location_map.get(location_choice, '')
    
    # Input keyword/posisi
    print("\n💼 POSISI/JABATAN YANG DICARI")
    keyword = input("Masukkan kata kunci (contoh: Software Engineer, Data Analyst, Marketing): ").strip()
    
    while not keyword:
        print("⚠️  Kata kunci tidak boleh kosong!")
        keyword = input("Masukkan kata kunci: ").strip()
    
    # Input jumlah halaman
    print("\n📄 JUMLAH HALAMAN")
    while True:
        try:
            max_pages = int(input("Berapa halaman yang ingin di-scraping? (1-10): ").strip())
            if 1 <= max_pages <= 10:
                break
            else:
                print("⚠️  Masukkan angka antara 1-10")
        except ValueError:
            print("⚠️  Masukkan angka yang valid!")
    
    # Input website target
    print("\n🌐 WEBSITE TARGET")
    print("Pilih website atau ketik URL custom:")
    print("1. JobStreet Indonesia")
    print("2. LinkedIn Jobs")
    print("3. Kalibrr")
    print("4. Glints")
    print("5. Custom URL")
    
    website_choice = input("\nPilihan website (1-5): ").strip()
    website_map = {
        '1': 'https://www.jobstreet.co.id',
        '2': 'https://www.linkedin.com/jobs',
        '3': 'https://www.kalibrr.com',
        '4': 'https://glints.com'
    }
    
    if website_choice == '5':
        url_target = input("Masukkan URL website: ").strip()
        while not url_target.startswith('http'):
            print("⚠️  URL harus dimulai dengan http:// atau https://")
            url_target = input("Masukkan URL website: ").strip()
    else:
        url_target = website_map.get(website_choice, 'https://www.jobstreet.co.id')
    
    # Input format output
    print("\n💾 FORMAT OUTPUT")
    print("1. CSV")
    print("2. JSON")
    print("3. Excel")
    print("4. Semua Format")
    
    format_choice = input("\nPilihan format (1-4): ").strip()
    format_map = {'1': 'csv', '2': 'json', '3': 'excel', '4': 'all'}
    output_format = format_map.get(format_choice, 'csv')
    
    # Input mode headless
    print("\n🖥️  MODE BROWSER")
    print("1. Headless (tanpa tampilan GUI - lebih cepat)")
    print("2. Visible (dengan tampilan GUI - untuk debugging)")
    
    headless_choice = input("\nPilihan mode (1-2): ").strip()
    headless = headless_choice != '2'
    
    return {
        'keyword': keyword,
        'location': location,
        'max_pages': max_pages,
        'url_target': url_target,
        'output_format': output_format,
        'headless': headless
    }


def main():
    """Main function untuk menjalankan scraper."""
    parser = argparse.ArgumentParser(
        description='Scraper lowongan kerja dengan Playwright',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python cariloker.py --interactive
  python cariloker.py -k "Data Analyst" -l "Jakarta" --pages 5
  python cariloker.py -k "Software Engineer" -u https://jobstreet.co.id
  python cariloker.py -k "Marketing" --format json
        """
    )
    
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Mode interaktif dengan menu pilihan')
    parser.add_argument('-k', '--keyword', type=str,
                        help='Kata kunci pencarian lowongan')
    parser.add_argument('-l', '--location', type=str, default='',
                        help='Lokasi pencarian lowongan')
    parser.add_argument('-p', '--pages', type=int, default=1,
                        help='Jumlah halaman yang di-scraping (default: 1)')
    parser.add_argument('-u', '--url', type=str, 
                        default='https://www.jobstreet.co.id',
                        help='URL base website lowongan kerja (default: https://www.jobstreet.co.id)')
    parser.add_argument('-f', '--format', type=str, choices=['csv', 'json', 'excel', 'all'],
                        default='csv', help='Format output file (default: csv)')
    parser.add_argument('--headless', type=str, default='true',
                        choices=['true', 'false'], help='Mode headless browser (default: true)')
    parser.add_argument('--timeout', type=int, default=60000,
                        help='Timeout navigasi dalam milidetik (default: 60000)')
    parser.add_argument('--output', type=str, default=None,
                        help='Nama file output (optional)')
    
    args = parser.parse_args()
    
    # Mode interaktif
    if args.interactive or (not args.keyword):
        params = interactive_menu()
        keyword = params['keyword']
        location = params['location']
        max_pages = params['max_pages']
        url_target = params['url_target']
        output_format = params['output_format']
        headless = params['headless']
    else:
        keyword = args.keyword
        location = args.location
        max_pages = args.pages
        url_target = args.url
        output_format = args.format
        headless = args.headless.lower() == 'true'
    
    # Initialize scraper
    scraper = JobScraper(
        headless=headless,
        timeout=args.timeout
    )
    
    try:
        # Run scraping
        print("\n" + "="*60)
        print("🚀 MEMULAI SCRAPING...")
        print("="*60)
        print(f"Keyword: {keyword}")
        print(f"Lokasi: {location or 'Semua Lokasi'}")
        print(f"Target: {max_pages} halaman")
        print(f"Website: {url_target}")
        print("="*60 + "\n")
        
        hasil = scraper.scrape_loker(
            url_target=url_target,
            keyword=keyword,
            location=location,
            max_pages=max_pages
        )
        
        if hasil:
            # Tampilkan ringkasan
            summary = scraper.get_summary()
            print("\n" + "="*60)
            print("📊 RINGKASAN HASIL SCRAPING")
            print("="*60)
            print(f"Total lowongan ditemukan: {summary['total_lowongan']}")
            print(f"Total perusahaan unik: {summary['total_perusahaan_unik']}")
            print(f"Total lokasi unik: {summary.get('total_lokasi_unik', 'N/A')}")
            if summary['total_perusahaan_unik'] > 0:
                print(f"Perusahaan dengan lowongan terbanyak: {summary['perusahaan_terbanyak']}")
            if summary.get('lokasi_terbanyak'):
                print(f"Lokasi dengan lowongan terbanyak: {summary['lokasi_terbanyak']}")
            print("="*60)
            
            # Tampilkan beberapa hasil pertama
            scraper.display_results(limit=5)
            
            # Tentukan nama file output
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            keyword_safe = keyword.replace(' ', '_').replace('/', '_')[:30]
            
            # Simpan sesuai format yang dipilih
            formats_to_save = []
            if output_format == 'all':
                formats_to_save = ['csv', 'json', 'excel']
            else:
                formats_to_save = [output_format]
            
            saved_files = []
            for fmt in formats_to_save:
                if args.output:
                    filename = args.output
                else:
                    ext = {'csv': 'csv', 'json': 'json', 'excel': 'xlsx'}
                    filename = f"hasil_loker_{keyword_safe}_{timestamp}.{ext[fmt]}"
                
                success = False
                if fmt == 'csv':
                    success = scraper.save_to_csv(filename)
                elif fmt == 'json':
                    success = scraper.save_to_json(filename)
                elif fmt == 'excel':
                    success = scraper.save_to_excel(filename)
                
                if success:
                    saved_files.append(filename)
            
            print("\n" + "="*60)
            print("💾 FILE TERSIMPAT")
            print("="*60)
            for file in saved_files:
                print(f"✓ {file}")
            print("="*60)
        else:
            print("\n⚠️  Tidak ada hasil ditemukan.")
            print("Tips:")
            print("  - Periksa CSS selector di kode")
            print("  - Pastikan URL target benar")
            print("  - Coba kata kunci yang berbeda")
            print("  - Website mungkin memiliki proteksi anti-bot")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"\n❌ Terjadi error: {str(e)}")
        import traceback
        traceback.print_exc()
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
    return scraper.scrape_loker(url_target, keyword, css_selectors=css_selectors)


if __name__ == "__main__":
    exit(main())
