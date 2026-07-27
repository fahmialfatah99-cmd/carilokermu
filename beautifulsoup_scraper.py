"""
🚀 BeautifulSoup Max Scraper - JobStreet Indonesia
Scraping maksimal tanpa batasan dengan Requests + BeautifulSoup
Memastikan data Gaji dan Nama Perusahaan selalu ada
TIDAK MEMERLUKAN CHROME/SELENIUM - Lebih ringan dan cepat!
"""

import csv
import os
import time
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from fake_useragent import UserAgent

CONFIG = {
    'max_pages': 0,
    'retry_attempts': 3,
    'timeout': 30,
    'ensure_salary_company': True,
}

HEADERS_TEMPLATE = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
}

class JobStreetScraper:
    def __init__(self, config=None):
        self.config = {**CONFIG, **(config or {})}
        self.jobs = []
        self.ua = UserAgent()
        self.session = requests.Session()
        
    def get_headers(self):
        headers = HEADERS_TEMPLATE.copy()
        headers['User-Agent'] = self.ua.random
        return headers
        
    def fetch_page(self, url, page_num):
        """Fetch halaman dengan retry logic"""
        for attempt in range(self.config['retry_attempts']):
            try:
                response = self.session.get(url, headers=self.get_headers(), timeout=self.config['timeout'])
                response.raise_for_status()
                return response.text
            except Exception as e:
                print(f"   ⚠️  Attempt {attempt + 1} failed: {e}")
                if attempt < self.config['retry_attempts'] - 1:
                    time.sleep(2 * (attempt + 1))
        return None
    
    def parse_job_cards(self, html, page_num):
        """Parse job cards dari HTML"""
        jobs = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Coba berbagai selector untuk job card
        selectors = [
            'article[data-automation="jobCard"]',
            'div[data-automation="jobCard"]',
            '.job-card',
            '[data-testid="job-card"]',
        ]
        
        job_cards = []
        for selector in selectors:
            job_cards = soup.select(selector)
            if job_cards:
                break
        
        # Fallback: cari elemen dengan class yang mengandung 'job' atau 'card'
        if not job_cards:
            all_articles = soup.find_all(['article', 'div'], class_=lambda x: x and ('job' in str(x).lower() or 'card' in str(x).lower()))
            job_cards = all_articles[:30]
        
        if job_cards:
            print(f"   ✓ Ditemukan {len(job_cards)} lowongan di halaman {page_num}")
            
        for idx, card in enumerate(job_cards[:30], 1):
            job_data = self.extract_job_data(card, len(self.jobs) + len(jobs) + 1)
            # Hanya tambahkan jika ada posisi atau perusahaan
            if job_data['Posisi'] != '-' or job_data['Perusahaan'] != '-':
                jobs.append(job_data)
                
        return jobs
    
    def extract_job_data(self, card, index):
        """Extract data dari job card"""
        job_data = {
            'No': index,
            'Posisi': '-',
            'Perusahaan': '-',
            'Lokasi': '-',
            'Gaji': '-',
            'Tipe Pekerjaan': '-',
            'Pengalaman': '-',
            'Pendidikan': '-',
            'Tanggal Posting': '-',
            'Deskripsi Singkat': '-',
            'Link': '',
            'Waktu Scraping': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Extract title dan link
        title_selectors = [
            'a[data-automation="jobCardTitle"]',
            'h1 a',
            '.job-title a',
            '[data-testid="job-card-title"] a',
            'a[href*="/job/"]',
        ]
        
        for selector in title_selectors:
            title_el = card.select_one(selector)
            if title_el:
                job_data['Posisi'] = title_el.get_text(strip=True)
                job_data['Link'] = title_el.get('href', '')
                if job_data['Link'] and not job_data['Link'].startswith('http'):
                    job_data['Link'] = f"https://id.jobstreet.com{job_data['Link']}"
                break
        
        # Extract company
        company_selectors = [
            '[data-automation="jobCardCompany"]',
            '.company-name',
            '[data-testid="company-name"]',
            'span[class*="company"]',
        ]
        
        for selector in company_selectors:
            company_el = card.select_one(selector)
            if company_el:
                job_data['Perusahaan'] = company_el.get_text(strip=True)
                break
        
        # Extract location
        location_selectors = [
            '[data-automation="jobCardLocation"]',
            '.location',
            '[data-testid="location"]',
            'span[class*="location"]',
        ]
        
        for selector in location_selectors:
            loc_el = card.select_one(selector)
            if loc_el:
                job_data['Lokasi'] = loc_el.get_text(strip=True)
                break
        
        # Extract salary
        salary_selectors = [
            '[data-automation="jobCardSalary"]',
            '.salary',
            '[data-testid="salary"]',
            '.job-salary',
            'span[class*="salary"]',
        ]
        
        for selector in salary_selectors:
            salary_el = card.select_one(selector)
            if salary_el:
                job_data['Gaji'] = salary_el.get_text(strip=True)
                break
        
        # Pastikan perusahaan dan gaji ada
        if not job_data['Perusahaan'] or job_data['Perusahaan'] == '-':
            job_data['Perusahaan'] = 'Perusahaan tidak disebutkan'
        if not job_data['Gaji'] or job_data['Gaji'] == '-':
            job_data['Gaji'] = 'Hubungi perusahaan untuk info gaji'
        
        # Extract deskripsi singkat jika ada
        desc_el = card.select_one('.job-description, [data-automation="jobCardDescription"], p[class*="desc"]')
        if desc_el:
            job_data['Deskripsi Singkat'] = desc_el.get_text(strip=True)[:200]
        
        return job_data
    
    def has_next_page(self, html):
        """Cek apakah ada halaman berikutnya"""
        soup = BeautifulSoup(html, 'html.parser')
        next_selectors = [
            'a[aria-label="Next Page"]',
            'a.next',
            '.pagination-next a',
            'a[href*="page="][rel="next"]',
        ]
        
        for selector in next_selectors:
            if soup.select_one(selector):
                return True
        return False
    
    def scrape(self, keyword, location):
        """Main scraping function"""
        print(f"\n{'='*60}")
        print(f"🔍 MENCARI LOWONGAN: {keyword.upper()}")
        print(f"📍 LOKASI: {location.upper()}")
        print(f"{'='*60}\n")
        
        page_num = 1
        base_url = f"https://id.jobstreet.com/id/jobs?keyword={quote_plus(keyword)}&location={quote_plus(location)}"
        
        try:
            while True:
                if self.config['max_pages'] > 0 and page_num > self.config['max_pages']:
                    break
                
                url = base_url
                if page_num > 1:
                    url += f"&page={page_num}"
                
                print(f"\n📄 Halaman {page_num}")
                print(f"   🌐 Loading: {url}")
                
                html = self.fetch_page(url, page_num)
                if not html:
                    print(f"   ❌ Gagal mengambil halaman {page_num}")
                    break
                
                jobs_on_page = self.parse_job_cards(html, page_num)
                self.jobs.extend(jobs_on_page)
                
                if not jobs_on_page:
                    print(f"   ⚠️  Tidak ada lowongan di halaman {page_num}, berhenti...")
                    break
                
                if not self.has_next_page(html):
                    print(f"   ✅ Halaman terakhir tercapai")
                    break
                
                # Random delay untuk menghindari blocking
                delay = random.uniform(2, 4)
                print(f"   ⏱️  Delay {delay:.1f}s...")
                time.sleep(delay)
                
                page_num += 1
                
        except KeyboardInterrupt:
            print("\n🛑 Dibatalkan oleh user.")
        except Exception as e:
            print(f"\n❌ Error saat scraping: {e}")
            import traceback
            traceback.print_exc()
        
        return self.jobs
    
    def save_to_csv(self, filename):
        """Save results to CSV"""
        if not self.jobs:
            return False
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=list(self.jobs[0].keys()))
            writer.writeheader()
            writer.writerows(self.jobs)
        print(f"\n✅ Data tersimpan di: {filename}")
        return True
    
    def display_summary(self):
        """Display summary of results"""
        if not self.jobs:
            print("\n⚠️ Tidak ada data.")
            return
        print(f"\n✅ Total: {len(self.jobs)} lowongan")
        for i, job in enumerate(self.jobs[:3], 1):
            print(f"\n{i}. {job['Posisi']} - {job['Perusahaan']}")
            print(f"   💰 {job['Gaji']} | 📍 {job['Lokasi']}")


def main():
    print("\n" + "="*60)
    print("🚀 BEAUTIFULSOUP MAX SCRAPER - JOBSTREET")
    print("="*60)
    print("💡 TIDAK PERLU CHROME/SELENIUM - Lebih ringan!")
    print("="*60)
    
    keyword = input("\n💼 Posisi: ").strip() or "Admin"
    location = input("🏙️  Lokasi: ").strip() or "Jakarta"
    pages = input("📄 Max halaman (Enter=unlimited): ").strip()
    max_pages = int(pages) if pages else 0
    
    config = {'max_pages': max_pages, 'ensure_salary_company': True}
    scraper = JobStreetScraper(config)
    results = scraper.scrape(keyword, location)
    scraper.display_summary()
    
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"loker_bs4_{keyword.replace(' ','_')}_{location.replace(' ','_')}_{timestamp}.csv"
        scraper.save_to_csv(filename)


if __name__ == "__main__":
    main()
