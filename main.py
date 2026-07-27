import asyncio
import csv
import logging
import os
import sys
import random
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, BrowserContext
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from datetime import datetime

# --- KONFIGURASI ---
KEYWORD = "staff"
LOCATION_FILTER = "jakarta"
MAX_PAGES = 100  # Jumlah halaman maksimal untuk discrape
MAX_JOBS = 1000  # Maksimal total lowongan yang ingin diambil
OUTPUT_FILE = f"loker_{KEYWORD.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
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
        self.base_url = ""

    async def start(self):
        logger.info("🌐 Memulai browser...")
        playwright = await async_playwright().start()
        
        args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process",
            "--disable-gpu",
            "--window-size=1920,1080"
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

    def build_search_url(self, page_num: int = 1) -> str:
        """Membangun URL pencarian JobStreet dengan format yang benar"""
        location_slug = LOCATION_FILTER.lower().replace(' ', '-')
        keyword_encoded = KEYWORD.replace(' ', '%20')
        
        # Format URL JobStreet yang benar
        if page_num == 1:
            return f"https://id.jobstreet.com/id/jobs/in-{location_slug}?k={keyword_encoded}"
        else:
            return f"https://id.jobstreet.com/id/jobs/in-{location_slug}?k={keyword_encoded}&page={page_num}"

    async def wait_for_jobs_to_load(self, timeout: int = 15000):
        """Tunggu sampai job cards selesai loading dengan multiple strategies"""
        try:
            # Tunggu selector utama
            await self.page.wait_for_selector('[data-automation-id="jobCard"]', timeout=timeout)
            
            # Tunggu tambahan untuk lazy loading
            await self.page.wait_for_timeout(3000)
            
            # Scroll berkali-kali untuk memastikan semua konten ter-load
            for i in range(5):
                scroll_height = int(await self.page.evaluate("document.body.scrollHeight"))
                scroll_position = int(scroll_height * (i + 1) / 6)
                await self.page.evaluate(f"window.scrollTo(0, {scroll_position})")
                await self.page.wait_for_timeout(random.randint(800, 1500))
            
            # Scroll ke paling bawah
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await self.page.wait_for_timeout(random.randint(2000, 4000))
            
            # Scroll ke atas lagi
            await self.page.evaluate("window.scrollTo(0, 0)")
            await self.page.wait_for_timeout(random.randint(1500, 2500))
            
            return True
        except Exception as e:
            logger.warning(f"⚠️ Timeout menunggu jobs: {e}")
            return False

    async def scrape_page(self, page_num: int) -> List[Dict]:
        """Scrape satu halaman pencarian"""
        jobs = []
        
        try:
            # Bangun URL
            url = self.build_search_url(page_num)
            self.base_url = url
            
            logger.info(f"📄 Halaman {page_num}: {url}")
            
            # Navigate ke halaman
            await self.page.goto(url, wait_until="networkidle", timeout=90000)
            await self.page.wait_for_timeout(5000)  # Initial wait
            
            # Tunggu jobs load dengan scrolling
            loaded = await self.wait_for_jobs_to_load()
            if not loaded:
                logger.warning("⚠️ Gagal menunggu jobs load, mencoba scrape apa adanya...")
            
            # Cek apakah ada hasil
            no_results = await self.page.query_selector('[data-automation="noJobsFound"]')
            if no_results:
                text = await no_results.inner_text()
                if text and ('tidak ada' in text.lower() or 'no jobs' in text.lower()):
                    logger.info("⚠️ Tidak ada lowongan ditemukan.")
                    return []
            
            # Ambil semua job cards - gunakan multiple selectors untuk fallback
            selectors = [
                '[data-automation-id="jobCard"]',
                'article[data-automation-id="jobCard"]',
                'div[data-automation-id="jobCard"]',
                '[data-testid="job-card"]',
                '.job-card',
                'article.job-listing'
            ]
            
            job_cards = []
            for selector in selectors:
                cards = await self.page.query_selector_all(selector)
                if cards:
                    job_cards = cards
                    if DEBUG:
                        logger.info(f"✓ Menggunakan selector: {selector}")
                    break
            
            if DEBUG:
                logger.info(f"🎴 Total job cards ditemukan: {len(job_cards)}")
            
            if not job_cards:
                logger.warning("⚠️ Tidak ada job cards ditemukan sama sekali!")
                # Coba screenshot untuk debug
                if DEBUG:
                    await self.page.screenshot(path=f"debug_page{page_num}.png")
                    logger.info(f"💾 Screenshot debug disimpan: debug_page{page_num}.png")
                return []
            
            # Process setiap job card
            for idx, card in enumerate(job_cards):
                try:
                    job_data = await self.extract_job_data(card, idx)
                    if job_data and job_data.get("Judul"):
                        jobs.append(job_data)
                except Exception as e:
                    if DEBUG:
                        logger.debug(f"  ⚠ Error processing card {idx}: {e}")
                    continue
            
            logger.info(f"✅ Ditemukan {len(jobs)} lowongan valid di halaman {page_num}")
            
        except Exception as e:
            logger.error(f"❌ Gagal scrape halaman {page_num}: {e}")
            if DEBUG:
                import traceback
                logger.debug(traceback.format_exc())
        
        return jobs

    async def extract_job_data(self, card, idx: int) -> Optional[Dict]:
        """Extract data dari satu job card dengan multiple fallback selectors"""
        try:
            # === EXTRACT TITLE ===
            title_selectors = [
                '[data-automation="jobCardTitle"]',
                'a[data-automation="jobCardTitle"]',
                '[data-testid="job-title"]',
                '.job-title',
                'h1',
                'h2',
                'h3'
            ]
            title = ""
            for selector in title_selectors:
                elem = await card.query_selector(selector)
                if elem:
                    title = await elem.inner_text()
                    if title:
                        break
            
            title = title.strip() if title else ""
            
            # Skip jika title kosong atau tidak valid
            if not title or len(title) < 3:
                return None
            
            # === EXTRACT COMPANY ===
            company_selectors = [
                '[data-automation="jobCardCompany"]',
                '[data-testid="company-name"]',
                '.company-name',
                '[class*="company"]',
                'span[class*="Company"]',
                'div[class*="Company"]'
            ]
            company = ""
            for selector in company_selectors:
                elem = await card.query_selector(selector)
                if elem:
                    company = await elem.inner_text()
                    if company:
                        break
            
            company = company.strip() if company else "Perusahaan tidak disebutkan"
            
            # Jika company masih kosong, coba cari dari text content card
            if not company or company == "Perusahaan tidak disebutkan":
                try:
                    all_text = await card.inner_text()
                    lines = all_text.split('\n')
                    # Biasanya company ada di baris setelah title
                    for i, line in enumerate(lines):
                        if title in line and i + 1 < len(lines):
                            potential_company = lines[i + 1].strip()
                            if potential_company and len(potential_company) > 2:
                                company = potential_company
                                break
                except:
                    pass
            
            # === EXTRACT LOCATION ===
            location_selectors = [
                '[data-automation="jobCardLocation"]',
                '[data-testid="job-location"]',
                '.job-location',
                '[class*="location"]',
                'span[class*="Location"]'
            ]
            location = ""
            for selector in location_selectors:
                elem = await card.query_selector(selector)
                if elem:
                    location = await elem.inner_text()
                    if location:
                        break
            
            location = location.strip() if location else LOCATION_FILTER
            
            # === EXTRACT SALARY ===
            salary_selectors = [
                '[data-automation="jobCardSalary"]',
                '[data-testid="salary-info"]',
                '.salary-info',
                '[class*="salary"]',
                'span[class*="Salary"]',
                'div[class*="Salary"]'
            ]
            salary = ""
            for selector in salary_selectors:
                elem = await card.query_selector(selector)
                if elem:
                    salary = await elem.inner_text()
                    if salary:
                        break
            
            salary = salary.strip() if salary else "Informasi tidak tersedia"
            
            # Jika salary kosong, cari pattern angka dalam text
            if not salary or salary == "Informasi tidak tersedia":
                try:
                    all_text = await card.inner_text()
                    import re
                    # Cari pattern Rupiah
                    rupiah_pattern = r'Rp\s*[\d,.]+(?:\s*-\s*Rp\s*[\d,.]+)?|[\d,.]+\s*Ribu|[\d,.]+\s*Juta'
                    matches = re.findall(rupiah_pattern, all_text, re.IGNORECASE)
                    if matches:
                        salary = matches[0]
                except:
                    pass
            
            # === EXTRACT LINK ===
            link = ""
            link_selectors = [
                'a[data-automation="jobCardTitle"]',
                'a[href*="/job/"]',
                'a.job-card-link'
            ]
            for selector in link_selectors:
                elem = await card.query_selector(selector)
                if elem:
                    href = await elem.get_attribute('href')
                    if href:
                        if href.startswith('/'):
                            link = f"https://id.jobstreet.com{href}"
                        elif href.startswith('http'):
                            link = href
                        break
            
            # Bersihkan data
            title = title.strip()
            company = company.strip() if company else "Perusahaan tidak disebutkan"
            location = location.strip() if location else LOCATION_FILTER
            salary = salary.strip() if salary else "Informasi tidak tersedia"
            
            if DEBUG:
                preview_title = title[:60] + "..." if len(title) > 60 else title
                preview_company = company[:40] + "..." if len(company) > 40 else company
                logger.debug(f"  [{idx+1}] ✓ {preview_title} | {preview_company} | {salary}")
            
            return {
                "Judul": title,
                "Perusahaan": company,
                "Lokasi": location,
                "Gaji": salary,
                "Link": link,
                "Sumber": "jobstreet.com"
            }
            
        except Exception as e:
            if DEBUG:
                logger.debug(f"  ⚠ Error extracting job data: {e}")
            return None

    async def check_has_next_page(self, current_page: int) -> bool:
        """Cek apakah masih ada halaman berikutnya"""
        try:
            # Method 1: Cek tombol Next
            next_selectors = [
                'a[rel="next"]',
                'button:has-text("Next")',
                'a:has-text("Berikutnya")',
                '[class*="next"] a',
                '.pagination-next a',
                'li.next a'
            ]
            
            for selector in next_selectors:
                next_btn = await self.page.query_selector(selector)
                if next_btn:
                    is_disabled = await next_btn.get_attribute('disabled')
                    if not is_disabled:
                        return True
            
            # Method 2: Cek pagination numbers
            page_numbers = await self.page.query_selector_all('.pagination button, .pagination a')
            if page_numbers:
                for btn in page_numbers:
                    text = await btn.inner_text()
                    try:
                        num = int(text.strip())
                        if num > current_page:
                            return True
                    except:
                        continue
            
            # Method 3: Coba akses halaman berikutnya langsung
            test_url = self.build_search_url(current_page + 1)
            await self.page.goto(test_url, wait_until="networkidle", timeout=30000)
            await self.page.wait_for_timeout(3000)
            
            # Cek apakah ada job cards di halaman berikutnya
            test_cards = await self.page.query_selector_all('[data-automation-id="jobCard"]')
            has_jobs = len(test_cards) > 0
            
            # Kembali ke halaman sebelumnya
            back_url = self.build_search_url(current_page)
            await self.page.goto(back_url, wait_until="networkidle", timeout=30000)
            await self.page.wait_for_timeout(2000)
            
            return has_jobs
            
        except Exception as e:
            logger.debug(f"Error checking next page: {e}")
            return False


async def run_scraper():
    scraper = JobScraper(headless=HEADLESS)
    await scraper.start()
    
    all_jobs = []
    page_count = 0
    seen_links = set()  # Untuk menghindari duplikasi
    
    try:
        while True:
            page_count += 1
            
            logger.info(f"\n{'='*60}")
            logger.info(f"🔄 Memproses Halaman {page_count} dari maksimal {MAX_PAGES}")
            logger.info(f"📊 Total jobs saat ini: {len(all_jobs)} dari target {MAX_JOBS}")
            logger.info(f"{'='*60}")
            
            # Scrape halaman saat ini
            jobs = await scraper.scrape_page(page_count)
            
            # Filter duplikat berdasarkan link
            new_jobs = []
            for job in jobs:
                link = job.get("Link", "")
                if link and link not in seen_links:
                    seen_links.add(link)
                    new_jobs.append(job)
                elif not link:
                    # Jobs tanpa link tetap ditambahkan (mungkin valid)
                    new_jobs.append(job)
            
            if new_jobs:
                all_jobs.extend(new_jobs)
                logger.info(f"✨ Ditambahkan {len(new_jobs)} jobs baru (total: {len(all_jobs)})")
            
            # Cek batas
            if page_count >= MAX_PAGES:
                logger.info(f"🎯 Batas halaman ({MAX_PAGES}) tercapai.")
                break
            
            if len(all_jobs) >= MAX_JOBS:
                logger.info(f"🎯 Target jumlah jobs ({MAX_JOBS}) tercapai.")
                break
            
            if not jobs or not new_jobs:
                logger.info("🏁 Tidak ada data baru atau akhir dari pagination.")
                # Beri kesempatan 1 halaman lagi untuk memastikan
                if page_count > 1:
                    break
            
            # Cek apakah masih ada halaman berikutnya
            has_next = await scraper.check_has_next_page(page_count)
            if not has_next:
                logger.info("🔚 Tidak ada halaman berikutnya.")
                break
            
            # Delay anti-ban dengan randomization
            delay = random.uniform(2.0, 4.0)
            logger.info(f"⏳ Delay {delay:.1f} detik...")
            await asyncio.sleep(delay)
            
    except KeyboardInterrupt:
        logger.warning("⛔ Proses dihentikan oleh pengguna.")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        import traceback
        logger.error(traceback.format_exc())
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
            fieldnames = ["Judul", "Perusahaan", "Lokasi", "Gaji", "Link", "Sumber"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)
        
        logger.success(f"\n✅ BERHASIL! Menyimpan {len(jobs)} data ke '{filename}'")
        
        print(f"\n{'='*60}")
        print(f"📈 RINGKASAN HASIL SCRAPING")
        print(f"{'='*60}")
        print(f"   Total data: {len(jobs)} lowongan")
        print(f"   File: {filename}")
        print(f"   Keyword: {KEYWORD}")
        print(f"   Lokasi: {LOCATION_FILTER}")
        print(f"{'='*60}")
        
        # Tampilkan sample data
        if jobs:
            print(f"\n📋 SAMPLE DATA (5 pertama):")
            print(f"{'-'*60}")
            for i, job in enumerate(jobs[:5], 1):
                print(f"\n{i}. {job['Judul']}")
                print(f"   Perusahaan: {job['Perusahaan']}")
                print(f"   Lokasi: {job['Lokasi']}")
                print(f"   Gaji: {job['Gaji']}")
                print(f"   Link: {job['Link'][:80]}...")
            
            # Statistik gaji
            jobs_with_salary = [j for j in jobs if j['Gaji'] != "Informasi tidak tersedia"]
            print(f"\n💰 STATISTIK GAJI:")
            print(f"   Jobs dengan info gaji: {len(jobs_with_salary)}/{len(jobs)} ({len(jobs_with_salary)*100//len(jobs)}%)")
            
            # Statistik perusahaan
            companies = set(j['Perusahaan'] for j in jobs if j['Perusahaan'] != "Perusahaan tidak disebutkan")
            print(f"\n🏢 STATISTIK PERUSAHAAN:")
            print(f"   Perusahaan unik: {len(companies)}")
        
        print(f"\n{'='*60}\n")
        
    except Exception as e:
        logger.error(f"❌ Gagal menyimpan CSV: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    print("="*60)
    print("🚀 JOBSTREET SCRAPER - VERSI IMPROVED TOTAL")
    print("="*60)
    print(f"   📝 Keyword: {KEYWORD}")
    print(f"   📍 Lokasi: {LOCATION_FILTER}")
    print(f"   📄 Max Halaman: {MAX_PAGES}")
    print(f"   🎯 Target Jobs: {MAX_JOBS}")
    print(f"   👁️ Headless: {HEADLESS}")
    print(f"   🐛 Debug: {DEBUG}")
    print("="*60)
    
    # Fix untuk Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(run_scraper())
