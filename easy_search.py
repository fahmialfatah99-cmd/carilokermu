import asyncio
import csv
import logging
import sys
import os
from typing import List, Dict, Optional
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote

# Setup Logging Sederhana
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class EasyJobScraper:
    def __init__(self, keyword: str, location: str, max_pages: int = 0, show_browser: bool = False):
        self.keyword = keyword
        self.location = location
        self.max_pages = max_pages # 0 = unlimited
        self.show_browser = show_browser
        self.output_file = f"loker_{keyword.lower().replace(' ', '_')}_{location.lower().replace(' ', '_')}.csv".replace(" ", "_")
        self.browser = None
        self.page = None

    async def start(self):
        playwright = await async_playwright().start()
        args = ["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        self.browser = await playwright.chromium.launch(headless=not self.show_browser, args=args)
        context = await self.browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        self.page = await context.new_page()
        await self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    async def close(self):
        if self.browser: await self.browser.close()

    def generate_search_url(self) -> str:
        # Membuat URL pencarian JobStreet umum (bisa disesuaikan provider lain)
        # Format: https://id.jobstreet.com/id/jobs/{keyword}-jobs-in-{location}
        kw_clean = self.keyword.lower().replace(" ", "-")
        loc_clean = self.location.lower().replace(" ", "-").replace(",", "")
        
        # Base URL JobStreet Indonesia
        base = "https://id.jobstreet.com/id/jobs"
        
        # Konstruksi URL sederhana
        # Catatan: Struktur URL JobStreet bisa berubah, ini pola umum
        if self.location:
            return f"{base}/in-{loc_clean}?k={quote(self.keyword)}"
        else:
            return f"{base}/{kw_clean}-jobs?k={quote(self.keyword)}"

    async def scrape_page(self, url: str) -> List[Dict]:
        jobs = []
        try:
            await self.page.goto(url, wait_until="networkidle", timeout=60000)
            await self.page.wait_for_timeout(3000) # Tunggu render
            
            content = await self.page.content()
            soup = BeautifulSoup(content, 'lxml')
            
            # Selector umum (fleksibel)
            cards = soup.select('article, div[data-job-id], li[class*="job"], div[class*="card"]')
            
            # Jika tidak ketemu dengan selector spesifik, coba cari link yang mengandung '/job/'
            if not cards:
                links = soup.select('a[href*="/job/"]')
                for link in links:
                    title = link.get_text(strip=True)
                    if title:
                        jobs.append({
                            "Judul": title,
                            "Perusahaan": "-",
                            "Lokasi": self.location,
                            "Link": urljoin(url, link.get('href', '')),
                            "Sumber": "jobstreet"
                        })
                return jobs

            for card in cards:
                try:
                    title_el = card.select_one('h1, h2, h3, a[class*="title"], span[class*="title"]')
                    comp_el = card.select_one('span[class*="company"], div[class*="company"]')
                    loc_el = card.select_one('span[class*="location"], div[class*="location"]')
                    link_el = card.select_one('a[href]')

                    title = title_el.get_text(strip=True) if title_el else "Tidak ada judul"
                    company = comp_el.get_text(strip=True) if comp_el else "-"
                    loc = loc_el.get_text(strip=True) if loc_el else self.location
                    link = urljoin(url, link_el['href']) if link_el and link_el.get('href') else ""

                    if title and link:
                        jobs.append({
                            "Judul": title,
                            "Perusahaan": company,
                            "Lokasi": loc,
                            "Link": link,
                            "Sumber": "jobstreet"
                        })
                except: continue
            
            logger.info(f"-> Ditemukan {len(jobs)} lowongan di halaman ini.")
        except Exception as e:
            logger.error(f"Gagal scrape halaman: {e}")
        
        return jobs

    async def get_next_url(self) -> Optional[str]:
        try:
            # Coba cari tombol next
            next_btn = await self.page.wait_for_selector('a[rel="next"], .pagination-next a, a:has-text("Berikutnya"), a:has-text("Next")', timeout=5000)
            if next_btn:
                href = await next_btn.get_attribute('href')
                if href: return urljoin(self.page.url, href)
        except: pass
        
        # Fallback manual parse
        content = await self.page.content()
        soup = BeautifulSoup(content, 'lxml')
        next_link = soup.select_one('a[rel="next"]')
        if not next_link:
            for a in soup.select('a'):
                txt = a.get_text(strip=True).lower()
                if 'next' in txt or 'berikutnya' in txt:
                    next_link = a
                    break
        
        if next_link and next_link.get('href'):
            return urljoin(self.page.url, next_link['href'])
        return None

    async def run(self):
        await self.start()
        all_jobs = []
        current_url = self.generate_search_url()
        page_count = 0
        
        print(f"\n🔍 Mulai mencari: '{self.keyword}' di '{self.location}'")
        if self.max_pages == 0:
            print("⚠️  Mode: TANPA BATAS HALAMAN (Akan berhenti otomatis jika data habis)")
        else:
            print(f"⚠️  Mode: Maksimal {self.max_pages} halaman")
        print("-" * 50)

        try:
            while True:
                page_count += 1
                logger.info(f"📄 Halaman {page_count}: {current_url[:50]}...")
                
                jobs = await self.scrape_page(current_url)
                if not jobs:
                    print("ℹ️  Tidak ada data lagi atau selesai.")
                    break
                
                all_jobs.extend(jobs)
                
                if self.max_pages > 0 and page_count >= self.max_pages:
                    print(f"🛑 Batas {self.max_pages} halaman tercapai.")
                    break
                
                next_url = await self.get_next_url()
                if not next_url:
                    print("🏁 Akhir dari daftar halaman.")
                    break
                
                current_url = next_url
                await asyncio.sleep(2) # Delay sopan

        except KeyboardInterrupt:
            print("\n⚠️  Dihentikan pengguna.")
        finally:
            await self.close()
            self.save(all_jobs)

    def save(self, jobs: List[Dict]):
        if not jobs:
            print("❌ Tidak ada data untuk disimpan.")
            return
        
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Judul", "Perusahaan", "Lokasi", "Link", "Sumber"])
                writer.writeheader()
                writer.writerows(jobs)
            print(f"\n✅ SUKSES! Tersimpan {len(jobs)} data ke file: {os.path.abspath(self.output_file)}")
        except Exception as e:
            print(f"❌ Gagal simpan file: {e}")

def main():
    print("=" * 50)
    print("   JOB SCRAPER OTOMATIS (MUDAH)")
    print("=" * 50)
    
    # Input User
    kw = input("1. Posisi/Jabatan yang dicari (cth: Administrasi): ").strip()
    if not kw: kw = "Administrasi"
    
    loc = input("2. Kota/Lokasi (cth: Jakarta Selatan): ").strip()
    if not loc: loc = "Indonesia"
    
    page_input = input("3. Jumlah halaman (Tekan ENTER untuk tanpa batas): ").strip()
    max_p = 0
    if page_input:
        try:
            val = int(page_input)
            if val > 0: max_p = val
        except:
            print("Input tidak valid, menggunakan mode tanpa batas.")
    
    show = input("4. Tampilkan browser? (y/n, default n): ").strip().lower()
    show_browser = True if show == 'y' else False

    # Jalankan
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    scraper = EasyJobScraper(keyword=kw, location=loc, max_pages=max_p, show_browser=show_browser)
    asyncio.run(scraper.run())

if __name__ == "__main__":
    main()
