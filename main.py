import asyncio
import csv
import logging
import os
import sys
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, BrowserContext
from urllib.parse import urljoin, urlparse, parse_qs, urlencode

# --- KONFIGURASI ---
KEYWORD = "staff"
LOCATION_FILTER = "jakarta"
MAX_PAGES = 50  # Jumlah halaman maksimal untuk discrape
OUTPUT_FILE = f"loker_{KEYWORD.lower().replace(' ', '_')}.csv"
HEADLESS = False  # False = menampilkan browser agar bisa lihat proses
DEBUG = True  # True = tampilkan detail debugging

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

# Tambahkan level SUCCESS
if not hasattr(logging, 'success'):
    logging.success = lambda msg, *args, **kwargs: logging.log(25, msg, *args, **kwargs)
    logging.addLevelName(25, 'SUCCESS')

class JobScraper:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        logger.info("🌐 Memulai browser...")
        playwright = await async_playwright().start()
        
        args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process"
        ]
        
        self.browser = await playwright.chromium.launch(headless=self.headless, args=args)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        self.page = await self.context.new_page()
        
        # Inject script untuk menyembunyikan automation
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        """)
        logger.info("✅ Browser siap.")

    async def close(self):
        if self.browser:
            await self.browser.close()
            logger.info("🔒 Browser ditutup.")

    async def scrape_page(self, page_num: int) -> List[Dict]:
        jobs = []
        
        try:
            # Bangun URL dengan parameter page
            base_url = "https://id.jobstreet.com/id/jobs/in-" + LOCATION_FILTER.lower().replace(' ', '-') + "?k=" + KEYWORD.replace(' ', '%20')
            if page_num > 1:
                base_url += f"&page={page_num}"
            
            logger.info(f"📄 Halaman {page_num}: {base_url}")
            await self.page.goto(base_url, wait_until="networkidle", timeout=90000)
            
            # Tunggu initial load
            await self.page.wait_for_timeout(5000)
            
            # Scroll berkali-kali untuk memuat semua lazy-loaded content
            for i in range(5):
                await self.page.evaluate(f"window.scrollTo(0, {document.body.scrollHeight * (i+1) / 6})")
                await self.page.wait_for_timeout(1500)
            
            # Scroll ke paling bawah
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await self.page.wait_for_timeout(3000)
            
            # Scroll ke atas lagi
            await self.page.evaluate("window.scrollTo(0, 0)")
            await self.page.wait_for_timeout(2000)

            # Cek apakah ada hasil
            no_results = await self.page.query_selector('[data-automation="noJobsFound"], text="tidak ada lowongan", text="no jobs found"')
            if no_results:
                logger.info("⚠️ Tidak ada lowongan ditemukan di halaman ini.")
                return []

            # Tunggu job cards muncul
            try:
                await self.page.wait_for_selector('[data-automation-id="jobCard"]', timeout=10000)
            except:
                logger.warning("⚠️ Timeout menunggu job cards, mencoba scrape apa adanya...")

            # Ambil semua job cards menggunakan Playwright (lebih reliable daripada BeautifulSoup)
            job_cards = await self.page.query_selector_all('[data-automation-id="jobCard"]')
            
            if DEBUG:
                logger.info(f"🎴 Total job cards ditemukan: {len(job_cards)}")
            
            if not job_cards:
                # Fallback: coba selector alternatif
                job_cards = await self.page.query_selector_all('article[data-automation-id="jobCard"]')
                if DEBUG and job_cards:
                    logger.info(f"🎴 Fallback berhasil, ditemukan: {len(job_cards)}")
            
            for idx, card in enumerate(job_cards):
                try:
                    # Extract title
                    title_elem = await card.query_selector('[data-automation="jobCardTitle"]')
                    title = await title_elem.inner_text() if title_elem else "Judul tidak tersedia"
                    
                    # Extract company
                    company_elem = await card.query_selector('[data-automation="jobCardCompany"]')
                    company = await company_elem.inner_text() if company_elem else "Perusahaan tidak disebutkan"
                    
                    # Extract location
                    location_elem = await card.query_selector('[data-automation="jobCardLocation"]')
                    location = await location_elem.inner_text() if location_elem else LOCATION_FILTER
                    
                    # Extract salary
                    salary_elem = await card.query_selector('[data-automation="jobCardSalary"]')
                    salary = await salary_elem.inner_text() if salary_elem else "Informasi tidak tersedia"
                    
                    # Extract link
                    link_elem = await card.query_selector('a[data-automation="jobCardTitle"]')
                    link = ""
                    if link_elem:
                        href = await link_elem.get_attribute('href')
                        if href:
                            link = urljoin(base_url, href) if not href.startswith('http') else href
                    
                    # Skip jika tidak ada judul valid
                    if not title or title == "Judul tidak tersedia":
                        continue
                    
                    # Bersihkan text
                    title = title.strip()
                    company = company.strip() if company else "Perusahaan tidak disebutkan"
                    location = location.strip() if location else LOCATION_FILTER
                    salary = salary.strip() if salary else "Informasi tidak tersedia"
                    
                    if DEBUG:
                        logger.debug(f"  [{idx+1}] ✓ {title[:60]} | {company[:40]} | {salary}")
                    
                    jobs.append({
                        "Judul": title,
                        "Perusahaan": company,
                        "Lokasi": location,
                        "Gaji": salary,
                        "Link": link,
                        "Sumber": "jobstreet.com"
                    })
                    
                except Exception as e:
                    if DEBUG:
                        logger.debug(f"  ⚠ Error processing card {idx}: {e}")
                    continue
            
            logger.info(f"✅ Ditemukan {len(jobs)} lowongan di halaman {page_num}")
            
        except Exception as e:
            logger.error(f"❌ Gagal scrape halaman {page_num}: {e}")
        
        return jobs

    async def check_has_next_page(self, page_num: int) -> bool:
        """Cek apakah masih ada halaman berikutnya"""
        try:
            # Coba klik next atau cek keberadaan next button
            next_btn = await self.page.query_selector('a[rel="next"], button:has-text("Next"), a:has-text("Berikutnya"), .pagination-next a')
            if next_btn:
                return True
            
            # Cek apakah ada tombol page number setelah current page
            current_page_btn = await self.page.query_selector(f'button:has-text("{page_num}"), a:has-text("{page_num}")')
            if current_page_btn:
                # Cek apakah ada page number berikutnya
                next_page_btn = await self.page.query_selector(f'button:has-text("{page_num + 1}"), a:has-text("{page_num + 1}")')
                if next_page_btn:
                    return True
            
            # Coba akses halaman berikutnya langsung untuk test
            test_url = "https://id.jobstreet.com/id/jobs/in-" + LOCATION_FILTER.lower().replace(' ', '-') + "?k=" + KEYWORD.replace(' ', '%20') + f"&page={page_num + 1}"
            await self.page.goto(test_url, wait_until="networkidle", timeout=30000)
            await self.page.wait_for_timeout(3000)
            
            # Cek apakah ada job cards di halaman berikutnya
            test_cards = await self.page.query_selector_all('[data-automation-id="jobCard"]')
            if len(test_cards) > 0:
                return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error checking next page: {e}")
            return False


async def run_scraper():
    scraper = JobScraper(headless=HEADLESS)
    await scraper.start()
    
    all_jobs = []
    page_count = 0
    
    try:
        while True:
            page_count += 1
            logger.info(f"\n{'='*60}")
            logger.info(f"🔄 Memproses Halaman {page_count} dari maksimal {MAX_PAGES}")
            logger.info(f"{'='*60}")
            
            # Scrape halaman saat ini
            jobs = await scraper.scrape_page(page_count)
            
            if not jobs:
                logger.info("🏁 Tidak ada data baru atau akhir dari pagination.")
                break
            
            all_jobs.extend(jobs)
            logger.info(f"📊 Total sementara: {len(all_jobs)} lowongan")
            
            # Cek batas halaman
            if page_count >= MAX_PAGES:
                logger.info(f"🎯 Batas halaman ({MAX_PAGES}) tercapai.")
                break
            
            # Cek apakah masih ada halaman berikutnya
            has_next = await scraper.check_has_next_page(page_count)
            if not has_next:
                logger.info("🔚 Tidak ada halaman berikutnya.")
                break
            
            # Delay anti-ban
            await asyncio.sleep(2)
            
    except KeyboardInterrupt:
        logger.warning("⛔ Proses dihentikan oleh pengguna.")
    finally:
        await scraper.close()
        save_to_csv(all_jobs, OUTPUT_FILE)

def save_to_csv(jobs: List[Dict], filename: str):
    if not jobs:
        logger.warning("⚠️ Tidak ada data untuk disimpan.")
        print("\n❌ Tidak ada data yang berhasil discrape!")
        print("Kemungkinan penyebab:")
        print("  1. JobStreet mendeteksi sebagai bot dan menampilkan CAPTCHA")
        print("  2. Keyword atau lokasi tidak menghasilkan hasil")
        print("  3. Struktur HTML JobStreet berubah")
        print("\n💡 Solusi:")
        print("  - Set HEADLESS = False untuk melihat apa yang terjadi")
        print("  - Coba keyword atau lokasi yang berbeda")
        print("  - Tunggu beberapa saat sebelum mencoba lagi")
        return

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Judul", "Perusahaan", "Lokasi", "Gaji", "Link", "Sumber"])
            writer.writeheader()
            writer.writerows(jobs)
        logger.success(f"\n✅ BERHASIL! Menyimpan {len(jobs)} data ke '{filename}'")
        print(f"\n📈 Ringkasan:")
        print(f"   Total data: {len(jobs)} lowongan")
        print(f"   File: {filename}")
        
        # Tampilkan beberapa sample
        print(f"\n📋 Sample data (5 pertama):")
        for i, job in enumerate(jobs[:5], 1):
            print(f"   {i}. {job['Judul'][:50]} - {job['Perusahaan'][:30]}")
        
    except Exception as e:
        logger.error(f"❌ Gagal menyimpan CSV: {e}")

if __name__ == "__main__":
    print("="*60)
    print("🚀 JOBSTREET SCRAPER - Versi Improved")
    print("="*60)
    print(f"   📝 Keyword: {KEYWORD}")
    print(f"   📍 Lokasi: {LOCATION_FILTER}")
    print(f"   📄 Max Halaman: {MAX_PAGES}")
    print(f"   👁️ Headless: {HEADLESS}")
    print(f"   🐛 Debug: {DEBUG}")
    print("="*60)
    
    # Fix untuk Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(run_scraper())
