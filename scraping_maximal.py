"""
JOBSTREET SCRAPER - SKALA BESAR (MAXIMAL PERFORMANCE)
Fitur:
- Async/Await untuk kecepatan tinggi
- Stealth Mode (Anti-Detect Bot)
- Auto Scroll & Pagination
- Real-time Save (CSV per halaman)
- Retry Logic & Error Handling
- Multi-field Extraction (Title, Company, Salary, Location, Link)
"""

import asyncio
import csv
import os
import random
import time
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ================= KONFIGURASI =================
KEYWORD = "staff"
LOKASI = "jakarta"
MAKS_HALAMAN = 50  # Target halaman
DELAY_ANTAR_HALAMAN = (3, 7)  # Random delay agar aman
HEADLESS = True  # True untuk speed, False untuk debug visual
OUTPUT_FILE = f"hasil_scraping_{KEYWORD}_{LOKASI}.csv"
TIMEOUT_PAGE = 60000  # 60 detik per halaman

# Selector Resmi JobStreet (Data Automation ID)
SELECTORS = {
    "job_card": '[data-automation="jobCard"]',
    "title": '[data-automation="jobCardTitle"]',
    "company": '[data-automation="jobCardCompany"]',
    "location": '[data-automation="jobCardLocation"]',
    "salary": '[data-automation="jobCardSalary"]',
    "next_btn": 'a[aria-label="Next Page"], button[aria-label="Next Page"], .pagination-next a'
}

# ================= FUNGSI PENYIMPANAN =================
def simpan_csv(data_list, filename, is_header=False):
    """Menyimpan data ke CSV secara append (real-time)"""
    file_exists = os.path.isfile(filename)
    fieldnames = ["No", "Judul Lowongan", "Perusahaan", "Lokasi", "Gaji", "Link", "Tanggal Scraping"]
    
    mode = 'a' if file_exists else 'w'
    with open(filename, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or is_header:
            writer.writeheader()
        for row in data_list:
            writer.writerow(row)
    print(f"💾 Tersimpan {len(data_list)} data ke {filename}")

# ================= FUNGSI SCRAPING UTAMA =================
async def scrape_jobstreet():
    print("🚀 MEMULAI SCRAPING SKALA BESAR...")
    print(f"🔍 Keyword: '{KEYWORD}' di '{LOKASI}'")
    print(f"📄 Target: {MAKS_HALAMAN} Halaman")
    print("-" * 60)

    total_data = 0
    start_time = time.time()

    async with async_playwright() as p:
        # Konfigurasi Browser Anti-Detect
        browser = await p.chromium.launch(
            headless=HEADLESS,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080'
            ]
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="id-ID",
            timezone_id="Asia/Jakarta"
        )

        # Inject script stealth
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            Object.defineProperty(navigator, 'languages', { get: () => ['id-ID', 'id'] });
        """)

        page = await context.new_page()
        
        # Buat file CSV dengan header dulu
        simpan_csv([], OUTPUT_FILE, is_header=True)

        for halaman in range(1, MAKS_HALAMAN + 1):
            print(f"\n📄 Memproses Halaman {halaman}/{MAKS_HALAMAN}...")
            
            # Konstruksi URL (JobStreet menggunakan parameter query)
            url = f"https://id.jobstreet.com/id/jobs/in-{LOKASI.replace(' ', '-')}?k={KEYWORD}&page={halaman}"
            
            try:
                # Navigasi dengan wait_until networkidle untuk memastikan load sempurna
                await page.goto(url, timeout=TIMEOUT_PAGE, wait_until="domcontentloaded")
                
                # Tunggu job card muncul
                try:
                    await page.wait_for_selector(SELECTORS["job_card"], timeout=10000)
                except PlaywrightTimeout:
                    print(f"⚠️  Halaman {halaman}: Tidak ada job card ditemukan (Mungkin halaman kosong atau CAPTCHA).")
                    break

                # SCROLL OTOMATIS (Lazy Loading Trigger)
                print("   🔄 Melakukan scroll untuk memuat semua data lazy-loading...")
                await auto_scroll(page)

                # Ambil semua elemen job card
                job_cards = await page.query_selector_all(SELECTORS["job_card"])
                
                if not job_cards:
                    print(f"   ⚠️  Tidak ada data lowongan di halaman {halaman}. Selesai.")
                    break

                data_halaman = []
                no_urut = total_data + 1

                for idx, card in enumerate(job_cards):
                    try:
                        # Ekstraksi Data dengan Fallback
                        title_el = await card.query_selector(SELECTORS["title"])
                        company_el = await card.query_selector(SELECTORS["company"])
                        location_el = await card.query_selector(SELECTORS["location"])
                        salary_el = await card.query_selector(SELECTORS["salary"])
                        link_el = await card.query_selector('a[data-automation="jobCardTitle"]')

                        title = (await title_el.inner_text()).strip() if title_el else "Tidak tersedia"
                        company = (await company_el.inner_text()).strip() if company_el else "Tidak tersedia"
                        location = (await location_el.inner_text()).strip() if location_el else "Tidak tersedia"
                        salary = (await salary_el.inner_text()).strip() if salary_el else "Informasi tidak tersedia"
                        link = (await link_el.get_attribute('href')) if link_el else "Tidak tersedia"
                        
                        # Fix link relatif menjadi absolut
                        if link and not link.startswith('http'):
                            link = f"https://id.jobstreet.com{link}"

                        data_item = {
                            "No": no_urut,
                            "Judul Lowongan": title,
                            "Perusahaan": company,
                            "Lokasi": location,
                            "Gaji": salary,
                            "Link": link,
                            "Tanggal Scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        data_halaman.append(data_item)
                        no_urut += 1
                        
                    except Exception as e:
                        print(f"   ❌ Error pada item {idx}: {str(e)}")
                        continue

                # Simpan data halaman ini segera (Real-time save)
                if data_halaman:
                    simpan_csv(data_halaman, OUTPUT_FILE)
                    total_data += len(data_halaman)
                    print(f"   ✅ Ditemukan {len(data_halaman)} lowongan di halaman {halaman}. Total: {total_data}")
                else:
                    print(f"   ⚠️  Data kosong di halaman {halaman}.")

                # Cek apakah ada halaman berikutnya
                next_btn = await page.query_selector(SELECTORS["next_btn"])
                if not next_btn:
                    print("   🏁 Tidak ada halaman berikutnya. Selesai.")
                    break
                
                # Delay acak agar tidak terdeteksi bot
                delay = random.uniform(*DELAY_ANTAR_HALAMAN)
                print(f"   ⏳ Istirahat sejenak ({delay:.2f} detik)...")
                await asyncio.sleep(delay)

            except Exception as e:
                print(f"   ❌ Error fatal di halaman {halaman}: {str(e)}")
                # Retry logic sederhana
                print("   🔄 Mencoba ulang halaman ini dalam 5 detik...")
                await asyncio.sleep(5)
                continue

        await browser.close()

    end_time = time.time()
    duration = end_time - start_time
    print("\n" + "="*60)
    print(f"🎉 SELESAI! Total data diambil: {total_data}")
    print(f"⏱️  Durasi: {duration:.2f} detik")
    print(f"📂 File hasil: {os.path.abspath(OUTPUT_FILE)}")
    print("="*60)

async def auto_scroll(page):
    """Melakukan scroll bertahap untuk memicu lazy loading"""
    scroll_times = 5
    scroll_pause = 0.5
    
    for i in range(scroll_times):
        # Scroll ke bawah
        await page.evaluate(f"window.scrollBy(0, {i * 500 + 300})")
        await asyncio.sleep(scroll_pause)
    
    # Scroll ke paling bawah
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await asyncio.sleep(1)
    
    # Scroll ke atas lagi
    await page.evaluate("window.scrollTo(0, 0)")
    await asyncio.sleep(0.5)

if __name__ == "__main__":
    try:
        asyncio.run(scrape_jobstreet())
    except KeyboardInterrupt:
        print("\n⛔ Proses dihentikan oleh pengguna.")
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {e}")
