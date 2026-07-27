import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import csv
import json
import os
import sys
import time
import random
import logging
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import threading
from queue import Queue
import hashlib

# Konfigurasi Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_scraper.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==================== KONFIGURASI GLOBAL ====================
@dataclass
class ScraperConfig:
    """Konfigurasi scraper untuk fleksibilitas maksimal"""
    max_pages: int = 10
    max_jobs_per_page: int = 50
    timeout_page_load: int = 30
    timeout_element: int = 15
    scroll_delay: float = 2.0
    click_delay: float = 1.5
    headless: bool = True
    disable_images: bool = True
    use_proxy: bool = False
    proxy_list: List[str] = None
    rotate_user_agent: bool = True
    max_workers: int = 3  # Untuk multi-threading
    retry_attempts: int = 3
    save_format: str = 'csv'  # csv, json, atau both
    
# Daftar kota populer untuk referensi
CITIES = [
    "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Semarang",
    "Medan", "Denpasar", "Makassar", "Palembang", "Tangerang",
    "Bekasi", "Depok", "Bogor", "Batam", "Balikpapan",
    "Malang", "Solo", "Manado", "Padang", "Pekanbaru",
    "Lampung", "Samarinda", "Banjarmasin", "Pontianak", "Mataram"
]

# Daftar kategori pekerjaan populer
JOB_CATEGORIES = [
    "Administrasi", "Akuntansi", "Customer Service", "Data Entry",
    "Digital Marketing", "Engineering", "Finance", "Graphic Designer",
    "Human Resources", "IT Developer", "IT Support", "Manager",
    "Marketing", "Nurse", "Operator", "Programmer", "Sales",
    "Secretary", "Software Engineer", "Staff", "Supervisor",
    "Teacher", "Telecom", "Warehouse", "Web Developer", "Writer"
]

# User Agent pool untuk rotasi
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

def display_menu():
    """Menampilkan menu pilihan"""
    print("\n" + "="*60)
    print("           🎯 MENU PENCARI LOWONGAN KERJA 🎯")
    print("="*60)
    
    print("\n📋 KOTA POPULER (contoh):")
    print("-"*40)
    for i, city in enumerate(CITIES[:10], 1):
        print(f"   • {city}")
    print(f"   ... dan {len(CITIES)-10} kota lainnya")
    print("\n💡 Ketik nama kota apa saja (misal: Jakarta, Bandung, Surabaya)")
    
    print("\n💼 KATEGORI PEKERJAAN POPULER (contoh):")
    print("-"*40)
    for i, job in enumerate(JOB_CATEGORIES[:10], 1):
        print(f"   • {job}")
    print(f"   ... dan {len(JOB_CATEGORIES)-10} kategori lainnya")
    print("\n💡 Ketik posisi/kata kunci apa saja (misal: Admin, Programmer, Sales)")
    
    print("\n" + "="*60)

def get_city_choice():
    """Mendapatkan pilihan kota dari user dengan input teks"""
    while True:
        city = input("\n🏙️  Masukkan nama kota: ").strip()
        if city:
            return city.title()  # Format title case
        else:
            print("   ❌ Nama kota tidak boleh kosong. Silakan coba lagi.")

def get_job_choice():
    """Mendapatkan pilihan pekerjaan dari user dengan input teks"""
    while True:
        job = input("\n💼 Masukkan posisi/kata kunci: ").strip()
        if job:
            return job.title()  # Format title case
        else:
            print("   ❌ Posisi tidak boleh kosong. Silakan coba lagi.")

def get_search_options():
    """Mendapatkan opsi pencarian tambahan"""
    print("\n⚙️  OPSI PENCARIAN:")
    print("-"*40)
    
    while True:
        pages = input("   Batas jumlah halaman (kosongkan untuk unlimited): ").strip()
        if not pages:
            pages = None  # Unlimited
            break
        try:
            pages = int(pages)
            if pages > 0:
                break
            else:
                print("   ❌ Masukkan angka positif")
        except ValueError:
            print("   ❌ Masukkan angka yang valid")
    
    debug = input("   Lihat browser berjalan? (y/n, default n): ").strip().lower() == 'y'
    
    return pages, debug


@dataclass
class JobData:
    """Data class untuk menyimpan informasi lowongan kerja"""
    no: int
    posisi: str
    perusahaan: str
    lokasi: str
    gaji: str
    tipe_pekerjaan: str
    pengalaman: str
    pendidikan: str
    tanggal_posting: str
    deskripsi_singkat: str
    link: str
    waktu_scraping: str
    page_number: int = 1
    
    def to_dict(self) -> Dict:
        """Convert ke dictionary"""
        return asdict(self)
    
    def to_csv_row(self) -> Dict:
        """Convert ke format CSV row"""
        return {
            'No': self.no,
            'Posisi': self.posisi,
            'Perusahaan': self.perusahaan,
            'Lokasi': self.lokasi,
            'Gaji': self.gaji,
            'Tipe Pekerjaan': self.tipe_pekerjaan,
            'Pengalaman': self.pengalaman,
            'Pendidikan': self.pendidikan,
            'Tanggal Posting': self.tanggal_posting,
            'Deskripsi Singkat': self.deskripsi_singkat,
            'Link': self.link,
            'Waktu Scraping': self.waktu_scraping
        }


class JobStreetScraper:
    """Class utama untuk scraping JobStreet dengan Selenium + Chromium"""
    
    SELECTORS = {
        'job_card': 'article[data-automation-id="jobCard"]',
        'job_title': '[data-automation="jobCardTitle"]',
        'job_company': '[data-automation="jobCardCompany"]',
        'job_location': '[data-automation="jobCardLocation"]',
        'job_salary': '[data-automation="jobCardSalary"]',
        'job_type': '[data-automation="jobCardJobType"]',
        'job_date': '[data-automation="jobCardPostedDate"]',
        'job_description': '[data-automation="jobCardDescription"]',
        'job_experience': '[data-automation="jobCardExperience"]',
        'job_education': '[data-automation="jobCardEducation"]',
        'next_button': '[aria-label="Next Page"]',
        'no_jobs': '[data-automation="noJobsFound"]'
    }
    
    def __init__(self, config: ScraperConfig = None):
        """Initialize scraper dengan konfigurasi"""
        self.config = config or ScraperConfig()
        self.driver = None
        self.jobs_found: List[JobData] = []
        self.ua = UserAgent() if self.config.rotate_user_agent else None
        self._lock = threading.Lock()
        
    def _get_chrome_options(self) -> Options:
        """Konfigurasi Chrome/Chromium options untuk performa maksimal"""
        options = Options()
        
        if self.config.headless:
            options.add_argument('--headless=new')
        
        # Konfigurasi penting untuk Linux/Server
        options.add_argument('--no-sandbox')  # Diperlukan untuk Linux
        options.add_argument('--disable-dev-shm-usage')  # Hindari masalah shared memory
        options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
        options.add_argument('--remote-debugging-port=9222')  # Fix DevToolsActivePort error
        
        # Optimasi untuk scraping skala besar
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Tambahan optimasi resource untuk stabilitas
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-accelerated-2d-canvas')
        options.add_argument('--disable-software-rasterizer')
        
        # Disable images untuk kecepatan
        if self.config.disable_images:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
        
        # Set user agent
        if self.config.rotate_user_agent and self.ua:
            options.add_argument(f'--user-agent={self.ua.random}')
        else:
            options.add_argument(f'--user-agent={random.choice(USER_AGENTS)}')
        
        # Proxy configuration jika ada
        if self.config.use_proxy and self.config.proxy_list:
            proxy = random.choice(self.config.proxy_list)
            options.add_argument(f'--proxy-server={proxy}')
        
        # Window size
        options.add_argument('--window-size=1920,1080')
        
        # Disable notifications
        options.add_argument('--disable-notifications')
        
        # Bahasa
        options.add_argument('--lang=id-ID')
        
        return options
    
    def _create_driver(self) -> webdriver.Chrome:
        """Membuat driver Chrome dengan konfigurasi optimal"""
        options = self._get_chrome_options()
        
        # Gunakan webdriver-manager untuk auto-download chromedriver
        # Gunakan driver_version=None untuk mendapatkan versi yang sesuai dengan browser
        service = Service(ChromeDriverManager(driver_version=None).install())
        
        driver = webdriver.Chrome(service=service, options=options)
        
        # Script untuk bypass detection
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['id-ID', 'id']
                });
            '''
        })
        
        return driver
    
    def _human_like_delay(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """Delay dengan pola seperti manusia"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def _scroll_page(self, driver):
        """Scroll halaman untuk trigger lazy loading"""
        scroll_pause_time = self.config.scroll_delay
        
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content to load
        time.sleep(scroll_pause_time)
        
        # Scroll back up a bit
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
        time.sleep(1)
    
    def _extract_job_from_card(self, card_element, page_num: int) -> Optional[JobData]:
        """Ekstrak data dari satu kartu lowongan"""
        try:
            # Extract title and link
            try:
                title_el = card_element.find_element(By.CSS_SELECTOR, self.SELECTORS['job_title'])
                title = title_el.text.strip()
                link = title_el.get_attribute('href') or ''
            except NoSuchElementException:
                logger.warning("   ⚠️ Tidak menemukan judul lowongan")
                return None
            
            # Extract company
            try:
                company_el = card_element.find_element(By.CSS_SELECTOR, self.SELECTORS['job_company'])
                company = company_el.text.strip()
            except NoSuchElementException:
                company = "Perusahaan tidak disebutkan"
            
            # Extract location
            try:
                loc_el = card_element.find_element(By.CSS_SELECTOR, self.SELECTORS['job_location'])
                location = loc_el.text.strip()
            except NoSuchElementException:
                location = "Tidak ditentukan"
            
            # Extract salary
            try:
                salary_el = card_element.find_element(By.CSS_SELECTOR, self.SELECTORS['job_salary'])
                salary = salary_el.text.strip()
            except NoSuchElementException:
                salary = "Informasi tidak tersedia"
            
            # Extract job type
            try:
                job_type_el = card_element.find_element(By.CSS_SELECTOR, self.SELECTORS['job_type'])
                job_type = job_type_el.text.strip()
            except NoSuchElementException:
                job_type = "Tidak disebutkan"
            
            # Extract posted date
            try:
                date_el = card_element.find_element(By.CSS_SELECTOR, self.SELECTORS['job_date'])
                posted_date = date_el.text.strip()
            except NoSuchElementException:
                posted_date = "Tidak diketahui"
            
            # Extract description
            try:
                desc_el = card_element.find_element(By.CSS_SELECTOR, self.SELECTORS['job_description'])
                description = desc_el.text.strip()
            except NoSuchElementException:
                description = "-"
            
            # Truncate description if too long
            if len(description) > 200:
                description = description[:200] + "..."
            
            # Extract experience
            try:
                exp_el = card_element.find_element(By.CSS_SELECTOR, self.SELECTORS['job_experience'])
                experience = exp_el.text.strip()
            except NoSuchElementException:
                experience = "Tidak ditentukan"
            
            # Extract education
            try:
                edu_el = card_element.find_element(By.CSS_SELECTOR, self.SELECTORS['job_education'])
                education = edu_el.text.strip()
            except NoSuchElementException:
                education = "Tidak ditentukan"
            
            # Create JobData object
            job = JobData(
                no=len(self.jobs_found) + 1,
                posisi=title,
                perusahaan=company,
                lokasi=location,
                gaji=salary,
                tipe_pekerjaan=job_type,
                pengalaman=experience,
                pendidikan=education,
                tanggal_posting=posted_date,
                deskripsi_singkat=description,
                link=f"https://id.jobstreet.com{link}" if link and link.startswith('/') else link,
                waktu_scraping=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                page_number=page_num
            )
            
            return job
            
        except StaleElementReferenceException:
            logger.warning("   ⚠️ Element sudah tidak valid (stale)")
            return None
        except Exception as e:
            logger.error(f"   ❌ Error extracting job: {e}")
            return None
    
    def scrape_page(self, page_num: int) -> List[JobData]:
        """Scrape satu halaman lowongan"""
        jobs_on_page = []
        
        try:
            # Tunggu job cards muncul
            WebDriverWait(self.driver, self.config.timeout_element).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.SELECTORS['job_card']))
            )
            
            # Scroll untuk trigger lazy loading
            self._scroll_page(self.driver)
            self._human_like_delay(1, 2)
            
            # Dapatkan semua job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, self.SELECTORS['job_card'])
            
            if not job_cards:
                logger.warning(f"   ⚠️ Tidak ada job cards ditemukan di halaman {page_num}")
                return jobs_on_page
            
            logger.info(f"   ✓ Ditemukan {len(job_cards)} lowongan di halaman {page_num}")
            
            # Ekstrak setiap job card
            for idx, card in enumerate(job_cards, 1):
                try:
                    job = self._extract_job_from_card(card, page_num)
                    if job:
                        with self._lock:
                            # Cek duplikasi berdasarkan link
                            is_duplicate = any(j.link == job.link for j in self.jobs_found)
                            if not is_duplicate:
                                job.no = len(self.jobs_found) + 1
                                self.jobs_found.append(job)
                                jobs_on_page.append(job)
                except Exception as e:
                    logger.error(f"   ⚠️ Error pada job {idx}: {e}")
                    continue
                    
        except TimeoutException:
            logger.warning(f"   ⚠️ Timeout menunggu job cards di halaman {page_num}")
        except Exception as e:
            logger.error(f"   ❌ Error scraping halaman {page_num}: {e}")
        
        return jobs_on_page
    
    def navigate_to_next_page(self) -> bool:
        """Navigasi ke halaman berikutnya, return True jika berhasil"""
        try:
            # Cari tombol next
            try:
                next_btn = WebDriverWait(self.driver, self.config.timeout_element).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.SELECTORS['next_button']))
                )
                
                # Scroll ke tombol next
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                self._human_like_delay(0.5, 1)
                
                # Klik dengan JavaScript untuk menghindari deteksi
                self.driver.execute_script("arguments[0].click();", next_btn)
                
                # Tunggu halaman baru load
                time.sleep(self.config.click_delay)
                WebDriverWait(self.driver, self.config.timeout_page_load).until(
                    lambda d: d.current_url != d.current_url  # URL berubah atau konten reload
                )
                time.sleep(2)  # Extra wait untuk stabilitas
                
                logger.info("   ➡️  Berhasil pindah ke halaman berikutnya")
                return True
                
            except NoSuchElementException:
                logger.info("   ✅ Halaman terakhir tercapai (tidak ada tombol Next)")
                return False
                
        except Exception as e:
            logger.error(f"   ❌ Error navigasi ke halaman berikutnya: {e}")
            return False
    
    def scrape(self, keyword: str, location: str) -> List[JobData]:
        """
        Fungsi utama scraping dengan retry mechanism
        """
        # Format URL
        search_keyword = keyword.replace(' ', '%20')
        search_location = location.replace(' ', '%20')
        base_url = f"https://id.jobstreet.com/id/jobs?keyword={search_keyword}&location={search_location}"
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🔍 MENCARI LOWONGAN: {keyword.upper()}")
        logger.info(f"📍 LOKASI: {location.upper()}")
        logger.info(f"🌐 URL: {base_url}")
        logger.info(f"{'='*60}")
        
        # Reset jobs found
        self.jobs_found = []
        
        # Buat driver
        self.driver = self._create_driver()
        
        try:
            # Navigate ke halaman pertama
            logger.info("📡 Menghubungkan ke JobStreet...")
            self.driver.get(base_url)
            time.sleep(5)  # Wait initial load
            
            page_num = 1
            
            # Loop halaman
            while True:
                if self.config.max_pages and page_num > self.config.max_pages:
                    logger.info(f"\n✅ Mencapai batas halaman ({self.config.max_pages})")
                    break
                
                logger.info(f"\n📄 Memproses halaman {page_num}...")
                
                # Scrape halaman ini
                jobs_on_page = self.scrape_page(page_num)
                
                if not jobs_on_page and page_num == 1:
                    logger.warning("   ⚠️ Tidak ada lowongan ditemukan sama sekali")
                    break
                
                # Coba ke halaman berikutnya
                if not self.navigate_to_next_page():
                    break
                
                page_num += 1
                
                # Random delay antar halaman untuk menghindari blocking
                self._human_like_delay(2, 4)
                
        except KeyboardInterrupt:
            logger.warning("\n\n🛑 Dibatalkan oleh user")
        except Exception as e:
            logger.error(f"❌ Error selama scraping: {e}", exc_info=True)
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("🔒 Browser ditutup")
        
        return self.jobs_found

def save_csv(data, filename):
    """Simpan data ke file CSV"""
    if not data:
        logger.warning("❌ Tidak ada data untuk disimpan.")
        return False
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"\n✅ Berhasil! Data tersimpan di: {filename}")
        return True
    except Exception as e:
        logger.error(f"❌ Error menyimpan file: {e}")
        return False

def save_json(data: List[JobData], filename: str) -> bool:
    """Simpan data ke file JSON"""
    if not data:
        logger.warning("❌ Tidak ada data untuk disimpan.")
        return False
    
    try:
        json_data = [job.to_dict() for job in data]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        logger.info(f"\n✅ Berhasil! Data JSON tersimpan di: {filename}")
        return True
    except Exception as e:
        logger.error(f"❌ Error menyimpan file JSON: {e}")
        return False

def display_results_summary(jobs: List[JobData]):
    """Menampilkan ringkasan hasil scraping"""
    if not jobs:
        print("\n⚠️  Tidak ada data yang ditemukan.")
        return
    
    print("\n" + "="*60)
    print(f"           📊 RINGKASAN HASIL PENCARIAN")
    print("="*60)
    print(f"\n✅ Total lowongan ditemukan: {len(jobs)}")
    
    # Statistik sederhana
    companies = set(job.perusahaan for job in jobs)
    locations = set(job.lokasi for job in jobs)
    job_types = {}
    
    for job in jobs:
        jt = job.tipe_pekerjaan
        job_types[jt] = job_types.get(jt, 0) + 1
    
    print(f"🏢 Jumlah perusahaan unik: {len(companies)}")
    print(f"📍 Variasi lokasi: {len(locations)}")
    
    if job_types:
        print("\n📋 Tipe Pekerjaan:")
        for jt, count in sorted(job_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {jt}: {count}")
    
    print("\n" + "="*60)
    print("           📝 CONTOH 5 LOWONGAN PERTAMA")
    print("="*60)
    
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n{i}. {job.posisi}")
        print(f"   🏢 Perusahaan: {job.perusahaan}")
        print(f"   📍 Lokasi: {job.lokasi}")
        print(f"   💰 Gaji: {job.gaji}")
        print(f"   📅 Diposting: {job.tanggal_posting}")
        print(f"   🔗 Link: {job.link}")


class MultiKeywordScraper:
    """Class untuk scraping multiple keywords secara paralel"""
    
    def __init__(self, config: ScraperConfig = None):
        self.config = config or ScraperConfig()
        self.all_results: Dict[str, List[JobData]] = {}
    
    def scrape_keyword(self, keyword: str, location: str) -> List[JobData]:
        """Scrape untuk satu keyword"""
        scraper = JobStreetScraper(self.config)
        return scraper.scrape(keyword, location)
    
    def scrape_multiple(self, keywords: List[str], location: str) -> Dict[str, List[JobData]]:
        """Scrape multiple keywords secara berurutan"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🚀 MEMULAI SCRAPING {len(keywords)} KEYWORD")
        logger.info(f"📍 LOKASI: {location}")
        logger.info(f"{'='*60}")
        
        for i, keyword in enumerate(keywords, 1):
            logger.info(f"\n[{i}/{len(keywords)}] Memproses keyword: {keyword}")
            results = self.scrape_keyword(keyword, location)
            self.all_results[keyword] = results
            logger.info(f"✓ Ditemukan {len(results)} lowongan untuk '{keyword}'")
            
            # Delay antar keyword
            time.sleep(random.uniform(3, 6))
        
        return self.all_results
    
    def save_all_results(self, base_filename: str, format: str = 'csv'):
        """Simpan semua hasil scraping"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Gabungkan semua results
        all_jobs = []
        for keyword, jobs in self.all_results.items():
            all_jobs.extend(jobs)
        
        if not all_jobs:
            logger.warning("⚠️ Tidak ada data untuk disimpan")
            return
        
        if format in ['csv', 'both']:
            csv_filename = f"{base_filename}_{timestamp}.csv"
            csv_data = [job.to_csv_row() for job in all_jobs]
            save_csv(csv_data, csv_filename)
        
        if format in ['json', 'both']:
            json_filename = f"{base_filename}_{timestamp}.json"
            save_json(all_jobs, json_filename)


def main():
    """Fungsi utama program"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█     🎯 SISTEM PENCARI LOWONGAN KERJA OTOMATIS 🎯     █")
    print("█" + " "*58 + "█")
    print("█"*60)
    print("\n💡 Menggunakan Selenium + Chromium untuk performa maksimal")
    print("="*60)
    
    # Tampilkan menu
    display_menu()
    
    # Dapatkan pilihan user
    print("\n" + "="*60)
    print("           SILAKAN BUAT SELEKSI ANDA")
    print("="*60)
    
    location = get_city_choice()
    keyword = get_job_choice()
    max_pages, debug = get_search_options()
    
    print("\n" + "="*60)
    print("🚀 MEMULAI PENCARIAN...")
    print("="*60)
    
    # Generate nama file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"loker_{keyword.replace(' ', '_')}_{location.replace(' ', '_')}_{timestamp}.csv"
    
    # Buat konfigurasi
    config = ScraperConfig(
        max_pages=max_pages if max_pages else 10,
        headless=not debug,
        disable_images=True,
        rotate_user_agent=True,
        timeout_page_load=30,
        timeout_element=15
    )
    
    # Jalankan scraping dengan class baru
    try:
        scraper = JobStreetScraper(config)
        results = scraper.scrape(keyword, location)
        
        # Convert ke format CSV
        if results:
            csv_data = [job.to_csv_row() for job in results]
            
            # Tampilkan ringkasan
            display_results_summary(results)
            
            # Simpan ke CSV
            save_csv(csv_data, filename)
            print(f"\n💾 File CSV siap dibuka dengan Excel atau aplikasi spreadsheet lainnya.")
            
            # Opsional: simpan juga ke JSON
            json_filename = filename.replace('.csv', '.json')
            save_json(results, json_filename)
        else:
            print("\n⚠️  Tidak ada data untuk disimpan.")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Dibatalkan oleh user.")
    except Exception as e:
        logger.error(f"\n❌ Terjadi kesalahan: {e}", exc_info=True)
        print("\n💡 Tips: Pastikan Chrome/Chromium dan dependencies sudah terinstall")


if __name__ == "__main__":
    main()
