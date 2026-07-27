"""
🚀 Selenium Max Scraper - JobStreet Indonesia
Scraping maksimal tanpa batasan dengan Selenium + Chromium
Memastikan data Gaji dan Nama Perusahaan selalu ada
"""

import csv
import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from fake_useragent import UserAgent
from urllib.parse import quote_plus
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

CONFIG = {
    'max_pages': 0,
    'headless': False,
    'explicit_wait': 20,
    'scroll_pause': 3,
    'retry_attempts': 3,
    'ensure_salary_company': True,
}

SELECTORS = {
    'job_card': 'article[data-automation="jobCard"], div[data-automation="jobCard"], .job-card',
    'job_title': 'a[data-automation="jobCardTitle"], h1 a, .job-title a, [data-testid="job-card-title"]',
    'company_name': '[data-automation="jobCardCompany"], .company-name, [data-testid="company-name"]',
    'location': '[data-automation="jobCardLocation"], .location, [data-testid="location"]',
    'salary': '[data-automation="jobCardSalary"], .salary, [data-testid="salary"], .job-salary',
    'next_button': 'a[aria-label="Next Page"], button:contains("Next"), .pagination-next',
}

class JobStreetScraper:
    def __init__(self, config=None):
        self.config = {**CONFIG, **(config or {})}
        self.driver = None
        self.jobs = []
        self.ua = UserAgent()
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={self.ua.random}')
        if self.config['headless']:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        
        for attempt in range(3):
            try:
                # Gunakan webdriver-manager untuk download chromedriver otomatis
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.set_page_load_timeout(60)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                print("✅ WebDriver berhasil diinisialisasi")
                return
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    time.sleep(2)
                else:
                    raise
        
    def scroll_page(self):
        try:
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.config['scroll_pause'])
            self.driver.execute_script("window.scrollTo(0, 0);")
        except: pass
    
    def extract_job_from_card(self, card, index):
        job_data = {
            'No': index, 'Posisi': '-', 'Perusahaan': '-', 'Lokasi': '-',
            'Gaji': '-', 'Tipe Pekerjaan': '-', 'Pengalaman': '-',
            'Pendidikan': '-', 'Tanggal Posting': '-', 'Deskripsi Singkat': '-',
            'Link': '', 'Waktu Scraping': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            title_el = card.find_element(By.CSS_SELECTOR, SELECTORS['job_title'])
            job_data['Posisi'] = title_el.text.strip()
            job_data['Link'] = title_el.get_attribute('href') or ''
        except: pass
        try:
            company_el = card.find_element(By.CSS_SELECTOR, SELECTORS['company_name'])
            job_data['Perusahaan'] = company_el.text.strip()
        except: pass
        try:
            loc_el = card.find_element(By.CSS_SELECTOR, SELECTORS['location'])
            job_data['Lokasi'] = loc_el.text.strip()
        except: pass
        try:
            salary_el = card.find_element(By.CSS_SELECTOR, SELECTORS['salary'])
            job_data['Gaji'] = salary_el.text.strip()
        except: pass
        if not job_data['Perusahaan'] or job_data['Perusahaan'] == '-':
            job_data['Perusahaan'] = 'Perusahaan tidak disebutkan'
        if not job_data['Gaji'] or job_data['Gaji'] == '-':
            job_data['Gaji'] = 'Hubungi perusahaan untuk info gaji'
        return job_data
    
    def scrape_page(self, page_num):
        jobs_on_page = []
        try:
            # Tunggu lebih lama untuk load konten
            time.sleep(3)
            self.scroll_page()
            
            # Coba multiple selectors untuk job cards
            wait = WebDriverWait(self.driver, self.config['explicit_wait'])
            
            job_cards = []
            for selector in SELECTORS['job_card'].split(', '):
                try:
                    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector.strip())))
                    if elements:
                        job_cards = elements
                        break
                except:
                    continue
            
            if not job_cards:
                # Fallback: cari semua elemen yang mirip job card
                try:
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR, 'article, div[class*="job"], div[class*="card"]')
                except:
                    pass
            
            if job_cards:
                print(f"   ✓ Ditemukan {len(job_cards)} lowongan di halaman {page_num}")
                for idx, card in enumerate(job_cards[:30], 1):  # Limit 30 per page untuk menghindari duplikasi
                    try:
                        job_data = self.extract_job_from_card(card, len(self.jobs) + len(jobs_on_page) + 1)
                        # Hanya tambahkan jika ada posisi atau perusahaan
                        if job_data['Posisi'] != '-' or job_data['Perusahaan'] != '-':
                            jobs_on_page.append(job_data)
                    except Exception as e:
                        continue
            else:
                print(f"   ⚠️  Tidak ditemukan job card dengan selector yang ada")
                
        except Exception as e:
            print(f"❌ Error scraping halaman {page_num}: {e}")
            import traceback
            traceback.print_exc()
        return jobs_on_page
    
    def has_next_page(self):
        try:
            next_btn = self.driver.find_element(By.CSS_SELECTOR, SELECTORS['next_button'])
            return next_btn.is_enabled() and next_btn.is_displayed()
        except: return False
    
    def go_to_next_page(self):
        try:
            next_btn = self.driver.find_element(By.CSS_SELECTOR, SELECTORS['next_button'])
            self.driver.execute_script("arguments[0].click();", next_btn)
            print("   ➡️  Pindah ke halaman berikutnya...")
            time.sleep(4)
            return True
        except: return False
    
    def scrape(self, keyword, location):
        print(f"\n{'='*60}")
        print(f"🔍 MENCARI LOWONGAN: {keyword.upper()}")
        print(f"📍 LOKASI: {location.upper()}")
        print(f"{'='*60}\n")
        self.setup_driver()
        page_num = 1
        base_url = f"https://id.jobstreet.com/id/jobs?keyword={quote_plus(keyword)}&location={quote_plus(location)}"
        
        try:
            # Load halaman pertama dulu
            print(f"\n📄 Halaman {page_num}")
            print(f"   🌐 Loading: {base_url}")
            self.driver.get(base_url)
            time.sleep(8)  # Tunggu lebih lama untuk load awal
            
            while True:
                if self.config['max_pages'] > 0 and page_num > self.config['max_pages']:
                    break
                    
                jobs_on_page = self.scrape_page(page_num)
                self.jobs.extend(jobs_on_page)
                
                if not jobs_on_page:
                    print(f"   ⚠️  Tidak ada lowongan di halaman {page_num}, berhenti...")
                    break
                    
                if not self.has_next_page():
                    print(f"   ✅ Halaman terakhir tercapai")
                    break
                    
                self.go_to_next_page()
                page_num += 1
                time.sleep(3)  # Delay antar halaman
                
        except KeyboardInterrupt:
            print("\n🛑 Dibatalkan oleh user.")
        except Exception as e:
            print(f"\n❌ Error saat scraping: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                self.driver.quit()
        return self.jobs
    
    def save_to_csv(self, filename):
        if not self.jobs: return False
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=list(self.jobs[0].keys()))
            writer.writeheader()
            writer.writerows(self.jobs)
        print(f"\n✅ Data tersimpan di: {filename}")
        return True
    
    def display_summary(self):
        if not self.jobs:
            print("\n⚠️ Tidak ada data.")
            return
        print(f"\n✅ Total: {len(self.jobs)} lowongan")
        for i, job in enumerate(self.jobs[:3], 1):
            print(f"\n{i}. {job['Posisi']} - {job['Perusahaan']}")
            print(f"   💰 {job['Gaji']} | 📍 {job['Lokasi']}")

def main():
    print("\n" + "="*60)
    print("🚀 SELENIUM MAX SCRAPER - JOBSTREET")
    print("="*60)
    keyword = input("\n💼 Posisi: ").strip() or "Admin"
    location = input("🏙️  Lokasi: ").strip() or "Jakarta"
    pages = input("📄 Max halaman (Enter=unlimited): ").strip()
    max_pages = int(pages) if pages else 0
    headless = input("👁️  Headless? (y/n): ").strip().lower() == 'y'
    
    config = {'max_pages': max_pages, 'headless': headless, 'ensure_salary_company': True}
    scraper = JobStreetScraper(config)
    results = scraper.scrape(keyword, location)
    scraper.display_summary()
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"loker_selenium_{keyword.replace(' ','_')}_{location.replace(' ','_')}_{timestamp}.csv"
        scraper.save_to_csv(filename)

if __name__ == "__main__":
    main()
