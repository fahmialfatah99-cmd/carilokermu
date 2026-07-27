import asyncio
import csv
import logging
import os
import sys
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, BrowserContext
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# --- KONFIGURASI ---
# Set MAX_PAGES = 0 untuk scraping tanpa batas (sampai habis)
# Set MAX_PAGES = angka tertentu (misal 5) untuk membatasi jumlah halaman
KEYWORD = "Administrasi"
LOCATION_FILTER = "Jakarta Selatan"
BASE_URL = "https://id.jobstreet.com/id/jobs?keyword={}&location={}".format(KEYWORD.replace(' ', '%20'), LOCATION_FILTER.replace(' ', '%20'))
MAX_PAGES = 0  # 0 = Unlimited
OUTPUT_FILE = f"loker_{KEYWORD.lower().replace(' ', '_')}.csv"
HEADLESS = True  # True = tidak menampilkan browser, False = menampilkan browser
DEBUG = True  # True = tampilkan detail debugging selector

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("scraper_log.txt", encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class JobScraper:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        logger.info("Memulai browser...")
        playwright = await async_playwright().start()
        # Argumen tambahan untuk menghindari deteksi bot
        args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        self.browser = await playwright.chromium.launch(headless=self.headless, args=args)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = await self.context.new_page()
        
        # Inject script untuk menyembunyikan properti automation
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        logger.info("Browser siap.")

    async def close(self):
        if self.browser:
            await self.browser.close()
            logger.info("Browser ditutup.")

    async def scrape_page(self, url: str) -> List[Dict]:
        jobs = []
        try:
            logger.info(f"Mengakses: {url}")
            await self.page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Tunggu sebentar agar konten dimuat penuh
            await self.page.wait_for_timeout(2000)

            # Cek apakah ada pesan "tidak ada hasil" atau sejenisnya
            content = await self.page.content()
            if "lowongan tidak ditemukan" in content.lower() or "no jobs found" in content.lower():
                logger.info("Tidak ada lowongan lagi di halaman ini atau seterusnya.")
                return []

            soup = BeautifulSoup(content, 'lxml')

            # Selector khusus JobStreet Indonesia (updated 2024)
            # Mencari job card dengan selector yang lebih spesifik
            job_cards = soup.select('article[data-automation-id="jobCard"], div[data-automation-id="jobCard"]')
            
            if not job_cards:
                # Fallback: coba ambil parent dari jobCardTitle
                title_elems = soup.select('[data-automation="jobCardTitle"]')
                if title_elems:
                    # Ambil parent terdekat yang merupakan container
                    job_cards = []
                    for elem in title_elems:
                        parent = elem.find_parent(['article', 'div', 'li'])
                        if parent:
                            job_cards.append(parent)
                else:
                    job_cards = []
                    
                if not job_cards:
                    job_cards = soup.select('div[class*="JobCard"], article[class*="JobCard"], li[class*="job"]')
                    
                if DEBUG and title_elems:
                    logger.warning(f"Selector utama tidak menemukan hasil, mencoba fallback. Ditemukan {len(job_cards)} elemen potensial.")

            if DEBUG:
                logger.info(f"Total job cards ditemukan: {len(job_cards)}")

            for card in job_cards:
                try:
                    # Selector spesifik JobStreet untuk setiap field (prioritas data-automation)
                    title_elem = card.select_one('[data-automation="jobCardTitle"], a[data-automation="jobCardTitle"], h1, h2, h3, a[class*="title"]')
                    company_elem = card.select_one('[data-automation="jobCardCompany"], span[data-automation="jobCardCompany"], div[class*="company"], span[class*="company"]')
                    location_elem = card.select_one('[data-automation="jobCardLocation"], span[data-automation="jobCardLocation"], div[class*="location"], span[class*="place"]')
                    salary_elem = card.select_one('[data-automation="jobCardSalary"], span[data-automation="jobCardSalary"], div[class*="salary"], span[class*="remuneration"]')
                    link_elem = card.select_one('a[data-automation="jobCardTitle"], a[href]')
                    
                    if DEBUG:
                        logger.debug(f"  - Title elem: {title_elem is not None}, Company: {company_elem is not None}, Salary: {salary_elem is not None}")
                    
                    # Skip jika tidak ada title atau link
                    if not title_elem and not link_elem:
                        continue

                    title = title_elem.get_text(strip=True) if title_elem else "Judul tidak tersedia"
                    company = company_elem.get_text(strip=True) if company_elem else "Perusahaan tidak disebutkan"
                    location = location_elem.get_text(strip=True) if location_elem else LOCATION_FILTER
                    salary = salary_elem.get_text(strip=True) if salary_elem else "Informasi tidak tersedia"
                    
                    link = ""
                    if link_elem and link_elem.get('href'):
                        href = link_elem['href']
                        link = urljoin(url, href) if not href.startswith('http') else href
                    
                    # Filter sederhana berdasarkan keyword jika diperlukan
                    if KEYWORD.lower() not in title.lower() and KEYWORD.lower() not in company.lower():
                        # Opsional: Skip jika tidak sesuai keyword (hati-hati agar tidak terlalu ketat)
                        pass 

                    if title and link:
                        jobs.append({
                            "Judul": title,
                            "Perusahaan": company,
                            "Lokasi": location,
                            "Gaji": salary,
                            "Link": link,
                            "Sumber": urlparse(url).netloc
                        })
                        if DEBUG:
                            logger.debug(f"    ✓ Added: {title[:50]} | {company[:30]} | {salary}")
                except Exception as e:
                    if DEBUG:
                        logger.debug(f"  ⚠ Gagal memproses satu kartu: {e}")
                    continue

            logger.info(f"Ditemukan {len(jobs)} lowongan di halaman ini.")
            
        except Exception as e:
            logger.error(f"Gagal mengambil halaman {url}: {e}")
        
        return jobs

    async def get_next_page_url(self, current_url: str) -> Optional[str]:
        """Mencoba menemukan tombol 'Next' atau link halaman berikutnya"""
        try:
            # Strategi 1: Cari tombol Next via Playwright (lebih akurat untuk JS site)
            try:
                next_btn = await self.page.wait_for_selector('a[rel="next"], button:has-text("Next"), a:has-text("Berikutnya"), .pagination-next a', timeout=5000)
                if next_btn:
                    href = await next_btn.get_attribute('href')
                    if href:
                        return urljoin(current_url, href)
            except:
                pass

            # Strategi 2: Parse HTML manual jika JS gagal
            content = await self.page.content()
            soup = BeautifulSoup(content, 'lxml')
            next_link = soup.select_one('a[rel="next"]')
            if not next_link:
                # Cari teks "Next" atau "Berikutnya" di anchor
                for a in soup.select('a'):
                    text = a.get_text(strip=True).lower()
                    if 'next' in text or 'berikutnya' in text or '>' in text:
                        next_link = a
                        break
            
            if next_link and next_link.get('href'):
                return urljoin(current_url, next_link['href'])
                
        except Exception as e:
            logger.debug(f"Tidak menemukan halaman berikutnya: {e}")
        
        return None

async def run_scraper():
    scraper = JobScraper(headless=HEADLESS)
    await scraper.start()
    
    all_jobs = []
    current_url = BASE_URL
    page_count = 0
    
    try:
        while True:
            page_count += 1
            logger.info(f"--- Memproses Halaman {page_count} ---")
            
            jobs = await scraper.scrape_page(current_url)
            if not jobs:
                logger.info("Tidak ada data baru atau akhir dari pagination.")
                break
                
            all_jobs.extend(jobs)
            logger.info(f"Total sementara: {len(all_jobs)} lowongan")

            # Cek batas halaman
            if MAX_PAGES > 0 and page_count >= MAX_PAGES:
                logger.info(f"Batas halaman ({MAX_PAGES}) tercapai.")
                break

            # Cari URL halaman berikutnya
            next_url = await scraper.get_next_page_url(current_url)
            if not next_url or next_url == current_url:
                logger.info("Tidak ada halaman berikutnya.")
                break
            
            current_url = next_url
            
            # Delay anti-ban
            await asyncio.sleep(2)

    except KeyboardInterrupt:
        logger.warning("Proses dihentikan oleh pengguna.")
    finally:
        await scraper.close()
        save_to_csv(all_jobs, OUTPUT_FILE)

def save_to_csv(jobs: List[Dict], filename: str):
    if not jobs:
        logger.warning("Tidak ada data untuk disimpan.")
        return

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Judul", "Perusahaan", "Lokasi", "Gaji", "Link", "Sumber"])
            writer.writeheader()
            writer.writerows(jobs)
        logger.success(f"✅ Berhasil menyimpan {len(jobs)} data ke '{filename}'")
    except Exception as e:
        logger.error(f"Gagal menyimpan CSV: {e}")

# Menambahkan method 'success' ke logger jika belum ada
if not hasattr(logging, 'success'):
    logging.success = lambda msg, *args, **kwargs: logging.log(25, msg, *args, **kwargs)

if __name__ == "__main__":
    print(f"🚀 Memulai Scraper Lowongan Kerja")
    print(f"   Keyword: {KEYWORD}")
    print(f"   Lokasi: {LOCATION_FILTER}")
    print(f"   Target URL: {BASE_URL}")
    print(f"   Batas Halaman: {'Tanpa Batas' if MAX_PAGES == 0 else MAX_PAGES}")
    print("-" * 50)
    
    # Untuk Windows yang butuh policy loop fix
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(run_scraper())
